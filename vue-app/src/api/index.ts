const API_BASE = import.meta.env.VITE_API_BASE || '/api'

interface RequestOptions extends RequestInit {
  token?: string
}

async function request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { token, ...fetchOptions } = options

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  }

  if (token) {
    ;(headers as Record<string, string>)['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...fetchOptions,
    headers,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(error.detail || `HTTP ${response.status}`)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}

// ============== Auth API ==============

export const authApi = {
  verify(token: string) {
    return request<{ valid: boolean; user: User | null }>('/auth/verify', { token })
  },

  getMe(token: string) {
    return request<User>('/auth/me', { token })
  },
}

// ============== Articles API ==============

export interface Article {
  id: string
  slug: string
  title: string
  excerpt: string
  content: string
  category: string
  tags: string[]
  status: 'draft' | 'published'
  read_time: number
  gradient: string
  author: User
  created_at: string
  updated_at: string
  published_at: string | null
}

export interface ArticleListResponse {
  items: Article[]
  total: number
  page: number
  page_size: number
}

export interface ArticleCreate {
  title: string
  slug: string
  excerpt: string
  content: string
  category: string
  tags: string[]
  status: 'draft' | 'published'
  gradient?: string
}

export interface ArticleUpdate {
  title?: string
  slug?: string
  excerpt?: string
  content?: string
  category?: string
  tags?: string[]
  status?: 'draft' | 'published'
  gradient?: string
}

export interface User {
  id: string
  email: string
  name: string
  avatar: string | null
  role: 'user' | 'admin'
  provider: 'github' | 'google'
}

export const articlesApi = {
  list(params: {
    page?: number
    page_size?: number
    category?: string
    tag?: string
    status?: string
    token?: string
  } = {}) {
    const { token, ...query } = params
    const searchParams = new URLSearchParams()

    Object.entries(query).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.set(key, String(value))
      }
    })

    const queryString = searchParams.toString()
    return request<ArticleListResponse>(
      `/articles${queryString ? `?${queryString}` : ''}`,
      { token }
    )
  },

  get(slug: string, token?: string) {
    return request<Article>(`/articles/${slug}`, { token })
  },

  create(data: ArticleCreate, token: string) {
    return request<Article>('/articles', {
      method: 'POST',
      body: JSON.stringify(data),
      token,
    })
  },

  update(id: string, data: ArticleUpdate, token: string) {
    return request<Article>(`/articles/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
      token,
    })
  },

  delete(id: string, token: string) {
    return request<void>(`/articles/${id}`, {
      method: 'DELETE',
      token,
    })
  },
}

// ============== Search API ==============

export interface SearchResult {
  title: string
  content: string
  url: string
  score: number
}

export interface SearchResponse {
  results: SearchResult[]
  query: string
}

export const searchApi = {
  search(query: string, limit = 5) {
    return request<SearchResponse>('/search', {
      method: 'POST',
      body: JSON.stringify({ query, limit }),
    })
  },
}

// ============== Chat API ==============

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface ChatResponse {
  response: string
  sources: { title: string; url: string; score: number }[]
}

export const chatApi = {
  chat(message: string, history: ChatMessage[] = []) {
    return request<ChatResponse>('/chat', {
      method: 'POST',
      body: JSON.stringify({ message, history }),
    })
  },

  async *chatStream(message: string, history: ChatMessage[] = []) {
    const response = await fetch(`${API_BASE}/chat/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history }),
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const reader = response.body?.getReader()
    if (!reader) throw new Error('No reader')

    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value)
      const lines = chunk.split('\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          if (data === '[DONE]') return
          yield JSON.parse(data)
        }
      }
    }
  },
}
