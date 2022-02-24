import { createApp } from 'vue'
import App from './App.vue'

import ui from 'lucky-ui1'
const app = createApp(App)

app.use(ui)

app.mount('#app')
