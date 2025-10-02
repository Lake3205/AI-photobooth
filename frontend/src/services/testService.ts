import { onMounted, ref } from "vue";

export function testService() {
    const isLoading = ref(false);
    const data = ref<string | null>(null);
    const error = ref<string | null>(null);

    async function fetchData() {
        isLoading.value = true;
        data.value = null;
        error.value = null;

        const res = await fetch('http://localhost:8000/test');
        
        isLoading.value = false;
        if (res.ok) {
            data.value = await res.json();
        } else {
            error.value = `Error: ${res.status} ${res.statusText}`;
        }
    }

    onMounted(() => {
        fetchData();
    });

    return { isLoading, data, error };
}