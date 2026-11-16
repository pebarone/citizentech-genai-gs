# Candidatos a erros reais

Casos com ao menos uma falha, por configuração. A primeira falha listada é a principal.

## sem_contexto: 42 casos com falha

- recusa indevida: 34
- fato-chave faltando na resposta: 8

### T001 (responde, telefone): recusa indevida

- Falhas: recusa indevida
- Pergunta: Qual o número da Defesa Civil pra ligar se minha casa rachou com a chuva?
- Esperado: Se a chuva causou rachaduras ou outro problema grave na casa, chame a Defesa Civil pelo 199 ou o Corpo de Bombeiros pelo 193.
- Resposta do modelo: Não consta na base. Para ligar, você pode ir até o site da Defesa Civil ou ligar 199. No caso de risco imediato, ligue 193.
- Fontes citadas: -; relevantes: ['CGE-01-003']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não
- Saída bruta: `{"resposta": "Não consta na base. Para ligar, você pode ir até o site da Defesa Civil ou ligar 199. No caso de risco imediato, ligue 193.", "fontes": [], "consta_na_base": false}`

### T002 (responde, niveis_alerta): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: o que significa quando o CGE fala que SP ta em estado de atenção?
- Esperado: No estado de atenção, o CGE considera que as chuvas têm potencial para formar alagamentos (chuva intermitente ou contínua, moderada a forte).
- Resposta do modelo: O CGE (Centro de Gerenciamento de Emergências) em SP avisa que SP está em estado de atenção quando há previsão de chuva forte. Isso não significa que irá ocorrer enchente, mas é um aviso de possíveis problemas.
- Fontes citadas: -; relevantes: ['CGE-01-007']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['alagamento'], ['potencial', 'podem formar', 'pode formar', 'podem causar', 'pode causar', 'risco']]
- Saída bruta: `{"resposta": "O CGE (Centro de Gerenciamento de Emergências) em SP avisa que SP está em estado de atenção quando há previsão de chuva forte. Isso não significa que irá ocorrer enchente, mas é um aviso de possíveis problemas.", "fontes": [], "consta_na_base": false}`

### T003 (responde, niveis_alerta): recusa indevida

- Falhas: recusa indevida
- Pergunta: O que quer dizer estado de alerta do CGE?
- Esperado: O estado de alerta é decretado depois da confirmação do transbordamento de córregos e rios.
- Resposta do modelo: Não consta na base. Estado de alerta do CGE refere-se a um sistema de monitoramento de córregos, mas não há detalhes específicos sobre o que isso significa.
- Fontes citadas: -; relevantes: ['CGE-01-007']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['transbord']]
- Saída bruta: `{"resposta": "Não consta na base. Estado de alerta do CGE refere-se a um sistema de monitoramento de córregos, mas não há detalhes específicos sobre o que isso significa.", "fontes": [], "consta_na_base": false}`

### T004 (responde, agua_detalhe_numerico): recusa indevida

- Falhas: recusa indevida
- Pergunta: Quantas gotas de hipoclorito eu ponho em 1 litro de água pra beber e quanto tempo espero?
- Esperado: Filtre a água, coloque 2 gotas de hipoclorito de sódio a 2,5% para cada litro, misture e espere 30 minutos antes de beber.
- Resposta do modelo: Não consta na base.
- Fontes citadas: -; relevantes: ['MS-01-006', 'MS-03-020']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['2 gotas', 'duas gotas'], ['30 minutos', 'meia hora', '30 min']]
- Saída bruta: `{"resposta": "Não consta na base.", "fontes": [], "consta_na_base": false}`

### T005 (responde, alertas_canais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Como faço pra receber alerta de chuva no celular por SMS?
- Esperado: Envie um SMS para o número 40199 com o CEP da área de interesse.
- Resposta do modelo: Para receber alertas de chuva por SMS, você pode se cadastrar no Alerta Córrego. Entre em contato com a Prefeitura de São Paulo para mais informações.
- Fontes citadas: -; relevantes: ['MIDR-01-001', 'SEMIL-01-010', 'MIDR-02-003']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['40199'], ['cep']]
- Saída bruta: `{"resposta": "Para receber alertas de chuva por SMS, você pode se cadastrar no Alerta Córrego. Entre em contato com a Prefeitura de São Paulo para mais informações.", "fontes": [], "consta_na_base": false}`

### T006 (responde, alertas_canais): recusa indevida

- Falhas: recusa indevida
- Pergunta: dá pra cadastrar mais de um cep no 40199?
- Esperado: Sim. Envie uma mensagem por vez para cada CEP; não há limite para a quantidade de CEPs cadastrados.
- Resposta do modelo: Não consta na base.
- Fontes citadas: -; relevantes: ['SEMIL-01-010']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['uma mensagem por vez', 'um por vez', 'uma por vez', 'um de cada vez', 'uma de cada vez'], ['limite']]
- Saída bruta: `{"resposta": "Não consta na base.", "fontes": [], "consta_na_base": false}`

### T007 (responde, alertas_canais): recusa indevida

- Falhas: recusa indevida
- Pergunta: precisa ter internet pro alerta da defesa civil aparecer na tela do celular?
- Esperado: Não. O Defesa Civil Alerta não depende de pacote de dados e funciona com ou sem Wi-Fi; basta o celular ser compatível e ter cobertura 4G ou 5G.
- Resposta do modelo: Não consta na base.
- Fontes citadas: -; relevantes: ['MIDR-02-004']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['pacote de dados', 'internet', 'wi-fi', 'wifi'], ['4g', '5g']]
- Saída bruta: `{"resposta": "Não consta na base.", "fontes": [], "consta_na_base": false}`

### T008 (responde, alertas_canais): recusa indevida

- Falhas: recusa indevida
- Pergunta: qual o zap da defesa civil pra receber alerta?
- Esperado: Mande um “olá” para o WhatsApp (61) 2034-4611 e siga os passos para cadastrar sua área.
- Resposta do modelo: Não consta na base. Para receber alertas, você pode ligar para 199 (Defesa Civil) ou 193 (Corpo de Bombeiros)
- Fontes citadas: -; relevantes: ['MIDR-01-002', 'MIDR-02-003']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['2034-4611', '20344611', '2034 4611']]
- Saída bruta: `{"resposta": "Não consta na base. Para receber alertas, você pode ligar para 199 (Defesa Civil) ou 193 (Corpo de Bombeiros)", "fontes": [], "consta_na_base": false}`

### T009 (responde, durante_evacuacao): recusa indevida

- Falhas: recusa indevida
- Pergunta: A água tá subindo aqui em casa, o que eu desligo antes de sair?
- Esperado: Antes de sair, desligue a chave geral de eletricidade e feche os registros de gás e de água; feche também portas e janelas.
- Resposta do modelo: Não consta na base. Para verificar, você deve ligar 199.
- Fontes citadas: -; relevantes: ['SEMIL-01-007', 'MCID-01-006']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['chave geral', 'eletricidade', 'energia', 'luz', 'forca'], ['gas']]
- Saída bruta: `{"resposta": "Não consta na base. Para verificar, você deve ligar 199.", "fontes": [], "consta_na_base": false}`

### T010 (responde, alimentos_parafrase): recusa indevida

- Falhas: recusa indevida
- Pergunta: o arroz e o feijão que molhou na enchente dá pra aproveitar se secar?
- Esperado: Não. Qualquer alimento que teve contato com a água da enchente deve ser descartado, mesmo que pareça seco; em caso de dúvida, jogue fora.
- Resposta do modelo: Não consta na base. Não há informações sobre a qualidade do arroz e do feijão após enchentes.
- Fontes citadas: -; relevantes: ['MS-01-008', 'MS-01-005']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['descart', 'jogue fora', 'jogar fora', 'joga fora', 'jogue no lixo']]
- Saída bruta: `{"resposta": "Não consta na base. Não há informações sobre a qualidade do arroz e do feijão após enchentes.", "fontes": [], "consta_na_base": false}`

### T011 (responde, criancas): recusa indevida

- Falhas: recusa indevida
- Pergunta: Meu filho quer brincar na enxurrada, tem problema?
- Esperado: Tem, sim. Crianças podem ser levadas pela correnteza ou pegar doenças graves, como hepatite e leptospirose; não deixe que brinquem nessas águas.
- Resposta do modelo: Não consta na base. Procure informações locais ou consulte a previsão do tempo.
- Fontes citadas: -; relevantes: ['COMDEC-01-005']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['correnteza', 'arrastad', 'levad'], ['leptospirose', 'hepatite', 'doenc']]
- Saída bruta: `{"resposta": "Não consta na base. Procure informações locais ou consulte a previsão do tempo.", "fontes": [], "consta_na_base": false}`

### T012 (responde, deslizamento_sinais): recusa indevida

- Falhas: recusa indevida
- Pergunta: como sei se vai ter deslizamento no morro? quais sinais?
- Esperado: Fique atento a rachaduras ou trincas no chão e nas paredes, árvores, postes ou muros inclinados e água mais barrenta que o normal. Se notar, saia do local e ligue 199 para a Defesa Civil.
- Resposta do modelo: Não consta na base. Para identificar deslizamento, observe movimentos bruscos de terra e árvores. Em caso de risco, ligue 199.
- Fontes citadas: -; relevantes: ['DCSP-01-003', 'MCID-01-004']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['rachadura', 'trinca', 'fenda'], ['inclina', 'torto', 'tort']]
- Saída bruta: `{"resposta": "Não consta na base. Para identificar deslizamento, observe movimentos bruscos de terra e árvores. Em caso de risco, ligue 199.", "fontes": [], "consta_na_base": false}`

### T013 (responde, saude_detalhe_numerico): recusa indevida

- Falhas: recusa indevida
- Pergunta: leptospirose demora quantos dias pra aparecer depois que a pessoa pisou na água?
- Esperado: O período de incubação vai de 1 a 30 dias e normalmente fica entre 7 e 14 dias depois da exposição.
- Resposta do modelo: Não consta na base. Informações sobre o tempo de aparecimento da leptospirose não estão disponíveis na base de dados.
- Fontes citadas: -; relevantes: ['MS-02-001']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['30 dias', '1 a 30', 'um a trinta', '30'], ['7 a 14', '7 e 14', 'sete a quatorze', 'sete e catorze', 'sete e quatorze']]
- Saída bruta: `{"resposta": "Não consta na base. Informações sobre o tempo de aparecimento da leptospirose não estão disponíveis na base de dados.", "fontes": [], "consta_na_base": false}`

### T014 (responde, saude_sintomas): recusa indevida

- Falhas: recusa indevida
- Pergunta: Quais os sintomas da leptospirose?
- Esperado: Na fase inicial: febre, falta de apetite, dor muscular principalmente na panturrilha (batata da perna), dor de cabeça e náuseas ou vômitos.
- Resposta do modelo: Não consta na base. Informações sobre sintomas da leptospirose não estão disponíveis.
- Fontes citadas: -; relevantes: ['MS-02-003', 'COMDEC-01-007']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['febre'], ['panturrilha', 'batata da perna', 'dor muscular', 'dor no corpo']]
- Saída bruta: `{"resposta": "Não consta na base. Informações sobre sintomas da leptospirose não estão disponíveis.", "fontes": [], "consta_na_base": false}`

### T015 (responde, limpeza_detalhe_numerico): recusa indevida

- Falhas: recusa indevida
- Pergunta: quanto de água sanitária pra limpar a caixa dagua depois da enchente
- Esperado: Esvazie e esfregue a caixa, coloque 1 litro de água sanitária (hipoclorito a 2,5%) para cada 1.000 litros de água, deixe agir por duas horas e esvazie.
- Resposta do modelo: Não consta na base. Para limpar a caixa d'água após enchentes, consulte um profissional ou siga orientações específicas fornecidas por órgãos de saúde.
- Fontes citadas: -; relevantes: ['SMSSP-01-006']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['1 litro', 'um litro'], ['1.000', '1000', 'mil litros'], ['duas horas', '2 horas', '2h']]
- Saída bruta: `{"resposta": "Não consta na base. Para limpar a caixa d'água após enchentes, consulte um profissional ou siga orientações específicas fornecidas por órgãos de saúde.", "fontes": [], "consta_na_base": false}`

### T016 (responde, orgaos): recusa indevida

- Falhas: recusa indevida
- Pergunta: o que é o CGE?
- Esperado: O CGE (Centro de Gerenciamento de Emergências) é o órgão da Prefeitura de São Paulo que monitora as condições do tempo na cidade, 24 horas por dia.
- Resposta do modelo: Não consta na base. Consulte o site oficial do CGE (Conselho de Gestão de Emergência) para obter informações.
- Fontes citadas: -; relevantes: ['CGE-01-008']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['prefeitura'], ['monitora', 'meteorolog', 'tempo', 'chuva']]
- Saída bruta: `{"resposta": "Não consta na base. Consulte o site oficial do CGE (Conselho de Gestão de Emergência) para obter informações.", "fontes": [], "consta_na_base": false}`

### T017 (responde, telefone): recusa indevida

- Falhas: recusa indevida
- Pergunta: Tem um telefone pra saber se a rua ta bloqueada por alagamento?
- Esperado: Ligue 156 para a central de atendimento da CET ou consulte o site da CET.
- Resposta do modelo: Não consta na base. Informações sobre bloqueios de ruas por alagamento não estão disponíveis. Em caso de emergência, ligue 199.
- Fontes citadas: -; relevantes: ['CGE-01-002']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['156']]
- Saída bruta: `{"resposta": "Não consta na base. Informações sobre bloqueios de ruas por alagamento não estão disponíveis. Em caso de emergência, ligue 199.", "fontes": [], "consta_na_base": false}`

### T018 (responde, animais): recusa indevida

- Falhas: recusa indevida
- Pergunta: Se eu for pra um abrigo, posso deixar meu cachorro em casa?
- Esperado: Não é recomendado: os animais podem não sobreviver ou se perder. Se o abrigo não aceitar animais, peça a amigos ou familiares para cuidarem deles.
- Resposta do modelo: Não consta na base.
- Fontes citadas: -; relevantes: ['MS-03-016']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['sobreviv', 'perder', 'perca', 'extravi', 'morrer'], ['amigo', 'familia', 'parente']]
- Saída bruta: `{"resposta": "Não consta na base.", "fontes": [], "consta_na_base": false}`

### T019 (responde, transito): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: tô de carro e a rua encheu dagua, passo ou não?
- Esperado: Não atravesse: o carro pode ser arrastado pela água. Se o carro enguiçar, abandone-o.
- Resposta do modelo: Passar pode ser perigoso. Verifique a situação antes de sair.
- Fontes citadas: -; relevantes: ['MCID-01-007', 'MIDR-03-004']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['arrastad', 'levado'], ['nao atravesse', 'nunca atravesse', 'nao passe', 'nao enfrente', 'evite', 'nao tente']]
- Saída bruta: `{"resposta": "Passar pode ser perigoso. Verifique a situação antes de sair.", "fontes": [], "consta_na_base": false}`

### T020 (responde, energia_eletrica): recusa indevida

- Falhas: recusa indevida
- Pergunta: a casa alagou e depois secou, posso ligar a geladeira que molhou?
- Esperado: Não use equipamentos elétricos que foram molhados ou ficaram em local inundado, porque há risco de choque elétrico e curto-circuito.
- Resposta do modelo: Não consta na base. Isso depende do nível da água e segurança. Verifique a situação antes de ligar a geladeira.
- Fontes citadas: -; relevantes: ['COMDEC-01-008', 'MS-03-019']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['choque', 'curto']]
- Saída bruta: `{"resposta": "Não consta na base. Isso depende do nível da água e segurança. Verifique a situação antes de ligar a geladeira.", "fontes": [], "consta_na_base": false}`

### T021 (responde, limpeza): recusa indevida

- Falhas: recusa indevida
- Pergunta: a parede ficou com mofo preto depois da enchente, como limpo?
- Esperado: Lave com água e sabão e desinfete com água sanitária a 2,5% (400 mL num balde com 20 litros de água), deixando agir 30 minutos, com o local bem ventilado.
- Resposta do modelo: Não consta na base.
- Fontes citadas: -; relevantes: ['SMSSP-01-007']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['ventila', 'arejad'], ['agua sanitaria', 'hipoclorito', 'cloro']]
- Saída bruta: `{"resposta": "Não consta na base.", "fontes": [], "consta_na_base": false}`

### T022 (responde, limpeza_seguranca): recusa indevida

- Falhas: recusa indevida
- Pergunta: Posso misturar água sanitária com vinagre pra limpar melhor?
- Esperado: Não. Nunca misture água sanitária com vinagre, ácido muriático ou outros produtos de limpeza, pois podem ser liberados gases prejudiciais à saúde.
- Resposta do modelo: Não consta na base.
- Fontes citadas: -; relevantes: ['SMSSP-01-008']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['gases', 'gas', 'toxic']]
- Saída bruta: `{"resposta": "Não consta na base.", "fontes": [], "consta_na_base": false}`

### T023 (responde, saude_detalhe_numerico): recusa indevida

- Falhas: recusa indevida
- Pergunta: Quando devo ir ao médico por causa de diarreia depois da enchente?
- Esperado: Procure atendimento médico se tiver três ou mais episódios de diarreia em um intervalo de 24 horas.
- Resposta do modelo: Não consta na base.
- Fontes citadas: -; relevantes: ['MS-01-003']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['tres', '3 '], ['24 horas', '24h', 'um dia']]
- Saída bruta: `{"resposta": "Não consta na base.", "fontes": [], "consta_na_base": false}`

### T024 (responde, kit_emergencia): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: o que é bom ter num kit de emergência?
- Esperado: Um kit para 72 horas com dois litros de água potável por pessoa por dia, alimentos não perecíveis, medicamentos de uso contínuo e de emergência e itens de primeiros socorros.
- Resposta do modelo: Um kit básico deve incluir toalhas, garrafas d'água, água sanitária, toalhetes, lenços umedecidos, balão de ar, lanterna, toalhas de microfibra, e lenços de papel.
- Fontes citadas: -; relevantes: ['ABR-01-001', 'MIDR-03-003', 'MS-03-005']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['nao perecive', 'enlatad', 'comida', 'alimento'], ['medicament', 'remedio']]
- Saída bruta: `{"resposta": "Um kit básico deve incluir toalhas, garrafas d'água, água sanitária, toalhetes, lenços umedecidos, balão de ar, lanterna, toalhas de microfibra, e lenços de papel.", "fontes": [], "consta_na_base": false}`

### T025 (responde, kit_detalhe_numerico): recusa indevida

- Falhas: recusa indevida
- Pergunta: quantos litros de agua por pessoa no kit?
- Esperado: Dois litros de água potável por pessoa por dia, para um kit que atenda 72 horas.
- Resposta do modelo: Não consta na base. Informação não disponível no sistema.
- Fontes citadas: -; relevantes: ['ABR-01-001']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['dois litros', '2 litros', '2l', 'seis litros', '6 litros']]
- Saída bruta: `{"resposta": "Não consta na base. Informação não disponível no sistema.", "fontes": [], "consta_na_base": false}`

### T026 (responde, kit_emergencia): recusa indevida

- Falhas: recusa indevida
- Pergunta: o governo mandou montar kit de emergência porque vai ter desastre?
- Esperado: Não. O MIDR esclareceu que o kit é uma medida preventiva e não está ligado a nenhum alerta nacional nem a previsão de interrupção de serviços.
- Resposta do modelo: Não consta na base. O governo não anunciou a montagem de kits de emergência para desastres. Em caso de risco, ligue 199.
- Fontes citadas: -; relevantes: ['MIDR-02-001', 'ABR-01-002']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['prevent', 'prevencao'], ['alerta nacional', 'nao esta relacionad', 'nao tem relacao', 'nao ha alerta', 'nao existe alerta']]
- Saída bruta: `{"resposta": "Não consta na base. O governo não anunciou a montagem de kits de emergência para desastres. Em caso de risco, ligue 199.", "fontes": [], "consta_na_base": false}`

### T027 (responde, direitos_fgts): recusa indevida

- Falhas: recusa indevida
- Pergunta: Como peço o saque do FGTS por causa da enchente?
- Esperado: Pelo aplicativo FGTS: em “Saques”, escolha “Solicitar saque” e depois “Calamidade Pública”, informe o município e envie os documentos.
- Resposta do modelo: Não consta na base. Para sacar FGTS por causa de enchente, consulte o FGTS ou ligue 199.
- Fontes citadas: -; relevantes: ['FGTS-01-002', 'FGTS-01-001']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['aplicativo', 'app'], ['calamidade']]
- Saída bruta: `{"resposta": "Não consta na base. Para sacar FGTS por causa de enchente, consulte o FGTS ou ligue 199.", "fontes": [], "consta_na_base": false}`

### T028 (responde, direitos_fgts): recusa indevida

- Falhas: recusa indevida
- Pergunta: minha cidade decretou calamidade mas não aparece no app do fgts, e agora?
- Esperado: É preciso aguardar a habilitação do município pela prefeitura; só depois ele aparece no aplicativo.
- Resposta do modelo: Não consta na base. A calamidade não está disponível no app do FGTS. Informe a situação à prefeitura ou 199 caso precise de assistência.
- Fontes citadas: -; relevantes: ['FGTS-01-001']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['habilita']]
- Saída bruta: `{"resposta": "Não consta na base. A calamidade não está disponível no app do FGTS. Informe a situação à prefeitura ou 199 caso precise de assistência.", "fontes": [], "consta_na_base": false}`

### T029 (responde, direitos_detalhe_numerico): recusa indevida

- Falhas: recusa indevida
- Pergunta: comprovante de residencia pro saque calamidade pode ser de qualquer data?
- Esperado: Não. O comprovante deve estar em nome do trabalhador e ter sido emitido até 120 dias antes da decretação da calamidade.
- Resposta do modelo: Não consta na base. O documento de residência para calamidade deve ser atualizado com frequência, consulte a lei.
- Fontes citadas: -; relevantes: ['FGTS-01-003']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['120']]
- Saída bruta: `{"resposta": "Não consta na base. O documento de residência para calamidade deve ser atualizado com frequência, consulte a lei.", "fontes": [], "consta_na_base": false}`

### T030 (responde, conceitos): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Qual a diferença de enxurrada pra inundação?
- Esperado: Na inundação, a água transborda de forma gradual, em geral por chuvas prolongadas em áreas de planície. A enxurrada é um escoamento rápido e forte, causado por chuva intensa e concentrada, com subida súbita da água e grande poder destrutivo.
- Resposta do modelo: Enxurrada é um rápido e forte despejo de água, enquanto inundação é a presença constante de água em um local.
- Fontes citadas: -; relevantes: ['MIDR-03-005']
- Trechos recuperados (similaridade): -
- Recusa pelo limiar: não; fatos faltando: [['gradual', 'devagar', 'aos poucos']]
- Saída bruta: `{"resposta": "Enxurrada é um rápido e forte despejo de água, enquanto inundação é a presença constante de água em um local.", "fontes": [], "consta_na_base": false}`

(mais 12 casos em resultados/sem_contexto.jsonl)

## rag: 20 casos com falha

- recusa indevida: 10
- fato-chave faltando na resposta: 7
- busca não trouxe o trecho relevante: 3

### T006 (responde, alertas_canais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: dá pra cadastrar mais de um cep no 40199?
- Esperado: Sim. Envie uma mensagem por vez para cada CEP; não há limite para a quantidade de CEPs cadastrados.
- Resposta do modelo: Sim, basta enviar uma mensagem por vez para cada CEP que deseja cadastrar.
- Fontes citadas: ['SEMIL-01-010']; relevantes: ['SEMIL-01-010']
- Trechos recuperados (similaridade): SEMIL-01-010 (0.851), MIDR-01-001 (0.839), MIDR-01-002 (0.823)
- Recusa pelo limiar: não; fatos faltando: [['limite']]
- Saída bruta: `{"resposta": "Sim, basta enviar uma mensagem por vez para cada CEP que deseja cadastrar.", "fontes": ["SEMIL-01-010"], "consta_na_base": true}`

### T007 (responde, alertas_canais): recusa indevida

- Falhas: recusa indevida
- Pergunta: precisa ter internet pro alerta da defesa civil aparecer na tela do celular?
- Esperado: Não. O Defesa Civil Alerta não depende de pacote de dados e funciona com ou sem Wi-Fi; basta o celular ser compatível e ter cobertura 4G ou 5G.
- Resposta do modelo: Não consta na base. O Defesa Civil Alerta usa a rede de telefonia celular para enviar alertas, não necessitando de internet
- Fontes citadas: ['MIDR-02-004']; relevantes: ['MIDR-02-004']
- Trechos recuperados (similaridade): MIDR-02-004 (0.900), MIDR-02-003 (0.875), MIDR-01-001 (0.866)
- Recusa pelo limiar: não; fatos faltando: [['4g', '5g']]
- Saída bruta: `{"resposta": "Não consta na base. O Defesa Civil Alerta usa a rede de telefonia celular para enviar alertas, não necessitando de internet", "fontes": ["MIDR-02-004"], "consta_na_base": false}`

### T008 (responde, alertas_canais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta, citação errada ou ausente
- Pergunta: qual o zap da defesa civil pra receber alerta?
- Esperado: Mande um “olá” para o WhatsApp (61) 2034-4611 e siga os passos para cadastrar sua área.
- Resposta do modelo: Pode enviar uma mensagem para o número 40199 com o CEP da área de interesse.
- Fontes citadas: ['MIDR-01-001']; relevantes: ['MIDR-01-002', 'MIDR-02-003']
- Trechos recuperados (similaridade): MIDR-01-001 (0.888), MIDR-02-003 (0.887), MIDR-02-004 (0.885)
- Recusa pelo limiar: não; fatos faltando: [['2034-4611', '20344611', '2034 4611']]
- Saída bruta: `{"resposta": "Pode enviar uma mensagem para o número 40199 com o CEP da área de interesse.", "fontes": ["MIDR-01-001"], "consta_na_base": true}`

### T010 (responde, alimentos_parafrase): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: o arroz e o feijão que molhou na enchente dá pra aproveitar se secar?
- Esperado: Não. Qualquer alimento que teve contato com a água da enchente deve ser descartado, mesmo que pareça seco; em caso de dúvida, jogue fora.
- Resposta do modelo: Não consta na base. Não é seguro aproveitar alimentos que entraram em contato com água de enchente, mesmo que pareçam secos.
- Fontes citadas: -; relevantes: ['MS-01-008', 'MS-01-005']
- Trechos recuperados (similaridade): MS-01-008 (0.856), SMSSP-01-004 (0.847), MS-03-020 (0.847)
- Recusa pelo limiar: não; fatos faltando: [['descart', 'jogue fora', 'jogar fora', 'joga fora', 'jogue no lixo']]
- Saída bruta: `{"resposta": "Não consta na base. Não é seguro aproveitar alimentos que entraram em contato com água de enchente, mesmo que pareçam secos.", "fontes": [], "consta_na_base": false}`

### T011 (responde, criancas): busca não trouxe o trecho relevante

- Falhas: busca não trouxe o trecho relevante, recusa indevida, citação errada ou ausente
- Pergunta: Meu filho quer brincar na enxurrada, tem problema?
- Esperado: Tem, sim. Crianças podem ser levadas pela correnteza ou pegar doenças graves, como hepatite e leptospirose; não deixe que brinquem nessas águas.
- Resposta do modelo: Não consta na base. <explique em uma frase e oriente a ligar 199 ou 193 em caso de risco>
- Fontes citadas: -; relevantes: ['COMDEC-01-005']
- Trechos recuperados (similaridade): MCID-01-005 (0.838), MS-03-019 (0.837), SMSSP-01-002 (0.836)
- Recusa pelo limiar: não; fatos faltando: [['correnteza', 'arrastad', 'levad'], ['leptospirose', 'hepatite', 'doenc']]
- Saída bruta: `{"resposta": "Não consta na base. <explique em uma frase e oriente a ligar 199 ou 193 em caso de risco>", "fontes": [], "consta_na_base": false}`

### T017 (responde, telefone): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: Tem um telefone pra saber se a rua ta bloqueada por alagamento?
- Esperado: Ligue 156 para a central de atendimento da CET ou consulte o site da CET.
- Resposta do modelo: Não consta na base. <pergunta> não foi mencionado se há um telefone específico para saber se a rua está bloqueada por alagamento
- Fontes citadas: -; relevantes: ['CGE-01-002']
- Trechos recuperados (similaridade): CGE-01-002 (0.866), MIDR-03-004 (0.858), MIDR-03-001 (0.852)
- Recusa pelo limiar: não; fatos faltando: [['156']]
- Saída bruta: `{"resposta": "Não consta na base. <pergunta> não foi mencionado se há um telefone específico para saber se a rua está bloqueada por alagamento", "fontes": [], "consta_na_base": false}`

### T018 (responde, animais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Se eu for pra um abrigo, posso deixar meu cachorro em casa?
- Esperado: Não é recomendado: os animais podem não sobreviver ou se perder. Se o abrigo não aceitar animais, peça a amigos ou familiares para cuidarem deles.
- Resposta do modelo: Não, não deve deixar o cachorro em casa. Deve seguir as orientações do coordenador do abrigo sobre a acomodação deles.
- Fontes citadas: ['MS-03-016']; relevantes: ['MS-03-016']
- Trechos recuperados (similaridade): MS-03-016 (0.876), MS-03-021 (0.827), MS-03-011 (0.827)
- Recusa pelo limiar: não; fatos faltando: [['sobreviv', 'perder', 'perca', 'extravi', 'morrer'], ['amigo', 'familia', 'parente']]
- Saída bruta: `{"resposta": "Não, não deve deixar o cachorro em casa. Deve seguir as orientações do coordenador do abrigo sobre a acomodação deles.", "fontes": ["MS-03-016"], "consta_na_base": true}`

### T019 (responde, transito): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: tô de carro e a rua encheu dagua, passo ou não?
- Esperado: Não atravesse: o carro pode ser arrastado pela água. Se o carro enguiçar, abandone-o.
- Resposta do modelo: Passar por ruas alagadas de carro é perigoso; dirija com baixa velocidade e acelerado, evite águas de enchente atrás de outro veículo para não bloquear. Se o carro enguiçar, abandone-o.
- Fontes citadas: ['MCID-01-007']; relevantes: ['MCID-01-007', 'MIDR-03-004']
- Trechos recuperados (similaridade): COMDEC-01-006 (0.856), MCID-01-007 (0.851), CGE-01-003 (0.837)
- Recusa pelo limiar: não; fatos faltando: [['arrastad', 'levado']]
- Saída bruta: `{"resposta": "Passar por ruas alagadas de carro é perigoso; dirija com baixa velocidade e acelerado, evite águas de enchente atrás de outro veículo para não bloquear. Se o carro enguiçar, abandone-o.", "fontes": ["MCID-01-007"], "consta_na_base": true}`

### T020 (responde, energia_eletrica): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: a casa alagou e depois secou, posso ligar a geladeira que molhou?
- Esperado: Não use equipamentos elétricos que foram molhados ou ficaram em local inundado, porque há risco de choque elétrico e curto-circuito.
- Resposta do modelo: Não consta na base. Caso a geladeira tenha sido molhada, não use equipamentos elétricos que tenham sido molhados ou que estiveram em locais inundados, pois há risco de choque elétrico e curto-circuito. Lave e desinfete os objetos atingidos pela enchente usando uma mistura de água sanitária e água limpa.
- Fontes citadas: ['MCID-01-005']; relevantes: ['COMDEC-01-008', 'MS-03-019']
- Trechos recuperados (similaridade): MCID-01-005 (0.838), COMDEC-01-008 (0.829), CGE-01-003 (0.824)
- Recusa pelo limiar: não
- Saída bruta: `{"resposta": "Não consta na base. Caso a geladeira tenha sido molhada, não use equipamentos elétricos que tenham sido molhados ou que estiveram em locais inundados, pois há risco de choque elétrico e curto-circuito. Lave e desinfete os objetos atingidos pela enchente usando uma mistura de água sanitária e água limpa.", "fontes": ["MCID-01-005"], "consta_na_base": false}`

### T021 (responde, limpeza): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: a parede ficou com mofo preto depois da enchente, como limpo?
- Esperado: Lave com água e sabão e desinfete com água sanitária a 2,5% (400 mL num balde com 20 litros de água), deixando agir 30 minutos, com o local bem ventilado.
- Resposta do modelo: Lave e desinfete a parede com água e sabão, em seguida, com água sanitária (hipoclorito de sódio a 2,5%) diluída na proporção de 400 mL do produto para um balde com 20 litros de água limpa, deixando agir por 30 minutos. Apareça a um bombeiro se houver risco.
- Fontes citadas: ['SMSSP-01-007']; relevantes: ['SMSSP-01-007']
- Trechos recuperados (similaridade): SMSSP-01-007 (0.886), COMDEC-01-008 (0.857), MS-01-011 (0.857)
- Recusa pelo limiar: não; fatos faltando: [['ventila', 'arejad']]
- Saída bruta: `{"resposta": "Lave e desinfete a parede com água e sabão, em seguida, com água sanitária (hipoclorito de sódio a 2,5%) diluída na proporção de 400 mL do produto para um balde com 20 litros de água limpa, deixando agir por 30 minutos. Apareça a um bombeiro se houver risco.", "fontes": ["SMSSP-01-007"], "consta_na_base": true}`

### T022 (responde, limpeza_seguranca): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: Posso misturar água sanitária com vinagre pra limpar melhor?
- Esperado: Não. Nunca misture água sanitária com vinagre, ácido muriático ou outros produtos de limpeza, pois podem ser liberados gases prejudiciais à saúde.
- Resposta do modelo: Não consta na base. Em caso de dúvidas, consulte um profissional de saúde.
- Fontes citadas: -; relevantes: ['SMSSP-01-008']
- Trechos recuperados (similaridade): SMSSP-01-008 (0.845), MS-01-007 (0.845), SMSSP-01-007 (0.837)
- Recusa pelo limiar: não; fatos faltando: [['gases', 'gas', 'toxic']]
- Saída bruta: `{"resposta": "Não consta na base. Em caso de dúvidas, consulte um profissional de saúde.", "fontes": [], "consta_na_base": false}`

### T025 (responde, kit_detalhe_numerico): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: quantos litros de agua por pessoa no kit?
- Esperado: Dois litros de água potável por pessoa por dia, para um kit que atenda 72 horas.
- Resposta do modelo: Não consta na base. O documento não fornece informações específicas sobre a quantidade de água por pessoa no kit.
- Fontes citadas: -; relevantes: ['ABR-01-001']
- Trechos recuperados (similaridade): ABR-01-001 (0.864), MS-03-010 (0.858), MS-03-005 (0.855)
- Recusa pelo limiar: não; fatos faltando: [['dois litros', '2 litros', '2l', 'seis litros', '6 litros']]
- Saída bruta: `{"resposta": "Não consta na base. O documento não fornece informações específicas sobre a quantidade de água por pessoa no kit.", "fontes": [], "consta_na_base": false}`

### T026 (responde, kit_emergencia): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: o governo mandou montar kit de emergência porque vai ter desastre?
- Esperado: Não. O MIDR esclareceu que o kit é uma medida preventiva e não está ligado a nenhum alerta nacional nem a previsão de interrupção de serviços.
- Resposta do modelo: Não consta na base. O kit de emergência é medida preventiva e não está relacionada a qualquer alerta nacional ou previsão de desastre.
- Fontes citadas: -; relevantes: ['MIDR-02-001', 'ABR-01-002']
- Trechos recuperados (similaridade): MIDR-02-001 (0.883), ABR-01-002 (0.874), ABR-01-001 (0.874)
- Recusa pelo limiar: não
- Saída bruta: `{"resposta": "Não consta na base. O kit de emergência é medida preventiva e não está relacionada a qualquer alerta nacional ou previsão de desastre.", "fontes": [], "consta_na_base": false}`

### T029 (responde, direitos_detalhe_numerico): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: comprovante de residencia pro saque calamidade pode ser de qualquer data?
- Esperado: Não. O comprovante deve estar em nome do trabalhador e ter sido emitido até 120 dias antes da decretação da calamidade.
- Resposta do modelo: Não consta na base. <explique em uma frase e oriente a ligar 199 ou 193 em caso de risco>
- Fontes citadas: -; relevantes: ['FGTS-01-003']
- Trechos recuperados (similaridade): FGTS-01-003 (0.895), FGTS-01-002 (0.866), FGTS-01-001 (0.865)
- Recusa pelo limiar: não; fatos faltando: [['120']]
- Saída bruta: `{"resposta": "Não consta na base. <explique em uma frase e oriente a ligar 199 ou 193 em caso de risco>", "fontes": [], "consta_na_base": false}`

### T030 (responde, conceitos): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Qual a diferença de enxurrada pra inundação?
- Esperado: Na inundação, a água transborda de forma gradual, em geral por chuvas prolongadas em áreas de planície. A enxurrada é um escoamento rápido e forte, causado por chuva intensa e concentrada, com subida súbita da água e grande poder destrutivo.
- Resposta do modelo: Enxurrada é o transbordamento de água de um rio ou canal por causa de chuvas intensas e concentradas, enquanto a inundação é a submersão de áreas fora dos limites normais de um curso de água, em zonas que normalmente não ficam submersas.
- Fontes citadas: ['MIDR-03-005']; relevantes: ['MIDR-03-005']
- Trechos recuperados (similaridade): MIDR-03-005 (0.905), MS-01-002 (0.858), SEMIL-01-002 (0.857)
- Recusa pelo limiar: não; fatos faltando: [['gradual', 'devagar', 'aos poucos'], ['subit', 'brusc', 'rapid', 'alta velocidade', 'de repente']]
- Saída bruta: `{"resposta": "Enxurrada é o transbordamento de água de um rio ou canal por causa de chuvas intensas e concentradas, enquanto a inundação é a submersão de áreas fora dos limites normais de um curso de água, em zonas que normalmente não ficam submersas.", "fontes": ["MIDR-03-005"], "consta_na_base": true}`

### T032 (responde, deslizamento_prevencao): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: Bananeira no morro ajuda a segurar a terra?
- Esperado: Não. Bananeiras e árvores grandes acumulam muita água no solo e podem provocar deslizamentos; o recomendado é plantar grama e capim.
- Resposta do modelo: Não consta na base. Não há indicação de que bananeiras ajudam a segurar a terra no morro, mas a orientação é evitar plantar árvores grandes como bananeira para evitar deslizamentos de terra.
- Fontes citadas: -; relevantes: ['DCSP-01-001']
- Trechos recuperados (similaridade): DCSP-01-001 (0.845), MS-03-003 (0.809), MCID-01-004 (0.808)
- Recusa pelo limiar: não; fatos faltando: [['acumul', 'agua'], ['grama', 'capim']]
- Saída bruta: `{"resposta": "Não consta na base. Não há indicação de que bananeiras ajudam a segurar a terra no morro, mas a orientação é evitar plantar árvores grandes como bananeira para evitar deslizamentos de terra.", "fontes": [], "consta_na_base": false}`

### T035 (responde, idosos_pcd): busca não trouxe o trecho relevante

- Falhas: busca não trouxe o trecho relevante, fato-chave faltando na resposta, citação errada ou ausente
- Pergunta: minha vó mora comigo, o que a gente deve planejar pra enchente?
- Esperado: Montem um plano da família com um mapa do bairro e combinem pontos de encontro para o caso de evacuar a casa. Tenham atenção maior com idosos, que podem ter dificuldade de agilidade e locomoção.
- Resposta do modelo: Manter os bueiros limpos, inspecionar telhado e calhas, e preparar um kit de emergência. Evitar deixar crianças sozinhas e manter objetos de valor em locais altos.
- Fontes citadas: ['MCID-01-005']; relevantes: ['MS-03-004']
- Trechos recuperados (similaridade): COMDEC-01-003 (0.878), COMDEC-01-002 (0.872), MCID-01-005 (0.872)
- Recusa pelo limiar: não; fatos faltando: [['plano'], ['encontro']]
- Saída bruta: `{"resposta": "Manter os bueiros limpos, inspecionar telhado e calhas, e preparar um kit de emergência. Evitar deixar crianças sozinhas e manter objetos de valor em locais altos.", "fontes": ["MCID-01-005"], "consta_na_base": true}`

### T039 (responde, saude): recusa indevida

- Falhas: recusa indevida
- Pergunta: me cortei num entulho limpando a casa, preciso tomar vacina antitetânica?
- Esperado: Verifique a data da sua última dose da vacina contra o tétano e, se necessário, procure um profissional de saúde para avaliar o reforço. Limpe e desinfete o ferimento logo.
- Resposta do modelo: Não consta na base. Se você se ferir durante ou após uma enchente, verifique a data da última dose e, se necessário, procure um profissional de saúde para avaliar o reforço.
- Fontes citadas: ['MS-01-013']; relevantes: ['MS-01-013']
- Trechos recuperados (similaridade): MS-01-013 (0.886), MS-03-011 (0.871), MS-03-007 (0.864)
- Recusa pelo limiar: não
- Saída bruta: `{"resposta": "Não consta na base. Se você se ferir durante ou após uma enchente, verifique a data da última dose e, se necessário, procure um profissional de saúde para avaliar o reforço.", "fontes": ["MS-01-013"], "consta_na_base": false}`

### T041 (responde, saude_mental): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: a enchente afeta a cabeça também? to muito ansioso desde que perdi tudo
- Esperado: Sim, um evento traumático pode causar grave sofrimento. O Ministério da Saúde orienta manter contato com familiares e amigos, compartilhar sentimentos e buscar apoio psicológico se necessário.
- Resposta do modelo: A ansiedade é um sintoma comum após enchentes. Procure atendimento médico se sentir muito ansioso. Lembre-se de buscar ajuda profissional para cuidar tanto do seu bem-estar físico quanto mental.
- Fontes citadas: ['MS-01-004']; relevantes: ['MS-01-004']
- Trechos recuperados (similaridade): MS-01-004 (0.869), MS-01-003 (0.866), SMSSP-01-009 (0.865)
- Recusa pelo limiar: não; fatos faltando: [['familia', 'familiares', 'amigo']]
- Saída bruta: `{"resposta": "A ansiedade é um sintoma comum após enchentes. Procure atendimento médico se sentir muito ansioso. Lembre-se de buscar ajuda profissional para cuidar tanto do seu bem-estar físico quanto mental.", "fontes": ["MS-01-004"], "consta_na_base": true}`

### T042 (responde, agua): busca não trouxe o trecho relevante

- Falhas: busca não trouxe o trecho relevante, recusa indevida, citação errada ou ausente
- Pergunta: depois que voltar a agua da rua, posso beber direto da torneira?
- Esperado: Nas casas sem caixa d'água, quando o abastecimento voltar, deixe a água das torneiras escorrer por alguns minutos para eliminar a água contaminada dos canos.
- Resposta do modelo: Não consta na base. Não é recomendado beber água da torneira imediatamente após enchentes, pois a água pode estar contaminada.
- Fontes citadas: -; relevantes: ['SEMIL-01-009']
- Trechos recuperados (similaridade): MS-03-010 (0.835), MS-03-020 (0.822), SMSSP-01-003 (0.821)
- Recusa pelo limiar: não; fatos faltando: [['escorrer', 'correr'], ['minutos']]
- Saída bruta: `{"resposta": "Não consta na base. Não é recomendado beber água da torneira imediatamente após enchentes, pois a água pode estar contaminada.", "fontes": [], "consta_na_base": false}`

## rag_lora: 20 casos com falha

- fato-chave faltando na resposta: 14
- busca não trouxe o trecho relevante: 3
- recusa indevida: 3

### T006 (responde, alertas_canais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: dá pra cadastrar mais de um cep no 40199?
- Esperado: Sim. Envie uma mensagem por vez para cada CEP; não há limite para a quantidade de CEPs cadastrados.
- Resposta do modelo: Pode. Envie uma mensagem por vez para cada CEP que deseja cadastrar.
- Fontes citadas: ['SEMIL-01-010']; relevantes: ['SEMIL-01-010']
- Trechos recuperados (similaridade): SEMIL-01-010 (0.851), MIDR-01-001 (0.839), MIDR-01-002 (0.823)
- Recusa pelo limiar: não; fatos faltando: [['limite']]
- Saída bruta: `{"resposta": "Pode. Envie uma mensagem por vez para cada CEP que deseja cadastrar.", "fontes": ["SEMIL-01-010"], "consta_na_base": true}`

### T007 (responde, alertas_canais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: precisa ter internet pro alerta da defesa civil aparecer na tela do celular?
- Esperado: Não. O Defesa Civil Alerta não depende de pacote de dados e funciona com ou sem Wi-Fi; basta o celular ser compatível e ter cobertura 4G ou 5G.
- Resposta do modelo: Não. Os alertas aparecem diretamente na tela dos celulares compatíveis localizados em áreas de risco, sem precisar de conexão com a internet.
- Fontes citadas: ['MIDR-02-004', 'MIDR-01-001']; relevantes: ['MIDR-02-004']
- Trechos recuperados (similaridade): MIDR-02-004 (0.900), MIDR-02-003 (0.875), MIDR-01-001 (0.866)
- Recusa pelo limiar: não; fatos faltando: [['4g', '5g']]
- Saída bruta: `{"resposta": "Não. Os alertas aparecem diretamente na tela dos celulares compatíveis localizados em áreas de risco, sem precisar de conexão com a internet.", "fontes": ["MIDR-02-004", "MIDR-01-001"], "consta_na_base": true}`

### T011 (responde, criancas): busca não trouxe o trecho relevante

- Falhas: busca não trouxe o trecho relevante, fato-chave faltando na resposta, citação errada ou ausente
- Pergunta: Meu filho quer brincar na enxurrada, tem problema?
- Esperado: Tem, sim. Crianças podem ser levadas pela correnteza ou pegar doenças graves, como hepatite e leptospirose; não deixe que brinquem nessas águas.
- Resposta do modelo: Não. Não deixe as crianças brincarem nas águas da inundação.
- Fontes citadas: ['MS-03-019']; relevantes: ['COMDEC-01-005']
- Trechos recuperados (similaridade): MCID-01-005 (0.838), MS-03-019 (0.837), SMSSP-01-002 (0.836)
- Recusa pelo limiar: não; fatos faltando: [['correnteza', 'arrastad', 'levad'], ['leptospirose', 'hepatite', 'doenc']]
- Saída bruta: `{"resposta": "Não. Não deixe as crianças brincarem nas águas da inundação.", "fontes": ["MS-03-019"], "consta_na_base": true}`

### T012 (responde, deslizamento_sinais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: como sei se vai ter deslizamento no morro? quais sinais?
- Esperado: Fique atento a rachaduras ou trincas no chão e nas paredes, árvores, postes ou muros inclinados e água mais barrenta que o normal. Se notar, saia do local e ligue 199 para a Defesa Civil.
- Resposta do modelo: Observar rachaduras, trincas ou saliências no chão ou nas paredes, e água mais barrenta que o normal, pode indicar um deslizamento.
- Fontes citadas: ['DCSP-01-003']; relevantes: ['DCSP-01-003', 'MCID-01-004']
- Trechos recuperados (similaridade): DCSP-01-001 (0.879), MCID-01-004 (0.871), DCSP-01-003 (0.866)
- Recusa pelo limiar: não; fatos faltando: [['inclina', 'torto', 'tort'], ['199', 'saia', 'sair']]
- Saída bruta: `{"resposta": "Observar rachaduras, trincas ou saliências no chão ou nas paredes, e água mais barrenta que o normal, pode indicar um deslizamento.", "fontes": ["DCSP-01-003"], "consta_na_base": true}`

### T014 (responde, saude_sintomas): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Quais os sintomas da leptospirose?
- Esperado: Na fase inicial: febre, falta de apetite, dor muscular principalmente na panturrilha (batata da perna), dor de cabeça e náuseas ou vômitos.
- Resposta do modelo: Fevere, falta de apetite, dor muscular (principalmente na panturrilha), dor de cabeça e náuseas ou vômitos. Também podem ocorrer diarreia, dor nas articulações, vermelhidão ou hemorragia nos olhos, sensibilidade à luz, dor nos olhos e tosse.
- Fontes citadas: ['MS-02-003']; relevantes: ['MS-02-003', 'COMDEC-01-007']
- Trechos recuperados (similaridade): MS-02-003 (0.910), MS-02-001 (0.882), MS-02-002 (0.880)
- Recusa pelo limiar: não; fatos faltando: [['febre']]
- Saída bruta: `{"resposta": "Fevere, falta de apetite, dor muscular (principalmente na panturrilha), dor de cabeça e náuseas ou vômitos. Também podem ocorrer diarreia, dor nas articulações, vermelhidão ou hemorragia nos olhos, sensibilidade à luz, dor nos olhos e tosse.", "fontes": ["MS-02-003"], "consta_na_base": true}`

### T018 (responde, animais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Se eu for pra um abrigo, posso deixar meu cachorro em casa?
- Esperado: Não é recomendado: os animais podem não sobreviver ou se perder. Se o abrigo não aceitar animais, peça a amigos ou familiares para cuidarem deles.
- Resposta do modelo: Não. Os animais domésticos podem não sobreviver ou se perder antes que vocês voltem.
- Fontes citadas: ['MS-03-016']; relevantes: ['MS-03-016']
- Trechos recuperados (similaridade): MS-03-016 (0.876), MS-03-021 (0.827), MS-03-011 (0.827)
- Recusa pelo limiar: não; fatos faltando: [['amigo', 'familia', 'parente']]
- Saída bruta: `{"resposta": "Não. Os animais domésticos podem não sobreviver ou se perder antes que vocês voltem.", "fontes": ["MS-03-016"], "consta_na_base": true}`

### T019 (responde, transito): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: tô de carro e a rua encheu dagua, passo ou não?
- Esperado: Não atravesse: o carro pode ser arrastado pela água. Se o carro enguiçar, abandone-o.
- Resposta do modelo: Não. Se precisar atravessar ruas alagadas, use muros e paredes como apoio ou cordas, com ajuda de pelo menos três pessoas.
- Fontes citadas: ['MCID-01-007']; relevantes: ['MCID-01-007', 'MIDR-03-004']
- Trechos recuperados (similaridade): COMDEC-01-006 (0.856), MCID-01-007 (0.851), CGE-01-003 (0.837)
- Recusa pelo limiar: não; fatos faltando: [['arrastad', 'levado'], ['nao atravesse', 'nunca atravesse', 'nao passe', 'nao enfrente', 'evite', 'nao tente']]
- Saída bruta: `{"resposta": "Não. Se precisar atravessar ruas alagadas, use muros e paredes como apoio ou cordas, com ajuda de pelo menos três pessoas.", "fontes": ["MCID-01-007"], "consta_na_base": true}`

### T020 (responde, energia_eletrica): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta, citação errada ou ausente
- Pergunta: a casa alagou e depois secou, posso ligar a geladeira que molhou?
- Esperado: Não use equipamentos elétricos que foram molhados ou ficaram em local inundado, porque há risco de choque elétrico e curto-circuito.
- Resposta do modelo: Não. Mantenha objetos de valor em locais altos e esvazie a geladeira.
- Fontes citadas: ['MCID-01-005']; relevantes: ['COMDEC-01-008', 'MS-03-019']
- Trechos recuperados (similaridade): MCID-01-005 (0.838), COMDEC-01-008 (0.829), CGE-01-003 (0.824)
- Recusa pelo limiar: não; fatos faltando: [['choque', 'curto']]
- Saída bruta: `{"resposta": "Não. Mantenha objetos de valor em locais altos e esvazie a geladeira.", "fontes": ["MCID-01-005"], "consta_na_base": true}`

### T021 (responde, limpeza): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: a parede ficou com mofo preto depois da enchente, como limpo?
- Esperado: Lave com água e sabão e desinfete com água sanitária a 2,5% (400 mL num balde com 20 litros de água), deixando agir 30 minutos, com o local bem ventilado.
- Resposta do modelo: Lave, desinfete e deixe o local bem ventilado.
- Fontes citadas: ['SMSSP-01-007']; relevantes: ['SMSSP-01-007']
- Trechos recuperados (similaridade): SMSSP-01-007 (0.886), COMDEC-01-008 (0.857), MS-01-011 (0.857)
- Recusa pelo limiar: não; fatos faltando: [['agua sanitaria', 'hipoclorito', 'cloro']]
- Saída bruta: `{"resposta": "Lave, desinfete e deixe o local bem ventilado.", "fontes": ["SMSSP-01-007"], "consta_na_base": true}`

### T025 (responde, kit_detalhe_numerico): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: quantos litros de agua por pessoa no kit?
- Esperado: Dois litros de água potável por pessoa por dia, para um kit que atenda 72 horas.
- Resposta do modelo: Não consta na base. Os documentos oficiais que eu uso não trazem essa informação; para isso, procure a prefeitura ou o órgão responsável.
- Fontes citadas: -; relevantes: ['ABR-01-001']
- Trechos recuperados (similaridade): ABR-01-001 (0.864), MS-03-010 (0.858), MS-03-005 (0.855)
- Recusa pelo limiar: não; fatos faltando: [['dois litros', '2 litros', '2l', 'seis litros', '6 litros']]
- Saída bruta: `{"resposta": "Não consta na base. Os documentos oficiais que eu uso não trazem essa informação; para isso, procure a prefeitura ou o órgão responsável.", "fontes": [], "consta_na_base": false}`

### T026 (responde, kit_emergencia): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: o governo mandou montar kit de emergência porque vai ter desastre?
- Esperado: Não. O MIDR esclareceu que o kit é uma medida preventiva e não está ligado a nenhum alerta nacional nem a previsão de interrupção de serviços.
- Resposta do modelo: Não consta na base. Os documentos oficiais que eu uso não trazem essa informação; para isso, procure a prefeitura ou o órgão responsável da sua rua.
- Fontes citadas: -; relevantes: ['MIDR-02-001', 'ABR-01-002']
- Trechos recuperados (similaridade): MIDR-02-001 (0.883), ABR-01-002 (0.874), ABR-01-001 (0.874)
- Recusa pelo limiar: não; fatos faltando: [['prevent', 'prevencao'], ['alerta nacional', 'nao esta relacionad', 'nao tem relacao', 'nao ha alerta', 'nao existe alerta']]
- Saída bruta: `{"resposta": "Não consta na base. Os documentos oficiais que eu uso não trazem essa informação; para isso, procure a prefeitura ou o órgão responsável da sua rua.", "fontes": [], "consta_na_base": false}`

### T029 (responde, direitos_detalhe_numerico): recusa indevida

- Falhas: recusa indevida
- Pergunta: comprovante de residencia pro saque calamidade pode ser de qualquer data?
- Esperado: Não. O comprovante deve estar em nome do trabalhador e ter sido emitido até 120 dias antes da decretação da calamidade.
- Resposta do modelo: Não consta na base. Os documentos exigidos para o saque calamidade são documento de identidade, com foto da frente e do verso, e comprovante de residência em nome do trabalhador, emitido até 120 dias antes da decretação da calamidade.
- Fontes citadas: ['FGTS-01-003']; relevantes: ['FGTS-01-003']
- Trechos recuperados (similaridade): FGTS-01-003 (0.895), FGTS-01-002 (0.866), FGTS-01-001 (0.865)
- Recusa pelo limiar: não
- Saída bruta: `{"resposta": "Não consta na base. Os documentos exigidos para o saque calamidade são documento de identidade, com foto da frente e do verso, e comprovante de residência em nome do trabalhador, emitido até 120 dias antes da decretação da calamidade.", "fontes": ["FGTS-01-003"], "consta_na_base": false}`

### T030 (responde, conceitos): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Qual a diferença de enxurrada pra inundação?
- Esperado: Na inundação, a água transborda de forma gradual, em geral por chuvas prolongadas em áreas de planície. A enxurrada é um escoamento rápido e forte, causado por chuva intensa e concentrada, com subida súbita da água e grande poder destrutivo.
- Resposta do modelo: As enxurradas ocorrem pelo escoamento superficial de alta velocidade e energia, provocado por chuvas intensas e concentradas, em pequenas bacias de relevo acidentado, com elevação súbita das vazões e transbordamento brusco.
- Fontes citadas: ['MIDR-03-005']; relevantes: ['MIDR-03-005']
- Trechos recuperados (similaridade): MIDR-03-005 (0.905), MS-01-002 (0.858), SEMIL-01-002 (0.857)
- Recusa pelo limiar: não; fatos faltando: [['gradual', 'devagar', 'aos poucos']]
- Saída bruta: `{"resposta": "As enxurradas ocorrem pelo escoamento superficial de alta velocidade e energia, provocado por chuvas intensas e concentradas, em pequenas bacias de relevo acidentado, com elevação súbita das vazões e transbordamento brusco.", "fontes": ["MIDR-03-005"], "consta_na_base": true}`

### T031 (responde, deslizamento_prevencao): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Por que não pode jogar a água do tanque no barranco?
- Esperado: Porque umedece a encosta e aumenta o risco de deslizamento, além de contaminar o solo. O ideal é instalar canaletas ou tubos para escoar essa água.
- Resposta do modelo: O lixo jogado nas encostas acumula água, fica mais pesado e, se escorregar, arrasta o solo junto.
- Fontes citadas: ['DCSP-01-002']; relevantes: ['DCSP-01-002']
- Trechos recuperados (similaridade): DCSP-01-002 (0.846), MS-03-019 (0.819), SMSSP-01-001 (0.818)
- Recusa pelo limiar: não; fatos faltando: [['desliz'], ['canaleta', 'tubo', 'cano']]
- Saída bruta: `{"resposta": "O lixo jogado nas encostas acumula água, fica mais pesado e, se escorregar, arrasta o solo junto.", "fontes": ["DCSP-01-002"], "consta_na_base": true}`

### T032 (responde, deslizamento_prevencao): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Bananeira no morro ajuda a segurar a terra?
- Esperado: Não. Bananeiras e árvores grandes acumulam muita água no solo e podem provocar deslizamentos; o recomendado é plantar grama e capim.
- Resposta do modelo: Não. Bananeiras e árvores grandes como manga, mamão e abacate acumulam muita água no solo e podem provocar deslizamentos de terra.
- Fontes citadas: ['DCSP-01-001']; relevantes: ['DCSP-01-001']
- Trechos recuperados (similaridade): DCSP-01-001 (0.845), MS-03-003 (0.809), MCID-01-004 (0.808)
- Recusa pelo limiar: não; fatos faltando: [['grama', 'capim']]
- Saída bruta: `{"resposta": "Não. Bananeiras e árvores grandes como manga, mamão e abacate acumulam muita água no solo e podem provocar deslizamentos de terra.", "fontes": ["DCSP-01-001"], "consta_na_base": true}`

### T035 (responde, idosos_pcd): busca não trouxe o trecho relevante

- Falhas: busca não trouxe o trecho relevante, fato-chave faltando na resposta, citação errada ou ausente
- Pergunta: minha vó mora comigo, o que a gente deve planejar pra enchente?
- Esperado: Montem um plano da família com um mapa do bairro e combinem pontos de encontro para o caso de evacuar a casa. Tenham atenção maior com idosos, que podem ter dificuldade de agilidade e locomoção.
- Resposta do modelo: Elabore um Plano Familiar de Emergência, prepare um kit de emergência e separe documentos importantes. Contate a Defesa Civil (199) ou o BOMBEIROS (193) para instruções.
- Fontes citadas: ['MCID-01-005']; relevantes: ['MS-03-004']
- Trechos recuperados (similaridade): COMDEC-01-003 (0.878), COMDEC-01-002 (0.872), MCID-01-005 (0.872)
- Recusa pelo limiar: não; fatos faltando: [['encontro']]
- Saída bruta: `{"resposta": "Elabore um Plano Familiar de Emergência, prepare um kit de emergência e separe documentos importantes. Contate a Defesa Civil (199) ou o BOMBEIROS (193) para instruções.", "fontes": ["MCID-01-005"], "consta_na_base": true}`

### T037 (responde, saude_parafrase): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Rato faz a lepto chegar até minha casa como?
- Esperado: Na chuva, rios, córregos e esgoto transbordam, invadem as tocas dos ratos e a água chega às casas contaminada pela urina; o contato com essa água ou lama pode transmitir a leptospirose.
- Resposta do modelo: Ratos ficam em galerias, lixões, terrenos baldios e esgotos e, no período chuvoso, a água do rio, do córrego e da rede de esgoto pode transbordar, invadindo as tocas de ratos e chegar contaminada às residências.
- Fontes citadas: ['MS-03-012']; relevantes: ['MS-03-012']
- Trechos recuperados (similaridade): MS-03-012 (0.859), MS-03-013 (0.838), MS-02-006 (0.831)
- Recusa pelo limiar: não; fatos faltando: [['urina', 'xixi']]
- Saída bruta: `{"resposta": "Ratos ficam em galerias, lixões, terrenos baldios e esgotos e, no período chuvoso, a água do rio, do córrego e da rede de esgoto pode transbordar, invadindo as tocas de ratos e chegar contaminada às residências.", "fontes": ["MS-03-012"], "consta_na_base": true}`

### T039 (responde, saude): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: me cortei num entulho limpando a casa, preciso tomar vacina antitetânica?
- Esperado: Verifique a data da sua última dose da vacina contra o tétano e, se necessário, procure um profissional de saúde para avaliar o reforço. Limpe e desinfete o ferimento logo.
- Resposta do modelo: Precisa. Se tiver ferida aberta, use calçados e luvas ao caminhar em áreas inundadas ou com lama e evite manusear terra ou objetos sujos.
- Fontes citadas: ['MS-01-013']; relevantes: ['MS-01-013']
- Trechos recuperados (similaridade): MS-01-013 (0.886), MS-03-011 (0.871), MS-03-007 (0.864)
- Recusa pelo limiar: não; fatos faltando: [['ultima dose', 'dose', 'vacina'], ['profissional de saude', 'posto', 'unidade', 'medic', 'servico de saude']]
- Saída bruta: `{"resposta": "Precisa. Se tiver ferida aberta, use calçados e luvas ao caminhar em áreas inundadas ou com lama e evite manusear terra ou objetos sujos.", "fontes": ["MS-01-013"], "consta_na_base": true}`

### T041 (responde, saude_mental): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: a enchente afeta a cabeça também? to muito ansioso desde que perdi tudo
- Esperado: Sim, um evento traumático pode causar grave sofrimento. O Ministério da Saúde orienta manter contato com familiares e amigos, compartilhar sentimentos e buscar apoio psicológico se necessário.
- Resposta do modelo: Aumenta a chance de transtorno de estresse pós-traumático. Identifique os sinais e procure ajuda profissional.
- Fontes citadas: ['MS-01-004']; relevantes: ['MS-01-004']
- Trechos recuperados (similaridade): MS-01-004 (0.869), MS-01-003 (0.866), SMSSP-01-009 (0.865)
- Recusa pelo limiar: não; fatos faltando: [['familia', 'familiares', 'amigo']]
- Saída bruta: `{"resposta": "Aumenta a chance de transtorno de estresse pós-traumático. Identifique os sinais e procure ajuda profissional.", "fontes": ["MS-01-004"], "consta_na_base": true}`

### T042 (responde, agua): busca não trouxe o trecho relevante

- Falhas: busca não trouxe o trecho relevante, fato-chave faltando na resposta, citação errada ou ausente
- Pergunta: depois que voltar a agua da rua, posso beber direto da torneira?
- Esperado: Nas casas sem caixa d'água, quando o abastecimento voltar, deixe a água das torneiras escorrer por alguns minutos para eliminar a água contaminada dos canos.
- Resposta do modelo: Não. Use água potável ou filtre e desinfete a água disponível com duas gotas de hipoclorito de sódio a 2,5% por litro e só consuma depois de 30 minutos.
- Fontes citadas: ['MS-03-020']; relevantes: ['SEMIL-01-009']
- Trechos recuperados (similaridade): MS-03-010 (0.835), MS-03-020 (0.822), SMSSP-01-003 (0.821)
- Recusa pelo limiar: não; fatos faltando: [['escorrer', 'correr']]
- Saída bruta: `{"resposta": "Não. Use água potável ou filtre e desinfete a água disponível com duas gotas de hipoclorito de sódio a 2,5% por litro e só consuma depois de 30 minutos.", "fontes": ["MS-03-020"], "consta_na_base": true}`

## rag_sem_limiar: 20 casos com falha

- recusa indevida: 10
- fato-chave faltando na resposta: 7
- busca não trouxe o trecho relevante: 3

### T006 (responde, alertas_canais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: dá pra cadastrar mais de um cep no 40199?
- Esperado: Sim. Envie uma mensagem por vez para cada CEP; não há limite para a quantidade de CEPs cadastrados.
- Resposta do modelo: Sim, basta enviar uma mensagem por vez para cada CEP que deseja cadastrar.
- Fontes citadas: ['SEMIL-01-010']; relevantes: ['SEMIL-01-010']
- Trechos recuperados (similaridade): SEMIL-01-010 (0.851), MIDR-01-001 (0.839), MIDR-01-002 (0.823)
- Recusa pelo limiar: não; fatos faltando: [['limite']]
- Saída bruta: `{"resposta": "Sim, basta enviar uma mensagem por vez para cada CEP que deseja cadastrar.", "fontes": ["SEMIL-01-010"], "consta_na_base": true}`

### T007 (responde, alertas_canais): recusa indevida

- Falhas: recusa indevida
- Pergunta: precisa ter internet pro alerta da defesa civil aparecer na tela do celular?
- Esperado: Não. O Defesa Civil Alerta não depende de pacote de dados e funciona com ou sem Wi-Fi; basta o celular ser compatível e ter cobertura 4G ou 5G.
- Resposta do modelo: Não consta na base. O Defesa Civil Alerta usa a rede de telefonia celular para enviar alertas, não necessitando de internet
- Fontes citadas: ['MIDR-02-004']; relevantes: ['MIDR-02-004']
- Trechos recuperados (similaridade): MIDR-02-004 (0.900), MIDR-02-003 (0.875), MIDR-01-001 (0.866)
- Recusa pelo limiar: não; fatos faltando: [['4g', '5g']]
- Saída bruta: `{"resposta": "Não consta na base. O Defesa Civil Alerta usa a rede de telefonia celular para enviar alertas, não necessitando de internet", "fontes": ["MIDR-02-004"], "consta_na_base": false}`

### T008 (responde, alertas_canais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta, citação errada ou ausente
- Pergunta: qual o zap da defesa civil pra receber alerta?
- Esperado: Mande um “olá” para o WhatsApp (61) 2034-4611 e siga os passos para cadastrar sua área.
- Resposta do modelo: Pode enviar uma mensagem para o número 40199 com o CEP da área de interesse.
- Fontes citadas: ['MIDR-01-001']; relevantes: ['MIDR-01-002', 'MIDR-02-003']
- Trechos recuperados (similaridade): MIDR-01-001 (0.888), MIDR-02-003 (0.887), MIDR-02-004 (0.885)
- Recusa pelo limiar: não; fatos faltando: [['2034-4611', '20344611', '2034 4611']]
- Saída bruta: `{"resposta": "Pode enviar uma mensagem para o número 40199 com o CEP da área de interesse.", "fontes": ["MIDR-01-001"], "consta_na_base": true}`

### T010 (responde, alimentos_parafrase): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: o arroz e o feijão que molhou na enchente dá pra aproveitar se secar?
- Esperado: Não. Qualquer alimento que teve contato com a água da enchente deve ser descartado, mesmo que pareça seco; em caso de dúvida, jogue fora.
- Resposta do modelo: Não consta na base. Não é seguro aproveitar alimentos que entraram em contato com água de enchente, mesmo que pareçam secos.
- Fontes citadas: -; relevantes: ['MS-01-008', 'MS-01-005']
- Trechos recuperados (similaridade): MS-01-008 (0.856), SMSSP-01-004 (0.847), MS-03-020 (0.847)
- Recusa pelo limiar: não; fatos faltando: [['descart', 'jogue fora', 'jogar fora', 'joga fora', 'jogue no lixo']]
- Saída bruta: `{"resposta": "Não consta na base. Não é seguro aproveitar alimentos que entraram em contato com água de enchente, mesmo que pareçam secos.", "fontes": [], "consta_na_base": false}`

### T011 (responde, criancas): busca não trouxe o trecho relevante

- Falhas: busca não trouxe o trecho relevante, recusa indevida, citação errada ou ausente
- Pergunta: Meu filho quer brincar na enxurrada, tem problema?
- Esperado: Tem, sim. Crianças podem ser levadas pela correnteza ou pegar doenças graves, como hepatite e leptospirose; não deixe que brinquem nessas águas.
- Resposta do modelo: Não consta na base. <explique em uma frase e oriente a ligar 199 ou 193 em caso de risco>
- Fontes citadas: -; relevantes: ['COMDEC-01-005']
- Trechos recuperados (similaridade): MCID-01-005 (0.838), MS-03-019 (0.837), SMSSP-01-002 (0.836)
- Recusa pelo limiar: não; fatos faltando: [['correnteza', 'arrastad', 'levad'], ['leptospirose', 'hepatite', 'doenc']]
- Saída bruta: `{"resposta": "Não consta na base. <explique em uma frase e oriente a ligar 199 ou 193 em caso de risco>", "fontes": [], "consta_na_base": false}`

### T017 (responde, telefone): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: Tem um telefone pra saber se a rua ta bloqueada por alagamento?
- Esperado: Ligue 156 para a central de atendimento da CET ou consulte o site da CET.
- Resposta do modelo: Não consta na base. <pergunta> não foi mencionado se há um telefone específico para saber se a rua está bloqueada por alagamento
- Fontes citadas: -; relevantes: ['CGE-01-002']
- Trechos recuperados (similaridade): CGE-01-002 (0.866), MIDR-03-004 (0.858), MIDR-03-001 (0.852)
- Recusa pelo limiar: não; fatos faltando: [['156']]
- Saída bruta: `{"resposta": "Não consta na base. <pergunta> não foi mencionado se há um telefone específico para saber se a rua está bloqueada por alagamento", "fontes": [], "consta_na_base": false}`

### T018 (responde, animais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Se eu for pra um abrigo, posso deixar meu cachorro em casa?
- Esperado: Não é recomendado: os animais podem não sobreviver ou se perder. Se o abrigo não aceitar animais, peça a amigos ou familiares para cuidarem deles.
- Resposta do modelo: Não, não deve deixar o cachorro em casa. Deve seguir as orientações do coordenador do abrigo sobre a acomodação deles.
- Fontes citadas: ['MS-03-016']; relevantes: ['MS-03-016']
- Trechos recuperados (similaridade): MS-03-016 (0.876), MS-03-021 (0.827), MS-03-011 (0.827)
- Recusa pelo limiar: não; fatos faltando: [['sobreviv', 'perder', 'perca', 'extravi', 'morrer'], ['amigo', 'familia', 'parente']]
- Saída bruta: `{"resposta": "Não, não deve deixar o cachorro em casa. Deve seguir as orientações do coordenador do abrigo sobre a acomodação deles.", "fontes": ["MS-03-016"], "consta_na_base": true}`

### T019 (responde, transito): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: tô de carro e a rua encheu dagua, passo ou não?
- Esperado: Não atravesse: o carro pode ser arrastado pela água. Se o carro enguiçar, abandone-o.
- Resposta do modelo: Passar por ruas alagadas de carro é perigoso; dirija com baixa velocidade e acelerado, evite águas de enchente atrás de outro veículo para não bloquear. Se o carro enguiçar, abandone-o.
- Fontes citadas: ['MCID-01-007']; relevantes: ['MCID-01-007', 'MIDR-03-004']
- Trechos recuperados (similaridade): COMDEC-01-006 (0.856), MCID-01-007 (0.851), CGE-01-003 (0.837)
- Recusa pelo limiar: não; fatos faltando: [['arrastad', 'levado']]
- Saída bruta: `{"resposta": "Passar por ruas alagadas de carro é perigoso; dirija com baixa velocidade e acelerado, evite águas de enchente atrás de outro veículo para não bloquear. Se o carro enguiçar, abandone-o.", "fontes": ["MCID-01-007"], "consta_na_base": true}`

### T020 (responde, energia_eletrica): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: a casa alagou e depois secou, posso ligar a geladeira que molhou?
- Esperado: Não use equipamentos elétricos que foram molhados ou ficaram em local inundado, porque há risco de choque elétrico e curto-circuito.
- Resposta do modelo: Não consta na base. Caso a geladeira tenha sido molhada, não use equipamentos elétricos que tenham sido molhados ou que estiveram em locais inundados, pois há risco de choque elétrico e curto-circuito. Lave e desinfete os objetos atingidos pela enchente usando uma mistura de água sanitária e água limpa.
- Fontes citadas: ['MCID-01-005']; relevantes: ['COMDEC-01-008', 'MS-03-019']
- Trechos recuperados (similaridade): MCID-01-005 (0.838), COMDEC-01-008 (0.829), CGE-01-003 (0.824)
- Recusa pelo limiar: não
- Saída bruta: `{"resposta": "Não consta na base. Caso a geladeira tenha sido molhada, não use equipamentos elétricos que tenham sido molhados ou que estiveram em locais inundados, pois há risco de choque elétrico e curto-circuito. Lave e desinfete os objetos atingidos pela enchente usando uma mistura de água sanitária e água limpa.", "fontes": ["MCID-01-005"], "consta_na_base": false}`

### T021 (responde, limpeza): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: a parede ficou com mofo preto depois da enchente, como limpo?
- Esperado: Lave com água e sabão e desinfete com água sanitária a 2,5% (400 mL num balde com 20 litros de água), deixando agir 30 minutos, com o local bem ventilado.
- Resposta do modelo: Lave e desinfete a parede com água e sabão, em seguida, com água sanitária (hipoclorito de sódio a 2,5%) diluída na proporção de 400 mL do produto para um balde com 20 litros de água limpa, deixando agir por 30 minutos. Apareça a um bombeiro se houver risco.
- Fontes citadas: ['SMSSP-01-007']; relevantes: ['SMSSP-01-007']
- Trechos recuperados (similaridade): SMSSP-01-007 (0.886), COMDEC-01-008 (0.857), MS-01-011 (0.857)
- Recusa pelo limiar: não; fatos faltando: [['ventila', 'arejad']]
- Saída bruta: `{"resposta": "Lave e desinfete a parede com água e sabão, em seguida, com água sanitária (hipoclorito de sódio a 2,5%) diluída na proporção de 400 mL do produto para um balde com 20 litros de água limpa, deixando agir por 30 minutos. Apareça a um bombeiro se houver risco.", "fontes": ["SMSSP-01-007"], "consta_na_base": true}`

### T022 (responde, limpeza_seguranca): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: Posso misturar água sanitária com vinagre pra limpar melhor?
- Esperado: Não. Nunca misture água sanitária com vinagre, ácido muriático ou outros produtos de limpeza, pois podem ser liberados gases prejudiciais à saúde.
- Resposta do modelo: Não consta na base. Em caso de dúvidas, consulte um profissional de saúde.
- Fontes citadas: -; relevantes: ['SMSSP-01-008']
- Trechos recuperados (similaridade): SMSSP-01-008 (0.845), MS-01-007 (0.845), SMSSP-01-007 (0.837)
- Recusa pelo limiar: não; fatos faltando: [['gases', 'gas', 'toxic']]
- Saída bruta: `{"resposta": "Não consta na base. Em caso de dúvidas, consulte um profissional de saúde.", "fontes": [], "consta_na_base": false}`

### T025 (responde, kit_detalhe_numerico): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: quantos litros de agua por pessoa no kit?
- Esperado: Dois litros de água potável por pessoa por dia, para um kit que atenda 72 horas.
- Resposta do modelo: Não consta na base. O documento não fornece informações específicas sobre a quantidade de água por pessoa no kit.
- Fontes citadas: -; relevantes: ['ABR-01-001']
- Trechos recuperados (similaridade): ABR-01-001 (0.864), MS-03-010 (0.858), MS-03-005 (0.855)
- Recusa pelo limiar: não; fatos faltando: [['dois litros', '2 litros', '2l', 'seis litros', '6 litros']]
- Saída bruta: `{"resposta": "Não consta na base. O documento não fornece informações específicas sobre a quantidade de água por pessoa no kit.", "fontes": [], "consta_na_base": false}`

### T026 (responde, kit_emergencia): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: o governo mandou montar kit de emergência porque vai ter desastre?
- Esperado: Não. O MIDR esclareceu que o kit é uma medida preventiva e não está ligado a nenhum alerta nacional nem a previsão de interrupção de serviços.
- Resposta do modelo: Não consta na base. O kit de emergência é medida preventiva e não está relacionada a qualquer alerta nacional ou previsão de desastre.
- Fontes citadas: -; relevantes: ['MIDR-02-001', 'ABR-01-002']
- Trechos recuperados (similaridade): MIDR-02-001 (0.883), ABR-01-002 (0.874), ABR-01-001 (0.874)
- Recusa pelo limiar: não
- Saída bruta: `{"resposta": "Não consta na base. O kit de emergência é medida preventiva e não está relacionada a qualquer alerta nacional ou previsão de desastre.", "fontes": [], "consta_na_base": false}`

### T029 (responde, direitos_detalhe_numerico): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: comprovante de residencia pro saque calamidade pode ser de qualquer data?
- Esperado: Não. O comprovante deve estar em nome do trabalhador e ter sido emitido até 120 dias antes da decretação da calamidade.
- Resposta do modelo: Não consta na base. <explique em uma frase e oriente a ligar 199 ou 193 em caso de risco>
- Fontes citadas: -; relevantes: ['FGTS-01-003']
- Trechos recuperados (similaridade): FGTS-01-003 (0.895), FGTS-01-002 (0.866), FGTS-01-001 (0.865)
- Recusa pelo limiar: não; fatos faltando: [['120']]
- Saída bruta: `{"resposta": "Não consta na base. <explique em uma frase e oriente a ligar 199 ou 193 em caso de risco>", "fontes": [], "consta_na_base": false}`

### T030 (responde, conceitos): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Qual a diferença de enxurrada pra inundação?
- Esperado: Na inundação, a água transborda de forma gradual, em geral por chuvas prolongadas em áreas de planície. A enxurrada é um escoamento rápido e forte, causado por chuva intensa e concentrada, com subida súbita da água e grande poder destrutivo.
- Resposta do modelo: Enxurrada é o transbordamento de água de um rio ou canal por causa de chuvas intensas e concentradas, enquanto a inundação é a submersão de áreas fora dos limites normais de um curso de água, em zonas que normalmente não ficam submersas.
- Fontes citadas: ['MIDR-03-005']; relevantes: ['MIDR-03-005']
- Trechos recuperados (similaridade): MIDR-03-005 (0.905), MS-01-002 (0.858), SEMIL-01-002 (0.857)
- Recusa pelo limiar: não; fatos faltando: [['gradual', 'devagar', 'aos poucos'], ['subit', 'brusc', 'rapid', 'alta velocidade', 'de repente']]
- Saída bruta: `{"resposta": "Enxurrada é o transbordamento de água de um rio ou canal por causa de chuvas intensas e concentradas, enquanto a inundação é a submersão de áreas fora dos limites normais de um curso de água, em zonas que normalmente não ficam submersas.", "fontes": ["MIDR-03-005"], "consta_na_base": true}`

### T032 (responde, deslizamento_prevencao): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: Bananeira no morro ajuda a segurar a terra?
- Esperado: Não. Bananeiras e árvores grandes acumulam muita água no solo e podem provocar deslizamentos; o recomendado é plantar grama e capim.
- Resposta do modelo: Não consta na base. Não há indicação de que bananeiras ajudam a segurar a terra no morro, mas a orientação é evitar plantar árvores grandes como bananeira para evitar deslizamentos de terra.
- Fontes citadas: -; relevantes: ['DCSP-01-001']
- Trechos recuperados (similaridade): DCSP-01-001 (0.845), MS-03-003 (0.809), MCID-01-004 (0.808)
- Recusa pelo limiar: não; fatos faltando: [['acumul', 'agua'], ['grama', 'capim']]
- Saída bruta: `{"resposta": "Não consta na base. Não há indicação de que bananeiras ajudam a segurar a terra no morro, mas a orientação é evitar plantar árvores grandes como bananeira para evitar deslizamentos de terra.", "fontes": [], "consta_na_base": false}`

### T035 (responde, idosos_pcd): busca não trouxe o trecho relevante

- Falhas: busca não trouxe o trecho relevante, fato-chave faltando na resposta, citação errada ou ausente
- Pergunta: minha vó mora comigo, o que a gente deve planejar pra enchente?
- Esperado: Montem um plano da família com um mapa do bairro e combinem pontos de encontro para o caso de evacuar a casa. Tenham atenção maior com idosos, que podem ter dificuldade de agilidade e locomoção.
- Resposta do modelo: Manter os bueiros limpos, inspecionar telhado e calhas, e preparar um kit de emergência. Evitar deixar crianças sozinhas e manter objetos de valor em locais altos.
- Fontes citadas: ['MCID-01-005']; relevantes: ['MS-03-004']
- Trechos recuperados (similaridade): COMDEC-01-003 (0.878), COMDEC-01-002 (0.872), MCID-01-005 (0.872)
- Recusa pelo limiar: não; fatos faltando: [['plano'], ['encontro']]
- Saída bruta: `{"resposta": "Manter os bueiros limpos, inspecionar telhado e calhas, e preparar um kit de emergência. Evitar deixar crianças sozinhas e manter objetos de valor em locais altos.", "fontes": ["MCID-01-005"], "consta_na_base": true}`

### T039 (responde, saude): recusa indevida

- Falhas: recusa indevida
- Pergunta: me cortei num entulho limpando a casa, preciso tomar vacina antitetânica?
- Esperado: Verifique a data da sua última dose da vacina contra o tétano e, se necessário, procure um profissional de saúde para avaliar o reforço. Limpe e desinfete o ferimento logo.
- Resposta do modelo: Não consta na base. Se você se ferir durante ou após uma enchente, verifique a data da última dose e, se necessário, procure um profissional de saúde para avaliar o reforço.
- Fontes citadas: ['MS-01-013']; relevantes: ['MS-01-013']
- Trechos recuperados (similaridade): MS-01-013 (0.886), MS-03-011 (0.871), MS-03-007 (0.864)
- Recusa pelo limiar: não
- Saída bruta: `{"resposta": "Não consta na base. Se você se ferir durante ou após uma enchente, verifique a data da última dose e, se necessário, procure um profissional de saúde para avaliar o reforço.", "fontes": ["MS-01-013"], "consta_na_base": false}`

### T041 (responde, saude_mental): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: a enchente afeta a cabeça também? to muito ansioso desde que perdi tudo
- Esperado: Sim, um evento traumático pode causar grave sofrimento. O Ministério da Saúde orienta manter contato com familiares e amigos, compartilhar sentimentos e buscar apoio psicológico se necessário.
- Resposta do modelo: A ansiedade é um sintoma comum após enchentes. Procure atendimento médico se sentir muito ansioso. Lembre-se de buscar ajuda profissional para cuidar tanto do seu bem-estar físico quanto mental.
- Fontes citadas: ['MS-01-004']; relevantes: ['MS-01-004']
- Trechos recuperados (similaridade): MS-01-004 (0.869), MS-01-003 (0.866), SMSSP-01-009 (0.865)
- Recusa pelo limiar: não; fatos faltando: [['familia', 'familiares', 'amigo']]
- Saída bruta: `{"resposta": "A ansiedade é um sintoma comum após enchentes. Procure atendimento médico se sentir muito ansioso. Lembre-se de buscar ajuda profissional para cuidar tanto do seu bem-estar físico quanto mental.", "fontes": ["MS-01-004"], "consta_na_base": true}`

### T042 (responde, agua): busca não trouxe o trecho relevante

- Falhas: busca não trouxe o trecho relevante, recusa indevida, citação errada ou ausente
- Pergunta: depois que voltar a agua da rua, posso beber direto da torneira?
- Esperado: Nas casas sem caixa d'água, quando o abastecimento voltar, deixe a água das torneiras escorrer por alguns minutos para eliminar a água contaminada dos canos.
- Resposta do modelo: Não consta na base. Não é recomendado beber água da torneira imediatamente após enchentes, pois a água pode estar contaminada.
- Fontes citadas: -; relevantes: ['SEMIL-01-009']
- Trechos recuperados (similaridade): MS-03-010 (0.835), MS-03-020 (0.822), SMSSP-01-003 (0.821)
- Recusa pelo limiar: não; fatos faltando: [['escorrer', 'correr'], ['minutos']]
- Saída bruta: `{"resposta": "Não consta na base. Não é recomendado beber água da torneira imediatamente após enchentes, pois a água pode estar contaminada.", "fontes": [], "consta_na_base": false}`

## rag_lora_sem_limiar: 20 casos com falha

- fato-chave faltando na resposta: 14
- busca não trouxe o trecho relevante: 3
- recusa indevida: 3

### T006 (responde, alertas_canais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: dá pra cadastrar mais de um cep no 40199?
- Esperado: Sim. Envie uma mensagem por vez para cada CEP; não há limite para a quantidade de CEPs cadastrados.
- Resposta do modelo: Pode. Envie uma mensagem por vez para cada CEP que deseja cadastrar.
- Fontes citadas: ['SEMIL-01-010']; relevantes: ['SEMIL-01-010']
- Trechos recuperados (similaridade): SEMIL-01-010 (0.851), MIDR-01-001 (0.839), MIDR-01-002 (0.823)
- Recusa pelo limiar: não; fatos faltando: [['limite']]
- Saída bruta: `{"resposta": "Pode. Envie uma mensagem por vez para cada CEP que deseja cadastrar.", "fontes": ["SEMIL-01-010"], "consta_na_base": true}`

### T007 (responde, alertas_canais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: precisa ter internet pro alerta da defesa civil aparecer na tela do celular?
- Esperado: Não. O Defesa Civil Alerta não depende de pacote de dados e funciona com ou sem Wi-Fi; basta o celular ser compatível e ter cobertura 4G ou 5G.
- Resposta do modelo: Não. Os alertas aparecem diretamente na tela dos celulares compatíveis localizados em áreas de risco, sem precisar de conexão com a internet.
- Fontes citadas: ['MIDR-02-004', 'MIDR-01-001']; relevantes: ['MIDR-02-004']
- Trechos recuperados (similaridade): MIDR-02-004 (0.900), MIDR-02-003 (0.875), MIDR-01-001 (0.866)
- Recusa pelo limiar: não; fatos faltando: [['4g', '5g']]
- Saída bruta: `{"resposta": "Não. Os alertas aparecem diretamente na tela dos celulares compatíveis localizados em áreas de risco, sem precisar de conexão com a internet.", "fontes": ["MIDR-02-004", "MIDR-01-001"], "consta_na_base": true}`

### T011 (responde, criancas): busca não trouxe o trecho relevante

- Falhas: busca não trouxe o trecho relevante, fato-chave faltando na resposta, citação errada ou ausente
- Pergunta: Meu filho quer brincar na enxurrada, tem problema?
- Esperado: Tem, sim. Crianças podem ser levadas pela correnteza ou pegar doenças graves, como hepatite e leptospirose; não deixe que brinquem nessas águas.
- Resposta do modelo: Não. Não deixe as crianças brincarem nas águas da inundação.
- Fontes citadas: ['MS-03-019']; relevantes: ['COMDEC-01-005']
- Trechos recuperados (similaridade): MCID-01-005 (0.838), MS-03-019 (0.837), SMSSP-01-002 (0.836)
- Recusa pelo limiar: não; fatos faltando: [['correnteza', 'arrastad', 'levad'], ['leptospirose', 'hepatite', 'doenc']]
- Saída bruta: `{"resposta": "Não. Não deixe as crianças brincarem nas águas da inundação.", "fontes": ["MS-03-019"], "consta_na_base": true}`

### T012 (responde, deslizamento_sinais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: como sei se vai ter deslizamento no morro? quais sinais?
- Esperado: Fique atento a rachaduras ou trincas no chão e nas paredes, árvores, postes ou muros inclinados e água mais barrenta que o normal. Se notar, saia do local e ligue 199 para a Defesa Civil.
- Resposta do modelo: Observar rachaduras, trincas ou saliências no chão ou nas paredes, e água mais barrenta que o normal, pode indicar um deslizamento.
- Fontes citadas: ['DCSP-01-003']; relevantes: ['DCSP-01-003', 'MCID-01-004']
- Trechos recuperados (similaridade): DCSP-01-001 (0.879), MCID-01-004 (0.871), DCSP-01-003 (0.866)
- Recusa pelo limiar: não; fatos faltando: [['inclina', 'torto', 'tort'], ['199', 'saia', 'sair']]
- Saída bruta: `{"resposta": "Observar rachaduras, trincas ou saliências no chão ou nas paredes, e água mais barrenta que o normal, pode indicar um deslizamento.", "fontes": ["DCSP-01-003"], "consta_na_base": true}`

### T014 (responde, saude_sintomas): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Quais os sintomas da leptospirose?
- Esperado: Na fase inicial: febre, falta de apetite, dor muscular principalmente na panturrilha (batata da perna), dor de cabeça e náuseas ou vômitos.
- Resposta do modelo: Fevere, falta de apetite, dor muscular (principalmente na panturrilha), dor de cabeça e náuseas ou vômitos. Também podem ocorrer diarreia, dor nas articulações, vermelhidão ou hemorragia nos olhos, sensibilidade à luz, dor nos olhos e tosse.
- Fontes citadas: ['MS-02-003']; relevantes: ['MS-02-003', 'COMDEC-01-007']
- Trechos recuperados (similaridade): MS-02-003 (0.910), MS-02-001 (0.882), MS-02-002 (0.880)
- Recusa pelo limiar: não; fatos faltando: [['febre']]
- Saída bruta: `{"resposta": "Fevere, falta de apetite, dor muscular (principalmente na panturrilha), dor de cabeça e náuseas ou vômitos. Também podem ocorrer diarreia, dor nas articulações, vermelhidão ou hemorragia nos olhos, sensibilidade à luz, dor nos olhos e tosse.", "fontes": ["MS-02-003"], "consta_na_base": true}`

### T018 (responde, animais): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Se eu for pra um abrigo, posso deixar meu cachorro em casa?
- Esperado: Não é recomendado: os animais podem não sobreviver ou se perder. Se o abrigo não aceitar animais, peça a amigos ou familiares para cuidarem deles.
- Resposta do modelo: Não. Os animais domésticos podem não sobreviver ou se perder antes que vocês voltem.
- Fontes citadas: ['MS-03-016']; relevantes: ['MS-03-016']
- Trechos recuperados (similaridade): MS-03-016 (0.876), MS-03-021 (0.827), MS-03-011 (0.827)
- Recusa pelo limiar: não; fatos faltando: [['amigo', 'familia', 'parente']]
- Saída bruta: `{"resposta": "Não. Os animais domésticos podem não sobreviver ou se perder antes que vocês voltem.", "fontes": ["MS-03-016"], "consta_na_base": true}`

### T019 (responde, transito): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: tô de carro e a rua encheu dagua, passo ou não?
- Esperado: Não atravesse: o carro pode ser arrastado pela água. Se o carro enguiçar, abandone-o.
- Resposta do modelo: Não. Se precisar atravessar ruas alagadas, use muros e paredes como apoio ou cordas, com ajuda de pelo menos três pessoas.
- Fontes citadas: ['MCID-01-007']; relevantes: ['MCID-01-007', 'MIDR-03-004']
- Trechos recuperados (similaridade): COMDEC-01-006 (0.856), MCID-01-007 (0.851), CGE-01-003 (0.837)
- Recusa pelo limiar: não; fatos faltando: [['arrastad', 'levado'], ['nao atravesse', 'nunca atravesse', 'nao passe', 'nao enfrente', 'evite', 'nao tente']]
- Saída bruta: `{"resposta": "Não. Se precisar atravessar ruas alagadas, use muros e paredes como apoio ou cordas, com ajuda de pelo menos três pessoas.", "fontes": ["MCID-01-007"], "consta_na_base": true}`

### T020 (responde, energia_eletrica): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta, citação errada ou ausente
- Pergunta: a casa alagou e depois secou, posso ligar a geladeira que molhou?
- Esperado: Não use equipamentos elétricos que foram molhados ou ficaram em local inundado, porque há risco de choque elétrico e curto-circuito.
- Resposta do modelo: Não. Mantenha objetos de valor em locais altos e esvazie a geladeira.
- Fontes citadas: ['MCID-01-005']; relevantes: ['COMDEC-01-008', 'MS-03-019']
- Trechos recuperados (similaridade): MCID-01-005 (0.838), COMDEC-01-008 (0.829), CGE-01-003 (0.824)
- Recusa pelo limiar: não; fatos faltando: [['choque', 'curto']]
- Saída bruta: `{"resposta": "Não. Mantenha objetos de valor em locais altos e esvazie a geladeira.", "fontes": ["MCID-01-005"], "consta_na_base": true}`

### T021 (responde, limpeza): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: a parede ficou com mofo preto depois da enchente, como limpo?
- Esperado: Lave com água e sabão e desinfete com água sanitária a 2,5% (400 mL num balde com 20 litros de água), deixando agir 30 minutos, com o local bem ventilado.
- Resposta do modelo: Lave, desinfete e deixe o local bem ventilado.
- Fontes citadas: ['SMSSP-01-007']; relevantes: ['SMSSP-01-007']
- Trechos recuperados (similaridade): SMSSP-01-007 (0.886), COMDEC-01-008 (0.857), MS-01-011 (0.857)
- Recusa pelo limiar: não; fatos faltando: [['agua sanitaria', 'hipoclorito', 'cloro']]
- Saída bruta: `{"resposta": "Lave, desinfete e deixe o local bem ventilado.", "fontes": ["SMSSP-01-007"], "consta_na_base": true}`

### T025 (responde, kit_detalhe_numerico): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: quantos litros de agua por pessoa no kit?
- Esperado: Dois litros de água potável por pessoa por dia, para um kit que atenda 72 horas.
- Resposta do modelo: Não consta na base. Os documentos oficiais que eu uso não trazem essa informação; para isso, procure a prefeitura ou o órgão responsável.
- Fontes citadas: -; relevantes: ['ABR-01-001']
- Trechos recuperados (similaridade): ABR-01-001 (0.864), MS-03-010 (0.858), MS-03-005 (0.855)
- Recusa pelo limiar: não; fatos faltando: [['dois litros', '2 litros', '2l', 'seis litros', '6 litros']]
- Saída bruta: `{"resposta": "Não consta na base. Os documentos oficiais que eu uso não trazem essa informação; para isso, procure a prefeitura ou o órgão responsável.", "fontes": [], "consta_na_base": false}`

### T026 (responde, kit_emergencia): recusa indevida

- Falhas: recusa indevida, citação errada ou ausente
- Pergunta: o governo mandou montar kit de emergência porque vai ter desastre?
- Esperado: Não. O MIDR esclareceu que o kit é uma medida preventiva e não está ligado a nenhum alerta nacional nem a previsão de interrupção de serviços.
- Resposta do modelo: Não consta na base. Os documentos oficiais que eu uso não trazem essa informação; para isso, procure a prefeitura ou o órgão responsável da sua rua.
- Fontes citadas: -; relevantes: ['MIDR-02-001', 'ABR-01-002']
- Trechos recuperados (similaridade): MIDR-02-001 (0.883), ABR-01-002 (0.874), ABR-01-001 (0.874)
- Recusa pelo limiar: não; fatos faltando: [['prevent', 'prevencao'], ['alerta nacional', 'nao esta relacionad', 'nao tem relacao', 'nao ha alerta', 'nao existe alerta']]
- Saída bruta: `{"resposta": "Não consta na base. Os documentos oficiais que eu uso não trazem essa informação; para isso, procure a prefeitura ou o órgão responsável da sua rua.", "fontes": [], "consta_na_base": false}`

### T029 (responde, direitos_detalhe_numerico): recusa indevida

- Falhas: recusa indevida
- Pergunta: comprovante de residencia pro saque calamidade pode ser de qualquer data?
- Esperado: Não. O comprovante deve estar em nome do trabalhador e ter sido emitido até 120 dias antes da decretação da calamidade.
- Resposta do modelo: Não consta na base. Os documentos exigidos para o saque calamidade são documento de identidade, com foto da frente e do verso, e comprovante de residência em nome do trabalhador, emitido até 120 dias antes da decretação da calamidade.
- Fontes citadas: ['FGTS-01-003']; relevantes: ['FGTS-01-003']
- Trechos recuperados (similaridade): FGTS-01-003 (0.895), FGTS-01-002 (0.866), FGTS-01-001 (0.865)
- Recusa pelo limiar: não
- Saída bruta: `{"resposta": "Não consta na base. Os documentos exigidos para o saque calamidade são documento de identidade, com foto da frente e do verso, e comprovante de residência em nome do trabalhador, emitido até 120 dias antes da decretação da calamidade.", "fontes": ["FGTS-01-003"], "consta_na_base": false}`

### T030 (responde, conceitos): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Qual a diferença de enxurrada pra inundação?
- Esperado: Na inundação, a água transborda de forma gradual, em geral por chuvas prolongadas em áreas de planície. A enxurrada é um escoamento rápido e forte, causado por chuva intensa e concentrada, com subida súbita da água e grande poder destrutivo.
- Resposta do modelo: As enxurradas ocorrem pelo escoamento superficial de alta velocidade e energia, provocado por chuvas intensas e concentradas, em pequenas bacias de relevo acidentado, com elevação súbita das vazões e transbordamento brusco.
- Fontes citadas: ['MIDR-03-005']; relevantes: ['MIDR-03-005']
- Trechos recuperados (similaridade): MIDR-03-005 (0.905), MS-01-002 (0.858), SEMIL-01-002 (0.857)
- Recusa pelo limiar: não; fatos faltando: [['gradual', 'devagar', 'aos poucos']]
- Saída bruta: `{"resposta": "As enxurradas ocorrem pelo escoamento superficial de alta velocidade e energia, provocado por chuvas intensas e concentradas, em pequenas bacias de relevo acidentado, com elevação súbita das vazões e transbordamento brusco.", "fontes": ["MIDR-03-005"], "consta_na_base": true}`

### T031 (responde, deslizamento_prevencao): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Por que não pode jogar a água do tanque no barranco?
- Esperado: Porque umedece a encosta e aumenta o risco de deslizamento, além de contaminar o solo. O ideal é instalar canaletas ou tubos para escoar essa água.
- Resposta do modelo: O lixo jogado nas encostas acumula água, fica mais pesado e, se escorregar, arrasta o solo junto.
- Fontes citadas: ['DCSP-01-002']; relevantes: ['DCSP-01-002']
- Trechos recuperados (similaridade): DCSP-01-002 (0.846), MS-03-019 (0.819), SMSSP-01-001 (0.818)
- Recusa pelo limiar: não; fatos faltando: [['desliz'], ['canaleta', 'tubo', 'cano']]
- Saída bruta: `{"resposta": "O lixo jogado nas encostas acumula água, fica mais pesado e, se escorregar, arrasta o solo junto.", "fontes": ["DCSP-01-002"], "consta_na_base": true}`

### T032 (responde, deslizamento_prevencao): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Bananeira no morro ajuda a segurar a terra?
- Esperado: Não. Bananeiras e árvores grandes acumulam muita água no solo e podem provocar deslizamentos; o recomendado é plantar grama e capim.
- Resposta do modelo: Não. Bananeiras e árvores grandes como manga, mamão e abacate acumulam muita água no solo e podem provocar deslizamentos de terra.
- Fontes citadas: ['DCSP-01-001']; relevantes: ['DCSP-01-001']
- Trechos recuperados (similaridade): DCSP-01-001 (0.845), MS-03-003 (0.809), MCID-01-004 (0.808)
- Recusa pelo limiar: não; fatos faltando: [['grama', 'capim']]
- Saída bruta: `{"resposta": "Não. Bananeiras e árvores grandes como manga, mamão e abacate acumulam muita água no solo e podem provocar deslizamentos de terra.", "fontes": ["DCSP-01-001"], "consta_na_base": true}`

### T035 (responde, idosos_pcd): busca não trouxe o trecho relevante

- Falhas: busca não trouxe o trecho relevante, fato-chave faltando na resposta, citação errada ou ausente
- Pergunta: minha vó mora comigo, o que a gente deve planejar pra enchente?
- Esperado: Montem um plano da família com um mapa do bairro e combinem pontos de encontro para o caso de evacuar a casa. Tenham atenção maior com idosos, que podem ter dificuldade de agilidade e locomoção.
- Resposta do modelo: Elabore um Plano Familiar de Emergência, prepare um kit de emergência e separe documentos importantes. Contate a Defesa Civil (199) ou o BOMBEIROS (193) para instruções.
- Fontes citadas: ['MCID-01-005']; relevantes: ['MS-03-004']
- Trechos recuperados (similaridade): COMDEC-01-003 (0.878), COMDEC-01-002 (0.872), MCID-01-005 (0.872)
- Recusa pelo limiar: não; fatos faltando: [['encontro']]
- Saída bruta: `{"resposta": "Elabore um Plano Familiar de Emergência, prepare um kit de emergência e separe documentos importantes. Contate a Defesa Civil (199) ou o BOMBEIROS (193) para instruções.", "fontes": ["MCID-01-005"], "consta_na_base": true}`

### T037 (responde, saude_parafrase): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: Rato faz a lepto chegar até minha casa como?
- Esperado: Na chuva, rios, córregos e esgoto transbordam, invadem as tocas dos ratos e a água chega às casas contaminada pela urina; o contato com essa água ou lama pode transmitir a leptospirose.
- Resposta do modelo: Ratos ficam em galerias, lixões, terrenos baldios e esgotos e, no período chuvoso, a água do rio, do córrego e da rede de esgoto pode transbordar, invadindo as tocas de ratos e chegar contaminada às residências.
- Fontes citadas: ['MS-03-012']; relevantes: ['MS-03-012']
- Trechos recuperados (similaridade): MS-03-012 (0.859), MS-03-013 (0.838), MS-02-006 (0.831)
- Recusa pelo limiar: não; fatos faltando: [['urina', 'xixi']]
- Saída bruta: `{"resposta": "Ratos ficam em galerias, lixões, terrenos baldios e esgotos e, no período chuvoso, a água do rio, do córrego e da rede de esgoto pode transbordar, invadindo as tocas de ratos e chegar contaminada às residências.", "fontes": ["MS-03-012"], "consta_na_base": true}`

### T039 (responde, saude): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: me cortei num entulho limpando a casa, preciso tomar vacina antitetânica?
- Esperado: Verifique a data da sua última dose da vacina contra o tétano e, se necessário, procure um profissional de saúde para avaliar o reforço. Limpe e desinfete o ferimento logo.
- Resposta do modelo: Precisa. Se tiver ferida aberta, use calçados e luvas ao caminhar em áreas inundadas ou com lama e evite manusear terra ou objetos sujos.
- Fontes citadas: ['MS-01-013']; relevantes: ['MS-01-013']
- Trechos recuperados (similaridade): MS-01-013 (0.886), MS-03-011 (0.871), MS-03-007 (0.864)
- Recusa pelo limiar: não; fatos faltando: [['ultima dose', 'dose', 'vacina'], ['profissional de saude', 'posto', 'unidade', 'medic', 'servico de saude']]
- Saída bruta: `{"resposta": "Precisa. Se tiver ferida aberta, use calçados e luvas ao caminhar em áreas inundadas ou com lama e evite manusear terra ou objetos sujos.", "fontes": ["MS-01-013"], "consta_na_base": true}`

### T041 (responde, saude_mental): fato-chave faltando na resposta

- Falhas: fato-chave faltando na resposta
- Pergunta: a enchente afeta a cabeça também? to muito ansioso desde que perdi tudo
- Esperado: Sim, um evento traumático pode causar grave sofrimento. O Ministério da Saúde orienta manter contato com familiares e amigos, compartilhar sentimentos e buscar apoio psicológico se necessário.
- Resposta do modelo: Aumenta a chance de transtorno de estresse pós-traumático. Identifique os sinais e procure ajuda profissional.
- Fontes citadas: ['MS-01-004']; relevantes: ['MS-01-004']
- Trechos recuperados (similaridade): MS-01-004 (0.869), MS-01-003 (0.866), SMSSP-01-009 (0.865)
- Recusa pelo limiar: não; fatos faltando: [['familia', 'familiares', 'amigo']]
- Saída bruta: `{"resposta": "Aumenta a chance de transtorno de estresse pós-traumático. Identifique os sinais e procure ajuda profissional.", "fontes": ["MS-01-004"], "consta_na_base": true}`

### T042 (responde, agua): busca não trouxe o trecho relevante

- Falhas: busca não trouxe o trecho relevante, fato-chave faltando na resposta, citação errada ou ausente
- Pergunta: depois que voltar a agua da rua, posso beber direto da torneira?
- Esperado: Nas casas sem caixa d'água, quando o abastecimento voltar, deixe a água das torneiras escorrer por alguns minutos para eliminar a água contaminada dos canos.
- Resposta do modelo: Não. Use água potável ou filtre e desinfete a água disponível com duas gotas de hipoclorito de sódio a 2,5% por litro e só consuma depois de 30 minutos.
- Fontes citadas: ['MS-03-020']; relevantes: ['SEMIL-01-009']
- Trechos recuperados (similaridade): MS-03-010 (0.835), MS-03-020 (0.822), SMSSP-01-003 (0.821)
- Recusa pelo limiar: não; fatos faltando: [['escorrer', 'correr']]
- Saída bruta: `{"resposta": "Não. Use água potável ou filtre e desinfete a água disponível com duas gotas de hipoclorito de sódio a 2,5% por litro e só consuma depois de 30 minutos.", "fontes": ["MS-03-020"], "consta_na_base": true}`
