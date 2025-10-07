<template>
  <div class="min-h-screen p-6">
    <div class="max-w-6xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-8 text-center">Webcam Test</h1>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Live video preview -->
        <div class="bg-white rounded-lg shadow-lg p-6">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Webcam</h2>
          <div class="relative mb-4">
            <video 
              ref="videoElement" 
              :class="[
                'w-full rounded-lg border-2',
                isStreaming ? 'border-green-400' : 'border-gray-300'
              ]"
              autoplay 
              playsinline
            ></video>
            <div v-if="!isStreaming" class="absolute inset-0 flex items-center justify-center bg-gray-200 rounded-lg">
              <span class="text-gray-500 text-lg">Camera not active</span>
            </div>
          </div>
          
          <div class="flex flex-wrap gap-3">
            <button 
              @click="startCamera" 
              :disabled="isStreaming || isLoading"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {{ isLoading ? 'Loading...' : 'Start Camera' }}
            </button>
            
            <button 
              @click="stopCamera" 
              :disabled="!isStreaming"
              class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              Stop Camera
            </button>
            
            <button 
              @click="takePicture" 
              :disabled="!isStreaming"
              class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              Foto maken
            </button>
          </div>
        </div>

        <!-- Captured images -->
        <div class="bg-white rounded-lg shadow-lg p-6">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Fotos</h2>
          <div v-if="capturedImages.length === 0" class="text-center py-12 text-gray-500">
            Geen foto's genomen
          </div>
          <div v-else class="space-y-4 max-h-96 overflow-y-auto">
            <div 
              v-for="(image, index) in capturedImages" 
              :key="index" 
              class="border rounded-lg p-3"
            >
              <img :src="image.dataUrl" :alt="`Picture ${index + 1}`" class="w-full h-32 object-cover rounded mb-2" />
              <div class="flex justify-between items-center">
                <p class="text-sm text-gray-600">{{ image.timestamp }}</p>
                <button 
                  @click="deleteImage(index)" 
                  class="px-2 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700 transition-colors"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Hidden canvas for image capture -->
      <canvas ref="canvasElement" class="hidden"></canvas>

      <!-- Error display -->
      <div v-if="error" class="mt-6 bg-red-50 border border-red-200 rounded-lg p-4">
        <h3 class="text-lg font-semibold text-red-800 mb-2">Error:</h3>
        <p class="text-red-600">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue'

// Template refs
const videoElement = ref<HTMLVideoElement | null>(null)
const canvasElement = ref<HTMLCanvasElement | null>(null)

// Reactive state
const isStreaming = ref(false)
const isLoading = ref(false)
const error = ref<string | null>(null)
const stream = ref<MediaStream | null>(null)

// Interface for captured images
interface CapturedImage {
  dataUrl: string
  timestamp: string
  blob: Blob
}

const capturedImages = ref<CapturedImage[]>([])

const startCamera = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error('error')
    }

    // Camara permissions
    const mediaStream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 1280 },
        height: { ideal: 720 },
        facingMode: 'user'
      },
      audio: false
    })

    if (videoElement.value) {
      videoElement.value.srcObject = mediaStream
      stream.value = mediaStream
      isStreaming.value = true
    }
  } catch (err) {
    console.error('Error', err)
    if (err instanceof Error) {
      error.value = err.message
    } else {
      error.value = 'error'
    }
  } finally {
    isLoading.value = false
  }
}

const stopCamera = () => {
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
    stream.value = null
  }
  
  if (videoElement.value) {
    videoElement.value.srcObject = null
  }

  isStreaming.value = false
  error.value = null
}

const takePicture = () => {
  if (!videoElement.value || !canvasElement.value || !isStreaming.value) {
    error.value = 'Camera not ready for capture'
    return
  }

  try {
    const video = videoElement.value
    const canvas = canvasElement.value
    const context = canvas.getContext('2d')

    if (!context) {
      throw new Error('Could not get canvas context')
    }

    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    context.drawImage(video, 0, 0, canvas.width, canvas.height)

    canvas.toBlob((blob) => {
      if (blob) {
        const dataUrl = canvas.toDataURL('image/jpeg', 0.9)
        const timestamp = new Date().toLocaleString()
        
        const capturedImage: CapturedImage = {
          dataUrl,
          timestamp,
          blob
        }
        
        capturedImages.value.push(capturedImage)
        
        error.value = null
      } else {
        error.value = 'Failed to create image blob'
      }
    }, 'image/jpeg', 0.9)

  } catch (err) {
    console.error('Error taking picture:', err)
    if (err instanceof Error) {
      error.value = `Failed to take picture: ${err.message}`
    } else {
      error.value = 'Failed to take picture: Unknown error'
    }
  }
}

// const downloadImage = (image: CapturedImage, index: number) => {
//   try {
//     const link = document.createElement('a')
//     link.href = image.dataUrl
//     link.download = `webcam-capture-${index + 1}-${Date.now()}.jpg`
//     document.body.appendChild(link)
//     link.click()
//     document.body.removeChild(link)
//   } catch (err) {
//     console.error('Error downloading image:', err)
//     error.value = 'Failed to download image'
//   }
// }

const deleteImage = (index: number) => {
  if (index >= 0 && index < capturedImages.value.length) {
    capturedImages.value.splice(index, 1)
  }
}

onUnmounted(() => {
  stopCamera()
})

</script>

