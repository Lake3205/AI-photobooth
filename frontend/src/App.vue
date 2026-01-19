<script lang="ts" setup>
</script>

<template>
  <div class="min-h-screen overflow-hidden min-w-svw bg-black text-white">
    <RouterView v-slot="{ Component }">
      <Transition appear mode="out-in" name="view">
        <component :is="Component"/>
      </Transition>
    </RouterView>
  </div>
</template>

<style scoped>
.view-enter-active,
.view-leave-active {
  transition: opacity 300ms ease, transform 400ms cubic-bezier(.2, .65, .2, 1);
}

.view-enter-from {
  opacity: 0;
  transform: translateY(12px) scale(0.995);
}

.view-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.995);
}
</style>
