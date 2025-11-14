export function useFormService() {
    async function getAssumptions(token: string): Promise<any> {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/form/assumptions`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch assumptions');
        }

        return await response.json();
    };

    return {
        getAssumptions,
    };
                
}