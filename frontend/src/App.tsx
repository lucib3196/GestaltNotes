import { Section } from "./components/Section";

import NavBar from "./components/NavBar/NavBar";
import Chat from "./features/Chat/Chat";

function App() {
  return (
    <>
      <NavBar />
      <Section>
        <Chat />
      </Section>
      {/* <h1 className="text-3xl font-bold">Gestalt Chat</h1> */}
      {/* <Chat /> */}

      {/* <MarkDownEditor /> */}
    </>
  );
}

export default App;
