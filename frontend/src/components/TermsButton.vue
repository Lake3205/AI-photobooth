<script lang="ts" setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'

const router = useRouter()

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
      class="group relative inline-flex items-center gap-2 rounded-full bg-white/10 px-5 py-2 text-sm font-semibold text-white ring-1 ring-white/20 backdrop-blur transition-all hover:bg-white/15 focus:outline-none focus:ring-white/40 cursor-pointer"
      @click=" router.push({name: 'terms-of-service'})"
      @mouseleave="handleMouseLeave"
      @mousemove="handleMouseMove"
  >
    <span class="relative z-10">Terms of Service</span>
    <span
        :style="isHovering
        ? `background: radial-gradient(circle at ${mouseX}px ${mouseY}px, rgba(59,130,246,0.25) 0%, transparent 60%); opacity: 1;`
        : 'opacity: 0;'"
        class="pointer-events-none absolute inset-0 -z-0 rounded-full transition-opacity duration-300"
    ></span>
  </button>
</template>

<style scoped>
/* Fixed position bottom-left */
.terms-btn-fixed {
  position: fixed;
  left: 1.5rem;
  bottom: 1.5rem;
  z-index: 50;
}
</style>
