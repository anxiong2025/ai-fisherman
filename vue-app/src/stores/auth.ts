import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'

const API_BASE = '/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const loading = ref(false)

  // Computed
  const isLoggedIn = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  // Initialize from localStorage
  async function init() {
    const savedToken = localStorage.getItem('auth_token')
    const savedUser = localStorage.getItem('auth_user')

    if (savedToken && savedUser) {
      token.value = savedToken
      user.value = JSON.parse(savedUser)

      // Verify token with backend
      try {
        const response = await fetch(`${API_BASE}/auth/verify`, {
          headers: {
            'Authorization': `Bearer ${savedToken}`
          }
        })

        if (!response.ok) {
          // Token invalid, clear auth
          logout()
        }
      } catch {
        // API not available in dev mode, keep local state
        console.log('Auth API not available, using local state')
      }
    }

    // Check for OAuth callback
    handleOAuthCallback()
  }

  // Handle OAuth callback (token and user in URL params)
  function handleOAuthCallback() {
    const params = new URLSearchParams(window.location.search)
    const urlToken = params.get('token')
    const urlUser = params.get('user')

    if (urlToken && urlUser) {
      try {
        token.value = urlToken
        user.value = JSON.parse(decodeURIComponent(urlUser))

        // Save to localStorage
        localStorage.setItem('auth_token', urlToken)
        localStorage.setItem('auth_user', JSON.stringify(user.value))

        // Clean URL
        window.history.replaceState({}, '', window.location.pathname)
      } catch (e) {
        console.error('Failed to parse OAuth callback:', e)
      }
    }
  }

  // Login with GitHub
  function loginWithGithub() {
    window.location.href = `${API_BASE}/auth/github`
  }

  // Login with Google
  function loginWithGoogle() {
    window.location.href = `${API_BASE}/auth/google`
  }

  // Logout
  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_user')
  }

  // Mock login for development
  function mockLogin(provider: 'github' | 'google') {
    user.value = {
      id: 'mock-user-1',
      name: 'Test User',
      email: 'test@example.com',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=test',
      role: 'admin',
      provider
    }
    token.value = 'mock-token-123'

    localStorage.setItem('auth_token', token.value)
    localStorage.setItem('auth_user', JSON.stringify(user.value))
  }

  return {
    user,
    token,
    loading,
    isLoggedIn,
    isAdmin,
    init,
    loginWithGithub,
    loginWithGoogle,
    logout,
    mockLogin
  }
})
