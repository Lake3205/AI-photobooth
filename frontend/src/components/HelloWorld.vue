<script setup lang="ts">
import { testService } from '@/services/testService';

const { isLoading, data } = testService();

</script>

<template>
  <div v-if="isLoading">Loading...</div>
  <h1 v-else>{{ data }}</h1>
</template>

<style scoped>

</style>
