import { chatModelOptions, ConfigSchema } from "../../../../stores/chat/config";
import { useChatStore } from "../../instance";
import { useFetchCourseVectorstore } from "../../hooks/useFetchCourseVectorstores";
import type { ChangeEvent } from "react";
export function ChatModelPicker({ disabled = false }: { disabled?: boolean }) {
  const model = useChatStore((state) => state.config.model);
  const setModel = useChatStore((state) => state.setModel);

  return (
    <select
      aria-label="Chat model"
      title="Choose a Gemini model"
      value={model}
      disabled={disabled}
      onChange={(event) => {
        const result = ConfigSchema.shape.model.safeParse(event.target.value);
        if (result.success) setModel(result.data);
      }}
      className="h-8 min-w-0 max-w-32 rounded-md border border-border bg-surface px-2 text-xs text-text outline-none focus-visible:ring-2 focus-visible:ring-accent/60 disabled:cursor-not-allowed disabled:opacity-50 sm:h-10 sm:max-w-44 sm:text-sm"
    >
      {chatModelOptions.map(({ value, label }) => (
        <option key={value} value={value}>
          Gemini {label}
        </option>
      ))}
    </select>
  );
}

export function ChatCoursePicker({ disabled = false }: { disabled?: boolean }) {
  const { configs, error } = useFetchCourseVectorstore();
  const collectionName = useChatStore(
    (state) => state.config.course_collection_name,
  );
  const updateConfig = useChatStore((state) => state.updateConfig);

  const selectedCourse = configs.find(
    ({ vectorstore }) =>
      vectorstore != null &&
      vectorstore.collection_name === collectionName,
  );

  const handleChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const courseId = event.target.value;
    if (courseId === "default") {
      updateConfig({
        course_collection_name: null,
        course_name: null,
        embedding_model: null,
      });
      return;
    }

    const selected = configs.find(({ course }) => course.id === courseId);
    if (!selected?.vectorstore || selected.vectorstore.status !== "ready") {
      return;
    }

    updateConfig({
      course_collection_name: selected.vectorstore.collection_name,
      course_name: selected.course.name,
      embedding_model: selected.vectorstore.embedding_model,
    });
  };

  return (
    <select
      aria-label="Chat course"
      title={error ? "Unable to load courses" : "Choose a course"}
      value={selectedCourse?.course.id ?? "default"}
      disabled={disabled}
      onChange={handleChange}
      className="h-8 min-w-0 max-w-32 rounded-md border border-border bg-surface px-2 text-xs text-text outline-none focus-visible:ring-2 focus-visible:ring-accent/60 disabled:cursor-not-allowed disabled:opacity-50 sm:h-10 sm:max-w-44 sm:text-sm"
    >
      <option value="default">Default</option>
      {configs.map(({ course, vectorstore }) => {
        const ready = vectorstore?.status === "ready";

        return (
          <option key={course.id} value={course.id} disabled={!ready}>
            {course.name}{ready ? "" : " (unavailable)"}
          </option>
        );
      })}
      {error && <option disabled>Unable to load courses</option>}
    </select>
  );
}
