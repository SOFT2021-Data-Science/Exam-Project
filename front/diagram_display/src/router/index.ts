import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Guide from '../views/Guide.vue'
import NoPageFound from '../views/NoPageFound.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/guide',
    name: 'Guide',
    component: Guide
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'PageNotFound',
    component: NoPageFound
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
