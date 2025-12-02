<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, RouterLink } from 'vue-router'
import { useThemeStore, useAuthStore } from '@/stores'
import type { Locale } from '@/types'

const { t, locale } = useI18n()
const route = useRoute()
const themeStore = useThemeStore()
const authStore = useAuthStore()

const isMenuOpen = ref(false)

// Navigation links
const navLinks = computed(() => [
  { name: 'home', path: '/', label: t('nav.home') },
  { name: 'articles', path: '/articles', label: t('nav.articles') },
  { name: 'projects', path: '/projects', label: t('nav.projects') },
  { name: 'courses', path: '/courses', label: t('nav.courses') },
  { name: 'about', path: '/about', label: t('nav.about') }
])

// Check if link is active
function isActive(name: string): boolean {
  if (name === 'home') {
    return route.path === '/'
  }
  return route.path.startsWith(`/${name}`)
}

// Toggle mobile menu
function toggleMenu() {
  isMenuOpen.value = !isMenuOpen.value
}

// Theme icon
const themeIcon = computed(() => {
  if (themeStore.theme === 'light') return '☀️'
  if (themeStore.theme === 'dark') return '🌙'
  return '💻'
})

// Toggle language
function toggleLanguage() {
  const newLocale: Locale = locale.value === 'en' ? 'zh' : 'en'
  locale.value = newLocale
  localStorage.setItem('locale', newLocale)
}

// Login handlers
function handleLogin(provider: 'github' | 'google') {
  if (provider === 'github') {
    authStore.loginWithGithub()
  } else {
    authStore.loginWithGoogle()
  }
}
</script>

<template>
  <nav class="navbar">
    <div class="container navbar__inner">
      <!-- Logo -->
      <RouterLink to="/" class="navbar__logo">
        <span class="logo-icon">🎣</span>
        <span class="logo-text">{{ locale === 'zh' ? '渔夫 AI' : 'AI Fisherman' }}</span>
      </RouterLink>

      <!-- Mobile toggle -->
      <button
        class="navbar__toggle"
        aria-label="Menu"
        @click="toggleMenu"
        :class="{ active: isMenuOpen }"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      <!-- Navigation links -->
      <ul class="navbar__menu" :class="{ open: isMenuOpen }">
        <li v-for="link in navLinks" :key="link.name">
          <RouterLink
            :to="link.path"
            class="navbar__link"
            :class="{ 'navbar__link--active': isActive(link.name) }"
            @click="isMenuOpen = false"
          >
            {{ link.label }}
          </RouterLink>
        </li>
        <!-- Admin link (only for admins) -->
        <li v-if="authStore.isAdmin">
          <RouterLink
            to="/admin"
            class="navbar__link"
            :class="{ 'navbar__link--active': route.path.startsWith('/admin') }"
            @click="isMenuOpen = false"
          >
            {{ t('nav.admin') }}
          </RouterLink>
        </li>
      </ul>

      <!-- Actions -->
      <div class="navbar__actions">
        <!-- Theme toggle -->
        <button
          class="action-btn theme-toggle"
          :title="t(`theme.${themeStore.theme}`)"
          @click="themeStore.toggleTheme"
        >
          {{ themeIcon }}
        </button>

        <!-- Language toggle -->
        <button
          class="action-btn lang-toggle"
          :title="locale === 'en' ? '切换到中文' : 'Switch to English'"
          @click="toggleLanguage"
        >
          {{ locale === 'en' ? '中' : 'EN' }}
        </button>

        <!-- Auth -->
        <template v-if="authStore.isLoggedIn">
          <div class="user-menu">
            <img
              :src="authStore.user?.avatar"
              :alt="authStore.user?.name"
              class="user-avatar"
            />
            <span class="user-name">{{ authStore.user?.name }}</span>
            <button class="logout-btn" @click="authStore.logout">
              {{ t('nav.logout') }}
            </button>
          </div>
        </template>
        <template v-else>
          <button class="login-btn" @click="handleLogin('github')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            <span class="login-text">{{ t('nav.loginWithGithub') }}</span>
          </button>
        </template>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: var(--navbar-bg);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid var(--color-border);
  transition: all 0.3s ease;
}

.navbar__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 52px;
  gap: 24px;
}

/* Logo */
.navbar__logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  flex-shrink: 0;
}

.logo-icon {
  font-size: 22px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text);
  letter-spacing: -0.02em;
}

/* Mobile Toggle */
.navbar__toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 40px;
  height: 40px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: background 0.2s;
}

.navbar__toggle:hover {
  background: var(--color-background-secondary);
}

.navbar__toggle span {
  display: block;
  width: 20px;
  height: 2px;
  background: var(--color-text);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.navbar__toggle.active span:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.navbar__toggle.active span:nth-child(2) {
  opacity: 0;
}

.navbar__toggle.active span:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* Navigation Menu */
.navbar__menu {
  display: flex;
  align-items: center;
  gap: 8px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.navbar__link {
  display: inline-flex;
  align-items: center;
  padding: 8px 14px;
  font-size: 14px;
  font-weight: 400;
  color: var(--color-text-secondary);
  text-decoration: none;
  border-radius: 20px;
  transition: all 0.2s ease;
}

.navbar__link:hover {
  color: var(--color-text);
  background: var(--color-background-secondary);
  text-decoration: none;
}

.navbar__link--active {
  color: var(--color-text);
  font-weight: 500;
  background: var(--color-background-secondary);
}

/* Actions */
.navbar__actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

.action-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-background-secondary);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 16px;
}

.action-btn:hover {
  background: var(--color-border);
  transform: scale(1.05);
}

.lang-toggle {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text);
}

/* User Menu */
.user-menu {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--color-border);
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.logout-btn {
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-text-secondary);
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  color: var(--color-danger);
  border-color: var(--color-danger);
}

/* Login Button */
.login-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text);
  background: var(--color-background-secondary);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.login-btn:hover {
  background: var(--color-text);
  color: var(--color-background);
  border-color: var(--color-text);
}

.login-btn svg {
  flex-shrink: 0;
}

/* Responsive */
@media (max-width: 900px) {
  .navbar__menu {
    display: none;
    position: absolute;
    top: 52px;
    left: 0;
    right: 0;
    background: var(--color-background);
    flex-direction: column;
    padding: 16px;
    border-bottom: 1px solid var(--color-border);
    gap: 4px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  }

  .navbar__menu.open {
    display: flex;
  }

  .navbar__toggle {
    display: flex;
  }

  .navbar__link {
    width: 100%;
    padding: 12px 16px;
    border-radius: 12px;
  }

  .user-name {
    display: none;
  }

  .login-text {
    display: none;
  }

  .login-btn {
    width: 36px;
    height: 36px;
    padding: 0;
    border-radius: 50%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .logo-text {
    font-size: 16px;
  }

  .navbar__actions {
    gap: 6px;
  }

  .action-btn {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }
}
</style>
