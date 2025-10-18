"""
日志配置模块
"""
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logger(app, log_config):
    """
    配置应用日志

    Args:
        app: Flask应用实例
        log_config: 日志配置字典
    """
    # 设置日志级别
    level_str = log_config.get('level', 'INFO')
    level = getattr(logging, level_str.upper(), logging.INFO)
    app.logger.setLevel(level)

    # 日志格式
    log_format = log_config.get(
        'format',
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    formatter = logging.Formatter(log_format)

    # 控制台处理器
    if log_config.get('console', True):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)

    # 文件处理器
    log_file = log_config.get('file', 'logs/app.log')
    if log_file:
        # 确保日志目录存在
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # 创建RotatingFileHandler (最大10MB,保留5个备份)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

    app.logger.info(f"日志系统初始化完成 (级别: {level_str})")
