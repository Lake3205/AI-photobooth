<script lang="ts" setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {useCommonStyles} from '@/composables/useCommonStyles'
import {authService} from '../services/authService'
import PageLayout from '@/components/shared/PageLayout.vue'

const router = useRouter()
const {cardClasses, inputClasses, buttonPrimaryClasses, headerGradientClasses} = useCommonStyles()
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
  <PageLayout container-class="min-h-screen flex items-center justify-center p-4 sm:p-6">
    <div class="w-full max-w-md">
      <!-- Card -->
      <div :class="['p-6 sm:p-8', cardClasses]">
        <div class="text-center mb-6 sm:mb-8">
          <h1 :class="['text-3xl sm:text-4xl font-extrabold mb-2 pb-2', headerGradientClasses]">
            Login
          </h1>
          <p class="text-sm sm:text-base text-gray-400">Sign in to access the dashboard</p>
        </div>

          <form class="space-y-4 sm:space-y-6" @submit.prevent="handleLogin">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2" for="username">
                Username
              </label>
              <input
                  id="username"
                  v-model="username"
                :class="inputClasses"
                autocomplete="username"
                placeholder="Enter your username"
                required
                type="text"
                @keypress="handleKeypress"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2" for="password">
              Password
            </label>
            <input
                id="password"
                v-model="password"
                :class="inputClasses"
                autocomplete="current-password"
                placeholder="Enter your password"
                required
                type="password"
                @keypress="handleKeypress"
            />
          </div>

          <div v-if="error" class="bg-red-500/10 border border-red-500/50 rounded-lg p-3 sm:p-4">
            <p class="text-red-400 text-sm text-center">{{ error }}</p>
          </div>

          <button
              :disabled="loading"
              :class="['w-full disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none', buttonPrimaryClasses]"
              type="submit"
          >
              <span v-if="loading" class="flex items-center justify-center gap-2">
                <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        fill="currentColor"></path>
                </svg>
                Logging in...
              </span>
              <span v-else>Sign In</span>
            </button>
          </form>

          <div class="mt-6 text-center">
            <a class="text-sm text-indigo-400 hover:text-indigo-300 transition" href="/">
              ← Back to Home
            </a>
          </div>
        </div>
      </div>
    </PageLayout>
  </template>
