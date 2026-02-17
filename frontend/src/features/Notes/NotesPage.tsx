import { useEffect } from "react";
import { NotesAPI } from "../../services";
import { useState } from "react";
import NoteCard from "./NoteCard";


interface Note {
    name: string;
}

export default function NotesPage() {
    const [notes, setNotes] = useState<Note[]>([]);
    const [currentNote, setCurrentNote] = useState<string | null>(null);

    useEffect(() => {
        const getNotes = async () => {
            const res = await NotesAPI.getNotes();

            setNotes(
                res.map((v) => ({
                    name: v.split("/").at(-1) ?? "Untitled",
                }))
            );
        };

        getNotes();
    }, []);

    return (
        <div className="flex flex-col w-1/2">
            <h1 className="text-lg font-semibold mb-4">Notes</h1>

            {notes.map((note) => (
                <NoteCard
                    key={note.name}
                    name={note.name}
                    selected={currentNote === note.name}
                    onSelect={() => setCurrentNote(note.name)}
                />
            ))}

            <div className="mt-4 text-sm text-slate-600">
                Selected Note: {currentNote ?? ""}
            </div>
        </div>
    );
}
