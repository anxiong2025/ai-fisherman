<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ProjectCard } from '@/components'
import { projects } from '@/data'

const { t } = useI18n()
</script>

<template>
  <div class="projects-page">
    <!-- Hero -->
    <section class="hero">
      <div class="container">
        <h1 class="hero__title">{{ t('projects.title') }}</h1>
        <p class="hero__subtitle">{{ t('projects.subtitle') }}</p>
      </div>
    </section>

  <!-- Projects Grid -->
  <section class="section">
    <div class="container">
      <div class="card-grid">
        <ProjectCard
          v-for="project in projects"
          :key="project.id"
          :project="project"
        />
      </div>
    </div>
  </section>

  <!-- Contribute CTA -->
  <section class="section" style="background: var(--color-background-secondary);">
    <div class="container text-center" style="max-width: 700px;">
      <h2 class="section__title">Want to Contribute?</h2>
      <p class="section__subtitle mb-md">
        All projects are open source and welcome contributions. Check out the repositories on GitHub to get started.
      </p>
      <a
        href="https://github.com/anxiong2025"
        target="_blank"
        rel="noopener"
        class="btn btn--primary btn--large"
      >
        {{ t('projects.viewGithub') }}
      </a>
    </div>
  </section>
  </div>
</template>

<style scoped>
.projects-page {
  min-height: 100vh;
  background: var(--color-background);
  position: relative;
  z-index: 1;
}
</style>
