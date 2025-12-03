<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import { Separator } from '@/components/ui/separator'

const { t } = useI18n()
</script>

<template>
  <footer class="bg-[var(--color-background-secondary)] py-12 mt-20">
    <div class="max-w-[1200px] mx-auto px-6">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-12">
        <!-- Explore -->
        <div>
          <h4 class="text-xs font-semibold uppercase tracking-[0.08em] text-[var(--color-text-secondary)] mb-4">
            {{ t('footer.explore') }}
          </h4>
          <ul class="list-none p-0 m-0 space-y-2">
            <li>
              <RouterLink to="/articles" class="text-sm text-[var(--color-text)] opacity-80 hover:opacity-100 transition-opacity no-underline">
                {{ t('footer.allArticles') }}
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/articles?category=ai-news" class="text-sm text-[var(--color-text)] opacity-80 hover:opacity-100 transition-opacity no-underline">
                AI {{ t('articles.categories.ai-news') }}
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/articles?category=agents" class="text-sm text-[var(--color-text)] opacity-80 hover:opacity-100 transition-opacity no-underline">
                {{ t('articles.categories.agents') }}
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/projects" class="text-sm text-[var(--color-text)] opacity-80 hover:opacity-100 transition-opacity no-underline">
                {{ t('footer.openSource') }}
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Learn -->
        <div>
          <h4 class="text-xs font-semibold uppercase tracking-[0.08em] text-[var(--color-text-secondary)] mb-4">
            {{ t('footer.learn') }}
          </h4>
          <ul class="list-none p-0 m-0 space-y-2">
            <li>
              <RouterLink to="/courses" class="text-sm text-[var(--color-text)] opacity-80 hover:opacity-100 transition-opacity no-underline">
                {{ t('footer.allCourses') }}
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/courses#agent-bootcamp" class="text-sm text-[var(--color-text)] opacity-80 hover:opacity-100 transition-opacity no-underline">
                Agent Bootcamp
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/courses#rag-course" class="text-sm text-[var(--color-text)] opacity-80 hover:opacity-100 transition-opacity no-underline">
                RAG Course
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- About -->
        <div>
          <h4 class="text-xs font-semibold uppercase tracking-[0.08em] text-[var(--color-text-secondary)] mb-4">
            {{ t('footer.about') }}
          </h4>
          <ul class="list-none p-0 m-0 space-y-2">
            <li>
              <RouterLink to="/about" class="text-sm text-[var(--color-text)] opacity-80 hover:opacity-100 transition-opacity no-underline">
                {{ t('about.title') }}
              </RouterLink>
            </li>
            <li>
              <a href="https://github.com/anxiong2025" target="_blank" rel="noopener" class="text-sm text-[var(--color-text)] opacity-80 hover:opacity-100 transition-opacity no-underline">
                GitHub
              </a>
            </li>
            <li>
              <a href="https://youtube.com/channel/UCwvN-yTMk67eyOKLqIEuiXQ" target="_blank" rel="noopener" class="text-sm text-[var(--color-text)] opacity-80 hover:opacity-100 transition-opacity no-underline">
                YouTube
              </a>
            </li>
          </ul>
        </div>

        <!-- Contact -->
        <div>
          <h4 class="text-xs font-semibold uppercase tracking-[0.08em] text-[var(--color-text-secondary)] mb-4">
            {{ t('footer.contact') }}
          </h4>
          <ul class="list-none p-0 m-0 space-y-2">
            <li>
              <a href="mailto:contact@example.com" class="text-sm text-[var(--color-text)] opacity-80 hover:opacity-100 transition-opacity no-underline">
                {{ t('footer.email') }}
              </a>
            </li>
            <li>
              <a href="#" class="text-sm text-[var(--color-text)] opacity-80 hover:opacity-100 transition-opacity no-underline">
                {{ t('footer.cooperation') }}
              </a>
            </li>
          </ul>
        </div>
      </div>

      <Separator class="my-12" />

      <div class="text-center text-xs text-[var(--color-text-secondary)]">
        <p>{{ t('common.copyright') }}</p>
      </div>
    </div>
  </footer>
</template>
