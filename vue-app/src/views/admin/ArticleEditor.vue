<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'
import { useArticlesStore } from '@/stores/articles'
import type { Article } from '@/types'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const articlesStore = useArticlesStore()

// Current article ID (for editing)
const articleId = ref<string | null>(null)

// Form data
const form = ref({
  title: '',
  slug: '',
  excerpt: '',
  content: '',
  category: 'tutorial' as Article['category'],
  tags: '',
  status: 'draft' as Article['status'],
  gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
})

// State
const isEditing = computed(() => !!route.params.id)
const showPreview = ref(false)
const saving = ref(false)

// Preview content
const previewContent = computed(() => {
  return marked.parse(form.value.content) as string
})

// Categories
const categories = [
  { value: 'ai-news', label: 'AI News' },
  { value: 'agents', label: 'Agents Development' },
  { value: 'tutorial', label: 'Tutorial' },
  { value: 'tools', label: 'Tools' }
]

// Gradients for random selection
const gradients = [
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
  'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
  'linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%)',
  'linear-gradient(135deg, #f6d365 0%, #fda085 100%)',
]

// Load article if editing
onMounted(async () => {
  if (isEditing.value) {
    const slug = route.params.id as string
    await articlesStore.fetchArticle(slug)

    if (articlesStore.currentArticle) {
      const article = articlesStore.currentArticle
      articleId.value = article.id
      form.value = {
        title: article.title,
        slug: article.slug,
        excerpt: article.excerpt,
        content: article.content,
        category: article.category as Article['category'],
        tags: article.tags.join(', '),
        status: article.status as Article['status'],
        gradient: article.gradient
      }
    }
  } else {
    // Random gradient for new articles
    form.value.gradient = gradients[Math.floor(Math.random() * gradients.length)] ?? gradients[0] ?? ''
  }
})

// Auto-generate slug from title
watch(() => form.value.title, (newTitle) => {
  if (!isEditing.value) {
    form.value.slug = newTitle
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '')
  }
})

// Markdown toolbar actions
function insertMarkdown(before: string, after = '') {
  const textarea = document.getElementById('content') as HTMLTextAreaElement
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const selectedText = form.value.content.substring(start, end)
  const newText = form.value.content.substring(0, start) + before + selectedText + after + form.value.content.substring(end)
  form.value.content = newText

  // Reset cursor position
  setTimeout(() => {
    textarea.focus()
    textarea.selectionStart = textarea.selectionEnd = start + before.length + selectedText.length + after.length
  }, 0)
}

// Toolbar buttons
const toolbarButtons = [
  { label: 'H1', action: () => insertMarkdown('# ') },
  { label: 'H2', action: () => insertMarkdown('## ') },
  { label: 'H3', action: () => insertMarkdown('### ') },
  { label: 'B', action: () => insertMarkdown('**', '**'), style: 'font-weight: bold' },
  { label: 'I', action: () => insertMarkdown('*', '*'), style: 'font-style: italic' },
  { label: '~', action: () => insertMarkdown('~~', '~~') },
  { label: 'Link', action: () => insertMarkdown('[', '](url)') },
  { label: 'Image', action: () => insertMarkdown('![alt](', ')') },
  { label: 'Code', action: () => insertMarkdown('```\n', '\n```') },
  { label: 'Quote', action: () => insertMarkdown('> ') },
  { label: 'List', action: () => insertMarkdown('- ') },
  { label: '1.', action: () => insertMarkdown('1. ') }
]

// Save article
async function saveArticle(status: 'draft' | 'published') {
  form.value.status = status

  // Validate
  if (!form.value.title || !form.value.content) {
    alert('Please fill in title and content')
    return
  }

  saving.value = true

  try {
    const tags = form.value.tags.split(',').map(t => t.trim()).filter(Boolean)

    const articleData = {
      title: form.value.title,
      slug: form.value.slug,
      excerpt: form.value.excerpt,
      content: form.value.content,
      category: form.value.category,
      tags,
      status,
      gradient: form.value.gradient,
    }

    if (isEditing.value && articleId.value) {
      await articlesStore.updateArticle(articleId.value, articleData)
    } else {
      await articlesStore.createArticle(articleData)
    }

    router.push('/admin/articles')
  } catch (e) {
    alert(e instanceof Error ? e.message : 'Failed to save article')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="editor-page">
    <div class="container">
      <!-- Header -->
      <div class="editor-header">
        <h1>{{ isEditing ? t('admin.articleEditor.editArticle') : t('admin.articleEditor.newArticle') }}</h1>
        <div class="editor-actions">
          <button class="btn btn--ghost" @click="router.back()">
            {{ t('common.cancel') }}
          </button>
          <button class="btn btn--secondary" @click="saveArticle('draft')">
            {{ t('admin.articleEditor.saveDraft') }}
          </button>
          <button class="btn btn--primary" @click="saveArticle('published')">
            {{ t('admin.articleEditor.publish') }}
          </button>
        </div>
      </div>

      <div class="editor-grid">
        <!-- Main Editor -->
        <div class="editor-main">
          <!-- Title -->
          <input
            v-model="form.title"
            type="text"
            :placeholder="t('admin.articleEditor.titlePlaceholder')"
            class="editor-title"
          />

          <!-- Toolbar -->
          <div class="editor-toolbar">
            <button
              v-for="btn in toolbarButtons"
              :key="btn.label"
              class="toolbar-btn"
              :style="btn.style"
              @click="btn.action"
            >
              {{ btn.label }}
            </button>
            <div class="toolbar-spacer"></div>
            <button
              class="toolbar-btn"
              :class="{ active: showPreview }"
              @click="showPreview = !showPreview"
            >
              {{ t('admin.articleEditor.preview') }}
            </button>
          </div>

          <!-- Content Area -->
          <div class="editor-content-area">
            <textarea
              v-show="!showPreview"
              id="content"
              v-model="form.content"
              :placeholder="t('admin.articleEditor.contentPlaceholder')"
              class="editor-textarea"
            ></textarea>
            <div
              v-show="showPreview"
              class="editor-preview article-content"
              v-html="previewContent"
            ></div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="editor-sidebar">
          <!-- Slug -->
          <div class="sidebar-section">
            <label>URL Slug</label>
            <input v-model="form.slug" type="text" class="sidebar-input" />
          </div>

          <!-- Excerpt -->
          <div class="sidebar-section">
            <label>{{ t('admin.articleEditor.excerptPlaceholder') }}</label>
            <textarea
              v-model="form.excerpt"
              class="sidebar-textarea"
              rows="3"
            ></textarea>
          </div>

          <!-- Category -->
          <div class="sidebar-section">
            <label>Category</label>
            <select v-model="form.category" class="sidebar-select">
              <option v-for="cat in categories" :key="cat.value" :value="cat.value">
                {{ cat.label }}
              </option>
            </select>
          </div>

          <!-- Tags -->
          <div class="sidebar-section">
            <label>Tags (comma separated)</label>
            <input
              v-model="form.tags"
              type="text"
              class="sidebar-input"
              placeholder="LLM, Claude, Agent"
            />
          </div>

          <!-- Status -->
          <div class="sidebar-section">
            <label>Status</label>
            <div class="status-indicator">
              <span
                class="status-badge"
                :class="`status-badge--${form.status}`"
              >
                {{ form.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.editor-page {
  padding: 40px 0;
  min-height: calc(100vh - 52px);
  background: var(--color-background-secondary);
  position: relative;
  z-index: 1;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.editor-header h1 {
  font-size: 24px;
  font-weight: 600;
}

.editor-actions {
  display: flex;
  gap: 12px;
}

.editor-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
}

@media (max-width: 900px) {
  .editor-grid {
    grid-template-columns: 1fr;
  }
}

.editor-main {
  background: var(--color-card);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.editor-title {
  width: 100%;
  padding: 24px;
  border: none;
  border-bottom: 1px solid var(--color-border);
  font-size: 28px;
  font-weight: 600;
  background: transparent;
  color: var(--color-text);
}

.editor-title:focus {
  outline: none;
}

.editor-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  padding: 12px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-background-secondary);
}

.toolbar-btn {
  padding: 8px 12px;
  border: none;
  background: transparent;
  color: var(--color-text);
  font-size: 14px;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: background 0.2s;
}

.toolbar-btn:hover {
  background: var(--color-border);
}

.toolbar-btn.active {
  background: var(--color-primary);
  color: white;
}

.toolbar-spacer {
  flex: 1;
}

.editor-content-area {
  min-height: 500px;
}

.editor-textarea {
  width: 100%;
  min-height: 500px;
  padding: 24px;
  border: none;
  font-family: 'SF Mono', SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 14px;
  line-height: 1.6;
  background: transparent;
  color: var(--color-text);
  resize: vertical;
}

.editor-textarea:focus {
  outline: none;
}

.editor-preview {
  padding: 24px;
  min-height: 500px;
  overflow-y: auto;
}

.editor-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-section {
  background: var(--color-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-sm);
}

.sidebar-section label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
}

.sidebar-input,
.sidebar-select,
.sidebar-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-background);
  color: var(--color-text);
  font-size: 14px;
}

.sidebar-input:focus,
.sidebar-select:focus,
.sidebar-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
}

.sidebar-textarea {
  resize: vertical;
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
</style>
