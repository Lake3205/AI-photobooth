import { authService } from './authService'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export interface AISettingData {
  provider: string
  enabled: boolean
  model_version: string
}

export interface AISettingUpdate {
  enabled?: boolean
  model_version?: string
}

class AISettingsService {
  async getAllSettings(): Promise<AISettingData[]> {
    try {
      const response = await authService.authenticatedFetch(`${API_BASE_URL}/api/ai-settings/`)

      if (!response.ok) {
        throw new Error('Failed to fetch AI settings')
      }

      return await response.json()
    } catch (error) {
      console.error('Error fetching AI settings:', error)
      throw error
    }
  }

  async getSetting(provider: string): Promise<AISettingData> {
    try {
      const response = await authService.authenticatedFetch(`${API_BASE_URL}/api/ai-settings/${provider}`)

      if (!response.ok) {
        throw new Error(`Failed to fetch setting for ${provider}`)
      }

      return await response.json()
    } catch (error) {
      console.error(`Error fetching setting for ${provider}:`, error)
      throw error
    }
  }

  async updateSetting(provider: string, update: AISettingUpdate): Promise<AISettingData> {
    const response = await authService.authenticatedFetch(`${API_BASE_URL}/api/ai-settings/${provider}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(update)
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error(`Update failed with status ${response.status}:`, errorText)
      throw new Error(`Failed to update setting for ${provider}`)
    }

    return await response.json()
  }

  async getEnabledProviders(): Promise<string[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/ai-settings/providers/enabled`)

      if (!response.ok) {
        throw new Error('Failed to fetch enabled providers')
      }

      return await response.json()
    } catch (error) {
      console.error('Error fetching enabled providers:', error)
      throw error
    }
  }
}

export const aiSettingsService = new AISettingsService()
