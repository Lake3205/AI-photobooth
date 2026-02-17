<script lang="ts" setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import AIOutputCharts from '../components/AIOutputCharts.vue'
import FormQuestionsManager from '../components/FormQuestionsManager.vue'
import FormResultsCharts from '../components/FormResultsCharts.vue'
import {authService} from '../services/authService'

const router = useRouter()
const activeView = ref<'aiOutput' | 'formResults' | 'questions'>('aiOutput')

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
        <p class="mt-2 text-sm sm:text-base text-gray-400">AI outputs, form responses, and question management</p>
      </div>

      <button
          class="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 rounded-lg text-red-300 hover:text-red-200 transition min-h-[44px]"
          @click="handleLogout"
      >
        Logout
      </button>
    </header>

    <div class="flex flex-wrap gap-2 sm:gap-3">
      <button
          :class="activeView === 'aiOutput' ? 'bg-indigo-500/30 border-indigo-400 text-indigo-100' : 'bg-white/5 border-white/20 text-white/80 hover:bg-white/10'"
          class="px-4 py-2 border rounded-lg transition min-h-[44px]"
          @click="activeView = 'aiOutput'"
      >
        AI Outputs
      </button>
      <button
          :class="activeView === 'formResults' ? 'bg-indigo-500/30 border-indigo-400 text-indigo-100' : 'bg-white/5 border-white/20 text-white/80 hover:bg-white/10'"
          class="px-4 py-2 border rounded-lg transition min-h-[44px]"
          @click="activeView = 'formResults'"
      >
        Form Responses
      </button>
      <button
          :class="activeView === 'questions' ? 'bg-indigo-500/30 border-indigo-400 text-indigo-100' : 'bg-white/5 border-white/20 text-white/80 hover:bg-white/10'"
          class="px-4 py-2 border rounded-lg transition min-h-[44px]"
          @click="activeView = 'questions'"
      >
        Manage Questions
      </button>
    </div>

    <AIOutputCharts v-if="activeView === 'aiOutput'" />
    
    <FormResultsCharts v-else-if="activeView === 'formResults'" />
    
    <FormQuestionsManager v-else />
  </section>
</template>
