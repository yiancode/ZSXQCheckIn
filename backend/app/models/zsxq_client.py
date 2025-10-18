"""
知识星球API客户端
封装所有知识星球API调用
"""
import requests
from flask import current_app


class ZSXQAPIError(Exception):
    """知识星球API错误"""
    def __init__(self, message, status_code=None, response_data=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class ZSXQClient:
    """知识星球API客户端"""

    def __init__(self, app=None):
        """
        初始化客户端

        Args:
            app: Flask应用实例
        """
        self.app = app
        self._init_from_app(app)

    def _init_from_app(self, app):
        """从Flask应用加载配置"""
        if app:
            config = app.config.get('ZSXQ_CONFIG', {})
            zsxq_config = config.get('知识星球', {})

            self.token = zsxq_config.get('token')
            self.group_id = zsxq_config.get('group_id')
            self.api_base = zsxq_config.get('api_base', 'https://api.zsxq.com')

            # 验证必需配置
            if not self.token or not self.group_id:
                raise ValueError("缺少必需的知识星球配置: token 或 group_id")

    def _get_headers(self):
        """
        构建请求头

        Returns:
            dict: 请求头字典
        """
        return {
            'Authorization': self.token,
            'User-Agent': 'xiaomiquan/5.28.1 (iPhone; iOS 14.7.1; Scale/3.00)',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'x-request-id': self._generate_request_id()
        }

    def _generate_request_id(self):
        """
        生成请求ID

        Returns:
            str: UUID格式的请求ID
        """
        import uuid
        return str(uuid.uuid4())

    def _make_request(self, method, endpoint, params=None, data=None):
        """
        发起HTTP请求

        Args:
            method: 请求方法 (GET, POST等)
            endpoint: API端点路径
            params: URL查询参数
            data: 请求体数据

        Returns:
            dict: 响应数据

        Raises:
            ZSXQAPIError: API调用失败
        """
        url = f"{self.api_base}{endpoint}"
        headers = self._get_headers()

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                timeout=10,
                verify=False  # 禁用SSL证书验证
            )

            # 记录日志
            if self.app:
                self.app.logger.debug(
                    f"ZSXQ API Request: {method} {url} "
                    f"Status: {response.status_code}"
                )

            # 检查HTTP状态码
            if response.status_code == 401:
                raise ZSXQAPIError("Token已失效", status_code=401)
            elif response.status_code == 429:
                raise ZSXQAPIError("请求过于频繁", status_code=429)
            elif response.status_code >= 500:
                raise ZSXQAPIError("知识星球服务器错误", status_code=response.status_code)

            # 解析响应
            try:
                response_data = response.json()
            except ValueError:
                # 如果响应不是JSON格式，直接抛出错误
                raise ZSXQAPIError(f"API响应格式错误: {response.text[:200]}")

            # 检查业务状态码
            if not response_data.get('succeeded', False):
                error_info = response_data.get('error', {})
                if isinstance(error_info, dict):
                    error_msg = error_info.get('message', '未知错误')
                else:
                    error_msg = str(error_info)
                raise ZSXQAPIError(f"API调用失败: {error_msg}", response_data=response_data)

            return response_data.get('resp_data', {})

        except requests.RequestException as e:
            if self.app:
                self.app.logger.error(f"ZSXQ API请求异常: {str(e)}", exc_info=True)
            raise ZSXQAPIError(f"网络请求失败: {str(e)}")

    def get_projects(self, scope='ongoing'):
        """
        获取打卡项目列表

        Args:
            scope: 项目范围 (ongoing|closed|over)

        Returns:
            list: 项目列表
        """
        endpoint = f"/v2/groups/{self.group_id}/checkins"
        params = {
            'scope': scope,
            'count': 100  # 添加count参数，最大100
        }

        data = self._make_request('GET', endpoint, params=params)
        return data.get('checkins', [])

    def get_project_stats(self, project_id):
        """
        获取项目统计数据

        Args:
            project_id: 项目ID

        Returns:
            dict: 统计数据
        """
        endpoint = f"/v2/groups/{self.group_id}/checkins/{project_id}/statistics"

        return self._make_request('GET', endpoint)

    def get_daily_stats(self, project_id, date=None):
        """
        获取每日统计数据

        Args:
            project_id: 项目ID
            date: 查询日期，格式为ISO8601，如果不提供则使用当前时间

        Returns:
            dict: 每日统计
        """
        from datetime import datetime
        import urllib.parse
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+0800'
        
        encoded_date = urllib.parse.quote(date)
        endpoint = f"/v2/groups/{self.group_id}/checkins/{project_id}/statistics/daily"
        params = {'date': encoded_date}

        return self._make_request('GET', endpoint, params=params)

    def get_ranking_list(self, project_id, ranking_type='continuous', index=0):
        """
        获取排行榜

        Args:
            project_id: 项目ID
            ranking_type: 排行榜类型 (continuous|accumulated)
            index: 分页索引

        Returns:
            dict: 排行榜数据,包含ranking_list和user_specific
        """
        endpoint = f"/v2/groups/{self.group_id}/checkins/{project_id}/ranking_list"
        params = {
            'type': ranking_type,
            'index': index
        }

        return self._make_request('GET', endpoint, params=params)

    def get_topics(self, project_id, count=20):
        """
        获取打卡话题列表

        Args:
            project_id: 项目ID
            count: 返回数量

        Returns:
            dict: 话题数据
        """
        endpoint = f"/v2/groups/{self.group_id}/checkins/{project_id}/topics"
        params = {'count': count}

        return self._make_request('GET', endpoint, params=params)

    def get_project_detail(self, project_id):
        """
        获取项目详情

        Args:
            project_id: 项目ID

        Returns:
            dict: 项目详情,如果不存在则返回None
        """
        endpoint = f"/v2/groups/{self.group_id}/checkins/{project_id}"
        
        try:
            return self._make_request('GET', endpoint)
        except ZSXQAPIError:
            # 如果单独接口失败，尝试从项目列表中查找
            for scope in ['ongoing', 'closed', 'over']:
                projects = self.get_projects(scope=scope)
                for project in projects:
                    if str(project.get('checkin_id')) == str(project_id):
                        return project
            return None
