type NoteCardProps = {
    name: string;
    selected: boolean;
    onSelect: () => void;
};

export default function NoteCard({
    name,
    selected,
    onSelect,
}: NoteCardProps) {
    return (
        <div
            onClick={onSelect}
            className={`
        group
        px-4 py-2.5
        rounded-lg
        transition-all duration-200
        cursor-pointer
        text-sm
        font-medium
        border
        ${selected
                    ? "bg-blue-50 border-blue-300 text-blue-700"
                    : "bg-white border-transparent text-slate-700 hover:bg-slate-100"
                }
      `}
        >
            {name}
        </div>
    );
}
