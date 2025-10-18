"""
全局错误处理器
"""
from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException
from ..utils.response import error_response
from ..utils.config_loader import get_system_config


def register_error_handlers(app):
    """
    注册全局错误处理器

    Args:
        app: Flask应用实例
    """

    @app.errorhandler(400)
    def bad_request(e):
        """处理400错误"""
        return error_response(message="请求参数错误", code=400)

    @app.errorhandler(401)
    def unauthorized(e):
        """处理401错误 - Token失效"""
        config = get_system_config(app)
        contact = config.get('contact', {})
        contact_info = f"{contact.get('type', '微信')}: {contact.get('value', '20133213')}"

        return error_response(
            message=f"Token已失效,请联系管理员更新。{contact_info}",
            code=401
        )

    @app.errorhandler(404)
    def not_found(e):
        """处理404错误"""
        return error_response(message="资源不存在", code=404)

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        """处理429错误 - 限流"""
        return error_response(message="请求过于频繁,请稍后再试", code=429)

    @app.errorhandler(500)
    def internal_server_error(e):
        """处理500错误"""
        app.logger.error(f"Internal Server Error: {str(e)}", exc_info=True)
        return error_response(message="系统错误,请稍后再试", code=500)

    @app.errorhandler(Exception)
    def handle_exception(e):
        """处理所有未捕获的异常"""
        # 如果是HTTP异常,直接返回
        if isinstance(e, HTTPException):
            return e

        # 记录异常日志
        app.logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)

        # 返回通用错误响应
        return error_response(message="系统错误,请稍后再试", code=500)
