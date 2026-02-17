<script lang="ts" setup>
import {onMounted, onUnmounted, ref} from 'vue'
import {useWebcamService} from '@/services/webcamService'
import {useFaceDetection} from '@/composables/useFaceDetection'
import {useCommonStyles} from '@/composables/useCommonStyles'
import {CheckCircleIcon} from '@heroicons/vue/24/outline'
import UploadButton from '@/components/UploadButton.vue'
import AssumptionsPanel from '@/components/AssumptionsPanel.vue'
import TermsButton from '@/components/TermsButton.vue'
import TermsPopup from '@/components/TermsPopup.vue'
import PageLayout from '@/components/shared/PageLayout.vue'
import CameraFrame from '@/components/shared/CameraFrame.vue'
import CameraOverlay from '@/components/shared/CameraOverlay.vue'
import CameraControls from '@/components/shared/CameraControls.vue'
import '@/assets/face-detection.css'

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
  reload,
} = useWebcamService()

const {formatField, getBarColorClass} = useCommonStyles()

const termsPopup = ref<InstanceType<typeof TermsPopup> | null>(null)

// Face detection
const {
  faceDetected,
  faceBounds,
  isModelLoading,
  isInitializing,
  loadModel
} = useFaceDetection(videoElement, isStreaming)

// Notification state: show when sessionStorage.comparison_data transitions from empty->present
const showComparisonNotification = ref(false)
let _pollInterval: number | null = null
let _hideTimeout: number | null = null
let _lastSeenComparison: string | null = null
let _lastSeenCompletedAt: number | null = null
let _mountedAt: number = Date.now()

function checkSessionComparison() {
  try {
    const raw = sessionStorage.getItem('comparison_data')

    if (!raw) {
      _lastSeenComparison = null
      _lastSeenCompletedAt = null
      return
    }

    if (raw === _lastSeenComparison) return

    let parsed: any = null
    try {
      parsed = JSON.parse(raw)
    } catch (e) {
      console.warn('comparison_data in sessionStorage is not valid JSON yet', e)
      return
    }

    const completedAt = parsed && typeof parsed.__comparison_completed_at === 'number' ? parsed.__comparison_completed_at : null

    if (completedAt == null || completedAt <= _mountedAt) {
      return
    }

    if (_lastSeenCompletedAt != null && completedAt <= _lastSeenCompletedAt) return

    const requiredKeys = ['gemini', 'claude', 'openai']
    const hasAllKeys = requiredKeys.every(k => {
      if (!parsed || typeof parsed !== 'object') return false
      const v = parsed[k]
      if (v == null) return false

      if (v && typeof v === 'object' && Array.isArray((v as any).assumptions)) {
        return (v as any).assumptions.length > 0
      }

      if (typeof v === 'object') return Object.keys(v).length > 0

      return Boolean(v)
    })

    if (hasAllKeys) {
      _lastSeenComparison = raw
      _lastSeenCompletedAt = completedAt
      showComparisonNotification.value = true
      if (_hideTimeout) {
        clearTimeout(_hideTimeout)
      }
      _hideTimeout = window.setTimeout(() => {
        showComparisonNotification.value = false
        _hideTimeout = null
      }, 5000)
    } else {
    }
  } catch (e) {
    console.error('Error reading comparison_data from sessionStorage', e)
  }
}

onMounted(async () => {
  _mountedAt = Date.now()
  await loadModel()
  startCamera()

  checkSessionComparison()
  _pollInterval = window.setInterval(checkSessionComparison, 1000)
})

onUnmounted(() => {
  if (_pollInterval) {
    clearInterval(_pollInterval);
    _pollInterval = null
  }
  if (_hideTimeout) {
    clearTimeout(_hideTimeout);
    _hideTimeout = null
  }
})
</script>

<template>
  <PageLayout container-class="px-4 sm:px-6 py-4 sm:py-8 mx-auto" style="--panel-w:28rem;">
    
    <TermsPopup ref="termsPopup"/>

    <Transition
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="translate-x-full opacity-0"
        enter-to-class="translate-x-0 opacity-100"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="translate-x-0 opacity-100"
        leave-to-class="translate-x-full opacity-0"
    >
      <div
          v-if="showComparisonNotification"
          class="fixed top-4 right-4 z-50 max-w-sm"
      >
        <div
            class="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg shadow-2xl p-4 border border-indigo-400/50 backdrop-blur-sm">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0">
              <CheckCircleIcon class="w-6 h-6 text-green-300"/>
            </div>
            <div class="flex-1">
              <h4 class="font-semibold text-white text-sm mb-1">
                AI Comparison Ready!
              </h4>
              <p class="text-indigo-100 text-xs">
                All 3 AI models have completed their analysis
              </p>
            </div>
            <button
                class="flex-shrink-0 text-white/70 hover:text-white transition-colors"
                @click="showComparisonNotification = false"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </Transition>
      <div class="flex flex-col md:flex-row items-start justify-center gap-4 md:gap-0">
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

          <CameraFrame>
            <video ref="videoElement"
                   :class="['camera-video', isStreaming ? '' : 'opacity-50']"
                   autoplay playsinline></video>

            <div v-if="(isModelLoading || isInitializing) && isStreaming"
                 class="absolute inset-0 z-10 pointer-events-none flex items-center justify-center">
              <div class="face-detection-loading">
                <div class="loading-text">
                  <span class="loading-dots">{{ isModelLoading ? 'Loading AI Model' : 'Preparing Detection' }}</span>
                </div>
              </div>
            </div>

            <div v-if="faceDetected && isStreaming && !isModelLoading && !isInitializing"
                 class="absolute inset-0 z-10 pointer-events-none">
              <div v-for="face in faceBounds"
                   :key="face.index"
                   :style="{
                     left: face.x + 'px',
                     top: face.y + 'px',
                     width: face.width + 'px',
                     height: face.height + 'px'
                   }"
                   class="face-box face-box-appear">

                <div class="face-info">
                  <div class="info-text">FACE {{ face.index + 1 }}</div>
                </div>
              </div>
            </div>

            <CameraOverlay v-if="!isStreaming && !isLoading" message="Camera not active">
              <template #actions>
                <div class="mt-4 sm:mt-6 flex flex-col gap-2 sm:gap-3">
                  <button
                      class="px-6 sm:px-8 py-3 sm:py-4 cursor-pointer bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium text-base sm:text-lg transition-colors min-h-[44px]"
                      @click="startCamera">Start Camera
                  </button>
                  <UploadButton :label="'Choose file instead'" :onChange="uploadFile" accept="image/*"
                                class="px-4 sm:px-6 py-3 text-sm sm:text-base min-h-[44px]"/>
                </div>
              </template>
            </CameraOverlay>

            <CameraOverlay v-if="isLoading" message="Loading camera..." :show-spinner="true" />

            <CameraControls v-if="isStreaming" :countdown="countdown" aria-label="Take selfie" @capture="takeLatestPicture" />
          </CameraFrame>
        </div>

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

    <canvas ref="canvasElement" class="hidden"></canvas>
    <TermsButton :onBeforeNavigate="stopCamera" class="terms-btn-fixed"/>
  </PageLayout>
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
