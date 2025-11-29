# Gunicorn配置文件（生产环境）
import multiprocessing
import os

# 服务器配置
# Railway使用PORT环境变量，如果没有则默认5000
port = os.getenv('PORT', '5000')
bind = f"0.0.0.0:{port}"  # 监听所有网络接口
workers = multiprocessing.cpu_count() * 2 + 1  # 工作进程数
worker_class = "sync"  # 工作模式
worker_connections = 1000
timeout = 120  # 超时时间（秒）
keepalive = 5

# 日志配置
# Railway会自动收集标准输出，使用"-"表示标准输出/错误
accesslog = "-"  # 标准输出（Railway会自动收集）
errorlog = "-"   # 标准错误（Railway会自动收集）
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 进程配置
daemon = False  # 不要以守护进程运行（Railway需要前台运行）
# pidfile = "gunicorn.pid"  # Railway不需要pidfile
umask = 0o007

# 性能优化
preload_app = True  # 预加载应用，节省内存
max_requests = 1000  # 每个worker处理1000个请求后重启
max_requests_jitter = 50  # 随机抖动，避免同时重启

# 安全配置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

