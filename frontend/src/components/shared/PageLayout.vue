<template>
  <main class="relative overflow-hidden bg-black text-white min-h-screen">
    <BackgroundGradient />
    
    <div class="relative z-10" :class="containerClass">
      <slot />
    </div>
  </main>
</template>

<script lang="ts" setup>
import BackgroundGradient from './BackgroundGradient.vue'

defineProps<{
  containerClass?: string
}>()
</script>
