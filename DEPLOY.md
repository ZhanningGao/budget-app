# 部署指南

本指南提供了多种方式将装修预算表管理系统部署到外网。

## 📋 目录

1. [快速测试 - ngrok内网穿透](#方案1-快速测试---ngrok内网穿透)
2. [云服务器部署 - 使用Gunicorn](#方案2-云服务器部署---使用gunicorn)
3. [Docker部署](#方案3-docker部署)
4. [安全建议](#安全建议)

---

## 方案1: 快速测试 - ngrok内网穿透

**适用场景**: 快速测试、临时访问、开发调试

### 步骤

1. **安装ngrok**
   ```bash
   # macOS
   brew install ngrok
   
   # 或下载: https://ngrok.com/download
   ```

2. **启动Flask应用**
   ```bash
   python app.py
   ```

3. **启动ngrok**
   ```bash
   ngrok http 5000
   ```

4. **获取公网地址**
   ngrok会显示类似这样的地址：
   ```
   Forwarding  https://abc123.ngrok.io -> http://localhost:5000
   ```
   使用这个地址即可从外网访问。

**优点**: 快速、简单、无需服务器  
**缺点**: 免费版地址会变化，有流量限制

---

## 方案2: 云服务器部署 - 使用Gunicorn

**适用场景**: 生产环境、长期使用

### 前置要求

- 一台云服务器（阿里云、腾讯云、AWS等）
- 域名（可选，但推荐）
- SSH访问权限

### 步骤

#### 1. 上传代码到服务器

```bash
# 在本地打包
tar -czf budget-app.tar.gz \
    app.py requirements.txt templates/ fonts/ \
    红玺台复式装修预算表.xlsx \
    gunicorn_config.py wsgi.py

# 上传到服务器
scp budget-app.tar.gz user@your-server-ip:/opt/
```

#### 2. 在服务器上安装依赖

```bash
# SSH登录服务器
ssh user@your-server-ip

# 解压文件
cd /opt
tar -xzf budget-app.tar.gz
cd budget-app

# 安装Python和依赖
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # 生产环境WSGI服务器

# 创建必要目录
mkdir -p uploads exports logs
```

#### 3. 配置Gunicorn

编辑 `gunicorn_config.py`，确保配置正确。

#### 4. 使用Systemd管理服务（推荐）

```bash
# 复制服务文件
sudo cp budget-app.service /etc/systemd/system/

# 修改服务文件中的路径（如果需要）
sudo nano /etc/systemd/system/budget-app.service

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable budget-app
sudo systemctl start budget-app

# 查看状态
sudo systemctl status budget-app

# 查看日志
sudo journalctl -u budget-app -f
```

#### 5. 配置Nginx反向代理（推荐）

```bash
# 安装Nginx
sudo apt-get install -y nginx

# 创建Nginx配置
sudo nano /etc/nginx/sites-available/budget-app
```

Nginx配置内容：
```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名

    client_max_body_size 20M;  # 允许上传大文件

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/budget-app /etc/nginx/sites-enabled/
sudo nginx -t  # 测试配置
sudo systemctl restart nginx
```

#### 6. 配置HTTPS（推荐）

使用Let's Encrypt免费SSL证书：

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 方案3: Docker部署

**适用场景**: 容器化部署、易于迁移

### 步骤

#### 1. 构建Docker镜像

```bash
docker build -t budget-app .
```

#### 2. 运行容器

```bash
docker run -d \
  --name budget-app \
  -p 5000:5000 \
  -v $(pwd)/红玺台复式装修预算表.xlsx:/app/红玺台复式装修预算表.xlsx \
  -v $(pwd)/exports:/app/exports \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/fonts:/app/fonts \
  budget-app
```

#### 3. 使用Docker Compose（推荐）

```bash
docker-compose up -d
```

查看日志：
```bash
docker-compose logs -f
```

停止服务：
```bash
docker-compose down
```

---

## 安全建议

### 1. 防火墙配置

```bash
# 只开放必要端口
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 2. 禁用Debug模式

确保生产环境不使用 `debug=True`，使用Gunicorn运行。

### 3. 定期备份

```bash
# 创建备份脚本
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
cp /opt/budget-app/红玺台复式装修预算表.xlsx $BACKUP_DIR/budget_$DATE.xlsx
# 只保留最近30天的备份
find $BACKUP_DIR -name "budget_*.xlsx" -mtime +30 -delete
EOF

chmod +x backup.sh

# 添加到crontab（每天凌晨2点备份）
crontab -e
# 添加: 0 2 * * * /opt/budget-app/backup.sh
```

### 4. 监控和日志

- 使用 `systemctl status budget-app` 监控服务状态
- 查看日志: `sudo journalctl -u budget-app -f`
- 配置日志轮转，避免日志文件过大

### 5. 访问控制（可选）

如果需要限制访问，可以在Nginx配置中添加：

```nginx
# 基本认证
location / {
    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://127.0.0.1:5000;
}
```

创建密码文件：
```bash
sudo apt-get install -y apache2-utils
sudo htpasswd -c /etc/nginx/.htpasswd username
```

---

## 常见问题

### Q: 服务无法启动？

A: 检查：
- Python版本（需要3.8+）
- 依赖是否安装完整
- 端口是否被占用
- 日志文件中的错误信息

### Q: 外网无法访问？

A: 检查：
- 防火墙是否开放端口
- 云服务器安全组规则
- Nginx配置是否正确
- 服务是否正常运行

### Q: PDF导出失败？

A: 确保：
- `fonts/` 目录中有字体文件
- 字体文件权限正确
- ReportLab已正确安装

### Q: 上传文件失败？

A: 检查：
- `uploads/` 目录权限
- Nginx的 `client_max_body_size` 配置
- Flask的 `MAX_CONTENT_LENGTH` 配置

---

## 更新应用

```bash
# 停止服务
sudo systemctl stop budget-app

# 备份数据
cp 红玺台复式装修预算表.xlsx 红玺台复式装修预算表.xlsx.backup

# 更新代码
git pull  # 或手动上传新文件

# 更新依赖
source venv/bin/activate
pip install -r requirements.txt

# 重启服务
sudo systemctl start budget-app
```

---

## 技术支持

如有问题，请检查：
1. 应用日志: `sudo journalctl -u budget-app -n 100`
2. Nginx日志: `/var/log/nginx/error.log`
3. Gunicorn日志: `logs/error.log`

