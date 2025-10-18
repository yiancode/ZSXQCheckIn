"""
健康检查路由
"""
from flask import jsonify, current_app
from . import api_bp


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    健康检查接口

    Returns:
        JSON响应:
        {
            "status": "ok",
            "service": "ZSXQCheckIn API",
            "version": "1.0.0"
        }
    """
    return jsonify({
        "status": "ok",
        "service": "ZSXQCheckIn API",
        "version": "1.0.0"
    })


@api_bp.route('/ping', methods=['GET'])
def ping():
    """
    简单ping测试

    Returns:
        JSON响应: {"message": "pong"}
    """
    return jsonify({"message": "pong"})
