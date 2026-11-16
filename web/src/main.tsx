import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { IconContext } from "@phosphor-icons/react"

import "./index.css"
import App from "./App.tsx"

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <IconContext.Provider value={{ weight: "duotone", size: "1em" }}>
      <App />
    </IconContext.Provider>
  </StrictMode>
)
