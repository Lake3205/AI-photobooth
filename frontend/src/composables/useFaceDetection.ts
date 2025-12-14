import {onUnmounted, ref, type Ref, watch} from 'vue'
import * as blazeface from '@tensorflow-models/blazeface'
import '@tensorflow/tfjs'

export interface FaceBounds {
    x: number
    y: number
    width: number
    height: number
    index: number
}

export function useFaceDetection(
    videoElement: Ref<HTMLVideoElement | null>,
    isStreaming: Ref<boolean>
) {
    // Face detection state
    const faceDetected = ref(false)
    const faceBounds = ref<FaceBounds[]>([])
    const isModelLoading = ref(false)

    let faceDetectionInterval: number | null = null
    let model: blazeface.BlazeFaceModel | null = null

    // Load BlazeFace model
    const loadModel = async () => {
        if (model) return
        try {
            isModelLoading.value = true
            console.log('Loading BlazeFace model...')
            model = await blazeface.load()
            console.log('BlazeFace model loaded successfully')
        } catch (error) {
            console.error('Error loading BlazeFace model:', error)
        } finally {
            isModelLoading.value = false
        }
    }

    // Face detection using TensorFlow BlazeFace
    const detectFace = async () => {
        if (!videoElement.value || !isStreaming.value || !model) return

        try {
            const video = videoElement.value

            // Make sure video is ready
            if (video.readyState !== video.HAVE_ENOUGH_DATA) return

            // Detect faces
            const predictions = await model.estimateFaces(video, false)

            if (predictions && predictions.length > 0) {
                // Get video element dimensions (display size)
                const videoBounds = video.getBoundingClientRect()

                // Calculate scale factors (video element size vs actual video size)
                const scaleX = videoBounds.width / video.videoWidth
                const scaleY = videoBounds.height / video.videoHeight

                // Process all detected faces
                const detectedFaces: FaceBounds[] = []

                predictions.forEach((face, index) => {
                    if (face && face.topLeft && face.bottomRight) {
                        const topLeft = face.topLeft as number[]
                        const bottomRight = face.bottomRight as number[]

                        if (topLeft.length >= 2 && bottomRight.length >= 2) {
                            const startX = topLeft[0] as number
                            const startY = topLeft[1] as number
                            const endX = bottomRight[0] as number
                            const endY = bottomRight[1] as number

                            // Calculate face bounding box in display coordinates
                            const faceWidth = endX - startX
                            const faceHeight = endY - startY

                            detectedFaces.push({
                                x: startX * scaleX,
                                y: startY * scaleY,
                                width: faceWidth * scaleX,
                                height: faceHeight * scaleY,
                                index: index
                            })
                        }
                    }
                })

                if (detectedFaces.length > 0) {
                    faceBounds.value = detectedFaces
                    faceDetected.value = true
                } else {
                    faceBounds.value = []
                    faceDetected.value = false
                }
            } else {
                faceBounds.value = []
                faceDetected.value = false
            }
        } catch (error) {
            console.error('Face detection error:', error)
            faceDetected.value = false
            faceBounds.value = []
        }
    }

    // Start/stop face detection based on streaming state
    watch(isStreaming, async (streaming) => {
        if (streaming) {
            // Load model if not loaded
            if (!model && !isModelLoading.value) {
                await loadModel()
            }

            // Start detection interval
            if (model) {
                faceDetectionInterval = window.setInterval(detectFace, 100) // 10 FPS for smooth tracking
            }
        } else {
            if (faceDetectionInterval) {
                clearInterval(faceDetectionInterval)
                faceDetectionInterval = null
            }
            faceDetected.value = false
            faceBounds.value = []
        }
    })

    // Cleanup on unmount
    onUnmounted(() => {
        if (faceDetectionInterval) {
            clearInterval(faceDetectionInterval)
        }
    })

    return {
        faceDetected,
        faceBounds,
        isModelLoading,
        loadModel
    }
}

