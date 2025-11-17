import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'node:url'
import dotenv from 'dotenv'
import path from 'path'

// Load environment from project root (one level up)
const projectRoot = path.resolve(__dirname, '..')
const envFile = process.env.NODE_ENV === 'production' 
  ? path.join(projectRoot, '.env') 
  : path.join(projectRoot, '.env.development')

dotenv.config({ path: envFile })

// Fallback to root .env if .env.development doesn't exist
if (process.env.NODE_ENV !== 'production') {
  dotenv.config({ path: path.join(projectRoot, '.env') })
}

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    }
  },
  server: {
    port: 3000
  }
})
