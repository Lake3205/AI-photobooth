<script lang="ts" setup>
import {ref} from 'vue'

const props = defineProps<{
  label: string
  onClick: () => void
  class?: string
}>()

const mouseX = ref(0)
const mouseY = ref(0)
const isHovering = ref(false)

function handleMouseMove(e: MouseEvent) {
  const rect = (e.currentTarget as HTMLElement).getBoundingClientRect()
  mouseX.value = e.clientX - rect.left
  mouseY.value = e.clientY - rect.top
  isHovering.value = true
}

function handleMouseLeave() {
  isHovering.value = false
}
</script>

<template>
  <button
      :class="`group relative inline-flex items-center gap-3 rounded-full bg-white/10 px-8 py-4 text-lg font-semibold text-white ring-1 ring-white/20 backdrop-blur transition-all hover:bg-white/15 focus:outline-none focus:ring-white/40 cursor-pointer ${props.class || ''}`"
      @click="props.onClick"
      @mouseleave="handleMouseLeave"
      @mousemove="handleMouseMove"
  >
    <span class="relative z-10">{{ props.label }}</span>
    <span
        :style="isHovering
        ? `background: radial-gradient(circle at ${mouseX}px ${mouseY}px, rgba(59,130,246,0.25) 0%, transparent 60%); opacity: 1;`
        : 'opacity: 0;'"
        class="pointer-events-none absolute inset-0 -z-0 rounded-full transition-opacity duration-300"
    ></span>
  </button>
</template>

<style scoped>
</style>
