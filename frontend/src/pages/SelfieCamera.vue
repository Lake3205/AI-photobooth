<script lang="ts" setup>
import {onMounted, ref} from 'vue'
import {useWebcamService} from '@/services/webcamService'
import {CameraIcon} from '@heroicons/vue/24/outline'
import UploadButton from '@/components/UploadButton.vue'
import AssumptionsPanel from '@/components/AssumptionsPanel.vue'
import TermsButton from '@/components/TermsButton.vue'
import TermsPopup from '@/components/TermsPopup.vue'

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

  clearAllData,

  // Webcam functions
  startCamera,
  stopCamera,
  takeLatestPicture,

  // Helper functions
  uploadFile,
  getBarColorClass,
  formatField,
  reload,
} = useWebcamService()

const termsPopup = ref<InstanceType<typeof TermsPopup> | null>(null)

// Auto-start camera when component mounts
onMounted(() => {
  startCamera()
})
</script>

<template>
  <main class="relative overflow-hidden bg-black text-white min-h-screen">

    <TermsPopup ref="termsPopup"/>

    <div class="pointer-events-none absolute inset-0 opacity-80">
      <div
          class="absolute -top-60 -left-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-br from-blue-500/60 to-blue-300/30 blur-3xl"></div>
      <div
          class="absolute -bottom-60 -right-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-tr from-blue-400/50 to-white/10 blur-3xl"></div>
      <div
          class="absolute inset-0 bg-[radial-gradient(circle_at_1px_1px,rgba(255,255,255,0.08)_1px,transparent_1px)] [background-size:24px_24px]"></div>
    </div>

    <div class="relative z-10 px-4 sm:px-6 py-4 sm:py-8 mx-auto" style="--panel-w:28rem;">
      <!-- Main row: left = title + live camera (always visible), right = result + assumptions (appears after capture) -->
      <div class="flex flex-col md:flex-row items-start justify-center gap-4 md:gap-0">
        <!-- Left column: title + live camera -->
        <div
            :class="['left-column transition-transform duration-500 ease-in-out w-full md:w-auto', latestImage ? 'slide-left' : '']"
            class="min-w-full md:min-w-[320px]"
            style="flex:1 1 auto; max-width: calc(100% - var(--panel-w));">
          <header class="mb-3 sm:mb-4">
            <h1 class="bg-gradient-to-b from-white to-blue-300 bg-clip-text text-2xl sm:text-3xl font-extrabold tracking-tight text-transparent">
              Take a Selfie
            </h1>
            <p class="mt-1 sm:mt-2 text-sm sm:text-base text-blue-100/90">Position yourself in the frame and capture the
              perfect shot</p>
          </header>

          <div
              class="relative rounded-2xl sm:rounded-3xl border border-white/15 bg-white/5 p-1.5 sm:p-2 overflow-hidden">
            <div
                class="relative aspect-[16/9] w-full rounded-xl overflow-hidden bg-black/50 flex items-center justify-center">
              <video ref="videoElement"
                     :class="['absolute inset-0 w-full h-full object-cover z-0', isStreaming ? '' : 'opacity-50']"
                     autoplay playsinline></video>

              <div v-if="!isStreaming && !isLoading"
                   class="absolute inset-0 z-10 flex items-center justify-center bg-black/70 rounded-xl p-4">
                <div class="text-center">
                  <CameraIcon class="h-16 sm:h-20 w-16 sm:w-20 text-white/50 mx-auto mb-3 sm:mb-4"/>
                  <p class="text-white/70 text-base sm:text-lg">Camera not active</p>
                  <div class="mt-4 sm:mt-6 flex flex-col gap-2 sm:gap-3">
                    <button
                        class="px-6 sm:px-8 py-3 sm:py-4 cursor-pointer bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium text-base sm:text-lg transition-colors min-h-[44px]"
                        @click="startCamera">Start Camera
                    </button>
                    <UploadButton :label="'Choose file instead'" :onChange="uploadFile" accept="image/*"
                                  class="px-4 sm:px-6 py-3 text-sm sm:text-base min-h-[44px]"/>
                  </div>
                </div>
              </div>

              <div v-if="isLoading" class="absolute inset-0 z-10 flex items-center justify-center bg-black/70">
                <div class="text-center">
                  <div
                      class="animate-spin rounded-full h-12 sm:h-16 w-12 sm:w-16 border-b-2 border-white mx-auto mb-3 sm:mb-4"></div>
                  <p class="text-white/70 text-base sm:text-lg">Loading camera...</p>
                </div>
              </div>

              <div v-if="isStreaming" class="absolute bottom-4 sm:bottom-8 left-1/2 transform -translate-x-1/2 z-20">
                <button :disabled="countdown > 0"
                        class="group relative p-2.5 sm:p-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full transition-all duration-200 hover:scale-110 min-w-[44px] min-h-[44px]"
                        tabindex="1" @click="takeLatestPicture">
                    <span
                        class="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500/20 to-blue-300/20 group-hover:from-blue-500/30 group-hover:to-blue-300/30 transition-all block"></span>
                  <CameraIcon class="relative h-6 sm:h-7 w-6 sm:w-7 text-white"/>
                  <span v-if="countdown > 0"
                        class="absolute inset-0 flex items-center justify-center text-2xl sm:text-3xl font-bold text-white bg-black/60 rounded-full z-10">{{
                      countdown
                    }}</span>
                </button>
              </div>

            </div>
          </div>
        </div>

        <!-- Right column: small captured image + assumptions -->
        <div :class="latestImage ? 'show' : 'hidden'"
             class="right-column w-full md:w-150 transition-all duration-500 ease-in-out"
             style="--panel-w:28rem;">
          <div v-if="latestImage" class="w-full">
            <div class="rounded-xl sm:rounded-2xl bg-white/5 to-transparent p-1.5 sm:p-2">
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
                :isAnalyzing="isAnalyzing"
            />
            <button
                class="fixed bottom-2 right-2 w-8 h-8 bg-gray-500/20 hover:bg-gray-500/30 rounded-full opacity-10 hover:opacity-50 transition-opacity"
                @click="reload"
            ></button>
          </div>
          <button
              class="w-full px-4 py-3 bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 text-red-300 rounded-lg transition-colors min-h-[44px] text-right md:text-center"
              @click="clearAllData"
          >
            Delete Photo
          </button>
        </div>
      </div>
    </div>

    <canvas ref="canvasElement" class="hidden"></canvas>
    <TermsButton :onBeforeNavigate="stopCamera" class="terms-btn-fixed"/>
  </main>
</template>

<style scoped>
.left-column {
  will-change: transform;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  transition: transform 500ms cubic-bezier(0.22, 0.9, 0.3, 1);
  transform: translate3d(0, 0, 0);
}

.left-column.slide-left {
  transform: translate3d(-0.5rem, 0, 0);
}

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
