# GitHub Actions 自动部署配置

## 腾讯云托管自动部署

本项目已配置 GitHub Actions 工作流，支持自动部署到腾讯云托管。

## 配置步骤

### 1. 获取腾讯云凭证

1. **获取环境ID**：
   - 登录 [CloudBase 控制台](https://console.cloud.tencent.com/tcb)
   - 在环境列表中查看环境ID

2. **获取 API 密钥**：
   - 登录 [腾讯云控制台](https://console.cloud.tencent.com/)
   - 进入「访问管理」→「API密钥管理」
   - 创建或查看 SecretId 和 SecretKey

### 2. 配置 GitHub Secrets

在 GitHub 仓库中：

1. 进入「Settings」→「Secrets and variables」→「Actions」
2. 点击「New repository secret」添加以下密钥：

   - **TCB_ENV_ID**: 腾讯云环境ID
   - **TCB_SECRET_ID**: 腾讯云 API 密钥 ID
   - **TCB_SECRET_KEY**: 腾讯云 API 密钥 Key

### 3. 触发部署

- **自动部署**：推送代码到 `dev_tcb` 分支时自动触发
- **手动部署**：在「Actions」页面选择工作流，点击「Run workflow」

## 工作流说明

工作流文件：`.github/workflows/cloudbase-deploy.yml`

工作流会执行以下步骤：
1. 检出代码
2. 安装 Node.js 和 CloudBase CLI
3. 登录腾讯云
4. 构建并部署到云托管

## 注意事项

1. 首次部署需要手动配置服务名称和端口
2. 确保 GitHub Secrets 配置正确
3. 部署失败时查看 Actions 日志排查问题

