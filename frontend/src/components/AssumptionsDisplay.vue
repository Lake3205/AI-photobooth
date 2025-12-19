<script lang="ts" setup>
import {LightBulbIcon, SparklesIcon} from '@heroicons/vue/24/outline';
import type {AssumptionData, ComparisonData} from '@/types/AssumptionType';
import {watch} from 'vue';

const props = defineProps<{
  assumptionsData: AssumptionData;
  comparisonData?: ComparisonData | null;
}>();

const isDev = import.meta.env.DEV;

watch(() => props.comparisonData, (newVal) => {
  console.log("AssumptionsDisplay - comparisonData updated:", newVal);
}, {immediate: true});

const renderBoldText = (text: string): string => {
  return text
      .replace(/\*\*(.+?):\*\*/g, '<strong class="font-bold text-white">$1:</strong><br>')
      .replace(/\*\*(.+?)\*\*/g, '<strong class="font-bold text-white">$1</strong>')
      .replace(/\*(.+?)\*/g, '<strong class="font-bold text-white">$1</strong>')
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
        <SparklesIcon class="w-6 h-6 text-indigo-400"/>
        AI Model Comparison
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
        Gemini Thought Process
      </h3>
      <div class="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap"
           v-html="renderBoldText(assumptionsData.thought)"></div>
    </div>

    <!-- 3-Column AI Comparison -->
    <div v-if="comparisonData" class="space-y-4">
      <!-- Header Row with AI Model Names -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        <div v-if="comparisonData.gemini"
             class="text-center p-4 rounded-xl bg-gradient-to-br from-blue-500/20 to-blue-600/10 border border-blue-400/30">
          <h3 class="text-xl font-bold text-blue-300 mb-1">Gemini</h3>
          <p class="text-xs text-gray-400">Google's AI Model</p>
        </div>
        <div v-if="comparisonData.claude"
             class="text-center p-4 rounded-xl bg-gradient-to-br from-purple-500/20 to-purple-600/10 border border-purple-400/30">
          <h3 class="text-xl font-bold text-purple-300 mb-1">Claude</h3>
          <p class="text-xs text-gray-400">Anthropic's AI Model</p>
        </div>
        <div v-if="comparisonData.openai"
             class="text-center p-4 rounded-xl bg-gradient-to-br from-green-500/20 to-green-600/10 border border-green-400/30">
          <h3 class="text-xl font-bold text-green-300 mb-1">ChatGPT</h3>
          <p class="text-xs text-gray-400">OpenAI's AI Model</p>
        </div>
      </div>

      <!-- Assumptions Rows - Each assumption type in its own row across all 3 columns -->
      <div
          v-for="(_assumption, key) in comparisonData.gemini?.assumptions || comparisonData.claude?.assumptions || comparisonData.openai?.assumptions"
          :key="key"
          class="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        <!-- Gemini Column -->
        <div v-if="comparisonData.gemini?.assumptions?.[key]"
             class="p-4 rounded-xl bg-blue-500/5 border border-blue-400/20 space-y-2 flex flex-col">
          <div class="flex items-start justify-between gap-2">
            <h4 class="font-semibold text-sm text-blue-200">{{ comparisonData.gemini.assumptions[key].name }}</h4>
            <span class="text-lg font-bold text-white shrink-0">{{
                formatValue(comparisonData.gemini.assumptions[key].value, comparisonData.gemini.assumptions[key].format)
              }}</span>
          </div>
          <div v-if="comparisonData.gemini.assumptions[key].reasoning"
               class="text-gray-400 text-xs leading-relaxed flex-grow">
            {{ comparisonData.gemini.assumptions[key].reasoning }}
          </div>
        </div>

        <!-- Claude Column -->
        <div v-if="comparisonData.claude?.assumptions?.[key]"
             class="p-4 rounded-xl bg-purple-500/5 border border-purple-400/20 space-y-2 flex flex-col">
          <div class="flex items-start justify-between gap-2">
            <h4 class="font-semibold text-sm text-purple-200">{{ comparisonData.claude.assumptions[key].name }}</h4>
            <span class="text-lg font-bold text-white shrink-0">{{
                formatValue(comparisonData.claude.assumptions[key].value, comparisonData.claude.assumptions[key].format)
              }}</span>
          </div>
          <div v-if="comparisonData.claude.assumptions[key].reasoning"
               class="text-gray-400 text-xs leading-relaxed flex-grow">
            {{ comparisonData.claude.assumptions[key].reasoning }}
          </div>
        </div>

        <!-- OpenAI Column -->
        <div v-if="comparisonData.openai?.assumptions?.[key]"
             class="p-4 rounded-xl bg-green-500/5 border border-green-400/20 space-y-2 flex flex-col">
          <div class="flex items-start justify-between gap-2">
            <h4 class="font-semibold text-sm text-green-200">{{ comparisonData.openai.assumptions[key].name }}</h4>
            <span class="text-lg font-bold text-white shrink-0">{{
                formatValue(comparisonData.openai.assumptions[key].value, comparisonData.openai.assumptions[key].format)
              }}</span>
          </div>
          <div v-if="comparisonData.openai.assumptions[key].reasoning"
               class="text-gray-400 text-xs leading-relaxed flex-grow">
            {{ comparisonData.openai.assumptions[key].reasoning }}
          </div>
        </div>
      </div>
    </div>

    <!-- Fallback: Show single model if no comparison data -->
    <div v-else class="space-y-4">
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
