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
        target: 'https://resume-backend.292450.xyz',
        // target: 'https://127.0.0.1:5000',
        changeOrigin: true
      },
      '/preview': {
        target: 'https://resume-backend.292450.xyz',
        // target: 'https://127.0.0.1:5000',
        changeOrigin: true
      },
      '/save': {
        target: 'https://resume-backend.292450.xyz',
        // target: 'https://127.0.0.1:5000',
        changeOrigin: true
      },
      '/candidates': {
        target: 'https://resume-backend.292450.xyz',
        // target: 'https://127.0.0.1:5000',
        changeOrigin: true
      },
      '/tags': {
        target: 'https://resume-backend.292450.xyz',
        // target: 'https://127.0.0.1:5000',
        changeOrigin: true
      },
      '/upload-text': {
        target: 'https://resume-backend.292450.xyz',
        // target: 'https://127.0.0.1:5000',
        changeOrigin: true
      }
    }
  }
});
