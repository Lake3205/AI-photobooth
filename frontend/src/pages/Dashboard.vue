<script lang="ts" setup>
import {onMounted, ref, watch} from 'vue'
import BaseCard from '../components/BaseCard.vue'
import {createChartForAssumption, fetchAssumptions, groupAssumptionsByFormat} from '../services/dashboardService'
import type {Chart} from 'chart.js'

const loading = ref(true)
const error = ref<string | null>(null)
const charts = ref<Chart[]>([])
const groupedAssumptions = ref<Record<string, { name: string; format: string; values: (string | number)[] }>>({})
const selectedModel = ref<string>('gemini')
const availableModels = ref<string[]>(['gemini', 'claude'])

const loadDashboardData = async () => {
  try {
    loading.value = true
    error.value = null

    charts.value.forEach(chart => chart.destroy())
    charts.value = []

    const assumptions = await fetchAssumptions(selectedModel.value)

    if (assumptions.length === 0) {
      error.value = 'No data available yet!'
      loading.value = false
      return
    }

    groupedAssumptions.value = groupAssumptionsByFormat(assumptions)

    loading.value = false

    setTimeout(() => {
      Object.entries(groupedAssumptions.value).forEach(([key, assumption]) => {
        const canvas = document.getElementById(`chart-${key}`) as HTMLCanvasElement
        if (canvas && assumption.values.length > 0) {
          const chart = createChartForAssumption(canvas, assumption)
          if (chart) {
            charts.value.push(chart)
          }
        }
      })
    }, 100)

  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load'
    loading.value = false
  }
}

onMounted(loadDashboardData)

watch(selectedModel, loadDashboardData)
</script>

<template>
  <section class="p-6 md:p-10 space-y-10">
    <header class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-4xl font-extrabold bg-gradient-to-r from-indigo-200 via-fuchsia-200 to-pink-300 text-transparent bg-clip-text">
          Dashboard
        </h1>
        <p class="mt-2 text-gray-400">Analytics and insights from AI assumptions</p>
      </div>

      <div class="flex items-center gap-3">
        <label class="text-white/70 text-sm font-medium" for="model-select">AI Model:</label>
        <select
            id="model-select"
            v-model="selectedModel"
            class="px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
        >
          <option v-for="model in availableModels" :key="model" :value="model">
            {{ model.charAt(0).toUpperCase() + model.slice(1) }}
          </option>
        </select>
      </div>
    </header>

    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
    </div>

    <div v-else-if="error" class="bg-red-500/10 border border-red-500/50 rounded-lg p-6 text-center">
      <p class="text-red-400 text-lg">{{ error }}</p>
    </div>

    <div v-else class="grid gap-6 sm:grid-cols-1 lg:grid-cols-2 xl:grid-cols-2">
      <BaseCard
          v-for="(assumption, key) in groupedAssumptions"
          :key="key"
          class="p-6"
      >
        <h2 class="text-xl font-semibold mb-4 text-white">{{ assumption.name }}</h2>
        <div class="h-80">
          <canvas :id="`chart-${key}`"></canvas>
        </div>
      </BaseCard>
    </div>
  </section>
</template>

<style scoped>
canvas {
  max-height: 100%;
  max-width: 100%;
}
</style>
