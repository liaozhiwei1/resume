<template>
  <div class="home-container">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <el-icon class="title-icon"><Document /></el-icon>
          简历管理系统
        </h1>
        <p class="hero-subtitle">智能解析 · 高效管理 · 精准筛选</p>
        <p class="hero-description">
          支持 PDF 和 DOCX 格式简历自动解析，快速提取候选人信息，
          支持标签管理和智能筛选，让招聘工作更高效。
        </p>
        <div class="hero-actions">
          <el-button 
            type="primary" 
            size="large" 
            @click="goToCandidates"
            class="action-btn"
          >
            <el-icon><List /></el-icon>
            查看候选人列表
          </el-button>
          <el-button 
            type="success" 
            size="large" 
            @click="goToCandidates"
            class="action-btn"
          >
            <el-icon><Upload /></el-icon>
            上传简历
          </el-button>
        </div>
      </div>
    </div>

    <div class="features-section">
      <h2 class="section-title">核心功能</h2>
      <div class="features-grid">
        <el-card shadow="hover" class="feature-card">
          <template #header>
            <div class="feature-header">
              <el-icon class="feature-icon"><Upload /></el-icon>
              <span>简历上传</span>
            </div>
          </template>
          <div class="feature-content">
            <p>支持 PDF 和 DOCX 格式，自动解析候选人基本信息</p>
          </div>
        </el-card>

        <el-card shadow="hover" class="feature-card">
          <template #header>
            <div class="feature-header">
              <el-icon class="feature-icon"><Search /></el-icon>
              <span>智能解析</span>
            </div>
          </template>
          <div class="feature-content">
            <p>自动提取姓名、邮箱、电话、学历、专业等关键信息</p>
          </div>
        </el-card>

        <el-card shadow="hover" class="feature-card">
          <template #header>
            <div class="feature-header">
              <el-icon class="feature-icon"><Collection /></el-icon>
              <span>标签管理</span>
            </div>
          </template>
          <div class="feature-content">
            <p>支持自定义标签，快速筛选和分类候选人</p>
          </div>
        </el-card>

        <el-card shadow="hover" class="feature-card">
          <template #header>
            <div class="feature-header">
              <el-icon class="feature-icon"><View /></el-icon>
              <span>在线预览</span>
            </div>
          </template>
          <div class="feature-content">
            <p>支持在线预览和下载原始简历文件</p>
          </div>
        </el-card>
      </div>
    </div>

    <div class="stats-section">
      <el-card shadow="never" class="stats-card">
        <div class="stats-content">
          <div class="stat-item">
            <el-icon class="stat-icon"><User /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ candidateCount }}</div>
              <div class="stat-label">候选人总数</div>
            </div>
          </div>
          <el-divider direction="vertical" />
          <div class="stat-item">
            <el-icon class="stat-icon"><Collection /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ tagCount }}</div>
              <div class="stat-label">标签总数</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { 
  Document, List, Upload, Search, Collection, View, User 
} from '@element-plus/icons-vue';
import { fetchCandidates, fetchAllTags } from '../api';
import { ElMessage } from 'element-plus';

export default {
  name: 'Home',
  components: {
    Document,
    List,
    Upload,
    Search,
    Collection,
    View,
    User
  },
  setup() {
    const router = useRouter();
    const candidateCount = ref(0);
    const tagCount = ref(0);

    const goToCandidates = () => {
      router.push('/candidates');
    };

    const loadStats = async () => {
      try {
        const candidates = await fetchCandidates();
        candidateCount.value = candidates.length;
        
        const tags = await fetchAllTags();
        tagCount.value = tags.length;
      } catch (e) {
        console.error('加载统计数据失败:', e);
      }
    };

    onMounted(() => {
      loadStats();
    });

    return {
      candidateCount,
      tagCount,
      goToCandidates
    };
  }
};
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.hero-section {
  text-align: center;
  padding: 60px 20px;
  margin-bottom: 60px;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-icon {
  font-size: 48px;
  color: #409eff;
}

.hero-subtitle {
  font-size: 24px;
  color: #606266;
  margin-bottom: 16px;
  font-weight: 500;
}

.hero-description {
  font-size: 16px;
  color: #909399;
  line-height: 1.8;
  margin-bottom: 40px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-btn {
  padding: 12px 32px;
  font-size: 16px;
  font-weight: 600;
}

.features-section {
  margin-bottom: 60px;
}

.section-title {
  font-size: 32px;
  font-weight: 700;
  color: #303133;
  text-align: center;
  margin-bottom: 40px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.feature-card {
  border-radius: 12px;
  transition: all 0.3s;
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.feature-header {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.feature-icon {
  font-size: 24px;
  color: #409eff;
}

.feature-content {
  padding: 16px 0;
  color: #606266;
  line-height: 1.6;
  font-size: 14px;
}

.stats-section {
  margin-top: 60px;
}

.stats-card {
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.stats-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
  padding: 40px 20px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 48px;
  color: rgba(255, 255, 255, 0.9);
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 36px;
  font-weight: 700;
  color: #fff;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
}

.stats-card :deep(.el-card__body) {
  padding: 0;
}

.stats-card :deep(.el-divider) {
  border-color: rgba(255, 255, 255, 0.3);
  height: 60px;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 32px;
  }

  .title-icon {
    font-size: 32px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .hero-description {
    font-size: 14px;
  }

  .section-title {
    font-size: 24px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .stats-content {
    flex-direction: column;
    gap: 20px;
  }

  .stats-card :deep(.el-divider) {
    display: none;
  }
}
</style>

