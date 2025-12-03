<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, RouterLink } from 'vue-router'
import { useThemeStore, useAuthStore } from '@/stores'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import { Sun, Moon, Monitor, Menu, X, Github, Star } from 'lucide-vue-next'
import type { Locale } from '@/types'

const { t, locale } = useI18n()
const route = useRoute()
const themeStore = useThemeStore()
const authStore = useAuthStore()

const isMenuOpen = ref(false)

// GitHub star count
const githubStars = ref<number | null>(null)

async function fetchGithubStars() {
  try {
    const response = await fetch('https://api.github.com/repos/anxiong2025/ai-fisherman')
    if (response.ok) {
      const data = await response.json()
      githubStars.value = data.stargazers_count
    }
  } catch {
    // Silently fail
  }
}

onMounted(() => {
  fetchGithubStars()
})

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

// Theme icon component
const ThemeIcon = computed(() => {
  if (themeStore.theme === 'light') return Sun
  if (themeStore.theme === 'dark') return Moon
  return Monitor
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
  <nav class="sticky top-0 z-[1000] bg-navbar border-b border-[var(--color-border)] transition-all duration-300">
    <div class="max-w-[1200px] mx-auto px-6 flex items-center justify-between h-[52px] gap-6">
      <!-- Logo -->
      <RouterLink to="/" class="flex items-center gap-2 no-underline shrink-0">
        <span class="text-[22px]">🎣</span>
        <span class="text-lg font-semibold text-[var(--color-text)] tracking-tight max-[480px]:text-base">
          {{ locale === 'zh' ? '渔夫 AI' : 'AI Fisherman' }}
        </span>
      </RouterLink>

      <!-- Mobile toggle -->
      <button
        class="hidden max-[900px]:flex items-center justify-center w-10 h-10 bg-transparent border-none cursor-pointer rounded-lg transition-colors hover:bg-[var(--color-background-secondary)]"
        aria-label="Menu"
        @click="toggleMenu"
      >
        <Menu v-if="!isMenuOpen" class="w-5 h-5 text-[var(--color-text)]" />
        <X v-else class="w-5 h-5 text-[var(--color-text)]" />
      </button>

      <!-- Navigation links -->
      <ul
        class="flex items-center gap-2 list-none m-0 p-0 max-[900px]:hidden max-[900px]:absolute max-[900px]:top-[52px] max-[900px]:left-0 max-[900px]:right-0 max-[900px]:bg-[var(--color-background)] max-[900px]:flex-col max-[900px]:p-4 max-[900px]:border-b max-[900px]:border-[var(--color-border)] max-[900px]:shadow-lg"
        :class="{ 'max-[900px]:!flex': isMenuOpen }"
      >
        <li v-for="link in navLinks" :key="link.name">
          <RouterLink
            :to="link.path"
            class="inline-flex items-center px-3.5 py-2 text-sm font-normal text-[var(--color-text-secondary)] no-underline rounded-[20px] transition-all duration-200 hover:text-[var(--color-text)] hover:bg-[var(--color-background-secondary)] max-[900px]:w-full max-[900px]:px-4 max-[900px]:py-3 max-[900px]:rounded-xl"
            :class="{ '!text-[var(--color-text)] font-medium bg-[var(--color-background-secondary)]': isActive(link.name) }"
            @click="isMenuOpen = false"
          >
            {{ link.label }}
          </RouterLink>
        </li>
        <!-- Admin link (only for admins) -->
        <li v-if="authStore.isAdmin">
          <RouterLink
            to="/admin"
            class="inline-flex items-center px-3.5 py-2 text-sm font-normal text-[var(--color-text-secondary)] no-underline rounded-[20px] transition-all duration-200 hover:text-[var(--color-text)] hover:bg-[var(--color-background-secondary)]"
            :class="{ '!text-[var(--color-text)] font-medium bg-[var(--color-background-secondary)]': route.path.startsWith('/admin') }"
            @click="isMenuOpen = false"
          >
            {{ t('nav.admin') }}
          </RouterLink>
        </li>
      </ul>

      <!-- Actions -->
      <div class="flex items-center gap-2 ml-auto max-[480px]:gap-1.5">
        <!-- GitHub Star Badge -->
        <a
          href="https://github.com/anxiong2025/ai-fisherman"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-medium text-[var(--color-text-secondary)] bg-[var(--color-background-secondary)] border border-[var(--color-border)] rounded-full no-underline transition-all hover:border-[var(--color-text-tertiary)] hover:text-[var(--color-text)]"
        >
          <Github class="w-3.5 h-3.5" />
          <Star class="w-3 h-3 text-amber-500 fill-amber-500" />
          <span>{{ githubStars !== null ? githubStars : '-' }}</span>
        </a>

        <!-- Theme toggle -->
        <Button
          variant="ghost"
          size="icon"
          :title="t(`theme.${themeStore.theme}`)"
          @click="themeStore.toggleTheme"
          class="!w-9 !h-9 max-[480px]:!w-8 max-[480px]:!h-8"
        >
          <component :is="ThemeIcon" class="w-4 h-4" />
        </Button>

        <!-- Language toggle -->
        <Button
          variant="ghost"
          size="icon"
          :title="locale === 'en' ? '切换到中文' : 'Switch to English'"
          @click="toggleLanguage"
          class="!w-9 !h-9 !text-xs !font-semibold max-[480px]:!w-8 max-[480px]:!h-8"
        >
          {{ locale === 'en' ? '中' : 'EN' }}
        </Button>

        <!-- Auth -->
        <template v-if="authStore.isLoggedIn">
          <div class="flex items-center gap-2.5">
            <Avatar size="sm" class="border-2 border-[var(--color-border)]">
              <AvatarImage :src="authStore.user?.avatar ?? ''" :alt="authStore.user?.name ?? ''" />
              <AvatarFallback>{{ authStore.user?.name?.charAt(0) }}</AvatarFallback>
            </Avatar>
            <span class="text-sm font-medium text-[var(--color-text)] max-w-[100px] truncate max-[900px]:hidden">
              {{ authStore.user?.name }}
            </span>
            <Button
              variant="outline"
              size="sm"
              @click="authStore.logout"
              class="!px-3 !py-1.5 !text-xs hover:!text-[var(--color-danger)] hover:!border-[var(--color-danger)]"
            >
              {{ t('nav.logout') }}
            </Button>
          </div>
        </template>
        <template v-else>
          <Button
            variant="ghost"
            size="sm"
            @click="handleLogin('github')"
            class="!gap-2 max-[900px]:!w-9 max-[900px]:!h-9 max-[900px]:!p-0"
          >
            <Github class="w-[18px] h-[18px]" />
            <span class="max-[900px]:hidden">{{ t('nav.loginWithGithub') }}</span>
          </Button>
        </template>
      </div>
    </div>
  </nav>
</template>
