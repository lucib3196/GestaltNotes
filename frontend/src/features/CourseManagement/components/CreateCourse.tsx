import { useState } from "react";
import { toast } from "react-toastify";

import { InputTextForm } from "../../../components/FormComponents";
import type { Course } from "../../../services/courses";
import { useCreateCourse } from "../hooks";

type CreateCourseProps = {
  onCreated?: (course: Course) => void;
};

export default function CreateCourse({ onCreated }: CreateCourseProps) {
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
    <section className="rounded-xl border border-border bg-surface p-5 shadow-soft">
      <div className="mb-5">
        <h2 className="text-lg font-semibold text-text">Create course</h2>
        <p className="mt-1 text-sm text-text-muted">
          Add a course workspace for notes, materials, and student access.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <InputTextForm
          id="course-name"
          label="Course Name"
          variant="auth"
          value={name}
          onChange={(event) => setName(event.target.value)}
          placeholder="Mechanics"
          required
        />

        <InputTextForm
          id="course-discipline"
          label="Discipline"
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
            Description
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

        <button
          type="submit"
          disabled={loading}
          className="w-fit rounded-lg bg-accent px-4 py-2.5 text-sm font-semibold text-bg transition-colors hover:bg-accent-strong disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? "Creating..." : "Create Course"}
        </button>
      </form>
    </section>
  );
}
