#!/bin/bash
# 部署脚本

set -e

echo "🚀 开始部署装修预算表管理系统..."

# 检查Python版本
echo "📋 检查Python版本..."
python3 --version

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 创建必要的目录
echo "📁 创建目录..."
mkdir -p uploads exports logs fonts

# 检查Excel文件
if [ ! -f "红玺台复式装修预算表.xlsx" ]; then
    echo "⚠️  警告: Excel文件不存在，请确保文件在项目根目录"
fi

# 检查字体文件
if [ ! -d "fonts" ] || [ -z "$(ls -A fonts/*.ttf 2>/dev/null)" ]; then
    echo "⚠️  警告: 字体文件目录为空，PDF导出可能无法正确显示中文"
fi

echo "✅ 部署准备完成！"
echo ""
echo "启动方式："
echo "  开发环境: python app.py"
echo "  生产环境: gunicorn --config gunicorn_config.py wsgi:app"
echo "  Docker:   docker-compose up -d"

