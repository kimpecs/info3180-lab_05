import { fileURLToPath, URL } from 'url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '^/api': {  // Match all paths starting with /api
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false,
      }
    }
  }
});