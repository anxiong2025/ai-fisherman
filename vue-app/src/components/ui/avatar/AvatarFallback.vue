<script setup lang="ts">
import { AvatarFallback as AvatarFallbackPrimitive, type AvatarFallbackProps } from 'radix-vue'
import { cn } from '@/lib/utils'

interface Props extends AvatarFallbackProps {
  class?: string
}

const props = defineProps<Props>()
</script>

<template>
  <AvatarFallbackPrimitive
    :class="cn(
      'flex h-full w-full items-center justify-center rounded-full bg-[var(--color-background-secondary)] text-[var(--color-text-secondary)]',
      props.class
    )"
    v-bind="props"
  >
    <slot />
  </AvatarFallbackPrimitive>
</template>
