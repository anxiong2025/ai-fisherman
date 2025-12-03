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
      'rounded-[var(--radius-lg)] bg-[var(--color-card)] shadow-[var(--shadow-sm)] transition-all duration-300 ease-[cubic-bezier(0.25,0.46,0.45,0.94)] hover:shadow-[var(--shadow-md)] hover:-translate-y-1',
      props.class
    )"
  >
    <slot />
  </div>
</template>
