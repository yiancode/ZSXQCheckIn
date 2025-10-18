"""
API接口测试脚本
运行方式: python backend/tests/test_api.py
"""
import requests
import json
import sys
from datetime import datetime


class Colors:
    """终端颜色"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class APITester:
    """API测试类"""

    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def print_header(self, text):
        """打印标题"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

    def print_success(self, text):
        """打印成功信息"""
        print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")
        self.passed += 1

    def print_error(self, text):
        """打印错误信息"""
        print(f"{Colors.RED}✗ {text}{Colors.RESET}")
        self.failed += 1

    def print_warning(self, text):
        """打印警告信息"""
        print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")
        self.warnings += 1

    def print_info(self, text):
        """打印信息"""
        print(f"  {text}")

    def test_endpoint(self, name, method, endpoint, expected_status=200, params=None, json_data=None):
        """
        测试API端点

        Args:
            name: 测试名称
            method: HTTP方法
            endpoint: API端点
            expected_status: 期望的HTTP状态码
            params: URL参数
            json_data: JSON请求体
        """
        url = f"{self.base_url}{endpoint}"
        print(f"\n{Colors.BOLD}测试: {name}{Colors.RESET}")
        print(f"请求: {method} {endpoint}")

        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=10
            )

            # 检查状态码
            if response.status_code == expected_status:
                self.print_success(f"状态码正确: {response.status_code}")
            else:
                self.print_error(f"状态码错误: 期望 {expected_status}, 实际 {response.status_code}")
                return False

            # 尝试解析JSON
            try:
                data = response.json()
                self.print_success("响应格式: JSON")

                # 打印响应摘要
                if isinstance(data, dict):
                    if 'code' in data:
                        self.print_info(f"业务码: {data.get('code')}")
                    if 'message' in data:
                        self.print_info(f"消息: {data.get('message')}")
                    if 'data' in data:
                        self.print_info(f"数据: {self._format_data_summary(data['data'])}")

                # 打印完整响应（仅在调试模式）
                if len(json.dumps(data, ensure_ascii=False)) < 500:
                    self.print_info(f"完整响应: {json.dumps(data, ensure_ascii=False, indent=2)}")

                return True

            except json.JSONDecodeError:
                if expected_status == 200:
                    self.print_error("响应不是有效的JSON")
                    self.print_info(f"响应内容: {response.text[:200]}")
                    return False
                else:
                    self.print_warning("响应不是JSON格式")
                    return True

        except requests.RequestException as e:
            self.print_error(f"请求失败: {str(e)}")
            return False

    def _format_data_summary(self, data):
        """格式化数据摘要"""
        if isinstance(data, dict):
            keys = list(data.keys())[:5]
            return f"Dict with keys: {keys}"
        elif isinstance(data, list):
            return f"List with {len(data)} items"
        else:
            return str(data)[:50]

    def run_all_tests(self):
        """运行所有测试"""
        start_time = datetime.now()

        self.print_header("知识星球打卡展示工具 - API测试")

        # 测试1: 健康检查
        self.test_endpoint(
            name="健康检查",
            method="GET",
            endpoint="/api/health"
        )

        # 测试2: Ping测试
        self.test_endpoint(
            name="Ping测试",
            method="GET",
            endpoint="/api/ping"
        )

        # 测试3: 获取项目列表 (进行中)
        projects = []
        result = self.test_endpoint(
            name="获取进行中的项目列表",
            method="GET",
            endpoint="/api/projects",
            params={"scope": "ongoing"}
        )
        if result:
            # 获取项目ID用于后续测试
            try:
                response = requests.get(f"{self.base_url}/api/projects?scope=ongoing")
                data = response.json()
                if data.get('code') == 0 and data.get('data', {}).get('projects'):
                    projects = data['data']['projects']
                    self.print_info(f"找到 {len(projects)} 个进行中的项目")
            except:
                pass

        # 测试4: 获取项目列表 (已关闭)
        self.test_endpoint(
            name="获取已关闭的项目列表",
            method="GET",
            endpoint="/api/projects",
            params={"scope": "closed"}
        )

        # 测试5: 获取项目列表 (已结束)
        self.test_endpoint(
            name="获取已结束的项目列表",
            method="GET",
            endpoint="/api/projects",
            params={"scope": "over"}
        )

        # 如果有项目，测试项目相关的接口
        if projects:
            project_id = projects[0]['project_id']
            self.print_info(f"\n使用项目ID: {project_id} 进行后续测试\n")

            # 测试6: 获取项目详情
            self.test_endpoint(
                name="获取项目详情",
                method="GET",
                endpoint=f"/api/projects/{project_id}"
            )

            # 测试7: 获取项目统计
            self.test_endpoint(
                name="获取项目统计",
                method="GET",
                endpoint=f"/api/projects/{project_id}/stats"
            )

            # 测试8: 获取每日统计
            self.test_endpoint(
                name="获取每日统计",
                method="GET",
                endpoint=f"/api/projects/{project_id}/daily-stats"
            )

            # 测试9: 获取连续打卡排行榜
            self.test_endpoint(
                name="获取连续打卡排行榜",
                method="GET",
                endpoint=f"/api/projects/{project_id}/leaderboard",
                params={"type": "continuous", "limit": 10}
            )

            # 测试10: 获取累计打卡排行榜
            self.test_endpoint(
                name="获取累计打卡排行榜",
                method="GET",
                endpoint=f"/api/projects/{project_id}/leaderboard",
                params={"type": "accumulated", "limit": 10}
            )

            # 测试11: 获取话题列表
            self.test_endpoint(
                name="获取话题列表",
                method="GET",
                endpoint=f"/api/projects/{project_id}/topics",
                params={"count": 20}
            )
        else:
            self.print_warning("没有找到项目，跳过项目相关接口测试")
            self.warnings += 6

        # 测试错误处理
        self.print_header("错误处理测试")

        # 测试12: 无效的项目ID
        self.test_endpoint(
            name="无效的项目ID",
            method="GET",
            endpoint="/api/projects/invalid_id",
            expected_status=400
        )

        # 测试13: 不存在的项目
        self.test_endpoint(
            name="不存在的项目",
            method="GET",
            endpoint="/api/projects/999999999",
            expected_status=404
        )

        # 测试14: 无效的排行榜类型
        if projects:
            self.test_endpoint(
                name="无效的排行榜类型",
                method="GET",
                endpoint=f"/api/projects/{projects[0]['project_id']}/leaderboard",
                params={"type": "invalid"},
                expected_status=400
            )

        # 打印测试摘要
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        self.print_header("测试摘要")
        print(f"{Colors.GREEN}✓ 通过: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}✗ 失败: {self.failed}{Colors.RESET}")
        print(f"{Colors.YELLOW}⚠ 警告: {self.warnings}{Colors.RESET}")
        print(f"总计: {self.passed + self.failed + self.warnings}")
        print(f"耗时: {duration:.2f}秒")

        if self.failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}所有测试通过! 🎉{Colors.RESET}\n")
            return 0
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}有 {self.failed} 个测试失败 ❌{Colors.RESET}\n")
            return 1


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='知识星球API测试工具')
    parser.add_argument(
        '--url',
        default='http://localhost:5000',
        help='API Base URL (默认: http://localhost:5000)'
    )

    args = parser.parse_args()

    # 检查服务是否运行
    try:
        response = requests.get(f"{args.url}/api/health", timeout=5)
        if response.status_code != 200:
            print(f"{Colors.RED}错误: API服务未正常运行{Colors.RESET}")
            print(f"请先启动服务: python backend/run.py")
            sys.exit(1)
    except requests.RequestException:
        print(f"{Colors.RED}错误: 无法连接到API服务 {args.url}{Colors.RESET}")
        print(f"请确认:")
        print(f"1. API服务已启动: python backend/run.py")
        print(f"2. 端口正确: {args.url}")
        sys.exit(1)

    # 运行测试
    tester = APITester(base_url=args.url)
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
