<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useChatStore } from '@/stores'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { MessageCircle, X, Trash2, Send } from 'lucide-vue-next'

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

// Format message with markdown-like links
function formatMessage(content: string): string {
  return content.replace(
    /\[([^\]]+)\]\(([^)]+)\)/g,
    '<a href="$2" class="text-[var(--color-primary)] hover:underline">$1</a>'
  ).replace(/\n/g, '<br>')
}
</script>

<template>
  <div class="fixed bottom-6 right-6 z-[1500] max-[768px]:bottom-4 max-[768px]:right-4">
    <!-- Chat window -->
    <div
      class="absolute bottom-[70px] right-0 w-[360px] h-[480px] max-[768px]:w-[calc(100vw-32px)] max-[768px]:h-[70vh] max-[768px]:right-[-8px] bg-[var(--color-background)] border border-[var(--color-border)] rounded-[var(--radius-xl)] shadow-[var(--shadow-lg)] flex flex-col overflow-hidden transition-all duration-300 ease-out"
      :class="chatStore.isOpen ? 'scale-100 translate-y-0 opacity-100 visible' : 'scale-90 translate-y-5 opacity-0 invisible'"
    >
      <!-- Header -->
      <div class="px-4 py-4 bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white font-semibold flex justify-between items-center">
        <span>{{ t('chat.title') }}</span>
        <div class="flex gap-2">
          <button
            @click="chatStore.clear"
            :title="t('chat.clear')"
            class="w-7 h-7 rounded-full bg-white/20 flex items-center justify-center text-white hover:bg-white/30 transition-colors"
          >
            <Trash2 class="w-3.5 h-3.5" />
          </button>
          <button
            @click="chatStore.close"
            :title="t('chat.close')"
            class="w-7 h-7 rounded-full bg-white/20 flex items-center justify-center text-white hover:bg-white/30 transition-colors"
          >
            <X class="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      <!-- Messages -->
      <div class="flex-1 p-4 overflow-y-auto" ref="messagesContainer">
        <div
          v-for="message in chatStore.messages"
          :key="message.id"
          class="mb-3 flex"
          :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-[85%] px-3.5 py-2.5 rounded-2xl text-sm leading-[1.5]"
            :class="message.role === 'user'
              ? 'bg-[var(--color-primary)] text-white rounded-br-[4px]'
              : 'bg-[var(--color-background-secondary)] text-[var(--color-text)] rounded-bl-[4px]'"
            v-html="formatMessage(message.content)"
          ></div>
        </div>

        <!-- Typing indicator -->
        <div v-if="chatStore.isLoading" class="mb-3 flex justify-start">
          <div class="max-w-[85%] px-3.5 py-2.5 rounded-2xl rounded-bl-[4px] bg-[var(--color-background-secondary)]">
            <div class="flex gap-1">
              <span class="w-1.5 h-1.5 bg-[var(--color-text-secondary)] rounded-full animate-bounce [animation-delay:0ms]"></span>
              <span class="w-1.5 h-1.5 bg-[var(--color-text-secondary)] rounded-full animate-bounce [animation-delay:150ms]"></span>
              <span class="w-1.5 h-1.5 bg-[var(--color-text-secondary)] rounded-full animate-bounce [animation-delay:300ms]"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="px-4 py-3 border-t border-[var(--color-border)] flex gap-2">
        <Input
          v-model="inputMessage"
          :placeholder="t('chat.placeholder')"
          @keydown="handleKeydown"
          :disabled="chatStore.isLoading"
          class="flex-1"
        />
        <Button
          size="icon"
          @click="sendMessage"
          :disabled="chatStore.isLoading || !inputMessage.trim()"
          class="!w-10 !h-10 shrink-0"
        >
          <Send class="w-4 h-4" />
        </Button>
      </div>
    </div>

    <!-- Toggle button -->
    <button
      @click="chatStore.toggle"
      class="w-14 h-14 rounded-full bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white border-none shadow-[0_4px_16px_rgba(102,126,234,0.4)] cursor-pointer flex items-center justify-center transition-all duration-200 hover:scale-105 hover:shadow-[0_6px_20px_rgba(102,126,234,0.5)]"
    >
      <MessageCircle v-if="!chatStore.isOpen" class="w-6 h-6" />
      <X v-else class="w-6 h-6" />
    </button>
  </div>
</template>
