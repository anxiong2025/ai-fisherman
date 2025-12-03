<script setup lang="ts">
import { cn } from '@/lib/utils'

interface Props {
  class?: string
}

const props = defineProps<Props>()
</script>

<template>
  <p :class="cn('text-sm text-[var(--color-text-secondary)] leading-[1.43]', props.class)">
    <slot />
  </p>
</template>
