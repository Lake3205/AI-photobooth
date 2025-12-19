<script lang="ts" setup>
import {useCookieService} from '@/services/cookieService';
import {useFormService} from '@/services/formService';
import FormQuestions from '@/components/FormQuestions.vue';
import AssumptionsDisplay from '@/components/AssumptionsDisplay.vue';
import {PencilSquareIcon} from '@heroicons/vue/24/outline';

const {setCookie} = useCookieService();
const {submitForm, isLoading, assumptionsData} = useFormService();

const token = new URLSearchParams(location.search).get('token');

if (token) {
  window.history.replaceState({}, document.title, window.location.pathname);
  setCookie('form_token', token, 1);
}
</script>

<template>
  <main class="relative overflow-hidden bg-black text-white min-h-screen">

    <div class="pointer-events-none absolute inset-0 opacity-80">
      <div
          class="absolute -top-60 -left-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-br from-blue-500/60 to-blue-300/30 blur-3xl"></div>
      <div
          class="absolute -bottom-60 -right-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-tr from-blue-400/50 to-white/10 blur-3xl"></div>
      <div
          class="absolute inset-0 bg-[radial-gradient(circle_at_1px_1px,rgba(255,255,255,0.08)_1px,transparent_1px)] [background-size:24px_24px]"></div>
    </div>

    <div class="relative z-10 w-full flex flex-col gap-4 justify-center items-center">
      <div class="w-full max-w-4xl py-8 sm:py-12 md:py-16 px-4 sm:px-6">
        <div class="text-center mb-6 sm:mb-10">
          <h1 class="text-3xl sm:text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-indigo-200 via-fuchsia-200 to-pink-300 bg-clip-text tracking-tight text-transparent mb-3">
            Assumption Form
          </h1>
          <p class="text-gray-400 text-base sm:text-lg">Review AI-generated assumptions and answer the questions
            below</p>
        </div>

        <div v-if="isLoading" class="flex justify-center items-center py-20">
          <div class="flex flex-col items-center gap-4">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
            <p class="text-gray-400 text-sm sm:text-base">Loading form...</p>
          </div>
        </div>

        <div v-else-if="assumptionsData">
          <form class="space-y-6 sm:space-y-8" @submit.prevent="submitForm($event.currentTarget as HTMLFormElement)">
            <!-- AI Assumptions & Thought Process Section -->
            <AssumptionsDisplay :assumptions-data="assumptionsData"/>

            <!-- Form Questions Section -->
            <div
                class="rounded-2xl bg-gradient-to-br from-white/5 to-white/2 border border-white/10 backdrop-blur-sm p-4 sm:p-6 space-y-4 sm:space-y-6">
              <h2 class="text-xl sm:text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <PencilSquareIcon class="w-6 h-6 text-indigo-400"/>
                Your Responses
              </h2>
              <FormQuestions></FormQuestions>
            </div>

            <!-- Submit Button -->
            <div class="flex justify-center pt-4">
              <button
                  class="w-full sm:w-auto px-6 sm:px-8 py-3.5 sm:py-4 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-semibold rounded-xl transition-all transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-black shadow-lg min-h-[44px]"
                  type="submit"
              >
                Submit Form
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>

</style>
