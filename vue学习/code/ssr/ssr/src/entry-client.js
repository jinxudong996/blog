import { createApp } from './app.js'

// 客户端特定引导逻辑……
console.log('执行了客户端渲染的代码嘛')
const { app } = createApp()

// 这里假定 App.vue 模板中根元素具有 `id="app"`

app.$mount('#app',true)