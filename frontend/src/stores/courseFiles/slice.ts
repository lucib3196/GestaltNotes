import type { StateCreator } from "zustand";
import type { CourseFileStore } from "./state";

export function createCourseFileSlice<
  Store extends CourseFileStore = CourseFileStore,
>(): StateCreator<Store, [], [], CourseFileStore> {
  return (set, get) => ({
    items: [],
    previewID: null,
    uploading: false,
    error: null,

    addFiles: (files) => {
      if (get().uploading) return;
      set(
        (state) =>
          ({
            error: null,
            items: [
              ...state.items,
              ...files.map((file) => ({
                id: crypto.randomUUID(),
                file,
                resourceType: "notes" as const,
              })),
            ],
          }) as Partial<Store>,
      );
    },

    removeFile: (id) => {
      if (get().uploading) return;
      set(
        (state) =>
          ({
            items: state.items.filter((item) => item.id !== id),
            previewID: state.previewID === id ? null : state.previewID,
          }) as Partial<Store>,
      );
    },

    updateResourceType: (id, resourceType) => {
      if (get().uploading) return;
      set(
        (state) =>
          ({
            items: state.items.map((item) =>
              item.id === id ? { ...item, resourceType } : item,
            ),
          }) as Partial<Store>,
      );
    },
  });
}
