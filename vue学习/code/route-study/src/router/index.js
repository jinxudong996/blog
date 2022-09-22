import Vue from 'vue'
// import VueRouter from 'vue-router'
import VueRouter from '../vueRouter'
import pageA from '../views/pageA.vue'
import pageB from '../views/pageB.vue'
import layout from '../components/layout.vue'
import btn from '../components/btn.vue'
import nothing from '../components/nothing.vue'
// import Detail from '../views/Detail.vue'

debugger
console.log(VueRouter)
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: layout,
    children:[
      {
        path: '/',
        name: 'index',
        component: btn
      },
      {
        path: '/pageB',
        name: 'pageB',
        component: pageB
      },
      {
        path: '/pageA',
        name: 'pageA',
        component: pageA
      },
      {
        path: '/detail/:id',
        name: 'Detail',
        props:true,
        component: () => import ('../views/Detail.vue')
      }
    ]
  },
  
  {
    path: '*',
    component: nothing
  },
  
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
