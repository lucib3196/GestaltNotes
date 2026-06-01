import { useGenContentProvider } from "../features/GeneratedContent";
import { useAuth } from "../context";
import { useState, useEffect, useMemo } from "react";
import { RenderMCQSingle } from "../features/MCQ";


export default function MyGeneratedContentPage() {
    const { user } = useAuth();
    const quizzes = useGenContentProvider((s) => s.quizes);
    const getMyQuizzes = useGenContentProvider((s) => s.setQuizes);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [page, setPage] = useState(1);
    const [selectedByQuestion, setSelectedByQuestion] = useState<Record<number, number | null>>({});
    const [submittedByQuestion, setSubmittedByQuestion] = useState<Record<number, boolean>>({});

    const pageSize = 4;
    const totalPages = Math.max(1, Math.ceil(quizzes.length / pageSize));

    const visibleQuizzes = useMemo(() => {
        const start = (page - 1) * pageSize;
        return quizzes.slice(start, start + pageSize);
    }, [quizzes, page]);
    const submittedCount = useMemo(
        () => Object.values(submittedByQuestion).filter(Boolean).length,
        [submittedByQuestion],
    );

    useEffect(() => {
        let isMounted = true;

        const load = async () => {
            if (!user) return;
            setLoading(true);
            setError(null);

            try {
                const token = await user.getIdToken();
                if (!isMounted) return;
                await getMyQuizzes(token);
            } catch (e) {
                if (!isMounted) return;
                setError(e instanceof Error ? e.message : "Failed to load quizzes");
            } finally {
                if (isMounted) setLoading(false);
            }
        };

        load();

        return () => {
            isMounted = false;
        };
    }, [user, getMyQuizzes]);

    useEffect(() => {
        if (page > totalPages) setPage(totalPages);
    }, [page, totalPages]);

    const handleSelect = (questionIndex: number, selectedIndex: number) => {
        if (submittedByQuestion[questionIndex]) return;
        setSelectedByQuestion((prev) => ({ ...prev, [questionIndex]: selectedIndex }));
    };

    const handleSubmitQuestion = (questionIndex: number) => {
        if (selectedByQuestion[questionIndex] == null) return;
        setSubmittedByQuestion((prev) => ({ ...prev, [questionIndex]: true }));
    };

    const handleResetQuestion = (questionIndex: number) => {
        setSubmittedByQuestion((prev) => ({ ...prev, [questionIndex]: false }));
    };

    if (!user) return <div>Please sign in.</div>;
    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;
    if (!quizzes.length) return <div>No generated questions yet.</div>;

    return (
        <div className="mx-auto w-full max-w-5xl px-4 py-6 sm:px-6 lg:px-8">
            <div className="mb-6 rounded-xl border border-border bg-surface p-4 shadow-soft">
                <div className="flex items-center justify-between">
                    <h1 className="text-xl font-semibold text-text sm:text-2xl">My Generated Questions</h1>
                    <span className="rounded-full border border-border bg-surface-muted px-2.5 py-1 text-xs text-text-muted">
                        {submittedCount} submitted
                    </span>
                </div>
                <p className="text-sm text-text-muted">
                    Showing {(page - 1) * pageSize + 1}-{Math.min(page * pageSize, quizzes.length)} of {quizzes.length}
                </p>
            </div>

            <div className="space-y-4">
                {visibleQuizzes.map((v, idx) => {
                    const globalIndex = (page - 1) * pageSize + idx;
                    const isSubmitted = Boolean(submittedByQuestion[globalIndex]);
                    const selectedIndex = selectedByQuestion[globalIndex] ?? null;

                    return (
                        <section
                            key={`${v.question}-${globalIndex}`}
                            className="rounded-xl border border-border bg-surface p-4 shadow-soft/20 transition duration-base ease-base hover:border-border-strong sm:p-5"
                        >
                            <div className="mb-3 text-xs font-medium uppercase tracking-wide text-text-muted">
                                Question {globalIndex + 1}
                            </div>
                            <RenderMCQSingle
                                question={v}
                                submitted={isSubmitted}
                                selectedIndex={selectedIndex}
                                onSelectedIndexChange={(next) => handleSelect(globalIndex, next)}
                            />
                            <div className="mt-4 flex items-center gap-2">
                                <button
                                    type="button"
                                    className="rounded-md border border-accent bg-surface px-3 py-2 text-sm font-medium text-text transition duration-base ease-base hover:border-accent/70 disabled:cursor-not-allowed disabled:opacity-60"
                                    disabled={isSubmitted || selectedIndex == null}
                                    onClick={() => handleSubmitQuestion(globalIndex)}
                                >
                                    Submit
                                </button>
                                <button
                                    type="button"
                                    className="rounded-md border border-border bg-button-secondary px-3 py-2 text-sm font-medium text-text transition duration-base ease-base hover:border-border-strong disabled:cursor-not-allowed disabled:opacity-60"
                                    disabled={!isSubmitted}
                                    onClick={() => handleResetQuestion(globalIndex)}
                                >
                                    Reset
                                </button>

                            </div>
                        </section>
                    );
                })}
            </div>

            <div className="mt-6 flex items-center justify-between rounded-md border border-border bg-surface-muted px-4 py-3">
                <button
                    type="button"
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                    disabled={page === 1}
                    className="rounded-md border border-border bg-button-secondary px-3 py-1.5 text-sm font-medium text-text transition duration-base ease-base hover:border-border-strong hover:text-accent disabled:cursor-not-allowed disabled:opacity-40"
                >
                    Previous
                </button>

                <span className="text-sm text-text-muted">
                    Page <span className="font-semibold text-text">{page}</span> of{" "}
                    <span className="font-semibold text-text">{totalPages}</span>
                </span>

                <button
                    type="button"
                    onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                    disabled={page === totalPages}
                    className="rounded-md border border-border bg-button-secondary px-3 py-1.5 text-sm font-medium text-text transition duration-base ease-base hover:border-border-strong hover:text-accent disabled:cursor-not-allowed disabled:opacity-40"
                >
                    Next
                </button>
            </div>
        </div>
    );
}
