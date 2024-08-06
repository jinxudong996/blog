import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"

import Home from '../view/Home.vue'

const routes: RouteRecordRaw[] = [
  {
    path:'/home',
    component:Home
  }
]

const router = createRouter({
  routes,
  history:createWebHistory()
})

export default router