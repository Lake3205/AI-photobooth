
import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import WebcamTest from './views/WebcamTest.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HelloWorld,
    },
    {
      path: '/webcam-test',
      name: 'webcam-test',
      component: WebcamTest,
    },
  ],
})

export default router
