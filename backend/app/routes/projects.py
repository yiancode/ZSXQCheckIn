"""
打卡项目相关路由
"""
from flask import jsonify, request, current_app
from . import api_bp
from ..services.zsxq_service import ZSXQService
from ..services.cache_service import CacheService
from ..utils.response import success_response, error_response
from ..utils.validators import validate_project_id, validate_leaderboard_type


@api_bp.route('/projects', methods=['GET'])
def get_projects():
    """
    获取所有打卡项目列表

    Query Parameters:
        scope: 项目范围 (ongoing|closed|over) 默认:ongoing

    Returns:
        {
            "code": 0,
            "message": "success",
            "data": {
                "projects": [
                    {
                        "project_id": "1141152412",
                        "title": "2025年打卡挑战",
                        "description": "每日打卡记录",
                        "status": "ongoing",
                        "start_date": "2025-01-01",
                        "end_date": "2025-12-31",
                        "total_members": 150,
                        "total_checkins": 3500
                    }
                ],
                "total": 1
            }
        }
    """
    try:
        scope = request.args.get('scope', 'ongoing')

        # 从服务层获取数据
        zsxq_service = ZSXQService(current_app)
        projects = zsxq_service.get_projects(scope=scope)

        return success_response(data={
            "projects": projects,
            "total": len(projects)
        })

    except Exception as e:
        current_app.logger.error(f"获取项目列表失败: {str(e)}", exc_info=True)
        return error_response(message=str(e))


@api_bp.route('/projects/<project_id>', methods=['GET'])
def get_project_detail(project_id):
    """
    获取项目详情

    Path Parameters:
        project_id: 项目ID

    Returns:
        {
            "code": 0,
            "message": "success",
            "data": {
                "project_id": "1141152412",
                "title": "2025年打卡挑战",
                "description": "每日打卡记录",
                "status": "ongoing",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31",
                "cover_image": "https://...",
                "total_members": 150,
                "total_checkins": 3500,
                "continuous_days": 10
            }
        }
    """
    try:
        if not validate_project_id(project_id):
            return error_response(message="无效的项目ID", code=400)

        zsxq_service = ZSXQService(current_app)
        project = zsxq_service.get_project_detail(project_id)

        if not project:
            return error_response(message="项目不存在", code=404)

        return success_response(data=project)

    except Exception as e:
        current_app.logger.error(f"获取项目详情失败: {str(e)}", exc_info=True)
        return error_response(message=str(e))


@api_bp.route('/projects/<project_id>/stats', methods=['GET'])
def get_project_stats(project_id):
    """
    获取项目统计数据

    Path Parameters:
        project_id: 项目ID

    Returns:
        {
            "code": 0,
            "message": "success",
            "data": {
                "total_members": 150,
                "total_checkins": 3500,
                "today_checkins": 120,
                "continuous_rate": 0.85,
                "avg_checkins_per_member": 23.3
            }
        }
    """
    try:
        if not validate_project_id(project_id):
            return error_response(message="无效的项目ID", code=400)

        zsxq_service = ZSXQService(current_app)
        stats = zsxq_service.get_project_stats(project_id)

        return success_response(data=stats)

    except Exception as e:
        current_app.logger.error(f"获取项目统计失败: {str(e)}", exc_info=True)
        return error_response(message=str(e))


@api_bp.route('/projects/<project_id>/daily-stats', methods=['GET'])
def get_daily_stats(project_id):
    """
    获取每日统计数据

    Path Parameters:
        project_id: 项目ID

    Returns:
        {
            "code": 0,
            "message": "success",
            "data": {
                "date": "2025-01-15",
                "total_checkins": 120,
                "new_members": 5,
                "active_members": 115
            }
        }
    """
    try:
        if not validate_project_id(project_id):
            return error_response(message="无效的项目ID", code=400)

        zsxq_service = ZSXQService(current_app)
        daily_stats = zsxq_service.get_daily_stats(project_id)

        return success_response(data=daily_stats)

    except Exception as e:
        current_app.logger.error(f"获取每日统计失败: {str(e)}", exc_info=True)
        return error_response(message=str(e))


@api_bp.route('/projects/<project_id>/leaderboard', methods=['GET'])
def get_leaderboard(project_id):
    """
    获取排行榜

    Path Parameters:
        project_id: 项目ID

    Query Parameters:
        type: 排行榜类型 (continuous|accumulated) 默认:continuous
        limit: 返回数量 (1-100) 默认:10

    Returns:
        {
            "code": 0,
            "message": "success",
            "data": {
                "type": "continuous",
                "rankings": [
                    {
                        "rank": 1,
                        "user": {
                            "user_id": 585221282158424,
                            "name": "伊雪儿",
                            "avatar": "https://..."
                        },
                        "days": 10,
                        "latest_checkin": "2025-01-15 08:30:00"
                    }
                ],
                "total": 100,
                "user_rank": {
                    "rank": 15,
                    "days": 8
                }
            }
        }
    """
    try:
        if not validate_project_id(project_id):
            return error_response(message="无效的项目ID", code=400)

        # 获取参数
        leaderboard_type = request.args.get('type', 'continuous')
        limit = request.args.get('limit', 10, type=int)

        # 验证参数
        if not validate_leaderboard_type(leaderboard_type):
            return error_response(message="无效的排行榜类型,支持: continuous, accumulated", code=400)

        if limit < 1 or limit > 100:
            return error_response(message="limit参数范围: 1-100", code=400)

        zsxq_service = ZSXQService(current_app)
        leaderboard = zsxq_service.get_leaderboard(
            project_id,
            leaderboard_type=leaderboard_type,
            limit=limit
        )

        return success_response(data=leaderboard)

    except Exception as e:
        current_app.logger.error(f"获取排行榜失败: {str(e)}", exc_info=True)
        return error_response(message=str(e))


@api_bp.route('/projects/<project_id>/topics', methods=['GET'])
def get_topics(project_id):
    """
    获取打卡话题列表

    Path Parameters:
        project_id: 项目ID

    Query Parameters:
        count: 返回数量 默认:20

    Returns:
        {
            "code": 0,
            "message": "success",
            "data": {
                "topics": [
                    {
                        "topic_id": "123456",
                        "title": "今日打卡",
                        "create_time": "2025-01-15 08:30:00",
                        "user": {
                            "user_id": 585221282158424,
                            "name": "张三",
                            "avatar": "https://..."
                        },
                        "content": "今天学习了Flask..."
                    }
                ],
                "total": 20
            }
        }
    """
    try:
        if not validate_project_id(project_id):
            return error_response(message="无效的项目ID", code=400)

        count = request.args.get('count', 20, type=int)

        if count < 1 or count > 100:
            return error_response(message="count参数范围: 1-100", code=400)

        zsxq_service = ZSXQService(current_app)
        topics = zsxq_service.get_topics(project_id, count=count)

        return success_response(data={
            "topics": topics,
            "total": len(topics)
        })

    except Exception as e:
        current_app.logger.error(f"获取话题列表失败: {str(e)}", exc_info=True)
        return error_response(message=str(e))
