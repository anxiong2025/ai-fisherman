<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, RouterLink } from 'vue-router'
import { articlesApi, type Article } from '@/api'
import { marked } from 'marked'

const { t } = useI18n()
const route = useRoute()

const article = ref<Article | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

const slug = computed(() => route.params.slug as string)

// Fetch article from API
async function fetchArticle() {
  loading.value = true
  error.value = null
  try {
    article.value = await articlesApi.get(slug.value)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load article'
    article.value = null
  } finally {
    loading.value = false
  }
}

// Watch for slug changes
watch(slug, fetchArticle, { immediate: true })

// Render markdown content
const renderedContent = computed(() => {
  if (!article.value) return ''
  return marked(article.value.content)
})

// Highlight code blocks when article loads
watch(article, async () => {
  if (article.value) {
    await new Promise(r => setTimeout(r, 100)) // Wait for DOM update
    import('highlight.js').then(hljs => {
      document.querySelectorAll('pre code').forEach((block) => {
        hljs.default.highlightElement(block as HTMLElement)
      })
    })
  }
})
</script>

<template>
  <template v-if="article">
    <!-- Article Header -->
    <header class="article-header">
      <div class="container">
        <RouterLink
          :to="`/articles?category=${article.category}`"
          class="article-header__category"
        >
          {{ t(`articles.categories.${article.category}`) }}
        </RouterLink>
        <h1 class="article-header__title">{{ article.title }}</h1>
        <div class="article-header__meta">
          <span>{{ new Date(article.created_at).toLocaleDateString() }}</span>
          <span>·</span>
          <span>{{ t('articles.readTime', { time: article.read_time }) }}</span>
          <span>·</span>
          <span>{{ article.author.name }}</span>
        </div>
        <div class="tags mt-md" style="justify-content: center;">
          <RouterLink
            v-for="tag in article.tags"
            :key="tag"
            :to="`/articles?tag=${tag}`"
            class="tag"
          >
            {{ tag }}
          </RouterLink>
        </div>
      </div>
    </header>

    <!-- Article Content -->
    <article class="article-content container">
      <div class="article-body" v-html="renderedContent"></div>
    </article>

    <!-- Course CTA -->
    <section class="section" style="background: var(--color-background-secondary);">
      <div class="container text-center" style="max-width: 700px;">
        <h2 class="section__title">{{ t('courses.cta.title') }}</h2>
        <p class="section__subtitle mb-md">{{ t('courses.cta.subtitle') }}</p>
        <RouterLink to="/courses" class="btn btn--primary btn--large">
          {{ t('courses.cta.button') }}
        </RouterLink>
      </div>
    </section>
  </template>

  <!-- 404 -->
  <template v-else>
    <section class="hero">
      <div class="container text-center">
        <h1 class="hero__title">Article Not Found</h1>
        <p class="hero__subtitle">The article you're looking for doesn't exist.</p>
        <RouterLink to="/articles" class="btn btn--primary mt-lg">
          Back to Articles
        </RouterLink>
      </div>
    </section>
  </template>
</template>

<style scoped>
.article-content {
  padding-bottom: var(--spacing-xl);
}
</style>
