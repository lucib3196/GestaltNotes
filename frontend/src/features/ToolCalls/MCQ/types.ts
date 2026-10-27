import type { z } from "zod";
import type { mcqQuestion, multipleChoiceSetSchema } from "./schema";

export type MCQQuestion = z.infer<typeof mcqQuestion>;
export type MultipleChoiceSet = z.infer<typeof multipleChoiceSetSchema>;
export type AnswerMap = Record<number, number>;
export type ReasoningMap = Record<number, string>;
export type QuestionResult = {
  questionIndex: number;
  question: string;
  selectedOptionIndex: number | null;
  selectedAnswer: string | null;
  correctOptionIndex: number;
  correctAnswer: string;
  isCorrect: boolean | null;
  reasoning: string | null;
  explanation: string;
};
export type QuizSubmission = {
  answers: AnswerMap;
  reasoning: ReasoningMap;
  results: QuestionResult[];
  correctCount: number;
  answeredCount: number;
  total: number;
};
export type QuizSavePayload = { quiz: MultipleChoiceSet; submission: QuizSubmission };
export type QuizAction = (submission: QuizSubmission) => void | Promise<void>;
export type QuizSaveHandler = (payload: QuizSavePayload) => void | Promise<void>;
