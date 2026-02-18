import { Section } from "./components/Section";
import { PDFViewer } from "./components/Viewer/PDFViewer";
import NavBar from "./components/NavBar/NavBar";
import Chat from "./features/Chat/Chat";

function App() {
  return (
    <>
      <NavBar />
      <Section>
        {/* <PDFViewer src={"http://localhost:5173/src/assets/9-26-25.pdf"} /> */}
        <Chat />
      </Section>
      {/* <h1 className="text-3xl font-bold">Gestalt Chat</h1> */}
      {/* <Chat /> */}

      {/* <MarkDownEditor /> */}
    </>
  );
}

export default App;
