import { createApp } from 'vue';
import App from './App.vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import router from './router';

const app = createApp(App);
app.use(ElementPlus);
app.use(router);
app.mount('#app');

// 错误处理
app.config.errorHandler = (err, instance, info) => {
  console.error('Vue Error:', err, info);
};
