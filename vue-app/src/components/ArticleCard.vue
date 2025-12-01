<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import type { Article } from '@/types'

const props = defineProps<{
  article: Article
}>()

const { t } = useI18n()

const categoryLabel = computed(() => {
  return t(`articles.categories.${props.article.category}`)
})
</script>

<template>
  <RouterLink :to="`/articles/${article.slug}`" class="article-card">
    <div class="article-card__image" :style="{ background: article.gradient }">
      <div class="article-card__category">{{ categoryLabel }}</div>
    </div>
    <div class="article-card__content">
      <h3 class="article-card__title">{{ article.title }}</h3>
      <p class="article-card__excerpt">{{ article.excerpt }}</p>
      <div class="article-card__tags">
        <span v-for="tag in article.tags.slice(0, 3)" :key="tag" class="article-card__tag">
          {{ tag }}
        </span>
      </div>
      <div class="article-card__meta">
        <span class="article-card__date">{{ article.date }}</span>
        <span class="article-card__read-time">{{ t('articles.readTime', { time: article.readTime }) }}</span>
      </div>
    </div>
    <div class="article-card__arrow">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M4 10h12M12 6l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
  </RouterLink>
</template>

<style scoped>
.article-card {
  display: flex;
  flex-direction: column;
  background: var(--color-card);
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  position: relative;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid var(--color-border);
}

.article-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.12);
  border-color: transparent;
}

[data-theme="dark"] .article-card:hover {
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

.article-card__image {
  height: 180px;
  position: relative;
  overflow: hidden;
}

.article-card__image::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.1) 100%);
}

.article-card__category {
  position: absolute;
  top: 16px;
  left: 16px;
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: #1d1d1f;
  font-size: 12px;
  font-weight: 600;
  border-radius: 100px;
  z-index: 1;
  letter-spacing: 0.3px;
}

.article-card__content {
  padding: 24px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.article-card__title {
  font-size: 19px;
  font-weight: 600;
  line-height: 1.35;
  margin-bottom: 12px;
  color: var(--color-text);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.3s ease;
}

.article-card:hover .article-card__title {
  color: var(--color-primary);
}

.article-card__excerpt {
  font-size: 15px;
  line-height: 1.6;
  color: var(--color-text-secondary);
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.article-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.article-card__tag {
  display: inline-flex;
  padding: 4px 12px;
  background: var(--color-background-secondary);
  color: var(--color-text-secondary);
  font-size: 12px;
  font-weight: 500;
  border-radius: 100px;
  transition: all 0.3s ease;
}

.article-card:hover .article-card__tag {
  background: var(--color-primary);
  color: white;
}

.article-card__meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  color: var(--color-text-tertiary);
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.article-card__date {
  font-weight: 500;
}

.article-card__read-time {
  opacity: 0.8;
}

.article-card__arrow {
  position: absolute;
  bottom: 24px;
  right: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-background-secondary);
  border-radius: 50%;
  color: var(--color-text-secondary);
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  opacity: 0;
  transform: translateX(-10px);
}

.article-card:hover .article-card__arrow {
  opacity: 1;
  transform: translateX(0);
  background: var(--color-primary);
  color: white;
}

@media (max-width: 768px) {
  .article-card__image {
    height: 160px;
  }

  .article-card__content {
    padding: 20px;
  }

  .article-card__title {
    font-size: 17px;
  }

  .article-card__excerpt {
    font-size: 14px;
  }
}
</style>
