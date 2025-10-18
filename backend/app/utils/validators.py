"""
参数验证工具
"""
import re


def validate_project_id(project_id):
    """
    验证项目ID格式

    Args:
        project_id: 项目ID字符串

    Returns:
        bool: 是否有效
    """
    if not project_id:
        return False

    # 项目ID应该是纯数字字符串
    return project_id.isdigit() and len(project_id) > 0


def validate_leaderboard_type(leaderboard_type):
    """
    验证排行榜类型

    Args:
        leaderboard_type: 排行榜类型

    Returns:
        bool: 是否有效
    """
    valid_types = ['continuous', 'accumulated']
    return leaderboard_type in valid_types


def validate_scope(scope):
    """
    验证项目范围

    Args:
        scope: 项目范围

    Returns:
        bool: 是否有效
    """
    valid_scopes = ['ongoing', 'closed', 'over']
    return scope in valid_scopes


def validate_pagination(page, page_size, max_page_size=100):
    """
    验证分页参数

    Args:
        page: 页码
        page_size: 每页大小
        max_page_size: 最大每页大小

    Returns:
        tuple: (是否有效, 错误消息)
    """
    if page < 1:
        return False, "页码必须大于0"

    if page_size < 1:
        return False, "每页大小必须大于0"

    if page_size > max_page_size:
        return False, f"每页大小不能超过{max_page_size}"

    return True, None


def validate_count(count, min_count=1, max_count=100):
    """
    验证数量参数

    Args:
        count: 数量
        min_count: 最小值
        max_count: 最大值

    Returns:
        tuple: (是否有效, 错误消息)
    """
    if count < min_count:
        return False, f"数量不能小于{min_count}"

    if count > max_count:
        return False, f"数量不能超过{max_count}"

    return True, None
