# 托管平台部署指南

本文档介绍如何将应用部署到各种托管平台。

## 🌟 推荐平台（按易用性排序）

### 1. Railway.app ⭐⭐⭐⭐⭐
**优点**: 
- 免费额度充足（$5/月）
- 支持Git自动部署
- 配置简单，一键部署
- 支持自定义域名

**部署步骤**:
1. 访问 https://railway.app
2. 使用GitHub登录
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择你的仓库
5. Railway会自动检测Python项目并部署

**配置文件**: 已包含 `railway.json`

---

### 2. Render.com ⭐⭐⭐⭐⭐
**优点**:
- 免费套餐可用（有休眠限制）
- 支持Git自动部署
- 配置简单
- 支持Web服务

**部署步骤**:
1. 访问 https://render.com
2. 注册账号（可用GitHub登录）
3. 点击 "New +" → "Web Service"
4. 连接GitHub仓库
5. 配置：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --config gunicorn_config.py wsgi:app`
   - **Environment**: `Python 3`

**配置文件**: 已包含 `render.yaml`

---

### 3. Fly.io ⭐⭐⭐⭐
**优点**:
- 免费额度（3个共享CPU应用）
- 全球CDN
- 配置灵活

**部署步骤**:
1. 安装Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. 登录: `fly auth login`
3. 初始化: `fly launch`
4. 部署: `fly deploy`

**配置文件**: 已包含 `fly.toml`

---

### 4. Heroku ⭐⭐⭐
**优点**:
- 老牌平台，稳定
- 生态丰富

**缺点**:
- 已取消免费套餐（需付费）

**部署步骤**:
1. 安装Heroku CLI
2. `heroku login`
3. `heroku create your-app-name`
4. `git push heroku main`

**配置文件**: 已包含 `Procfile`

---

### 5. 腾讯云 / 阿里云 ⭐⭐⭐⭐
**优点**:
- 国内访问快
- 价格相对便宜
- 支持多种部署方式

**部署方式**:
- 轻量应用服务器（推荐）
- 容器服务
- Serverless（函数计算）

---

## 📋 平台对比

| 平台 | 免费额度 | 易用性 | 国内访问 | 推荐度 |
|------|---------|--------|---------|--------|
| Railway | $5/月 | ⭐⭐⭐⭐⭐ | 一般 | ⭐⭐⭐⭐⭐ |
| Render | 有限 | ⭐⭐⭐⭐⭐ | 一般 | ⭐⭐⭐⭐ |
| Fly.io | 3个应用 | ⭐⭐⭐⭐ | 一般 | ⭐⭐⭐⭐ |
| Heroku | 需付费 | ⭐⭐⭐ | 慢 | ⭐⭐⭐ |
| 腾讯云 | 需付费 | ⭐⭐⭐ | 快 | ⭐⭐⭐⭐ |
| 阿里云 | 需付费 | ⭐⭐⭐ | 快 | ⭐⭐⭐⭐ |

---

## 🚀 快速开始（推荐：Railway）

### 方法1: 通过GitHub部署（推荐）

1. **准备GitHub仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-username/budget-app.git
   git push -u origin main
   ```

2. **在Railway部署**
   - 访问 https://railway.app
   - 登录（使用GitHub）
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的仓库
   - Railway会自动部署！

3. **配置环境变量**（如果需要）
   - 在Railway项目设置中添加环境变量
   - 例如: `FLASK_ENV=production`

4. **获取访问地址**
   - Railway会自动分配一个域名
   - 格式: `your-app.railway.app`
   - 也可以绑定自定义域名

### 方法2: 通过Railway CLI

```bash
# 安装Railway CLI
npm i -g @railway/cli

# 登录
railway login

# 初始化项目
railway init

# 部署
railway up
```

---

## 🔧 平台特定配置

### Railway
- 自动检测Python项目
- 使用 `railway.json` 配置
- 支持环境变量

### Render
- 使用 `render.yaml` 配置
- 需要指定启动命令
- 支持自动部署

### Fly.io
- 使用 `fly.toml` 配置
- 需要安装Fly CLI
- 支持全球部署

---

## ⚠️ 注意事项

### 1. 数据持久化
- 大多数平台的文件系统是临时的
- **重要**: Excel文件需要存储在外部存储（如S3）或数据库
- 或者使用平台提供的持久化存储

### 2. 环境变量
- 敏感信息（如API Key）使用环境变量
- 不要提交到Git仓库

### 3. 资源限制
- 免费套餐通常有资源限制
- 注意内存和CPU使用

### 4. 国内访问
- 国外平台在国内访问可能较慢
- 考虑使用CDN或国内平台

---

## 📝 推荐方案

### 方案A: 快速测试（免费）
**Railway** → 免费额度充足，部署简单

### 方案B: 生产环境（国内）
**腾讯云轻量应用服务器** → 国内访问快，价格合理

### 方案C: 企业级（稳定）
**阿里云ECS + Docker** → 稳定可靠，可扩展

---

## 🆘 遇到问题？

1. 查看平台文档
2. 检查日志输出
3. 确认配置文件正确
4. 验证环境变量设置

