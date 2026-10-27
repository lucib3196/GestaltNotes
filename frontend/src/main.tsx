import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ThemeProvider } from "@mui/material/styles";
import { AuthProvider } from "./features/Auth";
import { MathJaxContext } from "better-react-mathjax";
import { ToastContainer } from "react-toastify";
import { GenContentProvider } from "./features/GeneratedContent/instance/context.tsx";
import { LectureProvider } from "./features/Lectures/index.ts";
import "./index.css";
import App from "./App.tsx";
import { theme } from "./theme";

const mathJaxConfig = {
  tex: {
    inlineMath: [
      ["$", "$"],
      ["\\(", "\\)"],
    ],
    displayMath: [
      ["$$", "$$"],
      ["\\[", "\\]"],
    ],
    processEscapes: true,
    macros: {
      vect: ["\\mathbf{#1}", 1],
    },
  },
  options: {
    skipHtmlTags: ["script", "noscript", "style", "textarea", "pre", "code"],
  },
};

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <MathJaxContext config={mathJaxConfig} version={3}>
      <LectureProvider>
        <GenContentProvider>
          <AuthProvider>
            <ThemeProvider theme={theme}>
              <ToastContainer position="top-right" autoClose={3000} />
              <App />
            </ThemeProvider>
          </AuthProvider>
        </GenContentProvider>
      </LectureProvider>
    </MathJaxContext>
  </StrictMode>,
);
