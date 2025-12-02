<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { ArticleCard } from '@/components'
import { useArticlesStore } from '@/stores/articles'

const { t } = useI18n()
const route = useRoute()
const articlesStore = useArticlesStore()

const selectedCategory = ref('all')
const selectedTag = ref<string | null>(null)
const pageVisible = ref(false)

const categories = ['all', 'ai-news', 'agents', 'tutorial', 'tools']
const tags = ['LLM', 'Claude', 'GPT', 'RAG', 'LangChain', 'Prompt', 'Agent', 'Vector Database']

// Fetch articles when category changes
watch(selectedCategory, () => {
  fetchArticles()
})

async function fetchArticles() {
  await articlesStore.fetchArticles({
    category: selectedCategory.value === 'all' ? undefined : selectedCategory.value,
    tag: selectedTag.value || undefined,
  })
}

// Filter by tag (client-side for tags since we already have the data)
const filteredArticles = computed(() => {
  let result = articlesStore.articles

  if (selectedTag.value) {
    result = result.filter(a => a.tags.includes(selectedTag.value!))
  }

  return result
})

// Handle category filter
function selectCategory(category: string) {
  selectedCategory.value = category
  selectedTag.value = null
}

// Handle tag filter
function selectTag(tag: string) {
  if (selectedTag.value === tag) {
    selectedTag.value = null
  } else {
    selectedTag.value = tag
  }
}

// Check URL params on mount
onMounted(() => {
  const category = route.query.category as string
  const tag = route.query.tag as string

  if (category && categories.includes(category)) {
    selectedCategory.value = category
  }

  if (tag) {
    selectedTag.value = tag
  }

  // Trigger animation
  setTimeout(() => {
    pageVisible.value = true
  }, 100)
})
</script>

<template>
  <div class="articles-page">
    <!-- Hero Section -->
    <section class="articles-hero" :class="{ visible: pageVisible }">
      <div class="container">
        <div class="articles-hero__badge">
          <span class="badge-dot"></span>
          {{ t('articles.subtitle') }}
        </div>
        <h1 class="articles-hero__title">{{ t('articles.title') }}</h1>
        <p class="articles-hero__description">
          Explore our collection of in-depth articles, tutorials, and insights on AI,
          machine learning, and the latest developments in artificial intelligence.
        </p>
      </div>
    </section>

    <!-- Filters Section -->
    <section class="filters-section" :class="{ visible: pageVisible }">
      <div class="container">
        <!-- Category Pills -->
        <div class="category-filter">
          <button
            v-for="category in categories"
            :key="category"
            class="category-pill"
            :class="{ active: selectedCategory === category }"
            @click="selectCategory(category)"
          >
            {{ t(`articles.categories.${category}`) }}
          </button>
        </div>

        <!-- Tags -->
        <div class="tags-filter">
          <button
            v-for="tag in tags"
            :key="tag"
            class="tag-chip"
            :class="{ active: selectedTag === tag }"
            @click="selectTag(tag)"
          >
            {{ tag }}
          </button>
        </div>

        <!-- Results count -->
        <div class="results-info">
          <span class="results-count">{{ filteredArticles.length }}</span> articles found
        </div>
      </div>
    </section>

    <!-- Articles Grid -->
    <section class="articles-grid-section" :class="{ visible: pageVisible }">
      <div class="container">
        <div class="articles-grid">
          <ArticleCard
            v-for="(article, index) in filteredArticles"
            :key="article.id"
            :article="article"
            :style="{ animationDelay: `${index * 0.1}s` }"
            class="article-item"
          />
        </div>

        <div v-if="filteredArticles.length === 0" class="empty-state">
          <div class="empty-icon">📝</div>
          <h3>No articles found</h3>
          <p>Try adjusting your filters to find what you're looking for.</p>
          <button class="btn-reset" @click="selectCategory('all')">
            Clear filters
          </button>
        </div>

        <div v-if="filteredArticles.length > 8" class="load-more">
          <button class="btn-load-more">
            {{ t('articles.loadMore') }}
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M8 3v10M4 9l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.articles-page {
  min-height: 100vh;
  background: var(--color-background);
}

/* Hero Section */
.articles-hero {
  padding: 100px 0 60px;
  text-align: center;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.articles-hero.visible {
  opacity: 1;
  transform: translateY(0);
}

.articles-hero__badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  background: var(--color-background-secondary);
  border-radius: 100px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: 24px;
}

.badge-dot {
  width: 8px;
  height: 8px;
  background: var(--color-primary);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

.articles-hero__title {
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin-bottom: 20px;
  background: linear-gradient(135deg, var(--color-text) 0%, var(--color-text-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.articles-hero__description {
  max-width: 600px;
  margin: 0 auto;
  font-size: 18px;
  line-height: 1.7;
  color: var(--color-text-secondary);
}

/* Filters Section */
.filters-section {
  padding: 0 0 40px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.2s;
}

.filters-section.visible {
  opacity: 1;
  transform: translateY(0);
}

.category-filter {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
}

.category-pill {
  padding: 12px 24px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 100px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-pill:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.category-pill.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.tags-filter {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 24px;
}

.tag-chip {
  padding: 8px 16px;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.tag-chip:hover {
  background: var(--color-background-secondary);
  border-color: var(--color-text-tertiary);
}

.tag-chip.active {
  background: var(--color-text);
  border-color: var(--color-text);
  color: var(--color-background);
}

.results-info {
  text-align: center;
  font-size: 14px;
  color: var(--color-text-tertiary);
}

.results-count {
  font-weight: 600;
  color: var(--color-primary);
}

/* Articles Grid */
.articles-grid-section {
  padding: 20px 0 100px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.4s;
}

.articles-grid-section.visible {
  opacity: 1;
  transform: translateY(0);
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 32px;
}

.article-item {
  opacity: 0;
  animation: fadeInUp 0.6s ease forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.empty-state h3 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--color-text);
}

.empty-state p {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin-bottom: 24px;
}

.btn-reset {
  padding: 12px 24px;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 100px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-reset:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 30px rgba(0, 113, 227, 0.3);
}

/* Load More */
.load-more {
  text-align: center;
  margin-top: 60px;
}

.btn-load-more {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 16px 32px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 100px;
  font-size: 15px;
  font-weight: 500;
  color: var(--color-text);
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-load-more:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  transform: translateY(-2px);
}

.btn-load-more svg {
  transition: transform 0.3s ease;
}

.btn-load-more:hover svg {
  transform: translateY(3px);
}

@media (max-width: 768px) {
  .articles-hero {
    padding: 80px 0 40px;
  }

  .articles-hero__description {
    font-size: 16px;
  }

  .articles-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .category-filter {
    gap: 8px;
  }

  .category-pill {
    padding: 10px 18px;
    font-size: 13px;
  }
}
</style>
