import { createI18n } from 'vue-i18n'
import en from './en'
import zh from './zh'

// Get saved locale or default to 'en'
const savedLocale = localStorage.getItem('locale') || 'en'

const i18n = createI18n({
  legacy: false, // Use Composition API
  locale: savedLocale,
  fallbackLocale: 'en',
  messages: {
    en,
    zh
  }
})

export default i18n
