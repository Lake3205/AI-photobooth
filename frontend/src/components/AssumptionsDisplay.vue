<script lang="ts" setup>
import {LightBulbIcon} from '@heroicons/vue/24/outline';
import type {AssumptionData} from '@/types/AssumptionType';

const props = defineProps<{
  assumptionsData: AssumptionData;
}>();

const isDev = import.meta.env.DEV;

const renderBoldText = (text: string): string => {
  return text
      .replace(/\*\*(.+?):\*\*/g, '<strong class="font-bold text-white">$1:</strong><br>')
      .replace(/\*\*(.+?)\*\*/g, '<strong class="font-bold text-white">$1</strong>')
      .replace(/\*$/g, '');
};

const formatValue = (value: string | number, format: string): string => {
  const numValue = typeof value === 'number' ? value : parseFloat(value);

  switch (format) {
    case 'percentage':
      return `${numValue}%`;
    case 'currency':
      return `€${numValue.toLocaleString()}`;
    case 'weight':
      return `${numValue} kg`;
    case 'years':
      return `${numValue} years`;
    case 'hoursDay':
      return `${numValue} hrs/day`;
    case 'number':
      return numValue.toLocaleString();
    case 'text':
    default:
      return value.toString();
  }
};
</script>

<template>
  <div
      class="rounded-2xl bg-gradient-to-br from-white/5 to-white/2 border border-white/10 backdrop-blur-sm p-4 sm:p-6 space-y-4 sm:space-y-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl sm:text-2xl font-bold text-white flex items-center gap-2">
        <LightBulbIcon class="w-6 h-6 text-indigo-400"/>
        AI-Generated Assumptions
      </h2>
    </div>

    <!-- Debug Section -->
    <div v-if="isDev"
         class="mb-4 p-4 bg-red-500/20 border border-red-500/50 rounded text-xs space-y-3">
      <div>
        <div class="font-bold mb-2">DEBUG - All Assumptions:</div>
        <div v-for="(assumption, key) in assumptionsData.assumptions" :key="key" class="mb-1">
          <span class="text-yellow-300">{{ key }}:</span>
          <span class="text-green-300">{{ assumption.name }}</span> =
          <span class="text-blue-300">{{ assumption.value }}</span>
        </div>
      </div>
      <div>
        <div class="font-bold mb-2">DEBUG - Raw JSON:</div>
        <details class="mt-2">
          <summary class="cursor-pointer text-indigo-300 hover:text-indigo-200 font-semibold">
            Click to expand raw data
          </summary>
          <pre class="mt-2 p-3 bg-black/30 rounded overflow-x-auto text-[10px] leading-tight max-h-96 overflow-y-auto">{{
              JSON.stringify(assumptionsData, null, 2)
            }}</pre>
        </details>
      </div>
    </div>

    <!-- Thought Process Section -->
    <div v-if="assumptionsData.thought"
         class="p-4 sm:p-5 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 border border-indigo-400/30 space-y-3 mb-6">
      <h3 class="font-semibold text-base sm:text-lg text-indigo-300 mb-3 flex items-center gap-2">
        <LightBulbIcon class="w-5 h-5"/>
        AI Thought Process
      </h3>
      <div class="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap"
           v-html="renderBoldText(assumptionsData.thought)"></div>
    </div>

    <!-- Assumptions Display -->
    <div class="space-y-4">
      <div v-for="(assumption, key) in assumptionsData.assumptions" :key="key"
           class="p-4 sm:p-5 rounded-xl bg-white/5 border border-white/10 transition space-y-3">
        <div class="flex items-start justify-between gap-4">
          <h3 class="font-semibold text-base sm:text-lg text-indigo-300">{{ assumption.name.toString() }}</h3>
          <span class="text-xl sm:text-2xl font-bold text-white shrink-0">{{
              formatValue(assumption.value, assumption.format)
            }}</span>
        </div>
        <div v-if="assumption.reasoning" class="text-gray-400 text-sm leading-relaxed">
          {{ assumption.reasoning.toString() }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
