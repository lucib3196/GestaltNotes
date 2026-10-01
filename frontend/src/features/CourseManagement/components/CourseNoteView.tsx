import type { CourseNote } from "../../../services/courses";
import type { SupportedContentType } from "../../../services/courses/types";
type Props = {
  note: CourseNote;
};

export function CourseNoteTypeDropDown() {
  function updateResourceType(index: number, resourceType: TType) {
    setItems((current) =>
      current.map((item, itemIndex) =>
        itemIndex === index ? { ...item, resourceType } : item,
      ),
    );
  }
  return (
    <div>
      <select
        value={item.resourceType}
        onChange={(event) =>
          updateResourceType(index, event.target.value as TType)
        }
        className="mt-3 w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text outline-none focus:border-accent focus:ring-2 focus:ring-accent/35"
      >
        {resourceTypes.map((type) => (
          <option key={type} value={type}>
            {type}
          </option>
        ))}
      </select>
    </div>
  );
}
export function CourseNoteView({ note }: Props) {
  return (
    <article className="rounded-lg border border-border bg-surface-muted p-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0">
          <p className="truncate font-semibold text-text">{note.title}</p>
          <p className="mt-1 text-sm text-text-muted">{note.resource_type}</p>
        </div>
      </div>
    </article>
  );
}
