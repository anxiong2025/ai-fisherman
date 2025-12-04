<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'

const containerRef = ref<HTMLDivElement>()

let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
let renderer: THREE.WebGLRenderer
let animationId: number

// Scene objects
let starMesh: THREE.Points
let sun: THREE.Mesh
let planets: {
  mesh: THREE.Mesh
  distance: number
  angle: number
  speed: number
  selfRotationSpeed: number
  centerX: number
  centerZ: number
}[] = []

// Collision effect
let collisionParticles: THREE.Points | null = null
let collisionGlow: THREE.Mesh | null = null
let collisionPlanetMeshes: THREE.Mesh[] = []
let collisionTime = 0
let collisionPosition = new THREE.Vector3()

// Black hole effect
let blackHoleCore: THREE.Mesh | null = null
let accretionDisk: THREE.Points | null = null
let gaseousRing: THREE.Mesh | null = null
let jets: THREE.Points | null = null
let infallParticles: THREE.Points | null = null
let blackHolePosition = new THREE.Vector3()

// Mouse interaction
let mouseX = 0
let mouseY = 0

// Planet colors
const PLANET_COLORS = [
  0x34d399, // Emerald
  0xf472b6, // Pink
  0x60a5fa, // Blue
  0xfbbf24, // Amber
  0xa78bfa, // Purple
]

function createNoiseTexture() {
  const canvas = document.createElement('canvas')
  canvas.width = 512
  canvas.height = 512
  const ctx = canvas.getContext('2d')!
  
  // Fill background
  ctx.fillStyle = '#000000'
  ctx.fillRect(0, 0, 512, 512)
  
  // Draw noise clouds
  for (let i = 0; i < 200; i++) {
    const x = Math.random() * 512
    const y = Math.random() * 512
    const radius = 20 + Math.random() * 60
    const opacity = 0.05 + Math.random() * 0.1
    
    const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius)
    gradient.addColorStop(0, `rgba(255, 255, 255, ${opacity})`)
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)')
    
    ctx.fillStyle = gradient
    ctx.beginPath()
    ctx.arc(x, y, radius, 0, Math.PI * 2)
    ctx.fill()
  }
  
  // Add swirl lines
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)'
  ctx.lineWidth = 2
  for (let i = 0; i < 50; i++) {
    ctx.beginPath()
    const x = Math.random() * 512
    const y = Math.random() * 512
    ctx.moveTo(x, y)
    ctx.bezierCurveTo(
      x + Math.random() * 100 - 50, y + Math.random() * 100 - 50,
      x + Math.random() * 100 - 50, y + Math.random() * 100 - 50,
      x + Math.random() * 100 - 50, y + Math.random() * 100 - 50
    )
    ctx.stroke()
  }

  const texture = new THREE.CanvasTexture(canvas)
  texture.wrapS = THREE.RepeatWrapping
  texture.wrapT = THREE.RepeatWrapping
  return texture
}

function init() {
  if (!containerRef.value) return

  // 1. Create scene
  scene = new THREE.Scene()
  scene.fog = new THREE.FogExp2(0x050510, 0.0006)

  // 2. Create camera - 3D perspective view from above
  camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    2000
  )
  camera.position.set(0, 50, 100)
  camera.lookAt(0, 0, 0)

  // 3. Create renderer
  renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true
  })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  containerRef.value.appendChild(renderer.domElement)

  // 4. Lighting
  const ambientLight = new THREE.AmbientLight(0x333344)
  scene.add(ambientLight)

  // 5. Create scene objects
  createStarfield()
  createSun()
  createSolarSystem()
  createDistantCollision()
  createBlackHole()

  // 6. Event listeners
  window.addEventListener('resize', onResize)
  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('touchmove', onTouchMove, { passive: true })

  animate()
}

function createStarfield() {
  const geometry = new THREE.BufferGeometry()
  const vertices: number[] = []
  const colors: number[] = []

  const colorOptions = [
    new THREE.Color(0xffffff),
    new THREE.Color(0xa78bfa),
    new THREE.Color(0x60a5fa),
  ]

  // Generate 3000 stars
  for (let i = 0; i < 3000; i++) {
    const x = (Math.random() - 0.5) * 600
    const y = (Math.random() - 0.5) * 600
    const z = (Math.random() - 0.5) * 300
    vertices.push(x, y, z)

    const color = colorOptions[Math.floor(Math.random() * colorOptions.length)]!
    colors.push(color.r, color.g, color.b)
  }

  geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3))
  geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3))

  const material = new THREE.PointsMaterial({
    size: 0.5,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    sizeAttenuation: true
  })

  starMesh = new THREE.Points(geometry, material)
  scene.add(starMesh)
}

function createSun() {
  // Move sun to bottom-left corner, smaller and subtler
  const geometry = new THREE.SphereGeometry(3, 32, 32)
  const material = new THREE.MeshBasicMaterial({
    color: 0x667eea
  })
  sun = new THREE.Mesh(geometry, material)
  sun.position.set(-80, -20, -50) // Moved to corner

  // Subtle glow
  const glowGeo = new THREE.SphereGeometry(5, 32, 32)
  const glowMat = new THREE.MeshBasicMaterial({
    color: 0x764ba2,
    transparent: true,
    opacity: 0.2,
    side: THREE.BackSide
  })
  const glow = new THREE.Mesh(glowGeo, glowMat)
  sun.add(glow)

  // Point light from sun position
  const sunLight = new THREE.PointLight(0x667eea, 0.8, 200)
  sun.add(sunLight)

  scene.add(sun)
}

function createSolarSystem() {
  planets = []

  // Create planets with offset centers (not in the middle)
  const planetConfigs = [
    { distance: 25, centerX: -60, centerZ: 20, speed: 0.002 },
    { distance: 18, centerX: 70, centerZ: -30, speed: 0.0025 },
    { distance: 30, centerX: 50, centerZ: 40, speed: 0.0015 },
    { distance: 22, centerX: -40, centerZ: -50, speed: 0.003 },
    { distance: 35, centerX: 0, centerZ: -60, speed: 0.001 },
  ]

  planetConfigs.forEach((config, i) => {
    const size = Math.random() * 1.8 + 1
    const color = PLANET_COLORS[i]!

    // Create orbit ring (offset from center)
    const orbitGeometry = new THREE.BufferGeometry()
    const orbitPoints: number[] = []
    const segments = 128

    for (let j = 0; j <= segments; j++) {
      const angle = (j / segments) * Math.PI * 2
      orbitPoints.push(
        config.centerX + Math.cos(angle) * config.distance,
        0,
        config.centerZ + Math.sin(angle) * config.distance
      )
    }

    orbitGeometry.setAttribute('position', new THREE.Float32BufferAttribute(orbitPoints, 3))

    const orbitMaterial = new THREE.LineBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.06
    })
    const orbit = new THREE.LineLoop(orbitGeometry, orbitMaterial)
    scene.add(orbit)

    // Create planet
    const planetGeo = new THREE.SphereGeometry(size, 32, 32)
    const planetMat = new THREE.MeshPhongMaterial({
      color: color,
      shininess: 30,
      emissive: color,
      emissiveIntensity: 0.15
    })
    const planet = new THREE.Mesh(planetGeo, planetMat)

    // Add subtle glow
    const planetGlowGeo = new THREE.SphereGeometry(size * 1.4, 32, 32)
    const planetGlowMat = new THREE.MeshBasicMaterial({
      color: color,
      transparent: true,
      opacity: 0.1,
      side: THREE.BackSide
    })
    const planetGlow = new THREE.Mesh(planetGlowGeo, planetGlowMat)
    planet.add(planetGlow)

    scene.add(planet)

    planets.push({
      mesh: planet,
      distance: config.distance,
      angle: Math.random() * Math.PI * 2,
      speed: config.speed,
      selfRotationSpeed: Math.random() * 0.02 + 0.005,
      centerX: config.centerX,
      centerZ: config.centerZ
    })
  })
}

function createDistantCollision() {
  // Create two colliding planets in the distance
  collisionPosition.set(120, 30, -100)

  // Collision particles (debris)
  const particleCount = 200
  const geometry = new THREE.BufferGeometry()
  const positions = new Float32Array(particleCount * 3)
  const colors = new Float32Array(particleCount * 3)
  const velocities: THREE.Vector3[] = []

  const debrisColors = [
    new THREE.Color(0xff6b6b), // Red
    new THREE.Color(0xffa502), // Orange
    new THREE.Color(0xffeaa7), // Yellow
    new THREE.Color(0xdfe6e9), // White
  ]

  for (let i = 0; i < particleCount; i++) {
    const i3 = i * 3
    positions[i3] = collisionPosition.x
    positions[i3 + 1] = collisionPosition.y
    positions[i3 + 2] = collisionPosition.z

    const color = debrisColors[Math.floor(Math.random() * debrisColors.length)]!
    colors[i3] = color.r
    colors[i3 + 1] = color.g
    colors[i3 + 2] = color.b

    // Random velocity for explosion
    velocities.push(new THREE.Vector3(
      (Math.random() - 0.5) * 2,
      (Math.random() - 0.5) * 2,
      (Math.random() - 0.5) * 2
    ))
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))

  const material = new THREE.PointsMaterial({
    size: 1.5,
    vertexColors: true,
    transparent: true,
    opacity: 0,
    sizeAttenuation: true
  })

  collisionParticles = new THREE.Points(geometry, material)
  collisionParticles.userData.velocities = velocities
  scene.add(collisionParticles)

  // Create two approaching planets
  const planet1Geo = new THREE.SphereGeometry(4, 32, 32)
  const planet1Mat = new THREE.MeshBasicMaterial({ color: 0xff6b6b })
  const planet1 = new THREE.Mesh(planet1Geo, planet1Mat)
  planet1.position.copy(collisionPosition).add(new THREE.Vector3(-15, 0, 0))
  planet1.userData.startOffset = -15
  scene.add(planet1)

  const planet2Geo = new THREE.SphereGeometry(3, 32, 32)
  const planet2Mat = new THREE.MeshBasicMaterial({ color: 0xffa502 })
  const planet2 = new THREE.Mesh(planet2Geo, planet2Mat)
  planet2.position.copy(collisionPosition).add(new THREE.Vector3(12, 0, 0))
  planet2.userData.startOffset = 12
  scene.add(planet2)

  collisionPlanetMeshes = [planet1, planet2]

  // Add glow to collision area
  const glowGeo = new THREE.SphereGeometry(8, 32, 32)
  const glowMat = new THREE.MeshBasicMaterial({
    color: 0xff6b6b,
    transparent: true,
    opacity: 0,
    side: THREE.BackSide
  })
  collisionGlow = new THREE.Mesh(glowGeo, glowMat)
  collisionGlow.position.copy(collisionPosition)
  scene.add(collisionGlow)
}

function createBlackHole() {
  // Position black hole further away in the corner (less prominent)
  blackHolePosition.set(-130, 35, -120)

  // 1. Black hole core (event horizon) - smaller
  const coreGeo = new THREE.SphereGeometry(2, 32, 32)
  const coreMat = new THREE.MeshBasicMaterial({
    color: 0x000000
  })
  blackHoleCore = new THREE.Mesh(coreGeo, coreMat)
  blackHoleCore.position.copy(blackHolePosition)

  // Photon ring (glowing edge) - smaller
  const ringGeo = new THREE.RingGeometry(2, 2.3, 64)
  const ringMat = new THREE.MeshBasicMaterial({
    color: 0xffffff,
    transparent: true,
    opacity: 0.7,
    side: THREE.DoubleSide,
    blending: THREE.AdditiveBlending
  })
  const ring = new THREE.Mesh(ringGeo, ringMat)
  ring.lookAt(camera.position)
  blackHoleCore.add(ring)

  scene.add(blackHoleCore)

  // 2. Gaseous Accretion Disk (Mesh with Noise Texture) - smaller
  const gasGeo = new THREE.RingGeometry(4, 12, 64, 8)
  const uvAttribute = gasGeo.attributes.uv
  
  if (uvAttribute) {
    // Twist UVs to create spiral effect
    for (let i = 0; i < uvAttribute.count; i++) {
      const u = uvAttribute.getX(i)
      const v = uvAttribute.getY(i)
      
      // Convert to polar
      const x = u - 0.5
      const y = v - 0.5
      let angle = Math.atan2(y, x)
      const radius = Math.sqrt(x*x + y*y)
      
      // Twist
      angle += radius * 5
      
      // Back to cartesian
      const newU = 0.5 + Math.cos(angle) * radius
      const newV = 0.5 + Math.sin(angle) * radius
      
      uvAttribute.setXY(i, newU, newV)
    }
  }
  
  const noiseTexture = createNoiseTexture()
  const gasMat = new THREE.MeshBasicMaterial({
    map: noiseTexture,
    color: 0xff6b6b,
    transparent: true,
    opacity: 0.6,
    side: THREE.DoubleSide,
    blending: THREE.AdditiveBlending,
    depthWrite: false
  })
  
  gaseousRing = new THREE.Mesh(gasGeo, gasMat)
  gaseousRing.position.copy(blackHolePosition)
  gaseousRing.rotation.x = Math.PI / 3 // Tilt
  scene.add(gaseousRing)

  // 3. Particle Accretion Disk (Sparkles) - reduced particles
  const diskParticleCount = 600
  const diskGeometry = new THREE.BufferGeometry()
  const diskPositions = new Float32Array(diskParticleCount * 3)
  const diskColors = new Float32Array(diskParticleCount * 3)
  const diskData: { angle: number; radius: number; speed: number; height: number }[] = []

  const diskColorOptions = [
    new THREE.Color(0xff6b6b), // Red
    new THREE.Color(0xffa502), // Orange
    new THREE.Color(0xffeaa7), // Yellow
  ]

  for (let i = 0; i < diskParticleCount; i++) {
    const angle = Math.random() * Math.PI * 2
    const radius = 4 + Math.random() * 10
    const height = (Math.random() - 0.5) * 1 * (1 - (radius - 4) / 10)

    diskData.push({
      angle,
      radius,
      speed: 0.01 + (14 - radius) * 0.002,
      height
    })

    const i3 = i * 3
    diskPositions[i3] = blackHolePosition.x + Math.cos(angle) * radius
    diskPositions[i3 + 1] = blackHolePosition.y + height
    diskPositions[i3 + 2] = blackHolePosition.z + Math.sin(angle) * radius

    const color = diskColorOptions[Math.floor(Math.random() * diskColorOptions.length)]!
    diskColors[i3] = color.r
    diskColors[i3 + 1] = color.g
    diskColors[i3 + 2] = color.b
  }

  diskGeometry.setAttribute('position', new THREE.BufferAttribute(diskPositions, 3))
  diskGeometry.setAttribute('color', new THREE.BufferAttribute(diskColors, 3))

  const diskMaterial = new THREE.PointsMaterial({
    size: 0.4,
    vertexColors: true,
    transparent: true,
    opacity: 0.6,
    blending: THREE.AdditiveBlending
  })

  accretionDisk = new THREE.Points(diskGeometry, diskMaterial)
  accretionDisk.userData.particleData = diskData
  // Match rotation of gaseous ring
  accretionDisk.rotation.x = Math.PI / 3
  // Adjust position to match rotated ring center
  accretionDisk.position.copy(blackHolePosition)
  
  scene.add(accretionDisk)

  // 4. Relativistic Jets - smaller and less prominent
  const jetParticleCount = 300
  const jetGeometry = new THREE.BufferGeometry()
  const jetPositions = new Float32Array(jetParticleCount * 3)
  const jetColors = new Float32Array(jetParticleCount * 3)
  const jetData: { velocity: THREE.Vector3; life: number; maxLife: number }[] = []

  for (let i = 0; i < jetParticleCount; i++) {
    const i3 = i * 3
    jetPositions[i3] = 0
    jetPositions[i3 + 1] = 0
    jetPositions[i3 + 2] = 0

    // Blue-ish white for high energy
    jetColors[i3] = 0.8
    jetColors[i3 + 1] = 0.9
    jetColors[i3 + 2] = 1.0

    const up = Math.random() > 0.5
    const spread = 0.08
    jetData.push({
      velocity: new THREE.Vector3(
        (Math.random() - 0.5) * spread,
        up ? 0.5 + Math.random() * 0.5 : -0.5 - Math.random() * 0.5,
        (Math.random() - 0.5) * spread
      ),
      life: Math.random(),
      maxLife: 1
    })
  }

  jetGeometry.setAttribute('position', new THREE.BufferAttribute(jetPositions, 3))
  jetGeometry.setAttribute('color', new THREE.BufferAttribute(jetColors, 3))

  const jetMaterial = new THREE.PointsMaterial({
    size: 0.8,
    vertexColors: true,
    transparent: true,
    opacity: 0.4,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true
  })

  jets = new THREE.Points(jetGeometry, jetMaterial)
  jets.userData.particleData = jetData
  jets.position.copy(blackHolePosition)
  // Tilt jets to be perpendicular to accretion disk
  jets.rotation.x = Math.PI / 3
  scene.add(jets)

  // 5. Infall particles - fewer and smaller range
  const infallCount = 100
  const infallGeometry = new THREE.BufferGeometry()
  const infallPositions = new Float32Array(infallCount * 3)
  const infallColors = new Float32Array(infallCount * 3)
  const infallData: { angle: number; radius: number; speed: number; spiralSpeed: number }[] = []

  for (let i = 0; i < infallCount; i++) {
    const angle = Math.random() * Math.PI * 2
    const radius = 15 + Math.random() * 20

    infallData.push({
      angle,
      radius,
      speed: 0.15 + Math.random() * 0.15,
      spiralSpeed: 0.01 + Math.random() * 0.015
    })

    const i3 = i * 3
    infallPositions[i3] = blackHolePosition.x + Math.cos(angle) * radius
    infallPositions[i3 + 1] = blackHolePosition.y + (Math.random() - 0.5) * 8
    infallPositions[i3 + 2] = blackHolePosition.z + Math.sin(angle) * radius

    const brightness = 0.4 + Math.random() * 0.4
    infallColors[i3] = brightness * 0.7
    infallColors[i3 + 1] = brightness * 0.8
    infallColors[i3 + 2] = brightness
  }

  infallGeometry.setAttribute('position', new THREE.BufferAttribute(infallPositions, 3))
  infallGeometry.setAttribute('color', new THREE.BufferAttribute(infallColors, 3))

  const infallMaterial = new THREE.PointsMaterial({
    size: 0.4,
    vertexColors: true,
    transparent: true,
    opacity: 0.4,
    sizeAttenuation: true
  })

  infallParticles = new THREE.Points(infallGeometry, infallMaterial)
  infallParticles.userData.particleData = infallData
  scene.add(infallParticles)
}

function updateBlackHole() {
  // Rotate gaseous ring
  if (gaseousRing) {
    gaseousRing.rotation.z -= 0.005
    const mat = gaseousRing.material as THREE.MeshBasicMaterial
    if (mat.map) {
      mat.map.offset.x += 0.002
      mat.map.offset.y += 0.001
    }
  }

  // Update accretion disk particles
  if (accretionDisk && accretionDisk.geometry.attributes.position) {
    const positions = accretionDisk.geometry.attributes.position.array as Float32Array
    const data = accretionDisk.userData.particleData as { angle: number; radius: number; speed: number; height: number }[]

    for (let i = 0; i < data.length; i++) {
      const p = data[i]!
      p.angle += p.speed

      const i3 = i * 3
      // Local coordinates (since we rotated the Points object)
      positions[i3] = Math.cos(p.angle) * p.radius
      positions[i3 + 1] = p.height + Math.sin(p.angle * 3) * 0.5
      positions[i3 + 2] = Math.sin(p.angle) * p.radius
    }

    accretionDisk.geometry.attributes.position.needsUpdate = true
  }

  // Update Jets
  if (jets && jets.userData.particleData) {
     const geometry = jets.geometry
     const positionAttr = geometry.attributes.position
     const colorAttr = geometry.attributes.color

     if (positionAttr && colorAttr) {
       const positions = positionAttr.array as Float32Array
       const colors = colorAttr.array as Float32Array
       const data = jets.userData.particleData as { velocity: THREE.Vector3; life: number; maxLife: number }[]
       
       for(let i=0; i<data.length; i++) {
          const p = data[i]
          if (!p) continue

          p.life -= 0.01
          
          if(p.life <= 0) {
             p.life = 1
             positions[i*3] = 0
             positions[i*3+1] = 0
             positions[i*3+2] = 0
          } else {
             positions[i*3] += p.velocity.x
             positions[i*3+1] += p.velocity.y
             positions[i*3+2] += p.velocity.z
          }
          
          // Fade out
          const opacity = Math.max(0, p.life)
          colors[i*3] = 0.8 * opacity
          colors[i*3+1] = 0.9 * opacity
          colors[i*3+2] = 1.0 * opacity
       }
       positionAttr.needsUpdate = true
       colorAttr.needsUpdate = true
     }
  }

  // Update infall particles
  if (infallParticles && infallParticles.geometry.attributes.position) {
    const positions = infallParticles.geometry.attributes.position.array as Float32Array
    const data = infallParticles.userData.particleData as { angle: number; radius: number; speed: number; spiralSpeed: number }[]

    for (let i = 0; i < data.length; i++) {
      const p = data[i]!
      p.angle += p.spiralSpeed
      p.radius -= p.speed

      if (p.radius < 3) {
        p.radius = 15 + Math.random() * 20
        p.angle = Math.random() * Math.PI * 2
      }

      const i3 = i * 3
      positions[i3] = blackHolePosition.x + Math.cos(p.angle) * p.radius
      positions[i3 + 1] = blackHolePosition.y + Math.sin(p.angle * 2) * (p.radius * 0.1)
      positions[i3 + 2] = blackHolePosition.z + Math.sin(p.angle) * p.radius
    }

    infallParticles.geometry.attributes.position.needsUpdate = true
  }

  // Subtle pulse on black hole core
  if (blackHoleCore) {
    const pulse = 1 + Math.sin(Date.now() * 0.003) * 0.05
    blackHoleCore.scale.setScalar(pulse)
    
    // Rotate the photon ring to always face camera
    const ring = blackHoleCore.children[0]
    if (ring) {
       ring.lookAt(camera.position)
    }
  }
}

function updateCollision() {
  collisionTime += 0.016

  // Cycle: approach -> collide -> explode -> reset
  const cycleTime = 8 // seconds per cycle
  const phase = (collisionTime % cycleTime) / cycleTime

  if (phase < 0.4) {
    // Approaching phase
    collisionPlanetMeshes.forEach(planet => {
      planet.visible = true
      const progress = phase / 0.4
      const startOffset = planet.userData.startOffset as number
      const targetOffset = startOffset > 0 ? 2 : -2
      planet.position.x = collisionPosition.x + startOffset + (targetOffset - startOffset) * progress
    })

    if (collisionParticles) {
      (collisionParticles.material as THREE.PointsMaterial).opacity = 0
    }
    if (collisionGlow) {
      (collisionGlow.material as THREE.MeshBasicMaterial).opacity = 0
    }
  } else if (phase < 0.5) {
    // Collision moment - flash
    collisionPlanetMeshes.forEach(planet => {
      planet.visible = false
    })

    if (collisionGlow) {
      const flash = Math.sin((phase - 0.4) / 0.1 * Math.PI)
      ;(collisionGlow.material as THREE.MeshBasicMaterial).opacity = flash * 0.8
    }

    // Reset particle positions
    if (collisionParticles) {
      const positions = collisionParticles.geometry.attributes.position!.array as Float32Array
      for (let i = 0; i < positions.length; i += 3) {
        positions[i] = collisionPosition.x
        positions[i + 1] = collisionPosition.y
        positions[i + 2] = collisionPosition.z
      }
      collisionParticles.geometry.attributes.position!.needsUpdate = true
      ;(collisionParticles.material as THREE.PointsMaterial).opacity = 1
    }
  } else if (phase < 0.9) {
    // Explosion phase
    collisionPlanetMeshes.forEach(planet => {
      planet.visible = false
    })

    if (collisionGlow) {
      ;(collisionGlow.material as THREE.MeshBasicMaterial).opacity = 0
    }

    if (collisionParticles) {
      const positions = collisionParticles.geometry.attributes.position!.array as Float32Array
      const velocities = collisionParticles.userData.velocities as THREE.Vector3[]
      const explosionProgress = (phase - 0.5) / 0.4

      for (let i = 0; i < positions.length / 3; i++) {
        const i3 = i * 3
        const vel = velocities[i]!
        positions[i3] = collisionPosition.x + vel.x * explosionProgress * 30
        positions[i3 + 1] = collisionPosition.y + vel.y * explosionProgress * 30
        positions[i3 + 2] = collisionPosition.z + vel.z * explosionProgress * 30
      }
      collisionParticles.geometry.attributes.position!.needsUpdate = true
      ;(collisionParticles.material as THREE.PointsMaterial).opacity = 1 - explosionProgress * 0.8
    }
  } else {
    // Fade out and reset
    if (collisionParticles) {
      const fadeProgress = (phase - 0.9) / 0.1
      ;(collisionParticles.material as THREE.PointsMaterial).opacity = 0.2 * (1 - fadeProgress)
    }
  }
}

function animate() {
  animationId = requestAnimationFrame(animate)

  // Update planet positions
  planets.forEach(p => {
    p.angle += p.speed

    // Circular motion around offset center
    p.mesh.position.x = p.centerX + Math.cos(p.angle) * p.distance
    p.mesh.position.z = p.centerZ + Math.sin(p.angle) * p.distance

    // Planet self-rotation
    p.mesh.rotation.y += p.selfRotationSpeed
  })

  // Sun subtle pulse
  if (sun) {
    const pulse = Math.sin(Date.now() * 0.002) * 0.1 + 1
    sun.scale.setScalar(pulse)
  }

  // Update collision animation
  updateCollision()

  // Update black hole
  updateBlackHole()

  // Smooth camera follow mouse
  const targetX = mouseX * 15
  const targetY = 50 - mouseY * 8

  camera.position.x += (targetX - camera.position.x) * 0.02
  camera.position.y += (targetY - camera.position.y) * 0.02
  camera.lookAt(0, 0, 0)

  // Slowly rotate starfield
  if (starMesh) {
    starMesh.rotation.y += 0.0001
  }

  renderer.render(scene, camera)
}

function onResize() {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}

function onMouseMove(event: MouseEvent) {
  mouseX = (event.clientX - window.innerWidth / 2) * 0.002
  mouseY = (event.clientY - window.innerHeight / 2) * 0.002
}

function onTouchMove(event: TouchEvent) {
  if (event.touches.length > 0) {
    mouseX = (event.touches[0]!.clientX - window.innerWidth / 2) * 0.002
    mouseY = (event.touches[0]!.clientY - window.innerHeight / 2) * 0.002
  }
}

function cleanup() {
  cancelAnimationFrame(animationId)
  window.removeEventListener('resize', onResize)
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('touchmove', onTouchMove)

  if (renderer) {
    renderer.dispose()
    containerRef.value?.removeChild(renderer.domElement)
  }

  scene.traverse((object) => {
    if (object instanceof THREE.Mesh || object instanceof THREE.Points || object instanceof THREE.LineLoop) {
      object.geometry.dispose()
      if (object.material instanceof THREE.Material) {
        object.material.dispose()
      }
    }
  })
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
  background: radial-gradient(ellipse at center, #0a0a1a 0%, #000000 100%);
}

.particle-background :deep(canvas) {
  display: block;
}
</style>
