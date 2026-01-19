export interface AssumptionData {
    thought: string;
    assumptions: Record<string, AssumptionType>;
}

export interface ComparisonData {
    claude?: AssumptionData;
    openai?: AssumptionData;
    gemini?: AssumptionData;
}

export type AssumptionType = {
    name: string;
    value: string | number;
    format: "percentage" | "currency" | "number" | "weight" | "years" | "hoursDay" | "text",
    reasoning: string;
}