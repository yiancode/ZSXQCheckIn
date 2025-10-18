#!/bin/bash
# API接口curl测试脚本
# 用途: 使用curl手动测试所有API接口

BASE_URL="http://localhost:5000"
PROJECT_ID=""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印分隔线
print_separator() {
    echo "============================================================"
}

# 打印标题
print_title() {
    echo -e "${BLUE}${1}${NC}"
}

# 测试接口
test_endpoint() {
    local name=$1
    local url=$2

    echo ""
    print_title "测试: $name"
    echo "URL: $url"
    echo ""

    response=$(curl -s -w "\n%{http_code}" "$url")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" == "200" ]; then
        echo -e "${GREEN}✓ 状态码: $http_code${NC}"
    else
        echo -e "${RED}✗ 状态码: $http_code${NC}"
    fi

    echo "响应:"
    echo "$body" | python -m json.tool 2>/dev/null || echo "$body"
    echo ""
}

# 主函数
main() {
    print_separator
    print_title "知识星球API接口测试 (curl)"
    print_separator

    # 1. 健康检查
    test_endpoint "健康检查" "$BASE_URL/api/health"

    # 2. Ping
    test_endpoint "Ping测试" "$BASE_URL/api/ping"

    # 3. 项目列表
    test_endpoint "项目列表(进行中)" "$BASE_URL/api/projects?scope=ongoing"

    # 获取项目ID
    response=$(curl -s "$BASE_URL/api/projects?scope=ongoing")
    PROJECT_ID=$(echo "$response" | python -c "import sys, json; data=json.load(sys.stdin); print(data['data']['projects'][0]['project_id'] if data.get('data', {}).get('projects') else '')" 2>/dev/null)

    if [ -z "$PROJECT_ID" ]; then
        echo -e "${YELLOW}警告: 没有找到项目ID，跳过项目相关测试${NC}"
        exit 0
    fi

    echo -e "${GREEN}找到项目ID: $PROJECT_ID${NC}"

    # 4. 项目详情
    test_endpoint "项目详情" "$BASE_URL/api/projects/$PROJECT_ID"

    # 5. 项目统计
    test_endpoint "项目统计" "$BASE_URL/api/projects/$PROJECT_ID/stats"

    # 6. 每日统计
    test_endpoint "每日统计" "$BASE_URL/api/projects/$PROJECT_ID/daily-stats"

    # 7. 连续打卡排行榜
    test_endpoint "连续打卡排行榜" "$BASE_URL/api/projects/$PROJECT_ID/leaderboard?type=continuous&limit=5"

    # 8. 累计打卡排行榜
    test_endpoint "累计打卡排行榜" "$BASE_URL/api/projects/$PROJECT_ID/leaderboard?type=accumulated&limit=5"

    # 9. 话题列表
    test_endpoint "话题列表" "$BASE_URL/api/projects/$PROJECT_ID/topics?count=10"

    print_separator
    print_title "测试完成"
    print_separator
}

# 运行测试
main
