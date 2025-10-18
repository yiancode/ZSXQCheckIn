"""
知识星球打卡展示工具 - Flask应用初始化模块
"""
from flask import Flask
from flask_cors import CORS
import logging
from .utils.config_loader import load_config
from .utils.logger import setup_logger


def create_app(config_path='config.yml'):
    """
    Flask应用工厂函数

    Args:
        config_path: 配置文件路径

    Returns:
        Flask应用实例
    """
    app = Flask(__name__)

    # 加载配置
    config = load_config(config_path)
    app.config['ZSXQ_CONFIG'] = config

    # 配置Flask
    flask_config = config.get('系统配置', {}).get('flask', {})
    app.config['DEBUG'] = flask_config.get('debug', False)

    # 配置CORS
    cors_origins = flask_config.get('cors_origins', '*')
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})

    # 配置日志
    log_config = config.get('日志配置', {})
    setup_logger(app, log_config)

    # 注册蓝图
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # 注册错误处理器
    from .routes.errors import register_error_handlers
    register_error_handlers(app)

    # 初始化缓存
    cache_config = config.get('缓存配置', {})
    if cache_config.get('enabled', True):
        from .services.cache_service import init_cache
        init_cache(app, cache_config)

        # 初始化定时任务调度器
        from .services.scheduler import init_scheduler
        init_scheduler(app)

    app.logger.info("Flask应用初始化完成")

    return app
