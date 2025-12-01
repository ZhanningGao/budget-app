# 故障排查指南

## GitHub Actions 部署问题

### 问题：权限错误 `you are not authorized to perform operation`

**错误信息示例**：
```
[request id:xxx]you are not authorized to perform operation (tcb:DescribeEnvs)
resource (qcs::tcb:ap-shanghai:uin/xxx:env/*) has no permission
```

或

```
[DescribeCloudRunServerDetail] you are not authorized to perform operation (tcbr:DescribeCloudRunServerDetail)
resource (qcs::tcbr:ap-shanghai::env/xxx) has no permission
```

**原因**：API 密钥没有 CloudBase 或 CloudRun 相关权限

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
   - `tcb:DescribeEnvs`（查看环境）
   - `tcb:CreateCloudRunService`（创建服务）
   - `tcb:UpdateCloudRunService`（更新服务）
   - `tcb:DescribeCloudRunServices`（查看服务列表）
   - `tcb:DescribeCloudRunServiceDetail`（查看服务详情）
   - `tcbr:DescribeCloudRunServerDetail`（查看 CloudRun 服务详情）**重要**
   - `tcbr:CreateCloudRunServer`（创建 CloudRun 服务）
   - `tcbr:UpdateCloudRunServer`（更新 CloudRun 服务）
   - `tcr:CreateRepository`（创建镜像仓库）
   - `tcr:PushImage`（推送镜像）
   - `tcr:PullImage`（拉取镜像）

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

### 问题：部署确认中断 `Process completed with exit code 130`

**错误信息**：
```
? About to start deployment, confirm to continue? (Y/n) 
Error: Process completed with exit code 130.
```

**原因**：CloudBase CLI 在非交互式环境（GitHub Actions）中等待用户确认，无法输入导致进程中断

**解决方法**：
- 使用 `echo "y" |` 管道自动输入确认
- 或使用 `yes |` 命令自动确认所有提示
- 工作流已更新为自动确认模式

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

### 问题：存储挂载失败 `cosfs 挂载失败`

**错误信息**：
```
ERROR: cosfs 挂载失败
Warn:option url has invalid format:cos.ap-shanghai.myqcloud.com, 
correct example:-ourl=http://cos.ap-guangzhou.myqcloud.com
```

**原因**：存储挂载配置中的 COS URL 格式不正确，缺少 `http://` 或 `https://` 前缀

**解决方法**：

#### 方法一：重新配置存储挂载（推荐）

1. 进入云托管控制台 → 服务详情 → **存储挂载**
2. **删除现有的存储挂载配置**
3. 重新添加存储挂载：
   - **存储类型**：选择「云开发对象存储」（推荐，系统会自动处理 URL 格式）
   - 或选择「腾讯云对象存储」，确保 URL 格式正确
4. **配置挂载路径**：
   - 对象存储挂载目录：`/`
   - 挂载到实例目录：`/mnt`
5. 保存配置

#### 方法二：检查存储桶配置

1. 确认存储桶的地域（如：上海 ap-shanghai）
2. 如果使用「腾讯云对象存储」，确保：
   - 存储桶名称格式正确
   - 地域信息正确
   - 访问密钥配置正确

#### 方法三：使用云开发对象存储（最简单）

- 选择「云开发对象存储」而不是「腾讯云对象存储」
- 系统会自动处理 URL 格式和配置
- 无需手动配置访问密钥（如果使用云开发对象存储）

#### 方法四：临时禁用存储挂载

如果存储挂载持续失败，可以：
1. 暂时禁用存储挂载
2. 应用会使用本地存储（容器内）
3. 数据不会持久化，但服务可以正常运行
4. 修复存储挂载配置后重新启用

**注意**：
- 存储挂载失败不会影响应用启动，但数据不会持久化
- 应用会自动检测 `/mnt` 目录，如果不存在会使用本地存储
- 建议优先使用「云开发对象存储」，配置更简单

### 问题：400 Bad Request HTTP ERROR

**错误信息**：
```
✖ 400 Bad Request HTTP ERROR
Error: 400 Bad Request HTTP ERROR
```

**可能原因**：
1. **服务名称格式不符合规范**
   - 服务名称只能包含小写字母、数字、连字符（-）
   - 不能包含下划线、空格、特殊字符
   - 必须以字母开头和结尾
   - 长度限制：1-40 个字符
   - 示例：`budget-manager` ✅，`budget_manager` ❌，`Budget Manager` ❌

2. **环境ID格式错误**
   - 环境ID格式应为：`env-xxxxx`
   - 检查 GitHub Secrets 中的 `TCB_ENV_ID` 是否正确
   - 确保没有多余的空格或换行符

3. **Dockerfile 问题**
   - 确保 Dockerfile 在项目根目录
   - 检查 Dockerfile 语法是否正确
   - 确保 Dockerfile 中没有语法错误

4. **API 密钥权限不足**
   - 虽然能登录，但可能缺少创建服务的权限
   - 需要 `tcb:CreateCloudRunService` 权限

**解决方法**：

#### 方法一：检查并修复服务名称
1. 确保服务名称符合规范（小写字母、数字、连字符）
2. 如果服务名称包含特殊字符，修改为符合规范的名称
3. 工作流已自动规范化服务名称，但建议在 GitHub Secrets 中直接使用规范名称

#### 方法二：验证环境ID
1. 登录 [CloudBase 控制台](https://console.cloud.tencent.com/tcb)
2. 查看环境列表，确认环境ID格式为 `env-xxxxx`
3. 复制环境ID（不要包含空格）
4. 更新 GitHub Secrets 中的 `TCB_ENV_ID`

#### 方法三：检查 Dockerfile
1. 确保 `Dockerfile` 在项目根目录
2. 检查 Dockerfile 语法是否正确
3. 尝试本地构建测试：`docker build -t test .`

#### 方法四：验证 API 权限
1. 确保 API 密钥有 `QcloudTCBFullAccess` 权限
2. 或至少包含 `tcb:CreateCloudRunService` 权限
3. 参考「权限错误」部分的解决方法

#### 方法五：使用交互式部署测试
在本地运行：
```bash
tcb login
tcb cloudrun deploy
```
按照提示输入参数，查看具体错误信息

#### 方法六：查看详细日志
1. 在 GitHub Actions 中查看完整的错误日志
2. 检查是否有更详细的错误信息
3. 查看 CloudBase 控制台的部署日志
4. 检查是否有更具体的错误提示

