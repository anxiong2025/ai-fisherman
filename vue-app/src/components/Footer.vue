<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'

const { t } = useI18n()
</script>

<template>
  <footer class="footer">
    <div class="container">
      <div class="footer__inner">
        <!-- Explore -->
        <div class="footer__section">
          <h4>{{ t('footer.explore') }}</h4>
          <ul class="footer__links">
            <li><RouterLink to="/articles">{{ t('footer.allArticles') }}</RouterLink></li>
            <li><RouterLink to="/articles?category=ai-news">AI {{ t('articles.categories.ai-news') }}</RouterLink></li>
            <li><RouterLink to="/articles?category=agents">{{ t('articles.categories.agents') }}</RouterLink></li>
            <li><RouterLink to="/projects">{{ t('footer.openSource') }}</RouterLink></li>
          </ul>
        </div>

        <!-- Learn -->
        <div class="footer__section">
          <h4>{{ t('footer.learn') }}</h4>
          <ul class="footer__links">
            <li><RouterLink to="/courses">{{ t('footer.allCourses') }}</RouterLink></li>
            <li><RouterLink to="/courses#agent-bootcamp">Agent Bootcamp</RouterLink></li>
            <li><RouterLink to="/courses#rag-course">RAG Course</RouterLink></li>
          </ul>
        </div>

        <!-- About -->
        <div class="footer__section">
          <h4>{{ t('footer.about') }}</h4>
          <ul class="footer__links">
            <li><RouterLink to="/about">{{ t('about.title') }}</RouterLink></li>
            <li>
              <a href="https://github.com/anxiong2025" target="_blank" rel="noopener">
                GitHub
              </a>
            </li>
            <li>
              <a href="https://youtube.com/channel/UCwvN-yTMk67eyOKLqIEuiXQ" target="_blank" rel="noopener">
                YouTube
              </a>
            </li>
          </ul>
        </div>

        <!-- Contact -->
        <div class="footer__section">
          <h4>{{ t('footer.contact') }}</h4>
          <ul class="footer__links">
            <li>
              <a href="mailto:contact@example.com">{{ t('footer.email') }}</a>
            </li>
            <li>
              <a href="#">{{ t('footer.cooperation') }}</a>
            </li>
          </ul>
        </div>
      </div>

      <div class="footer__bottom">
        <p>{{ t('common.copyright') }}</p>
      </div>
    </div>
  </footer>
</template>
