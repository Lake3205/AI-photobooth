<script lang="ts" setup>
import { onMounted, ref, watch } from 'vue'
import ChartCard from './ChartCard.vue'
import { fetchAssumptions, groupAssumptionsByFormat } from '../services/dashboardService'
import { createCombinedChartForAssumption } from '../services/combinedChartService'

const availableModels = ['gemini', 'claude', 'openai']
const selectedModels = ref<string[]>(['gemini'])

const loading = ref(true)
const error = ref<string | null>(null)
const combinedData = ref<Record<string, { 
  name: string; 
  format: string; 
  modelValues: Record<string, (string | number)[]> 
}>>({})

const toggleModel = (model: string) => {
  const index = selectedModels.value.indexOf(model)
  if (index > -1) {
    selectedModels.value.splice(index, 1)
  } else {
    selectedModels.value.push(model)
  }
}

const loadDashboardData = async () => {
  try {
    loading.value = true
    error.value = null

    if (selectedModels.value.length === 0) {
      error.value = 'Please select at least one model to view data'
      loading.value = false
      return
    }

    // First, fetch data for all models
    const modelData: Record<string, Record<string, { name: string; format: string; values: (string | number)[] }>> = {}
    
    for (const model of selectedModels.value) {
      const assumptions = await fetchAssumptions(model)
      
      if (assumptions.length > 0) {
        modelData[model] = groupAssumptionsByFormat(assumptions)
      }
    }

    // Now combine by assumption key
    const combined: Record<string, { 
      name: string; 
      format: string; 
      modelValues: Record<string, (string | number)[]> 
    }> = {}

    // Iterate through all models and their assumptions
    for (const [model, assumptions] of Object.entries(modelData)) {
      for (const [key, assumption] of Object.entries(assumptions)) {
        if (!combined[key]) {
          combined[key] = {
            name: assumption.name,
            format: assumption.format,
            modelValues: {}
          }
        }
        combined[key].modelValues[model] = assumption.values
      }
    }

    if (Object.keys(combined).length === 0) {
      error.value = 'No data available yet!'
    }

    combinedData.value = combined
    loading.value = false

  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load'
    loading.value = false
  }
}

onMounted(loadDashboardData)

watch(selectedModels, loadDashboardData, { deep: true })
</script>

<template>
  <div class="space-y-6">
    <!-- Model Selection -->
    <div class="bg-white/5 border border-white/20 rounded-lg p-4">
      <label class="text-white/70 text-sm font-medium mb-3 block">Select AI Models to Compare:</label>
      <div class="flex flex-wrap gap-3">
        <label 
          v-for="model in availableModels" 
          :key="model"
          class="flex items-center gap-2 px-4 py-2 bg-white/10 border border-white/20 rounded-lg cursor-pointer hover:bg-white/15 transition"
        >
          <input 
            type="checkbox" 
            :value="model"
            :checked="selectedModels.includes(model)"
            @change="toggleModel(model)"
            class="w-4 h-4 rounded border-white/30 bg-white/10 text-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-0"
          />
          <span class="text-white capitalize">{{ model }}</span>
        </label>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
    </div>

    <div v-else-if="error" class="bg-red-500/10 border border-red-500/50 rounded-lg p-6 text-center">
      <p class="text-red-400 text-lg">{{ error }}</p>
    </div>

    <div v-else class="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-2">
      <ChartCard
        v-for="(assumption, key) in combinedData"
        :key="`assumption-${key}`"
        :title="assumption.name"
        :chart-id="`chart-${key}`"
        :chart-data="assumption"
        :create-chart="createCombinedChartForAssumption"
      />
    </div>
  </div>
</template>

<style scoped>
</style>
