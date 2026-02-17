<script lang="ts" setup>
import {ref, onMounted} from 'vue'
import {aiSettingsService, type AISettingData} from '../services/aiSettingsService'

const settings = ref<AISettingData[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const updating = ref<string | null>(null)

// Model options for each provider
const modelOptions: Record<string, string[]> = {
  openai: ['gpt-4o'],
  claude: ['claude-sonnet-4-5'],
  gemini: ['gemini-3-flash-preview', 'gemini-2.5-flash']
}

const providerDisplayNames: Record<string, string> = {
  openai: 'OpenAI',
  claude: 'Claude (Anthropic)',
  gemini: 'Gemini (Google)'
}

const loadSettings = async () => {
  try {
    loading.value = true
    error.value = null
    settings.value = await aiSettingsService.getAllSettings()
  } catch (e) {
    error.value = 'Failed to load AI settings'
    console.error('Load settings error:', e)
  } finally {
    loading.value = false
  }
}

const toggleProvider = async (provider: string, currentEnabled: boolean) => {
  try {
    updating.value = provider
    error.value = null
    
    const result = await aiSettingsService.updateSetting(provider, {
      enabled: !currentEnabled
    })
    
    // Update the local settings directly instead of reloading
    const settingIndex = settings.value.findIndex(s => s.provider === provider)
    if (settingIndex > -1) {
      settings.value[settingIndex] = result
    }
  } catch (e) {
    console.error('Toggle provider error:', e)
    error.value = `Failed to toggle ${provider}`
  } finally {
    updating.value = null
  }
}

const updateModel = async (provider: string, newModel: string) => {
  try {
    updating.value = provider
    error.value = null
    
    const result = await aiSettingsService.updateSetting(provider, {
      model_version: newModel
    })
    
    // Update the local settings directly instead of reloading
    const settingIndex = settings.value.findIndex(s => s.provider === provider)
    if (settingIndex > -1) {
      settings.value[settingIndex] = result
    }
  } catch (e) {
    console.error('Update model error:', e)
    error.value = `Failed to update model for ${provider}`
  } finally {
    updating.value = null
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-white mb-2">AI Provider Settings</h2>
      <p class="text-gray-400 text-sm">Manage AI providers and their models</p>
    </div>

    <div v-if="error" class="bg-red-500/20 border border-red-500/50 rounded-lg p-4 text-red-300">
      {{ error }}
    </div>

    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-400"></div>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
          v-for="setting in settings"
          :key="setting.provider"
          class="bg-white/5 border border-white/10 rounded-lg p-6 space-y-4 hover:bg-white/10 transition"
      >
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-white">
              {{ providerDisplayNames[setting.provider] || setting.provider }}
            </h3>
            <p class="text-xs text-gray-400 mt-1">
              Status: 
              <span :class="setting.enabled ? 'text-green-400' : 'text-red-400'">
                {{ setting.enabled ? 'Enabled' : 'Disabled' }}
              </span>
            </p>
          </div>
          
          <button
              :disabled="updating === setting.provider"
              :class="[
                'relative inline-flex h-8 w-14 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-900',
                setting.enabled ? 'bg-indigo-500' : 'bg-gray-600',
                updating === setting.provider && 'opacity-50 cursor-not-allowed'
              ]"
              @click="toggleProvider(setting.provider, setting.enabled)"
          >
            <span
                :class="[
                  'inline-block h-6 w-6 transform rounded-full bg-white transition-transform',
                  setting.enabled ? 'translate-x-7' : 'translate-x-1'
                ]"
            />
          </button>
        </div>

        <div v-if="setting.enabled" class="space-y-2">
          <label class="block text-sm font-medium text-gray-300">
            Model Version
          </label>
          <select
              v-model="setting.model_version"
              :disabled="updating === setting.provider"
              class="w-full px-3 py-2 bg-gray-800/50 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
              @change="updateModel(setting.provider, setting.model_version)"
          >
            <option
                v-for="model in modelOptions[setting.provider]"
                :key="model"
                :value="model"
            >
              {{ model }}
            </option>
          </select>
          <p class="text-xs text-gray-500 mt-1">
            Current: {{ setting.model_version }}
          </p>
        </div>

        <div v-if="updating === setting.provider" class="flex items-center justify-center py-2">
          <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-indigo-400"></div>
          <span class="ml-2 text-sm text-gray-400">Updating...</span>
        </div>
      </div>
    </div>

    <div class="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4 text-sm text-blue-300">
      <strong>Note:</strong> Disabling a provider will prevent users from selecting it for image analysis. 
      Model changes take effect immediately for all new requests.
    </div>
  </div>
</template>
