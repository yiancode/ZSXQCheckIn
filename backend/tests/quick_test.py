"""
快速API测试脚本 - 简化版
运行方式: python backend/tests/quick_test.py
"""
import sys
import io
import requests
import json

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_api(base_url='http://localhost:5000'):
    """快速测试所有API"""

    print("=" * 60)
    print("知识星球API快速测试")
    print("=" * 60)

    tests = [
        ("健康检查", "GET", "/api/health"),
        ("Ping", "GET", "/api/ping"),
        ("项目列表(进行中)", "GET", "/api/projects?scope=ongoing"),
        ("项目列表(已关闭)", "GET", "/api/projects?scope=closed"),
        ("项目列表(已结束)", "GET", "/api/projects?scope=over"),
    ]

    project_id = None

    for name, method, path in tests:
        url = base_url + path
        try:
            response = requests.request(method, url, timeout=10)
            status = "✓" if response.status_code == 200 else "✗"
            print(f"{status} {name}: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    # 获取项目ID用于后续测试
                    if 'projects' in path and data.get('code') == 0:
                        projects = data.get('data', {}).get('projects', [])
                        if projects and not project_id:
                            project_id = projects[0]['project_id']
                            print(f"  → 找到项目ID: {project_id}")
                except:
                    pass
        except Exception as e:
            print(f"✗ {name}: {str(e)}")

    # 如果有项目ID，测试项目相关接口
    if project_id:
        print(f"\n使用项目ID {project_id} 测试项目接口:")
        print("-" * 60)

        project_tests = [
            (f"项目详情", "GET", f"/api/projects/{project_id}"),
            (f"项目统计", "GET", f"/api/projects/{project_id}/stats"),
            (f"每日统计", "GET", f"/api/projects/{project_id}/daily-stats"),
            (f"连续打卡榜", "GET", f"/api/projects/{project_id}/leaderboard?type=continuous&limit=5"),
            (f"累计打卡榜", "GET", f"/api/projects/{project_id}/leaderboard?type=accumulated&limit=5"),
            (f"话题列表", "GET", f"/api/projects/{project_id}/topics?count=10"),
        ]

        for name, method, path in project_tests:
            url = base_url + path
            try:
                response = requests.request(method, url, timeout=10)
                status = "✓" if response.status_code == 200 else "✗"
                print(f"{status} {name}: {response.status_code}")

                # 显示数据概要
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get('code') == 0 and 'data' in data:
                            result = data['data']
                            if isinstance(result, dict):
                                if 'rankings' in result:
                                    print(f"  → 返回 {len(result['rankings'])} 条排行榜数据")
                                elif 'topics' in result:
                                    print(f"  → 返回 {len(result['topics'])} 条话题")
                    except:
                        pass
            except Exception as e:
                print(f"✗ {name}: {str(e)}")
    else:
        print("\n警告: 没有找到项目，无法测试项目相关接口")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == '__main__':
    import sys

    # 检查服务是否运行
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=3)
    except:
        print("错误: API服务未运行")
        print("请先运行: python backend/run.py")
        sys.exit(1)

    test_api()
