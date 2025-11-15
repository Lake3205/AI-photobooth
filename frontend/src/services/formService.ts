import type { AssumptionData } from "@/types/AssumptionType";
import type { FormQuestion } from "@/types/FormTypes";
import { ref } from "vue";

export function useFormService() {
    const isLoading = ref(false);
    const assumptions = ref<null | AssumptionData>(null);

    async function getAssumptions(token: string): Promise<any> {
        isLoading.value = true;
        const response = await fetch(`${import.meta.env.VITE_API_URL}/form/assumptions`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error("Failed to fetch assumptions");
        }

        const data = (await response.json()) as AssumptionData;
        isLoading.value = false;

        assumptions.value = data;

        return data;
    };

    function getFormQuestions(): FormQuestion[] {
        return [
            {
                id: "shock",
                question: "On a scale from 1 to 10, how shocked are you by the results?",
                type: "scale",
                scale: [1, 10]
            },
            {
                id: "happiness",
                question: "On a scale from 1 to 10, how happy are you with the results?",
                type: "scale",
                scale: [1, 10]
            },
            {
                id: "accuracy",
                question: "On a scale from 1 to 10, how accurate do you feel the results are?",
                type: "scale",
                scale: [1, 10]
            },
            {
                id: "viewpoint_change",
                question: "Have you changed your viewpoint on AI after seeing the results?",
                type: "yes_no_explain"
            },
            {
                id: "regulation_opinion",
                question: "Do you feel there should be more regulation on AI?",
                type: "yes_no_explain"
            }
        ]
    }

    return {
        assumptions, isLoading, getAssumptions, getFormQuestions
    };
                
}