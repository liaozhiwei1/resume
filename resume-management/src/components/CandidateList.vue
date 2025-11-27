<template>
  <el-card shadow="hover" class="candidate-card">
    <template #header>
      <div class="card-header">
        <div class="header-left">
          <el-icon class="header-icon"><User /></el-icon>
          <span class="card-title">候选人列表</span>
          <el-tag type="info" size="small" class="count-tag">
            共 {{ candidates.length }} 人
          </el-tag>
        </div>
        <div class="header-right">
          <UploadResume @uploaded="handleUploaded"/>
        </div>
      </div>
    </template>

    <div class="toolbar">
      <div class="search-group">
        <span class="search-label">姓名：</span>
        <el-input
            v-model="filter"
            placeholder="请输入姓名进行搜索"
            size="default"
            clearable
            class="search-input"
            @clear="handleSearch"
            @input="handleSearch"
            @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      
      <el-select
          v-model="selectedTag"
          placeholder="按标签筛选（可输入搜索）"
          clearable
          filterable
          class="tag-filter"
          @change="handleTagFilter"
      >
        <el-option
            v-for="tag in allTags"
            :key="tag"
            :label="tag"
            :value="tag"
        />
      </el-select>
      
      <el-select
          v-model="selectedDegree"
          placeholder="按学历筛选"
          clearable
          class="degree-filter"
          @change="handleDegreeFilter"
      >
        <el-option label="博士" value="博士" />
        <el-option label="硕士" value="硕士" />
        <el-option label="本科" value="本科" />
        <el-option label="大专" value="大专" />
        <el-option label="中专" value="中专" />
      </el-select>
      
      <el-button 
          type="primary" 
          @click="loadCandidates" 
          :loading="loading"
          :icon="RefreshRight"
      >
        刷新
      </el-button>
      <el-button 
          type="info" 
          @click="openColumnConfigDialog"
      >
        <el-icon><Tools /></el-icon>
        列设置
      </el-button>
    </div>

    <el-table
        :key="configVersion"
        :data="paginatedCandidates"
        style="width: 100%"
        v-loading="loading"
        element-loading-text="加载中..."
        empty-text="暂无候选人数据"
        stripe
        :row-class-name="tableRowClassName"
        class="candidate-table"
    >
      <el-table-column 
          v-if="columnConfig.id.visible"
          prop="id" 
          label="ID" 
          :width="columnConfig.id.width" 
          align="center"
      >
        <template #default="{ row }">
          <el-tag type="info" size="small">#{{ row.id }}</el-tag>
        </template>
      </el-table-column>
      
      <el-table-column 
          v-if="columnConfig.name.visible"
          prop="name" 
          label="姓名" 
          :width="columnConfig.name.width"
      >
        <template #default="{ row }">
          <div class="name-cell">
            <el-icon class="name-icon"><User /></el-icon>
            <span>{{ row.name || '未解析' }}</span>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column 
          v-if="columnConfig.email.visible"
          prop="email" 
          label="邮箱" 
          :min-width="columnConfig.email.width"
      >
        <template #default="{ row }">
          <div v-if="row.email" class="email-cell">
            <el-icon><Message /></el-icon>
            <span>{{ row.email }}</span>
          </div>
          <span v-else class="empty-text">-</span>
        </template>
      </el-table-column>
      
      <el-table-column 
          v-if="columnConfig.phone.visible"
          prop="phone" 
          label="电话" 
          :width="columnConfig.phone.width"
      >
        <template #default="{ row }">
          <div v-if="row.phone" class="phone-cell">
            <el-icon><Phone /></el-icon>
            <span>{{ row.phone }}</span>
          </div>
          <span v-else class="empty-text">-</span>
        </template>
      </el-table-column>
      
      <el-table-column 
          v-if="columnConfig.university.visible"
          prop="university" 
          label="毕业院校" 
          :min-width="columnConfig.university.width"
      >
        <template #default="{ row }">
          <div v-if="row.university" class="university-cell">
            <el-icon><School /></el-icon>
            <span>{{ row.university }}</span>
          </div>
          <span v-else class="empty-text">-</span>
        </template>
      </el-table-column>
      
      <el-table-column 
          v-if="columnConfig.degree.visible"
          prop="degree" 
          label="学历" 
          :width="columnConfig.degree.width" 
          align="center"
      >
        <template #default="{ row }">
          <el-tag v-if="row.degree" :type="getDegreeType(row.degree)" size="small">
            {{ row.degree }}
          </el-tag>
          <span v-else class="empty-text">-</span>
        </template>
      </el-table-column>
      
      <el-table-column 
          v-if="columnConfig.major.visible"
          prop="major" 
          label="专业" 
          :min-width="columnConfig.major.width"
      >
        <template #default="{ row }">
          <span v-if="row.major">{{ row.major }}</span>
          <span v-else class="empty-text">-</span>
        </template>
      </el-table-column>
      
      <el-table-column 
          v-if="columnConfig.tags.visible"
          prop="tags" 
          label="标签" 
          :min-width="columnConfig.tags.width"
      >
        <template #default="{ row }">
          <div class="tags-cell">
            <el-tag
                v-for="tag in getTagList(row.tags)"
                :key="tag"
                size="small"
                class="tag-item"
                :type="selectedTag === tag ? 'primary' : 'info'"
                @click="handleTagClick(tag)"
            >
              {{ tag }}
            </el-tag>
            <el-button
                text
                type="primary"
                size="small"
                @click="openTagDialog(row)"
                class="add-tag-btn"
            >
              <el-icon><Plus /></el-icon>
            </el-button>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column 
          v-if="columnConfig.notes.visible"
          prop="notes" 
          label="备注" 
          :min-width="columnConfig.notes.width"
      >
        <template #default="{ row }">
          <div class="notes-cell">
            <span v-if="row.notes" class="notes-text" :title="row.notes">
              {{ row.notes.length > 30 ? row.notes.substring(0, 30) + '...' : row.notes }}
            </span>
            <span v-else class="empty-text">-</span>
            <el-button
                text
                type="primary"
                size="small"
                @click="openNotesDialog(row)"
                class="edit-notes-btn"
                title="编辑备注"
            >
              <el-icon><Edit /></el-icon>
            </el-button>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column 
          v-if="columnConfig.created_at.visible"
          prop="created_at" 
          label="上传时间" 
          :width="columnConfig.created_at.width" 
          align="center"
      >
        <template #default="{ row }">
          <div class="time-cell">
            <el-icon><Clock /></el-icon>
            <span>{{ formatDate(row.created_at) }}</span>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="200" align="center" fixed="right">
        <template #default="{ row }">
          <div class="action-buttons">
            <el-button
                text
                type="primary"
                size="small"
                @click="handlePreview(row)"
                title="预览简历"
            >
              <el-icon><View /></el-icon>
              预览
            </el-button>
            <el-button
                text
                type="success"
                size="small"
                @click="handleDownload(row)"
                title="下载简历"
            >
              <el-icon><Download /></el-icon>
              下载
            </el-button>
            <el-button
                text
                type="danger"
                size="small"
                @click="handleDelete(row)"
                title="删除候选人"
            >
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <div v-if="total > 0" class="pagination-wrapper">
      <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next, jumper"
          @current-change="handlePageChange"
      />
    </div>

    <!-- 简历预览对话框 -->
    <el-dialog
        v-model="previewDialogVisible"
        title="简历预览"
        width="90%"
        :fullscreen="false"
        top="5vh"
        class="preview-dialog"
        @close="handlePreviewClose"
    >
      <div class="preview-content-wrapper">
        <div v-if="previewLoading" class="preview-loading">
          <el-icon class="is-loading"><Loading /></el-icon>
          <span>加载中...</span>
        </div>
        <div v-else-if="previewError" class="preview-error">
          <el-alert
              :title="previewError"
              type="error"
              show-icon
              :closable="false"
          />
          <el-button type="primary" @click="handleDownloadPreview" style="margin-top: 15px;">
            <el-icon><Download /></el-icon>
            下载简历
          </el-button>
        </div>
        <div v-else-if="previewFileType === 'pdf'" class="preview-pdf">
          <iframe
              :src="previewUrl"
              class="preview-iframe"
              frameborder="0"
          ></iframe>
        </div>
        <div v-else-if="previewFileType === 'docx'" class="preview-docx">
          <div v-if="previewHtmlContent" class="docx-html-content" v-html="previewHtmlContent"></div>
          <div v-else class="preview-docx-error">
            <el-alert
                title="无法加载 DOCX 预览"
                description="请尝试下载文件后使用 Microsoft Word 或其他文档编辑器打开"
                type="warning"
                show-icon
                :closable="false"
            />
            <div class="preview-docx-actions">
              <el-button type="primary" @click="handleDownloadPreview" size="large">
                <el-icon><Download /></el-icon>
                下载简历文件
              </el-button>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="preview-footer">
          <span class="preview-filename">{{ previewFileName }}</span>
          <div>
            <el-button @click="previewDialogVisible = false">关闭</el-button>
            <el-button type="primary" @click="handleDownloadPreview">
              <el-icon><Download /></el-icon>
              下载
            </el-button>
          </div>
        </div>
      </template>
    </el-dialog>

    <!-- 标签编辑对话框 -->
    <el-dialog
        v-model="tagDialogVisible"
        title="编辑标签"
        width="500px"
    >
      <div class="tag-dialog-content">
        <p class="tag-dialog-hint">多个标签用逗号分隔，例如：前端,React,3年经验</p>
        <el-input
            v-model="editingTags"
            type="textarea"
            :rows="3"
            placeholder="请输入标签，多个标签用逗号分隔"
        />
        <div class="tag-suggestions" v-if="allTags.length > 0">
          <p class="suggestions-title">常用标签：</p>
          <el-tag
              v-for="tag in allTags"
              :key="tag"
              size="small"
              class="suggestion-tag"
              @click="addTagToInput(tag)"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>
      <template #footer>
        <el-button @click="tagDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveTags" :loading="savingTags">保存</el-button>
      </template>
    </el-dialog>

    <!-- 备注编辑对话框 -->
    <el-dialog
        v-model="notesDialogVisible"
        title="编辑备注"
        width="600px"
    >
      <div class="notes-dialog-content">
        <el-input
            v-model="editingNotes"
            type="textarea"
            :rows="6"
            placeholder="请输入备注信息..."
            maxlength="500"
            show-word-limit
        />
      </div>
      <template #footer>
        <el-button @click="notesDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveNotes" :loading="savingNotes">保存</el-button>
      </template>
    </el-dialog>

    <!-- 列配置对话框 -->
    <el-dialog
        v-model="columnConfigDialogVisible"
        title="列设置"
        width="500px"
    >
      <div class="column-config-content">
        <p class="config-hint">勾选要显示的列，取消勾选隐藏列</p>
        <el-checkbox-group v-model="visibleColumns" class="column-checkbox-group">
          <el-checkbox 
              v-for="(config, key) in columnConfig" 
              :key="key"
              :label="key"
              class="column-checkbox"
          >
            {{ config.label }}
          </el-checkbox>
        </el-checkbox-group>
        <el-button 
            type="text" 
            @click="resetColumnConfig"
            class="reset-btn"
        >
          重置为默认
        </el-button>
      </div>
      <template #footer>
        <el-button @click="columnConfigDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveColumnConfig">保存</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { 
  User, Search, RefreshRight, Message, Phone, School, Clock, Plus, View, Download, Loading, Delete, Edit, Tools
} from '@element-plus/icons-vue';
import { fetchCandidates, updateCandidateTags, updateCandidateNotes, fetchAllTags, downloadResume, getDocxHtmlPreview, deleteCandidate } from "../api";
import { ElMessageBox } from "element-plus";
import { ElMessage } from "element-plus";
import UploadResume from "./UploadResume.vue";

export default {
  name: "CandidateList",
  components: {
    User,
    Search,
    Refresh: RefreshRight,
    Message,
    Phone,
    School,
    Clock,
    Plus,
    View,
    Download,
    Loading,
    Delete,
    Edit,
    Tools,
    UploadResume
  },
  data() {
    return {
      candidates: [],
      filter: "",
      loading: false,
      currentPage: 1,
      pageSize: 10,
      selectedTag: null,  // 选中的标签筛选
      selectedDegree: null,  // 选中的学历筛选
      allTags: [],  // 所有标签列表
      searchTimer: null,  // 搜索防抖定时器
      tagDialogVisible: false,  // 标签编辑对话框
      editingCandidateId: null,  // 正在编辑的候选人ID
      editingTags: "",  // 正在编辑的标签
      savingTags: false,  // 保存标签中
      previewDialogVisible: false,  // 预览对话框
      previewUrl: "",  // 预览URL
      previewFileType: "",  // 文件类型 (pdf/docx)
      previewFileName: "",  // 文件名
      previewLoading: false,  // 预览加载中
      previewError: "",  // 预览错误
      previewCandidateId: null,  // 正在预览的候选人ID
      previewHtmlContent: "",  // DOCX 的 HTML 预览内容
      notesDialogVisible: false,  // 备注编辑对话框
      editingCandidateIdForNotes: null,  // 正在编辑备注的候选人ID
      editingNotes: "",  // 正在编辑的备注
      savingNotes: false,  // 保存备注中
      columnConfigDialogVisible: false,  // 列配置对话框
      visibleColumns: [],  // 可见的列
      configVersion: 0,  // 配置版本号，用于触发更新
      total: 0,  // 总记录数（后端分页）
      totalPages: 0  // 总页数（后端分页）
    };
  },
  computed: {
    // 列配置（默认配置）
    defaultColumnConfig() {
      return {
        id: { label: 'ID', visible: true, width: 70 },
        name: { label: '姓名', visible: true, width: 120 },
        email: { label: '邮箱', visible: true, width: 180 },
        phone: { label: '电话', visible: true, width: 130 },
        university: { label: '毕业院校', visible: true, width: 150 },
        degree: { label: '学历', visible: true, width: 100 },
        major: { label: '专业', visible: true, width: 150 },
        tags: { label: '标签', visible: true, width: 200 },
        notes: { label: '备注', visible: true, width: 200 },
        created_at: { label: '上传时间', visible: true, width: 180 }
      };
    },
    // 列配置（从 localStorage 加载或使用默认值）
    columnConfig() {
      // 使用 configVersion 来触发响应式更新
      const _ = this.configVersion;
      
      const config = { ...this.defaultColumnConfig };
      const savedConfig = this.loadColumnConfig();
      
      if (savedConfig) {
        // 更新可见状态
        Object.keys(savedConfig).forEach(key => {
          if (config[key]) {
            config[key].visible = savedConfig[key].visible !== false;
            if (savedConfig[key].width) {
              config[key].width = savedConfig[key].width;
            }
          }
        });
      }
      
      return config;
    },
    paginatedCandidates() {
      // 后端已经完成搜索和筛选，直接返回数据
      return this.candidates;
    }
  },
  watch: {
    selectedTag() {
      this.currentPage = 1;
      // 标签变化时重新加载数据
      this.loadCandidates();
    },
    selectedDegree() {
      this.currentPage = 1;
      // 学历变化时重新加载数据
      this.loadCandidates();
    },
    configVersion() {
      // 当配置版本号改变时，更新可见列列表
      this.$nextTick(() => {
        this.updateVisibleColumns();
      });
    }
  },
  methods: {
    // 加载列配置
    loadColumnConfig() {
      if (typeof window === 'undefined') return null;
      try {
        const saved = localStorage.getItem('candidate_table_columns');
        if (saved) {
          return JSON.parse(saved);
        }
      } catch (e) {
        console.error('加载列配置失败:', e);
      }
      return null;
    },
    // 保存列配置
    saveColumnConfigToStorage(config) {
      if (typeof window === 'undefined') return;
      try {
        localStorage.setItem('candidate_table_columns', JSON.stringify(config));
      } catch (e) {
        console.error('保存列配置失败:', e);
      }
    },
    // 更新可见列列表
    updateVisibleColumns() {
      this.visibleColumns = Object.keys(this.columnConfig).filter(
        key => this.columnConfig[key].visible
      );
    },
    // 打开列配置对话框
    openColumnConfigDialog() {
      this.updateVisibleColumns();
      this.columnConfigDialogVisible = true;
    },
    // 保存列配置
    saveColumnConfig() {
      const config = {};
      Object.keys(this.defaultColumnConfig).forEach(key => {
        config[key] = {
          visible: this.visibleColumns.includes(key),
          width: this.columnConfig[key].width || this.defaultColumnConfig[key].width
        };
      });
      this.saveColumnConfigToStorage(config);
      // 更新配置版本号，触发计算属性重新计算
      this.configVersion++;
      this.columnConfigDialogVisible = false;
      ElMessage.success('列配置已保存');
    },
    // 重置列配置
    resetColumnConfig() {
      this.visibleColumns = Object.keys(this.defaultColumnConfig);
      if (typeof window !== 'undefined') {
        localStorage.removeItem('candidate_table_columns');
      }
      // 更新配置版本号，触发计算属性重新计算
      this.configVersion++;
      ElMessage.success('已重置为默认配置');
    },
    async loadCandidates() {
      this.loading = true;
      try {
        // 传递姓名搜索和学历筛选参数
        const nameSearch = this.filter.trim() || null;
        const response = await fetchCandidates(
          this.selectedTag, 
          nameSearch, 
          this.selectedDegree, 
          this.currentPage, 
          this.pageSize
        );
        // 后端返回分页结构：{ total, page, page_size, total_pages, data }
        this.candidates = response.data || [];
        this.total = response.total || 0;
        this.totalPages = response.total_pages || 0;
        
        await this.loadAllTags();
      } catch (e) {
        ElMessage.error(e.message || "加载失败");
        this.candidates = [];
        this.total = 0;
        this.totalPages = 0;
      } finally {
        this.loading = false;
      }
    },
    async loadAllTags() {
      try {
        this.allTags = await fetchAllTags();
      } catch (e) {
        console.error("加载标签列表失败:", e);
      }
    },
    handleTagFilter() {
      this.loadCandidates();
    },
    handleTagClick(tag) {
      // 点击标签时切换筛选
      if (this.selectedTag === tag) {
        this.selectedTag = null;
      } else {
        this.selectedTag = tag;
      }
      this.loadCandidates();
    },
    getTagList(tags) {
      if (!tags || !tags.trim()) return [];
      return tags.split(",").map(t => t.trim()).filter(t => t);
    },
    openTagDialog(row) {
      this.editingCandidateId = row.id;
      this.editingTags = row.tags || "";
      this.tagDialogVisible = true;
    },
    addTagToInput(tag) {
      const tags = this.editingTags ? this.editingTags.split(",").map(t => t.trim()) : [];
      if (!tags.includes(tag)) {
        tags.push(tag);
        this.editingTags = tags.join(",");
      }
    },
    async saveTags() {
      if (!this.editingCandidateId) return;
      
      this.savingTags = true;
      try {
        await updateCandidateTags(this.editingCandidateId, this.editingTags);
        ElMessage.success("标签更新成功");
        this.tagDialogVisible = false;
        await this.loadCandidates();
      } catch (e) {
        ElMessage.error(e.message || "保存标签失败");
      } finally {
        this.savingTags = false;
      }
    },
    openNotesDialog(row) {
      this.editingCandidateIdForNotes = row.id;
      this.editingNotes = row.notes || "";
      this.notesDialogVisible = true;
    },
    async saveNotes() {
      if (!this.editingCandidateIdForNotes) return;
      
      this.savingNotes = true;
      try {
        await updateCandidateNotes(this.editingCandidateIdForNotes, this.editingNotes);
        ElMessage.success("备注更新成功");
        this.notesDialogVisible = false;
        await this.loadCandidates();
      } catch (e) {
        ElMessage.error(e.message || "保存备注失败");
      } finally {
        this.savingNotes = false;
      }
    },
    handleSearch() {
      // 姓名搜索，使用防抖避免频繁请求
      if (this.searchTimer) {
        clearTimeout(this.searchTimer);
      }
      this.searchTimer = setTimeout(() => {
        this.currentPage = 1;
        this.loadCandidates();
      }, 500); // 500ms 防抖
    },
    handleDegreeFilter() {
      // 学历筛选变化时重新加载
      this.currentPage = 1;
      this.loadCandidates();
    },
    handlePageChange(page) {
      this.currentPage = page;
      // 切换页码时重新加载数据
      this.loadCandidates();
    },
    handleUploaded() {
      // 上传成功后刷新列表
      this.loadCandidates();
    },
    formatDate(dateString) {
      if (!dateString) return '-';
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${year}-${month}-${day} ${hours}:${minutes}`;
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
    },
    tableRowClassName({ rowIndex }) {
      if (rowIndex % 2 === 1) {
        return 'warning-row';
      }
      return '';
    },
    async handlePreview(row) {
      this.previewCandidateId = row.id;
      this.previewFileName = row.resume_original_name || "简历文件";
      
      // 判断文件类型
      const fileName = row.resume_original_name || "";
      if (fileName.toLowerCase().endsWith('.pdf')) {
        this.previewFileType = 'pdf';
        // 构建预览URL
        const API_BASE_URL = import.meta.env.DEV ? '' : 'http://localhost:5000';
        this.previewUrl = `${API_BASE_URL}/candidates/${row.id}/resume/preview`;
        this.previewLoading = true;
        this.previewError = "";
        this.previewDialogVisible = true;
        
        // 模拟加载（实际加载由iframe完成）
        setTimeout(() => {
          this.previewLoading = false;
        }, 500);
      } else if (fileName.toLowerCase().endsWith('.docx')) {
        this.previewFileType = 'docx';
        this.previewHtmlContent = "";
        this.previewLoading = true;
        this.previewError = "";
        this.previewDialogVisible = true;
        
        // 获取 DOCX 的 HTML 预览
        try {
          const result = await getDocxHtmlPreview(row.id);
          this.previewHtmlContent = result.content || "";
          this.previewLoading = false;
        } catch (e) {
          this.previewError = e.message || "加载预览失败";
          this.previewLoading = false;
          ElMessage.error("加载 DOCX 预览失败");
        }
      } else {
        this.previewFileType = 'unknown';
        this.previewError = "不支持的文件格式";
        this.previewDialogVisible = true;
        this.previewLoading = false;
      }
    },
    handleDownloadPreview() {
      if (this.previewCandidateId) {
        downloadResume(this.previewCandidateId);
        ElMessage.success("正在下载简历...");
      }
    },
    handlePreviewClose() {
      // 关闭预览时重置状态
      this.previewUrl = "";
      this.previewFileType = "";
      this.previewFileName = "";
      this.previewLoading = false;
      this.previewError = "";
      this.previewCandidateId = null;
      this.previewHtmlContent = "";
    },
    handleDownload(row) {
      try {
        downloadResume(row.id);
        ElMessage.success("正在下载简历...");
      } catch (e) {
        ElMessage.error("下载失败：" + (e.message || "未知错误"));
      }
    },
    async handleDelete(row) {
      try {
        await ElMessageBox.confirm(
          `确定要删除候选人"${row.name || '未命名'}"吗？此操作将同时删除关联的简历文件，且无法恢复。`,
          '确认删除',
          {
            confirmButtonText: '确定删除',
            cancelButtonText: '取消',
            type: 'warning',
            confirmButtonClass: 'el-button--danger',
          }
        );
        
        // 用户确认删除
        this.loading = true;
        try {
          await deleteCandidate(row.id);
          ElMessage.success({
            message: '删除成功',
            duration: 2000
          });
          // 刷新列表
          await this.loadCandidates();
        } catch (e) {
          ElMessage.error(e.message || '删除失败');
        } finally {
          this.loading = false;
        }
      } catch (e) {
        // 用户取消删除，不做任何操作
        if (e !== 'cancel') {
          console.error('删除操作出错:', e);
        }
      }
    }
  },
  mounted() {
    this.loadCandidates();
    // 初始化可见列列表
    this.updateVisibleColumns();
  },
  beforeUnmount() {
    // 清理定时器
    if (this.searchTimer) {
      clearTimeout(this.searchTimer);
    }
  }
};
</script>

<style scoped>
.candidate-card {
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-right {
  display: flex;
  align-items: center;
}

.header-icon {
  font-size: 20px;
  color: #409eff;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.count-tag {
  margin-left: 8px;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  align-items: center;
}

.search-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-label {
  font-size: 14px;
  color: #606266;
  white-space: nowrap;
}

.search-input {
  width: 250px;
}

.tag-filter {
  width: 200px;
}

.degree-filter {
  width: 150px;
}

.candidate-table {
  margin-top: 10px;
}

.candidate-table :deep(.el-table__row) {
  transition: all 0.3s;
}

.candidate-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
  transform: scale(1.01);
}

.name-cell,
.email-cell,
.phone-cell,
.university-cell,
.time-cell {
  display: flex;
  align-items: center;
  gap: 6px;
}

.name-icon {
  color: #409eff;
  font-size: 16px;
}

.email-cell .el-icon,
.phone-cell .el-icon,
.university-cell .el-icon,
.time-cell .el-icon {
  color: #909399;
  font-size: 14px;
}

.empty-text {
  color: #c0c4cc;
  font-style: italic;
}

.tags-cell {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
}

.tag-item {
  cursor: pointer;
  transition: all 0.3s;
}

.tag-item:hover {
  transform: scale(1.1);
}

.add-tag-btn {
  padding: 0 4px;
  min-height: auto;
}

.notes-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.notes-text {
  flex: 1;
  color: #606266;
  font-size: 14px;
  word-break: break-word;
}

.edit-notes-btn {
  padding: 0 4px;
  min-height: auto;
  flex-shrink: 0;
}

.tag-dialog-content {
  padding: 10px 0;
}

.notes-dialog-content {
  padding: 10px 0;
}

.tag-dialog-hint {
  color: #909399;
  font-size: 13px;
  margin-bottom: 15px;
}

.tag-suggestions {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #e4e7ed;
}

.suggestions-title {
  font-size: 13px;
  color: #606266;
  margin-bottom: 10px;
}

.suggestion-tag {
  margin-right: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.suggestion-tag:hover {
  transform: scale(1.1);
  background-color: #409eff;
  color: white;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
  align-items: center;
}

.action-buttons .el-button {
  padding: 5px 10px;
}

.preview-dialog :deep(.el-dialog__body) {
  padding: 0;
  height: calc(90vh - 120px);
  overflow: hidden;
}

.preview-content-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  color: #909399;
  font-size: 16px;
  padding: 60px;
}

.preview-loading .el-icon {
  font-size: 32px;
}

.preview-error {
  padding: 30px;
  text-align: center;
}

.preview-pdf {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.preview-iframe {
  width: 100%;
  height: calc(90vh - 120px);
  border: none;
}

.preview-docx {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  padding: 20px;
}

.docx-html-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.docx-html-content :deep(h3) {
  color: #303133;
  font-size: 18px;
  font-weight: 600;
  margin: 20px 0 10px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #409eff;
}

.docx-html-content :deep(p) {
  color: #606266;
  font-size: 14px;
  line-height: 1.8;
  margin: 10px 0;
}

.docx-html-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  border: 1px solid #e4e7ed;
}

.docx-html-content :deep(table td) {
  padding: 10px 15px;
  border: 1px solid #e4e7ed;
  color: #606266;
  font-size: 14px;
}

.docx-html-content :deep(table tr:nth-child(even)) {
  background-color: #f5f7fa;
}

.preview-docx-error {
  padding: 40px;
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.preview-docx-actions {
  margin-top: 30px;
}

.preview-docx {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  padding: 20px;
}

.docx-html-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.docx-html-content :deep(h3) {
  color: #303133;
  font-size: 18px;
  font-weight: 600;
  margin: 20px 0 10px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #409eff;
}

.docx-html-content :deep(p) {
  color: #606266;
  font-size: 14px;
  line-height: 1.8;
  margin: 10px 0;
}

.docx-html-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  border: 1px solid #e4e7ed;
}

.docx-html-content :deep(table td) {
  padding: 10px 15px;
  border: 1px solid #e4e7ed;
  color: #606266;
  font-size: 14px;
}

.docx-html-content :deep(table tr:nth-child(even)) {
  background-color: #f5f7fa;
}

.preview-docx-error {
  padding: 40px;
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.preview-docx-actions {
  margin-top: 30px;
}

.preview-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.preview-filename {
  color: #606266;
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 60%;
}

.column-config-content {
  padding: 10px 0;
}

.config-hint {
  color: #909399;
  font-size: 13px;
  margin-bottom: 20px;
}

.column-checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.column-checkbox {
  display: flex;
  align-items: center;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.column-checkbox:hover {
  background-color: #f5f7fa;
}

.reset-btn {
  margin-top: 20px;
  color: #909399;
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-group {
    width: 100%;
  }
  
  .search-input {
    width: 100%;
  }
  
  .candidate-table {
    font-size: 12px;
  }
}
</style>
