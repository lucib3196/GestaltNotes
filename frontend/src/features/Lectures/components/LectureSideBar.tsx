import type { GroupedFiles, FileEntry } from "../models/lecture.types"
import { getFileName } from "../utils";


type LectureSideBarProps = {
    grouped: GroupedFiles,
    setSelected: (val: FileEntry) => void
}
export default function LectureSideBar({ grouped, setSelected }: LectureSideBarProps) {
    return (
        <aside className="h-full rounded-lg border border-border bg-surface/80 p-4 shadow-soft backdrop-blur-sm">
            <div className="mb-3">
                <h2 className="text-sm font-semibold uppercase tracking-wide text-text-muted">Lecture Files</h2>
            </div>

            <div className="space-y-4">
                {Object.entries(grouped).map(([parent, parentFiles]) => {
                    const lectureName = parent.split("/").at(-1);

                    return (
                        <section
                            key={parent}
                            className="rounded-md border border-border/70 bg-surface-muted/60 p-3"
                        >
                            <h3 className="mb-2 text-sm font-semibold text-text">
                                Lecture Name : <span className="text-accent">{lectureName}</span>
                            </h3>

                            <ul className="space-y-1.5">
                                {parentFiles.map((f) => {
                                    const fileName = getFileName(f)
                                    return (
                                        <li key={f.path}>
                                            <button
                                                type="button"
                                                onClick={() => setSelected(f)}
                                                className="w-full rounded-md border border-transparent bg-surface/40 px-3 py-2 text-left text-sm text-text-muted transition-all duration-base ease-base hover:border-border-strong hover:bg-surface hover:text-text"
                                            >
                                                {fileName}
                                            </button>
                                        </li>
                                    )
                                })}
                            </ul>
                        </section>
                    );
                })}
            </div>
        </aside>
    )
}
