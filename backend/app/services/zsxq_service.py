"""
知识星球业务服务层
整合API客户端和缓存服务,提供统一的业务接口
"""
from datetime import datetime
from ..models.zsxq_client import ZSXQClient, ZSXQAPIError
from .cache_service import CacheService, CacheKeys
from flask import current_app


class ZSXQService:
    """知识星球业务服务类"""

    def __init__(self, app):
        """
        初始化服务

        Args:
            app: Flask应用实例
        """
        self.app = app
        self.client = ZSXQClient(app)

    def _get_with_cache(self, cache_key, fetch_func, ttl=None):
        """
        带缓存的数据获取

        Args:
            cache_key: 缓存键
            fetch_func: 数据获取函数
            ttl: 缓存过期时间

        Returns:
            数据
        """
        # 尝试从缓存获取
        if CacheService.is_enabled():
            cached_data = CacheService.get(cache_key)
            if cached_data:
                self.app.logger.debug(f"缓存命中: {cache_key}")
                return cached_data
            else:
                self.app.logger.info(f"缓存未命中: {cache_key}")

        # 缓存未命中,调用API
        data = fetch_func()

        # 添加缓存时间戳
        if isinstance(data, dict):
            data['cached_at'] = datetime.now().isoformat()

        # 写入缓存
        if CacheService.is_enabled():
            CacheService.set(cache_key, data, ttl=ttl)

        return data

    def get_projects(self, scope='ongoing'):
        """
        获取项目列表

        Args:
            scope: 项目范围

        Returns:
            list: 项目列表
        """
        cache_key = CacheKeys.projects_list(scope)

        def fetch():
            raw_projects = self.client.get_projects(scope=scope)
            return [self._format_project(p) for p in raw_projects]

        return self._get_with_cache(cache_key, fetch, ttl=7200)  # 2小时

    def get_project_detail(self, project_id):
        """
        获取项目详情

        Args:
            project_id: 项目ID

        Returns:
            dict: 项目详情,不存在则返回None
        """
        cache_key = CacheKeys.project_info(project_id)

        def fetch():
            raw_project = self.client.get_project_detail(project_id)
            if not raw_project:
                return None
            return self._format_project_detail(raw_project)

        return self._get_with_cache(cache_key, fetch, ttl=7200)  # 2小时

    def get_project_stats(self, project_id):
        """
        获取项目统计

        Args:
            project_id: 项目ID

        Returns:
            dict: 统计数据
        """
        cache_key = CacheKeys.project_stats(project_id)

        def fetch():
            raw_stats = self.client.get_project_stats(project_id)
            return self._format_project_stats(raw_stats)

        return self._get_with_cache(cache_key, fetch, ttl=3600)  # 1小时

    def get_daily_stats(self, project_id):
        """
        获取每日统计

        Args:
            project_id: 项目ID

        Returns:
            dict: 每日统计
        """
        cache_key = CacheKeys.project_daily_stats(project_id)

        def fetch():
            raw_stats = self.client.get_daily_stats(project_id)
            return self._format_daily_stats(raw_stats)

        return self._get_with_cache(cache_key, fetch, ttl=1800)  # 30分钟

    def get_leaderboard(self, project_id, leaderboard_type='continuous', limit=10):
        """
        获取排行榜

        Args:
            project_id: 项目ID
            leaderboard_type: 排行榜类型
            limit: 返回数量

        Returns:
            dict: 排行榜数据
        """
        cache_key = CacheKeys.project_leaderboard(project_id, leaderboard_type)

        def fetch():
            # 知识星球API一次返回所有数据,我们在这里做限制
            raw_data = self.client.get_ranking_list(
                project_id,
                ranking_type=leaderboard_type,
                index=0
            )
            return self._format_leaderboard(raw_data, leaderboard_type, limit)

        return self._get_with_cache(cache_key, fetch, ttl=3600)  # 1小时

    def get_topics(self, project_id, count=20):
        """
        获取话题列表

        Args:
            project_id: 项目ID
            count: 返回数量

        Returns:
            list: 话题列表
        """
        cache_key = CacheKeys.project_topics(project_id)

        def fetch():
            raw_data = self.client.get_topics(project_id, count=count)
            topics = raw_data.get('topics', [])
            return [self._format_topic(t) for t in topics]

        return self._get_with_cache(cache_key, fetch, ttl=600)  # 10分钟

    # ==================== 数据格式化方法 ====================

    def _format_project(self, raw_project):
        """
        格式化项目基本信息

        Args:
            raw_project: 原始项目数据

        Returns:
            dict: 格式化后的项目信息
        """
        return {
            'project_id': str(raw_project.get('checkin_id', '')),
            'title': raw_project.get('name', ''),
            'description': raw_project.get('description', ''),
            'status': self._determine_project_status(raw_project),
            'start_date': raw_project.get('start_time', ''),
            'end_date': raw_project.get('end_time', ''),
            'cover_image': raw_project.get('background', {}).get('image_url', ''),
            'total_members': raw_project.get('users_count', 0),
            'total_checkins': raw_project.get('checkined_count', 0)
        }

    def _format_project_detail(self, raw_project):
        """
        格式化项目详情

        Args:
            raw_project: 原始项目数据

        Returns:
            dict: 格式化后的项目详情
        """
        basic_info = self._format_project(raw_project)

        # 添加详情特有字段
        basic_info.update({
            'continuous_days': raw_project.get('current_continuous_days', 0),
            'rules': raw_project.get('rules', ''),
            'created_at': raw_project.get('create_time', '')
        })

        return basic_info

    def _format_project_stats(self, raw_stats):
        """
        格式化项目统计数据

        Args:
            raw_stats: 原始统计数据

        Returns:
            dict: 格式化后的统计数据
        """
        total_members = raw_stats.get('users_count', 0)
        total_checkins = raw_stats.get('checkined_count', 0)

        return {
            'total_members': total_members,
            'total_checkins': total_checkins,
            'today_checkins': raw_stats.get('today_count', 0),
            'continuous_rate': raw_stats.get('continuous_rate', 0),
            'avg_checkins_per_member': round(total_checkins / total_members, 2) if total_members > 0 else 0
        }

    def _format_daily_stats(self, raw_stats):
        """
        格式化每日统计

        Args:
            raw_stats: 原始每日统计

        Returns:
            dict: 格式化后的每日统计
        """
        return {
            'date': raw_stats.get('date', datetime.now().strftime('%Y-%m-%d')),
            'total_checkins': raw_stats.get('count', 0),
            'new_members': raw_stats.get('new_users', 0),
            'active_members': raw_stats.get('active_users', 0)
        }

    def _format_leaderboard(self, raw_data, leaderboard_type, limit):
        """
        格式化排行榜数据

        Args:
            raw_data: 原始排行榜数据
            leaderboard_type: 排行榜类型
            limit: 返回数量限制

        Returns:
            dict: 格式化后的排行榜
        """
        ranking_list = raw_data.get('ranking_list', [])
        user_specific = raw_data.get('user_specific', {})

        # 限制返回数量
        limited_rankings = ranking_list[:limit]

        return {
            'type': leaderboard_type,
            'rankings': [self._format_ranking_item(item) for item in limited_rankings],
            'total': len(ranking_list),
            'user_rank': self._format_user_rank(user_specific) if user_specific else None
        }

    def _format_ranking_item(self, raw_item):
        """
        格式化排行榜条目

        Args:
            raw_item: 原始排行条目

        Returns:
            dict: 格式化后的排行条目
        """
        user = raw_item.get('user', {})

        return {
            'rank': raw_item.get('rankings', 0),
            'user': {
                'user_id': user.get('user_id', 0),
                'name': user.get('name', ''),
                'alias': user.get('alias', ''),
                'avatar': user.get('avatar_url', '')
            },
            'days': raw_item.get('checkined_days', 0)
        }

    def _format_user_rank(self, raw_user_rank):
        """
        格式化用户排名信息

        Args:
            raw_user_rank: 原始用户排名

        Returns:
            dict: 格式化后的用户排名
        """
        return {
            'rank': raw_user_rank.get('rankings', 0),
            'days': raw_user_rank.get('checkined_days', 0)
        }

    def _format_topic(self, raw_topic):
        """
        格式化话题数据

        Args:
            raw_topic: 原始话题数据

        Returns:
            dict: 格式化后的话题
        """
        topic = raw_topic.get('topic', {})
        user = topic.get('user', {})

        return {
            'topic_id': str(topic.get('topic_id', '')),
            'title': topic.get('title', ''),
            'content': topic.get('text', ''),
            'create_time': topic.get('create_time', ''),
            'user': {
                'user_id': user.get('user_id', 0),
                'name': user.get('name', ''),
                'avatar': user.get('avatar_url', '')
            }
        }

    def _determine_project_status(self, raw_project):
        """
        判断项目状态

        Args:
            raw_project: 原始项目数据

        Returns:
            str: 项目状态 (ongoing|closed|over)
        """
        # 根据时间判断状态
        now = datetime.now()
        start_time = raw_project.get('start_time', '')
        end_time = raw_project.get('end_time', '')

        try:
            if end_time:
                end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                if now > end_dt:
                    return 'over'

            if start_time:
                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                if now < start_dt:
                    return 'closed'

            return 'ongoing'
        except:
            return 'ongoing'

    # ==================== 缓存管理方法 ====================

    def clear_project_cache(self, project_id):
        """
        清除项目相关的所有缓存

        Args:
            project_id: 项目ID

        Returns:
            int: 清除的键数量
        """
        pattern = CacheKeys.project_all(project_id)
        count = CacheService.delete_pattern(pattern)
        self.app.logger.info(f"清除项目 {project_id} 缓存,共 {count} 个键")
        return count

    def refresh_all_cache(self):
        """
        刷新所有缓存(用于定时任务)

        Returns:
            dict: 刷新结果统计
        """
        stats = {
            'success': 0,
            'failed': 0,
            'errors': []
        }

        try:
            # 刷新所有scope的项目列表
            for scope in ['ongoing', 'closed', 'over']:
                try:
                    self.get_projects(scope=scope)
                    stats['success'] += 1
                except Exception as e:
                    stats['failed'] += 1
                    stats['errors'].append(f"刷新{scope}项目列表失败: {str(e)}")

            self.app.logger.info(f"缓存刷新完成: {stats}")

        except Exception as e:
            self.app.logger.error(f"缓存刷新异常: {str(e)}", exc_info=True)
            stats['errors'].append(str(e))

        return stats
