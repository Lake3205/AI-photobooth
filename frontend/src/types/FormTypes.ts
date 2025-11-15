export type questionType = "scale" | "yes_no_explain";
export type FormQuestion = {
    id: string;
    question: string;
    type: questionType;
    scale?: [number, number];
}