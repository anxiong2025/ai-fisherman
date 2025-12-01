<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="hero" style="min-height: 60vh; display: flex; align-items: center;">
    <div class="container text-center">
      <h1 style="font-size: 120px; font-weight: 600; opacity: 0.2; margin-bottom: 16px;">404</h1>
      <h2 class="hero__title">Page Not Found</h2>
      <p class="hero__subtitle">The page you're looking for doesn't exist or has been moved.</p>
      <RouterLink to="/" class="btn btn--primary btn--large mt-lg">
        Back to Home
      </RouterLink>
    </div>
  </section>
</template>
