// Shared utility functions and common styles
export const useCommonStyles = () => {
  // CSS class utilities
  const cardClasses = 'rounded-2xl bg-gradient-to-br from-white/5 to-white/2 border border-white/10 backdrop-blur-sm'
  
  const buttonPrimaryClasses = 'px-6 sm:px-8 py-3.5 sm:py-4 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-semibold rounded-xl transition-all transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-black shadow-lg min-h-[44px]'
  
  const buttonSecondaryClasses = 'px-4 py-3 bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 text-red-300 rounded-lg transition-colors min-h-[44px]'
  
  const inputClasses = 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition text-base'
  
  const headerGradientClasses = 'bg-gradient-to-r from-indigo-200 via-fuchsia-200 to-pink-300 text-transparent bg-clip-text'

  // Format utilities
  const formatField = (field: { format: string; value: string | number; name: string }): string => {
    if (field.format === 'percentage' && typeof field.value === 'number') {
      return `${field.value.toFixed(1)}%`
    } else if (field.format === 'currency' && typeof field.value === 'number') {
      return `€${field.value.toLocaleString()}`
    } else if (field.format === 'number' && typeof field.value === 'number') {
      return field.value.toString()
    } else if (field.format === 'weight' && typeof field.value === 'number') {
      return `${field.value.toFixed(1)} kg`
    } else if (field.format === 'years' && typeof field.value === 'number') {
      return `${field.value} years`
    } else if (field.format === 'hoursDay' && typeof field.value === 'number') {
      return `${field.value} hours per day`
    }
    return String(field.value)
  }

  // Color utilities
  const getStringHash = (str: string): number => {
    let hash = 0
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash + str.charCodeAt(i)) & 0xffffffff
    }
    return Math.abs(hash)
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
    ]

    const index = Math.abs(getStringHash(key)) % colorClasses.length
    return colorClasses[index] as string
  }

  return {
    // Classes
    cardClasses,
    buttonPrimaryClasses,
    buttonSecondaryClasses,
    inputClasses,
    headerGradientClasses,
    
    // Utilities
    formatField,
    getStringHash,
    getBarColorClass,
  }
}
