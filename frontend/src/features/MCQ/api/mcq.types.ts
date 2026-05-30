export type DifficultyLevel = string;
export type LearningObjective = string;

export type Option = {
  option: string;
  correct: boolean;
};

export type MultipleChoiceQuestionBase = {
  question: string;
  options: Option[];
};
export type MCQSubmission = {
  selected: string;
  is_correct: boolean;
};
export type MultipleChoiceQuestion = MultipleChoiceQuestionBase & {
  topic: string;
  difficulty: DifficultyLevel;
  learning_objective: LearningObjective;
};

export type MultipleChoiceQuestionSubmitted = MultipleChoiceQuestion & {
  submission: MCQSubmission
}

export type MultipleChoiceQuestionToolResponse = {
  payload: MultipleChoiceQuestion[];
};

export type MCQDB = {
  id: string;
  quiz_data: any;
  created_at: string;
  updated_at: string;
  schema_version: number;
  user_id: string;
  thread_id: string;
};

export type GeneratedContentSaveRequest = {
  qpayload: MultipleChoiceQuestionToolResponse;
  thread_id?: string | null;
};
