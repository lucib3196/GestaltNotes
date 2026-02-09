import "./App.css";
import { MathJaxContext } from "better-react-mathjax";

import MarkDownEditor from "./components/MarkdownEditor/MarkdownEditor";

const mathJaxConfig = {
  tex: {
    inlineMath: [["$", "$"]],
    displayMath: [["$$", "$$"]],
  },
};

function App() {
  return (
    <MathJaxContext config={mathJaxConfig}>
      
      <MarkDownEditor />
    </MathJaxContext>
  );
}

export default App;
