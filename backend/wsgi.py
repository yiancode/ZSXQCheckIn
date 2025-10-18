"""
WSGI入口文件 - 用于Gunicorn等WSGI服务器
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app import create_app

# 加载配置
config_path = os.getenv('CONFIG_PATH', 'config.yml')

# 创建应用实例
application = create_app(config_path)
app = application

if __name__ == '__main__':
    app.run()
