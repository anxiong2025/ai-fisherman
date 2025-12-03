<script setup lang="ts">
import { Badge } from '@/components/ui/badge'
import { Star, Package } from 'lucide-vue-next'
import type { Project } from '@/types'

defineProps<{
  project: Project
}>()
</script>

<template>
  <a
    :href="project.github"
    target="_blank"
    rel="noopener"
    class="group block bg-[var(--color-card)] rounded-[var(--radius-lg)] p-6 shadow-[var(--shadow-sm)] transition-all duration-[300ms] ease-[cubic-bezier(0.25,0.46,0.45,0.94)] no-underline hover:-translate-y-1 hover:shadow-[var(--shadow-md)]"
  >
    <!-- Header -->
    <div class="flex items-start justify-between mb-4">
      <div
        class="w-12 h-12 rounded-[var(--radius-md)] flex items-center justify-center text-white text-2xl"
        :style="{ background: project.gradient }"
      >
        <Package class="w-6 h-6" />
      </div>
      <div class="flex items-center gap-1 text-sm text-[var(--color-text-secondary)]">
        <Star class="w-4 h-4 fill-yellow-400 text-yellow-400" />
        {{ project.stars }}
      </div>
    </div>

    <!-- Title -->
    <h3 class="text-[21px] font-semibold mb-2 text-[var(--color-text)] transition-colors duration-300 group-hover:text-[var(--color-primary)]">
      {{ project.name }}
    </h3>

    <!-- Description -->
    <p class="text-sm text-[var(--color-text-secondary)] leading-[1.43] mb-4 line-clamp-2">
      {{ project.description }}
    </p>

    <!-- Tags -->
    <div class="flex flex-wrap gap-2">
      <Badge v-for="tag in project.tags" :key="tag" variant="secondary">
        {{ tag }}
      </Badge>
    </div>
  </a>
</template>
