import { useState } from "react";
import { FiBookOpen, FiLoader, FiPlus } from "react-icons/fi";
import { toast } from "react-toastify";

import { InputTextForm } from "../../../components/FormComponents";
import type { Course } from "../../../services/courses";
import { useCreateCourse } from "../hooks";

type CreateCourseProps = {
  onCreated?: (course: Course) => void;
  onCancel?: () => void;
};

export default function CreateCourse({ onCreated, onCancel }: CreateCourseProps) {
  const { createCourse, loading, error } = useCreateCourse();

  const [name, setName] = useState("");
  const [discipline, setDiscipline] = useState("");
  const [description, setDescription] = useState("");

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedName = name.trim();
    if (!trimmedName) {
      toast.error("Course name is required.");
      return;
    }

    try {
      const course = await createCourse({
        name: trimmedName,
        discipline: discipline.trim() || null,
        description: description.trim() || null,
      });

      setName("");
      setDiscipline("");
      setDescription("");
      toast.success("Course created.");
      onCreated?.(course);
    } catch {
      toast.error("Failed to create course.");
    }
  }

  return (
    <section className="">
      <div className="mb-6">
        <div className="mb-4 inline-flex rounded-xl bg-accent/10 p-3 text-accent"><FiBookOpen aria-hidden="true" size={24} /></div>
        <h2 className="text-2xl font-semibold tracking-tight text-text">Create a course</h2>
        <p className="mt-2 text-sm leading-6 text-text-muted">
          Start with the basics. Give your course a name and a little context.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <InputTextForm
          id="course-name"
          label="Course name"
          variant="auth"
          value={name}
          onChange={(event) => setName(event.target.value)}
          placeholder="Mechanics"
          required
        />

        <InputTextForm
          id="course-discipline"
          label="Discipline (optional)"
          variant="auth"
          value={discipline}
          onChange={(event) => setDiscipline(event.target.value)}
          placeholder="Physics"
        />

        <div className="w-full">
          <label
            htmlFor="course-description"
            className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-text-soft"
          >
            Description (optional)
          </label>
          <textarea
            id="course-description"
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            placeholder="A short summary of the course"
            rows={4}
            className="block w-full resize-none rounded-lg border border-border bg-surface-strong px-3.5 py-2.5 text-sm text-text shadow-sm outline-none transition-all duration-200 placeholder:text-text-soft focus:border-accent focus:ring-2 focus:ring-accent/35"
          />
        </div>

        {error && <p className="text-sm text-red-400">{error.message}</p>}

        <div className="mt-2 flex items-center justify-end gap-3 border-t border-border pt-5">
          {onCancel && <button type="button" onClick={onCancel} disabled={loading} className="rounded-xl border border-border px-4 py-2.5 text-sm font-medium text-text-muted hover:bg-surface-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-60">Cancel</button>}
          <button type="submit" disabled={loading} className="inline-flex items-center justify-center gap-2 rounded-xl bg-accent px-5 py-2.5 text-sm font-semibold text-bg hover:bg-accent-strong focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:cursor-not-allowed disabled:opacity-60">
            {loading ? <FiLoader aria-hidden="true" className="motion-safe:animate-spin" size={16} /> : <FiPlus aria-hidden="true" size={16} />}
            {loading ? "Creating…" : "Create course"}
          </button>
        </div>
      </form>
    </section>
  );
}
