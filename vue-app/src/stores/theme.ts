import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Theme } from '@/types'

export const useThemeStore = defineStore('theme', () => {
  // Get saved theme or default to 'system'
  const savedTheme = (localStorage.getItem('theme') as Theme) || 'system'
  const theme = ref<Theme>(savedTheme)

  // Actual applied theme (resolved from 'system')
  const resolvedTheme = ref<'light' | 'dark'>('light')

  // Apply theme to document
  function applyTheme(t: 'light' | 'dark') {
    resolvedTheme.value = t
    document.documentElement.setAttribute('data-theme', t)

    // Also update meta theme-color for mobile browsers
    const metaThemeColor = document.querySelector('meta[name="theme-color"]')
    if (metaThemeColor) {
      metaThemeColor.setAttribute('content', t === 'dark' ? '#1a1a2e' : '#ffffff')
    }
  }

  // Get system preference
  function getSystemTheme(): 'light' | 'dark' {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark'
    }
    return 'light'
  }

  // Update theme
  function setTheme(newTheme: Theme) {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)

    if (newTheme === 'system') {
      applyTheme(getSystemTheme())
    } else {
      applyTheme(newTheme)
    }
  }

  // Toggle between light and dark
  function toggleTheme() {
    if (theme.value === 'light') {
      setTheme('dark')
    } else if (theme.value === 'dark') {
      setTheme('system')
    } else {
      setTheme('light')
    }
  }

  // Initialize theme
  function initTheme() {
    if (theme.value === 'system') {
      applyTheme(getSystemTheme())
    } else {
      applyTheme(theme.value)
    }

    // Listen for system theme changes
    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (theme.value === 'system') {
          applyTheme(e.matches ? 'dark' : 'light')
        }
      })
    }
  }

  return {
    theme,
    resolvedTheme,
    setTheme,
    toggleTheme,
    initTheme
  }
})
