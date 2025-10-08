import {reactive, readonly} from 'vue'

type UploadedImage = {
    file: File
    url: string
}

type State = {
    image: UploadedImage | null
}

const state = reactive<State>({
    image: null,
})

export function useUploadStore() {
    function setImage(file: File) {
        if (!file || !file.type.startsWith('image/')) return
        if (state.image?.url) URL.revokeObjectURL(state.image.url)
        const url = URL.createObjectURL(file)
        state.image = {file, url}
    }

    function clearImage() {
        if (state.image?.url) URL.revokeObjectURL(state.image.url)
        state.image = null
    }

    return {
        state: readonly(state),
        setImage,
        clearImage,
    }
}
