# 腾讯云托管部署指南

本项目已配置好，可以直接部署到腾讯云托管（CloudBase 云托管）。

## 部署方式

### 方式一：使用 GitHub Actions 自动部署（推荐）

项目已配置 GitHub Actions 工作流，支持自动部署。

#### 1. 配置 GitHub Secrets

在 GitHub 仓库设置中添加以下 Secrets：

- `TCB_ENV_ID`: 腾讯云环境ID（在 CloudBase 控制台查看）
- `TCB_SECRET_ID`: 腾讯云 API 密钥 ID（在腾讯云控制台-访问管理-API密钥管理）
- `TCB_SECRET_KEY`: 腾讯云 API 密钥 Key

#### 2. 触发自动部署

- **自动触发**：推送代码到 `dev_tcb` 分支时自动部署
- **手动触发**：在 GitHub Actions 页面手动运行工作流

#### 3. 查看部署状态

在 GitHub Actions 页面查看部署进度和日志。

### 方式二：使用 CloudBase CLI 手动部署

#### 1. 安装 CloudBase CLI

```bash
npm install -g @cloudbase/cli
```

#### 2. 登录腾讯云

```bash
tcb login
```

#### 3. 部署到云托管

在项目根目录下执行：

```bash
tcb cloudrun deploy
```

按照提示输入：
- 环境名称（如果还没有，会自动创建）
- 服务名称（例如：budget-manager）

CLI 会自动：
1. 构建 Docker 镜像
2. 上传到腾讯云容器镜像服务
3. 部署到云托管

### 4. 配置环境变量

在云托管控制台配置以下环境变量：

- `APP_PASSWORD`: 应用访问密码（默认：902124，建议修改）
- `DATA_DIR`: 数据目录（可选，默认：/app）
- `PORT`: 服务端口（可选，默认：80）

### 5. 配置服务

在云托管控制台：
1. 设置服务端口为 `80`
2. 配置健康检查（可选）
3. 设置自动扩缩容（可选）

## 项目结构说明

项目已按照腾讯云托管要求配置：

- ✅ `Dockerfile`: 使用 Python 3-alpine 基础镜像
- ✅ `requirements.txt`: 包含所有依赖
- ✅ `.dockerignore`: 排除不必要的文件
- ✅ `wsgi.py`: WSGI 入口文件
- ✅ 使用 gunicorn 作为生产环境 WSGI 服务器
- ✅ 使用腾讯云镜像源加速依赖安装
- ✅ 设置时区为上海时间

## 注意事项

1. **数据持久化**: 数据库文件（budget.db）和备份文件存储在容器内，建议：
   - 使用云数据库（如 MySQL）替代 SQLite
   - 或使用云存储（COS）定期备份数据库文件

2. **文件上传**: 上传的 Excel 文件和导出的文件存储在容器内，建议：
   - 使用云存储（COS）存储文件
   - 或定期清理旧文件

3. **密码安全**: 建议通过环境变量设置强密码，不要使用默认密码

4. **资源限制**: 根据实际使用情况配置 CPU 和内存限制

## 参考文档

- [腾讯云托管 Python 快速开始](https://docs.cloudbase.net/run/quick-start/dockerize-python)
- [CloudBase CLI 文档](https://docs.cloudbase.net/cli/overview)

