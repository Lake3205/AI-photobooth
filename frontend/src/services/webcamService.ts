import { ref, onUnmounted } from 'vue'

// Interface for captured images
interface CapturedImage {
  dataUrl: string
  timestamp: string
  blob: Blob
}

export const useWebcamService = () => {
  // Template refs
  const videoElement = ref<HTMLVideoElement | null>(null)
  const canvasElement = ref<HTMLCanvasElement | null>(null)

  // Reactive state
  const isStreaming = ref(false)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const stream = ref<MediaStream | null>(null)
  const capturedImages = ref<CapturedImage[]>([])

  const startCamera = async () => {
    try {
      isLoading.value = true
      error.value = null
      
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Camera not supported in this browser')
      }

      // Request camera permissions
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
      console.error('Error accessing camera:', err)
      if (err instanceof Error) {
        error.value = err.message
      } else {
        error.value = 'Failed to access camera'
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

  const deleteImage = (index: number) => {
    if (index >= 0 && index < capturedImages.value.length) {
      capturedImages.value.splice(index, 1)
    }
  }

  // Cleanup on unmount
  onUnmounted(() => {
    stopCamera()
  })

  return {
    videoElement,
    canvasElement,
    isStreaming,
    isLoading,
    error,
    capturedImages,
    startCamera,
    stopCamera,
    takePicture,
    deleteImage
  }
}
