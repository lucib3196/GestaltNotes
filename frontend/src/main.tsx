import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ThemeProvider } from "@mui/material/styles";
import { AuthProvider } from './context/AuthProvider.tsx';
import { MathJaxContext } from "better-react-mathjax";
import { AuthModeProvider } from './features/UserManagement/context.tsx';
import { ToastContainer } from "react-toastify";
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
    <AuthModeProvider>
      <MathJaxContext config={mathJaxConfig}>
        <AuthProvider>
          <ThemeProvider theme={theme}>
            <ToastContainer position="top-right" autoClose={3000} />
            <App />

          </ThemeProvider>
        </AuthProvider>
      </MathJaxContext>
    </AuthModeProvider>

  </StrictMode>,
)
