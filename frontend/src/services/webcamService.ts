import type { AssumptionData, AssumptionType } from '@/types/AssumptionType';
import { ref, onUnmounted, computed, watch } from 'vue'

interface CapturedImage {
  dataUrl: string
  timestamp: string
  blob: Blob
}

interface AnalysisResponse {
  [filename: string]: AssumptionData;
}

class AssumptionsService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  }

  async generateAssumptions(imageBlob: Blob, filename: string = 'selfie.jpg'): Promise<AssumptionData> {
    try {
      const formData = new FormData();
      formData.append('image', imageBlob, filename);

      const response = await fetch(`${this.baseUrl}/assumptions/generate`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: AnalysisResponse = await response.json();
      
      const assumptions = data[filename];
      if (!assumptions) {
        return null as unknown as AssumptionData;
      }
      
      return assumptions;
    } catch (error) {
      console.error('Error generating assumptions:', error);
      throw new Error('Failed to generate assumptions');
    }
  }
}

const assumptionsService = new AssumptionsService();

export const useWebcamService = () => {
  // Template
  const videoElement = ref<HTMLVideoElement | null>(null)
  const canvasElement = ref<HTMLCanvasElement | null>(null)

  // Webcam
  const isStreaming = ref(false)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const stream = ref<MediaStream | null>(null)
  const capturedImages = ref<CapturedImage[]>([])

  // Analysis
  const analysisData = ref<AssumptionData | null>(null)
  const isAnalyzing = ref(false)
  const analysisError = ref<string | null>(null)

  // UI
  const isNavbarOpen = ref(false)
  const countdown = ref(0)
  let countdownInterval: number | null = null

  // Computed properties
  const latestImage = computed(() => {
    return capturedImages.value[capturedImages.value.length - 1]
  })

  watch(() => capturedImages.value.length, (newLength) => {
    if (newLength > 0) {
      isNavbarOpen.value = true
    }
  })

  watch(() => capturedImages.value.length, (newLength, oldLength) => {
    if (newLength > oldLength && capturedImages.value.length > 0) {
      const latestImage = capturedImages.value[capturedImages.value.length - 1]
      if (latestImage) {
        analyzeImage(latestImage.blob)
      }
    }
  })

  const analyzeImage = async (imageBlob: Blob) => {
    try {
      isAnalyzing.value = true
      analysisError.value = null
      
      const assumptions = await assumptionsService.generateAssumptions(imageBlob)
      analysisData.value = assumptions
    } catch (error) {
      console.error('Analysis error:', error)
      analysisError.value = error instanceof Error ? error.message : 'Analysis failed'
    } finally {
      isAnalyzing.value = false
    }
  }

  const takeLatestPicture = () => {
    if (countdown.value > 0) return
    countdown.value = 3
    capturedImages.value.length = 0
    analysisData.value = null
    analysisError.value = null
    
    countdownInterval = window.setInterval(() => {
      if (countdown.value > 1) {
        countdown.value--
      } else {
        countdown.value = 0
        if (countdownInterval) {
          clearInterval(countdownInterval)
          countdownInterval = null
        }
        takePicture()
      }
    }, 1000)
  }

  const closeNavbar = () => {
    isNavbarOpen.value = false
  }

  const formatField = (field: AssumptionType): string => {
    if (field.format === 'PERCENTAGE' && typeof field.value === 'number') {
      return `${field.value.toFixed(1)}%`
    } else if (field.format === 'CURRENCY' && typeof field.value === 'number') {
      return `€${field.value.toLocaleString()}`
    } else if (field.format === 'NUMBER' && typeof field.value === 'number') {
      return field.value.toString()
    } else if (field.format === 'WEIGHT' && typeof field.value === 'number') {
      return `${field.value.toFixed(1)} kg`
    } else if (field.format === 'YEARS' && typeof field.value === 'number') {
      return `${field.value} years`
    } else if (field.format === 'HOURS_DAY' && typeof field.value === 'number') {
      return `${field.value} hours per day`
    } 
    return String(field.value)
  }


  const getStringHash = (str: string): number => {
    let hash = 0
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash + str.charCodeAt(i)) & 0xffffffff
    }
    return Math.abs(hash)
  }

  const getConsistentPercentage = (field: AssumptionType): number => {
    // If the field has a defined range, calculate percentage within that range
    if (field.format === 'PERCENTAGE' && typeof field.value === 'number') {
      return Math.min(Math.max(field.value, 0), 100)
    }

    if (field.min !== undefined && field.max !== undefined && typeof field.value === 'number') {
      if (field.max === field.min) return 100

      // If ideal is defined, adjust calculation to reflect distance from ideal
      if (field.ideal !== undefined) {
        if (field.ideal === field.min) {
          if (field.value <= field.min) return 100
          if (field.value >= field.max) return 0
          return ((field.max - field.value) / (field.max - field.min)) * 100;
        }
      }

      const clampedValue = Math.min(Math.max(field.value, field.min), field.max)
      return ((clampedValue - field.min) / (field.max - field.min)) * 100
    }

    // Fallback: use hash-based percentage for consistent but arbitrary value
    return getStringHash(field.name) % 80 + 20 // Range from 20-100%
  }

  const getBarColorClass = (key: string): string => {
    const colorClasses = [
      'bg-gradient-to-r from-blue-500 to-blue-300',
      'bg-gradient-to-r from-green-500 to-emerald-300',
      'bg-gradient-to-r from-yellow-500 to-orange-300',
      'bg-gradient-to-r from-yellow-500 to-orange-300',
      'bg-gradient-to-r from-purple-500 to-pink-300',
      'bg-gradient-to-r from-rose-500 to-red-300',
      'bg-gradient-to-r from-indigo-500 to-purple-300',
      'bg-gradient-to-r from-cyan-500 to-blue-300',
      'bg-gradient-to-r from-emerald-500 to-green-300',
      'bg-gradient-to-r from-amber-500 to-yellow-300'
    ];

    const index = Math.abs(getStringHash(key)) % colorClasses.length; // Ensure index is always valid
    return colorClasses[index] as string;
  };

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

  // Clear all images and analysis data
  const clearAllData = () => {
    capturedImages.value.length = 0
    analysisData.value = null
    analysisError.value = null
    closeNavbar()
  }

  // Upload file from upload button
  function uploadFile(e: Event) {
    const files = (e.target as HTMLInputElement).files
    const file = files && files.length > 0 ? files[0] : undefined
    if (!file || !file.type.startsWith('image/')) return

    const blob: Blob = file;

    capturedImages.value.push({ 
      dataUrl: URL.createObjectURL(blob),
      timestamp: new Date().toLocaleString(),
      blob: blob
    });
  }

  // Cleanup on unmount
  onUnmounted(() => {
    stopCamera()
  })

  return {
    // Template
    videoElement,
    canvasElement,
    
    // Webcam
    isStreaming,
    isLoading,
    error,
    capturedImages,
    
    // Analysis
    analysisData,
    isAnalyzing,
    analysisError,
    
    // UI
    isNavbarOpen,
    countdown,
    latestImage,
    
    // Webcam
    startCamera,
    stopCamera,
    takePicture,
    takeLatestPicture,
    deleteImage,
    
    // Analysis
    analyzeImage,
    
    // UI
    closeNavbar,
    clearAllData,
    
    // Helper
    formatField,
    getStringHash,
    getConsistentPercentage,
    getBarColorClass,
    uploadFile
  }
}
