"""
配置文件加载模块
"""
import os
import yaml
from pathlib import Path


def load_config(config_path='config.yml'):
    """
    加载YAML配置文件

    Args:
        config_path: 配置文件路径(相对于项目根目录)

    Returns:
        dict: 配置字典

    Raises:
        FileNotFoundError: 配置文件不存在
        yaml.YAMLError: YAML格式错误
    """
    # 获取项目根目录
    root_dir = Path(__file__).parent.parent.parent.parent
    full_path = root_dir / config_path

    if not full_path.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {full_path}\n"
            f"请复制 config.example.yml 为 config.yml 并填入真实配置"
        )

    with open(full_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 验证必需配置项
    _validate_config(config)

    return config


def _validate_config(config):
    """
    验证配置项是否完整

    Args:
        config: 配置字典

    Raises:
        ValueError: 缺少必需配置项
    """
    required_keys = [
        ('知识星球', 'token'),
        ('知识星球', 'group_id'),
    ]

    for keys in required_keys:
        value = config
        path = []
        for key in keys:
            path.append(key)
            if key not in value:
                raise ValueError(f"缺少必需配置项: {' -> '.join(path)}")
            value = value[key]

        # 检查是否为占位符
        if isinstance(value, str) and ('your_' in value or 'here' in value):
            raise ValueError(
                f"配置项 {' -> '.join(path)} 未设置实际值\n"
                f"请编辑 config.yml 填入真实配置"
            )


def get_zsxq_config(app):
    """
    获取知识星球配置

    Args:
        app: Flask应用实例

    Returns:
        dict: 知识星球配置
    """
    return app.config['ZSXQ_CONFIG'].get('知识星球', {})


def get_cache_config(app):
    """
    获取缓存配置

    Args:
        app: Flask应用实例

    Returns:
        dict: 缓存配置
    """
    return app.config['ZSXQ_CONFIG'].get('缓存配置', {})


def get_system_config(app):
    """
    获取系统配置

    Args:
        app: Flask应用实例

    Returns:
        dict: 系统配置
    """
    return app.config['ZSXQ_CONFIG'].get('系统配置', {})


def get_leaderboard_config(app):
    """
    获取排行榜配置

    Args:
        app: Flask应用实例

    Returns:
        dict: 排行榜配置
    """
    return app.config['ZSXQ_CONFIG'].get('排行榜配置', {})
