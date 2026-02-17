<script lang="ts" setup>
import {nextTick, onBeforeUnmount, onMounted, ref, watch} from 'vue'
import BaseCard from './BaseCard.vue'
import {createChartForAssumption, fetchAssumptions, groupAssumptionsByFormat} from '../services/dashboardService'
import type {Chart} from 'chart.js'

const props = defineProps<{
  selectedModel: string
}>()

const loading = ref(true)
const error = ref<string | null>(null)
const charts = ref<Chart[]>([])
const groupedAssumptions = ref<Record<string, { name: string; format: string; values: (string | number)[] }>>({})
const chartKey = ref(0)

const destroyCharts = () => {
  charts.value.forEach(chart => {
    try {
      chart.destroy()
    } catch (e) {
      console.warn('Error destroying chart:', e)
    }
  })
  charts.value = []
}

const renderCharts = async () => {
  await nextTick()
  
  Object.entries(groupedAssumptions.value).forEach(([key, assumption]) => {
    const canvas = document.getElementById(`chart-${key}`) as HTMLCanvasElement
    if (canvas && assumption.values.length > 0) {
      const chart = createChartForAssumption(canvas, assumption)
      if (chart) {
        charts.value.push(chart)
      }
    }
  })
}

const loadDashboardData = async () => {
  try {
    loading.value = true
    error.value = null

    destroyCharts()

    const assumptions = await fetchAssumptions(props.selectedModel)

    if (assumptions.length === 0) {
      error.value = 'No data available yet!'
      loading.value = false
      return
    }

    groupedAssumptions.value = groupAssumptionsByFormat(assumptions)
    
    // Force Vue to recreate canvas elements
    chartKey.value++

    loading.value = false

    await renderCharts()

  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load'
    loading.value = false
  }
}

onMounted(loadDashboardData)

watch(() => props.selectedModel, loadDashboardData)

onBeforeUnmount(() => {
  destroyCharts()
})
</script>

<template>
  <div v-if="loading" class="flex justify-center items-center py-20">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
  </div>

  <div v-else-if="error" class="bg-red-500/10 border border-red-500/50 rounded-lg p-6 text-center">
    <p class="text-red-400 text-lg">{{ error }}</p>
  </div>

  <div v-else class="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-2">
    <BaseCard
        v-for="(assumption, key) in groupedAssumptions"
        :key="`${key}-${chartKey}`"
        class="p-4 sm:p-6"
    >
      <h2 class="text-lg sm:text-xl font-semibold mb-4 text-white">{{ assumption.name }}</h2>
      <div class="h-64 sm:h-80">
        <canvas :id="`chart-${key}`"></canvas>
      </div>
    </BaseCard>
  </div>
</template>

<style scoped>
/* Chart canvas sizing */
canvas {
  max-height: 100%;
  max-width: 100%;
}
</style>
