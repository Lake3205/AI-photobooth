const TOKEN_KEY = 'user_token'
const USERNAME_KEY = 'username'
const API_BASE_URL = 'http://localhost:8000'

export interface LoginCredentials {
  username: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export interface VerifyResponse {
  username: string
  role: string
  authenticated: boolean
}

export const authService = {
  async login(credentials: LoginCredentials): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Login failed')
      }

      const data: AuthResponse = await response.json()
      localStorage.setItem(TOKEN_KEY, data.access_token)
      
      await this.verifyToken()
      
      return true
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  },

  logout(): void {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USERNAME_KEY)
  },

  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY)
  },
  
  getUsername(): string | null {
    return localStorage.getItem(USERNAME_KEY)
  },

  isAuthenticated(): boolean {
    return this.getToken() !== null
  },

  async verifyToken(): Promise<boolean> {
    const token = this.getToken()
    if (!token) return false

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/verify`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })

      if (!response.ok) {
        this.logout()
        return false
      }

      const data: VerifyResponse = await response.json()
      localStorage.setItem(USERNAME_KEY, data.username)
      
      return data.authenticated
    } catch (error) {
      console.error('Token error:', error)
      this.logout()
      return false
    }
  },

  async authenticatedFetch(url: string, options: RequestInit = {}): Promise<Response> {
    const token = this.getToken()
    
    if (!token) {
      throw new Error('No token found')
    }

    const headers = {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
    }

    const response = await fetch(url, {
      ...options,
      headers,
    })

    if (response.status === 401) {
      this.logout()
      window.location.href = '/login'
      throw new Error('Authentication required')
    }

    if (response.status === 403) {
      // User is authenticated but doesn't have permission
      window.location.href = '/selfie'
      throw new Error('Insufficient permissions')
    }

    return response
  },
}
