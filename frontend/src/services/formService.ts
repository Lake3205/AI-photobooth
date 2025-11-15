import type { AssumptionData } from "@/types/AssumptionType";
import type { FormQuestion, formResponsePayload } from "@/types/FormTypes";
import { ref } from "vue";
import { useCookieService } from "@/services/cookieService";

const { getCookie } = useCookieService();

export function useFormService() {
    const isLoading = ref(false);
    const isSubmitting = ref(false);
    const assumptions = ref<null | AssumptionData>(null);
    const submitSuccess = ref(false);

    async function getAssumptions(): Promise<any> {
        const token = getCookie("form_token") || "";
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

    async function sendFormResponse(formData: FormData, token: string) {
        const questions = getFormQuestions();
        const responsePayload: formResponsePayload = {};

        questions.forEach((question) => {
            switch (question.type) {
                case "scale":
                    const scaleAnswer = formData.get(question.id) as string;
                    responsePayload[question.id] = {
                        questions: question.question,
                        type: question.type,
                        answer: scaleAnswer,
                        scale: question.scale
                    };
                    break;
                case "yes_no_explain":
                    const yesNoAnswer = formData.get(question.id) as string;
                    const explanation = formData.get(question.id + "_explanation") as string | null;
                    responsePayload[question.id] = {
                        questions: question.question,
                        type: question.type,
                        answer: yesNoAnswer,
                        explanation: explanation || undefined
                    };
                    break;
            }
        });

        isSubmitting.value = true;

        const response = await fetch(`${import.meta.env.VITE_API_URL}/form/submit`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify(responsePayload),
        });

        isSubmitting.value = false;

        if (!response.ok) {
            throw new Error("Failed to submit form");
        }

        submitSuccess.value = await response.json();        
    }

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

    function validateScaleInput(value: string, scale: [number, number]): boolean {
        const num = parseInt(value, 10);
        return !isNaN(num) && num >= scale[0] && num <= scale[1];
    }

    function validateYesNoExplainInput(yesNoValue: string | null): boolean {
        if (yesNoValue !== "yes" && yesNoValue !== "no") {
            return false;
        }
        return true;
    }

    function submitForm(form: HTMLFormElement) {
        const token = getCookie("form_token") || "";
        const formData = new FormData(form);
        const formQuestions = getFormQuestions();
        let valid = true;

        formQuestions.forEach((question) => {
            switch (question.type) {
                case "scale":
                    const scaleAnswer = formData.get(question.id) as string;
                    if (!question.scale || !validateScaleInput(scaleAnswer, question.scale)) {
                        valid = false;
                    }
                    break;
                case "yes_no_explain":
                    const yesNoAnswer = formData.get(question.id);
                    if (!validateYesNoExplainInput(yesNoAnswer as string | null)) {
                        valid = false;
                    }
                    break;
            }
        });

        if (!valid) {
            return;
        }

        void sendFormResponse(formData, token);
    }

    return {
        assumptions, isLoading, isSubmitting, submitSuccess, getAssumptions, getFormQuestions, submitForm
    };
                
}