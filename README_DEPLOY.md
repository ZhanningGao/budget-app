# 🚀 快速部署指南

## 最简单的方式：Railway.app（推荐）

### 1分钟部署步骤：

1. **准备代码**
   ```bash
   # 确保代码已提交到GitHub
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

2. **部署到Railway**
   - 访问 https://railway.app
   - 点击 "Start a New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的仓库
   - 完成！Railway会自动部署

3. **获取访问地址**
   - Railway会分配一个域名，如：`your-app.railway.app`
   - 点击域名即可访问

### 优点：
- ✅ 完全免费（$5/月额度）
- ✅ 自动部署（Git推送即部署）
- ✅ 无需配置服务器
- ✅ 支持自定义域名

---

## 其他平台快速链接

### Render.com
- 访问: https://render.com
- 点击 "New +" → "Web Service"
- 连接GitHub仓库
- 使用配置: `gunicorn --config gunicorn_config.py wsgi:app`

### Fly.io
```bash
fly launch
fly deploy
```

### 腾讯云轻量应用服务器
- 购买服务器（约¥24/月）
- SSH登录后运行 `./deploy.sh`
- 配置Nginx反向代理

---

## 📝 注意事项

### 数据持久化
大多数云平台的文件系统是临时的，重启后会丢失数据。

**解决方案**：
1. 使用平台提供的持久化存储（如Railway的Volume）
2. 定期备份Excel文件到外部存储
3. 使用数据库存储数据（需要修改代码）

### 当前配置
- Excel文件存储在项目根目录
- 上传和导出文件存储在 `uploads/` 和 `exports/` 目录
- 这些目录在云平台上需要配置持久化存储

---

## 🔧 配置持久化存储（Railway示例）

1. 在Railway项目中添加Volume
2. 挂载到 `/app/data`
3. 设置环境变量: `DATA_DIR=/app/data`
4. 将Excel文件复制到Volume中

---

## 📞 需要帮助？

查看详细文档: `DEPLOY.md` 和 `HOSTING.md`

