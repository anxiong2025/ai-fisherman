<script setup lang="ts">
import { type VariantProps, cva } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'inline-flex items-center rounded-full px-3 py-1 text-xs font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-[var(--color-primary-light)] text-[var(--color-primary)]',
        secondary: 'bg-[var(--color-background-secondary)] text-[var(--color-text-secondary)]',
        success: 'bg-[var(--color-success)]/10 text-[var(--color-success)]',
        warning: 'bg-[var(--color-warning)]/10 text-[var(--color-warning)]',
        danger: 'bg-[var(--color-danger)]/10 text-[var(--color-danger)]',
        outline: 'border border-[var(--color-border)] text-[var(--color-text)]',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
)

type BadgeVariants = VariantProps<typeof badgeVariants>

interface Props {
  variant?: BadgeVariants['variant']
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
})
</script>

<template>
  <span :class="cn(badgeVariants({ variant }), props.class)">
    <slot />
  </span>
</template>
