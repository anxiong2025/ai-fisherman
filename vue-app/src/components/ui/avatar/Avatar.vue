<script setup lang="ts">
import { AvatarRoot, type AvatarRootProps } from 'radix-vue'
import { cn } from '@/lib/utils'

interface Props extends AvatarRootProps {
  class?: string
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
})

const sizeClasses = {
  sm: 'h-8 w-8',
  md: 'h-10 w-10',
  lg: 'h-12 w-12',
}
</script>

<template>
  <AvatarRoot
    :class="cn(
      'relative flex shrink-0 overflow-hidden rounded-full',
      sizeClasses[size],
      props.class
    )"
  >
    <slot />
  </AvatarRoot>
</template>
