"""Busca semântica: índice de embeddings (numpy) com cache, métricas de recuperação e limiar.

Uso pela linha de comando::

    python -m alerta_ia.busca indexar            # cria/atualiza o cache do índice
    python -m alerta_ia.busca avaliar            # recall@1, recall@3 e MRR no teste
    python -m alerta_ia.busca calibrar           # varre o limiar no dev e grava limiar.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
from pathlib import Path

import numpy as np

from alerta_ia import config, dados

log = logging.getLogger(__name__)


# ======================================================================
# Funções puras (testáveis sem GPU)
# ======================================================================
def texto_passagem(trecho: dict) -> str:
    """Texto indexado de um trecho (título e seção ajudam a busca)."""
    return f"passage: {trecho['titulo']} - {trecho['secao']}. {trecho['texto']}"


def texto_consulta(pergunta: str) -> str:
    return f"query: {pergunta.strip()}"


def hash_indice(trechos: list[dict], modelo_id: str) -> str:
    """Hash do conteúdo indexado + modelo; muda se qualquer trecho mudar."""
    h = hashlib.sha256(modelo_id.encode("utf-8"))
    for t in trechos:
        h.update(b"\x00" + t["id"].encode("utf-8") + b"\x01" + texto_passagem(t).encode("utf-8"))
    return h.hexdigest()[:16]


def metricas_recuperacao(
    ranqueados: list[list[str]], relevantes: list[list[str]], ks: tuple[int, ...] = (1, 3)
) -> dict:
    """recall@k (fração das perguntas com ao menos um trecho relevante no top-k) e MRR.

    ``ranqueados[i]`` é a lista de ids ordenada por similaridade para a pergunta i;
    ``relevantes[i]`` são os ids do gabarito. Só devem entrar perguntas do tipo ``responde``.
    """
    if len(ranqueados) != len(relevantes):
        raise ValueError("listas de tamanhos diferentes")
    n = len(ranqueados)
    if n == 0:
        return {"n": 0, **{f"recall@{k}": None for k in ks}, "mrr": None}
    acertos = {k: 0 for k in ks}
    soma_rr = 0.0
    for ids, rel in zip(ranqueados, relevantes):
        rel = set(rel)
        posicao = next((i for i, t in enumerate(ids, start=1) if t in rel), None)
        if posicao is not None:
            soma_rr += 1.0 / posicao
            for k in ks:
                if posicao <= k:
                    acertos[k] += 1
    return {"n": n, **{f"recall@{k}": acertos[k] / n for k in ks}, "mrr": soma_rr / n}


def varrer_limiar(
    scores_top1: list[float], tem_resposta: list[bool], limiares: list[float] | None = None
) -> list[dict]:
    """Para cada limiar candidato, mede o portão "similaridade do top-1 >= limiar".

    Positivo = pergunta com resposta na base (``responde``). Um caso passa pelo portão
    quando ``score >= limiar``. Retorna uma linha por limiar com a matriz de confusão,
    sensibilidade, especificidade, precisão, F1 e índice de Youden.
    """
    s = np.asarray(scores_top1, dtype=float)
    y = np.asarray(tem_resposta, dtype=bool)
    if s.size == 0 or y.size != s.size:
        raise ValueError("scores e rótulos devem ter o mesmo tamanho (> 0)")
    if limiares is None:
        inicio = np.floor(s.min() * 100) / 100 - 0.01
        fim = np.ceil(s.max() * 100) / 100 + 0.01
        limiares = np.round(np.arange(inicio, fim + 1e-9, 0.0025), 4).tolist()
    n_pos, n_neg = int(y.sum()), int((~y).sum())
    linhas = []
    for lim in limiares:
        passa = s >= lim
        vp = int((passa & y).sum())
        fn = n_pos - vp
        fp = int((passa & ~y).sum())
        vn = n_neg - fp
        sens = vp / n_pos if n_pos else 0.0
        espec = vn / n_neg if n_neg else 0.0
        prec = vp / (vp + fp) if (vp + fp) else 0.0
        f1 = 2 * prec * sens / (prec + sens) if (prec + sens) else 0.0
        linhas.append(
            {
                "limiar": float(lim),
                "vp": vp,
                "fn": fn,
                "fp": fp,
                "vn": vn,
                "sensibilidade": sens,
                "especificidade": espec,
                "precisao": prec,
                "f1": f1,
                "youden": sens + espec - 1,
                # leitura de produto
                "recusa_indevida_pelo_limiar": fn / n_pos if n_pos else 0.0,
                "nao_consta_que_passam": fp / n_neg if n_neg else 0.0,
            }
        )
    return linhas


def escolher_limiar(varredura: list[dict], criterio: str = "youden") -> dict:
    """Escolhe o limiar que maximiza ``criterio`` ("youden" ou "f1").

    Em empate (platô de limiares com o mesmo valor ótimo), escolhe o limiar mediano
    do platô, o que dá margem dos dois lados e torna a escolha determinística.
    """
    if criterio == "recusa_max":
        # Portão conservador: o maior limiar que ainda barra no máximo RECUSA_INDEVIDA_MAX das
        # perguntas com resposta. Recusar uma dúvida real de segurança custa mais do que deixar
        # passar uma pergunta sem resposta, porque a LLM ainda pode recusá-la (segunda barreira).
        aceitos = [l for l in varredura if l["recusa_indevida_pelo_limiar"] <= config.RECUSA_INDEVIDA_MAX]
        return max(aceitos, key=lambda l: l["limiar"]) if aceitos else min(varredura, key=lambda l: l["limiar"])
    if criterio not in {"youden", "f1"}:
        raise ValueError("critério deve ser 'recusa_max', 'youden' ou 'f1'")
    melhor = max(l[criterio] for l in varredura)
    empatados = [l for l in varredura if abs(l[criterio] - melhor) < 1e-12]
    empatados.sort(key=lambda l: l["limiar"])
    return empatados[(len(empatados) - 1) // 2]


def justificativa_limiar(escolhido: dict, varredura: list[dict], criterio: str, n_pos: int, n_neg: int) -> str:
    """Texto com a justificativa numérica da escolha, incluindo a troca nos vizinhos."""

    def pct(x):
        return f"{100 * x:.1f}%"

    lim = escolhido["limiar"]
    abaixo = min(varredura, key=lambda l: abs(l["limiar"] - (lim - 0.02)))
    acima = min(varredura, key=lambda l: abs(l["limiar"] - (lim + 0.02)))
    if criterio == "recusa_max":
        regra = (
            f"como o maior limiar que barra no máximo {pct(config.RECUSA_INDEVIDA_MAX)} das perguntas com "
            f"resposta (índice de Youden nesse ponto = {escolhido['youden']:.3f}). "
        )
    else:
        nome = "índice de Youden (sensibilidade + especificidade - 1)" if criterio == "youden" else "F1"
        regra = f"maximizando o {nome} = {escolhido[criterio]:.3f}. "
    return (
        f"Limiar {lim:.4f} escolhido no conjunto de calibração ({n_pos} perguntas com resposta, "
        f"{n_neg} sem resposta) {regra}"
        f"Nesse ponto, {pct(escolhido['sensibilidade'])} das perguntas com resposta seguem para a LLM "
        f"(recusa indevida causada pelo limiar: {pct(escolhido['recusa_indevida_pelo_limiar'])}) e "
        f"{pct(escolhido['especificidade'])} das perguntas sem resposta são recusadas antes da LLM "
        f"(as outras {pct(escolhido['nao_consta_que_passam'])} dependem da recusa do próprio modelo). "
        f"Troca: com limiar {abaixo['limiar']:.4f} (mais baixo) passariam "
        f"{pct(abaixo['nao_consta_que_passam'])} das sem resposta (mais risco de alucinação) e a recusa "
        f"indevida seria {pct(abaixo['recusa_indevida_pelo_limiar'])}; com {acima['limiar']:.4f} (mais alto) "
        f"a recusa indevida subiria para {pct(acima['recusa_indevida_pelo_limiar'])} e passariam "
        f"{pct(acima['nao_consta_que_passam'])} das sem resposta."
    )


def carregar_limiar(caminho: str | Path | None = None) -> float:
    """Lê o limiar calibrado; sem calibração, usa ``config.LIMIAR_PADRAO`` com aviso."""
    caminho = Path(caminho or config.LIMIAR_JSON)
    if caminho.exists():
        return float(json.loads(caminho.read_text(encoding="utf-8"))["limiar"])
    log.warning("limiar.json não encontrado; usando limiar padrão %.3f", config.LIMIAR_PADRAO)
    return config.LIMIAR_PADRAO


# ======================================================================
# Índice (usa o modelo de embeddings)
# ======================================================================
def resolver_dispositivo(pedido: str = "auto") -> str:
    if pedido != "auto":
        return pedido
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:  # pragma: no cover
        return "cpu"


class Buscador:
    """Índice denso em memória (matriz numpy normalizada) com cache em disco."""

    def __init__(
        self,
        trechos: list[dict] | None = None,
        modelo_id: str | None = None,
        dispositivo: str | None = None,
        dir_cache: str | Path | None = None,
    ):
        self.trechos = trechos if trechos is not None else dados.carregar_trechos()
        self.por_id = {t["id"]: t for t in self.trechos}
        self.ids = [t["id"] for t in self.trechos]
        self.modelo_id = modelo_id or config.MODELO_EMB
        self.dispositivo = resolver_dispositivo(dispositivo or config.DISPOSITIVO_EMB)
        self.dir_cache = Path(dir_cache or config.DIR_INDICE)
        self._modelo = None
        self.matriz = self._carregar_ou_indexar()

    # -- modelo
    @property
    def modelo(self):
        if self._modelo is None:
            from sentence_transformers import SentenceTransformer

            self._modelo = SentenceTransformer(self.modelo_id, device=self.dispositivo)
        return self._modelo

    def _codificar(self, textos: list[str]) -> np.ndarray:
        emb = self.modelo.encode(
            textos, batch_size=32, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False
        )
        return emb.astype(np.float32)

    def _carregar_ou_indexar(self) -> np.ndarray:
        h = hash_indice(self.trechos, self.modelo_id)
        arquivo = self.dir_cache / f"indice_{h}.npz"
        if arquivo.exists():
            pacote = np.load(arquivo, allow_pickle=False)
            if list(pacote["ids"]) == self.ids:
                log.info("índice carregado do cache %s", arquivo.name)
                return pacote["matriz"]
        log.info("indexando %d trechos com %s", len(self.trechos), self.modelo_id)
        matriz = self._codificar([texto_passagem(t) for t in self.trechos])
        self.dir_cache.mkdir(parents=True, exist_ok=True)
        for antigo in self.dir_cache.glob("indice_*.npz"):
            antigo.unlink()
        np.savez(arquivo, matriz=matriz, ids=np.array(self.ids))
        return matriz

    def liberar_modelo(self) -> None:
        """Descarrega o modelo de embeddings (libera VRAM); o índice continua em memória."""
        self._modelo = None
        try:
            import gc

            import torch

            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:  # pragma: no cover
            pass

    # -- consulta
    def similaridades(self, perguntas: list[str]) -> np.ndarray:
        """Matriz (n_perguntas, n_trechos) de similaridade de cosseno."""
        consultas = self._codificar([texto_consulta(p) for p in perguntas])
        return consultas @ self.matriz.T

    def buscar_lote(self, perguntas: list[str], k: int = config.TOP_K) -> list[list[dict]]:
        sims = self.similaridades(perguntas)
        saida = []
        for linha in sims:
            ordem = np.argsort(-linha, kind="stable")[:k]
            saida.append([{**self.trechos[i], "similaridade": float(linha[i])} for i in ordem])
        return saida

    def buscar(self, pergunta: str, k: int = config.TOP_K) -> list[dict]:
        """Top-k trechos (cópias com o campo ``similaridade``), do mais ao menos similar."""
        return self.buscar_lote([pergunta], k)[0]

    def ranquear(self, perguntas: list[str]) -> tuple[list[list[str]], list[float]]:
        """Ranking completo de ids e similaridade do top-1 para cada pergunta."""
        sims = self.similaridades(perguntas)
        ranques, top1 = [], []
        for linha in sims:
            ordem = np.argsort(-linha, kind="stable")
            ranques.append([self.ids[i] for i in ordem])
            top1.append(float(linha[ordem[0]]))
        return ranques, top1


# ======================================================================
# Avaliação e calibração
# ======================================================================
def avaliar_busca(buscador: Buscador, casos: list[dict]) -> dict:
    """recall@1, recall@3 e MRR sobre os casos ``responde``, com o detalhe por caso."""
    responde = [c for c in casos if c["tipo"] == "responde"]
    ranques, top1 = buscador.ranquear([c["pergunta"] for c in responde])
    metricas = metricas_recuperacao(ranques, [c["trechos_relevantes"] for c in responde])
    detalhes = []
    for c, r, s in zip(responde, ranques, top1):
        rel = set(c["trechos_relevantes"])
        pos = next((i for i, t in enumerate(r, start=1) if t in rel), None)
        detalhes.append(
            {"id": c["id"], "categoria": c["categoria"], "top3": r[:3], "relevantes": c["trechos_relevantes"],
             "posicao_primeiro_relevante": pos, "similaridade_top1": s}
        )
    por_categoria = {}
    for cat in sorted({d["categoria"] for d in detalhes}):
        sub = [d for d in detalhes if d["categoria"] == cat]
        por_categoria[cat] = {
            "n": len(sub),
            "recall@1": sum(1 for d in sub if d["posicao_primeiro_relevante"] == 1) / len(sub),
            "recall@3": sum(1 for d in sub if (d["posicao_primeiro_relevante"] or 99) <= 3) / len(sub),
        }
    return {**metricas, "por_categoria": por_categoria, "detalhes": detalhes}


def calibrar_limiar(buscador: Buscador, casos: list[dict], criterio: str = config.CRITERIO_LIMIAR) -> dict:
    """Varre o limiar nos casos (dev) e devolve o pacote que vai para limiar.json."""
    _, top1 = buscador.ranquear([c["pergunta"] for c in casos])
    rotulos = [c["tipo"] == "responde" for c in casos]
    varredura = varrer_limiar(top1, rotulos)
    escolhido = escolher_limiar(varredura, criterio)
    n_pos, n_neg = sum(rotulos), len(rotulos) - sum(rotulos)
    return {
        "limiar": round(escolhido["limiar"], 4),
        "criterio": criterio,
        "modelo_embeddings": buscador.modelo_id,
        "n_responde": n_pos,
        "n_nao_consta": n_neg,
        "no_limiar": escolhido,
        "justificativa": justificativa_limiar(escolhido, varredura, criterio, n_pos, n_neg),
        "scores_top1": [{"id": c["id"], "tipo": c["tipo"], "similaridade_top1": s} for c, s in zip(casos, top1)],
        "varredura": varredura,
    }


def grafico_limiar(pacote: dict, caminho: str | Path) -> None:
    """Salva o gráfico da varredura (sensibilidade, especificidade, critério) e dos scores."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    v = pacote["varredura"]
    x = [l["limiar"] for l in v]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    a1.plot(x, [l["recusa_indevida_pelo_limiar"] for l in v], label="recusa indevida (responde barradas)")
    a1.plot(x, [l["nao_consta_que_passam"] for l in v], label="não consta que passam (risco de alucinação)")
    a1.plot(x, [l["youden"] for l in v], label="índice de Youden", linestyle="--")
    a1.axvline(pacote["limiar"], color="black", linewidth=1)
    a1.set_xlabel("limiar de similaridade do top-1")
    a1.set_title("Varredura do limiar (calibração)")
    a1.legend(fontsize=8)
    pos = [s["similaridade_top1"] for s in pacote["scores_top1"] if s["tipo"] == "responde"]
    neg = [s["similaridade_top1"] for s in pacote["scores_top1"] if s["tipo"] != "responde"]
    a2.hist(pos, bins=20, alpha=0.6, label="responde")
    a2.hist(neg, bins=20, alpha=0.6, label="não consta")
    a2.axvline(pacote["limiar"], color="black", linewidth=1)
    a2.set_xlabel("similaridade do top-1")
    a2.set_title("Distribuição dos scores (dev)")
    a2.legend(fontsize=8)
    fig.tight_layout()
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho, dpi=120)
    plt.close(fig)


def _main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description="Índice, avaliação da busca e calibração do limiar")
    ap.add_argument("acao", choices=["indexar", "avaliar", "calibrar"])
    ap.add_argument("--arquivo", help="JSONL de casos (padrão: teste para avaliar; dev + treino para calibrar)")
    ap.add_argument("--criterio", default=config.CRITERIO_LIMIAR, choices=["recusa_max", "youden", "f1"])
    args = ap.parse_args()

    buscador = Buscador()
    if args.acao == "indexar":
        print(f"Índice pronto: {len(buscador.ids)} trechos, dimensão {buscador.matriz.shape[1]}")
    elif args.acao == "avaliar":
        arquivo = Path(args.arquivo or config.TESTE)
        res = avaliar_busca(buscador, dados.carregar_casos(arquivo))
        res["arquivo"] = arquivo.name
        res["modelo_embeddings"] = buscador.modelo_id
        config.BUSCA_JSON.parent.mkdir(parents=True, exist_ok=True)
        config.BUSCA_JSON.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{arquivo.name}: n={res['n']} recall@1={res['recall@1']:.3f} "
              f"recall@3={res['recall@3']:.3f} MRR={res['mrr']:.3f} -> {config.BUSCA_JSON}")
    else:
        if args.arquivo:
            casos = dados.carregar_casos(Path(args.arquivo))
            origem = Path(args.arquivo).name
        else:
            # Padrão: dev + perguntas de treino (rótulos responde/nao_consta), nunca o teste.
            # Só 30 perguntas de dev dão um limiar instável; com as de treino são 530.
            casos = [{"id": c["id"], "pergunta": c["pergunta"], "tipo": c["tipo"]}
                     for c in dados.carregar_casos(config.DEV)]
            arq_treino = config.DIR_TREINO / "perguntas_treino.jsonl"
            with open(arq_treino, encoding="utf-8") as f:
                casos += [{"id": c["id"], "pergunta": c["pergunta"], "tipo": c["tipo"]}
                          for c in map(json.loads, filter(str.strip, f))]
            origem = f"{config.DEV.name} + {arq_treino.name}"
        pacote = calibrar_limiar(buscador, casos, args.criterio)
        pacote["arquivo"] = origem
        config.LIMIAR_JSON.write_text(json.dumps(pacote, ensure_ascii=False, indent=2), encoding="utf-8")
        grafico_limiar(pacote, config.DIR_GRAFICOS / "limiar_varredura.png")
        print(pacote["justificativa"])
        print(f"-> {config.LIMIAR_JSON}")


if __name__ == "__main__":
    _main()
