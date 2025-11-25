<template>
  <!-- 上传按钮 -->
  <el-button 
    type="primary" 
    size="default" 
    @click="dialogVisible = true"
    class="upload-trigger-btn"
  >
    <el-icon><Upload /></el-icon>
    <span>上传简历</span>
  </el-button>

  <!-- 上传弹窗 -->
  <el-dialog
    v-model="dialogVisible"
    title="上传简历"
    width="800px"
    :close-on-click-modal="false"
    @close="handleDialogClose"
  >
    <div class="upload-dialog-content">
      <!-- 第一步：文件上传 -->
      <div v-if="!previewData" class="upload-step">
        <el-upload
          drag
          action="#"
          :file-list="fileList"
          :before-upload="beforeUpload"
          :auto-upload="false"
          class="upload-area"
          @change="handleChange"
          accept=".pdf,.docx"
        >
          <el-icon class="upload-icon"><UploadFilled /></el-icon>
          <div class="upload-text">
            <p class="upload-main-text">将文件拖到此处，或<em class="upload-link">点击上传</em></p>
            <p class="upload-hint">支持 PDF 和 DOCX 格式，文件大小不超过 10MB</p>
          </div>
        </el-upload>

        <div v-if="fileList.length > 0" class="file-info">
          <el-icon class="file-icon"><Document /></el-icon>
          <div class="file-details">
            <div class="file-name">{{ fileList[0].name }}</div>
            <div class="file-size">{{ formatFileSize(fileList[0].size) }}</div>
          </div>
          <el-button
            text
            type="danger"
            @click="fileList = []; error = ''"
            class="remove-btn"
          >
            <el-icon><Close /></el-icon>
          </el-button>
        </div>

        <el-button
          type="primary"
          :disabled="fileList.length === 0 || loading"
          @click="previewResume"
          class="upload-btn"
          :loading="loading"
          size="large"
        >
          <el-icon v-if="!loading"><Search /></el-icon>
          <span>{{ loading ? "解析中..." : "解析简历" }}</span>
        </el-button>

        <el-alert
          v-if="error"
          :title="error"
          type="error"
          show-icon
          class="upload-alert"
          :closable="true"
          @close="error = ''"
        />
      </div>

      <!-- 第二步：预览解析结果 -->
      <div v-else class="preview-step">
        <el-alert
          title="解析完成，请确认信息是否正确"
          type="success"
          show-icon
          :closable="false"
          class="preview-alert"
        />

        <div class="preview-content">
          <el-descriptions
            title="候选人信息"
            :column="2"
            border
            class="preview-descriptions"
          >
            <el-descriptions-item label="姓名">
              <span :class="{ 'empty-value': !previewData.parsed.name }">
                {{ previewData.parsed.name || '未解析' }}
              </span>
            </el-descriptions-item>
            <el-descriptions-item label="邮箱">
              <span :class="{ 'empty-value': !previewData.parsed.email }">
                {{ previewData.parsed.email || '未解析' }}
              </span>
            </el-descriptions-item>
            <el-descriptions-item label="电话">
              <span :class="{ 'empty-value': !previewData.parsed.phone }">
                {{ previewData.parsed.phone || '未解析' }}
              </span>
            </el-descriptions-item>
            <el-descriptions-item label="学历">
              <el-tag v-if="previewData.parsed.degree" :type="getDegreeType(previewData.parsed.degree)" size="small">
                {{ previewData.parsed.degree }}
              </el-tag>
              <span v-else class="empty-value">未解析</span>
            </el-descriptions-item>
            <el-descriptions-item label="毕业院校" :span="2">
              <span :class="{ 'empty-value': !previewData.parsed.university }">
                {{ previewData.parsed.university || '未解析' }}
              </span>
            </el-descriptions-item>
            <el-descriptions-item label="专业" :span="2">
              <span :class="{ 'empty-value': !previewData.parsed.major }">
                {{ previewData.parsed.major || '未解析' }}
              </span>
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="preview-actions">
          <el-button @click="handleCancel" :disabled="saving">
            取消
          </el-button>
          <el-button 
            type="primary" 
            @click="saveCandidate" 
            :loading="saving"
            size="large"
          >
            <el-icon v-if="!saving"><Check /></el-icon>
            <span>{{ saving ? '保存中...' : '确认保存' }}</span>
          </el-button>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script>
import { Upload, UploadFilled, Document, Close, Search, Check } from '@element-plus/icons-vue';
import { previewResumeParse, saveCandidate } from "../api";
import { ElMessage } from "element-plus";

export default {
  name: "UploadResume",
  components: {
    Upload,
    UploadFilled,
    Document,
    Close,
    Search,
    Check
  },
  data() {
    return {
      dialogVisible: false,
      fileList: [],
      error: "",
      loading: false,
      saving: false,
      previewData: null,  // 预览数据
    };
  },
  methods: {
    formatFileSize(bytes) {
      if (bytes === 0) return '0 B';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    },
    beforeUpload(file) {
      const validExt = /\.(pdf|docx)$/i;
      if (!validExt.test(file.name)) {
        this.error = "请选择 PDF 或 DOCX 格式的文件";
        ElMessage.error("不支持的文件格式");
        return false;
      }
      if (file.size > 10 * 1024 * 1024) {
        this.error = "文件大小不能超过 10MB";
        ElMessage.error("文件大小超出限制");
        return false;
      }
      this.error = "";
      return true;
    },
    handleChange(file) {
      this.fileList = [file];
      this.error = "";
      this.previewData = null;  // 清除之前的预览数据
    },
    async previewResume() {
      if (this.fileList.length === 0) {
        this.error = "请先选择文件";
        return;
      }
      this.loading = true;
      this.error = "";
      try {
        const formData = new FormData();
        formData.append("file", this.fileList[0].raw);
        const res = await previewResumeParse(formData);
        this.previewData = res;
        ElMessage.success("解析成功！请确认信息");
      } catch (e) {
        const errorMsg = (e && e.message) || "解析失败，请重试";
        this.error = errorMsg;
        ElMessage.error(errorMsg);
      } finally {
        this.loading = false;
      }
    },
    async saveCandidate() {
      if (!this.previewData) {
        ElMessage.error("没有可保存的数据");
        return;
      }
      this.saving = true;
      try {
        const res = await saveCandidate(this.previewData);
        ElMessage.success({
          message: `保存成功！候选人：${res.name || '未知'}`,
          duration: 3000
        });
        // 保存成功后关闭弹窗并通知父组件
        this.handleDialogClose();
        this.$emit("uploaded");
      } catch (e) {
        const errorMsg = (e && e.message) || "保存失败，请重试";
        ElMessage.error(errorMsg);
      } finally {
        this.saving = false;
      }
    },
    handleCancel() {
      this.previewData = null;
      this.fileList = [];
      this.error = "";
    },
    handleDialogClose() {
      // 关闭弹窗时重置所有状态
      this.previewData = null;
      this.fileList = [];
      this.error = "";
      this.loading = false;
      this.saving = false;
    },
    getDegreeType(degree) {
      const degreeMap = {
        '博士': 'danger',
        '硕士': 'warning',
        '本科': 'success',
        '大专': 'info',
        '中专': ''
      };
      return degreeMap[degree] || 'info';
    }
  }
};
</script>

<style scoped>
.upload-trigger-btn {
  /* 按钮样式已在组件内定义 */
}

.upload-dialog-content {
  padding: 10px 0;
}

.upload-step {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.upload-area {
  padding: 50px 20px;
  border: 2px dashed #d3dce6;
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafafa;
}

.upload-area:hover {
  border-color: #409eff;
  background: #f0f9ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.15);
}

.upload-icon {
  font-size: 64px;
  color: #409eff;
  margin-bottom: 16px;
  display: block;
}

.upload-text {
  margin-top: 16px;
}

.upload-main-text {
  font-size: 16px;
  color: #606266;
  margin-bottom: 8px;
}

.upload-link {
  color: #409eff;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
}

.upload-hint {
  font-size: 13px;
  color: #909399;
  margin: 0;
}

.file-info {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  border: 1px solid #e4e7ed;
}

.file-icon {
  font-size: 24px;
  color: #409eff;
}

.file-details {
  flex: 1;
}

.file-name {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
  margin-bottom: 4px;
  word-break: break-all;
}

.file-size {
  font-size: 12px;
  color: #909399;
}

.remove-btn {
  padding: 8px;
}

.upload-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}

.upload-alert {
  margin-top: 10px;
}

.preview-step {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.preview-alert {
  margin-bottom: 10px;
}

.preview-content {
  max-height: 500px;
  overflow-y: auto;
}

.preview-descriptions {
  margin: 20px 0;
}

.empty-value {
  color: #c0c4cc;
  font-style: italic;
}

.preview-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
}

@media (max-width: 768px) {
  .upload-area {
    padding: 30px 15px;
  }
  
  .upload-icon {
    font-size: 48px;
  }
}
</style>
