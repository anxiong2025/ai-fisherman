<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import { ArticleCard, ProjectCard } from '@/components'
import { getFeaturedArticles, getFeaturedProjects, courses } from '@/data'

const { t } = useI18n()

const featuredArticles = getFeaturedArticles(3)
const featuredProjects = getFeaturedProjects(3)
const featuredCourses = courses.slice(0, 2)

// Animation states
const heroVisible = ref(false)
const sectionsVisible = ref<boolean[]>([false, false, false, false])

onMounted(() => {
  // Trigger hero animation
  setTimeout(() => {
    heroVisible.value = true
  }, 100)

  // Intersection Observer for scroll animations
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
  <!-- Hero Section - Apple Style -->
  <section class="hero-apple">
    <div class="hero-apple__bg"></div>
    <div class="container">
      <div class="hero-apple__content" :class="{ visible: heroVisible }">
        <div class="hero-apple__badge">
          <span class="badge-dot"></span>
          AI Development Platform
        </div>
        <h1 class="hero-apple__title">
          <span class="title-prefix">{{ t('home.hero.prefix') }}</span>
          <span class="gradient-text">{{ t('home.hero.title') }}</span>
        </h1>
        <p class="hero-apple__tagline">{{ t('home.hero.subtitle') }}</p>
        <p class="hero-apple__description">{{ t('home.hero.description') }}</p>
        <div class="hero-apple__actions">
          <RouterLink to="/courses" class="btn-apple btn-apple--primary">
            <span>{{ t('home.hero.cta') }}</span>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M4 10H16M16 10L11 5M16 10L11 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </RouterLink>
          <RouterLink to="/articles" class="btn-apple btn-apple--secondary">
            {{ t('home.featured.viewAll') }}
          </RouterLink>
        </div>

        <!-- Stats -->
        <div class="hero-stats">
          <div class="hero-stat">
            <span class="hero-stat__value">1000+</span>
            <span class="hero-stat__label">Students</span>
          </div>
          <div class="hero-stat">
            <span class="hero-stat__value">50+</span>
            <span class="hero-stat__label">Articles</span>
          </div>
          <div class="hero-stat">
            <span class="hero-stat__value">10+</span>
            <span class="hero-stat__label">Projects</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Featured Articles -->
  <section class="section-apple animate-section" data-section="0" :class="{ visible: sectionsVisible[0] }">
    <div class="container">
      <div class="section-header-apple">
        <span class="section-eyebrow">Latest</span>
        <h2 class="section-title-apple">{{ t('home.featured.title') }}</h2>
        <p class="section-subtitle-apple">Insights and tutorials on AI development</p>
      </div>
      <div class="card-grid-apple">
        <ArticleCard
          v-for="(article, index) in featuredArticles"
          :key="article.id"
          :article="article"
          :style="{ animationDelay: `${index * 0.1}s` }"
          class="card-animate"
        />
      </div>
      <div class="section-action">
        <RouterLink to="/articles" class="link-apple">
          View all articles
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </RouterLink>
      </div>
    </div>
  </section>

  <!-- Featured Courses - Premium Look -->
  <section class="section-courses animate-section" data-section="1" :class="{ visible: sectionsVisible[1] }">
    <div class="container">
      <div class="section-header-apple">
        <span class="section-eyebrow">Learn</span>
        <h2 class="section-title-apple">{{ t('home.courses.title') }}</h2>
        <p class="section-subtitle-apple">Master AI development with hands-on courses</p>
      </div>
      <div class="courses-showcase">
        <div
          v-for="(course, index) in featuredCourses"
          :key="course.id"
          class="course-showcase-card"
          :style="{ animationDelay: `${index * 0.15}s` }"
        >
          <div class="course-showcase-card__visual" :style="{ background: course.gradient }">
            <div class="course-showcase-card__badge" v-if="course.badge">{{ course.badge }}</div>
            <div class="course-showcase-card__icon">
              {{ course.id === 'agent-bootcamp' ? '🤖' : '📚' }}
            </div>
          </div>
          <div class="course-showcase-card__content">
            <h3>{{ course.title }}</h3>
            <p>{{ course.subtitle }}</p>
            <div class="course-showcase-card__features">
              <span v-for="feature in course.features.slice(0, 3)" :key="feature">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M13.5 4.5L6 12L2.5 8.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                {{ feature }}
              </span>
            </div>
            <div class="course-showcase-card__footer">
              <div class="course-showcase-card__price">
                <span class="price-current">¥{{ course.price.toLocaleString() }}</span>
                <span class="price-original">¥{{ course.originalPrice.toLocaleString() }}</span>
              </div>
              <RouterLink :to="`/courses#${course.id}`" class="btn-apple btn-apple--primary btn-apple--small">
                {{ t('courses.enroll') }}
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Featured Projects -->
  <section class="section-apple animate-section" data-section="2" :class="{ visible: sectionsVisible[2] }">
    <div class="container">
      <div class="section-header-apple">
        <span class="section-eyebrow">Open Source</span>
        <h2 class="section-title-apple">{{ t('home.projects.title') }}</h2>
        <p class="section-subtitle-apple">Production-ready AI tools and templates</p>
      </div>
      <div class="card-grid-apple">
        <ProjectCard
          v-for="(project, index) in featuredProjects"
          :key="project.id"
          :project="project"
          :style="{ animationDelay: `${index * 0.1}s` }"
          class="card-animate"
        />
      </div>
      <div class="section-action">
        <RouterLink to="/projects" class="link-apple">
          Explore all projects
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </RouterLink>
      </div>
    </div>
  </section>

  <!-- CTA Section - Premium -->
  <section class="section-cta animate-section" data-section="3" :class="{ visible: sectionsVisible[3] }">
    <div class="cta-bg"></div>
    <div class="container">
      <div class="cta-content">
        <h2>{{ t('courses.cta.title') }}</h2>
        <p>{{ t('courses.cta.subtitle') }}</p>
        <RouterLink to="/courses" class="btn-apple btn-apple--white">
          {{ t('courses.cta.button') }}
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Hero - Apple Style with Premium Visual */
.hero-apple {
  position: relative;
  padding: 100px 0 80px;
  overflow: hidden;
  min-height: 85vh;
  display: flex;
  align-items: center;
}

.hero-apple__bg {
  position: absolute;
  inset: 0;
  background: var(--color-background);
}

/* Premium glow effects */
.hero-apple__bg::before {
  content: '';
  position: absolute;
  top: -30%;
  left: 50%;
  transform: translateX(-50%);
  width: 140%;
  height: 600px;
  background: radial-gradient(ellipse 50% 80% at 50% 0%, rgba(0, 113, 227, 0.12), transparent 70%);
  pointer-events: none;
}

.hero-apple__bg::after {
  content: '';
  position: absolute;
  top: 20%;
  right: -10%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(168, 85, 247, 0.08), transparent 60%);
  pointer-events: none;
}

[data-theme="dark"] .hero-apple__bg::before {
  background: radial-gradient(ellipse 50% 80% at 50% 0%, rgba(59, 130, 246, 0.2), transparent 70%);
}

[data-theme="dark"] .hero-apple__bg::after {
  background: radial-gradient(circle, rgba(168, 85, 247, 0.15), transparent 60%);
}

.hero-apple__content {
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
  opacity: 0;
  transform: translateY(20px);
  transition: all 1s cubic-bezier(0.16, 1, 0.3, 1);
}

.hero-apple__content.visible {
  opacity: 1;
  transform: translateY(0);
}

.hero-apple__badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(0, 113, 227, 0.08);
  border: 1px solid rgba(0, 113, 227, 0.15);
  border-radius: 980px;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-primary);
  margin-bottom: 24px;
  letter-spacing: 0.02em;
}

[data-theme="dark"] .hero-apple__badge {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.25);
}

.badge-dot {
  width: 6px;
  height: 6px;
  background: var(--color-primary);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.9); }
}

.hero-apple__title {
  font-size: clamp(56px, 10vw, 96px);
  font-weight: 700;
  line-height: 1.0;
  letter-spacing: -0.04em;
  margin-bottom: 20px;
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.12em;
}

.title-prefix {
  font-weight: 400;
  font-size: 0.45em;
  background: linear-gradient(135deg, #6b7280 0%, #9ca3af 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.gradient-text {
  background: linear-gradient(135deg,
    var(--color-text) 0%,
    var(--color-text) 40%,
    #3b82f6 70%,
    #8b5cf6 100%
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  background-size: 200% auto;
  animation: shimmer 8s ease-in-out infinite;
}

@keyframes shimmer {
  0%, 100% { background-position: 0% center; }
  50% { background-position: 100% center; }
}

[data-theme="dark"] .gradient-text {
  background: linear-gradient(135deg,
    #f5f5f7 0%,
    #f5f5f7 40%,
    #60a5fa 70%,
    #a78bfa 100%
  );
  -webkit-background-clip: text;
  background-clip: text;
  background-size: 200% auto;
}

.hero-apple__tagline {
  font-size: clamp(21px, 3vw, 28px);
  font-weight: 600;
  background: linear-gradient(135deg, var(--color-text) 0%, var(--color-text-secondary) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 12px;
  letter-spacing: -0.02em;
}

.hero-apple__description {
  font-size: 21px;
  color: var(--color-text-secondary);
  max-width: 560px;
  margin: 0 auto 40px;
  line-height: 1.47;
  letter-spacing: 0.011em;
}

.hero-apple__actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 64px;
}

/* Apple-style Buttons */
.btn-apple {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 28px;
  font-size: 17px;
  font-weight: 500;
  border-radius: 980px;
  text-decoration: none;
  cursor: pointer;
  border: none;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  position: relative;
}

.btn-apple--primary {
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  color: white;
  box-shadow:
    0 1px 2px rgba(0, 0, 0, 0.05),
    0 4px 16px rgba(59, 130, 246, 0.25);
}

.btn-apple--primary:hover {
  transform: translateY(-1px);
  box-shadow:
    0 2px 4px rgba(0, 0, 0, 0.05),
    0 8px 24px rgba(59, 130, 246, 0.35);
  text-decoration: none;
}

.btn-apple--primary:active {
  transform: translateY(0) scale(0.98);
}

.btn-apple--primary svg {
  transition: transform 0.2s ease;
}

.btn-apple--primary:hover svg {
  transform: translateX(2px);
}

.btn-apple--secondary {
  background: rgba(0, 0, 0, 0.05);
  color: var(--color-text);
  padding: 14px 24px;
}

[data-theme="dark"] .btn-apple--secondary {
  background: rgba(255, 255, 255, 0.1);
}

.btn-apple--secondary:hover {
  background: rgba(0, 0, 0, 0.08);
  text-decoration: none;
}

[data-theme="dark"] .btn-apple--secondary:hover {
  background: rgba(255, 255, 255, 0.15);
}

.btn-apple--white {
  background: white;
  color: #3b82f6;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.btn-apple--white:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
  text-decoration: none;
}

.btn-apple--small {
  padding: 11px 21px;
  font-size: 14px;
}

/* Hero Stats */
.hero-stats {
  display: flex;
  justify-content: center;
  gap: 56px;
  padding: 32px 48px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 20px;
  max-width: 480px;
  margin: 0 auto;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 0, 0, 0.04);
}

[data-theme="dark"] .hero-stats {
  background: rgba(255, 255, 255, 0.03);
  border-color: rgba(255, 255, 255, 0.06);
}

.hero-stat {
  text-align: center;
}

.hero-stat__value {
  display: block;
  font-size: 36px;
  font-weight: 700;
  letter-spacing: -0.03em;
  background: linear-gradient(135deg, var(--color-text) 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-stat__label {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-top: 4px;
}

/* Section Styles */
.section-apple {
  padding: 80px 0;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.section-apple.visible {
  opacity: 1;
  transform: translateY(0);
}

.section-courses {
  padding: 80px 0;
  background: var(--color-background-secondary);
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.section-courses.visible {
  opacity: 1;
  transform: translateY(0);
}

.section-header-apple {
  text-align: center;
  margin-bottom: 48px;
}

.section-eyebrow {
  display: inline-block;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
}

.section-title-apple {
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 600;
  letter-spacing: -0.025em;
  margin-bottom: 8px;
}

.section-subtitle-apple {
  font-size: 19px;
  color: var(--color-text-secondary);
  max-width: 500px;
  margin: 0 auto;
  line-height: 1.42;
}

/* Card Grid */
.card-grid-apple {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}

.card-animate {
  opacity: 0;
  transform: translateY(20px);
  animation: cardFadeIn 0.6s ease forwards;
}

@keyframes cardFadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-action {
  text-align: center;
  margin-top: 48px;
}

.link-apple {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 17px;
  font-weight: 400;
  color: var(--color-primary);
  text-decoration: none;
}

.link-apple:hover {
  text-decoration: underline;
}

.link-apple svg {
  transition: transform 0.2s ease;
}

.link-apple:hover svg {
  transform: translateX(3px);
}

/* Course Showcase Cards */
.courses-showcase {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 24px;
  max-width: 900px;
  margin: 0 auto;
}

@media (max-width: 480px) {
  .courses-showcase {
    grid-template-columns: 1fr;
  }
}

.course-showcase-card {
  background: var(--color-card);
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid var(--color-border);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  opacity: 0;
  transform: translateY(20px);
  animation: cardFadeIn 0.6s ease forwards;
}

.course-showcase-card:hover {
  transform: scale(1.02);
  box-shadow: var(--shadow-lg);
}

.course-showcase-card__visual {
  position: relative;
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.course-showcase-card__badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 980px;
  font-size: 11px;
  font-weight: 600;
  color: white;
  letter-spacing: 0.02em;
}

.course-showcase-card__icon {
  font-size: 56px;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.15));
}

.course-showcase-card__content {
  padding: 24px;
}

.course-showcase-card__content h3 {
  font-size: 21px;
  font-weight: 600;
  margin-bottom: 6px;
  letter-spacing: -0.01em;
}

.course-showcase-card__content p {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: 16px;
  line-height: 1.47;
}

.course-showcase-card__features {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.course-showcase-card__features span {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.course-showcase-card__features svg {
  color: var(--color-success);
  flex-shrink: 0;
}

.course-showcase-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.course-showcase-card__price {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.price-current {
  font-size: 24px;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.price-original {
  font-size: 14px;
  color: var(--color-text-tertiary);
  text-decoration: line-through;
}

/* CTA Section */
.section-cta {
  position: relative;
  padding: 120px 0;
  overflow: hidden;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.section-cta.visible {
  opacity: 1;
  transform: translateY(0);
}

.cta-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #1e1e2e 0%, #0f0f1a 100%);
}

.cta-bg::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at 30% 30%, rgba(59, 130, 246, 0.15), transparent 50%),
              radial-gradient(circle at 70% 70%, rgba(139, 92, 246, 0.15), transparent 50%);
  animation: ctaGlow 15s ease-in-out infinite;
}

@keyframes ctaGlow {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-5%, -5%); }
}

.cta-content {
  position: relative;
  text-align: center;
  color: white;
}

.cta-content h2 {
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 700;
  margin-bottom: 16px;
  letter-spacing: -0.03em;
  background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.cta-content p {
  font-size: 19px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 32px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.47;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-apple {
    padding: 80px 0 60px;
    min-height: auto;
  }

  .hero-apple__bg::before,
  .hero-apple__bg::after {
    opacity: 0.7;
  }

  .hero-stats {
    gap: 24px;
    padding: 24px 32px;
    flex-wrap: wrap;
  }

  .hero-stat__value {
    font-size: 28px;
  }

  .section-apple,
  .section-courses {
    padding: 60px 0;
  }

  .section-cta {
    padding: 80px 0;
  }

  .card-grid-apple {
    grid-template-columns: 1fr;
  }

  .courses-showcase {
    grid-template-columns: 1fr;
  }

  .btn-apple {
    padding: 12px 24px;
    font-size: 15px;
  }

  .cta-content h2 {
    font-size: 28px;
  }
}
</style>
