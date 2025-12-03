<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { courses } from '@/data'

const { t } = useI18n()

// Edit modal
const showEditModal = ref(false)
const editingCourse = ref<typeof courses[0] | null>(null)

function openEditModal(course: typeof courses[0]) {
  editingCourse.value = { ...course }
  showEditModal.value = true
}

function closeEditModal() {
  showEditModal.value = false
  editingCourse.value = null
}

function saveCourse() {
  console.log('Save course:', editingCourse.value)
  alert('Course saved!')
  closeEditModal()
}
</script>

<template>
  <div class="admin-page">
    <div class="container">
      <div class="admin-header">
        <h1>{{ t('admin.courses') }}</h1>
        <button class="btn btn--primary">
          + New Course
        </button>
      </div>

      <!-- Courses Grid -->
      <div class="courses-grid">
        <div v-for="course in courses" :key="course.id" class="course-admin-card">
          <div class="course-admin-card__header" :style="{ background: course.gradient }">
            <span v-if="course.badge" class="course-badge">{{ course.badge }}</span>
          </div>
          <div class="course-admin-card__body">
            <h3>{{ course.title }}</h3>
            <p>{{ course.subtitle }}</p>

            <div class="course-stats">
              <div class="stat">
                <span class="stat-value">¥{{ course.price }}</span>
                <span class="stat-label">Price</span>
              </div>
              <div class="stat">
                <span class="stat-value">{{ course.curriculum.length }}</span>
                <span class="stat-label">Modules</span>
              </div>
              <div class="stat">
                <span class="stat-value">156</span>
                <span class="stat-label">Students</span>
              </div>
            </div>

            <div class="course-actions">
              <button class="btn btn--secondary btn--small" @click="openEditModal(course)">
                {{ t('common.edit') }}
              </button>
              <button class="btn btn--ghost btn--small">
                View Stats
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit Modal -->
  <div v-if="showEditModal" class="modal-overlay active" @click.self="closeEditModal">
    <div class="modal-content" style="max-width: 600px;">
      <button class="modal-close" @click="closeEditModal">×</button>

      <h2 style="margin-bottom: 24px;">Edit Course</h2>

      <div v-if="editingCourse" class="modal-form">
        <div class="form-group">
          <label>Title</label>
          <input v-model="editingCourse.title" type="text" class="form-input" />
        </div>

        <div class="form-group">
          <label>Subtitle</label>
          <input v-model="editingCourse.subtitle" type="text" class="form-input" />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Price (¥)</label>
            <input v-model.number="editingCourse.price" type="number" class="form-input" />
          </div>
          <div class="form-group">
            <label>Original Price (¥)</label>
            <input v-model.number="editingCourse.originalPrice" type="number" class="form-input" />
          </div>
        </div>

        <div class="form-group">
          <label>Badge</label>
          <input v-model="editingCourse.badge" type="text" class="form-input" />
        </div>

        <div class="form-group">
          <label>Description</label>
          <textarea v-model="editingCourse.description" class="form-textarea" rows="4"></textarea>
        </div>

        <div class="form-actions">
          <button class="btn btn--ghost" @click="closeEditModal">
            {{ t('common.cancel') }}
          </button>
          <button class="btn btn--primary" @click="saveCourse">
            {{ t('common.save') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-page {
  padding: 40px 0;
  min-height: calc(100vh - 52px);
  background: var(--color-background-secondary);
  position: relative;
  z-index: 1;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.admin-header h1 {
  font-size: 32px;
  font-weight: 600;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.course-admin-card {
  background: var(--color-card);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.course-admin-card__header {
  height: 120px;
  position: relative;
}

.course-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 980px;
  font-size: 12px;
  font-weight: 500;
}

.course-admin-card__body {
  padding: 24px;
}

.course-admin-card__body h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
}

.course-admin-card__body p {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: 20px;
}

.course-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--color-border);
}

.stat {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
}

.stat-label {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.course-actions {
  display: flex;
  gap: 12px;
}

/* Modal Form */
.modal-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
}

.form-input,
.form-textarea {
  padding: 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-background);
  color: var(--color-text);
  font-size: 14px;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
}

.form-textarea {
  resize: vertical;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
}
</style>
