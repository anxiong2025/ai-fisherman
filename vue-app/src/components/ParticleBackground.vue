<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'

const containerRef = ref<HTMLDivElement>()

let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
let renderer: THREE.WebGLRenderer
let particleSystem: THREE.Points
let animationId: number
let mouseX = 0
let mouseY = 0
let time = 0

const PARTICLE_COUNT = 2000
const DEPTH = 3000

// Golden ratio - the mathematical constant of beauty
const PHI = (1 + Math.sqrt(5)) / 2
const GOLDEN_ANGLE = Math.PI * 2 / (PHI * PHI)

interface ParticleData {
  basePositions: Float32Array
  velocities: Float32Array
  spiralPhase: Float32Array
}

let particleData: ParticleData

function init() {
  if (!containerRef.value) return

  scene = new THREE.Scene()

  // Camera looking into the depth
  camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    1,
    DEPTH * 2
  )
  camera.position.z = 100

  renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true
  })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setClearColor(0x000000, 0)
  containerRef.value.appendChild(renderer.domElement)

  createGoldenSpiral()

  window.addEventListener('resize', onResize)
  window.addEventListener('mousemove', onMouseMove)

  animate()
}

function createGoldenSpiral() {
  const geometry = new THREE.BufferGeometry()
  const positions = new Float32Array(PARTICLE_COUNT * 3)
  const colors = new Float32Array(PARTICLE_COUNT * 3)
  const sizes = new Float32Array(PARTICLE_COUNT)
  const basePositions = new Float32Array(PARTICLE_COUNT * 3)
  const velocities = new Float32Array(PARTICLE_COUNT)
  const spiralPhase = new Float32Array(PARTICLE_COUNT)

  // Color palette inspired by cosmos and mathematics
  const colorPalette = [
    new THREE.Color('#60a5fa'), // Blue
    new THREE.Color('#34d399'), // Emerald
    new THREE.Color('#a78bfa'), // Purple
    new THREE.Color('#f472b6'), // Pink
    new THREE.Color('#fbbf24'), // Amber
    new THREE.Color('#22d3ee'), // Cyan
  ]

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const i3 = i * 3

    // Fibonacci/Golden spiral distribution
    // Each particle is placed at golden angle from previous
    const t = i / PARTICLE_COUNT
    const angle = i * GOLDEN_ANGLE

    // Radius grows with square root for even distribution (sunflower pattern)
    const radiusBase = Math.sqrt(i + 1) * 15
    const radius = radiusBase * (0.8 + Math.random() * 0.4)

    // Initial position - spread across depth
    const z = t * DEPTH * 0.8 + Math.random() * 200

    positions[i3] = Math.cos(angle) * radius
    positions[i3 + 1] = Math.sin(angle) * radius
    positions[i3 + 2] = z

    basePositions[i3] = positions[i3]!
    basePositions[i3 + 1] = positions[i3 + 1]!
    basePositions[i3 + 2] = z

    // Velocity - particles fly into the distance
    velocities[i] = 0.3 + Math.random() * 0.4

    // Phase for spiral animation
    spiralPhase[i] = angle

    // Color based on fibonacci position - creates beautiful patterns
    const fibIndex = Math.floor((i * PHI) % colorPalette.length)
    const color = colorPalette[fibIndex]!.clone()

    // Slight color variation
    color.offsetHSL(Math.random() * 0.05 - 0.025, 0, Math.random() * 0.1 - 0.05)

    colors[i3] = color.r
    colors[i3 + 1] = color.g
    colors[i3 + 2] = color.b

    // Size based on golden ratio sequence
    const fibSize = ((i % 8) + 1) / 8
    sizes[i] = 1 + fibSize * 3
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
  geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1))

  particleData = { basePositions, velocities, spiralPhase }

  const material = new THREE.ShaderMaterial({
    uniforms: {
      time: { value: 0 },
      pixelRatio: { value: renderer.getPixelRatio() }
    },
    vertexShader: `
      attribute float size;
      attribute vec3 color;
      varying vec3 vColor;
      varying float vAlpha;
      uniform float pixelRatio;
      uniform float time;

      void main() {
        vColor = color;

        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        float depth = -mvPosition.z;

        // Particles fade as they go into distance
        vAlpha = smoothstep(3000.0, 100.0, depth) * 0.9;

        // Size decreases with distance - strong perspective
        float perspective = 400.0 / max(depth, 50.0);
        gl_PointSize = size * pixelRatio * perspective;

        gl_Position = projectionMatrix * mvPosition;
      }
    `,
    fragmentShader: `
      varying vec3 vColor;
      varying float vAlpha;

      void main() {
        vec2 center = gl_PointCoord - vec2(0.5);
        float dist = length(center);

        if (dist > 0.5) discard;

        // Soft glowing particle
        float core = 1.0 - smoothstep(0.0, 0.15, dist);
        float glow = 1.0 - smoothstep(0.15, 0.5, dist);

        vec3 finalColor = vColor * (core * 1.5 + glow * 0.5);
        float alpha = (core * 0.9 + glow * 0.3) * vAlpha;

        gl_FragColor = vec4(finalColor, alpha);
      }
    `,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending
  })

  particleSystem = new THREE.Points(geometry, material)
  scene.add(particleSystem)
}

function animate() {
  animationId = requestAnimationFrame(animate)
  time += 0.006 // Slow, meditative pace

  const posAttr = particleSystem.geometry.attributes.position
  if (!posAttr) return

  const positions = posAttr.array as Float32Array
  const { basePositions, velocities, spiralPhase } = particleData

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const i3 = i * 3
    const vel = velocities[i] ?? 0.3
    const phase = spiralPhase[i] ?? 0

    // Move into the distance
    positions[i3 + 2] = (positions[i3 + 2] ?? 0) + vel

    // Gentle spiral rotation as particles travel
    const currentZ = positions[i3 + 2] ?? 0
    const spiralAmount = currentZ * 0.0003
    const baseX = basePositions[i3] ?? 0
    const baseY = basePositions[i3 + 1] ?? 0
    const radius = Math.sqrt(baseX * baseX + baseY * baseY)

    positions[i3] = Math.cos(phase + spiralAmount + time * 0.1) * radius
    positions[i3 + 1] = Math.sin(phase + spiralAmount + time * 0.1) * radius

    // Recycle particles that go too far
    if (currentZ > DEPTH) {
      positions[i3 + 2] = 50 + Math.random() * 100

      // New spiral position
      const newAngle = Math.random() * Math.PI * 2
      const newRadius = 50 + Math.random() * 400
      basePositions[i3] = Math.cos(newAngle) * newRadius
      basePositions[i3 + 1] = Math.sin(newAngle) * newRadius
      spiralPhase[i] = newAngle
    }
  }

  posAttr.needsUpdate = true

  // Gentle camera movement with mouse
  const targetX = mouseX * 80
  const targetY = mouseY * 50
  camera.position.x += (targetX - camera.position.x) * 0.015
  camera.position.y += (targetY - camera.position.y) * 0.015
  camera.lookAt(0, 0, DEPTH / 2)

  // Very subtle overall rotation - like looking into a vortex
  particleSystem.rotation.z = time * 0.02

  const material = particleSystem.material as THREE.ShaderMaterial
  if (material.uniforms.time) {
    material.uniforms.time.value = time
  }

  renderer.render(scene, camera)
}

function onResize() {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}

function onMouseMove(event: MouseEvent) {
  mouseX = (event.clientX / window.innerWidth) * 2 - 1
  mouseY = (event.clientY / window.innerHeight) * 2 - 1
}

function cleanup() {
  cancelAnimationFrame(animationId)
  window.removeEventListener('resize', onResize)
  window.removeEventListener('mousemove', onMouseMove)

  if (renderer) {
    renderer.dispose()
    containerRef.value?.removeChild(renderer.domElement)
  }
  if (particleSystem) {
    particleSystem.geometry.dispose()
    ;(particleSystem.material as THREE.Material).dispose()
  }
}

onMounted(init)
onUnmounted(cleanup)
</script>

<template>
  <div ref="containerRef" class="particle-background"></div>
</template>

<style scoped>
.particle-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
  background: var(--color-background);
}

.particle-background :deep(canvas) {
  display: block;
}
</style>
