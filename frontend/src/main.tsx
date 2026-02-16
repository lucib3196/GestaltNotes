import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ThemeProvider } from "@mui/material/styles";
import { AuthProvider } from './context/AuthProvider.tsx';
import { MathJaxContext } from "better-react-mathjax";
import './index.css'
import App from './App.tsx'
import { theme } from './theme';

const mathJaxConfig = {
  tex: {
    inlineMath: [["$", "$"]],
    displayMath: [["$$", "$$"]],
  },
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MathJaxContext config={mathJaxConfig}>
      <AuthProvider>
        <ThemeProvider theme={theme}>
          <App />

        </ThemeProvider>
      </AuthProvider>
    </MathJaxContext>

  </StrictMode>,
)
