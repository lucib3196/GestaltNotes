import { MathJaxContext } from "better-react-mathjax";
import { Section } from "./components/Section";
import Chat from "./features/Chat/Chat";
const mathJaxConfig = {
  tex: {
    inlineMath: [["$", "$"]],
    displayMath: [["$$", "$$"]],
  },
};
import NavBar from "./components/NavBar/NavBar";

function App() {
  return (
    <MathJaxContext config={mathJaxConfig}>

      <NavBar />
      <Section>
        Content
      </Section>
      {/* <h1 className="text-3xl font-bold">Gestalt Chat</h1> */}
      {/* <Chat /> */}

      {/* <MarkDownEditor /> */}
    </MathJaxContext>
  );
}

export default App;
