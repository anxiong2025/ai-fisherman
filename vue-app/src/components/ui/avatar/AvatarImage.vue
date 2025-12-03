<script setup lang="ts">
import { AvatarImage as AvatarImagePrimitive, type AvatarImageProps } from 'radix-vue'
import { cn } from '@/lib/utils'

interface Props extends AvatarImageProps {
  class?: string
}

const props = defineProps<Props>()
</script>

<template>
  <AvatarImagePrimitive
    :class="cn('aspect-square h-full w-full object-cover', props.class)"
    v-bind="props"
  />
</template>
