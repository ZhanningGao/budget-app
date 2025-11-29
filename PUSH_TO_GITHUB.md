# 推送到GitHub指南

## ✅ Git仓库已初始化并提交

代码已经准备好推送到GitHub了！

## 📋 推送步骤

### 方法1: 在GitHub网站创建仓库（推荐）

1. **访问GitHub并登录**
   - 打开 https://github.com
   - 登录你的账号

2. **创建新仓库**
   - 点击右上角 "+" → "New repository"
   - 仓库名称: `budget-app` (或你喜欢的名字)
   - 描述: `装修预算表管理系统`
   - 选择: **Public** 或 **Private**
   - **不要**勾选 "Initialize with README"（我们已经有了）
   - 点击 "Create repository"

3. **推送代码**
   在终端运行以下命令（GitHub会显示这些命令，但我们已经准备好了）：
   
   ```bash
   cd /Users/gzn/gaozn/code/hxt
   
   # 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
   git remote add origin https://github.com/ZhanningGao/budget-app.git
   
   # 推送代码
   git branch -M main
   git push -u origin main
   ```

### 方法2: 使用GitHub CLI（如果已安装）

```bash
# 创建并推送（会自动创建GitHub仓库）
gh repo create budget-app --public --source=. --remote=origin --push
```

### 方法3: 如果仓库已存在

如果你已经在GitHub上创建了仓库，只需要：

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/budget-app.git

# 推送代码
git push -u origin main
```

## 🔐 认证方式

### 使用Personal Access Token（推荐）

1. **生成Token**
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 点击 "Generate new token (classic)"
   - 勾选 `repo` 权限
   - 生成并复制token

2. **推送时使用Token**
   ```bash
   # 当提示输入密码时，使用token而不是GitHub密码
   git push -u origin main
   # Username: your-username
   # Password: your-token-here
   ```

### 使用SSH（更安全）

1. **生成SSH密钥**（如果还没有）
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **添加SSH密钥到GitHub**
   ```bash
   # 复制公钥
   cat ~/.ssh/id_ed25519.pub
   # 然后添加到 GitHub → Settings → SSH and GPG keys
   ```

3. **使用SSH URL**
   ```bash
   git remote set-url origin git@github.com:YOUR_USERNAME/budget-app.git
   git push -u origin main
   ```

## 📝 后续操作

推送成功后，你可以：

1. **在Railway部署**（推荐）
   - 访问 https://railway.app
   - 连接GitHub仓库
   - 自动部署！

2. **查看代码**
   - 访问 `https://github.com/YOUR_USERNAME/budget-app`

3. **继续开发**
   ```bash
   # 修改代码后
   git add .
   git commit -m "描述你的修改"
   git push
   ```

## ⚠️ 注意事项

- **不要提交敏感信息**：`.config.json` 已在 `.gitignore` 中
- **Excel文件**：如果文件较大，考虑使用Git LFS或不上传
- **环境变量**：敏感配置使用环境变量，不要提交到代码库

## 🆘 遇到问题？

### 错误: remote origin already exists
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/budget-app.git
```

### 错误: authentication failed
- 检查用户名和token是否正确
- 或使用SSH方式

### 错误: large file
如果Excel文件太大，可以：
```bash
# 从git中移除但保留本地文件
git rm --cached 红玺台复式装修预算表.xlsx
git commit -m "Remove large Excel file from git"
# 然后添加到.gitignore
```

