<script lang="ts" setup>
import {computed} from 'vue'
import type {AssumptionData, AssumptionType} from '@/types/AssumptionType'
import {useCookieService} from '@/services/cookieService';
import {
  ChartBarIcon,
  CurrencyDollarIcon,
  FlagIcon,
  GlobeAltIcon,
  QuestionMarkCircleIcon,
  ScaleIcon,
  ShieldExclamationIcon,
  UserIcon,
  UsersIcon,
} from '@heroicons/vue/24/outline'

const props = defineProps<{
  analysisData: AssumptionData | null,
  isAnalyzing: boolean,
  analysisError: string | null,
  formatField: (f: AssumptionType) => string,
  getBarColorClass: (k: string) => string,
}>()

const {getCookie} = useCookieService();

const entries = computed(() => {
  if (!props.analysisData) return []
  return Object.keys(props.analysisData).map((k) => (props.analysisData as any)[k]) as AssumptionType[]
})

// Separate text and numeric fields for better presentation
const textFields = computed(() => entries.value.filter(f => f.format === 'text'))
const numericFields = computed(() => entries.value.filter(f => f.format !== 'text'))

// Icon selection helper
const getIcon = (field: AssumptionType) => {
  const name = field.name.toLowerCase()

  if (name.includes('age')) return UserIcon
  if (name.includes('ethnic') || name.includes('ethnicity') || name.includes('people')) return FlagIcon
  if (name.includes('relig') || name.includes('belief')) return GlobeAltIcon
  if (name.includes('polit') || name.includes('opinion')) return ChartBarIcon
  if (name.includes('theft') || name.includes('risk')) return ShieldExclamationIcon
  if (name.includes('weight')) return ScaleIcon
  if (name.includes('gender')) return UsersIcon
  if (name.includes('salary') || name.includes('debt') || name.includes('currency') || name.includes('annual')) return CurrencyDollarIcon
  if (field.format === 'percentage' || name.includes('score') || name.includes('iq')) return ChartBarIcon

  return QuestionMarkCircleIcon
}
</script>

<template>
  <section class="assumptions-root p-3">
    <div v-if="props.isAnalyzing" class="text-center py-10">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
      <p class="text-white/80">Analyzing image...</p>
    </div>

    <div v-else-if="props.analysisError" class="p-4 bg-red-500/8 border border-red-500/20 rounded-xl backdrop-blur-sm">
      <p class="text-red-300 text-sm">{{ props.analysisError }}</p>
    </div>

    <div v-else-if="entries.length === 0" class="space-y-3 text-center py-8">
      <p class="text-white/60">No assumptions yet — capture or upload an image to generate insights.</p>
    </div>

    <div v-else class="grid gap-6">
      <div
          class="summary-card rounded-2xl p-3 bg-gradient-to-br from-white/6 to-transparent border border-white/10 flex items-center justify-start">
        <div>
          <h3 class="text-2xl md:text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-indigo-100 to-fuchsia-200 pb-2">
            Insights</h3>
        </div>
      </div>

      <div v-if="textFields.length > 0" class="text-section">
        <div class="grid gap-3 grid-cols-1 sm:grid-cols-2">
          <div v-for="field in textFields" :key="field.name" :aria-label="field.name" role="group">
            <div
                class="assumption-chip w-full flex items-center gap-3 p-3 rounded-xl bg-white/4 border border-white/8 shadow-sm">
              <div
                  :class="['chip-badge flex-shrink-0 h-10 w-10 rounded-lg flex items-center justify-center', props.getBarColorClass(field.name)]">
                <component :is="getIcon(field)" class="h-5 w-5 text-white/95"/>
              </div>

              <div class="chip-body min-w-0">
                <div class="chip-title text-sm font-semibold text-white truncate">{{ field.name }}</div>
                <div class="chip-value text-xs text-white/80 truncate">{{ props.formatField(field) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="numericFields.length > 0" class="numeric-section">
        <div class="grid gap-4 sm:grid-cols-2">
          <div v-for="field in numericFields" :key="field.name" :aria-label="field.name" class="assumption-card"
               role="article">
            <div class="flex items-start justify-between gap-4">
              <div class="flex items-start gap-3">
                <div :class="['avatar', props.getBarColorClass(field.name)]">
                  <component :is="getIcon(field)" class="h-6 w-6 text-white/95"/>
                </div>
                <div>
                  <div class="text-sm text-white/70">{{ field.name }}</div>
                  <div class="text-2xl md:text-3xl font-extrabold text-white">{{ props.formatField(field) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="w-full mb-3 flex items-center justify-center">
        <router-link :to="'/form?token=' + getCookie('form_token')" class="text-center hover:underline">The AI made some
          bold guesses... care to correct it?
        </router-link>
      </div>
    </div>
  </section>
</template>

<style scoped>
.rounded-2xl {
  box-shadow: 0 40px 80px rgba(79, 70, 229, 0.22), 0 10px 30px rgba(0, 0, 0, 0.28);
}

.summary-card {
  backdrop-filter: blur(6px);
  transition: transform 220ms ease, box-shadow 220ms ease;
}

.assumption-chip {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 6px 12px;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
  transition: transform 180ms ease, box-shadow 180ms ease;
}

.chip-left {
  display: flex;
  align-items: center
}

.chip-badge {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.06);
}

.chip-body {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-right: 3px;
}

.assumption-card {
  padding: 8px;
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.02), rgba(255, 255, 255, 0.01));
  border: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: 0 18px 40px rgba(2, 6, 23, 0.45);
  transition: transform 200ms ease, box-shadow 200ms ease;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600
}
</style>