import type { Article } from '@/types'

export const articles: Article[] = [
  {
    id: '1',
    slug: 'building-ai-agents',
    title: 'Building Your First AI Agent',
    excerpt: 'Learn the core concepts of AI Agents and build an intelligent assistant with autonomous decision-making capabilities.',
    content: '',
    category: 'agents',
    tags: ['Agent', 'LangChain', 'Claude'],
    author: 'Robert',
    date: '2024-12-01',
    readTime: 10,
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    status: 'published'
  },
  {
    id: '2',
    slug: 'claude-api-guide',
    title: 'Complete Claude API Guide',
    excerpt: 'A comprehensive guide to using the Anthropic Claude API, including best practices and optimization techniques.',
    content: '',
    category: 'ai-news',
    tags: ['Claude', 'API', 'LLM'],
    author: 'Robert',
    date: '2024-11-28',
    readTime: 15,
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    status: 'published'
  },
  {
    id: '3',
    slug: 'rag-implementation',
    title: 'RAG System in Practice: Building a Smart Knowledge Base',
    excerpt: 'Learn how to use RAG technology to build an enterprise-grade knowledge base system.',
    content: '',
    category: 'agents',
    tags: ['RAG', 'Vector Database', 'LangChain'],
    author: 'Robert',
    date: '2024-11-25',
    readTime: 12,
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    status: 'published'
  },
  {
    id: '4',
    slug: 'prompt-engineering',
    title: 'Prompt Engineering: Making AI Understand You',
    excerpt: 'Master the core techniques of prompt design to write high-quality prompts for better AI outputs.',
    content: '',
    category: 'tutorial',
    tags: ['Prompt', 'LLM', 'GPT'],
    author: 'Robert',
    date: '2024-11-22',
    readTime: 8,
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    status: 'published'
  },
  {
    id: '5',
    slug: 'gpt-4-turbo',
    title: 'GPT-4 Turbo Deep Dive',
    excerpt: "What improvements does OpenAI's latest GPT-4 Turbo bring? A comprehensive comparison of the new and old versions.",
    content: '',
    category: 'ai-news',
    tags: ['GPT', 'OpenAI', 'LLM'],
    author: 'Robert',
    date: '2024-11-20',
    readTime: 10,
    gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    status: 'published'
  },
  {
    id: '6',
    slug: 'vector-database',
    title: 'Vector Database Selection Guide',
    excerpt: 'Compare Pinecone, Weaviate, Milvus and other popular vector databases to help you choose the right solution.',
    content: '',
    category: 'tools',
    tags: ['Vector Database', 'Pinecone', 'RAG'],
    author: 'Robert',
    date: '2024-11-18',
    readTime: 14,
    gradient: 'linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)',
    status: 'published'
  },
  {
    id: '7',
    slug: 'multi-agent-system',
    title: 'Multi-Agent System Architecture',
    excerpt: 'Explore design patterns for multi-agent collaboration and learn how to build complex AI systems.',
    content: '',
    category: 'agents',
    tags: ['Agent', 'Multi-Agent', 'AutoGPT'],
    author: 'Robert',
    date: '2024-11-15',
    readTime: 18,
    gradient: 'linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%)',
    status: 'published'
  },
  {
    id: '8',
    slug: 'langchain-tutorial',
    title: 'LangChain: From Beginner to Expert',
    excerpt: 'A complete guide to LangChain framework from basic concepts to advanced usage and best practices.',
    content: '',
    category: 'tutorial',
    tags: ['LangChain', 'Python', 'Agent'],
    author: 'Robert',
    date: '2024-11-12',
    readTime: 20,
    gradient: 'linear-gradient(135deg, #f6d365 0%, #fda085 100%)',
    status: 'published'
  }
]

// Get article by slug
export function getArticleBySlug(slug: string): Article | undefined {
  return articles.find(a => a.slug === slug)
}

// Get articles by category
export function getArticlesByCategory(category: string): Article[] {
  if (category === 'all') return articles
  return articles.filter(a => a.category === category)
}

// Get articles by tag
export function getArticlesByTag(tag: string): Article[] {
  return articles.filter(a => a.tags.includes(tag))
}

// Get featured articles
export function getFeaturedArticles(count = 3): Article[] {
  return articles.slice(0, count)
}
