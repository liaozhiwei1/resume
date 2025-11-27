<template>
  <div class="login-container">
    <div class="login-background">
      <div class="background-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </div>
    
    <div class="login-content">
      <div class="login-logo">
        <div class="logo-icon-wrapper">
          <el-icon class="logo-icon"><Document /></el-icon>
        </div>
        <h1 class="system-title">简历管理系统</h1>
        <p class="system-subtitle">智能解析 · 高效管理 · 精准筛选</p>
      </div>
      
      <el-card class="login-card" shadow="always">
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          label-position="top"
        >
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              size="large"
              clearable
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <el-icon class="input-icon"><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              show-password
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <el-icon class="input-icon"><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              @click="handleLogin"
              class="login-button"
            >
              <span v-if="!loading">登录</span>
              <span v-else>登录中...</span>
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="login-footer">
          <el-divider>
            <span class="divider-text">提示信息</span>
          </el-divider>
          <div class="login-tip">
            <el-icon class="tip-icon"><InfoFilled /></el-icon>
            <span>默认账号：<strong>admin</strong> / <strong>admin123</strong></span>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { User, Lock, Document, InfoFilled } from '@element-plus/icons-vue';
import { login } from '../api';

export default {
  name: 'Login',
  components: {
    User,
    Lock,
    Document,
    InfoFilled
  },
  setup() {
    const router = useRouter();
    const loginFormRef = ref(null);
    const loading = ref(false);
    
    const loginForm = reactive({
      username: '',
      password: ''
    });
    
    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
      ]
    };
    
    const handleLogin = async () => {
      if (!loginFormRef.value) return;
      
      await loginFormRef.value.validate(async (valid) => {
        if (!valid) return;
        
        loading.value = true;
        try {
          const response = await login(loginForm.username, loginForm.password);
          
          // 存储 token 和用户信息
          localStorage.setItem('token', response.access_token);
          localStorage.setItem('username', response.username);
          // 存储过期时间戳（当前时间 + 过期秒数）
          const expiresAt = Math.floor(Date.now() / 1000) + response.expires_in;
          localStorage.setItem('token_expires_at', expiresAt.toString());
          
          ElMessage.success('登录成功');
          
          // 跳转到首页
          router.push('/');
        } catch (error) {
          ElMessage.error(error.message || '登录失败，请检查用户名和密码');
        } finally {
          loading.value = false;
        }
      });
    };
    
    return {
      loginFormRef,
      loginForm,
      loginRules,
      loading,
      handleLogin
    };
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0;
  margin: 0;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
}

.background-shapes {
  position: relative;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 20s infinite ease-in-out;
}

.shape-1 {
  width: 300px;
  height: 300px;
  top: -150px;
  left: -150px;
  animation-delay: 0s;
}

.shape-2 {
  width: 200px;
  height: 200px;
  bottom: -100px;
  right: -100px;
  animation-delay: 5s;
}

.shape-3 {
  width: 150px;
  height: 150px;
  top: 50%;
  right: 10%;
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  33% {
    transform: translate(30px, -30px) rotate(120deg);
  }
  66% {
    transform: translate(-20px, 20px) rotate(240deg);
  }
}

.login-content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-logo {
  text-align: center;
  margin-bottom: 40px;
  color: #fff;
}

.logo-icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  margin-bottom: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.logo-icon {
  font-size: 40px;
  color: #fff;
}

.system-title {
  margin: 0 0 10px 0;
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.system-subtitle {
  margin: 0;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 400;
}

.login-card {
  border-radius: 16px;
  border: none;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.login-card :deep(.el-card__body) {
  padding: 40px;
}

.login-form {
  margin: 0;
}

.login-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
  margin-bottom: 8px;
  padding: 0;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 0 0 1px #dcdfe6 inset;
  transition: all 0.3s;
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #c0c4cc inset;
}

.login-form :deep(.el-input.is-focus .el-input__wrapper) {
  box-shadow: 0 0 0 1px #409eff inset;
}

.input-icon {
  color: #909399;
  font-size: 18px;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  margin-top: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

.login-footer {
  margin-top: 30px;
}

.divider-text {
  color: #909399;
  font-size: 12px;
  padding: 0 16px;
}

.login-tip {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: #f0f9ff;
  border-radius: 8px;
  color: #606266;
  font-size: 13px;
}

.tip-icon {
  color: #409eff;
  font-size: 16px;
}

.login-tip strong {
  color: #409eff;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-content {
    max-width: 100%;
    padding: 0 20px;
  }
  
  .system-title {
    font-size: 24px;
  }
  
  .system-subtitle {
    font-size: 14px;
  }
  
  .logo-icon-wrapper {
    width: 60px;
    height: 60px;
  }
  
  .logo-icon {
    font-size: 30px;
  }
  
  .login-card :deep(.el-card__body) {
    padding: 30px 20px;
  }
}
</style>

