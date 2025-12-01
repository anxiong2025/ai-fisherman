import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './stores'
import i18n from './locales'

// Import global styles
import './assets/styles/main.css'

const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(i18n)

app.mount('#app')
