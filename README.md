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

2. 构建并启动容器（确保前端镜像在构建时把 `VITE_BACKEND_URL` 写入 `env.production`，已经在 `docker-compose.yml` 中通过 `build.args` 指向 `https://resume-backend.292450.xyz`，不要跳过 `--build`）：
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

5. 如果你在 `resume.292450.xyz` / `resume-backend.292450.xyz` 等域名下部署，请在 `.env` 中配置：
   ```
   VITE_BACKEND_URL=https://resume-backend.292450.xyz
   ALLOWED_ORIGINS=https://resume.292450.xyz
   ```
   然后用 `docker compose --env-file .env up --build` 启动，后端将允许来自 `resume.292450.xyz` 的跨域请求。

## 自动 CI/CD 镜像构建

仓库包含 GitHub Actions 工作流 `.github/workflows/docker-build.yml`，默认推送到阿里云容器镜像服务（ACR）。
- **触发器**：`main` 分支 push 以及手动触发（`workflow_dispatch`）。
- **操作**：
  1. 使用 `Dockerfile.backend` 构建后端镜像，推送到 `${ALIYUN_REGISTRY_URL}/resume-team/resume-backend:latest`
  2. 使用 `Dockerfile.frontend` 构建前端镜像，推送到 `${ALIYUN_REGISTRY_URL}/resume-team/resume-frontend:latest`
- **凭据**：需要在仓库 Secrets 中设置 `ALIYUN_REGISTRY_URL`（例：`registry.cn-hangzhou.aliyuncs.com`）、`ALIYUN_USERNAME`、`ALIYUN_PASSWORD`，Workflow 会用这些信息登录阿里湾的 registry。
- **自定义命名空间**：`resume-team` 只是示例命名空间，若你在阿里云开启了不同的 registry namespace，把 workflow 中的 `env.BACKEND_IMAGE`/`env.FRONTEND_IMAGE` 替换成自己的路径。
  - **加速镜像源**：默认 base image 已改为 `python:3.13-slim-bullseye`（官方仍提供）和 `node:20-alpine`。
    如果你在自建阿里云镜像库遇到需要换镜像，可在 Secrets 中添加
    `ALIYUN_PYTHON_IMAGE`（例如 `registry.cn-hangzhou.aliyuncs.com/aliyunpython/python:3.13-slim-bullseye`）
    以及 `ALIYUN_NODE_IMAGE`（比如 `registry.cn-hangzhou.aliyuncs.com/aliyun-nodejs/node:20-alpine`）；Workflow 会把它们作为 build-arg 传入对应 Dockerfile。遇到 `docker.io/library/python:3.13-slim-buster: not found` 这类错误时只需指向可用的镜像即可。

CI 构建出的镜像可以直接在生产环境拉取，并在 `docker-compose.yml` 中用 `image` 替代 `build`（也可在外部部署脚本里用 `docker pull` + `docker run`）。

### 使用预打包镜像的一键部署

如果你已经通过 CI 构建并推送了镜像，可以使用 `docker-compose.prod.yml` 直接运行：

1. 把镜像地址写入环境变量（可在项目根目录新建 `.env.prod`）：
   ```
   BACKEND_IMAGE=registry.cn-hangzhou.aliyuncs.com/resume-team/resume-backend:latest
   FRONTEND_IMAGE=registry.cn-hangzhou.aliyuncs.com/resume-team/resume-frontend:latest
   ```
2. 运行：
   ```bash
   docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
   ```

- `backend` 使用已有镜像，映射 5000 端口，并通过命名卷保存 `/app/uploads` 和 `/app/resume_app.db`，不会在宿主出现单个数据库文件，方便多个环境复用。
- `frontend` 通过 `VITE_BACKEND_URL` 连接 `backend`（容器内部 DNS），默认指向 `http://backend:5000`。
- 需要时可在 `.env.prod` 里把 `VITE_BACKEND_URL` 改成公网地址，并在 `docker compose` 里加上 `ports` 或 `nginx` 反向代理。
- 如果前端域名不是 localhost，请同时在 `.env.prod`（或宿主环境变量）中设置：
  ```
  ALLOWED_ORIGINS=https://resume.292450.xyz
  ```
  后端将根据逗号分隔的清单为 `/preview` 等接口附加 `Access-Control-Allow-Origin` 头，不设置则默认仅允许 `http://localhost:3000` 和 `http://localhost:5173`。
 - 你的 CI 镜像构建会推送到阿里云，生产部署时可以把 `docker-compose.prod.yml` 中的 `VITE_BACKEND_URL` 和 `ALLOWED_ORIGINS` 都设置为上述 `292450.xyz` 域名，使前后端通过 HTTPS 通信。

要停止：
```
docker compose -f docker-compose.prod.yml down
```

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
