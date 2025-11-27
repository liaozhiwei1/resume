import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Candidates from '../views/Candidates.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/candidates',
    name: 'Candidates',
    component: Candidates
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

