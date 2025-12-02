import { defineStore } from 'pinia'
import { ref } from 'vue'
import { articlesApi, type Article, type ArticleCreate, type ArticleUpdate } from '@/api'
import { useAuthStore } from './auth'

export const useArticlesStore = defineStore('articles', () => {
  const articles = ref<Article[]>([])
  const currentArticle = ref<Article | null>(null)
  const total = ref(0)
  const page = ref(1)
  const pageSize = ref(10)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const authStore = useAuthStore()

  async function fetchArticles(params: {
    page?: number
    category?: string
    tag?: string
    status?: string
  } = {}) {
    loading.value = true
    error.value = null

    try {
      const result = await articlesApi.list({
        page: params.page || page.value,
        page_size: pageSize.value,
        category: params.category,
        tag: params.tag,
        status: params.status,
        token: authStore.token || undefined,
      })

      articles.value = result.items
      total.value = result.total
      page.value = result.page
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch articles'
      console.error('Failed to fetch articles:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchArticle(slug: string) {
    loading.value = true
    error.value = null

    try {
      currentArticle.value = await articlesApi.get(slug, authStore.token || undefined)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch article'
      currentArticle.value = null
      console.error('Failed to fetch article:', e)
    } finally {
      loading.value = false
    }
  }

  async function createArticle(data: ArticleCreate) {
    if (!authStore.token) {
      throw new Error('Not authenticated')
    }

    loading.value = true
    error.value = null

    try {
      const article = await articlesApi.create(data, authStore.token)
      articles.value.unshift(article)
      return article
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to create article'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateArticle(id: string, data: ArticleUpdate) {
    if (!authStore.token) {
      throw new Error('Not authenticated')
    }

    loading.value = true
    error.value = null

    try {
      const article = await articlesApi.update(id, data, authStore.token)

      // Update in list
      const index = articles.value.findIndex(a => a.id === id)
      if (index !== -1) {
        articles.value[index] = article
      }

      // Update current if same
      if (currentArticle.value?.id === id) {
        currentArticle.value = article
      }

      return article
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to update article'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteArticle(id: string) {
    if (!authStore.token) {
      throw new Error('Not authenticated')
    }

    loading.value = true
    error.value = null

    try {
      await articlesApi.delete(id, authStore.token)
      articles.value = articles.value.filter(a => a.id !== id)

      if (currentArticle.value?.id === id) {
        currentArticle.value = null
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to delete article'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    articles,
    currentArticle,
    total,
    page,
    pageSize,
    loading,
    error,
    fetchArticles,
    fetchArticle,
    createArticle,
    updateArticle,
    deleteArticle,
  }
})
