<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const experience = [
  {
    title: 'Senior AI Engineer',
    company: 'Tech Company',
    period: '2021 - Present',
    description: 'Leading AI product development, building LLM-powered applications and agent systems.'
  },
  {
    title: 'Software Engineer',
    company: 'Startup',
    period: '2018 - 2021',
    description: 'Full-stack development with focus on backend systems and API design.'
  },
  {
    title: 'Backend Developer',
    company: 'Enterprise Corp',
    period: '2016 - 2018',
    description: 'Building scalable microservices and data processing pipelines.'
  }
]

const skills = [
  { name: 'Python', level: 95 },
  { name: 'TypeScript', level: 90 },
  { name: 'LangChain', level: 85 },
  { name: 'RAG Systems', level: 85 },
  { name: 'Claude/GPT APIs', level: 90 },
  { name: 'Vector Databases', level: 80 },
  { name: 'FastAPI', level: 85 },
  { name: 'React/Vue', level: 80 }
]

const social = [
  { name: 'GitHub', url: 'https://github.com/anxiong2025', icon: '🔗' },
  { name: 'YouTube', url: 'https://youtube.com/channel/UCwvN-yTMk67eyOKLqIEuiXQ', icon: '📺' },
  { name: 'Twitter', url: 'https://twitter.com', icon: '🐦' }
]
</script>

<template>
  <!-- Hero -->
  <section class="hero">
    <div class="container">
      <div class="about-avatar">👨‍💻</div>
      <h1 class="hero__title">Robert</h1>
      <p class="hero__subtitle">{{ t('about.subtitle') }}</p>
    </div>
  </section>

  <!-- About Content -->
  <section class="section">
    <div class="container container--narrow">
      <!-- Intro -->
      <div class="about-section">
        <p class="about-intro">
          {{ t('about.intro') }}
        </p>
        <p class="about-text">
          I've been working in software development for 8 years, with the last 3 years focused on AI applications.
          I'm passionate about building tools that help developers work more efficiently with AI.
        </p>
        <p class="about-text">
          Through this blog and my courses, I share practical knowledge about AI Agent development, RAG systems,
          and LLM integration. My goal is to help others learn how to build production-ready AI applications.
        </p>
      </div>

      <!-- Experience -->
      <div class="about-section">
        <h2>{{ t('about.experience') }}</h2>
        <div class="timeline">
          <div v-for="(job, index) in experience" :key="index" class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
              <h3>{{ job.title }}</h3>
              <p class="timeline-company">{{ job.company }} · {{ job.period }}</p>
              <p class="timeline-description">{{ job.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Skills -->
      <div class="about-section">
        <h2>{{ t('about.skills') }}</h2>
        <div class="skills-grid">
          <div v-for="skill in skills" :key="skill.name" class="skill-item">
            <div class="skill-header">
              <span class="skill-name">{{ skill.name }}</span>
              <span class="skill-level">{{ skill.level }}%</span>
            </div>
            <div class="skill-bar">
              <div class="skill-progress" :style="{ width: `${skill.level}%` }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Social -->
      <div class="about-section">
        <h2>{{ t('about.social') }}</h2>
        <div class="social-links">
          <a
            v-for="link in social"
            :key="link.name"
            :href="link.url"
            target="_blank"
            rel="noopener"
            class="social-link"
          >
            <span class="social-icon">{{ link.icon }}</span>
            <span>{{ link.name }}</span>
          </a>
        </div>
      </div>

      <!-- Contact -->
      <div class="about-section">
        <h2>{{ t('about.contact') }}</h2>
        <p class="about-text">
          For business inquiries, course questions, or collaboration opportunities,
          please reach out via email.
        </p>
        <a href="mailto:contact@example.com" class="btn btn--primary">
          {{ t('footer.email') }}
        </a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.about-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  margin: 0 auto 24px;
}

.about-section {
  margin-bottom: 48px;
}

.about-section h2 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 24px;
}

.about-intro {
  font-size: 21px;
  line-height: 1.5;
  margin-bottom: 16px;
}

.about-text {
  font-size: 17px;
  line-height: 1.65;
  color: var(--color-text-secondary);
  margin-bottom: 16px;
}

/* Timeline */
.timeline {
  position: relative;
  padding-left: 32px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 8px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: var(--color-border);
}

.timeline-item {
  position: relative;
  margin-bottom: 32px;
}

.timeline-item:last-child {
  margin-bottom: 0;
}

.timeline-dot {
  position: absolute;
  left: -28px;
  top: 8px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-primary);
}

.timeline-content h3 {
  font-size: 19px;
  font-weight: 600;
  margin-bottom: 4px;
}

.timeline-company {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
}

.timeline-description {
  font-size: 15px;
  color: var(--color-text-secondary);
  line-height: 1.5;
}

/* Skills */
.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.skill-item {
  background: var(--color-background-secondary);
  border-radius: var(--radius-md);
  padding: 16px;
}

.skill-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.skill-name {
  font-weight: 500;
}

.skill-level {
  font-size: 14px;
  color: var(--color-text-secondary);
}

.skill-bar {
  height: 6px;
  background: var(--color-border);
  border-radius: 3px;
  overflow: hidden;
}

.skill-progress {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 3px;
  transition: width 0.5s ease;
}

/* Social */
.social-links {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.social-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--color-background-secondary);
  border-radius: var(--radius-md);
  text-decoration: none;
  color: var(--color-text);
  transition: background var(--transition-fast);
}

.social-link:hover {
  background: var(--color-border);
  text-decoration: none;
}

.social-icon {
  font-size: 20px;
}
</style>
