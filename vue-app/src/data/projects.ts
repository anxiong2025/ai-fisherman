import type { Project } from '@/types'

export const projects: Project[] = [
  {
    id: '1',
    name: 'AI Chat Widget',
    description: 'A customizable AI chat widget that can be embedded in any website. Supports multiple LLM backends.',
    github: 'https://github.com/anxiong2025/ai-chat-widget',
    demo: 'https://ai-chat-widget.demo.com',
    stars: 1200,
    tags: ['TypeScript', 'React', 'LLM'],
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    id: '2',
    name: 'RAG Template',
    description: 'A production-ready RAG template with vector search, document processing, and chat interface.',
    github: 'https://github.com/anxiong2025/rag-template',
    stars: 890,
    tags: ['Python', 'FastAPI', 'Pinecone'],
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  {
    id: '3',
    name: 'Agent Framework',
    description: 'A lightweight framework for building AI agents with tool calling, memory, and planning capabilities.',
    github: 'https://github.com/anxiong2025/agent-framework',
    demo: 'https://agent-framework.demo.com',
    stars: 650,
    tags: ['Python', 'LangChain', 'Claude'],
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    id: '4',
    name: 'Prompt Library',
    description: 'A curated collection of high-quality prompts for various AI tasks and use cases.',
    github: 'https://github.com/anxiong2025/prompt-library',
    stars: 420,
    tags: ['Prompts', 'GPT', 'Claude'],
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  }
]

export function getFeaturedProjects(count = 3): Project[] {
  return projects.slice(0, count)
}
