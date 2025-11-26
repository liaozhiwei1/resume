# 简历管理系统

一个基于 FastAPI 和 Vue 3 的智能简历解析与管理系统，支持 PDF 和 DOCX 格式简历的自动解析、预览和管理。

## 项目结构

```
resume/
├── app/                    # 后端服务（FastAPI）
│   ├── main.py            # 主应用入口
│   ├── models.py          # 数据模型
│   ├── database.py        # 数据库配置
│   ├── parser.py          # 简历解析逻辑
│   ├── migrate.py         # 数据库迁移脚本
│   ├── requirements.txt  # Python 依赖
│   └── resume_app.db      # SQLite 数据库文件
└── resume-management/     # 前端应用（Vue 3）
    ├── src/
    │   ├── App.vue        # 主组件
    │   ├── api.js         # API 接口封装
    │   └── components/    # 组件目录
    ├── package.json       # Node.js 依赖
    └── vite.config.js     # Vite 配置
```

## 功能特性

- ✅ **智能解析**：自动从 PDF/DOCX 简历中提取候选人信息（姓名、邮箱、电话、学历、专业等）
- ✅ **预览功能**：支持 PDF 在线预览和 DOCX 转 HTML 预览
- ✅ **标签管理**：为候选人添加标签，支持按标签筛选
- ✅ **文件管理**：上传、下载、预览简历文件
- ✅ **搜索功能**：支持按姓名、邮箱、专业等字段搜索
- ✅ **响应式设计**：现代化的 UI 设计，支持移动端

## 技术栈

### 后端
- **FastAPI** - 现代、快速的 Web 框架
- **SQLAlchemy** - ORM 数据库操作
- **SQLite** - 轻量级数据库
- **pdfplumber** - PDF 文本提取
- **python-docx** - DOCX 文件处理

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Element Plus** - Vue 3 组件库
- **Vite** - 快速的前端构建工具

## 快速开始

### 后端设置

1. 进入后端目录：
```bash
cd app
```

2. 安装 Python 依赖：
```bash
pip install -r requirements.txt
```

3. 启动后端服务：
```bash
uvicorn main:app --reload --port 5000
```

后端服务将在 `http://localhost:5000` 启动，API 文档可在 `http://localhost:5000/docs` 查看。

### 前端设置

1. 进入前端目录：
```bash
cd resume-management
```

2. 安装 Node.js 依赖：
```bash
npm install
```

3. 启动开发服务器：
```bash
npm run dev
```

前端应用将在 `http://localhost:3000` 启动（或根据 vite.config.js 配置的端口）。

### Docker Compose 一键部署

1. 在项目根目录准备容器数据目录（如果你希望持久化数据）：
   ```bash
   mkdir -p app/uploads
   touch app/resume_app.db
   ```
   `uploads` 用于保存已上传的简历文件，`resume_app.db` 是 SQLite 数据库文件。

2. 构建并启动容器：
   ```bash
   docker compose up --build
   ```
   - `backend` 使用 `Dockerfile.backend`，自动安装 Python 依赖并运行 FastAPI（5000 端口）。
   - `frontend` 使用 `Dockerfile.frontend`，构建 Vue 项目并通过 `serve` 提供静态站点（3000 端口）。
   - 前端服务通过 `VITE_BACKEND_URL=http://backend:5000` 指向后端容器，Docker Compose 会自动解析。

3. 打开浏览器访问：
   - 前端：`http://localhost:3000`
   - FastAPI 文档：`http://localhost:5000/docs`

4. 关闭服务：
   ```bash
   docker compose down
   ```
   如果修改了代码或依赖后需要强制重建，添加 `--build` 参数。

5. 可选：将 `.env` 中的 `VITE_BACKEND_URL` 设置为外部可访问地址，例如：
   ```
   VITE_BACKEND_URL=http://api.example.com
   ```
   然后在 `docker compose up` 时使用 `docker compose --env-file .env up --build` 看 Docker Compose 文档。

## API 接口

### 主要接口

- `POST /preview` - 预览简历解析结果（不保存）
- `POST /save` - 保存已解析的候选人信息
- `POST /upload` - 上传简历并直接保存
- `GET /candidates` - 获取候选人列表（支持标签筛选）
- `PUT /candidates/{id}/tags` - 更新候选人标签
- `GET /tags` - 获取所有标签列表
- `GET /candidates/{id}/resume/preview` - 预览简历文件
- `GET /candidates/{id}/resume/download` - 下载简历文件

详细 API 文档请访问 `http://localhost:5000/docs`。

## 使用说明

1. **上传简历**：点击"上传简历"按钮，选择 PDF 或 DOCX 格式的简历文件
2. **预览解析**：系统会自动解析简历信息，确认无误后保存
3. **管理候选人**：在列表中查看、搜索、筛选候选人
4. **添加标签**：点击标签区域的"+"按钮，为候选人添加标签
5. **预览/下载**：点击操作列的"预览"或"下载"按钮查看或下载简历

## 注意事项

- 支持的文件格式：PDF、DOCX
- 文件大小限制：10MB
- 数据库文件位于 `app/resume_app.db`
- 上传的文件保存在 `app/uploads/` 目录

## 开发说明

### 数据库迁移

项目包含自动迁移脚本，首次启动时会自动检查并添加 `tags` 字段。如需手动执行迁移：

```bash
cd app
python migrate.py
```

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

## 许可证

MIT License
