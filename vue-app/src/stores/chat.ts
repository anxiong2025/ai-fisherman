import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ChatMessage } from '@/types'

const API_BASE = '/api'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([])
  const isOpen = ref(false)
  const isLoading = ref(false)

  // Toggle chat window
  function toggle() {
    isOpen.value = !isOpen.value
  }

  // Close chat
  function close() {
    isOpen.value = false
  }

  // Clear messages
  function clear() {
    messages.value = []
  }

  // Add message
  function addMessage(role: 'user' | 'assistant', content: string) {
    messages.value.push({
      id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      role,
      content,
      timestamp: Date.now()
    })
  }

  // Send message
  async function sendMessage(content: string) {
    if (!content.trim() || isLoading.value) return

    // Add user message
    addMessage('user', content.trim())
    isLoading.value = true

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: content,
          history: messages.value.slice(-10) // Send last 10 messages for context
        })
      })

      if (response.ok) {
        const data = await response.json()
        addMessage('assistant', data.response)
      } else {
        throw new Error('API error')
      }
    } catch {
      // Fallback to mock response in dev mode
      const mockReply = getMockReply(content)
      addMessage('assistant', mockReply)
    } finally {
      isLoading.value = false
    }
  }

  // Mock reply for development
  function getMockReply(question: string): string {
    const q = question.toLowerCase()

    // Article related
    if (q.includes('agent') || q.includes('代理')) {
      return 'We have several articles about AI Agents! Check out "Building Your First AI Agent" which covers the core concepts. You can also explore the Multi-Agent System Architecture article for advanced patterns. [View Articles](/articles?category=agents)'
    }

    if (q.includes('rag') || q.includes('知识库')) {
      return 'RAG (Retrieval Augmented Generation) is a powerful technique! We have a comprehensive article "RAG System in Practice: Building a Smart Knowledge Base" that covers implementation details. [Read Article](/articles/rag-implementation)'
    }

    if (q.includes('claude') || q.includes('api')) {
      return 'Looking for Claude API information? Check out our "Complete Claude API Guide" which covers authentication, best practices, and optimization techniques. [Read Guide](/articles/claude-api-guide)'
    }

    if (q.includes('prompt') || q.includes('提示词')) {
      return 'Prompt engineering is crucial for getting good results from LLMs. Our article "Prompt Engineering: Making AI Understand You Better" covers essential techniques. [Learn More](/articles/prompt-engineering)'
    }

    // Course related
    if (q.includes('course') || q.includes('课程') || q.includes('learn') || q.includes('学习')) {
      return 'We offer two main courses:\n\n1. **AI Agent Development Bootcamp** - Learn to build intelligent agents from scratch\n2. **RAG Practical Course** - Master retrieval-augmented generation\n\nBoth include hands-on projects and community support. [View Courses](/courses)'
    }

    // Project related
    if (q.includes('project') || q.includes('项目') || q.includes('github') || q.includes('开源')) {
      return 'We have several open source projects including AI Chat Widget, RAG Template, and Agent Framework. All are available on GitHub with detailed documentation. [View Projects](/projects)'
    }

    // Contact/about
    if (q.includes('contact') || q.includes('联系') || q.includes('about') || q.includes('关于')) {
      return 'You can learn more about me on the About page. For business inquiries, please email contact@example.com. [About Me](/about)'
    }

    // Default response
    return "I can help you find information about our articles, courses, and projects. Feel free to ask about:\n\n- AI Agent development\n- RAG systems\n- LLM APIs (Claude, GPT)\n- Prompt engineering\n- Our courses and learning paths\n\nWhat would you like to know?"
  }

  return {
    messages,
    isOpen,
    isLoading,
    toggle,
    close,
    clear,
    sendMessage,
    addMessage
  }
})
