<script lang="ts" setup>
import {onMounted, ref} from 'vue'
import BaseCard from './BaseCard.vue'
import {
  addFormQuestion,
  fetchFormQuestions,
  removeFormQuestion,
  type DashboardQuestion
} from '../services/dashboardService'
import type {questionType} from '@/types/FormTypes'

const questionsLoading = ref(true)
const questionsError = ref<string | null>(null)
const questionsMessage = ref<string | null>(null)
const questions = ref<DashboardQuestion[]>([])
const newQuestionText = ref('')
const newQuestionType = ref<questionType>('scale')
const scaleMin = ref(1)
const scaleMax = ref(10)

const loadQuestions = async () => {
  try {
    questionsLoading.value = true
    questionsError.value = null
    questions.value = await fetchFormQuestions()
  } catch (err) {
    questionsError.value = err instanceof Error ? err.message : 'Failed to load questions'
  } finally {
    questionsLoading.value = false
  }
}

const addQuestion = async () => {
  try {
    questionsError.value = null
    questionsMessage.value = null

    const payload: { question: string; type: questionType; scale?: [number, number] } = {
      question: newQuestionText.value.trim(),
      type: newQuestionType.value,
    }

    if (!payload.question) {
      questionsError.value = 'Question text is required.'
      return
    }

    if (newQuestionType.value === 'scale') {
      if (scaleMin.value >= scaleMax.value) {
        questionsError.value = 'Scale minimum must be smaller than maximum.'
        return
      }
      payload.scale = [scaleMin.value, scaleMax.value]
    }

    await addFormQuestion(payload)
    newQuestionText.value = ''
    questionsMessage.value = 'Question added successfully.'
    await loadQuestions()
  } catch (err) {
    questionsError.value = err instanceof Error ? err.message : 'Failed to add question'
  }
}

const deleteQuestion = async (questionId: number) => {
  try {
    questionsError.value = null
    questionsMessage.value = null
    await removeFormQuestion(questionId)
    questionsMessage.value = 'Question removed successfully.'
    await loadQuestions()
  } catch (err) {
    questionsError.value = err instanceof Error ? err.message : 'Failed to delete question'
  }
}

onMounted(loadQuestions)
</script>

<template>
  <div class="space-y-6">
    <BaseCard class="p-4 sm:p-6">
      <h2 class="text-lg sm:text-xl font-semibold mb-4 text-white">Add Question</h2>

      <div class="grid gap-4">
        <div class="space-y-2">
          <label for="question-text" class="text-sm font-medium text-white/80">Question text</label>
          <input
              id="question-text"
              v-model="newQuestionText"
              type="text"
              class="w-full px-3 sm:px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 min-h-[44px]"
              placeholder="Type the question..."
          />
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="space-y-2 sm:col-span-1">
            <label for="question-type" class="text-sm font-medium text-white/80">Type</label>
            <select
                id="question-type"
                v-model="newQuestionType"
                class="w-full px-3 sm:px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 min-h-[44px]"
            >
              <option value="scale">Scale</option>
              <option value="yes_no_explain">Yes/No + Explain</option>
            </select>
          </div>

          <div v-if="newQuestionType === 'scale'" class="space-y-2">
            <label for="scale-min" class="text-sm font-medium text-white/80">Scale min</label>
            <input
                id="scale-min"
                v-model.number="scaleMin"
                type="number"
                class="w-full px-3 sm:px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 min-h-[44px]"
            />
          </div>

          <div v-if="newQuestionType === 'scale'" class="space-y-2">
            <label for="scale-max" class="text-sm font-medium text-white/80">Scale max</label>
            <input
                id="scale-max"
                v-model.number="scaleMax"
                type="number"
                class="w-full px-3 sm:px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 min-h-[44px]"
            />
          </div>
        </div>

        <div class="flex justify-end">
          <button
              class="px-4 py-2 bg-indigo-500/30 hover:bg-indigo-500/40 border border-indigo-400/60 rounded-lg text-indigo-100 transition min-h-[44px]"
              @click="addQuestion"
          >
            Add question
          </button>
        </div>
      </div>
    </BaseCard>

    <BaseCard class="p-4 sm:p-6">
      <h2 class="text-lg sm:text-xl font-semibold mb-4 text-white">Existing Questions</h2>

      <div v-if="questionsLoading" class="flex justify-center items-center py-10">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-500"></div>
      </div>

      <div v-else-if="questionsError" class="bg-red-500/10 border border-red-500/50 rounded-lg p-4 text-red-300">
        {{ questionsError }}
      </div>

      <div v-else class="space-y-3">
        <div v-if="questionsMessage" class="bg-emerald-500/10 border border-emerald-500/40 rounded-lg p-3 text-emerald-300">
          {{ questionsMessage }}
        </div>

        <div
            v-for="question in questions"
            :key="question.key"
            class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 p-4 rounded-lg bg-white/5 border border-white/10"
        >
          <div>
            <p class="text-white font-medium">{{ question.question }}</p>
            <p class="text-xs sm:text-sm text-gray-400 mt-1">
              {{ question.type }}
              <span v-if="question.type === 'scale' && question.scale"> · {{ question.scale[0] }}-{{ question.scale[1] }}</span>
            </p>
          </div>

          <button
              class="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 rounded-lg text-red-300 hover:text-red-200 transition min-h-[44px]"
              @click="deleteQuestion(question.id)"
          >
            Remove
          </button>
        </div>

        <p v-if="questions.length === 0" class="text-gray-400">No questions configured yet.</p>
      </div>
    </BaseCard>
  </div>
</template>
