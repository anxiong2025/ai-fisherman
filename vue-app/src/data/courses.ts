import type { Course } from '@/types'

export const courses: Course[] = [
  {
    id: 'agent-bootcamp',
    title: 'AI Agent Development Bootcamp',
    subtitle: 'Master AI Agent design, development and deployment from scratch',
    description: 'AI Agent is one of the most promising directions in AI. This course takes you from basic concepts to Agent architecture design, tool development, memory systems, multi-agent collaboration, and ultimately completing a full AI Agent project.',
    price: 2999,
    originalPrice: 4999,
    badge: 'Popular',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    features: [
      '40+ hours of video content',
      '8 hands-on projects',
      'Lifetime access',
      'Community support',
      'Certificate of completion'
    ],
    curriculum: [
      {
        title: 'Module 1: Agent Fundamentals',
        duration: '6 hours',
        lessons: [
          'What is an AI Agent?',
          'LLM fundamentals for Agents',
          'The ReAct pattern',
          'Setting up your environment'
        ]
      },
      {
        title: 'Module 2: Tool Development',
        duration: '8 hours',
        lessons: [
          'Designing effective tools',
          'Building custom tools',
          'Tool orchestration',
          'Error handling patterns'
        ]
      },
      {
        title: 'Module 3: Memory Systems',
        duration: '6 hours',
        lessons: [
          'Short-term memory',
          'Long-term memory with vectors',
          'Conversation management',
          'Memory optimization'
        ]
      },
      {
        title: 'Module 4: Multi-Agent Systems',
        duration: '10 hours',
        lessons: [
          'Agent communication patterns',
          'Task decomposition',
          'Coordination strategies',
          'Building an agent team'
        ]
      }
    ],
    instructor: {
      name: 'Robert',
      avatar: '👨‍💻',
      bio: '8 years of software development experience, 3 years focused on AI application development. Led AI projects at multiple tech companies, author of several open source projects with 3000+ GitHub stars.'
    }
  },
  {
    id: 'rag-course',
    title: 'RAG Practical Course',
    subtitle: 'Build production-ready RAG systems from scratch',
    description: 'RAG (Retrieval-Augmented Generation) is a key technique for building AI applications with private knowledge. This course covers document processing, vector databases, retrieval strategies, and production deployment.',
    price: 1999,
    originalPrice: 3999,
    badge: 'New',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    features: [
      '25+ hours of video content',
      '5 hands-on projects',
      'Lifetime access',
      'Community support',
      'Certificate of completion'
    ],
    curriculum: [
      {
        title: 'Module 1: RAG Fundamentals',
        duration: '4 hours',
        lessons: [
          'Introduction to RAG',
          'Document processing',
          'Chunking strategies',
          'Embedding models'
        ]
      },
      {
        title: 'Module 2: Vector Databases',
        duration: '6 hours',
        lessons: [
          'Vector database fundamentals',
          'Pinecone deep dive',
          'Self-hosted options',
          'Performance optimization'
        ]
      },
      {
        title: 'Module 3: Retrieval Strategies',
        duration: '8 hours',
        lessons: [
          'Semantic search',
          'Hybrid search',
          'Re-ranking',
          'Query transformation'
        ]
      },
      {
        title: 'Module 4: Production Deployment',
        duration: '7 hours',
        lessons: [
          'System architecture',
          'Scaling strategies',
          'Monitoring & evaluation',
          'Cost optimization'
        ]
      }
    ],
    instructor: {
      name: 'Robert',
      avatar: '👨‍💻',
      bio: '8 years of software development experience, 3 years focused on AI application development. Led AI projects at multiple tech companies, author of several open source projects with 3000+ GitHub stars.'
    }
  }
]

export function getCourseById(id: string): Course | undefined {
  return courses.find(c => c.id === id)
}
