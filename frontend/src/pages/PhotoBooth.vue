<script lang="ts" setup>
import {computed, onMounted, ref, watch} from 'vue'
import {useWebcamService} from '@/services/webcamService'
import {CameraIcon} from '@heroicons/vue/24/outline'
import UploadButton from '@/components/UploadButton.vue'
import AssumptionsPanel from '@/components/AssumptionsPanel.vue'
import {useRouter} from "vue-router";
import TermsButton from '@/components/TermsButton.vue'
import QrcodeVue from 'qrcode.vue'
import {useCookieService} from '@/services/cookieService'

const router = useRouter()
const { getCookie } = useCookieService()

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



// Terms of Service agreement state
const hasAgreedToTerms = ref(false)

// Check cookie for agreement
function checkTermsCookie() {
  return document.cookie.split(';').some((c) => c.trim().startsWith('agreedToTermsOfService=1'))
}

function setTermsCookie() {
  document.cookie = 'agreedToTermsOfService=1; path=/'
}

function agreeToTerms() {
  setTermsCookie()
  hasAgreedToTerms.value = true
}

const formToken = ref('')

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

onMounted(() => {
  hasAgreedToTerms.value = checkTermsCookie()
  updateFormToken()
  startCamera()
})
</script>

<template>
  <main class="relative overflow-hidden bg-black text-white min-h-screen">

    <!-- Terms of Service Popup -->
    <div v-if="!hasAgreedToTerms" class="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
      <div class="bg-neutral-900/85 rounded-xl shadow-xl p-8 max-w-md w-full text-center text-blue-100/90">
        <h2 class="text-2xl font-bold mb-4">Terms of Service</h2>
        <p class="mb-6">Please read and agree to our <span class="underline cursor-pointer" @click="router.push({name: 'terms-of-service'})">Terms of Service</span>
          before using the selfie camera.</p>
        <button class="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                @click="agreeToTerms">
          I Agree
        </button>
      </div>
    </div>

    <div class="pointer-events-none absolute inset-0 opacity-80">
      <div
          class="absolute -top-60 -left-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-br from-blue-500/60 to-blue-300/30 blur-3xl"></div>
      <div
          class="absolute -bottom-60 -right-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-tr from-blue-400/50 to-white/10 blur-3xl"></div>
      <div
          class="absolute inset-0 bg-[radial-gradient(circle_at_1px_1px,rgba(255,255,255,0.08)_1px,transparent_1px)] [background-size:24px_24px]"></div>
    </div>

    <div class="relative z-10 px-6 py-8 mx-auto" style="--panel-w:28rem;">
      <!-- Main row: left = title + live camera (always visible), right = result + assumptions (appears after capture) -->
      <div class="flex flex-col md:flex-row items-start justify-center">
        <!-- Left column: title + live camera -->
        <div
            :class="['left-column transition-transform duration-500 ease-in-out w-full md:w-auto', latestImage ? 'slide-left' : '']"
            :style="latestImage ? 'min-width:320px; width: 40vw; max-width:640px; flex-shrink: 0;' : 'min-width:320px; width: 80vw; max-width:1200px; flex-shrink: 0;'">
          <header class="mb-4">
            <h1 class="bg-gradient-to-b from-white to-blue-300 bg-clip-text text-3xl font-extrabold tracking-tight text-transparent">
              Take a Selfie
            </h1>
            <p class="mt-2 text-blue-100/90">Position yourself in the frame and capture the perfect shot</p>
          </header>

          <div class="relative rounded-3xl border border-white/15 bg-white/5 p-2 overflow-hidden">
            <div
                class="relative aspect-[16/9] w-full rounded-xl overflow-hidden bg-black/50 flex items-center justify-center">
              <video ref="videoElement"
                     :class="['absolute inset-0 w-full h-full object-cover z-0', isStreaming ? '' : 'opacity-50']"
                     autoplay playsinline></video>

              <div v-if="!isStreaming && !isLoading"
                   class="absolute inset-0 z-10 flex items-center justify-center bg-black/70 rounded-xl">
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

              <div v-if="isLoading" class="absolute inset-0 z-10 flex items-center justify-center bg-black/70">
                <div class="text-center">
                  <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-white mx-auto mb-4"></div>
                  <p class="text-white/70 text-lg">Loading camera...</p>
                </div>
              </div>

              <div v-if="isStreaming" class="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-20">
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

        <!-- Right column: small captured image + assumptions + QR -->
        <div :class="latestImage ? 'show' : 'hidden'"
             class="right-column flex-1 transition-all duration-500 ease-in-out ml-0 md:ml-6">
          <div v-if="latestImage" class="w-full">
            <div class="rounded-2xl bg-white/5 to-transparent p-2 mb-4 max-w-sm">
              <div class="relative w-full aspect-[16/9] rounded-md overflow-hidden">
                <img
                    :src="latestImage.dataUrl"
                    alt="Preview"
                    class="absolute inset-0 w-full h-full object-contain"
                />
              </div>
            </div>

            <!-- Assumptions and QR Code Side by Side -->
            <div class="flex flex-col lg:flex-row gap-4">
              <!-- Assumptions Panel -->
              <div class="flex-1">
                <AssumptionsPanel
                    :analysisData="analysisData"
                    :analysisError="analysisError"
                    :formatField="formatField"
                    :getBarColorClass="getBarColorClass"
                    :isAnalyzing="isAnalyzing"
                />
              </div>
              
              <!-- QR Code Panel -->
              <div v-if="qrCodeUrl && analysisData" class="lg:w-80 flex-shrink-0">
                <div class="rounded-2xl bg-white/5 p-4 h-full">
                  <h3 class="text-lg font-bold mb-3 bg-gradient-to-b from-white to-blue-300 bg-clip-text text-transparent">
                    Continue on Your Phone
                  </h3>
                    <p class="text-blue-100/80 text-sm font-medium mb-4 font-semibold">
                    Want to find out how the AI got these assumptions? Scan the code and find out!
                    </p>
                  <div class="flex justify-center bg-white p-4 rounded-xl">
                    <QrcodeVue :value="qrCodeUrl" :size="250" level="H" />
                  </div>
                  <p class="text-blue-100/60 text-xs mt-3 text-center break-all">
                    {{ qrCodeUrl }}
                  </p>
                </div>
              </div>
            </div>
            
            <button
                class="fixed bottom-2 right-2 w-8 h-8 bg-gray-500/20 hover:bg-gray-500/30 rounded-full opacity-10 hover:opacity-50 transition-opacity"
                @click="reload"
            ></button>
            
            <button
                class="w-full mt-4 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 text-red-300 rounded-lg transition-colors"
                @click="clearAllData"
            >
              Delete Photo
            </button>
          </div>
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
