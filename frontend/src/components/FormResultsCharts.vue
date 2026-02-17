<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import ChartCard from './ChartCard.vue'
import { createChartForFormQuestion, fetchFormResults } from '../services/dashboardService'
import type { FormResult } from '../services/dashboardService'

const loading = ref(true)
const error = ref<string | null>(null)
const questions = ref<FormResult[]>([])

const loadFormResults = async () => {
  try {
    loading.value = true
    error.value = null

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

    loading.value = false

  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load form results'
    loading.value = false
  }
}

onMounted(loadFormResults)
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
        v-for="question in questions"
        :key="`question-${question.id}`"
        :title="question.question"
        :subtitle="`Total responses: ${question.answers.length}`"
        :chart-id="`chart-question-${question.id}`"
        :chart-data="question"
        :create-chart="createChartForFormQuestion"
    >
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
    </ChartCard>
  </div>
</template>

<style scoped>
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
