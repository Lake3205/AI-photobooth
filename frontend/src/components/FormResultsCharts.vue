<script lang="ts" setup>
import {nextTick, onBeforeUnmount, onMounted, ref} from 'vue'
import BaseCard from './BaseCard.vue'
import {createChartForFormQuestion, fetchFormResults} from '../services/dashboardService'
import type {FormResult} from '../services/dashboardService'
import type {Chart} from 'chart.js'

const loading = ref(true)
const error = ref<string | null>(null)
const charts = ref<Chart[]>([])
const questions = ref<FormResult[]>([])
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
  
  questions.value.forEach((question) => {
    const canvas = document.getElementById(`chart-question-${question.id}`) as HTMLCanvasElement
    if (canvas && question.answers.length > 0) {
      const chart = createChartForFormQuestion(canvas, question)
      if (chart) {
        charts.value.push(chart)
      }
    }
  })
}

const loadFormResults = async () => {
  try {
    loading.value = true
    error.value = null

    destroyCharts()

    const results = await fetchFormResults()

    if (results.length === 0) {
      error.value = 'No form responses yet!'
      loading.value = false
      return
    }

    questions.value = results.filter(q => q.answers.length > 0)
    
    if (questions.value.length === 0) {
      error.value = 'No form responses yet!'
      loading.value = false
      return
    }

    // Force Vue to recreate canvas elements
    chartKey.value++

    loading.value = false

    await renderCharts()

  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load form results'
    loading.value = false
  }
}

onMounted(loadFormResults)

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
        v-for="question in questions"
        :key="`${question.id}-${chartKey}`"
        class="p-4 sm:p-6"
    >
      <h2 class="text-lg sm:text-xl font-semibold mb-4 text-white">{{ question.question }}</h2>
      <p class="text-sm text-gray-400 mb-4">Total responses: {{ question.answers.length }}</p>
      <div class="h-64 sm:h-80">
        <canvas :id="`chart-question-${question.id}`"></canvas>
      </div>
      
      <!-- Show explanations for yes/no questions if they exist -->
      <div v-if="question.type === 'yes_no_explain'" class="mt-6">
        <h3 class="text-md font-semibold text-white mb-2">Explanations:</h3>
        <div class="space-y-2 max-h-60 overflow-y-auto">
          <div 
            v-for="(answer, idx) in question.answers.filter(a => a.explanation)" 
            :key="idx"
            class="p-3 bg-white/5 border border-white/10 rounded-lg"
          >
            <p class="text-xs text-gray-400 mb-1">
              <span :class="answer.value.toLowerCase() === 'yes' ? 'text-green-400' : 'text-red-400'" class="font-medium">
                {{ answer.value.toUpperCase() }}
              </span>
            </p>
            <p class="text-sm text-gray-300">{{ answer.explanation }}</p>
          </div>
          <p v-if="question.answers.filter(a => a.explanation).length === 0" class="text-sm text-gray-500 italic">
            No explanations provided
          </p>
        </div>
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

/* Custom scrollbar styling */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
