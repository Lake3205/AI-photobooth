<script lang="ts" setup>
import {computed, onMounted, ref, watch} from 'vue'
import {useWebcamService} from '@/services/webcamService'
import {useFaceDetection} from '@/composables/useFaceDetection'
import {useCommonStyles} from '@/composables/useCommonStyles'
import UploadButton from '@/components/UploadButton.vue'
import AssumptionsPanel from '@/components/AssumptionsPanel.vue'
import PageLayout from '@/components/shared/PageLayout.vue'
import CameraFrame from '@/components/shared/CameraFrame.vue'
import CameraOverlay from '@/components/shared/CameraOverlay.vue'
import CameraControls from '@/components/shared/CameraControls.vue'
import QrcodeVue from 'qrcode.vue'
import {useCookieService} from '@/services/cookieService'
import '@/assets/face-detection.css'

const {getCookie} = useCookieService()
const {formatField, getBarColorClass} = useCommonStyles()

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
  takeLatestPicture,

  // Helper functions
  uploadFile,
} = useWebcamService()

// Face detection
const {
  faceDetected,
  faceBounds,
  isModelLoading,
  isInitializing,
  loadModel
} = useFaceDetection(videoElement, isStreaming)

const formToken = ref('')
const capturedAt = ref<string | null>(null)
const copySuccess = ref(false)

function updateFormToken() {
  formToken.value = getCookie('form_token') || ''
}

const qrCodeUrl = computed(() => {
  if (!formToken.value) return ''
//      const baseUrl = window.location.origin
//      Should only be used on live
  return `parallax-darktech.nl/form?token=${formToken.value}`
})

watch(() => analysisData.value, (newData) => {
  if (newData) {
    updateFormToken()
  }
})

watch(latestImage, (val) => {
  if (val) {
    capturedAt.value = new Date().toLocaleString()
    copySuccess.value = false
  } else {
    capturedAt.value = null
  }
})

onMounted(async () => {
  updateFormToken()
  await loadModel()
  startCamera()
})
</script>

<template>
  <PageLayout container-class="px-4 sm:px-6 py-4 sm:py-8 mx-auto" style="--panel-w:28rem;">
    <div class="flex flex-col md:flex-row items-start justify-center gap-4 md:gap-0">
      <div
          :class="['left-column transition-transform duration-500 ease-in-out w-full md:w-auto']"
          :data-slide="latestImage ? 'true' : 'false'"
          :style="latestImage ? 'min-width:320px; width: 40vw; max-width:640px; flex-shrink: 0;' : 'min-width:320px; width: 80vw; max-width:1200px; flex-shrink: 0;'">
        <header v-if="!latestImage?.dataUrl" class="mb-3 sm:mb-4">
          <h1 class="bg-gradient-to-b from-white to-blue-300 bg-clip-text text-2xl sm:text-3xl font-extrabold tracking-tight text-transparent">
            Take a Selfie
          </h1>
          <p class="mt-1 sm:mt-2 text-sm sm:text-base text-blue-100/90">Position yourself in the frame and capture the
            perfect shot</p>
        </header>

        <CameraFrame>
          <video v-if="!latestImage?.dataUrl"
                 ref="videoElement"
                 :class="['absolute inset-0 w-full h-full object-cover z-0', isStreaming ? '' : 'opacity-50']"
                 autoplay playsinline></video>

          <div v-if="(isModelLoading || isInitializing) && isStreaming && !latestImage?.dataUrl"
               class="absolute inset-0 z-10 pointer-events-none flex items-center justify-center">
            <div class="face-detection-loading">
              <div class="loading-text">
                <span class="loading-dots">{{ isModelLoading ? 'Loading AI Model' : 'Preparing Detection' }}</span>
              </div>
            </div>
          </div>

          <div v-if="faceDetected && isStreaming && !isModelLoading && !isInitializing && !latestImage?.dataUrl"
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

          <img v-if="latestImage?.dataUrl"
               :src="latestImage.dataUrl"
               alt="Captured"
               class="absolute inset-0 w-full h-full object-contain z-0"/>

          <CameraOverlay v-if="!latestImage?.dataUrl && !isStreaming && !isLoading" message="Camera not active">
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

          <CameraOverlay v-if="!latestImage?.dataUrl && isLoading" message="Loading camera..." :show-spinner="true" />

          <CameraControls v-if="!latestImage?.dataUrl && isStreaming" :countdown="countdown" aria-label="Take selfie" @capture="takeLatestPicture" />
        </CameraFrame>

          <div v-if="latestImage?.dataUrl && qrCodeUrl && analysisData" class="mt-3 sm:mt-4 flex justify-center">
            <div class="rounded-xl sm:rounded-2xl p-3 sm:p-4 w-full max-w-md">
              <h3 class="text-xs sm:text-sm font-semibold mb-2 text-center text-white/90">Scan to continue on your
                phone</h3>
              <div class="flex items-center justify-center gap-3">
                <div class="flex justify-center bg-white p-2 sm:p-3 rounded-lg sm:rounded-xl">
                  <QrcodeVue :size="160" :value="qrCodeUrl" class="sm:hidden" level="H"/>
                  <QrcodeVue :size="200" :value="qrCodeUrl" class="hidden sm:block" level="H"/>
                </div>
              </div>
              <p class="text-blue-100/60 text-xs mt-2 sm:mt-3 text-center break-all">{{ qrCodeUrl }}</p>
            </div>
          </div>
        </div>

        <div :class="latestImage?.dataUrl ? 'show' : 'hidden'"
             class="right-column flex-1 flex flex-col justify-center items-center transition-all duration-500 ease-in-out ml-0 md:ml-6 w-full">
          <div v-if="latestImage" class="w-full relative">
            <div class="mt-4 sm:mt-6">
              <AssumptionsPanel
                  :analysisData="analysisData"
                  :analysisError="analysisError"
                  :formatField="formatField"
                  :getBarColorClass="getBarColorClass"
                  :isAnalyzing="isAnalyzing"
              />
            </div>

            <button
                class="w-full mt-3 sm:mt-4 px-4 py-3 bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 text-red-300 rounded-lg transition-colors min-h-[44px]"
                @click="clearAllData"
            >
              Delete Photo
            </button>
          </div>
        </div>
      </div>

    <canvas ref="canvasElement" class="hidden"></canvas>
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

.left-column[data-slide="true"] {
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

button[aria-label="Take selfie"] {
  box-shadow: 0 6px 18px rgba(59, 119, 242, 0.18);
}

button[aria-label="Take selfie"]:active {
  transform: translateY(1px) scale(0.99);
}

button[class*="bg-white/6"] {
  border: 1px solid rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(4px);
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
