<script setup lang="ts">
import { cn } from '@/lib/utils'

interface Props {
  class?: string
}

const props = defineProps<Props>()
</script>

<template>
  <h3
    :class="cn(
      'text-[21px] font-semibold leading-[1.19] tracking-[0.011em] text-[var(--color-text)]',
      props.class
    )"
  >
    <slot />
  </h3>
</template>
