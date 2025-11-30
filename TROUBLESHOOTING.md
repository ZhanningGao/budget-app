# 故障排查指南

## GitHub Actions 部署问题

### 问题：权限错误 `you are not authorized to perform operation`

**错误信息**：
```
[request id:xxx]you are not authorized to perform operation (tcb:DescribeEnvs)
resource (qcs::tcb:ap-shanghai:uin/xxx:env/*) has no permission
```

**原因**：API 密钥没有 CloudBase 相关权限

**解决方法**：

#### 方法一：使用子账号（推荐）

1. 登录 [腾讯云控制台](https://console.cloud.tencent.com/)
2. 进入「访问管理」→「用户」→「新建子用户」
3. 选择「编程访问」，创建子用户
4. 为子用户添加策略：
   - 搜索并添加：`QcloudTCBFullAccess`（CloudBase 全读写访问权限）
5. 使用子用户的 SecretId 和 SecretKey 配置到 GitHub Secrets

#### 方法二：为主账号 API 密钥添加权限

1. 进入「访问管理」→「策略」
2. 搜索 `QcloudTCBFullAccess`
3. 将该策略关联到您的账号
4. 或创建自定义策略，包含以下操作：
   - `tcb:DescribeEnvs`
   - `tcb:CreateCloudRunService`
   - `tcb:UpdateCloudRunService`
   - `tcb:DescribeCloudRunServices`
   - `tcb:DescribeCloudRunServiceDetail`
   - `tcr:CreateRepository`
   - `tcr:PushImage`

#### 方法三：检查权限配置

1. 进入「访问管理」→「用户」→ 选择您的账号
2. 查看「关联策略」，确保有 CloudBase 相关权限
3. 如果没有，点击「关联策略」添加 `QcloudTCBFullAccess`

### 问题：找不到 GitHub Secrets 配置入口

**解决方法**：
1. 确认您是仓库的管理员或所有者
2. 进入仓库主页 → 点击 **Settings** 标签（在 Code、Issues 等标签旁边）
3. 左侧菜单查找：
   - **Secrets and variables** → **Actions**（新版本）
   - 或直接找到 **Secrets**（旧版本）
4. 如果仍然找不到，联系仓库所有者

### 问题：命令参数错误 `unknown option '--dockerfilePath'`

**错误信息**：
```
error: unknown option '--dockerfilePath'
```

**原因**：CloudBase CLI 2.x 版本不支持 `--dockerfilePath` 参数

**解决方法**：
- CloudBase CLI 会自动检测项目根目录下的 `Dockerfile`
- 移除工作流中的 `--dockerfilePath` 参数
- 确保 `Dockerfile` 文件在项目根目录

### 问题：部署失败，查看日志

1. 进入 GitHub 仓库的 **Actions** 页面
2. 点击失败的 workflow 运行
3. 查看详细的错误日志
4. 根据错误信息进行排查

## 其他常见问题

### 问题：环境ID找不到

1. 登录 [CloudBase 控制台](https://console.cloud.tencent.com/tcb)
2. 在环境列表中查看环境ID（格式类似：`env-xxxxx`）
3. 如果没有环境，需要先创建一个环境

### 问题：服务名称冲突

如果服务名称已存在，可以：
1. 在 GitHub Secrets 中设置 `TCB_SERVICE_NAME` 为其他名称
2. 或在云托管控制台删除旧服务后重新部署

