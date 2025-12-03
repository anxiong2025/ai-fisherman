<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import { Badge } from '@/components/ui/badge'
import { ArrowRight } from 'lucide-vue-next'
import type { Article } from '@/types'

const props = defineProps<{
  article: Article
}>()

const { t } = useI18n()

const categoryLabel = computed(() => {
  return t(`articles.categories.${props.article.category}`)
})

// Support both old format (date) and new API format (created_at)
const articleDate = computed(() => {
  if (props.article.date) {
    return props.article.date
  }
  if (props.article.created_at) {
    return new Date(props.article.created_at).toLocaleDateString()
  }
  return ''
})

// Support both old format (readTime) and new API format (read_time)
const readTime = computed(() => {
  return props.article.readTime ?? props.article.read_time ?? 5
})
</script>

<template>
  <RouterLink
    :to="`/articles/${article.slug}`"
    class="group flex flex-col bg-[var(--color-card)] rounded-[20px] overflow-hidden transition-all duration-[400ms] ease-[cubic-bezier(0.25,0.46,0.45,0.94)] relative shadow-[0_2px_20px_rgba(0,0,0,0.04)] border border-[var(--color-border)] no-underline hover:-translate-y-2 hover:shadow-[0_20px_60px_rgba(0,0,0,0.12)] hover:border-transparent dark:hover:shadow-[0_20px_60px_rgba(0,0,0,0.4)]"
  >
    <!-- Image -->
    <div
      class="h-[180px] max-[768px]:h-[160px] relative overflow-hidden"
      :style="{ background: article.gradient }"
    >
      <div class="absolute inset-0 bg-gradient-to-b from-transparent to-black/10"></div>
      <span class="absolute top-4 left-4 px-3.5 py-1.5 bg-white/95 backdrop-blur-[10px] text-[#1d1d1f] text-xs font-semibold rounded-full z-[1] tracking-[0.3px]">
        {{ categoryLabel }}
      </span>
    </div>

    <!-- Content -->
    <div class="p-6 max-[768px]:p-5 flex-1 flex flex-col">
      <h3 class="text-[19px] max-[768px]:text-[17px] font-semibold leading-[1.35] mb-3 text-[var(--color-text)] line-clamp-2 transition-colors duration-300 group-hover:text-[var(--color-primary)]">
        {{ article.title }}
      </h3>
      <p class="text-[15px] max-[768px]:text-sm leading-[1.6] text-[var(--color-text-secondary)] mb-4 line-clamp-2 flex-1">
        {{ article.excerpt }}
      </p>

      <!-- Tags -->
      <div class="flex flex-wrap gap-2 mb-4">
        <Badge
          v-for="tag in article.tags.slice(0, 3)"
          :key="tag"
          variant="secondary"
          class="transition-all duration-300 group-hover:bg-[var(--color-primary)] group-hover:text-white"
        >
          {{ tag }}
        </Badge>
      </div>

      <!-- Meta -->
      <div class="flex items-center justify-between text-[13px] text-[var(--color-text-tertiary)] pt-4 border-t border-[var(--color-border)]">
        <span class="font-medium">{{ articleDate }}</span>
        <span class="opacity-80">{{ t('articles.readTime', { time: readTime }) }}</span>
      </div>
    </div>

    <!-- Arrow -->
    <div class="absolute bottom-6 right-6 w-10 h-10 flex items-center justify-center bg-[var(--color-background-secondary)] rounded-full text-[var(--color-text-secondary)] transition-all duration-[400ms] ease-[cubic-bezier(0.25,0.46,0.45,0.94)] opacity-0 -translate-x-2.5 group-hover:opacity-100 group-hover:translate-x-0 group-hover:bg-[var(--color-primary)] group-hover:text-white">
      <ArrowRight class="w-5 h-5" />
    </div>
  </RouterLink>
</template>
