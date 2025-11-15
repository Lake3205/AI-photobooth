import type { AssumptionData } from '@/types/AssumptionType';
import { ref } from 'vue';

export function useFormService() {
    const isLoading = ref(false);
    const assumptions = ref<null | AssumptionData>(null);

    async function getAssumptions(token: string): Promise<any> {
        isLoading.value = true;
        const response = await fetch(`${import.meta.env.VITE_API_URL}/form/assumptions`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch assumptions');
        }

        const data = (await response.json()) as AssumptionData;
        isLoading.value = false;

        assumptions.value = data;

        return data;
    };

    return {
        assumptions, isLoading, getAssumptions
    };
                
}