import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { useEditCourse, useGetCourse } from "./hooks";

export default function SingleCourse() {
  const navigate = useNavigate();
  const { courseId } = useParams();
  const { course, loading, error, refetch } = useGetCourse(courseId);
  const {
    updateCourse,
    loading: updating,
    error: updateError,
  } = useEditCourse();
  const [editing, setEditing] = useState(false);
  const [name, setName] = useState("");
  const [discipline, setDiscipline] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    if (!course) return;

    setName(course.name);
    setDiscipline(course.discipline ?? "");
    setDescription(course.description ?? "");
  }, [course]);

  function handleCancel() {
    if (!course) return;

    setName(course.name);
    setDiscipline(course.discipline ?? "");
    setDescription(course.description ?? "");
    setEditing(false);
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!course) return;

    await updateCourse(course.id, {
      name: name.trim(),
      discipline: discipline.trim() || null,
      description: description.trim() || null,
    });
    await refetch();
    setEditing(false);
  }

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-6 px-4 py-8 sm:px-6 lg:px-8">
      <button
        type="button"
        onClick={() => navigate("/educator/courses")}
        className="w-fit rounded-lg border border-border bg-surface px-4 py-2 text-sm font-semibold text-text transition-colors hover:bg-surface-muted"
      >
        Back to courses
      </button>

      {loading && <p className="text-sm text-text-muted">Loading course...</p>}
      {error && <p className="text-sm text-red-400">{error.message}</p>}
      {updateError && (
        <p className="text-sm text-red-400">{updateError.message}</p>
      )}

      {course && (
        <form
          onSubmit={handleSubmit}
          className="rounded-xl border border-border bg-surface p-6 shadow-soft"
        >
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <p className="text-sm font-medium text-text-muted">
                Course Overview
              </p>
              {editing ? (
                <input
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  className="mt-1 w-full rounded-lg border border-border bg-surface-strong px-3 py-2 text-3xl font-bold text-text outline-none focus:border-accent focus:ring-2 focus:ring-accent/35"
                  required
                />
              ) : (
                <h1 className="mt-1 text-3xl font-bold text-text">
                  {course.name}
                </h1>
              )}
            </div>

            <div className="flex gap-2">
              {editing ? (
                <>
                  <button
                    type="button"
                    onClick={handleCancel}
                    disabled={updating}
                    className="rounded-lg border border-border bg-surface px-4 py-2 text-sm font-semibold text-text transition-colors hover:bg-surface-muted disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={updating}
                    className="rounded-lg bg-accent px-4 py-2 text-sm font-semibold text-bg transition-colors hover:bg-accent-strong disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {updating ? "Saving..." : "Save"}
                  </button>
                </>
              ) : (
                <button
                  type="button"
                  onClick={() => setEditing(true)}
                  className="rounded-lg border border-border bg-surface px-4 py-2 text-sm font-semibold text-text transition-colors hover:bg-surface-muted"
                >
                  Edit
                </button>
              )}
            </div>
          </div>

          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            <label className="rounded-lg border border-border bg-surface-muted p-4">
              <span className="text-xs font-semibold uppercase tracking-wide text-text-soft">
                Discipline
              </span>
              {editing ? (
                <input
                  value={discipline}
                  onChange={(event) => setDiscipline(event.target.value)}
                  className="mt-2 block w-full rounded-lg border border-border bg-surface-strong px-3 py-2 text-sm text-text outline-none focus:border-accent focus:ring-2 focus:ring-accent/35"
                  placeholder="No discipline set"
                />
              ) : (
                <p className="mt-2 text-sm text-text">
                  {course.discipline ?? "No discipline set"}
                </p>
              )}
            </label>

            <div className="rounded-lg border border-border bg-surface-muted p-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-text-soft">
                Storage Prefix
              </p>
              <p className="mt-2 break-words text-sm text-text">
                {course.storage_prefix ?? "No storage prefix set"}
              </p>
            </div>
          </div>

          <label className="mt-4 block rounded-lg border border-border bg-surface-muted p-4">
            <span className="text-xs font-semibold uppercase tracking-wide text-text-soft">
              Description
            </span>
            {editing ? (
              <textarea
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                rows={5}
                className="mt-2 block w-full resize-none rounded-lg border border-border bg-surface-strong px-3 py-2 text-sm leading-6 text-text outline-none focus:border-accent focus:ring-2 focus:ring-accent/35"
                placeholder="No description set"
              />
            ) : (
              <p className="mt-2 text-sm leading-6 text-text">
                {course.description ?? "No description set"}
              </p>
            )}
          </label>
        </form>
      )}
    </div>
  );
}
