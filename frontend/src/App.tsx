
import { MathJaxContext } from "better-react-mathjax";
import ViewNotes from "./pages/NotesPage";
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
      <ViewNotes />

      {/* <MarkDownEditor /> */}
    </MathJaxContext>
  );
}

export default App;
