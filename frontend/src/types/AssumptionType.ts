export interface AssumptionData {
    [key: string]: AssumptionType;
}

export type AssumptionType = {
    name: string;
    value: string | number;
    format:  "percentage" | "currency" | "number" | "weight" | "years" | "hoursDay" | "text",
    min?: number;
    max?: number;
    ideal?: number;
}