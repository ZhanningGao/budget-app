# 腾讯云托管部署指南

本项目已配置好，可以直接部署到腾讯云托管（CloudBase 云托管）。

## 部署方式

### 方式一：使用 GitHub Actions 自动部署（推荐）

项目已配置 GitHub Actions 工作流，支持自动部署。

#### 1. 配置 GitHub Secrets

在 GitHub 仓库中配置 Secrets（需要仓库管理员权限）：

**步骤**：
1. 进入 GitHub 仓库主页
2. 点击右上角的 **Settings**（设置）
3. 在左侧菜单中找到：
   - **Secrets and variables** → **Actions**（新版本）
   - 或直接找到 **Secrets**（旧版本）
4. 点击 **New repository secret** 或 **New secret** 按钮
5. 添加以下 Secrets：

   - **TCB_ENV_ID**: 腾讯云环境ID（在 CloudBase 控制台查看）
   - **TCB_SECRET_ID**: 腾讯云 API 密钥 ID（在腾讯云控制台-访问管理-API密钥管理）
   - **TCB_SECRET_KEY**: 腾讯云 API 密钥 Key

**重要：配置 API 密钥权限**

API 密钥必须有 CloudBase 相关权限，否则会报错 `you are not authorized to perform operation`。

**配置权限步骤**：

1. **使用子账号（推荐）**：
   - 登录 [腾讯云控制台](https://console.cloud.tencent.com/)
   - 进入「访问管理」→「用户」→「新建子用户」
   - 选择「编程访问」，创建子用户
   - 为子用户添加策略：`QcloudTCBFullAccess`（CloudBase 全读写访问权限）
   - 使用子用户的 SecretId 和 SecretKey

2. **或为主账号 API 密钥添加权限**：
   - 进入「访问管理」→「API密钥管理」
   - 点击需要使用的密钥，查看权限
   - 确保有 CloudBase 相关权限

3. **最小权限策略**（如果不想使用全权限）：
   - `QcloudTCBReadOnlyAccess`（只读）+ 自定义策略包含以下操作：
     - `tcb:DescribeEnvs`（查看环境）
     - `tcb:CreateCloudRunService`（创建服务）
     - `tcb:UpdateCloudRunService`（更新服务）
     - `tcb:DescribeCloudRunServices`（查看服务）
     - `tcb:DescribeCloudRunServiceDetail`（查看服务详情）
     - `tcbr:DescribeCloudRunServerDetail`（查看 CloudRun 服务详情）**重要**
     - `tcbr:CreateCloudRunServer`（创建 CloudRun 服务）
     - `tcbr:UpdateCloudRunServer`（更新 CloudRun 服务）
     - `tcr:CreateRepository`（创建镜像仓库）
     - `tcr:PushImage`（推送镜像）
     - `tcr:PullImage`（拉取镜像）

**推荐**：直接使用 `QcloudTCBFullAccess` + `QcloudTCBRFullAccess`（如果存在）策略，避免权限问题

**注意**：
- 如果看不到 Settings 选项，说明您没有仓库的管理员权限
- Secrets 的值一旦创建就无法再查看，只能删除后重新创建
- 如果遇到权限错误，请检查 API 密钥是否有 CloudBase 相关权限

#### 2. 触发自动部署

- **自动触发**：推送代码到 `dev_tcb` 分支时自动部署
- **手动触发**：在 GitHub Actions 页面手动运行工作流

#### 3. 配置存储挂载（重要）⭐

**重要**：GitHub Actions 工作流**不会自动配置存储挂载**，需要在云托管控制台手动配置一次。

**配置步骤**：
1. 部署完成后，进入 [CloudBase 控制台](https://console.cloud.tencent.com/tcb)
2. 选择您的环境 → 云托管 → 服务管理
3. 找到您的服务（如：`budget-manager`）→ 点击进入服务详情
4. 选择「存储挂载」标签
5. 点击「启用存储挂载」或「新增存储挂载」
6. 配置：
   - **存储类型**：选择「云开发对象存储」（推荐）
   - **存储桶**：选择或创建存储桶
   - **对象存储挂载目录**：`/`
   - **挂载到实例目录**：`/mnt`
7. 保存配置

**注意**：
- ⚠️ 存储挂载需要在**首次部署后手动配置一次**
- ✅ 配置后，每次通过 GitHub Actions 部署新版本时，**存储挂载配置会自动保留**
- ✅ 应用会自动检测 `/mnt` 目录，如果存在则使用持久存储

#### 4. 查看部署状态

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
tcb cloudrun deploy --envId <环境ID> --serviceName <服务名称>
```

或者交互式部署：

```bash
tcb cloudrun deploy
```

按照提示输入：
- 环境ID（如果还没有，会自动创建）
- 服务名称（例如：budget-manager）

CLI 会自动：
1. 检测 Dockerfile（项目根目录下的 Dockerfile）
2. 构建 Docker 镜像
3. 上传到腾讯云容器镜像服务
4. 部署到云托管

**注意**：
- CloudBase CLI 会自动检测项目根目录下的 `Dockerfile`
- 不需要指定 `--dockerfilePath` 参数
- 会自动忽略 `.gitignore` 中列出的文件

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

1. **数据持久化**（已解决）✅：
   - 通过配置存储挂载到 `/mnt`，数据库和备份文件会自动持久化到 COS
   - 应用会自动检测并使用持久存储（如果可用）
   - 无需额外配置，数据不会因容器重启而丢失

2. **文件上传**: 上传的 Excel 文件和导出的文件存储在容器内，建议：
   - 可以配置额外的存储挂载用于文件存储
   - 或定期清理旧文件

3. **密码安全**: 建议通过环境变量设置强密码，不要使用默认密码

4. **资源限制**: 根据实际使用情况配置 CPU 和内存限制

5. **存储性能**: 
   - COS 挂载适合存储数据库文件和备份
   - 频繁访问的文件可以考虑缓存到内存
   - 大文件操作建议分片处理

## 参考文档

- [腾讯云托管 Python 快速开始](https://docs.cloudbase.net/run/quick-start/dockerize-python)
- [CloudBase CLI 文档](https://docs.cloudbase.net/cli/overview)

