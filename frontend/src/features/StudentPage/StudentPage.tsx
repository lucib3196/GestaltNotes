import NavBar from "../../components/NavBar/NavBar";
import { Section } from "../../components/Section";
import { Chat } from "../Chat";

export default function StudentPage() {
    return (
        <>
            <NavBar />
            <Section>
                <Chat />
            </Section>
        </>
    );
}