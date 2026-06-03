import type { GroupedFiles, FileEntry } from "../models/lecture.types";
import { getFileName } from "../utils";
import { useState } from "react";
import {
    IoIosArrowDropdownCircle,
    IoIosArrowDroprightCircle,
} from "react-icons/io";
import { GiHamburgerMenu } from "react-icons/gi";
type LectureSideBarProps = {
    grouped: GroupedFiles;
    selected: FileEntry | null,
    setSelected: (val: FileEntry) => void;
};
function LectureDropDown({
    parent,
    files,
    selected,
    setSelected,
}: {
    parent?: string;
    files: FileEntry[];
    selected: FileEntry | null
    setSelected: (file: FileEntry) => void;
}) {
    const [isOpen, setIsOpen] = useState<boolean>(false)

    return (
        <section
            key={parent}
            className="rounded-md border border-border/70 bg-surface-muted/60 p-3"
        >
            <button className="flex flex-row justify-baseline gap-1" role="button" onClick={() => setIsOpen(prev => !prev)}>
                {isOpen ? <IoIosArrowDropdownCircle /> : <IoIosArrowDroprightCircle />}
                <h3 className="flex flex-row mb-2 text-sm font-semibold text-text">
                    {parent ?? "Untitled Lecture"}
                </h3>
            </button>
            {isOpen && (<ul className="space-y-1.5">
                {files.map((f) => {
                    const fileName = getFileName(f);
                    const isSelected = selected?.path === f.path;

                    return (
                        <li key={f.path}>
                            <button
                                type="button"
                                onClick={() => setSelected(f)}
                                className={`w-full rounded-md border px-3 py-2 text-left text-sm transition-all duration-base ease-base ${isSelected
                                    ? "border-primary bg-primary/10 text-primary shadow-sm"
                                    : "border-transparent bg-surface/40 text-text-muted hover:border-border-strong hover:bg-surface hover:text-text"
                                    }`}
                            >
                                {fileName === "output.json" ? "Lecture Cards" : fileName}
                            </button>
                        </li>
                    );
                })}
            </ul>)}
        </section>
    );
}

export default function LectureSideBar({
    grouped,
    selected,
    setSelected,
}: LectureSideBarProps) {
    const [sidebarOpen, setSidebarOpen] = useState(true);

    const priorityFiles: Record<string, number> = {
        "output.json": 1,
    };

    const sidebarWidth = sidebarOpen ? "w-[320px]" : "w-14";
    const buttonLabel = sidebarOpen ? "Close Menu" : "Open Menu";

    return (
        <aside
            className={`${sidebarWidth} min-h-0 overflow-hidden border-r border-border bg-surface transition-all duration-base ease-base`}
        >
            <div className="flex h-full min-h-0 flex-col">
                <div className="flex items-center justify-between gap-2 border-b border-border px-3 py-2">
                    {sidebarOpen && (
                        <div>
                            <h2 className="text-sm font-semibold uppercase tracking-wide text-text-muted">
                                Course Notes
                            </h2>

                        </div>
                    )}

                    {/* Info */}

                    <button
                        type="button"
                        aria-label={buttonLabel}
                        title={buttonLabel}
                        onClick={() => setSidebarOpen((prev) => !prev)}
                        className="inline-flex size-9 shrink-0 items-center justify-center rounded-md border border-border bg-surface text-text transition-all duration-base ease-base hover:border-border-strong hover:bg-surface-strong"
                    >
                        <GiHamburgerMenu />
                    </button>
                </div>

                {sidebarOpen && (
                    <div className="min-h-0 flex-1 space-y-4 overflow-y-auto p-3">
                        {Object.entries(grouped).map(([parent, parentFiles]) => {
                            const lectureName = parent.split("/").at(-1);
                            const sortedFiles = parentFiles.sort((a, b) => {
                                const aPriority =
                                    priorityFiles[getFileName(a)] ?? Number.MAX_SAFE_INTEGER;
                                const bPriority =
                                    priorityFiles[getFileName(b)] ?? Number.MAX_SAFE_INTEGER;
                                return aPriority - bPriority;
                            });

                            return (
                                <LectureDropDown
                                    key={parent}
                                    parent={lectureName}
                                    files={sortedFiles}
                                    selected={selected}
                                    setSelected={setSelected}
                                />
                            );
                        })}
                    </div>
                )}
            </div>
        </aside>
    );
}



export  function HomeworkSideBar({
    grouped,
    selected,
    setSelected,
}: LectureSideBarProps) {
    const [sidebarOpen, setSidebarOpen] = useState(true);

    const priorityFiles: Record<string, number> = {
        "output.json": 1,
    };

    const sidebarWidth = sidebarOpen ? "w-[320px]" : "w-14";
    const buttonLabel = sidebarOpen ? "Close Menu" : "Open Menu";

    return (
        <aside
            className={`${sidebarWidth} min-h-0 overflow-hidden border-r border-border bg-surface transition-all duration-base ease-base`}
        >
            <div className="flex h-full min-h-0 flex-col">
                <div className="flex items-center justify-between gap-2 border-b border-border px-3 py-2">
                    {sidebarOpen && (
                        <div>
                            <h2 className="text-sm font-semibold uppercase tracking-wide text-text-muted">
                                Course Notes
                            </h2>

                        </div>
                    )}

                    {/* Info */}

                    <button
                        type="button"
                        aria-label={buttonLabel}
                        title={buttonLabel}
                        onClick={() => setSidebarOpen((prev) => !prev)}
                        className="inline-flex size-9 shrink-0 items-center justify-center rounded-md border border-border bg-surface text-text transition-all duration-base ease-base hover:border-border-strong hover:bg-surface-strong"
                    >
                        <GiHamburgerMenu />
                    </button>
                </div>

                {sidebarOpen && (
                    <div className="min-h-0 flex-1 space-y-4 overflow-y-auto p-3">
                        {Object.entries(grouped).map(([parent, parentFiles]) => {
                            const lectureName = parent.split("/").at(-1);
                            const sortedFiles = parentFiles.sort((a, b) => {
                                const aPriority =
                                    priorityFiles[getFileName(a)] ?? Number.MAX_SAFE_INTEGER;
                                const bPriority =
                                    priorityFiles[getFileName(b)] ?? Number.MAX_SAFE_INTEGER;
                                return aPriority - bPriority;
                            });

                            return (
                                <LectureDropDown
                                    key={parent}
                                    parent={lectureName}
                                    files={sortedFiles}
                                    selected={selected}
                                    setSelected={setSelected}
                                />
                            );
                        })}
                    </div>
                )}
            </div>
        </aside>
    );
}

