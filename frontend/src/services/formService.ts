import type {AssumptionData, ComparisonData} from "@/types/AssumptionType";
import type {FormQuestions, formResponsePayload} from "@/types/FormTypes";
import {onMounted, ref} from "vue";
import {useCookieService} from "@/services/cookieService";
import router from "@/router";

const {getCookie} = useCookieService();

export function useFormService() {
    const isLoading = ref(false);
    const isSubmitting = ref(false);
    const assumptionsData = ref<null | AssumptionData>(null);
    const comparisonData = ref<null | ComparisonData>(null);
    const submitSuccess = ref(false);
    const questions = ref<FormQuestions>({});
    const isComparisonLoading = ref(false);
    const comparisonStarted = ref(false);

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
            router.push({name: "selfie"});
            throw new Error("Failed to fetch assumptions");
        }

        const data = (await response.json()) as AssumptionData;
        assumptionsData.value = data;

        isLoading.value = false;

        void getComparison();

        return data;
    }

    async function getComparison(): Promise<void> {
        try {
            comparisonStarted.value = true;
            isComparisonLoading.value = true;

            const cachedComparison = sessionStorage.getItem("comparison_data");
            if (cachedComparison) {
                comparisonData.value = JSON.parse(cachedComparison) as ComparisonData;
                isComparisonLoading.value = false;
                return;
            }

            const imageData = sessionStorage.getItem("captured_image");
            const assumptionId = sessionStorage.getItem("assumption_id");
            const aiModel = sessionStorage.getItem("ai_model");

            if (!imageData || !assumptionId || !aiModel) {
                console.warn("Missing data for comparison:", {imageData: !!imageData, assumptionId, aiModel});
                isComparisonLoading.value = false;
                return;
            }

            // Convert base64 to blob
            const response = await fetch(imageData);
            const blob = await response.blob();

            const formData = new FormData();
            formData.append('image', blob, 'selfie.jpg');

            const url = `${import.meta.env.VITE_API_URL}/assumptions/compare?assumptions_id=${assumptionId}&ai_model=${aiModel}`;

            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 60000);

            const compareResponse = await fetch(url, {
                method: "POST",
                body: formData,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!compareResponse.ok) {
                const errorText = await compareResponse.text();
                console.error("Comparison fetch failed:", {
                    status: compareResponse.status,
                    statusText: compareResponse.statusText,
                    error: errorText
                });
                throw new Error("Failed to fetch comparison data");
            }

            const data = (await compareResponse.json()) as ComparisonData;

            sessionStorage.setItem("comparison_data", JSON.stringify(data));

            comparisonData.value = data;
            isComparisonLoading.value = false;
        } catch (error) {
            isComparisonLoading.value = false;
            if (error instanceof Error) {
                if (error.name === 'AbortError') {
                    console.error("Comparison request timed out after 60 seconds");
                } else {
                    console.error("Error fetching comparison:", error.message, error);
                }
            } else {
                console.error("Unknown error fetching comparison:", error);
            }
        }
    }

    async function sendFormResponse(formData: FormData, token: string) {
        const responsePayload: formResponsePayload = {};

        Object.entries(questions.value).forEach(([id, question]) => {
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
        submitSuccess.value = await response.ok;
        return submitSuccess.value;
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

    async function submitForm(form: HTMLFormElement) {
        const token = getCookie("form_token") || "";
        const formData = new FormData(form);
        let valid = true;

        Object.entries(questions.value).forEach(([id, question]) => {
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
                default:
                    valid = false;
                    break;
            }
        });

        if (!valid) {
            return;
        }

        const response = await sendFormResponse(formData, token);
        if (response === true) {
            router.push({name: "selfie"});
        } else {
            return;
        }
    }

    onMounted(async () => {
        await getAssumptions();
        void getFormQuestions();
    });

    return {
        assumptionsData: assumptionsData,
        comparisonData,
        questions,
        isLoading,
        isSubmitting,
        submitSuccess,
        getAssumptions,
        getFormQuestions,
        submitForm
    };

}