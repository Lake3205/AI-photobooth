export interface AssumptionData {
    [key: string]: AssumptionType;
}

export type AssumptionType = {
    name: string;
    value: string | number;
    format:  "PERCENTAGE" | "CURRENCY" | "NUMBER" | "WEIGHT" | "YEARS" | "HOURS_DAY" | "TEXT",
}