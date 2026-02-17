<script lang="ts" setup>
import {useCookieService} from '@/services/cookieService';
import {useFormService} from '@/services/formService';
import {useCommonStyles} from '@/composables/useCommonStyles';
import FormQuestions from '@/components/FormQuestions.vue';
import AssumptionsDisplay from '@/components/AssumptionsDisplay.vue';
import PageLayout from '@/components/shared/PageLayout.vue';
import {PencilSquareIcon} from '@heroicons/vue/24/outline';

const {setCookie} = useCookieService();
const {submitForm, isLoading, assumptionsData, comparisonData} = useFormService();
const {cardClasses, buttonPrimaryClasses, headerGradientClasses} = useCommonStyles();
const token = new URLSearchParams(location.search).get('token');

if (token) {
  window.history.replaceState({}, document.title, window.location.pathname);
  setCookie('form_token', token, 1);
}
</script>

<template>
  <PageLayout container-class="w-full flex flex-col gap-4 justify-center items-center">
      <div class="w-full max-w-6xl py-8 sm:py-12 md:py-16 px-4 sm:px-6">
        <div class="text-center mb-6 sm:mb-10">
          <h1 :class="['text-3xl sm:text-4xl md:text-5xl font-extrabold tracking-tight mb-3', headerGradientClasses]">
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
            <!-- AI Assumptions -->
            <AssumptionsDisplay
                :assumptions-data="assumptionsData"
                :comparison-data="comparisonData"
            />

            <!-- Form Questions -->
            <div :class="['p-4 sm:p-6 space-y-4 sm:space-y-6', cardClasses]">
              <h2 class="text-xl sm:text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <PencilSquareIcon class="w-6 h-6 text-indigo-400"/>
                Your Responses
              </h2>
              <FormQuestions></FormQuestions>
            </div>

            <!-- Submit Button -->
            <div class="flex justify-center pt-4">
              <button
                  :class="['w-full sm:w-auto', buttonPrimaryClasses]"
                  type="submit"
              >
                Submit Form
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </PageLayout>
</template>
