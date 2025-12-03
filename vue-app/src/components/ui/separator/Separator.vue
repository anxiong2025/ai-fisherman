<script setup lang="ts">
import { Separator as SeparatorPrimitive, type SeparatorProps } from 'radix-vue'
import { cn } from '@/lib/utils'

interface Props extends SeparatorProps {
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  orientation: 'horizontal',
})
</script>

<template>
  <SeparatorPrimitive
    :class="cn(
      'shrink-0 bg-[var(--color-border)]',
      orientation === 'horizontal' ? 'h-px w-full' : 'h-full w-px',
      props.class
    )"
    v-bind="props"
  />
</template>
