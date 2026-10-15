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
      set((state) => ({
        error: null,
        items: [
          ...state.items,
          ...files.map((file) => ({
            id: crypto.randomUUID(),
            file,
            resourceType: "notes" as const,
          })),
        ],
      }) as Partial<Store>);
    },

    removeFile: (id) => {
      if (get().uploading) return;
      set((state) => ({
        items: state.items.filter((item) => item.id !== id),
        previewID: state.previewID === id ? null : state.previewID,
      }) as Partial<Store>);
    },

    updateResourceType: (id, resourceType) => {
      if (get().uploading) return;
      set((state) => ({
        items: state.items.map((item) =>
          item.id === id ? { ...item, resourceType } : item,
        ),
      }) as Partial<Store>);
    },

    togglePreview: (id) => {
      if (!get().items.some((item) => item.id === id)) return;
      set((state) => ({
        previewID: state.previewID === id ? null : id,
      }) as Partial<Store>);
    },

    beginUpload: () => {
      const { items, uploading } = get();
      if (uploading || items.length === 0) return null;
      set({ uploading: true, error: null } as Partial<Store>);
      return [...items];
    },

    completeFile: (id) => {
      set((state) => ({
        items: state.items.filter((item) => item.id !== id),
        previewID: state.previewID === id ? null : state.previewID,
      }) as Partial<Store>);
    },

    finishUpload: (error) => {
      set({ uploading: false, error: error ?? null } as Partial<Store>);
    },
  });
}
