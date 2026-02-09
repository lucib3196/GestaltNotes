import { NotesAPI } from "../services";
import { useEffect, useState } from "react";

export default function ViewNotes() {
    const [notes, setNotes] = useState<string[]>([])

    const getNotes = async () => {
        try {
            const response = await NotesAPI.getNotes()
            console.log(response)
            return response
        }
        catch (error: any) {
            console.log(error)
        }
    }
    useEffect(() => {
        const set = async () => setNotes(await getNotes())
        set()
    }, [])


    return <div>
        <h1>Notes</h1>
        {notes.map((v) => <p className="text-black">{v}</p>)}
    </div>
}