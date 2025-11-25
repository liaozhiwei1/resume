<template>
  <el-container class="app-container">
    <el-header class="header">
      <div class="header-content">
        <div class="header-left">
          <el-icon class="header-icon"><Document /></el-icon>
          <span class="header-title">简历管理系统</span>
        </div>
        <div class="header-right">
          <el-tag type="info" size="small">智能解析 · 高效管理</el-tag>
        </div>
      </div>
    </el-header>
    
    <el-main class="main-content">
      <div class="content-wrapper">
        <CandidateList ref="candidateList"/>
      </div>
    </el-main>

    <el-footer class="footer">
      <div class="footer-content">
        <span>© 2025 简历管理系统 | Powered by FastAPI & Vue 3</span>
      </div>
    </el-footer>
  </el-container>
</template>

<script>
import { Document } from '@element-plus/icons-vue';
import CandidateList from './components/CandidateList.vue';

export default {
  name: 'App',
  components: {
    CandidateList,
    Document
  }
};
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header {
  height: 70px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 0;
}

.header-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  font-size: 28px;
  color: #409eff;
}

.header-title {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
  user-select: none;
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-right {
  display: flex;
  align-items: center;
}

.main-content {
  padding: 30px;
  min-height: calc(100vh - 70px - 60px);
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.footer {
  height: 60px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.footer-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
  font-size: 13px;
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 15px;
  }
  
  .header-title {
    font-size: 20px;
  }
  
  .main-content {
    padding: 15px;
  }
}
</style>
