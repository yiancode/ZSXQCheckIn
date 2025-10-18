#!/bin/bash
# 开发环境启动脚本

echo "========================================="
echo "知识星球打卡展示工具 - 开发环境启动"
echo "========================================="

# 检查配置文件
if [ ! -f "config.yml" ]; then
    echo "错误: config.yml 不存在"
    echo "请复制 config.example.yml 为 config.yml 并填入真实配置"
    exit 1
fi

# 检查Python虚拟环境
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装Python依赖..."
pip install -r backend/requirements.txt

# 检查Redis
echo "检查Redis连接..."
if ! redis-cli ping > /dev/null 2>&1; then
    echo "警告: Redis未运行,缓存功能将不可用"
    echo "可以使用命令启动Redis: redis-server"
fi

# 创建日志目录
mkdir -p logs

# 启动Flask应用
echo "启动Flask应用..."
export FLASK_ENV=development
python backend/run.py
