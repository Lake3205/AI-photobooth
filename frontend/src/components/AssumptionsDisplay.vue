<script lang="ts" setup>
import {LightBulbIcon} from '@heroicons/vue/24/outline';
import type {AssumptionData} from '@/types/AssumptionType';

const props = defineProps<{
  assumptionsData: AssumptionData
}>();

const isDev = import.meta.env.DEV;

const renderBoldText = (text: string): string => {
  return text
      .replace(/\*\*(.+?):\*\*/g, '<strong class="font-bold text-white">$1:</strong><br>')
      .replace(/\*\*(.+?)\*\*/g, '<strong class="font-bold text-white">$1</strong>')
      .replace(/\*$/g, '');
};

const getAssumptionValue = (heading: string): string | null => {
  if (!props.assumptionsData?.assumptions) {
    if (import.meta.env.DEV) console.log('No assumptions data available');
    return null;
  }

  const normalizedHeading = heading.replace(/:$/, '').trim().toLowerCase();
  if (import.meta.env.DEV) console.log('Looking for heading:', normalizedHeading);

  for (const key in props.assumptionsData.assumptions) {
    const assumption = props.assumptionsData.assumptions[key];
    if (assumption) {
      const assumptionName = assumption.name.toString().toLowerCase();
      if (import.meta.env.DEV) console.log('Comparing heading "' + normalizedHeading + '" with assumption "' + assumptionName + '" Value:', assumption.value);

      if (assumptionName === normalizedHeading) {
        if (import.meta.env.DEV) console.log('✓ Found exact match!');
        return assumption.value.toString();
      }

      if (key.toLowerCase() === normalizedHeading.replace(/\s+/g, '_')) {
        if (import.meta.env.DEV) console.log('✓ Found key match!');
        return assumption.value.toString();
      }

      if (assumptionName.includes(normalizedHeading)) {
        if (import.meta.env.DEV) console.log('✓ Found partial match (assumption contains heading)!');
        return assumption.value.toString();
      }

      if (normalizedHeading.includes(assumptionName)) {
        if (import.meta.env.DEV) console.log('✓ Found partial match (heading contains assumption)!');
        return assumption.value.toString();
      }
    }
  }

  if (import.meta.env.DEV) console.log('✗ No match found for:', normalizedHeading);
  return null;
};

const parseThoughtSections = (thought: string) => {
  const lines = thought.split('\n');
  const sections: Array<{ heading?: string; content: string }> = [];
  let currentParagraph = '';
  let hasSeenCategory = false;

  for (const line of lines) {
    const trimmed = line.trim();

    if (!trimmed) {
      if (hasSeenCategory && currentParagraph) {
        sections.push({content: currentParagraph});
        currentParagraph = '';
      }
      continue;
    }

    const categoryMatch = trimmed.match(/^\*\*([^*]+)\*\*:?\s*(.*)$/);

    if (categoryMatch && categoryMatch[1] && categoryMatch[2] !== undefined) {
      const potentialHeading = categoryMatch[1].trim();
      const contentAfterHeading = categoryMatch[2].trim();

      const isLikelyCategory = potentialHeading.length < 30 &&
          !potentialHeading.includes('.') &&
          !potentialHeading.includes('?');

      if (isLikelyCategory) {
        hasSeenCategory = true;

        if (currentParagraph) {
          sections.push({content: currentParagraph});
          currentParagraph = '';
        }

        sections.push({
          heading: potentialHeading.endsWith(':') ? potentialHeading : potentialHeading + ':',
          content: contentAfterHeading
        });
        continue;
      }
    }

    currentParagraph += (currentParagraph ? ' ' : '') + trimmed;
  }

  if (currentParagraph) {
    sections.push({content: currentParagraph});
  }

  return sections;
};
</script>

<template>
  <div
      class="rounded-2xl bg-gradient-to-br from-white/5 to-white/2 border border-white/10 backdrop-blur-sm p-4 sm:p-6 space-y-4 sm:space-y-6">
    <h2 class="text-xl sm:text-2xl font-bold text-white mb-4 flex items-center gap-2">
      <LightBulbIcon class="w-6 h-6 text-indigo-400"/>
      AI-Generated Assumptions
    </h2>

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
      <div v-if="assumptionsData.thought">
        <div class="font-bold mb-2">DEBUG - Parsed Sections:</div>
        <div v-for="(section, idx) in parseThoughtSections(assumptionsData.thought)" :key="idx" class="mb-1">
          <span class="text-purple-300">{{ idx }}:</span>
          <span v-if="section.heading" class="text-cyan-300">HEADING: "{{ section.heading }}"</span>
          <span v-else class="text-orange-300">PARAGRAPH ({{ section.content.substring(0, 50) }}...)</span>
        </div>
      </div>
    </div>

    <!-- Assumptions Display -->
    <div v-if="assumptionsData.thought" class="space-y-4">
      <template v-for="(section, index) in parseThoughtSections(assumptionsData.thought)" :key="index">
        <div v-if="section.heading"
             class="relative overflow-hidden p-4 sm:p-5 rounded-xl bg-white/5 border border-white/10 space-y-3 transition">
          <div
              class="absolute inset-0 flex items-center justify-end px-4 sm:px-6 pointer-events-none select-none">
            <span
                class="text-6xl sm:text-7xl md:text-8xl lg:text-9xl font-black text-white/[0.15] leading-none text-right break-all">{{
                getAssumptionValue(section.heading) || 'NO_VALUE'
              }}</span>
          </div>
          <div class="relative z-10">
            <h3 class="font-semibold text-base sm:text-lg text-indigo-300 mb-2">{{ section.heading }}</h3>
            <div v-if="isDev" class="text-xs text-yellow-400 mb-2">
              DEBUG: Looking for "{{ section.heading }}" → Found:
              "{{ getAssumptionValue(section.heading) || 'NO MATCH' }}"
            </div>
            <div class="text-gray-400 text-sm leading-relaxed" v-html="renderBoldText(section.content)"></div>
          </div>
        </div>

        <!-- Intro/outro paragraphs -->
        <div v-else
             class="p-4 sm:p-5 rounded-xl bg-white/5 border border-white/10 space-y-3 transition mb-6">
          <p class="text-gray-400 text-sm leading-relaxed" v-html="renderBoldText(section.content)"></p>
        </div>
      </template>
    </div>

    <!-- Fallback: Show assumptions without thought process if thought is not available -->
    <div v-else class="space-y-4">
      <div v-for="(assumption, key) in assumptionsData.assumptions" :key="key"
           class="relative overflow-hidden p-4 sm:p-5 rounded-xl bg-white/5 border border-white/10 space-y-3 hover:bg-white/10 transition">
        <div
            class="absolute inset-0 flex items-center justify-end px-4 sm:px-6 pointer-events-none select-none">
          <span
              class="text-6xl sm:text-7xl md:text-8xl lg:text-9xl font-black text-white/[0.15] leading-none text-right break-all">{{
              assumption.value.toString()
            }}</span>
        </div>
        <div class="relative z-10">
          <h3 class="font-semibold text-base sm:text-lg text-indigo-300">{{ assumption.name.toString() }}</h3>
          <div v-if="assumption.reasoning" class="text-gray-400 text-sm italic">
            {{ assumption.reasoning.toString() }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
