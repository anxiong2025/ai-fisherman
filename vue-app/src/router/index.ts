import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return { top: 0, behavior: 'smooth' }
  },
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/articles',
      name: 'articles',
      component: () => import('@/views/Articles.vue')
    },
    {
      path: '/articles/:slug',
      name: 'article-detail',
      component: () => import('@/views/ArticleDetail.vue')
    },
    {
      path: '/courses',
      name: 'courses',
      component: () => import('@/views/Courses.vue')
    },
    {
      path: '/projects',
      name: 'projects',
      component: () => import('@/views/Projects.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/About.vue')
    },
    // Admin routes
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/views/admin/Dashboard.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/articles',
      name: 'admin-articles',
      component: () => import('@/views/admin/Articles.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/articles/new',
      name: 'admin-article-new',
      component: () => import('@/views/admin/ArticleEditor.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/articles/:id/edit',
      name: 'admin-article-edit',
      component: () => import('@/views/admin/ArticleEditor.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/courses',
      name: 'admin-courses',
      component: () => import('@/views/admin/Courses.vue'),
      meta: { requiresAdmin: true }
    },
    // 404
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFound.vue')
    }
  ]
})

// Navigation guard for admin routes
router.beforeEach((to, _from, next) => {
  if (to.meta.requiresAdmin) {
    const authStore = useAuthStore()
    if (!authStore.isAdmin) {
      // Redirect to home if not admin
      next({ name: 'home' })
      return
    }
  }
  next()
})

export default router
