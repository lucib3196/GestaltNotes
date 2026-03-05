import { Section } from "./components/Section";

import NavBar from "./components/NavBar/NavBar";
import { Chat } from "./features/Chat";
import { useAuth } from "./context";

function App() {
  const { user } = useAuth();

  return (
    <>
      <NavBar />

      <Section>
        {user ? (
          <Chat />
        ) : (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <h2 className="text-xl font-semibold text-slate-800">
              Please login to continue
            </h2>

            <p className="text-slate-500 mt-2">
              You must be logged in to use the lecture tutor.
            </p>
          </div>
        )}
      </Section>
    </>
  );
}

export default App;
