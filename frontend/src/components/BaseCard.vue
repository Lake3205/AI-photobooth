<template>
  <div
      :class="['dashboard-card p-5 rounded-2xl bg-gradient-to-br from-white/5 to-white/2 border border-white/10 backdrop-blur-sm transition transform hover:-translate-y-2 hover:shadow-2xl', extraClass]">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div v-if="$slots.icon" class="h-10 w-10 rounded-xl bg-indigo-500/20 flex items-center justify-center">
          <slot name="icon"/>
        </div>
        <div>
          <p v-if="subtitle" class="text-white/70 text-sm">{{ subtitle }}</p>
          <h2 v-if="title || $slots.title" class="text-2xl font-bold text-white">
            <slot name="title">{{ title }}</slot>
          </h2>
          <slot name="header"/>
        </div>
      </div>
      <slot name="right"/>
    </div>

    <div class="mt-3">
      <slot/>
    </div>

    <div v-if="$slots.footer" class="mt-3">
      <slot name="footer"/>
    </div>
  </div>
</template>

<script lang="ts" setup>
defineProps({
  extraClass: {type: String, default: ''},
  title: {type: String, default: ''},
  subtitle: {type: String, default: ''}
})
</script>