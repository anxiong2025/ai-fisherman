<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import { ArticleCard, ProjectCard } from '@/components'
import AnimatedCounter from '@/components/ui/AnimatedCounter.vue'
import { getFeaturedArticles, getFeaturedProjects, courses } from '@/data'
import { ArrowRight, Check } from 'lucide-vue-next'

const { t } = useI18n()

const featuredArticles = getFeaturedArticles(3)
const featuredProjects = getFeaturedProjects(3)
const featuredCourses = courses.slice(0, 2)

// Animation states
const heroVisible = ref(false)
const sectionsVisible = ref<boolean[]>([false, false, false, false])

// Counter animation
const stats = [
  { target: 1000, suffix: '+', label: 'Students' },
  { target: 50, suffix: '+', label: 'Articles' },
  { target: 10, suffix: '+', label: 'Projects' }
]

onMounted(() => {
  setTimeout(() => {
    heroVisible.value = true
  }, 100)

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const index = parseInt(entry.target.getAttribute('data-section') || '0')
          sectionsVisible.value[index] = true
        }
      })
    },
    { threshold: 0.1 }
  )

  document.querySelectorAll('.animate-section').forEach((el) => {
    observer.observe(el)
  })
})
</script>

<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section" :class="{ visible: heroVisible }">
      <div class="container">
        <div class="hero-badge">
          <span class="badge-dot"></span>
          AI Development Platform
        </div>

        <h1 class="hero-title">
          <span class="hero-prefix">{{ t('home.hero.prefix') }}</span>
          <span class="hero-main">{{ t('home.hero.title') }}</span>
        </h1>

        <p class="hero-tagline">{{ t('home.hero.subtitle') }}</p>
        <p class="hero-description">{{ t('home.hero.description') }}</p>

        <div class="hero-actions">
          <RouterLink to="/courses" class="btn-primary">
            {{ t('home.hero.cta') }}
            <ArrowRight class="btn-icon" />
          </RouterLink>
          <RouterLink to="/articles" class="btn-outline">
            {{ t('home.featured.viewAll') }}
          </RouterLink>
        </div>

        <div class="hero-stats">
          <div v-for="(stat, index) in stats" :key="stat.label" class="stat-item">
            <span class="stat-number">
              <AnimatedCounter 
                :value="stat.target" 
                :delay="index * 200 + 200"
                :format="(v) => Math.floor(v).toLocaleString() + stat.suffix"
              />
            </span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Articles -->
    <section
      class="content-section animate-section"
      data-section="0"
      :class="{ visible: sectionsVisible[0] }"
    >
      <div class="container">
        <div class="section-header">
          <span class="section-badge">Latest</span>
          <h2 class="section-title">{{ t('home.featured.title') }}</h2>
          <p class="section-description">Insights and tutorials on AI development</p>
        </div>

        <div class="articles-grid">
          <ArticleCard
            v-for="(article, index) in featuredArticles"
            :key="article.id"
            :article="article"
            :style="{ animationDelay: `${index * 0.1}s` }"
            class="card-item"
          />
        </div>

        <div class="section-footer">
          <RouterLink to="/articles" class="view-all-link">
            View all articles
            <ArrowRight class="link-icon" />
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Featured Courses -->
    <section
      class="content-section bg-secondary animate-section"
      data-section="1"
      :class="{ visible: sectionsVisible[1] }"
    >
      <div class="container">
        <div class="section-header">
          <span class="section-badge">Learn</span>
          <h2 class="section-title">{{ t('home.courses.title') }}</h2>
          <p class="section-description">Master AI development with hands-on courses</p>
        </div>

        <div class="courses-grid">
          <div
            v-for="(course, index) in featuredCourses"
            :key="course.id"
            class="course-card card-item"
            :style="{ animationDelay: `${index * 0.15}s` }"
          >
            <div class="course-visual" :style="{ background: course.gradient }">
              <span v-if="course.badge" class="course-badge">{{ course.badge }}</span>
              <span class="course-emoji">{{ course.id === 'agent-bootcamp' ? '🤖' : '📚' }}</span>
            </div>

            <div class="course-content">
              <h3 class="course-title">{{ course.title }}</h3>
              <p class="course-subtitle">{{ course.subtitle }}</p>

              <div class="course-features">
                <span v-for="feature in course.features.slice(0, 3)" :key="feature" class="feature-item">
                  <Check class="feature-icon" />
                  {{ feature }}
                </span>
              </div>

              <div class="course-footer">
                <div class="course-price">
                  <span class="price-current">¥{{ course.price.toLocaleString() }}</span>
                  <span class="price-original">¥{{ course.originalPrice.toLocaleString() }}</span>
                </div>
                <RouterLink :to="`/courses#${course.id}`" class="btn-primary btn-sm">
                  {{ t('courses.enroll') }}
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Projects -->
    <section
      class="content-section animate-section"
      data-section="2"
      :class="{ visible: sectionsVisible[2] }"
    >
      <div class="container">
        <div class="section-header">
          <span class="section-badge">Open Source</span>
          <h2 class="section-title">{{ t('home.projects.title') }}</h2>
          <p class="section-description">Production-ready AI tools and templates</p>
        </div>

        <div class="projects-grid">
          <ProjectCard
            v-for="(project, index) in featuredProjects"
            :key="project.id"
            :project="project"
            :style="{ animationDelay: `${index * 0.1}s` }"
            class="card-item"
          />
        </div>

        <div class="section-footer">
          <RouterLink to="/projects" class="view-all-link">
            Explore all projects
            <ArrowRight class="link-icon" />
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section
      class="cta-section animate-section"
      data-section="3"
      :class="{ visible: sectionsVisible[3] }"
    >
      <div class="container">
        <h2 class="cta-title">{{ t('courses.cta.title') }}</h2>
        <p class="cta-subtitle">{{ t('courses.cta.subtitle') }}</p>
        <RouterLink to="/courses" class="btn-primary">
          {{ t('courses.cta.button') }}
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background: var(--color-background);
}

/* Hero Section */
.hero-section {
  padding: 100px 0 80px;
  text-align: center;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.hero-section.visible {
  opacity: 1;
  transform: translateY(0);
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  background: var(--color-background-secondary);
  border-radius: 100px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: 24px;
}

.badge-dot {
  width: 8px;
  height: 8px;
  background: var(--color-primary);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

.hero-title {
  font-size: clamp(48px, 8vw, 80px);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.1;
  margin-bottom: 20px;
  color: var(--color-text);
}

.hero-prefix {
  font-size: 0.5em;
  font-weight: 400;
  color: var(--color-text-secondary);
  margin-right: 0.2em;
}

.hero-main {
  background: linear-gradient(
    90deg,
    #667eea 0%,
    #764ba2 25%,
    #f093fb 50%,
    #667eea 75%,
    #764ba2 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientFlow 4s ease infinite;
}

@keyframes gradientFlow {
  0% {
    background-position: 0% center;
  }
  50% {
    background-position: 100% center;
  }
  100% {
    background-position: 0% center;
  }
}

.hero-tagline {
  font-size: clamp(20px, 3vw, 28px);
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 12px;
}

.hero-description {
  font-size: 18px;
  line-height: 1.6;
  color: var(--color-text-secondary);
  max-width: 560px;
  margin: 0 auto 40px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 60px;
}

.hero-stats {
  display: inline-flex;
  gap: 48px;
  padding: 24px 48px;
  background: var(--color-background-secondary);
  border-radius: 20px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 32px;
  font-weight: 700;
  color: var(--color-text);
  font-variant-numeric: tabular-nums;
}

.stat-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* Buttons */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  background: var(--color-primary);
  color: white;
  border-radius: 100px;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-primary:hover {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 113, 227, 0.25);
}

.btn-primary.btn-sm {
  padding: 10px 20px;
  font-size: 14px;
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  background: transparent;
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
  border-radius: 100px;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-outline:hover {
  background: var(--color-primary);
  color: white;
}

.btn-icon {
  width: 20px;
  height: 20px;
}

/* Content Sections */
.content-section {
  padding: 80px 0;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.content-section.visible {
  opacity: 1;
  transform: translateY(0);
}

.content-section.bg-secondary {
  background: linear-gradient(135deg, #667eea 0%, #00d4ff 100%);
  max-width: 1200px;
  margin: 40px auto;
  border-radius: 24px;
}

.content-section.bg-secondary .section-title,
.content-section.bg-secondary .section-badge,
.content-section.bg-secondary .section-description {
  color: white;
}

.content-section.bg-secondary .section-badge {
  opacity: 0.9;
}

.content-section.bg-secondary .section-description {
  opacity: 0.9;
}

.section-header {
  text-align: center;
  margin-bottom: 48px;
}

.section-badge {
  display: inline-block;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 12px;
}

.section-title {
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 600;
  letter-spacing: -0.02em;
  margin-bottom: 12px;
  color: var(--color-text);
}

.section-description {
  font-size: 18px;
  color: var(--color-text-secondary);
  max-width: 500px;
  margin: 0 auto;
}

.section-footer {
  text-align: center;
  margin-top: 48px;
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 16px;
  color: var(--color-primary);
  text-decoration: none;
  transition: all 0.3s ease;
}

.view-all-link:hover {
  text-decoration: underline;
}

.link-icon {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

.view-all-link:hover .link-icon {
  transform: translateX(4px);
}

/* Grids */
.articles-grid,
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 24px;
  max-width: 900px;
  margin: 0 auto;
}

.card-item {
  opacity: 0;
  animation: cardFadeIn 0.6s ease forwards;
}

@keyframes cardFadeIn {
  to {
    opacity: 1;
  }
}

/* Course Card */
.course-card {
  background: var(--color-card);
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid var(--color-border);
  transition: all 0.3s ease;
}

.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
}

.course-visual {
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.course-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.course-emoji {
  font-size: 56px;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.15));
}

.course-content {
  padding: 24px;
}

.course-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--color-text);
}

.course-subtitle {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: 16px;
}

.course-features {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.feature-icon {
  width: 16px;
  height: 16px;
  color: var(--color-success);
  flex-shrink: 0;
}

.course-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.course-price {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.price-current {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text);
}

.price-original {
  font-size: 14px;
  color: var(--color-text-tertiary);
  text-decoration: line-through;
}

/* CTA Section */
.cta-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  text-align: center;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  max-width: 1200px;
  margin: 0 auto 40px;
  border-radius: 24px;
}

.cta-section.visible {
  opacity: 1;
  transform: translateY(0);
}

.cta-title {
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 16px;
  color: white;
}

.cta-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 32px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.cta-section .btn-primary {
  background: white;
  color: #667eea;
}

.cta-section .btn-primary:hover {
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

/* Responsive */
@media (max-width: 768px) {
  .hero-section {
    padding: 80px 0 60px;
  }

  .hero-stats {
    flex-direction: column;
    gap: 20px;
    padding: 24px 32px;
  }

  .articles-grid,
  .projects-grid,
  .courses-grid {
    grid-template-columns: 1fr;
  }

  .content-section {
    padding: 60px 0;
  }
}
</style>
