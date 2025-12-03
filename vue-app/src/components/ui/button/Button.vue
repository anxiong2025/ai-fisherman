<script setup lang="ts">
import { computed } from 'vue'
import { Primitive, type PrimitiveProps } from 'radix-vue'
import { type VariantProps, cva } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap text-base font-normal transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 cursor-pointer',
  {
    variants: {
      variant: {
        default: 'bg-[var(--color-primary)] text-white hover:bg-[var(--color-primary-hover)] active:scale-[0.98]',
        secondary: 'bg-transparent text-[var(--color-primary)] hover:underline',
        outline: 'border border-[var(--color-primary)] bg-transparent text-[var(--color-primary)] hover:bg-[var(--color-primary)] hover:text-white',
        ghost: 'bg-black/5 text-[var(--color-text)] hover:bg-black/10 dark:bg-white/10 dark:hover:bg-white/15',
        link: 'text-[var(--color-primary)] underline-offset-4 hover:underline',
        danger: 'bg-[var(--color-danger)] text-white hover:bg-[var(--color-danger)]/90',
      },
      size: {
        default: 'px-6 py-3 rounded-full',
        sm: 'px-4 py-2 text-sm rounded-full',
        lg: 'px-8 py-4 text-base rounded-full',
        icon: 'h-10 w-10 rounded-full p-0',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

type ButtonVariants = VariantProps<typeof buttonVariants>

interface Props extends PrimitiveProps {
  variant?: ButtonVariants['variant']
  size?: ButtonVariants['size']
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  as: 'button',
  variant: 'default',
  size: 'default',
})

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props
  return delegated
})
</script>

<template>
  <Primitive
    v-bind="delegatedProps"
    :class="cn(buttonVariants({ variant, size }), props.class)"
  >
    <slot />
  </Primitive>
</template>
