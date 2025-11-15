export type questionType = "scale" | "yes_no_explain";
export type FormQuestion = {
    id: string;
    question: string;
    type: questionType;
    scale?: [number, number];
}
export type formResponsePayload = Record<string, {
    questions: string;
    type: questionType;
    answer: string;
    explanation?: string;
    scale?: [number, number];
}>;