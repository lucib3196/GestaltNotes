import { useNavigate } from "react-router-dom";
import Modal from "../../components/Modal/Modal";
import { CourseCard, CreateCourse } from "./components";
import { useFetchMyCourses } from "./hooks";
import { useState } from "react";
import { FiBookOpen, FiPlus } from "react-icons/fi";

export default function CourseManagement() {
  const navigate = useNavigate();
  const { courses, loading, error, refetch } = useFetchMyCourses();
  const [showModal, setShowModal] = useState<boolean>(false);

  function refreshCourses() {
    void refetch().catch(() => {
      // The fetch hook displays the error on the page.
    });
  }

  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-8 sm:px-6 lg:px-8">
      <header className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
        <div>
        <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-accent">Teaching workspace</p>
        <h1 className="text-3xl font-bold text-text">My courses</h1>
        <p className="mt-2 text-sm text-text-muted">
          A home for everything you teach. Create a course or pick up where you left off.
        </p>
        </div>
        <button type="button" onClick={() => setShowModal(true)} className="inline-flex shrink-0 items-center justify-center gap-2 self-start rounded-xl bg-accent px-5 py-3 text-sm font-semibold text-bg transition-colors hover:bg-accent-strong focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent">
          <FiPlus aria-hidden="true" size={18} /> Create course
        </button>
      </header>

      {showModal && <Modal setShowModal={setShowModal} className="sm:max-w-lg" contentClassName="px-6 pb-6 pt-0">
        <CreateCourse onCancel={() => setShowModal(false)} onCreated={() => {
          setShowModal(false);
          refreshCourses();
        }} />
      </Modal>}

      <section aria-labelledby="course-list-title" className="mt-4">
        <div className="mb-5 flex items-center gap-3 border-b border-border pb-4">
          <h2 id="course-list-title" className="text-base font-semibold text-text">Your courses</h2>
          {!loading && !error && <span className="rounded-full bg-surface-muted px-2.5 py-1 text-xs font-medium text-text-muted">{courses.length}</span>}
        </div>

        {loading && (
          <p role="status" className="py-10 text-center text-sm text-text-muted">Loading your courses…</p>
        )}

        {error && (
          <div role="alert" className="rounded-xl border border-border bg-surface p-6">
            <p className="font-medium text-text">We couldn’t load your courses.</p>
            <p className="mt-2 text-sm text-text-muted">{error.message}</p>
            <button type="button" disabled={loading} onClick={refreshCourses} className="mt-4 rounded-lg border border-border px-4 py-2 text-sm font-semibold text-accent hover:bg-surface-muted disabled:opacity-60">Try again</button>
          </div>
        )}
        {!loading && !error && courses.length === 0 && (
          <div className="flex flex-col items-center rounded-2xl border border-dashed border-border bg-surface px-6 py-16 text-center">
            <div className="mb-5 rounded-2xl bg-accent/10 p-4 text-accent"><FiBookOpen aria-hidden="true" size={28} /></div>
            <h3 className="text-lg font-semibold text-text">Your first course starts here</h3>
            <p className="mt-2 max-w-sm text-sm leading-6 text-text-muted">Give your course a name and a short description to get started.</p>
            <button type="button" onClick={() => setShowModal(true)} className="mt-6 inline-flex items-center gap-2 rounded-xl bg-accent px-5 py-3 text-sm font-semibold text-bg hover:bg-accent-strong focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"><FiPlus aria-hidden="true" size={18} /> Create your first course</button>
          </div>
        )}

        {!loading && !error && courses.length > 0 && <div className="grid auto-rows-fr gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {courses.map((course) => (
            <CourseCard
              key={course.id}
              course={course}
              onClick={(selectedCourse) =>
                navigate(`/educator/courses/${selectedCourse.id}`)
              }
            />
          ))}
        </div>}
      </section>
    </div>
  );
}
