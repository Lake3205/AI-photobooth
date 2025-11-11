<script lang="ts" setup>
import {useRouter} from 'vue-router'
import LandingButton from '@/components/LandingButton.vue'
import TermsButton from '@/components/TermsButton.vue'

const router = useRouter()

function goToSelfie() {
  router.push({name: 'selfie'})
}
</script>

<template>
  <main class="relative overflow-hidden bg-black text-white">
    <!-- Simplified Background -->
    <div class="pointer-events-none absolute inset-0 opacity-80">
      <div
          class="absolute -top-60 -left-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-br from-blue-500/60 to-blue-300/30 blur-3xl"></div>
      <div
          class="absolute -bottom-60 -right-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-tr from-blue-400/50 to-white/10 blur-3xl"></div>
      <div
          class="absolute inset-0 bg-[radial-gradient(circle_at_1px_1px,rgba(255,255,255,0.08)_1px,transparent_1px)] [background-size:24px_24px]"></div>
    </div>

    <!-- Content -->
    <section
        class="relative z-10 mx-auto flex min-h-screen max-w-5xl flex-col items-center justify-center px-6 text-center">
      <h1 class="select-none bg-gradient-to-b from-white to-blue-300 bg-clip-text text-6xl font-extrabold tracking-tight text-transparent sm:text-7xl md:text-8xl">
        ParallaxAI
      </h1>
      <p class="mt-5 max-w-2xl text-balance text-lg text-blue-100/90 sm:text-xl">
        Uncover the unseen — shifting perspectives, one image at a time.
      </p>

      <LandingButton :label="'Get Started'" :onClick="goToSelfie" class="mt-5"/>
    </section>
    <TermsButton class="terms-btn-fixed"/>
  </main>
</template>

<style scoped>
</style>
