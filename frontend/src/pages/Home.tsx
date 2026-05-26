import { Link } from "react-router-dom";
import { useAuth } from "../context";

type CourseInfo = {
  id: string;
  title: string;
  description: string;
  active: boolean;
};

const courses: CourseInfo[] = [
  {
    id: "me116",
    title: "ME116 Heat Transfer",
    description:
      "Course-focused study chat for conduction, convection, radiation, and heat exchanger problem solving.",
    active: true,
  },
];

const me116Highlights = [
  "Conduction and thermal resistance intuition",
  "Convection setup and interpretation support",
  "Heat exchanger and exam-prep question practice",
];

export default function HomePage() {
  const { user } = useAuth();
  const activeCourse = courses.find((course) => course.active);

  return (
    <main className="relative overflow-hidden px-4 py-14 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-5xl">
        <section className="rounded-xl border border-border bg-surface p-8 shadow-soft sm:p-10">
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-accent">
            GestaltNotes
          </p>

          <h1 className="mt-3 max-w-3xl text-4xl font-semibold leading-tight text-text sm:text-5xl">
            Study Heat Transfer Through Conversation
          </h1>

          <p className="mt-4 max-w-2xl text-base leading-relaxed text-text-muted sm:text-lg">
            ME116 Study Chat helps you ask better questions, get clear
            explanations, and keep momentum when conduction, convection, or
            radiation problems get difficult.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-3">
            <Link
              to="/chat"
              className="rounded-lg bg-accent px-5 py-2.5 text-sm font-semibold text-bg transition hover:opacity-90"
            >
              Open Chat
            </Link>

            {user ? (
              <Link
                to="/account"
                className="rounded-lg border border-border-strong bg-button-secondary px-5 py-2.5 text-sm font-medium text-text transition hover:border-accent/50 hover:text-accent"
              >
                My Account
              </Link>
            ) : (
              <Link
                to="/login"
                className="rounded-lg border border-border-strong bg-button-secondary px-5 py-2.5 text-sm font-medium text-text transition hover:border-accent/50 hover:text-accent"
              >
                Log In
              </Link>
            )}
          </div>
        </section>

        {activeCourse && (
          <section className="mt-8 grid gap-4 sm:grid-cols-3">
            <article className="sm:col-span-3 rounded-lg border border-border bg-surface-strong p-5">
              <p className="font-mono text-xs uppercase tracking-[0.16em] text-text-soft">
                Active Course
              </p>
              <h2 className="mt-2 text-2xl font-semibold text-text">
                {activeCourse.title}
              </h2>
              <p className="mt-2 text-sm leading-relaxed text-text-muted">
                {activeCourse.description}
              </p>
            </article>

            {me116Highlights.map((highlight) => (
              <article
                key={highlight}
                className="rounded-lg border border-border bg-surface p-4"
              >
                <p className="text-sm text-text">{highlight}</p>
              </article>
            ))}
          </section>
        )}
      </div>
    </main>
  );
}
