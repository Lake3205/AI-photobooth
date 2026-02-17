<template>
  <div class="absolute inset-0 z-10 flex items-center justify-center bg-black/70 rounded-xl p-4">
    <div class="text-center">
      <div v-if="showSpinner"
           class="animate-spin rounded-full h-12 sm:h-16 w-12 sm:w-16 border-b-2 border-white mx-auto mb-3 sm:mb-4"></div>
      <slot v-else name="icon">
        <CameraIcon class="h-16 sm:h-20 w-16 sm:w-20 text-white/50 mx-auto mb-3 sm:mb-4"/>
      </slot>
      <p class="text-white/70 text-base sm:text-lg">{{ message }}</p>
      <slot name="actions" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import {CameraIcon} from '@heroicons/vue/24/outline'

defineProps<{
  message: string
  showSpinner?: boolean
}>()
</script>
