<script lang="ts" setup>
import { onMounted, ref, computed } from 'vue'
import { authService } from '../services/authService'

interface AssumptionValue {
  name: string
  format: string
  value: string | number | null
}

interface Assumption {
  id: number
  ai_model: string
  assumptions: Record<string, AssumptionValue>
  date_created: string
}

interface Session {
  id: number
  created_at: string
  assumptions: Assumption[]
}

interface SessionWithComparison {
  id: number
  timestamp: string
  models: Record<string, Record<string, AssumptionValue>>
  hasDifferences: boolean
}

const loading = ref(true)
const error = ref<string | null>(null)
const allSessions = ref<Session[]>([])
const expandedRows = ref<Set<number>>(new Set())

// Get all unique assumption constant keys
const assumptionKeys = computed(() => {
  if (allSessions.value.length === 0) return []
  const keysSet = new Set<string>()
  allSessions.value.forEach(session => {
    session.assumptions.forEach(assumption => {
      Object.keys(assumption.assumptions).forEach(key => keysSet.add(key))
    })
  })
  return Array.from(keysSet).sort()
})

// Process sessions for comparison
const processedSessions = computed<SessionWithComparison[]>(() => {
  const sessions = allSessions.value.map(session => {
    const models: Record<string, Record<string, AssumptionValue>> = {}
    
    // Group assumptions by AI model
    session.assumptions.forEach(assumption => {
      models[assumption.ai_model] = assumption.assumptions
    })
    
    // Check for differences
    let hasDifferences = false
    const modelNames = Object.keys(models)
    if (modelNames.length > 1) {
      // Check each assumption key for differences
      for (const key of assumptionKeys.value) {
        const values = modelNames
          .map(model => models[model]?.[key]?.value)
          .filter(v => v !== undefined && v !== null)
        
        if (values.length > 1) {
          const uniqueValues = new Set(values.map(v => String(v)))
          if (uniqueValues.size > 1) {
            hasDifferences = true
            break
          }
        }
      }
    }
    
    return {
      id: session.id,
      timestamp: session.created_at,
      models,
      hasDifferences
    }
  })
  
  return sessions.sort((a, b) => 
    new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
  )
})

// Check if a specific key has differences across models
const hasDifferencesForKey = (session: SessionWithComparison, key: string): boolean => {
  const modelNames = Object.keys(session.models)
  if (modelNames.length <= 1) return false
  
  const values = modelNames
    .map(model => session.models[model]?.[key]?.value)
    .filter(v => v !== undefined && v !== null)
  
  if (values.length <= 1) return false
  
  const uniqueValues = new Set(values.map(v => String(v)))
  return uniqueValues.size > 1
}

// Get the display value for a specific assumption
const getDisplayValue = (value: AssumptionValue | undefined): string => {
  if (!value || value.value === null || value.value === undefined) {
    return 'N/A'
  }
  
  const val = value.value
  
  switch (value.format) {
    case 'percentage':
      return `${val}%`
    case 'currency':
      return `€${val}`
    case 'years':
      return `${val} years`
    case 'weight':
      return `${val} kg`
    case 'number':
      return String(val)
    default:
      return String(val)
  }
}

const toggleRow = (id: number) => {
  if (expandedRows.value.has(id)) {
    expandedRows.value.delete(id)
  } else {
    expandedRows.value.add(id)
  }
}

const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr)
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadSessions = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await authService.authenticatedFetch(
      `${import.meta.env.VITE_API_URL}/database/sessions`
    )
    
    if (!response.ok) {
      throw new Error('Failed to fetch sessions')
    }
    
    allSessions.value = await response.json()
    
    if (allSessions.value.length === 0) {
      error.value = 'No session data available yet!'
    }
    
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load data'
  } finally {
    loading.value = false
  }
}

onMounted(loadSessions)
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white/5 border border-white/20 rounded-lg p-4">
      <h2 class="text-xl font-bold text-white mb-2">Session Comparison</h2>
      <p class="text-sm text-white/70">
        Compare AI model outputs for each session. 
        Each session represents one photo analyzed by multiple AI models.
        <span class="text-yellow-400">Yellow highlights</span> indicate differences between models.
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-500/10 border border-red-500/50 rounded-lg p-6 text-center">
      <p class="text-red-400 text-lg">{{ error }}</p>
    </div>

    <!-- Data Display -->
    <div v-else class="space-y-4">
      <div
        v-for="session in processedSessions"
        :key="session.id"
        class="bg-white/5 border border-white/20 rounded-lg overflow-hidden"
      >
        <!-- Session Header -->
        <div
          class="flex items-center justify-between p-4 cursor-pointer hover:bg-white/5 transition"
          @click="toggleRow(session.id)"
        >
          <div class="flex items-center gap-3">
            <svg
              class="w-5 h-5 text-white/70 transition-transform"
              :class="{ 'rotate-90': expandedRows.has(session.id) }"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            <div>
              <div class="text-white font-medium">
                Session #{{ session.id }}
              </div>
              <div class="text-sm text-white/50">
                {{ formatDate(session.timestamp) }}
              </div>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <div class="flex gap-2">
              <span
                v-for="modelName in Object.keys(session.models)"
                :key="modelName"
                class="px-2 py-1 text-xs rounded bg-indigo-500/30 text-indigo-200 border border-indigo-400/50 capitalize"
              >
                {{ modelName }}
              </span>
            </div>
            <span
              v-if="session.hasDifferences"
              class="px-3 py-1 text-xs rounded bg-yellow-500/20 text-yellow-300 border border-yellow-500/50"
            >
              Has Differences
            </span>
          </div>
        </div>

        <!-- Expanded Content -->
        <div v-if="expandedRows.has(session.id)" class="border-t border-white/20">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-white/5">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-white/70 uppercase tracking-wider">
                    Attribute
                  </th>
                  <th
                    v-for="modelName in Object.keys(session.models)"
                    :key="`header-${modelName}`"
                    class="px-4 py-3 text-left text-xs font-medium text-white/70 uppercase tracking-wider capitalize"
                  >
                    {{ modelName }}
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/10">
                <tr
                  v-for="key in assumptionKeys"
                  :key="key"
                  :class="{
                    'bg-yellow-500/10': hasDifferencesForKey(session, key)
                  }"
                >
                  <td class="px-4 py-3 text-sm text-white/90 font-medium">
                    {{ Object.values(session.models)[0]?.[key]?.name || key }}
                  </td>
                  <td
                    v-for="modelName in Object.keys(session.models)"
                    :key="`${key}-${modelName}`"
                    class="px-4 py-3 text-sm text-white/70"
                  >
                    {{ session.models[modelName] ? getDisplayValue(session.models[modelName][key]) : 'N/A' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom scrollbar for table */
.overflow-x-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) rgba(255, 255, 255, 0.1);
}

.overflow-x-auto::-webkit-scrollbar {
  height: 8px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>
