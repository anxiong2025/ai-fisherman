<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores'
import { courses } from '@/data'

const { t } = useI18n()
const authStore = useAuthStore()
const pageVisible = ref(false)

// Handle purchase
function handlePurchase(courseId: string) {
  if (!authStore.isLoggedIn) {
    alert(t('auth.loginRequired'))
    return
  }

  // In production, this would open a payment modal
  alert(`Purchase course: ${courseId} - Payment integration coming soon!`)
}

onMounted(() => {
  setTimeout(() => {
    pageVisible.value = true
  }, 100)
})
</script>

<template>
  <div class="courses-page">
    <!-- Hero Section -->
    <section class="courses-hero" :class="{ visible: pageVisible }">
      <div class="container">
        <div class="courses-hero__badge">
          <span class="badge-icon">🎓</span>
          Premium AI Education
        </div>
        <h1 class="courses-hero__title">{{ t('courses.title') }}</h1>
        <p class="courses-hero__subtitle">{{ t('courses.subtitle') }}</p>

        <div class="courses-hero__stats">
          <div class="stat-item">
            <span class="stat-number">2,000+</span>
            <span class="stat-label">Students</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-number">50+</span>
            <span class="stat-label">Hours Content</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-number">4.9/5</span>
            <span class="stat-label">Rating</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Courses Section -->
    <section class="courses-section">
      <div class="container">
        <div
          v-for="(course, index) in courses"
          :key="course.id"
          :id="course.id"
          class="course-card"
          :class="{ visible: pageVisible }"
          :style="{ animationDelay: `${0.3 + index * 0.2}s` }"
        >
          <!-- Course Header -->
          <div class="course-card__header" :style="{ background: course.gradient }">
            <div class="course-header__content">
              <span v-if="course.badge" class="course-badge">{{ course.badge }}</span>
              <h2 class="course-card__title">{{ course.title }}</h2>
              <p class="course-card__subtitle">{{ course.subtitle }}</p>

              <div class="course-quick-stats">
                <div class="quick-stat">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12,6 12,12 16,14"/>
                  </svg>
                  <span>{{ course.curriculum.reduce((acc, c) => acc + parseInt(c.duration), 0) }}h</span>
                </div>
                <div class="quick-stat">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                  </svg>
                  <span>{{ course.curriculum.length }} Modules</span>
                </div>
                <div class="quick-stat">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                    <circle cx="9" cy="7" r="4"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                  </svg>
                  <span>500+ Students</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Course Body -->
          <div class="course-card__body">
            <div class="course-card__main">
              <!-- Overview -->
              <div class="content-section">
                <h3 class="section-title">
                  <span class="section-icon">📋</span>
                  {{ t('courses.overview') }}
                </h3>
                <p class="course-description">{{ course.description }}</p>
              </div>

              <!-- Features -->
              <div class="content-section">
                <h3 class="section-title">
                  <span class="section-icon">✨</span>
                  {{ t('courses.whatYouWillLearn') }}
                </h3>
                <div class="features-grid">
                  <div v-for="(feature, idx) in course.features" :key="idx" class="feature-item">
                    <div class="feature-check">
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path d="M13.5 4.5L6 12L2.5 8.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </div>
                    <span>{{ feature }}</span>
                  </div>
                </div>
              </div>

              <!-- Curriculum -->
              <div class="content-section">
                <h3 class="section-title">
                  <span class="section-icon">📚</span>
                  {{ t('courses.curriculum') }}
                </h3>
                <div class="curriculum-list">
                  <div
                    v-for="(section, idx) in course.curriculum"
                    :key="idx"
                    class="curriculum-item"
                  >
                    <div class="curriculum-header">
                      <div class="curriculum-number">{{ String(idx + 1).padStart(2, '0') }}</div>
                      <div class="curriculum-info">
                        <span class="curriculum-title">{{ section.title }}</span>
                        <span class="curriculum-meta">{{ section.lessons.length }} lessons • {{ section.duration }}</span>
                      </div>
                      <div class="curriculum-toggle">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                          <path d="M6 8l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                      </div>
                    </div>
                    <div class="curriculum-lessons">
                      <div
                        v-for="lesson in section.lessons"
                        :key="lesson"
                        class="lesson-item"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
                          <polygon points="7,5.5 10.5,8 7,10.5" fill="currentColor"/>
                        </svg>
                        <span>{{ lesson }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Instructor -->
              <div class="content-section">
                <h3 class="section-title">
                  <span class="section-icon">👨‍🏫</span>
                  {{ t('courses.instructor') }}
                </h3>
                <div class="instructor-card">
                  <div class="instructor-avatar">{{ course.instructor.avatar }}</div>
                  <div class="instructor-info">
                    <div class="instructor-name">{{ course.instructor.name }}</div>
                    <div class="instructor-bio">{{ course.instructor.bio }}</div>
                    <div class="instructor-social">
                      <a href="#" class="social-link">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                        </svg>
                      </a>
                      <a href="#" class="social-link">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                        </svg>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Sidebar -->
            <div class="course-card__sidebar">
              <div class="price-card">
                <div class="price-tag">
                  <span class="price-current">¥{{ course.price.toLocaleString() }}</span>
                  <span class="price-original">¥{{ course.originalPrice.toLocaleString() }}</span>
                </div>
                <div class="discount-badge">
                  Save {{ Math.round((1 - course.price / course.originalPrice) * 100) }}%
                </div>

                <button
                  class="enroll-btn"
                  @click="handlePurchase(course.id)"
                >
                  <span>{{ t('courses.enroll') }}</span>
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M4 10h12M12 6l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>

                <div class="includes-list">
                  <div class="includes-title">This course includes:</div>
                  <div class="include-item">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M13.5 4.5L6 12L2.5 8.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <span>{{ t('courses.lifetime') }}</span>
                  </div>
                  <div class="include-item">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M13.5 4.5L6 12L2.5 8.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <span>{{ t('courses.community') }}</span>
                  </div>
                  <div class="include-item">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M13.5 4.5L6 12L2.5 8.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <span>{{ t('courses.certificate') }}</span>
                  </div>
                </div>

                <div class="guarantee-text">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M8 1L2 4v4.5c0 3.5 2.5 6 6 7.5 3.5-1.5 6-4 6-7.5V4L8 1z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M5.5 8l2 2 3-3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  {{ t('courses.guarantee') }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section" :class="{ visible: pageVisible }">
      <div class="container">
        <div class="cta-content">
          <h2 class="cta-title">{{ t('courses.cta.title') }}</h2>
          <p class="cta-subtitle">{{ t('courses.cta.subtitle') }}</p>
          <a href="#agent-bootcamp" class="cta-btn">
            {{ t('courses.cta.button') }}
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M4 10h12M12 6l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.courses-page {
  min-height: 100vh;
  background: var(--color-background);
}

/* Hero Section */
.courses-hero {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: white;
  padding: 120px 0 80px;
  text-align: center;
  position: relative;
  overflow: hidden;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.courses-hero.visible {
  opacity: 1;
  transform: translateY(0);
}

.courses-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 20%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(118, 75, 162, 0.15) 0%, transparent 50%);
}

.courses-hero .container {
  position: relative;
  z-index: 1;
}

.courses-hero__badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 24px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 100px;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 32px;
}

.badge-icon {
  font-size: 18px;
}

.courses-hero__title {
  font-size: clamp(40px, 6vw, 64px);
  font-weight: 700;
  letter-spacing: -0.03em;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #ffffff 0%, rgba(255, 255, 255, 0.8) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.courses-hero__subtitle {
  font-size: 20px;
  line-height: 1.6;
  opacity: 0.85;
  max-width: 600px;
  margin: 0 auto 48px;
}

.courses-hero__stats {
  display: inline-flex;
  align-items: center;
  gap: 32px;
  padding: 20px 40px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
}

.stat-label {
  font-size: 13px;
  opacity: 0.7;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
}

/* Courses Section */
.courses-section {
  padding: 80px 0 120px;
}

.course-card {
  background: var(--color-card);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 4px 40px rgba(0, 0, 0, 0.08);
  margin-bottom: 60px;
  border: 1px solid var(--color-border);
  opacity: 0;
  transform: translateY(40px);
  animation: cardFadeIn 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
}

@keyframes cardFadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.course-card__header {
  padding: 60px 48px;
  position: relative;
  overflow: hidden;
}

.course-card__header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.2) 100%);
}

.course-header__content {
  position: relative;
  z-index: 1;
  color: white;
}

.course-badge {
  display: inline-block;
  padding: 8px 18px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 100px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 20px;
  letter-spacing: 0.3px;
}

.course-card__title {
  font-size: clamp(28px, 4vw, 40px);
  font-weight: 700;
  margin-bottom: 12px;
  letter-spacing: -0.02em;
}

.course-card__subtitle {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 24px;
}

.course-quick-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}

.quick-stat {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  opacity: 0.9;
}

.quick-stat svg {
  opacity: 0.8;
}

/* Course Body */
.course-card__body {
  display: grid;
  grid-template-columns: 1fr 380px;
}

@media (max-width: 1024px) {
  .course-card__body {
    grid-template-columns: 1fr;
  }
}

.course-card__main {
  padding: 48px;
}

.content-section {
  margin-bottom: 48px;
}

.content-section:last-child {
  margin-bottom: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 24px;
  color: var(--color-text);
}

.section-icon {
  font-size: 24px;
}

.course-description {
  font-size: 16px;
  line-height: 1.8;
  color: var(--color-text-secondary);
}

/* Features Grid */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 16px;
  background: var(--color-background-secondary);
  border-radius: 12px;
  font-size: 15px;
  color: var(--color-text);
  transition: all 0.3s ease;
}

.feature-item:hover {
  background: var(--color-primary);
  color: white;
}

.feature-item:hover .feature-check {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.feature-check {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(52, 199, 89, 0.1);
  color: #34c759;
  border-radius: 50%;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

/* Curriculum */
.curriculum-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.curriculum-item {
  border: 1px solid var(--color-border);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.curriculum-item:hover {
  border-color: var(--color-primary);
  box-shadow: 0 4px 20px rgba(0, 113, 227, 0.1);
}

.curriculum-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: var(--color-background-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.curriculum-item:hover .curriculum-header {
  background: rgba(0, 113, 227, 0.05);
}

.curriculum-number {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary);
  color: white;
  font-size: 14px;
  font-weight: 600;
  border-radius: 10px;
}

.curriculum-info {
  flex: 1;
}

.curriculum-title {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 4px;
}

.curriculum-meta {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.curriculum-toggle {
  color: var(--color-text-tertiary);
  transition: transform 0.3s ease;
}

.curriculum-lessons {
  padding: 16px 24px 20px;
  border-top: 1px solid var(--color-border);
}

.lesson-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.lesson-item svg {
  color: var(--color-primary);
  flex-shrink: 0;
}

/* Instructor */
.instructor-card {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 28px;
  background: var(--color-background-secondary);
  border-radius: 20px;
}

.instructor-avatar {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  flex-shrink: 0;
}

.instructor-info {
  flex: 1;
}

.instructor-name {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 8px;
}

.instructor-bio {
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text-secondary);
  margin-bottom: 12px;
}

.instructor-social {
  display: flex;
  gap: 12px;
}

.social-link {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-card);
  border-radius: 10px;
  color: var(--color-text-secondary);
  transition: all 0.3s ease;
}

.social-link:hover {
  background: var(--color-primary);
  color: white;
}

/* Sidebar */
.course-card__sidebar {
  padding: 48px;
  background: var(--color-background-secondary);
  border-left: 1px solid var(--color-border);
}

@media (max-width: 1024px) {
  .course-card__sidebar {
    border-left: none;
    border-top: 1px solid var(--color-border);
  }
}

.price-card {
  background: var(--color-card);
  border-radius: 20px;
  padding: 32px;
  text-align: center;
  position: sticky;
  top: 100px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.06);
}

.price-tag {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 12px;
  margin-bottom: 12px;
}

.price-current {
  font-size: 44px;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.02em;
}

.price-original {
  font-size: 20px;
  color: var(--color-text-tertiary);
  text-decoration: line-through;
}

.discount-badge {
  display: inline-block;
  padding: 6px 16px;
  background: linear-gradient(135deg, #ff3b30 0%, #ff6b6b 100%);
  color: white;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 28px;
}

.enroll-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 18px 32px;
  background: linear-gradient(135deg, #0071e3 0%, #0077ed 100%);
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 4px 20px rgba(0, 113, 227, 0.3);
}

.enroll-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(0, 113, 227, 0.4);
}

.enroll-btn svg {
  transition: transform 0.3s ease;
}

.enroll-btn:hover svg {
  transform: translateX(4px);
}

.includes-list {
  margin-top: 28px;
  text-align: left;
}

.includes-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 16px;
}

.include-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  font-size: 14px;
  color: var(--color-text);
  border-bottom: 1px solid var(--color-border);
}

.include-item:last-child {
  border-bottom: none;
}

.include-item svg {
  color: #34c759;
  flex-shrink: 0;
}

.guarantee-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
  font-size: 13px;
  color: var(--color-text-secondary);
}

.guarantee-text svg {
  color: #34c759;
}

/* CTA Section */
.cta-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.6s;
}

.cta-section.visible {
  opacity: 1;
  transform: translateY(0);
}

.cta-content {
  text-align: center;
  color: white;
}

.cta-title {
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 700;
  margin-bottom: 16px;
  letter-spacing: -0.02em;
}

.cta-subtitle {
  font-size: 19px;
  opacity: 0.9;
  margin-bottom: 32px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 36px;
  background: white;
  color: #667eea;
  border-radius: 100px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.cta-btn:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

.cta-btn svg {
  transition: transform 0.3s ease;
}

.cta-btn:hover svg {
  transform: translateX(4px);
}

/* Responsive */
@media (max-width: 768px) {
  .courses-hero {
    padding: 100px 0 60px;
  }

  .courses-hero__stats {
    flex-direction: column;
    gap: 20px;
    padding: 24px 32px;
  }

  .stat-divider {
    width: 60px;
    height: 1px;
  }

  .course-card__header {
    padding: 40px 24px;
  }

  .course-card__main {
    padding: 32px 24px;
  }

  .course-card__sidebar {
    padding: 32px 24px;
  }

  .instructor-card {
    flex-direction: column;
    text-align: center;
  }

  .instructor-social {
    justify-content: center;
  }
}
</style>
