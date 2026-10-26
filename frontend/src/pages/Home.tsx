import { Link } from "react-router-dom";
import { useAuth } from "../features/Auth";

const highlights = [
  {
    title: "Ask a question",
    description:
      "Explore a topic, break down a difficult concept, or work through a problem.",
  },
  {
    title: "Choose a course",
    description:
      "Select an available course in chat to use its materials for your questions.",
  },
  {
    title: "Keep it general",
    description:
      "Leave the course picker on Default for questions beyond your courses.",
  },
];

export default function HomePage() {
  const { user } = useAuth();

  return (
    <main className="px-4 py-14 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-5xl">
        <section className="rounded-xl border border-border bg-surface p-8 shadow-soft sm:p-10">
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-accent">
            GestaltNotes
          </p>

          <h1 className="mt-3 max-w-3xl text-4xl font-semibold leading-tight text-text sm:text-5xl">
            A place to ask, learn, and make sense of your courses.
          </h1>

          <p className="mt-4 max-w-2xl text-base leading-relaxed text-text-muted sm:text-lg">
            Start a conversation about what you’re learning. Choose a course
            for help with its materials, or use Default for general questions.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-3">
            <Link
              to={user ? "/chat" : "/login"}
              className="rounded-lg bg-accent px-5 py-2.5 text-sm font-semibold text-bg transition hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-surface"
            >
              {user ? "Open Chat" : "Get Started"}
            </Link>

            {user && (
              <Link
                to="/account"
                className="rounded-lg border border-border-strong bg-button-secondary px-5 py-2.5 text-sm font-medium text-text transition hover:border-accent/50 hover:text-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
              >
                My Account
              </Link>
            )}
          </div>
        </section>

        <section
          aria-label="Ways to get started"
          className="mt-6 grid gap-4 sm:grid-cols-3"
        >
          {highlights.map(({ title, description }) => (
            <article
              key={title}
              className="rounded-lg border border-border bg-surface p-5"
            >
              <h2 className="text-base font-semibold text-text">{title}</h2>
              <p className="mt-2 text-sm leading-relaxed text-text-muted">
                {description}
              </p>
            </article>
          ))}
        </section>
      </div>
    </main>
  );
}
