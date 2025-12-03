<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import { useArticlesStore } from '@/stores/articles'

const { t } = useI18n()
const articlesStore = useArticlesStore()

const searchQuery = ref('')
const selectedCategory = ref('all')
const selectedStatus = ref('all')

const categories = ['all', 'ai-news', 'agents', 'tutorial', 'tools']
const statuses = ['all', 'published', 'draft']

// Fetch articles on mount
onMounted(() => {
  fetchArticles()
})

// Refetch when filters change
watch([selectedCategory, selectedStatus], () => {
  fetchArticles()
})

async function fetchArticles() {
  await articlesStore.fetchArticles({
    category: selectedCategory.value === 'all' ? undefined : selectedCategory.value,
    status: selectedStatus.value === 'all' ? undefined : selectedStatus.value,
  })
}

// Filter articles by search (client-side for immediate feedback)
const filteredArticles = computed(() => {
  if (!searchQuery.value) {
    return articlesStore.articles
  }
  return articlesStore.articles.filter(article =>
    article.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// Delete article
async function deleteArticle(id: string) {
  if (confirm('Are you sure you want to delete this article?')) {
    try {
      await articlesStore.deleteArticle(id)
    } catch (e) {
      alert(e instanceof Error ? e.message : 'Failed to delete article')
    }
  }
}

// Format date
function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString()
}
</script>

<template>
  <div class="admin-page">
    <div class="container">
      <div class="admin-header">
        <h1>{{ t('admin.articles') }}</h1>
        <RouterLink to="/admin/articles/new" class="btn btn--primary">
          + {{ t('admin.articleEditor.newArticle') }}
        </RouterLink>
      </div>

      <!-- Filters -->
      <div class="admin-filters">
        <input
          v-model="searchQuery"
          type="text"
          :placeholder="t('common.search')"
          class="admin-search"
        />
        <select v-model="selectedCategory" class="admin-select">
          <option v-for="category in categories" :key="category" :value="category">
            {{ category === 'all' ? 'All Categories' : t(`articles.categories.${category}`) }}
          </option>
        </select>
        <select v-model="selectedStatus" class="admin-select">
          <option v-for="status in statuses" :key="status" :value="status">
            {{ status === 'all' ? 'All Status' : status }}
          </option>
        </select>
      </div>

      <!-- Articles Table -->
      <div class="admin-card">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Category</th>
              <th>Status</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="article in filteredArticles" :key="article.id">
              <td>
                <div class="article-title-cell">
                  <strong>{{ article.title }}</strong>
                  <span class="article-excerpt">{{ article.excerpt.substring(0, 60) }}...</span>
                </div>
              </td>
              <td>
                <span class="badge">{{ t(`articles.categories.${article.category}`) }}</span>
              </td>
              <td>
                <span
                  class="status-badge"
                  :class="`status-badge--${article.status}`"
                >
                  {{ article.status }}
                </span>
              </td>
              <td>{{ formatDate(article.created_at) }}</td>
              <td>
                <div class="action-buttons">
                  <RouterLink
                    :to="`/admin/articles/${article.id}/edit`"
                    class="btn btn--ghost btn--small"
                  >
                    {{ t('common.edit') }}
                  </RouterLink>
                  <button
                    class="btn btn--ghost btn--small"
                    style="color: var(--color-danger);"
                    @click="deleteArticle(article.id)"
                  >
                    {{ t('common.delete') }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="filteredArticles.length === 0" class="empty-state">
          <p>No articles found.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-page {
  padding: 40px 0;
  min-height: calc(100vh - 52px);
  background: var(--color-background-secondary);
  position: relative;
  z-index: 1;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.admin-header h1 {
  font-size: 32px;
  font-weight: 600;
}

.admin-filters {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.admin-search {
  flex: 1;
  min-width: 200px;
  padding: 12px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-card);
  color: var(--color-text);
  font-size: 14px;
}

.admin-search:focus {
  outline: none;
  border-color: var(--color-primary);
}

.admin-select {
  padding: 12px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-card);
  color: var(--color-text);
  font-size: 14px;
  cursor: pointer;
}

.admin-card {
  background: var(--color-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  overflow-x: auto;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 700px;
}

.admin-table th,
.admin-table td {
  padding: 16px 12px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.admin-table th {
  font-weight: 600;
  color: var(--color-text-secondary);
  font-size: 12px;
  text-transform: uppercase;
}

.admin-table tr:last-child td {
  border-bottom: none;
}

.article-title-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.article-title-cell strong {
  font-size: 15px;
}

.article-excerpt {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.badge {
  display: inline-block;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 500;
  background: var(--color-background-secondary);
  border-radius: 980px;
}

.status-badge {
  display: inline-block;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 500;
  border-radius: 980px;
}

.status-badge--published {
  background: rgba(52, 199, 89, 0.1);
  color: #34c759;
}

.status-badge--draft {
  background: rgba(255, 149, 0, 0.1);
  color: #ff9500;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.empty-state {
  text-align: center;
  padding: 48px;
  color: var(--color-text-secondary);
}
</style>
