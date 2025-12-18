export interface AssumptionData {
    thought: string;
    assumptions: Record<string, AssumptionType>;
}

export type AssumptionType = {
    name: string;
    value: string | number;
    format: "percentage" | "currency" | "number" | "weight" | "years" | "hoursDay" | "text",
    reasoning: string;
}