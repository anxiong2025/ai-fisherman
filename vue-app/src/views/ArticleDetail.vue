<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, RouterLink } from 'vue-router'
import { ArticleCard } from '@/components'
import { getArticleBySlug, articles } from '@/data'

const { t } = useI18n()
const route = useRoute()

const slug = computed(() => route.params.slug as string)
const article = computed(() => getArticleBySlug(slug.value))

// Get related articles (same category)
const relatedArticles = computed(() => {
  if (!article.value) return []
  return articles
    .filter(a => a.category === article.value!.category && a.id !== article.value!.id)
    .slice(0, 2)
})

// Highlight code blocks on mount
onMounted(() => {
  // Import highlight.js dynamically
  import('highlight.js').then(hljs => {
    document.querySelectorAll('pre code').forEach((block) => {
      hljs.default.highlightElement(block as HTMLElement)
    })
  })
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
          <span>{{ article.date }}</span>
          <span>·</span>
          <span>{{ t('articles.readTime', { time: article.readTime }) }}</span>
          <span>·</span>
          <span>{{ article.author }}</span>
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
    <article class="article-content">
      <p>{{ article.excerpt }}</p>

      <!-- Placeholder content - in real app, this would come from article.content -->
      <h2>Introduction</h2>
      <p>This is a placeholder for the full article content. In a production application, this content would be loaded from a CMS or database and rendered from Markdown.</p>

      <h2>Key Concepts</h2>
      <p>The article would cover important concepts related to the topic, with code examples, diagrams, and explanations.</p>

      <pre><code class="language-typescript">// Example code block
const agent = new AIAgent({
  model: 'claude-3-sonnet',
  tools: [searchTool, calculatorTool],
  memory: new ConversationMemory()
});

const result = await agent.run('What is the weather today?');
console.log(result);</code></pre>

      <h2>Conclusion</h2>
      <p>The article would conclude with a summary of key takeaways and next steps for the reader.</p>

      <blockquote>
        <p>"AI is not about replacing humans, but augmenting human capabilities."</p>
      </blockquote>
    </article>

    <!-- Related Articles -->
    <section v-if="relatedArticles.length > 0" class="section">
      <div class="container">
        <div class="section__header">
          <h2 class="section__title">{{ t('articles.relatedArticles') }}</h2>
        </div>
        <div class="card-grid" style="max-width: 900px; margin: 0 auto;">
          <ArticleCard
            v-for="related in relatedArticles"
            :key="related.id"
            :article="related"
          />
        </div>
      </div>
    </section>

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
