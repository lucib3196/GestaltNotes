import type { StateCreator } from "zustand";
import type { CourseStore, CourseNoteStore } from "./state";
import { setItemsById } from "../../utils/utils";

export type CourseSliceCreator = StateCreator<CourseStore, [], [], CourseStore>;

export type CourseNoteSliceCreator = StateCreator<
  CourseNoteStore,
  [],
  [],
  CourseNoteStore
>;

export function createCourseStore<
  Store extends CourseStore = CourseStore,
>(): CourseSliceCreator {
  return (set) => ({
    selectedCourseId: "",
    selectedCourse: null,
    setSelectedCourseId: (id) => {
      set(
        (state) =>
          ({
            selectedCourseId: id,
            selectedCourse:
              state.selectedCourse?.id === id ? state.selectedCourse : null,
          }) as Partial<Store>,
      );
    },
    setSelectedCourse: (course) => {
      set(
        (state) =>
          ({
            selectedCourse: course,
            selectedCourseId: course?.id ?? state.selectedCourseId,
          }) as Partial<Store>,
      );
    },
  });
}

export function createCourseNoteStore(): CourseNoteSliceCreator {
  return (set, get) => ({
    notesById: {},
    selectedNoteID: null,
    checkedNoteIds: [],
    notesLoading: false,
    notesError: null,
    setNotes: (notes) => {
      const byId = setItemsById(notes);
      set({
        notesById: byId,
      });
    },
    removeNotes: (ids) =>
      set((state) => {
        const removed = new Set(ids);
        return {
          notesById: setItemsById(
            Object.values(state.notesById).filter(
              (note) => !removed.has(note.id),
            ),
          ),
        };
      }),
    selectNote: (id) => set({ selectedNoteID: id }),
    getSelectedNote: () => {
      const { selectedNoteID, notesById } = get();
      return selectedNoteID === null
        ? null
        : notesById[selectedNoteID] ?? null;
    },
    toggleCheckedNote: (id) =>
      set((state) => ({
        checkedNoteIds: state.checkedNoteIds.includes(id)
          ? state.checkedNoteIds.filter((currentId) => currentId != id)
          : [...state.checkedNoteIds, id],
      })),
    clearCheckedNotes: () => set({ checkedNoteIds: [] }),
    setNotesLoading: (loading) => set({ notesLoading: loading }),
    setNotesError: (error) => set({ notesError: error }),
  });
}
