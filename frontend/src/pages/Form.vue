<script lang="ts" setup>
import { useCookieService } from '@/services/cookieService';

const { setCookie } = useCookieService();

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

    <div class="w-full">

    </div>
  </main>
</template>

<style scoped>

</style>
