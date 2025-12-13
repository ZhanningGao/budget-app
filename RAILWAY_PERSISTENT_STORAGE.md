# Railway 持久化存储配置指南

## ✅ Railway 支持持久化存储

Railway 提供了 **Volume** 功能，可以实现数据持久化存储。即使服务重启或重新部署，数据也不会丢失。

---

## 📋 配置步骤

### 方法一：通过 Railway Web 控制台配置（推荐）

1. **登录 Railway**
   - 访问 https://railway.app
   - 登录你的账号

2. **创建 Volume**
   - 进入你的项目
   - 点击服务（Service）
   - 在左侧菜单找到 **"Volumes"** 或 **"存储"**
   - 点击 **"New Volume"** 或 **"创建存储卷"**

3. **配置 Volume**
   - **Volume 名称**：`budget-data`（或任意名称）
   - **挂载路径**：`/app/data`（或 `/data`）
   - **大小**：建议至少 1GB（根据数据量调整）

4. **设置环境变量**
   - 在服务设置中找到 **"Variables"** 或 **"环境变量"**
   - 添加环境变量：
     ```
     DATA_DIR=/app/data
     ```
   - 保存环境变量

5. **重新部署**
   - Railway 会自动检测到 Volume 和环境变量的变化
   - 或者手动触发重新部署

### 方法二：通过 Railway CLI 配置

```bash
# 安装 Railway CLI
npm i -g @railway/cli

# 登录
railway login

# 进入项目目录
cd /path/to/your/project

# 创建 Volume
railway volume create budget-data --size 1GB

# 挂载 Volume 到服务
railway volume mount budget-data --mount-path /app/data

# 设置环境变量
railway variables set DATA_DIR=/app/data

# 部署
railway up
```

---

## 🔧 代码配置说明

当前代码已经支持通过 `DATA_DIR` 环境变量指定数据目录：

```python
# database.py 中的配置
LOCAL_DATA_DIR = os.getenv('DATA_DIR', '.')  # 默认当前目录
LOCAL_DB_FILE = os.path.join(LOCAL_DATA_DIR, 'budget.db')
LOCAL_BACKUP_DIR = os.path.join(LOCAL_DATA_DIR, 'backups')
```

**工作原理**：
1. 代码会优先检查 `/mnt` 目录（用于腾讯云 COS 挂载）
2. 如果 `/mnt` 不存在，则使用 `DATA_DIR` 环境变量指定的目录
3. 如果 `DATA_DIR` 未设置，则使用当前目录（`.`）

---

## 📁 数据存储位置

配置完成后，以下数据会存储在 Volume 中：

- **数据库文件**：`/app/data/budget.db`
- **备份文件**：`/app/data/backups/`
- **上传文件**：`/app/data/uploads/`（如果配置了）
- **导出文件**：`/app/data/exports/`（如果配置了）

---

## ✅ 验证配置

### 1. 检查 Volume 是否挂载成功

在 Railway 控制台查看服务日志，应该能看到类似信息：
```
✅ 数据库路径: /app/data/budget.db
```

### 2. 检查数据是否持久化

1. 在应用中添加一些数据
2. 重启服务（在 Railway 控制台点击 "Restart"）
3. 检查数据是否还在

---

## 💰 费用说明

- **免费套餐**：Railway 提供 $5/月的免费额度
- **Volume 费用**：Volume 按使用量计费，通常很小
- **建议**：1GB 的 Volume 对于大多数应用已经足够

---

## ⚠️ 注意事项

### 1. Volume 大小限制
- 免费套餐可能有大小限制
- 建议根据实际数据量设置合适的大小
- 可以随时扩容

### 2. 数据备份
- Volume 中的数据是持久化的，但建议定期备份
- 可以使用应用内置的备份功能
- 或者定期导出数据到外部存储

### 3. 迁移数据
如果之前没有使用 Volume，需要迁移数据：

```bash
# 方法1：通过 Railway CLI
railway run bash
# 然后在容器内复制数据到 Volume

# 方法2：通过应用功能
# 使用应用内的"备份/恢复"功能导出数据
# 然后在新的 Volume 环境中恢复
```

### 4. 多服务共享
- 一个 Volume 可以挂载到多个服务
- 但要注意并发访问的问题（SQLite 支持 WAL 模式，可以处理并发）

---

## 🔄 与腾讯云 COS 的对比

| 特性 | Railway Volume | 腾讯云 COS |
|------|---------------|-----------|
| 配置难度 | ⭐⭐⭐⭐⭐ 简单 | ⭐⭐⭐ 中等 |
| 费用 | 按使用量计费 | 按存储和流量计费 |
| 性能 | 本地磁盘，速度快 | 网络存储，速度较慢 |
| 可靠性 | 高 | 非常高 |
| 适用场景 | 中小型应用 | 大型应用，需要高可用 |

**建议**：
- 如果使用 Railway 部署，优先使用 Railway Volume
- 如果使用腾讯云部署，使用 COS 挂载

---

## 📚 相关文档

- [Railway Volume 官方文档](https://docs.railway.app/develop/storage)
- [Railway 环境变量配置](https://docs.railway.app/develop/variables)
- [项目部署文档](./README_DEPLOY.md)

---

## 🆘 常见问题

### Q: Volume 创建后数据丢失？
A: 检查环境变量 `DATA_DIR` 是否正确设置，以及挂载路径是否正确。

### Q: 如何查看 Volume 使用情况？
A: 在 Railway 控制台的 Volume 页面可以查看使用量和大小。

### Q: 可以同时使用 Volume 和外部存储吗？
A: 可以，代码会优先使用 `/mnt`（外部存储），如果不存在则使用 `DATA_DIR`（Volume）。

### Q: 如何迁移到其他平台？
A: 使用应用内的备份功能导出数据，然后在其他平台恢复。

