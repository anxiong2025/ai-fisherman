<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { Navbar, Footer, AiChat } from '@/components'
import ParticleBackground from '@/components/ParticleBackground.vue'
import { useThemeStore, useAuthStore } from '@/stores'

const themeStore = useThemeStore()
const authStore = useAuthStore()

onMounted(() => {
  // Initialize theme
  themeStore.initTheme()

  // Initialize auth
  authStore.init()
})
</script>

<template>
  <div id="app">
    <ParticleBackground />
    <Navbar />

    <main>
      <RouterView />
    </main>

    <Footer />

    <!-- AI Chat Widget -->
    <AiChat />
  </div>
</template>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

main {
  flex: 1;
}
</style>
