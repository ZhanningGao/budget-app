# Dockerfile for 装修预算表管理系统
# 使用官方 Python 轻量级镜像（符合腾讯云托管推荐）
FROM python:3-alpine

# 容器默认时区为UTC，设置时区为上海时间
RUN apk add tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo Asia/Shanghai > /etc/timezone

ENV APP_HOME /app
WORKDIR $APP_HOME

# 将本地代码拷贝到容器内
COPY . .

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV GUNICORN_WORKERS=2
ENV GUNICORN_THREADS=4
ENV GUNICORN_TIMEOUT=60

# 创建必要的目录
RUN mkdir -p uploads exports logs fonts backups

# 安装依赖到指定的/install文件夹
# 选用国内镜像源以提高下载速度（腾讯云镜像）
RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple && \
    pip config set global.trusted-host mirrors.cloud.tencent.com && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 暴露端口（腾讯云托管默认使用80端口，可通过环境变量配置）
EXPOSE 80

# 启动 Web 服务
# 如果您的容器实例拥有多个 CPU 核心，我们推荐您把线程数设置为与 CPU 核心数一致
# 使用环境变量 PORT（腾讯云托管会自动设置）或默认80端口
# 注意：腾讯云托管会自动设置 PORT 环境变量，如果没有设置则使用80
CMD exec gunicorn --bind :${PORT:-80} --workers ${GUNICORN_WORKERS} --threads ${GUNICORN_THREADS} --timeout ${GUNICORN_TIMEOUT} wsgi:app

