import type { AssumptionData } from "@/types/AssumptionType";
import type { FormQuestions, formResponsePayload } from "@/types/FormTypes";
import { onMounted, ref } from "vue";
import { useCookieService } from "@/services/cookieService";
import router from "@/router";

const { getCookie } = useCookieService();

export function useFormService() {
    const isLoading = ref(false);
    const isSubmitting = ref(false);
    const assumptions = ref<null | AssumptionData>(null);
    const submitSuccess = ref(false);
    const questions = ref<FormQuestions>({});

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
            router.push({ name: "home" });
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

        Object.entries(questions).forEach(([id, question]) => {
            switch (question.type) {
                case "scale":
                    const scaleAnswer = formData.get(id) as string;
                    responsePayload[id] = {
                        question: question.question,
                        type: question.type,
                        answer: scaleAnswer,
                        scale: question.scale
                    };
                    break;
                case "yes_no_explain":
                    const yesNoAnswer = formData.get(id) as string;
                    const explanation = formData.get(id + "_explanation") as string | null;
                    responsePayload[id] = {
                        question: question.question,
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

    async function getFormQuestions(): Promise<FormQuestions> {
        isLoading.value = true;

        const response = await fetch(`${import.meta.env.VITE_API_URL}/form/questions`, {
            method: "GET",
        });
        isLoading.value = false;

        if (!response.ok) {
            throw new Error("Failed to fetch form questions");
        }

        questions.value = (await response.json()) as FormQuestions;
        
        return questions.value;
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
        let valid = true;

        Object.entries(questions).forEach(([id, question]) => {
            switch (question.type) {
                case "scale":
                    const scaleAnswer = formData.get(id) as string;
                    if (!question.scale || !validateScaleInput(scaleAnswer, question.scale)) {
                        valid = false;
                    }
                    break;
                case "yes_no_explain":
                    const yesNoAnswer = formData.get(id);
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

    onMounted(() => {
        void getAssumptions();
        void getFormQuestions();
    });

    return {
        assumptions, questions, isLoading, isSubmitting, submitSuccess, getAssumptions, getFormQuestions, submitForm
    };
                
}