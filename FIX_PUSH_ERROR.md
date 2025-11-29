# 解决 "Repository not found" 错误

## 🔍 问题原因

错误信息：`fatal: repository 'https://github.com/ZhanningGao/budget-app.git/' not found`

**原因**：GitHub上还没有创建这个仓库。

## ✅ 解决步骤

### 步骤1: 创建GitHub仓库

1. **打开创建页面**
   - 直接访问：https://github.com/new
   - 或登录GitHub后，点击右上角 "+" → "New repository"

2. **填写仓库信息**
   - **Repository name**: `budget-app`
   - **Description**: `装修预算表管理系统`（可选）
   - **Visibility**: 选择 Public 或 Private
   - **重要**: 不要勾选以下选项：
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license

3. **创建仓库**
   - 点击绿色的 "Create repository" 按钮

### 步骤2: 推送代码

创建仓库后，在终端运行：

```bash
cd /Users/gzn/gaozn/code/hxt

# 确保分支名为main
git branch -M main

# 推送代码
git push -u origin main
```

### 步骤3: 认证

推送时会要求输入用户名和密码：

- **Username**: `ZhanningGao`
- **Password**: 使用 **Personal Access Token**（不是GitHub密码）

#### 如何获取Personal Access Token：

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写信息：
   - **Note**: `budget-app-push`（描述，可选）
   - **Expiration**: 选择过期时间（建议90天或No expiration）
   - **Select scopes**: 勾选 `repo`（会同时勾选所有子权限）
4. 点击 "Generate token"
5. **重要**: 立即复制token（只显示一次！）
6. 推送时，将token作为密码输入

## 🔄 如果仓库名称不同

如果你想使用不同的仓库名称，需要修改远程地址：

```bash
# 移除现有远程仓库
git remote remove origin

# 添加新的远程仓库（替换YOUR_REPO_NAME）
git remote add origin https://github.com/ZhanningGao/YOUR_REPO_NAME.git

# 推送
git push -u origin main
```

## 🆘 其他常见问题

### 问题1: 认证失败

**解决方案**：
- 确认使用Token而不是密码
- 检查Token是否有 `repo` 权限
- 如果Token过期，生成新的Token

### 问题2: 权限不足

**解决方案**：
- 确认你是仓库的所有者或有推送权限
- 检查仓库是Public还是Private（Private需要权限）

### 问题3: 网络问题

**解决方案**：
- 检查网络连接
- 如果在中国，可能需要使用代理
- 或使用SSH方式（需要配置SSH密钥）

## 📝 使用SSH方式（可选，更安全）

如果你配置了SSH密钥，可以使用SSH URL：

```bash
# 修改远程地址为SSH
git remote set-url origin git@github.com:ZhanningGao/budget-app.git

# 推送
git push -u origin main
```

## ✅ 验证推送成功

推送成功后，你应该看到类似输出：

```
Enumerating objects: 28, done.
Counting objects: 100% (28/28), done.
Delta compression using up to 8 threads
Compressing objects: 100% (26/26), done.
Writing objects: 100% (28/28), done.
Total 28 (delta 2), reused 0 (delta 0)
remote: Resolving deltas: 100% (2/2), done.
To https://github.com/ZhanningGap/budget-app.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

然后访问 https://github.com/ZhanningGao/budget-app 就能看到你的代码了！

