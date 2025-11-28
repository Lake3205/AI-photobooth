<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/authService'
import BaseCard from '../components/BaseCard.vue'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref<string | null>(null)
const loading = ref(false)

const handleLogin = async () => {
  if (!username.value || !password.value) {
    error.value = 'Please enter both username and password'
    return
  }

  try {
    loading.value = true
    error.value = null
    
    await authService.login({
      username: username.value,
      password: password.value,
    })
    
    const redirectPath = localStorage.getItem('redirectAfterLogin') || '/dashboard'
    localStorage.removeItem('redirectAfterLogin')
    router.push(redirectPath)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Login failed. Please check your password or username.'
  } finally {
    loading.value = false
  }
}

const handleKeypress = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    handleLogin()
  }
}
</script>

<template>
  <section class="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
    <BaseCard class="w-full max-w-md p-8">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-extrabold bg-gradient-to-r from-indigo-200 via-fuchsia-200 to-pink-300 text-transparent bg-clip-text mb-2">
          Login
        </h1>
        <p class="text-gray-400">Sign in to access the dashboard</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-300 mb-2">
            Username
          </label>
          <input
            id="username"
            v-model="username"
            type="text"
            autocomplete="username"
            required
            class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
            placeholder="Enter your username"
            @keypress="handleKeypress"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-300 mb-2">
            Password
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            autocomplete="current-password"
            required
            class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
            placeholder="Enter your password"
            @keypress="handleKeypress"
          />
        </div>

        <div v-if="error" class="bg-red-500/10 border border-red-500/50 rounded-lg p-4">
          <p class="text-red-400 text-sm text-center">{{ error }}</p>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-semibold rounded-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          <span v-if="loading" class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Logging in...
          </span>
          <span v-else>Sign In</span>
        </button>
      </form>

      <div class="mt-6 text-center">
        <a href="/" class="text-sm text-indigo-400 hover:text-indigo-300 transition">
          ← Back to Home
        </a>
      </div>
    </BaseCard>
  </section>
</template>
