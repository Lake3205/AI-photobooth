<script lang="ts" setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import DashboardAnalytics from '../components/DashboardAnalytics.vue'
import FormQuestionsManager from '../components/FormQuestionsManager.vue'
import {authService} from '../services/authService'

const router = useRouter()
const activeView = ref<'analytics' | 'questions'>('analytics')
const selectedModel = ref<string>('gemini')
const availableModels = ref<string[]>(['gemini', 'claude'])

const handleLogout = () => {
  authService.logout()
  router.push('/login')
}
</script>

<template>
  <section class="p-4 sm:p-6 md:p-10 space-y-6 sm:space-y-10">
    <header class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-3xl sm:text-4xl font-extrabold bg-gradient-to-r from-indigo-200 via-fuchsia-200 to-pink-300 text-transparent bg-clip-text">
          Admin Dashboard
        </h1>
        <p class="mt-2 text-sm sm:text-base text-gray-400">Analytics and form question management</p>
      </div>

      <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
        <div class="flex items-center gap-2 sm:gap-3">
          <label class="text-white/70 text-sm font-medium" for="model-select">AI Model:</label>
          <select
              id="model-select"
              v-model="selectedModel"
              class="flex-1 sm:flex-initial px-3 sm:px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition min-h-[44px]"
          >
            <option v-for="model in availableModels" :key="model" :value="model">
              {{ model.charAt(0).toUpperCase() + model.slice(1) }}
            </option>
          </select>
        </div>

        <button
            class="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 rounded-lg text-red-300 hover:text-red-200 transition min-h-[44px]"
            @click="handleLogout"
        >
          Logout
        </button>
      </div>
    </header>

    <div class="flex gap-2 sm:gap-3">
      <button
          :class="activeView === 'analytics' ? 'bg-indigo-500/30 border-indigo-400 text-indigo-100' : 'bg-white/5 border-white/20 text-white/80 hover:bg-white/10'"
          class="px-4 py-2 border rounded-lg transition min-h-[44px]"
          @click="activeView = 'analytics'"
      >
        Analytics
      </button>
      <button
          :class="activeView === 'questions' ? 'bg-indigo-500/30 border-indigo-400 text-indigo-100' : 'bg-white/5 border-white/20 text-white/80 hover:bg-white/10'"
          class="px-4 py-2 border rounded-lg transition min-h-[44px]"
          @click="activeView = 'questions'"
      >
        Form Questions
      </button>
    </div>

    <DashboardAnalytics v-if="activeView === 'analytics'" :selected-model="selectedModel" />
    
    <FormQuestionsManager v-else />
  </section>
</template>
