<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useChatStore } from '@/stores'

const { t } = useI18n()
const chatStore = useChatStore()

const inputMessage = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

// Send message
async function sendMessage() {
  if (!inputMessage.value.trim()) return

  await chatStore.sendMessage(inputMessage.value)
  inputMessage.value = ''

  // Scroll to bottom
  await nextTick()
  scrollToBottom()
}

// Handle enter key
function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

// Scroll to bottom of messages
function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Watch for new messages
watch(() => chatStore.messages.length, () => {
  nextTick(() => scrollToBottom())
})

// Add welcome message on first open
watch(() => chatStore.isOpen, (isOpen) => {
  if (isOpen && chatStore.messages.length === 0) {
    chatStore.addMessage('assistant', t('chat.welcome'))
  }
})
</script>

<template>
  <div class="ai-chat-widget">
    <!-- Chat window -->
    <div class="ai-chat-window" :class="{ open: chatStore.isOpen }">
      <!-- Header -->
      <div class="ai-chat-header">
        <span>{{ t('chat.title') }}</span>
        <div class="ai-chat-header-actions">
          <button @click="chatStore.clear" :title="t('chat.clear')">🗑️</button>
          <button @click="chatStore.close" :title="t('chat.close')">✕</button>
        </div>
      </div>

      <!-- Messages -->
      <div class="ai-chat-messages" ref="messagesContainer">
        <div
          v-for="message in chatStore.messages"
          :key="message.id"
          class="ai-message"
          :class="message.role"
        >
          <div class="ai-message-content" v-html="formatMessage(message.content)"></div>
        </div>

        <!-- Typing indicator -->
        <div v-if="chatStore.isLoading" class="ai-message assistant">
          <div class="ai-message-content">
            <div class="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="ai-chat-input">
        <input
          v-model="inputMessage"
          :placeholder="t('chat.placeholder')"
          @keydown="handleKeydown"
          :disabled="chatStore.isLoading"
        />
        <button
          class="ai-send-btn"
          @click="sendMessage"
          :disabled="chatStore.isLoading || !inputMessage.trim()"
        >
          ➤
        </button>
      </div>
    </div>

    <!-- Toggle button -->
    <button class="ai-chat-toggle" @click="chatStore.toggle">
      <span v-if="!chatStore.isOpen">💬</span>
      <span v-else>✕</span>
    </button>
  </div>
</template>

<script lang="ts">
// Format message with markdown-like links
function formatMessage(content: string): string {
  // Convert [text](url) to <a> tags
  return content.replace(
    /\[([^\]]+)\]\(([^)]+)\)/g,
    '<a href="$2">$1</a>'
  ).replace(/\n/g, '<br>')
}
</script>
