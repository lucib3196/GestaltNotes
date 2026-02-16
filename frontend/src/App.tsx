
import { Section } from "./components/Section";
import Chat from "./features/Chat/Chat";
import { useAuth } from "./context";
import NavBar from "./components/NavBar/NavBar";

function App() {
  
  return (
    <>


      <NavBar />
      <Section>
        Content
      </Section>
      {/* <h1 className="text-3xl font-bold">Gestalt Chat</h1> */}
      {/* <Chat /> */}

      {/* <MarkDownEditor /> */}
    </>
  );
}

export default App;
