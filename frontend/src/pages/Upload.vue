<script lang="ts" setup>
import {computed, ref} from 'vue'
import {useUploadStore} from '@/services/uploadStore'
import LandingButton from '@/components/LandingButton.vue'
import UploadButton from '@/components/UploadButton.vue'
import {ArrowUpTrayIcon} from '@heroicons/vue/24/outline'

const {state, setImage, clearImage} = useUploadStore()

const dragOver = ref(false)
const error = ref<string | null>(null)

function onFileSelected(e: Event) {
  const files = (e.target as HTMLInputElement).files
  const file = files && files.length > 0 ? files[0] : undefined
  if (!file) return
  handleFile(file)
}

function handleFile(file: File) {
  error.value = null
  if (!file.type.startsWith('image/')) {
    error.value = 'Please select an image file (PNG, JPG, GIF, etc.)'
    return
  }
  setImage(file)
}

function onDrop(e: DragEvent) {
  dragOver.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) handleFile(file)
}

const hasImage = computed(() => !!state.image)
</script>

<template>
  <main class="relative overflow-hidden bg-black text-white">
    <!-- Soft background -->
    <div class="pointer-events-none absolute inset-0 opacity-80">
      <div
          class="absolute -top-60 -left-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-br from-indigo-600/60 to-fuchsia-600/10 blur-3xl"></div>
      <div
          class="absolute -bottom-60 -right-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-tr from-fuchsia-600/60 to-indigo-600/10 blur-3xl"></div>
      <div
          class="absolute inset-0 bg-[radial-gradient(circle_at_1px_1px,rgba(255,255,255,0.08)_1px,transparent_1px)] [background-size:24px_24px]"></div>
    </div>

    <section class="relative z-10 mx-auto flex min-h-screen max-w-5xl flex-col items-center justify-center px-6">
      <div class="w-full max-w-2xl">
        <header class="mb-3 text-center">
          <h2 class="bg-gradient-to-b from-white to-neutral-400 bg-clip-text text-4xl font-extrabold tracking-tight text-transparent sm:text-5xl leading-normal">
            Upload your image
          </h2>
          <p class="mt-3 text-neutral-300/90">Drag and drop, or choose a file. A crisp preview appears instantly.</p>
        </header>

        <div
            :class="dragOver ? 'ring-2 ring-fuchsia-500/50 shadow-[0_0_32px_8px_rgba(192,132,252,0.4)] bg-gradient-to-br from-fuchsia-500/10 to-indigo-500/10' : ''"
            class="group relative rounded-2xl border border-white/15 bg-white/5 p-1 backdrop-blur"
            @dragenter.prevent="dragOver = true"
            @dragover.prevent="dragOver = true"
            @dragleave.prevent="dragOver = false"
            @drop.prevent="onDrop"
        >
          <div class="rounded-xl bg-gradient-to-b from-white/5 to-transparent p-8">
            <div class="flex flex-col items-center justify-center text-center">
              <div
                  class="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-white/10 ring-1 ring-white/20">
                <ArrowUpTrayIcon class="h-8 w-8 text-white/70"/>
              </div>
              <p class="text-lg font-medium">Drop an image here</p>
              <p class="mt-1 text-sm text-neutral-400">PNG, JPG, GIF up to ~10MB</p>
              <div class="mt-6">
                <UploadButton
                    :label="'Choose file'"
                    :onChange="onFileSelected"
                    accept="image/*"
                    class="px-6 py-3 text-base"
                />
              </div>
              <p v-if="error" class="mt-4 text-sm text-rose-300">{{ error }}</p>
            </div>
          </div>
        </div>

        <div v-if="hasImage" class="mt-8 grid gap-6 sm:grid-cols-2">
          <div class="overflow-hidden rounded-xl border border-white/10 bg-white/5 p-1">
            <div class="overflow-hidden rounded-lg bg-black/30">
              <img :src="state.image!.url" alt="Preview" class="block max-h-[320px] w-full object-contain"/>
            </div>
          </div>
          <div class="flex flex-col justify-between rounded-xl border border-white/10 bg-white/5 p-6">
            <div>
              <h3 class="text-xl font-semibold">Ready to go</h3>
              <p class="mt-2 text-neutral-300/90">Your image is cached locally and ready for the next step.</p>
            </div>
            <div class="mt-6 flex flex-wrap items-center gap-3">
              <LandingButton
                  :label="'Continue'"
                  :onClick="() => {/* TODO: Add logic for assumptions */}"
                  class="bg-white/10 text-white ring-1 ring-white/15 hover:bg-white/15 px-5 py-2.5 text-sm font-semibold"
              />
              <LandingButton
                  :label="'Remove'"
                  :onClick="clearImage"
                  class="bg-white/10 text-white ring-1 ring-white/15 hover:bg-white/15 px-5 py-2.5 text-sm font-semibold"
              />
            </div>
          </div>
        </div>

        <div class="mt-10 text-center text-sm text-neutral-500">
          <router-link class="hover:text-neutral-300" to="/">Back to start</router-link>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
</style>
