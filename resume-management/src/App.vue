<template>
  <el-container class="app-container">
    <el-container class="body-container">
      <el-aside 
        class="sidebar" 
        :width="isCollapse ? '64px' : '240px'"
        :class="{ 'is-collapse': isCollapse }"
      >
        <div class="sidebar-header">
          <div class="logo-wrapper">
            <div class="logo-icon">
              <el-icon><Document /></el-icon>
            </div>
            <transition name="fade">
              <span v-show="!isCollapse" class="logo-text">简历管理系统</span>
            </transition>
          </div>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          :collapse="isCollapse"
          @select="handleMenuSelect"
          background-color="#1a1d29"
          text-color="#ffffff"
          active-text-color="#409eff"
          :collapse-transition="true"
        >
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <template #title>
              <span>首页</span>
            </template>
          </el-menu-item>
          <el-menu-item index="/candidates">
            <el-icon><List /></el-icon>
            <template #title>
              <span>候选人列表</span>
            </template>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-container class="main-container">
        <el-header class="main-header">
          <div class="header-content">
            <div class="header-left">
              <el-icon 
                class="menu-icon" 
                @click="toggleCollapse"
              >
                <Menu />
              </el-icon>
              <span class="page-title">{{ currentPageTitle }}</span>
            </div>
          </div>
        </el-header>
        
        <el-main class="main-content">
          <div class="content-wrapper">
            <router-view />
          </div>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { Document, HomeFilled, List, Menu } from '@element-plus/icons-vue';

export default {
  name: 'App',
  components: {
    Document,
    HomeFilled,
    List,
    Menu
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const isCollapse = ref(false);

    const activeMenu = computed(() => {
      return route.path;
    });

    const currentPageTitle = computed(() => {
      const titleMap = {
        '/': '首页',
        '/candidates': '候选人列表'
      };
      return titleMap[route.path] || '首页';
    });

    const toggleCollapse = () => {
      isCollapse.value = !isCollapse.value;
    };

    const handleMenuSelect = (index) => {
      router.push(index);
    };

    return {
      isCollapse,
      activeMenu,
      currentPageTitle,
      toggleCollapse,
      handleMenuSelect
    };
  }
};
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.body-container {
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  background: #1a1d29;
  overflow-y: auto;
  overflow-x: hidden;
  transition: width 0.3s;
}

.sidebar.is-collapse {
  width: 64px !important;
}

.sidebar-header {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
  transition: all 0.3s;
}

.logo-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #409eff;
  border-radius: 6px;
  color: #fff;
  font-size: 18px;
  flex-shrink: 0;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.sidebar-menu {
  border-right: none;
  padding: 12px 0;
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 240px;
}

.sidebar.is-collapse .sidebar-menu {
  width: 64px;
}

.sidebar-menu :deep(.el-menu-item) {
  height: 48px;
  line-height: 48px;
  color: #ffffff;
  font-size: 14px;
  margin: 4px 12px;
  border-radius: 6px;
  transition: all 0.3s;
  padding-left: 20px !important;
}

.sidebar.is-collapse .sidebar-menu :deep(.el-menu-item) {
  padding: 0 !important;
  margin: 4px 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center;
  width: 100% !important;
  min-width: 64px;
}

.sidebar.is-collapse .sidebar-menu :deep(.el-menu-item .el-icon) {
  margin: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  visibility: visible !important;
  opacity: 1 !important;
  width: 100%;
  height: 100%;
}

.sidebar.is-collapse .sidebar-menu :deep(.el-menu-item span) {
  display: none !important;
}

.sidebar.is-collapse .sidebar-menu :deep(.el-menu-item__title) {
  display: none !important;
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background: rgba(64, 158, 255, 0.15);
  color: #409eff;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: rgba(64, 158, 255, 0.2);
  color: #409eff;
  position: relative;
}

.sidebar-menu :deep(.el-menu-item.is-active::before) {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: #409eff;
  border-radius: 0 2px 2px 0;
}

.sidebar.is-collapse .sidebar-menu :deep(.el-menu-item.is-active::before) {
  display: none;
}

.sidebar-menu :deep(.el-menu-item.is-active .el-icon) {
  color: #409eff;
}

.sidebar-menu :deep(.el-icon) {
  font-size: 18px;
  margin-right: 12px;
  color: rgba(255, 255, 255, 0.7);
}

.sidebar-menu :deep(.el-menu-item:hover .el-icon) {
  color: #409eff;
}

.main-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.main-header {
  height: 64px;
  background: #ffffff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.header-content {
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.menu-icon {
  font-size: 20px;
  color: #606266;
  cursor: pointer;
  transition: all 0.3s;
  padding: 8px;
  border-radius: 4px;
}

.menu-icon:hover {
  color: #409eff;
  background: rgba(64, 158, 255, 0.1);
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.main-content {
  padding: 24px;
  background: #f5f7fa;
  overflow-y: auto;
  flex: 1;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

@media (max-width: 768px) {
  .sidebar {
    width: 200px !important;
  }
  
  .main-content {
    padding: 16px;
  }
  
  .logo-text {
    font-size: 16px;
  }
}
</style>
