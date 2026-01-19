<script lang="ts" setup>
import {onMounted, ref} from 'vue'
import {useRouter} from 'vue-router'

const router = useRouter()
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

onMounted(() => {
  hasAgreedToTerms.value = checkTermsCookie()
})

defineExpose({
  hasAgreedToTerms
})
</script>

<template>
  <div v-if="!hasAgreedToTerms" class="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
    <div class="bg-neutral-900/85 rounded-xl shadow-xl p-8 max-w-md w-full text-center text-blue-100/90">
      <h2 class="text-2xl font-bold mb-4">Terms of Service</h2>
      <p class="mb-6">
        Please read and agree to our
        <span class="underline cursor-pointer" @click="router.push({name: 'terms-of-service'})">Terms of Service</span>
        before using the selfie camera.
      </p>
      <button
          class="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          @click="agreeToTerms"
      >
        I Agree
      </button>
    </div>
  </div>
</template>

<style scoped>

</style>