<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '@/lib/utils'

interface Props {
  class?: string
  modelValue?: string | number
  type?: string
  placeholder?: string
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const modelValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', String(value)),
})
</script>

<template>
  <input
    v-model="modelValue"
    :type="type"
    :placeholder="placeholder"
    :disabled="disabled"
    :class="cn(
      'flex w-full rounded-full border bg-[var(--color-background)] px-4 py-2.5 text-sm text-[var(--color-text)] border-[var(--color-border)] outline-none transition-all duration-200',
      'placeholder:text-[var(--color-text-tertiary)]',
      'focus:border-[var(--color-primary)] focus:ring-2 focus:ring-[var(--color-primary)]/20',
      'disabled:cursor-not-allowed disabled:opacity-50',
      props.class
    )"
  />
</template>
