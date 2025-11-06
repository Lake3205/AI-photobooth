<script lang="ts" setup>
import {
  ArrowTrendingUpIcon,
  BellIcon,
  BriefcaseIcon,
  CalendarIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  UserGroupIcon
} from '@heroicons/vue/24/outline'

import BaseCard from '../components/BaseCard.vue'
</script>

<template>
  <section class="p-6 md:p-10 space-y-10">
    <!-- Header -->
    <header class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-4xl font-extrabold bg-gradient-to-r from-indigo-200 via-fuchsia-200 to-pink-300 text-transparent bg-clip-text">
          Dashboard
        </h1>
        <p class="text-white/60 text-sm">Overview of your activity, stats, and projects.</p>
      </div>
      <div class="flex gap-3">
        <button
            class="px-4 py-2 bg-white/10 border border-white/20 rounded-xl text-sm text-white/90 hover:bg-white/20 transition">
          <BellIcon class="h-5 w-5 inline-block mr-1"/>
          Notifications
        </button>
        <button
            class="px-4 py-2 bg-indigo-500/20 border border-indigo-400/30 rounded-xl text-sm text-indigo-100 hover:bg-indigo-500/30 transition">
          <Cog6ToothIcon class="h-5 w-5 inline-block mr-1"/>
          Settings
        </button>
      </div>
    </header>

    <!-- Stats Section -->
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <BaseCard v-for="card in 4" :key="card" :subtitle="`Metric ${card}`">
        <template #icon>
          <component :is="[ChartBarIcon, UserGroupIcon, BriefcaseIcon, ArrowTrendingUpIcon][card - 1]"
                     class="h-6 w-6 text-indigo-200"/>
        </template>
        <template #title>
          {{ (Math.random() * 1000).toFixed(0) }}
        </template>
      </BaseCard>
    </div>

    <!-- Projects / Activity Section -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left column: projects -->
      <div class="lg:col-span-2 space-y-4">
        <h2 class="text-lg font-semibold text-white/80 flex items-center gap-2">
          <BriefcaseIcon class="h-5 w-5 text-white/60"/>
          Recent Projects
        </h2>

        <div class="grid gap-4 sm:grid-cols-2">
          <BaseCard v-for="n in 4" :key="n"
                    extraClass="project-card p-4 rounded-2xl bg-gradient-to-tr from-indigo-900/20 to-fuchsia-900/10 border border-white/10 hover:shadow-xl hover:-translate-y-2 transition">
            <template #title>
              <h3 class="text-white font-semibold truncate">Project {{ n }}</h3>
            </template>

            <div class="flex flex-col gap-2 mt-2">
              <p class="text-white/60 text-sm line-clamp-2">A quick summary of what this project does or its current
                progress...</p>
              <div class="flex items-center justify-between mt-3 text-xs text-white/60">
                <span>Updated {{ n }}d ago</span>
                <span class="px-2 py-1 bg-white/10 rounded-lg">In progress</span>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>

      <!-- Right column: activity -->
      <div>
        <h2 class="text-lg font-semibold text-white/80 flex items-center gap-2">
          <CalendarIcon class="h-5 w-5 text-white/60"/>
          Recent Activity
        </h2>

        <ul class="space-y-3 mt-3">
          <li v-for="i in 5" :key="i"
              class="p-3 rounded-xl bg-white/5 border border-white/10 flex items-start gap-3 hover:bg-white/10 transition">
            <div class="h-8 w-8 rounded-lg bg-indigo-500/30 flex items-center justify-center">
              <ArrowTrendingUpIcon class="h-4 w-4 text-indigo-100"/>
            </div>
            <div class="text-sm text-white/80 leading-tight">
              <p><span class="text-white font-medium">User {{ i }}</span> added a new entry</p>
              <p class="text-white/50 text-xs">Just now</p>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>
