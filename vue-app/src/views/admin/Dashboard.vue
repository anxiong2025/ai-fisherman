<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import { articles, courses } from '@/data'

const { t } = useI18n()

// Mock stats
const stats = {
  totalArticles: articles.length,
  totalCourses: courses.length,
  totalUsers: 1256,
  totalRevenue: 89650
}

// Recent articles
const recentArticles = articles.slice(0, 5)

// Mock recent orders
const recentOrders = [
  { id: 'ORD001', user: 'Zhang Wei', course: 'AI Agent Bootcamp', amount: 2999, date: '2024-12-01' },
  { id: 'ORD002', user: 'Li Ming', course: 'RAG Course', amount: 1999, date: '2024-11-30' },
  { id: 'ORD003', user: 'Wang Fang', course: 'AI Agent Bootcamp', amount: 2999, date: '2024-11-29' },
  { id: 'ORD004', user: 'Chen Hua', course: 'RAG Course', amount: 1999, date: '2024-11-28' }
]
</script>

<template>
  <div class="admin-dashboard">
    <div class="container">
      <div class="admin-header">
        <h1>{{ t('admin.dashboard') }}</h1>
        <RouterLink to="/admin/articles/new" class="btn btn--primary">
          + {{ t('admin.articleEditor.newArticle') }}
        </RouterLink>
      </div>

      <!-- Stats Grid -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-card__icon">📝</div>
          <div class="stat-card__content">
            <div class="stat-card__value">{{ stats.totalArticles }}</div>
            <div class="stat-card__label">{{ t('admin.stats.totalArticles') }}</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-card__icon">📚</div>
          <div class="stat-card__content">
            <div class="stat-card__value">{{ stats.totalCourses }}</div>
            <div class="stat-card__label">{{ t('admin.stats.totalCourses') }}</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-card__icon">👥</div>
          <div class="stat-card__content">
            <div class="stat-card__value">{{ stats.totalUsers.toLocaleString() }}</div>
            <div class="stat-card__label">{{ t('admin.stats.totalUsers') }}</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-card__icon">💰</div>
          <div class="stat-card__content">
            <div class="stat-card__value">¥{{ stats.totalRevenue.toLocaleString() }}</div>
            <div class="stat-card__label">{{ t('admin.stats.totalRevenue') }}</div>
          </div>
        </div>
      </div>

      <div class="dashboard-grid">
        <!-- Recent Articles -->
        <div class="dashboard-card">
          <div class="dashboard-card__header">
            <h2>Recent Articles</h2>
            <RouterLink to="/admin/articles">View All</RouterLink>
          </div>
          <table class="admin-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Category</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="article in recentArticles" :key="article.id">
                <td>{{ article.title }}</td>
                <td><span class="badge">{{ article.category }}</span></td>
                <td>{{ article.date }}</td>
                <td>
                  <RouterLink :to="`/admin/articles/${article.id}/edit`" class="btn btn--text btn--small">
                    {{ t('common.edit') }}
                  </RouterLink>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Recent Orders -->
        <div class="dashboard-card">
          <div class="dashboard-card__header">
            <h2>Recent Orders</h2>
            <a href="#">View All</a>
          </div>
          <table class="admin-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>User</th>
                <th>Course</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in recentOrders" :key="order.id">
                <td>{{ order.id }}</td>
                <td>{{ order.user }}</td>
                <td>{{ order.course }}</td>
                <td>¥{{ order.amount }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
  padding: 40px 24px;
  min-height: calc(100vh - 52px);
  background: var(--color-background);
  position: relative;
  z-index: 1;
}

.admin-dashboard > .container {
  max-width: 1200px;
  margin: 0 auto;
  background: var(--color-background-secondary);
  border-radius: 24px;
  padding: 40px;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.admin-header h1 {
  font-size: 32px;
  font-weight: 600;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--color-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: var(--shadow-sm);
}

.stat-card__icon {
  width: 56px;
  height: 56px;
  background: var(--color-background-secondary);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.stat-card__value {
  font-size: 28px;
  font-weight: 600;
}

.stat-card__label {
  font-size: 14px;
  color: var(--color-text-secondary);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 24px;
}

@media (max-width: 600px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

.dashboard-card {
  background: var(--color-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.dashboard-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dashboard-card__header h2 {
  font-size: 18px;
  font-weight: 600;
}

.dashboard-card__header a {
  font-size: 14px;
  color: var(--color-primary);
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
}

.admin-table th,
.admin-table td {
  padding: 12px 8px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
  font-size: 14px;
}

.admin-table th {
  font-weight: 600;
  color: var(--color-text-secondary);
  font-size: 12px;
  text-transform: uppercase;
}

.admin-table tr:last-child td {
  border-bottom: none;
}

.badge {
  display: inline-block;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 500;
  background: var(--color-background-secondary);
  border-radius: 980px;
}
</style>
