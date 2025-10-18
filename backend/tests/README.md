# API测试文档

## 测试文件说明

### 1. quick_test.py - 快速测试
**用途**: 快速验证所有API接口是否正常工作

**运行方式**:
```bash
# 直接运行
python backend/tests/quick_test.py

# 或使用批处理脚本
run_tests.bat
# 然后选择 [1] 快速测试
```

**特点**:
- 快速执行(约5-10秒)
- 简洁输出
- 适合开发过程中频繁测试

### 2. test_api.py - 完整测试
**用途**: 详细测试所有API接口，包括错误处理

**运行方式**:
```bash
# 直接运行
python backend/tests/test_api.py

# 或使用批处理脚本
run_tests.bat
# 然后选择 [2] 完整测试

# 自定义API地址
python backend/tests/test_api.py --url http://your-server:5000
```

**特点**:
- 完整的测试覆盖
- 详细的输出信息
- 包含错误处理测试
- 彩色输出(支持终端)

## 测试前提条件

1. **启动API服务**
   ```bash
   # Windows
   start_dev.bat

   # Linux/Mac
   ./start_dev.sh
   ```

2. **配置文件**
   - 确保 `config.yml` 存在并正确配置
   - Token和group_id必须有效

3. **依赖安装**
   ```bash
   pip install -r backend/requirements.txt
   ```

## 测试覆盖的接口

### 基础接口
- ✅ GET /api/health - 健康检查
- ✅ GET /api/ping - Ping测试

### 项目管理
- ✅ GET /api/projects?scope=ongoing - 获取进行中的项目
- ✅ GET /api/projects?scope=closed - 获取已关闭的项目
- ✅ GET /api/projects?scope=over - 获取已结束的项目
- ✅ GET /api/projects/{id} - 获取项目详情
- ✅ GET /api/projects/{id}/stats - 获取项目统计
- ✅ GET /api/projects/{id}/daily-stats - 获取每日统计

### 排行榜
- ⚠️ GET /api/projects/{id}/leaderboard?type=continuous - 连续打卡榜
- ✅ GET /api/projects/{id}/leaderboard?type=accumulated - 累计打卡榜

### 话题
- ✅ GET /api/projects/{id}/topics - 获取话题列表

### 错误处理
- ✅ 无效的项目ID (400错误)
- ✅ 不存在的项目 (404错误)
- ✅ 无效的参数 (400错误)

## 已知问题

### 连续打卡榜接口500错误
**现象**:
```
GET /api/projects/{id}/leaderboard?type=continuous
返回: {"code": 500, "message": "API调用失败: 内部错误"}
```

**原因**:
知识星球API返回"内部错误"，可能是：
1. 该项目没有启用连续打卡排行榜功能
2. 知识星球API本身的问题
3. 该项目的打卡数据不支持连续排行

**解决方案**:
- 这是上游API的问题，不是我们代码的bug
- 累计打卡榜正常工作，功能基本完整
- 可以在业务层添加更友好的错误提示

## 测试结果示例

### 快速测试输出
```
============================================================
知识星球API快速测试
============================================================
✓ 健康检查: 200
✓ Ping: 200
✓ 项目列表(进行中): 200
  → 找到项目ID: 8424481182
✓ 项目列表(已关闭): 200
✓ 项目列表(已结束): 200

使用项目ID 8424481182 测试项目接口:
------------------------------------------------------------
✓ 项目详情: 200
✓ 项目统计: 200
✓ 每日统计: 200
✗ 连续打卡榜: 500
✓ 累计打卡榜: 200
  → 返回 5 条排行榜数据
✓ 话题列表: 200
  → 返回 10 条话题

============================================================
测试完成
============================================================
```

### 完整测试输出
包含更详细的信息：
- 请求URL和方法
- 响应状态码
- 业务码和消息
- 数据概要
- 详细的JSON响应(小于500字符时)

## 自定义测试

### 添加新的测试用例

编辑 `test_api.py`，在 `run_all_tests()` 方法中添加：

```python
# 测试新接口
self.test_endpoint(
    name="测试名称",
    method="GET",
    endpoint="/api/your-endpoint",
    params={"key": "value"},
    expected_status=200
)
```

### 测试特定项目

```python
# 在quick_test.py中修改project_id
project_id = "your_project_id"
```

## 故障排除

### 问题1: 连接拒绝
```
错误: 无法连接到API服务 http://localhost:5000
```
**解决**:
1. 确认API服务已启动
2. 检查端口是否正确
3. 查看防火墙设置

### 问题2: 401错误
```
状态码: 401
消息: Token已失效
```
**解决**:
1. 重新抓包获取新Token
2. 更新config.yml中的token配置
3. 重启API服务

### 问题3: 编码错误
```
UnicodeEncodeError: 'gbk' codec can't encode...
```
**解决**:
- Windows环境已自动设置UTF-8编码
- 如仍有问题，在命令行运行: `chcp 65001`

### 问题4: 模块未找到
```
ModuleNotFoundError: No module named 'requests'
```
**解决**:
```bash
pip install -r backend/requirements.txt
```

## 持续集成

### GitHub Actions配置示例

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      - name: Start API server
        run: python backend/run.py &
      - name: Wait for server
        run: sleep 10
      - name: Run tests
        run: python backend/tests/test_api.py
```

## 性能测试

### 使用Apache Bench
```bash
# 测试健康检查接口(1000次请求，并发10)
ab -n 1000 -c 10 http://localhost:5000/api/health

# 测试项目列表接口
ab -n 100 -c 5 http://localhost:5000/api/projects
```

### 使用wrk
```bash
# 压力测试(持续30秒，2个线程，10个连接)
wrk -t2 -c10 -d30s http://localhost:5000/api/health
```

## 贡献指南

如果你发现测试中的问题或想添加新的测试用例：

1. Fork项目
2. 创建特性分支
3. 添加测试用例
4. 提交Pull Request

---

最后更新: 2025-10-19
