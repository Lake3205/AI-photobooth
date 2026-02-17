<template>
  <div class="absolute bottom-4 sm:bottom-8 left-1/2 transform -translate-x-1/2 z-20">
    <button 
        :disabled="countdown > 0"
        :aria-label="ariaLabel"
        class="group relative p-2.5 sm:p-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full transition-all duration-200 hover:scale-110 min-w-[44px] min-h-[44px]"
        tabindex="1" 
        @click="$emit('capture')">
      <span
          class="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500/20 to-blue-300/20 group-hover:from-blue-500/30 group-hover:to-blue-300/30 transition-all block"></span>
      <slot name="icon">
        <CameraIcon class="relative h-6 sm:h-7 w-6 sm:w-7 text-white"/>
      </slot>
      <span v-if="countdown > 0"
            class="absolute inset-0 flex items-center justify-center text-2xl sm:text-3xl font-bold text-white bg-black/60 rounded-full z-10">
        {{ countdown }}
      </span>
    </button>
  </div>
</template>

<script lang="ts" setup>
import {CameraIcon} from '@heroicons/vue/24/outline'

defineProps<{
  countdown?: number
  ariaLabel?: string
}>()

defineEmits<{
  capture: []
}>()
</script>
