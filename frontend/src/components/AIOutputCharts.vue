<script lang="ts" setup>
import { onMounted, ref, watch } from 'vue'
import ChartCard from './ChartCard.vue'
import { createChartForAssumption, fetchAssumptions, groupAssumptionsByFormat } from '../services/dashboardService'

const props = defineProps<{
  selectedModel: string
}>()

const loading = ref(true)
const error = ref<string | null>(null)
const groupedAssumptions = ref<Record<string, { name: string; format: string; values: (string | number)[] }>>({})

const loadDashboardData = async () => {
  try {
    loading.value = true
    error.value = null

    const assumptions = await fetchAssumptions(props.selectedModel)

    if (assumptions.length === 0) {
      error.value = 'No data available yet!'
      loading.value = false
      return
    }

    groupedAssumptions.value = groupAssumptionsByFormat(assumptions)
    
    loading.value = false

  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load'
    loading.value = false
  }
}

onMounted(loadDashboardData)

watch(() => props.selectedModel, loadDashboardData)
</script>

<template>
  <div v-if="loading" class="flex justify-center items-center py-20">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
  </div>

  <div v-else-if="error" class="bg-red-500/10 border border-red-500/50 rounded-lg p-6 text-center">
    <p class="text-red-400 text-lg">{{ error }}</p>
  </div>

  <div v-else class="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-2">
    <ChartCard
        v-for="(assumption, key) in groupedAssumptions"
        :key="`assumption-${key}`"
        :title="assumption.name"
        :chart-id="`chart-${key}`"
        :chart-data="assumption"
        :create-chart="createChartForAssumption"
    />
  </div>
</template>

<style scoped>
</style>
