<script lang="ts" setup>
import {onMounted} from 'vue'
import {useWebcamService} from '@/services/webcamService'
import {CameraIcon} from '@heroicons/vue/24/outline'
import UploadButton from '@/components/UploadButton.vue'
import AssumptionsPanel from '@/components/AssumptionsPanel.vue'

const {
  // Template refs
  videoElement,
  canvasElement,

  // Webcam state
  isStreaming,
  isLoading,

  // Analysis state
  analysisData,
  isAnalyzing,
  analysisError,

  // UI state
  countdown,
  latestImage,

  // Webcam functions
  startCamera,
  takeLatestPicture,

  // Helper functions
  uploadFile,
  getBarColorClass,
  getConsistentPercentage,
  formatField,
} = useWebcamService()

// Auto-start camera when component mounts
onMounted(() => {
  startCamera()
})
</script>

<template>
  <main class="relative overflow-hidden bg-black text-white min-h-screen">
    <div class="pointer-events-none absolute inset-0 opacity-80">
      <div
          class="absolute -top-60 -left-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-br from-blue-500/60 to-blue-300/30 blur-3xl"></div>
      <div
          class="absolute -bottom-60 -right-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-tr from-blue-400/50 to-white/10 blur-3xl"></div>
      <div
          class="absolute inset-0 bg-[radial-gradient(circle_at_1px_1px,rgba(255,255,255,0.08)_1px,transparent_1px)] [background-size:24px_24px]"></div>
    </div>

    <div class="relative z-10 px-6 py-8 mx-auto">
      <!-- Main row: left = title + live camera (always visible), right = result + assumptions (appears after capture) -->
      <div class="flex flex-col md:flex-row items-start gap-6">
        <!-- Left column: title + live camera -->
        <div :class="['left-column transition-transform duration-500 ease-in-out', latestImage ? 'slide-left' : '']"
             style="min-width:320px;">
          <header class="mb-4">
            <h1 class="bg-gradient-to-b from-white to-blue-300 bg-clip-text text-3xl font-extrabold tracking-tight text-transparent">
              Take a Selfie
            </h1>
            <p class="mt-2 text-blue-100/90">Position yourself in the frame and capture the perfect shot</p>
          </header>

          <div class="relative rounded-3xl border border-white/15 bg-white/5 p-2 overflow-hidden">
            <div class="rounded-2xl bg-gradient-to-b from-white/5 to-transparent p-3">
              <div
                  class="relative aspect-[16/9] w-full rounded-xl overflow-hidden bg-black/50 flex items-center justify-center">
                <video ref="videoElement" :class="['w-full h-full object-cover', isStreaming ? '' : 'opacity-50']"
                       autoplay playsinline></video>

                <div v-if="!isStreaming && !isLoading"
                     class="absolute inset-0 flex items-center justify-center bg-black/70">
                  <div class="text-center">
                    <CameraIcon class="h-20 w-20 text-white/50 mx-auto mb-4"/>
                    <p class="text-white/70 text-lg">Camera not active</p>
                    <div class="mt-6 flex flex-col gap-3">
                      <button
                          class="px-8 py-4 cursor-pointer bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium text-lg transition-colors"
                          @click="startCamera">Start Camera
                      </button>
                      <UploadButton :label="'Choose file instead'" :onChange="uploadFile" accept="image/*"
                                    class="px-6 py-3 text-base"/>
                    </div>
                  </div>
                </div>

                <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-black/70">
                  <div class="text-center">
                    <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-white mx-auto mb-4"></div>
                    <p class="text-white/70 text-lg">Loading camera...</p>
                  </div>
                </div>

                <div v-if="isStreaming" class="absolute bottom-8 left-1/2 transform -translate-x-1/2">
                  <button :disabled="countdown > 0"
                          class="group relative p-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full transition-all duration-200 hover:scale-110"
                          tabindex="1" @click="takeLatestPicture">
                    <span
                        class="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500/20 to-blue-300/20 group-hover:from-blue-500/30 group-hover:to-blue-300/30 transition-all block"></span>
                    <CameraIcon class="relative h-7 w-7 text-white"/>
                    <span v-if="countdown > 0"
                          class="absolute inset-0 flex items-center justify-center text-3xl font-bold text-white bg-black/60 rounded-full z-10">{{
                        countdown
                      }}</span>
                  </button>
                </div>

              </div>
            </div>
          </div>
        </div>

        <!-- Right column: small captured image + assumptions -->
        <div :class="latestImage ? 'show' : 'hidden'"
             class="right-column w-full md:w-150 transition-all duration-500 ease-in-out">
          <div v-if="latestImage" class="w-full">
            <div class="rounded-2xl bg-white/5 to-transparent p-2">
              <div class="relative w-full aspect-[16/9] rounded-md overflow-hidden">
                <img
                    :src="latestImage.dataUrl"
                    alt="Preview"
                    class="absolute inset-0 w-full h-full object-contain"
                />
              </div>
            </div>

            <AssumptionsPanel
                :analysisData="analysisData"
                :analysisError="analysisError"
                :formatField="formatField"
                :getBarColorClass="getBarColorClass"
                :getConsistentPercentage="getConsistentPercentage"
                :isAnalyzing="isAnalyzing"
            />
          </div>
        </div>
      </div>
    </div>

    <canvas ref="canvasElement" class="hidden"></canvas>
  </main>
</template>

<style scoped>
/* Use GPU-accelerated transforms and avoid layout thrashing for smooth motion */
.left-column {
  will-change: transform;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  transition: transform 360ms cubic-bezier(0.22, 0.9, 0.3, 1);
  transform: translate3d(0, 0, 0);
}

/* right column slides in from slightly right and fades in after left has moved */
.right-column {
  will-change: opacity, transform;
  transform: translate3d(1rem, 0, 0);
  opacity: 0;
  pointer-events: none;
  transition: transform 320ms ease, opacity 320ms ease;
}

.right-column.show {
  transform: translate3d(0, 0, 0);
  opacity: 1;
  pointer-events: auto;
  transition-delay: 180ms;
}

.right-column.hidden {
  opacity: 0;
  pointer-events: none;
}

@media (max-width: 768px) {
  .left-column {
    transform: none !important;
  }

  .right-column {
    transform: none !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    transition-delay: 0ms !important;
  }
}
</style>
