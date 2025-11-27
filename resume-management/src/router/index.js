import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Candidates from '../views/Candidates.vue';
import Login from '../views/Login.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false, hideLayout: true }
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/candidates',
    name: 'Candidates',
    component: Candidates,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const isAuthenticated = !!token;
  
  // 如果路由需要认证
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      // 未登录，跳转到登录页
      next('/login');
    } else {
      // 已登录，检查 token 是否过期
      const expiresAt = localStorage.getItem('token_expires_at');
      if (expiresAt) {
        const now = Math.floor(Date.now() / 1000);
        const expiresTimestamp = parseInt(expiresAt);
        if (now > expiresTimestamp) {
          // token 已过期
          localStorage.removeItem('token');
          localStorage.removeItem('username');
          localStorage.removeItem('token_expires_at');
          next('/login');
        } else {
          next();
        }
      } else {
        // 如果没有过期时间，也允许通过（兼容旧数据）
        next();
      }
    }
  } else if (to.path === '/login' && isAuthenticated) {
    // 已登录用户访问登录页，跳转到首页
    next('/');
  } else {
    next();
  }
});

export default router;

