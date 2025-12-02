<script lang="ts" setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {authService} from '../services/authService'

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
  <main class="relative overflow-hidden bg-black text-white min-h-screen">
    <!-- Animated Background -->
    <div class="pointer-events-none absolute inset-0 opacity-80">
      <div
          class="absolute -top-60 -left-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-br from-blue-500/60 to-blue-300/30 blur-3xl"></div>
      <div
          class="absolute -bottom-60 -right-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-tr from-blue-400/50 to-white/10 blur-3xl"></div>
      <div
          class="absolute inset-0 bg-[radial-gradient(circle_at_1px_1px,rgba(255,255,255,0.08)_1px,transparent_1px)] [background-size:24px_24px]"></div>
    </div>

    <!-- Content -->
    <section class="relative z-10 min-h-screen flex items-center justify-center p-4 sm:p-6">
      <div class="w-full max-w-md">
        <!-- Card -->
        <div
            class="rounded-2xl bg-gradient-to-br from-white/5 to-white/2 border border-white/10 backdrop-blur-sm p-6 sm:p-8">
          <div class="text-center mb-6 sm:mb-8">
            <h1 class="text-3xl sm:text-4xl font-extrabold bg-gradient-to-r from-indigo-200 via-fuchsia-200 to-pink-300 text-transparent bg-clip-text mb-2 pb-2">
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
                  autocomplete="username"
                  class="w-full px-4 py-3 sm:py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition text-base"
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
                  autocomplete="current-password"
                  class="w-full px-4 py-3 sm:py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition text-base"
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
                class="w-full px-6 py-3.5 sm:py-3 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-semibold rounded-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none min-h-[44px]"
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
    </section>
  </main>
</template>
