import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/fonts.css'
import './assets/normalize.styl'
import './assets/tailwind_preflight.styl'
import './assets/main.styl'
import './assets/home.styl'

const app = createApp(App)
app.use(router)
app.mount('#app')
