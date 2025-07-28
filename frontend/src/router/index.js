import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/explore',
    name: 'Explorar',
    component: () => import('@/views/Explore.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router