import { createApp } from 'vue'
import App from './App.vue'

import luckyUi from './package/index';

const app = createApp(App)

app.use(luckyUi);

app.mount('#app')
