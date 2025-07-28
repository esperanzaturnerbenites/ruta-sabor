import { createApp } from 'vue'
import './style.css'
import 'leaflet/dist/leaflet.css'
import App from './App.vue'

import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import router from './router/index.js'


const i18n = createI18n({
  locale: 'es',
  messages: {
    es: {},
    en: {}
  }
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')
