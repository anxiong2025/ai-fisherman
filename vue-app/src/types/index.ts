// User types
export interface User {
  id: string
  name: string
  email: string
  avatar: string
  role: 'user' | 'admin'
  provider: 'github' | 'google'
}

// Article types
export interface Article {
  id: string
  slug: string
  title: string
  excerpt: string
  content: string
  category: 'ai-news' | 'agents' | 'tutorial' | 'tools' | string
  tags: string[]
  author: User | string
  // Support both old format (date/readTime) and new API format (created_at/read_time)
  date?: string
  readTime?: number
  created_at?: string
  read_time?: number
  gradient: string
  status: 'draft' | 'published'
  updated_at?: string
  published_at?: string | null
}

// Course types
export interface Course {
  id: string
  title: string
  subtitle: string
  description: string
  price: number
  originalPrice: number
  badge?: string
  gradient: string
  features: string[]
  curriculum: CourseSection[]
  instructor: Instructor
}

export interface CourseSection {
  title: string
  duration: string
  lessons: string[]
}

export interface Instructor {
  name: string
  avatar: string
  bio: string
}

// Project types
export interface Project {
  id: string
  name: string
  description: string
  github: string
  demo?: string
  stars: number
  tags: string[]
  gradient: string
}

// Chat types
export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: number
}

// Theme types
export type Theme = 'light' | 'dark' | 'system'

// Locale types
export type Locale = 'en' | 'zh'
