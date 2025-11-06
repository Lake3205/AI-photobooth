<script lang="ts" setup>
import {computed} from 'vue'
import type {AssumptionData, AssumptionType} from '@/types/AssumptionType'
import {
  AcademicCapIcon,
  ChartBarIcon,
  CurrencyDollarIcon,
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
  getConsistentPercentage: (f: AssumptionType) => number,
  getBarColorClass: (k: string) => string,
}>()

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
  if (name.includes('ethnic') || name.includes('ethnicity') || name.includes('people')) return UsersIcon
  if (name.includes('relig') || name.includes('belief')) return GlobeAltIcon
  if (name.includes('polit') || name.includes('opinion')) return ChartBarIcon
  if (name.includes('theft') || name.includes('risk')) return ShieldExclamationIcon
  if (name.includes('weight')) return ScaleIcon
  if (name.includes('school') || name.includes('education') || name.includes('level')) return AcademicCapIcon
  if (name.includes('salary') || name.includes('debt') || name.includes('currency') || name.includes('annual')) return CurrencyDollarIcon
  if (field.format === 'percentage' || name.includes('score')) return ChartBarIcon

  return QuestionMarkCircleIcon
}

// Determine whether to show a progress bar for a field
const percentForField = (field: AssumptionType): number | null => {
  if (field.format === 'percentage' && typeof field.value === 'number') {
    return Math.min(Math.max(field.value, 0), 100)
  }
  if (typeof field.value === 'number' && field.min !== undefined && field.max !== undefined) {
    if (field.max === field.min) return 100
    const clamped = Math.min(Math.max(field.value, field.min), field.max)
    return ((clamped - field.min) / (field.max - field.min)) * 100
  }

  return null
}

const averageConfidence = computed(() => {
  const percents: number[] = []
  for (const f of entries.value) {
    const p = percentForField(f)
    if (p !== null) percents.push(p)
  }
  if (percents.length === 0) return null
  const sum = percents.reduce((s, v) => s + v, 0)
  return Math.round(sum / percents.length)
})
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
          class="summary-card rounded-2xl p-3 bg-gradient-to-br from-white/6 to-transparent border border-white/10 flex items-center justify-between">
        <div>
          <h3 class="text-2xl md:text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-indigo-100 to-fuchsia-200 pb-2">
            Insights</h3>
        </div>

        <div class="text-right">
          <div class="text-sm text-white/70">Confidence</div>
          <div class="text-3xl font-bold text-white mt-1">
            <template v-if="averageConfidence !== null">{{ averageConfidence }}%</template>
            <template v-else>—</template>
          </div>
        </div>
      </div>

      <div v-if="textFields.length > 0" class="text-section">
        <div class="flex flex-wrap items-center gap-3">
          <template v-for="field in textFields" :key="field.name">
            <div :aria-label="field.name" :class="['assumption-chip', props.getBarColorClass(field.name)]" role="group">
              <div class="chip-left">
                <div class="chip-badge text-xs font-semibold">
                  <component :is="getIcon(field)" class="h-5 w-5 text-white/90"/>
                </div>
              </div>
              <div class="chip-body">
                <div class="chip-title text-sm font-semibold">{{ field.name }}</div>
                <div class="chip-value text-xs text-white/90">{{ props.formatField(field) }}</div>
              </div>
            </div>
          </template>
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

            <div v-if="percentForField(field) !== null" class="mt-4">
              <div class="flex items-center justify-between text-xs text-white/60 mb-2">
                <div>Normalized</div>
                <div class="font-semibold">{{ Math.round(percentForField(field) ?? 0) }}%</div>
              </div>
              <div class="w-full bg-white/8 h-2 rounded-full overflow-hidden">
                <div :class="props.getBarColorClass(field.name)" :style="{ width: (percentForField(field) ?? 0) + '%' }"
                     class="h-2 rounded-full transition-all"></div>
              </div>
            </div>
          </div>
        </div>
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

.summary-card:hover {
  transform: translateY(-6px)
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

.assumption-chip:hover {
  transform: translateY(-4px);
  box-shadow: 0 18px 44px rgba(0, 0, 0, 0.26);
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

.assumption-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 28px 64px rgba(2, 6, 23, 0.55);
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