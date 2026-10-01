import { useState, type FormEvent } from "react";
import { MdOutlineEdit } from "react-icons/md";

import type { Course } from "../../../services/courses";
import { useEditCourse } from "../../CourseManagement/hooks";

const fieldClass =
  "w-full rounded-lg border border-border bg-surface-strong px-3 py-2 text-sm text-text outline-none focus:border-accent focus:ring-2 focus:ring-accent/35 disabled:opacity-60";

const buttonClass =
  "inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:cursor-not-allowed disabled:opacity-60";

export default function CourseHeader({
  course,
  refetch,
}: {
  course: Course;
  refetch?: () => void;
}) {
  const { updateCourse, loading: updating } = useEditCourse();
  const [editing, setEditing] = useState(false);
  const [name, setName] = useState("");
  const [discipline, setDiscipline] = useState("");
  const [description, setDescription] = useState("");
  const [saveError, setSaveError] = useState<string | null>(null);

  function handleEdit() {
    setName(course.name);
    setDiscipline(course.discipline ?? "");
    setDescription(course.description ?? "");
    setSaveError(null);
    setEditing(true);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (updating || !name.trim()) return;

    setSaveError(null);

    try {
      await updateCourse(course.id, {
        name: name.trim(),
        discipline: discipline.trim() || null,
        description: description.trim() || null,
      });
    } catch (error) {
      setSaveError(
        error instanceof Error ? error.message : "Unable to save changes.",
      );
      return;
    }

    setEditing(false);
    refetch?.();
  }

  return (
    <section className="border-b border-border pb-8">
      {editing ? (
        <form onSubmit={handleSubmit} className="max-w-3xl space-y-5">
          <div>
            <h2 className="text-lg font-semibold text-text">Edit course</h2>
            <p className="mt-1 text-sm text-text-muted">
              Update the course name, discipline, and description.
            </p>
          </div>

          <fieldset disabled={updating} className="space-y-5">
            <label className="block">
              <span className="mb-2 block text-sm font-medium text-text">
                Course name
              </span>
              <input
                value={name}
                onChange={(event) => setName(event.target.value)}
                className={fieldClass}
                autoFocus
                required
              />
            </label>

            <label className="block">
              <span className="mb-2 block text-sm font-medium text-text">
                Discipline
                <span className="ml-2 font-normal text-text-muted">
                  Optional
                </span>
              </span>
              <input
                value={discipline}
                onChange={(event) => setDiscipline(event.target.value)}
                className={fieldClass}
                placeholder="e.g. Biology"
              />
            </label>

            <label className="block">
              <span className="mb-2 block text-sm font-medium text-text">
                Description
                <span className="ml-2 font-normal text-text-muted">
                  Optional
                </span>
              </span>
              <textarea
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                rows={4}
                className={`${fieldClass} resize-y leading-6`}
                placeholder="What will students learn in this course?"
              />
            </label>
          </fieldset>

          {saveError && (
            <p role="alert" className="text-sm text-text">
              Couldn’t save changes: {saveError}
            </p>
          )}

          <div className="flex flex-wrap gap-2">
            <button
              type="submit"
              disabled={updating || !name.trim()}
              className={`${buttonClass} bg-accent text-bg hover:bg-accent-strong`}
            >
              {updating ? "Saving..." : "Save changes"}
            </button>
            <button
              type="button"
              onClick={() => setEditing(false)}
              disabled={updating}
              className={`${buttonClass} text-text-muted hover:bg-surface-muted hover:text-text`}
            >
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <>
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div className="min-w-0">
              <p className="text-sm font-medium text-text-muted">Course</p>
              <h1 className="mt-1 wrap-break-word text-3xl font-bold tracking-tight text-text">
                {course.name}
              </h1>
              <p className="mt-2 text-sm text-text-muted">
                {course.discipline?.trim() || "No discipline added"}
              </p>
            </div>

            <button
              type="button"
              onClick={handleEdit}
              className={`${buttonClass} shrink-0 self-start text-accent hover:bg-accent/10`}
            >
              <MdOutlineEdit aria-hidden="true" className="text-lg" />
              Edit course
            </button>
          </div>

          <div className="mt-6 max-w-3xl">
            <h2 className="text-sm font-semibold text-text">
              About this course
            </h2>
            <p className="mt-2 whitespace-pre-wrap wrap-break-word text-sm leading-7 text-text-muted">
              {course.description?.trim() || "No description added yet."}
            </p>
          </div>
        </>
      )}
    </section>
  );
}
