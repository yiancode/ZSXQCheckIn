"""
统一响应格式工具
"""
from flask import jsonify


def success_response(data=None, message="success", code=0):
    """
    成功响应

    Args:
        data: 响应数据
        message: 响应消息
        code: 响应码 (0表示成功)

    Returns:
        Flask JSON响应对象
    """
    response = {
        "code": code,
        "message": message
    }

    if data is not None:
        response["data"] = data

    return jsonify(response)


def error_response(message="error", code=500, data=None):
    """
    错误响应

    Args:
        message: 错误消息
        code: 错误码 (非0表示错误)
        data: 额外数据

    Returns:
        Flask JSON响应对象,HTTP状态码
    """
    response = {
        "code": code,
        "message": message
    }

    if data is not None:
        response["data"] = data

    # 映射HTTP状态码
    http_status = code if 400 <= code < 600 else 500

    return jsonify(response), http_status


def paginated_response(items, total, page=1, page_size=20):
    """
    分页响应

    Args:
        items: 当前页数据列表
        total: 总数据量
        page: 当前页码
        page_size: 每页大小

    Returns:
        Flask JSON响应对象
    """
    total_pages = (total + page_size - 1) // page_size

    return success_response(data={
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    })
