<script lang="ts" setup>
import { useCookieService } from '@/services/cookieService';
import { useFormService } from '@/services/formService';
import FormQuestions from '@/components/FormQuestions.vue';

const { setCookie } = useCookieService();
const { getAssumptions, getFormQuestions, submitForm, isLoading, assumptions, isSubmitting, submitSuccess } = useFormService();

const token = new URLSearchParams(location.search).get('token');

if (token) {
  window.history.replaceState({}, document.title, window.location.pathname);
  setCookie('form_token', token, 1);
}

void getAssumptions();

const formQuestions = getFormQuestions();

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

    <div class="w-full flex flex-col gap-4 justify-center items-center">
      <div class="w-full max-w-3xl py-16 px-4">
        <h1 class="mb-8 bg-gradient-to-b from-white to-blue-300 bg-clip-text tracking-tight text-transparent font-bold text-center">Assumption Form</h1>
        <div v-if="isLoading" class="text-center">
          <p class="text-xl">Loading form...</p>
        </div>
        <div v-else-if="assumptions">
          <form class="flex flex-col gap-6" @submit.prevent="submitForm($event.currentTarget as HTMLFormElement)">
            <div v-for="(assumption, key) in assumptions" :key="key" class="flex flex-col gap-2">
              <span class="font-medium">{{ assumption.name.toString() }}</span>
              <div>
                {{ assumption.value.toString() }}<br/>
              </div>
              <div>
                {{ assumption.reasoning.toString() }}
              </div>
            </div>
            <hr>
            <div class="flex flex-col gap-6">
              <FormQuestions :form-questions="formQuestions"></FormQuestions>
            </div>
            <button
                type="submit"
                class="rounded-md cursor-pointer bg-blue-600 px-6 py-2 font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Submit
            </button>
          </form>
        </div>
      </div> 
    </div>
  </main>
</template>

<style scoped>

</style>
