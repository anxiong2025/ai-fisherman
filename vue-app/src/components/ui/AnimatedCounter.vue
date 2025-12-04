<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'

const props = defineProps<{
  value: number
  duration?: number
  delay?: number
  format?: (val: number) => string
}>()

const displayValue = ref(0)
const duration = props.duration || 1000
const delay = props.delay || 0

// Check if the target value is an integer
const isInteger = computed(() => Number.isInteger(props.value))

function animate(start: number, end: number) {
  const startTime = performance.now()
  let lastUpdate = 0
  const frameDuration = 1000 / 30 // Limit to 30fps for readability

  function easeOutExpo(t: number): number {
    return t === 1 ? 1 : 1 - Math.pow(2, -10 * t)
  }

  function update(currentTime: number) {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)

    // Only update display value if enough time has passed or if it's the final frame
    if (currentTime - lastUpdate >= frameDuration || progress === 1) {
      const easedProgress = easeOutExpo(progress)
      let current = start + (end - start) * easedProgress
      // Round to integer if target value is an integer
      if (isInteger.value) {
        current = Math.round(current)
      }
      displayValue.value = current
      lastUpdate = currentTime
    }

    if (progress < 1) {
      requestAnimationFrame(update)
    } else {
      displayValue.value = end
    }
  }

  requestAnimationFrame(update)
}

onMounted(() => {
  if (delay > 0) {
    setTimeout(() => animate(0, props.value), delay)
  } else {
    animate(0, props.value)
  }
})

watch(() => props.value, (newVal, oldVal) => {
  animate(oldVal || 0, newVal)
})

function formatValue(val: number) {
  if (props.format) {
    return props.format(val)
  }
  return Math.round(val).toLocaleString()
}
</script>

<template>
  <span>{{ formatValue(displayValue) }}</span>
</template>
