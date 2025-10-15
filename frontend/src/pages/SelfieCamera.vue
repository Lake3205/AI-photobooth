<script lang="ts" setup>
import {onMounted} from 'vue'
import {useWebcamService} from '@/services/webcamService'
import {CameraIcon, XMarkIcon} from '@heroicons/vue/24/outline'
import {useRouter} from 'vue-router'
import UploadButton from '@/components/UploadButton.vue'

const router = useRouter()

const {
  // Template refs
  videoElement,
  canvasElement,

  // Webcam state
  isStreaming,
  isLoading,
  error,
  capturedImages,

  // Analysis state
  analysisData,
  isAnalyzing,
  analysisError,

  // UI state
  isNavbarOpen,
  countdown,
  latestImage,

  // Webcam functions
  startCamera,
  stopCamera,
  takeLatestPicture,

  // UI functions
  closeNavbar,
  clearAllData,

  // Helper functions
  uploadFile,
  getBarColorClass,
  getConsistentPercentage,
  formatField
} = useWebcamService()

const goBack = () => {
  stopCamera()
  router.push({name: 'landing'})
}

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

    <div :class="latestImage && isNavbarOpen ? 'mr-80' : ''"
         class="relative z-10 flex min-h-screen transition-all duration-300 ease-in-out">
      <div class="flex-1 flex flex-col items-center justify-center p-8">
        <div class="w-full max-w-5xl">
          <header class="mb-6 text-center">
            <h1 class="bg-gradient-to-b from-white to-blue-300 bg-clip-text text-4xl font-extrabold tracking-tight text-transparent sm:text-5xl">
              Take a Selfie
            </h1>
            <p class="mt-3 text-blue-100/90">Position yourself in the frame and capture the perfect shot</p>
          </header>

          <div class="relative group">
            <div class="relative rounded-3xl border border-white/15 bg-white/5 p-2 overflow-hidden">
              <div class="rounded-2xl bg-gradient-to-b from-white/5 to-transparent p-6">
                <div
                    class="relative aspect-[16/9] w-full h-[60vh] max-h-[700px] rounded-xl overflow-hidden bg-black/50 flex items-center justify-center">
                  <video
                      ref="videoElement"
                      :class="[
                      'w-full h-full object-cover',
                      isStreaming ? '' : 'opacity-50'
                    ]"
                      autoplay
                      playsinline
                  ></video>

                  <div v-if="!isStreaming && !isLoading"
                       class="absolute inset-0 flex items-center justify-center bg-black/70">
                    <div class="text-center">
                      <CameraIcon class="h-20 w-20 text-white/50 mx-auto mb-4"/>
                      <p class="text-white/70 text-lg">Camera not active</p>
                      <div class="mt-6 flex flex-col gap-3">
                        <button
                            class="px-8 py-4 cursor-pointer bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium text-lg transition-colors"
                            @click="startCamera"
                        >
                          Start Camera
                        </button>
                        <UploadButton
                            :label="'Choose file instead'"
                            :onChange="uploadFile"
                            accept="image/*"
                            class="px-6 py-3 text-base"
                        />
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
                    <button
                        :disabled="countdown > 0"
                        class="group relative p-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full transition-all duration-200 hover:scale-110"
                        @click="takeLatestPicture"
                    >
                      <div
                          class="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500/20 to-blue-300/20 group-hover:from-blue-500/30 group-hover:to-blue-300/30 transition-all"></div>
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

          <div v-if="error" class="mt-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg backdrop-blur-sm">
            <p class="text-red-300">{{ error }}</p>
          </div>

          <div class="mt-8 text-center">
            <button
                class="text-blue-300 hover:text-white transition-colors"
                @click="goBack"
            >
              ← Back to start
            </button>
          </div>
        </div>
      </div>

      <div
          :class="[
          'fixed top-0 right-0 h-full w-[30rem] bg-black/90 backdrop-blur-xl border-l border-white/10 transform transition-transform duration-300 ease-in-out z-50',
          (latestImage && isNavbarOpen) ? 'translate-x-0' : 'translate-x-full'
        ]"
      >
        <div class="p-6 !pr-0 h-full flex flex-col *:pr-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-semibold text-white">Picture Info</h2>
            <button
                class="p-2 hover:bg-white/10 rounded-lg transition-colors"
                @click="closeNavbar"
            >
              <XMarkIcon class="h-6 w-6 text-white"/>
            </button>
          </div>

          <div class="flex-1 overflow-y-auto">
            <div v-if="latestImage" class="space-y-6">
              <div>
                <h3 class="text-lg font-medium text-white mb-3">Latest Capture</h3>
                <div class="rounded-lg overflow-hidden border border-white/10">
                  <img
                      :src="latestImage.dataUrl"
                      alt="Latest capture"
                      class="w-full h-48 object-cover"
                  />
                </div>
              </div>

              <div>
                <h3 class="text-lg font-medium text-white mb-3">Analysis</h3>

                <div v-if="isAnalyzing" class="text-center py-8">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-4"></div>
                  <p class="text-white/70">Analyzing image...</p>
                </div>

                <div v-else-if="analysisError"
                     class="p-4 bg-red-500/10 border border-red-500/20 rounded-lg backdrop-blur-sm">
                  <p class="text-red-300 text-sm">{{ analysisError }}</p>
                </div>

                <div v-else-if="analysisData" class="space-y-3">
                  <div v-for="field in analysisData" :key="field.name">
                    <div class="flex justify-between text-sm mb-1">
                      <span class="text-blue-200/70">{{ field.name }}</span>
                      <span class="text-white text-xs">{{ formatField(field) }}</span>
                    </div>
                    <div class="w-full bg-white/10 rounded-full h-2">
                      <div
                          :class="getBarColorClass(field.name)"
                          :style="`width: ${getConsistentPercentage(field)}%`"
                          class="h-2 rounded-full transition-all duration-1000"
                      ></div>
                    </div>
                  </div>
                </div>

                <div v-else class="space-y-3">
                  <div>
                    <div class="flex justify-between text-sm mb-1">
                      <span class="text-blue-200/70">Quality Score</span>
                      <span class="text-white">--</span>
                    </div>
                    <div class="w-full bg-white/10 rounded-full h-2">
                      <div class="bg-gradient-to-r from-blue-500 to-blue-300 h-2 rounded-full" style="width: 0%"></div>
                    </div>
                  </div>

                  <div>
                    <div class="flex justify-between text-sm mb-1">
                      <span class="text-blue-200/70">Lighting</span>
                      <span class="text-white">--</span>
                    </div>
                    <div class="w-full bg-white/10 rounded-full h-2">
                      <div class="bg-gradient-to-r from-yellow-500 to-orange-300 h-2 rounded-full"
                           style="width: 0%"></div>
                    </div>
                  </div>

                  <div>
                    <div class="flex justify-between text-sm mb-1">
                      <span class="text-blue-200/70">Clarity</span>
                      <span class="text-white">--</span>
                    </div>
                    <div class="w-full bg-white/10 rounded-full h-2">
                      <div class="bg-gradient-to-r from-green-500 to-emerald-300 h-2 rounded-full"
                           style="width: 0%"></div>
                    </div>
                  </div>

                  <div>
                    <div class="flex justify-between text-sm mb-1">
                      <span class="text-blue-200/70">Composition</span>
                      <span class="text-white">--</span>
                    </div>
                    <div class="w-full bg-white/10 rounded-full h-2">
                      <div class="bg-gradient-to-r from-purple-500 to-pink-300 h-2 rounded-full"
                           style="width: 0%"></div>
                    </div>
                  </div>

                  <div>
                    <div class="flex justify-between text-sm mb-1">
                      <span class="text-blue-200/70">Expression</span>
                      <span class="text-white">--</span>
                    </div>
                    <div class="w-full bg-white/10 rounded-full h-2">
                      <div class="bg-gradient-to-r from-rose-500 to-red-300 h-2 rounded-full" style="width: 0%"></div>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <h3 class="text-lg font-medium text-white mb-3">Actions</h3>
                <div class="space-y-2">
                  <button
                      class="w-full px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 text-red-300 rounded-lg transition-colors"
                      @click="clearAllData"
                  >
                    Delete Photo
                  </button>
                  <!--                  <button-->
                  <!--                      class="w-full px-4 py-2 bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/30 text-blue-300 rounded-lg transition-colors"-->
                  <!--                  >-->
                  <!--                    Continue with Photo-->
                  <!--                  </button>-->
                </div>
              </div>
            </div>

            <div v-if="capturedImages.length === 0" class="text-center py-12">
              <CameraIcon class="h-16 w-16 text-white/30 mx-auto mb-4"/>
              <p class="text-white/50">No photos captured yet</p>
              <p class="text-white/30 text-sm mt-2">Take a selfie to see it here</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <canvas ref="canvasElement" class="hidden"></canvas>
  </main>
</template>

<style scoped>
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(254, 255, 255, 0.3);
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>