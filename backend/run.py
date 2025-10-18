"""
Flask应用启动入口
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app import create_app
from app.utils.config_loader import load_config


def main():
    """
    主函数 - 启动Flask应用
    """
    # 加载配置
    config_path = os.getenv('CONFIG_PATH', 'config.yml')

    try:
        # 创建Flask应用
        app = create_app(config_path)

        # 获取Flask配置
        flask_config = app.config['ZSXQ_CONFIG'].get('系统配置', {}).get('flask', {})
        host = flask_config.get('host', '0.0.0.0')
        port = flask_config.get('port', 5000)
        debug = flask_config.get('debug', False)

        # 启动应用
        app.logger.info(f"启动Flask应用: http://{host}:{port}")
        app.run(host=host, port=port, debug=debug)

    except FileNotFoundError as e:
        print(f"错误: {str(e)}")
        sys.exit(1)
    except ValueError as e:
        print(f"配置错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"启动失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
