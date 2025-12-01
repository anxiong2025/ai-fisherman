<script setup lang="ts">
import type { Project } from '@/types'

defineProps<{
  project: Project
}>()
</script>

<template>
  <a :href="project.github" target="_blank" rel="noopener" class="project-card">
    <div class="project-card__header">
      <div class="project-card__icon" :style="{ background: project.gradient }">
        📦
      </div>
      <div class="project-card__stars">
        ⭐ {{ project.stars }}
      </div>
    </div>
    <h3 class="project-card__title">{{ project.name }}</h3>
    <p class="project-card__description">{{ project.description }}</p>
    <div class="project-card__tech">
      <span v-for="tag in project.tags" :key="tag" class="tech-tag">
        {{ tag }}
      </span>
    </div>
  </a>
</template>
