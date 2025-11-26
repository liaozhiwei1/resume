// vite.config.js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // 监听所有网络接口
    port: 3000, // 你也可以改为 5173/其他端口
    proxy: {
      '/upload': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/preview': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/save': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/candidates': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/tags': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/upload-text': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
});

