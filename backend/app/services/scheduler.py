"""
定时任务调度模块
使用APScheduler实现缓存定时刷新
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from .zsxq_service import ZSXQService
from .cache_service import CacheService, CacheKeys


class CacheScheduler:
    """缓存刷新调度器"""

    _scheduler = None
    _app = None

    @classmethod
    def init_scheduler(cls, app):
        """
        初始化调度器

        Args:
            app: Flask应用实例
        """
        cls._app = app

        # 检查缓存是否启用
        cache_config = app.config.get('ZSXQ_CONFIG', {}).get('缓存配置', {})
        if not cache_config.get('enabled', True):
            app.logger.info("缓存未启用,跳过定时任务初始化")
            return

        # 创建后台调度器
        cls._scheduler = BackgroundScheduler(
            timezone='Asia/Shanghai',
            job_defaults={
                'coalesce': True,  # 合并错过的任务
                'max_instances': 1  # 同一任务最多同时运行1个实例
            }
        )

        # 添加定时任务
        cls._add_jobs(app, cache_config)

        # 启动调度器
        cls._scheduler.start()
        app.logger.info("定时任务调度器启动成功")

    @classmethod
    def _add_jobs(cls, app, cache_config):
        """
        添加定时任务

        Args:
            app: Flask应用实例
            cache_config: 缓存配置
        """
        scheduler_config = cache_config.get('scheduler', {})

        # 1. 刷新项目列表 (每小时)
        projects_interval = scheduler_config.get('projects_list', 3600)
        cls._scheduler.add_job(
            func=cls._refresh_projects_list,
            trigger=IntervalTrigger(seconds=projects_interval),
            id='refresh_projects_list',
            name='刷新项目列表',
            replace_existing=True
        )
        app.logger.info(f"添加任务: 刷新项目列表 (间隔: {projects_interval}秒)")

        # 2. 刷新排行榜 (每30分钟)
        leaderboard_interval = scheduler_config.get('leaderboard', 1800)
        cls._scheduler.add_job(
            func=cls._refresh_leaderboards,
            trigger=IntervalTrigger(seconds=leaderboard_interval),
            id='refresh_leaderboards',
            name='刷新排行榜',
            replace_existing=True
        )
        app.logger.info(f"添加任务: 刷新排行榜 (间隔: {leaderboard_interval}秒)")

        # 3. 刷新项目统计 (每30分钟)
        stats_interval = scheduler_config.get('project_stats', 1800)
        cls._scheduler.add_job(
            func=cls._refresh_project_stats,
            trigger=IntervalTrigger(seconds=stats_interval),
            id='refresh_project_stats',
            name='刷新项目统计',
            replace_existing=True
        )
        app.logger.info(f"添加任务: 刷新项目统计 (间隔: {stats_interval}秒)")

        # 4. 刷新每日统计 (每15分钟)
        daily_stats_interval = scheduler_config.get('daily_stats', 900)
        cls._scheduler.add_job(
            func=cls._refresh_daily_stats,
            trigger=IntervalTrigger(seconds=daily_stats_interval),
            id='refresh_daily_stats',
            name='刷新每日统计',
            replace_existing=True
        )
        app.logger.info(f"添加任务: 刷新每日统计 (间隔: {daily_stats_interval}秒)")

        # 5. 刷新话题列表 (每5分钟)
        topics_interval = scheduler_config.get('topics', 300)
        cls._scheduler.add_job(
            func=cls._refresh_topics,
            trigger=IntervalTrigger(seconds=topics_interval),
            id='refresh_topics',
            name='刷新话题列表',
            replace_existing=True
        )
        app.logger.info(f"添加任务: 刷新话题列表 (间隔: {topics_interval}秒)")

    @classmethod
    def _refresh_projects_list(cls):
        """刷新所有项目列表"""
        with cls._app.app_context():
            try:
                cls._app.logger.info("开始定时刷新项目列表")
                service = ZSXQService(cls._app)

                for scope in ['ongoing', 'closed', 'over']:
                    try:
                        # 先删除缓存
                        cache_key = CacheKeys.projects_list(scope)
                        CacheService.delete(cache_key)

                        # 重新获取并缓存
                        service.get_projects(scope=scope)
                        cls._app.logger.debug(f"刷新 {scope} 项目列表成功")
                    except Exception as e:
                        cls._app.logger.error(f"刷新 {scope} 项目列表失败: {str(e)}")

                cls._app.logger.info("项目列表刷新完成")

            except Exception as e:
                cls._app.logger.error(f"刷新项目列表异常: {str(e)}", exc_info=True)

    @classmethod
    def _refresh_leaderboards(cls):
        """刷新所有排行榜"""
        with cls._app.app_context():
            try:
                cls._app.logger.info("开始定时刷新排行榜")
                service = ZSXQService(cls._app)

                # 获取所有进行中的项目
                projects = service.get_projects(scope='ongoing')

                for project in projects:
                    project_id = project['project_id']

                    for leaderboard_type in ['continuous', 'accumulated']:
                        try:
                            # 先删除缓存
                            cache_key = CacheKeys.project_leaderboard(project_id, leaderboard_type)
                            CacheService.delete(cache_key)

                            # 重新获取并缓存
                            service.get_leaderboard(project_id, leaderboard_type=leaderboard_type, limit=100)
                            cls._app.logger.debug(f"刷新项目 {project_id} {leaderboard_type} 排行榜成功")
                        except Exception as e:
                            cls._app.logger.error(
                                f"刷新项目 {project_id} {leaderboard_type} 排行榜失败: {str(e)}"
                            )

                cls._app.logger.info("排行榜刷新完成")

            except Exception as e:
                cls._app.logger.error(f"刷新排行榜异常: {str(e)}", exc_info=True)

    @classmethod
    def _refresh_project_stats(cls):
        """刷新项目统计"""
        with cls._app.app_context():
            try:
                cls._app.logger.info("开始定时刷新项目统计")
                service = ZSXQService(cls._app)

                # 获取所有进行中的项目
                projects = service.get_projects(scope='ongoing')

                for project in projects:
                    project_id = project['project_id']
                    try:
                        # 先删除缓存
                        cache_key = CacheKeys.project_stats(project_id)
                        CacheService.delete(cache_key)

                        # 重新获取并缓存
                        service.get_project_stats(project_id)
                        cls._app.logger.debug(f"刷新项目 {project_id} 统计成功")
                    except Exception as e:
                        cls._app.logger.error(f"刷新项目 {project_id} 统计失败: {str(e)}")

                cls._app.logger.info("项目统计刷新完成")

            except Exception as e:
                cls._app.logger.error(f"刷新项目统计异常: {str(e)}", exc_info=True)

    @classmethod
    def _refresh_daily_stats(cls):
        """刷新每日统计"""
        with cls._app.app_context():
            try:
                cls._app.logger.info("开始定时刷新每日统计")
                service = ZSXQService(cls._app)

                # 获取所有进行中的项目
                projects = service.get_projects(scope='ongoing')

                for project in projects:
                    project_id = project['project_id']
                    try:
                        # 先删除缓存
                        cache_key = CacheKeys.project_daily_stats(project_id)
                        CacheService.delete(cache_key)

                        # 重新获取并缓存
                        service.get_daily_stats(project_id)
                        cls._app.logger.debug(f"刷新项目 {project_id} 每日统计成功")
                    except Exception as e:
                        cls._app.logger.error(f"刷新项目 {project_id} 每日统计失败: {str(e)}")

                cls._app.logger.info("每日统计刷新完成")

            except Exception as e:
                cls._app.logger.error(f"刷新每日统计异常: {str(e)}", exc_info=True)

    @classmethod
    def _refresh_topics(cls):
        """刷新话题列表"""
        with cls._app.app_context():
            try:
                cls._app.logger.info("开始定时刷新话题列表")
                service = ZSXQService(cls._app)

                # 获取所有进行中的项目
                projects = service.get_projects(scope='ongoing')

                for project in projects:
                    project_id = project['project_id']
                    try:
                        # 先删除缓存
                        cache_key = CacheKeys.project_topics(project_id)
                        CacheService.delete(cache_key)

                        # 重新获取并缓存
                        service.get_topics(project_id, count=20)
                        cls._app.logger.debug(f"刷新项目 {project_id} 话题列表成功")
                    except Exception as e:
                        cls._app.logger.error(f"刷新项目 {project_id} 话题列表失败: {str(e)}")

                cls._app.logger.info("话题列表刷新完成")

            except Exception as e:
                cls._app.logger.error(f"刷新话题列表异常: {str(e)}", exc_info=True)

    @classmethod
    def shutdown(cls):
        """关闭调度器"""
        if cls._scheduler:
            cls._scheduler.shutdown()
            if cls._app:
                cls._app.logger.info("定时任务调度器已关闭")

    @classmethod
    def get_jobs(cls):
        """
        获取所有任务信息

        Returns:
            list: 任务信息列表
        """
        if not cls._scheduler:
            return []

        jobs = []
        for job in cls._scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            })

        return jobs


def init_scheduler(app):
    """
    初始化调度器(在Flask应用启动时调用)

    Args:
        app: Flask应用实例
    """
    CacheScheduler.init_scheduler(app)

    # 注册应用关闭时的清理函数
    import atexit
    atexit.register(CacheScheduler.shutdown)
