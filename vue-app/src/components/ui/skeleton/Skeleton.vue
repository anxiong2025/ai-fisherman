<script setup lang="ts">
import { cn } from '@/lib/utils'

interface Props {
  class?: string
}

const props = defineProps<Props>()
</script>

<template>
  <div
    :class="cn(
      'animate-pulse rounded-[var(--radius-md)] bg-[var(--color-background-secondary)]',
      props.class
    )"
  />
</template>
