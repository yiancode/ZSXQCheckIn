"""
Redis缓存服务模块
"""
import redis
import json
from functools import wraps
from flask import current_app


class CacheService:
    """Redis缓存服务类"""

    _redis_client = None

    @classmethod
    def init_cache(cls, app, cache_config):
        """
        初始化Redis连接

        Args:
            app: Flask应用实例
            cache_config: 缓存配置字典
        """
        redis_config = cache_config.get('redis', {})

        try:
            cls._redis_client = redis.Redis(
                host=redis_config.get('host', 'localhost'),
                port=redis_config.get('port', 6379),
                db=redis_config.get('db', 0),
                password=redis_config.get('password', None),
                decode_responses=True,  # 自动解码为字符串
                socket_timeout=5,
                socket_connect_timeout=5
            )

            # 测试连接
            cls._redis_client.ping()
            app.logger.info("Redis缓存连接成功")

            # 存储配置到app.config
            app.config['CACHE_CONFIG'] = cache_config
            app.config['REDIS_CLIENT'] = cls._redis_client

        except redis.RedisError as e:
            app.logger.warning(f"Redis连接失败: {str(e)}, 将使用降级模式(无缓存)")
            cls._redis_client = None
            app.config['CACHE_CONFIG'] = {'enabled': False}

    @classmethod
    def get_client(cls):
        """
        获取Redis客户端

        Returns:
            redis.Redis: Redis客户端实例,如果未初始化则返回None
        """
        return cls._redis_client

    @classmethod
    def is_enabled(cls):
        """
        检查缓存是否启用

        Returns:
            bool: 缓存是否可用
        """
        return cls._redis_client is not None

    @classmethod
    def _get_key_prefix(cls):
        """获取键前缀"""
        try:
            config = current_app.config.get('CACHE_CONFIG', {})
            return config.get('redis', {}).get('key_prefix', 'zsxq:')
        except:
            return 'zsxq:'

    @classmethod
    def _get_default_ttl(cls):
        """获取默认过期时间"""
        try:
            config = current_app.config.get('CACHE_CONFIG', {})
            return config.get('redis', {}).get('default_ttl', 7200)
        except:
            return 7200

    @classmethod
    def build_key(cls, *parts):
        """
        构建缓存键

        Args:
            *parts: 键的各个部分

        Returns:
            str: 完整的缓存键

        Examples:
            build_key('projects', 'list') -> 'zsxq:projects:list'
            build_key('project', '123', 'info') -> 'zsxq:project:123:info'
        """
        prefix = cls._get_key_prefix()
        return prefix + ':'.join(str(p) for p in parts)

    @classmethod
    def get(cls, key):
        """
        获取缓存

        Args:
            key: 缓存键

        Returns:
            解析后的数据,如果不存在或出错则返回None
        """
        if not cls.is_enabled():
            return None

        try:
            value = cls._redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            current_app.logger.error(f"获取缓存失败 {key}: {str(e)}")
            return None

    @classmethod
    def set(cls, key, value, ttl=None):
        """
        设置缓存

        Args:
            key: 缓存键
            value: 要缓存的数据(会被JSON序列化)
            ttl: 过期时间(秒),None则使用默认值

        Returns:
            bool: 是否成功
        """
        if not cls.is_enabled():
            return False

        try:
            if ttl is None:
                ttl = cls._get_default_ttl()

            serialized = json.dumps(value, ensure_ascii=False)
            cls._redis_client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            current_app.logger.error(f"设置缓存失败 {key}: {str(e)}")
            return False

    @classmethod
    def delete(cls, key):
        """
        删除缓存

        Args:
            key: 缓存键

        Returns:
            bool: 是否成功
        """
        if not cls.is_enabled():
            return False

        try:
            cls._redis_client.delete(key)
            return True
        except Exception as e:
            current_app.logger.error(f"删除缓存失败 {key}: {str(e)}")
            return False

    @classmethod
    def delete_pattern(cls, pattern):
        """
        批量删除匹配模式的缓存键

        Args:
            pattern: 键模式(支持通配符*)

        Returns:
            int: 删除的键数量
        """
        if not cls.is_enabled():
            return 0

        try:
            keys = cls._redis_client.keys(pattern)
            if keys:
                return cls._redis_client.delete(*keys)
            return 0
        except Exception as e:
            current_app.logger.error(f"批量删除缓存失败 {pattern}: {str(e)}")
            return 0

    @classmethod
    def exists(cls, key):
        """
        检查缓存键是否存在

        Args:
            key: 缓存键

        Returns:
            bool: 是否存在
        """
        if not cls.is_enabled():
            return False

        try:
            return cls._redis_client.exists(key) > 0
        except Exception as e:
            current_app.logger.error(f"检查缓存存在性失败 {key}: {str(e)}")
            return False

    @classmethod
    def get_ttl(cls, key):
        """
        获取缓存键的剩余过期时间

        Args:
            key: 缓存键

        Returns:
            int: 剩余秒数,-1表示永不过期,-2表示不存在
        """
        if not cls.is_enabled():
            return -2

        try:
            return cls._redis_client.ttl(key)
        except Exception as e:
            current_app.logger.error(f"获取TTL失败 {key}: {str(e)}")
            return -2


# 缓存键常量定义
class CacheKeys:
    """缓存键模板"""

    # 项目列表 (按scope分组)
    PROJECTS_LIST = "projects:list:{scope}"

    # 项目详情
    PROJECT_INFO = "project:{project_id}:info"

    # 项目统计
    PROJECT_STATS = "project:{project_id}:stats"

    # 每日统计
    PROJECT_DAILY_STATS = "project:{project_id}:daily_stats"

    # 排行榜 (按type分组)
    PROJECT_LEADERBOARD = "project:{project_id}:leaderboard:{type}"

    # 话题列表
    PROJECT_TOPICS = "project:{project_id}:topics"

    @classmethod
    def projects_list(cls, scope='ongoing'):
        """构建项目列表缓存键"""
        return CacheService.build_key('projects', 'list', scope)

    @classmethod
    def project_info(cls, project_id):
        """构建项目详情缓存键"""
        return CacheService.build_key('project', project_id, 'info')

    @classmethod
    def project_stats(cls, project_id):
        """构建项目统计缓存键"""
        return CacheService.build_key('project', project_id, 'stats')

    @classmethod
    def project_daily_stats(cls, project_id):
        """构建每日统计缓存键"""
        return CacheService.build_key('project', project_id, 'daily_stats')

    @classmethod
    def project_leaderboard(cls, project_id, leaderboard_type='continuous'):
        """构建排行榜缓存键"""
        return CacheService.build_key('project', project_id, 'leaderboard', leaderboard_type)

    @classmethod
    def project_topics(cls, project_id):
        """构建话题列表缓存键"""
        return CacheService.build_key('project', project_id, 'topics')

    @classmethod
    def project_all(cls, project_id):
        """
        获取项目相关的所有缓存键模式

        Args:
            project_id: 项目ID

        Returns:
            str: 键模式
        """
        prefix = CacheService._get_key_prefix()
        return f"{prefix}project:{project_id}:*"


# 初始化函数
def init_cache(app, cache_config):
    """
    初始化缓存服务

    Args:
        app: Flask应用实例
        cache_config: 缓存配置
    """
    CacheService.init_cache(app, cache_config)
