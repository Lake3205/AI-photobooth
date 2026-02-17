<script lang="ts" setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import BaseCard from './BaseCard.vue'
import type { Chart } from 'chart.js'

const props = defineProps<{
  title: string
  subtitle?: string
  chartId: string
  chartData: any
  createChart: (canvas: HTMLCanvasElement, data: any) => Chart | null
}>()

const chart = ref<Chart | null>(null)

const destroyChart = () => {
  if (chart.value) {
    try {
      chart.value.destroy()
    } catch (e) {
      console.warn('Error destroying chart:', e)
    }
    chart.value = null
  }
}

const renderChart = () => {
  const canvas = document.getElementById(props.chartId) as HTMLCanvasElement
  if (canvas && props.chartData) {
    destroyChart()
    chart.value = props.createChart(canvas, props.chartData)
  }
}

onMounted(renderChart)

watch(() => props.chartData, renderChart, { deep: true })

onBeforeUnmount(destroyChart)
</script>

<template>
  <BaseCard class="p-4 sm:p-6">
    <h2 class="text-lg sm:text-xl font-semibold mb-4 text-white">{{ title }}</h2>
    <p v-if="subtitle" class="text-sm text-gray-400 mb-4">{{ subtitle }}</p>
    <div class="h-64 sm:h-80">
      <canvas :id="chartId"></canvas>
    </div>
    <slot></slot>
  </BaseCard>
</template>

<style scoped>
canvas {
  max-height: 100%;
  max-width: 100%;
}
</style>
