<script lang="ts" setup>
import {useRouter} from "vue-router";

const router = useRouter()

</script>

<template>
  <main class="relative overflow-hidden bg-black text-white">
    <div class="pointer-events-none absolute inset-0 opacity-80">
      <div
          class="absolute -top-60 -left-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-br from-blue-500/60 to-blue-300/30 blur-3xl"></div>
      <div
          class="absolute -bottom-60 -right-60 h-[36rem] w-[36rem] rounded-full bg-gradient-to-tr from-blue-400/50 to-white/10 blur-3xl"></div>
      <div
          class="absolute inset-0 bg-[radial-gradient(circle_at_1px_1px,rgba(255,255,255,0.08)_1px,transparent_1px)] [background-size:24px_24px]"></div>
    </div>
    <section
        class="relative z-10 my-10 mx-auto flex min-h-screen max-w-3xl flex-col items-center justify-center px-6 text-center">
      <h1 class="select-none bg-gradient-to-b from-white to-blue-300 bg-clip-text text-5xl font-extrabold tracking-tight text-transparent mb-6">
        Terms of Service</h1>
      <div class="bg-white/10 rounded-2xl shadow-lg p-8 w-full text-left text-base text-blue-100/90">
        <p class="mb-4">Welcome to our application. By using our service, you agree to the following terms and
          conditions. Please read them carefully.</p>
        <ol class="list-decimal list-inside space-y-2 mb-4">
          <li>
            <strong>Use of Webcam:</strong> This application requires access to your device’s webcam to capture an
            image. By using this feature, you consent to the collection and processing of the captured image.
          </li>

          <li>
            <strong>Image Processing:</strong> The captured image will be securely transmitted to AI services for
            analysis and generating assumptions. These AI services may include third-party providers such as OpenAI,
            Google Gemini, and Anthropic Claude.
          </li>

          <li>
            <strong>Third-Party AI Terms:</strong> By using this service, you also agree to the terms and policies of
            the AI providers we use. Please review their respective Terms of Service:
            <ul>
              <li><a class="underline" href="https://openai.com/policies/terms-of-use" target="_blank">OpenAI Terms of
                Use</a></li>
              <li><a class="underline" href="https://policies.google.com/terms" target="_blank">Google Terms of
                Service</a></li>
              <li><a class="underline" href="https://ai.google.dev/gemini-api/terms" target="_blank">Gemini API Terms of
                Service</a></li>
              <li><a class="underline" href="https://www.anthropic.com/legal/consumer-terms" target="_blank">Anthropic
                (Claude) Terms of
                Service</a></li>
            </ul>
          </li>

          <li>
            <strong>Data Usage:</strong> The AI-generated assumptions derived from your image will be anonymized and
            stored in our database for analytical and product improvement purposes. No personally identifiable
            information will be retained alongside the assumptions.
          </li>

          <li>
            <strong>Data Ownership:</strong> You retain ownership of your original image. However, by using the service,
            you grant us a limited, non-exclusive license to process and temporarily store the image for the purpose of
            generating and saving AI-based assumptions.
          </li>

          <li>
            <strong>Model Training:</strong> The third-party AI providers may use submitted data (including your image)
            to improve their models, in accordance with their own data usage and privacy policies.
          </li>

          <li>
            <strong>Prohibited Use:</strong> You agree not to use the application to upload or process unlawful,
            harmful, or inappropriate content. Any misuse may result in termination of access.
          </li>

          <li>
            <strong>Disclaimer:</strong> The AI-generated assumptions are provided for informational or entertainment
            purposes only and should not be treated as factual, diagnostic, or professional advice.
          </li>

          <li>
            <strong>Limitation of Liability:</strong> We are not responsible for any damages or losses arising from the
            use or inability to use this application or reliance on AI-generated outputs.
          </li>

          <li>
            <strong>Changes to Terms:</strong> We may update these Terms of Service at any time. Continued use of the
            application after updates constitutes acceptance of the revised terms.
          </li>
        </ol>
        <p>If you have any questions about these terms, please contact us.</p>
        <div class="mt-8 text-center">
          <button
              class="text-blue-300 hover:text-white transition-colors"
              @click="router.push({name: 'selfie'})"
          >
            ← Back to start
          </button>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
</style>