# Gunicorn配置文件（生产环境）
import multiprocessing
import os

# 服务器配置
bind = "0.0.0.0:5000"  # 监听所有网络接口
workers = multiprocessing.cpu_count() * 2 + 1  # 工作进程数
worker_class = "sync"  # 工作模式
worker_connections = 1000
timeout = 120  # 超时时间（秒）
keepalive = 5

# 日志配置
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 进程配置
daemon = False  # 不要以守护进程运行（使用systemd管理）
pidfile = "gunicorn.pid"
umask = 0o007

# 性能优化
preload_app = True  # 预加载应用，节省内存
max_requests = 1000  # 每个worker处理1000个请求后重启
max_requests_jitter = 50  # 随机抖动，避免同时重启

# 安全配置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

