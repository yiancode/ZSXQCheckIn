# 结构化提示词模板库

本文档整理了对话过程中体现的各类提示词模板,可用于类似场景。

---

## 1. 代码库分析提示词

### 1.1 全局探索提示词

**目标**: 系统化探索代码库结构

```
请分析这个代码库并完成以下任务:

1. 文件结构探索
   - 搜索所有主要文件类型
   - 识别项目类型和技术栈
   - 查找配置和文档文件

2. 关键内容读取
   - README.md
   - 需求/设计文档
   - 配置文件
   - 已有的开发指南

3. 项目特征分析
   - 技术栈识别
   - 架构设计理解
   - 开发流程提取
   - 常用命令识别

4. 输出格式
   - 项目概述
   - 技术架构
   - 开发指南
   - 重要约束
```

**适用场景**:
- 新项目onboarding
- 项目文档生成
- 技术债务评估

---

### 1.2 文件搜索提示词模式

**模式**: 按类型逐步搜索

```bash
# 第一层: 顶层文件
Glob: *

# 第二层: 按语言搜索
Glob: **/*.js
Glob: **/*.ts
Glob: **/*.py
Glob: **/*.java

# 第三层: 配置文件
Glob: **/*.json
Glob: **/*.yml
Glob: **/*.yaml

# 第四层: 文档
Glob: **/*.md

# 第五层: 隐藏文件
Bash: ls -la
```

**设计原理**:
- 从通用到具体
- 先结构后内容
- 确保全覆盖

---

## 2. 文档生成提示词

### 2.1 架构文档生成模板

```markdown
基于以下信息生成架构文档:

## 输入要求
- 已读取的代码文件列表
- 需求文档内容
- 现有的README

## 输出结构
### 1. 系统概述
   - 项目定位
   - 核心价值
   - 技术特点

### 2. 架构设计
   - 系统架构图
   - 技术栈说明
   - 模块划分
   - 数据流向

### 3. 关键决策
   - 技术选型理由
   - 架构模式选择
   - 重要约束

### 4. 开发指南
   - 环境搭建
   - 常用命令
   - 开发规范

## 质量要求
- 基于事实,不编造
- 聚焦大局,不陷入细节
- 实用导向,可操作
- 结构清晰,易查阅
```

---

### 2.2 API文档生成模板

```markdown
为以下API生成标准文档:

## 文档结构

### 1. 接口列表
\`\`\`
HTTP方法 路径 功能描述
GET /api/resource 获取资源列表
POST /api/resource 创建资源
\`\`\`

### 2. 详细说明
每个接口包含:
- 功能描述
- 请求参数
- 请求示例
- 响应格式
- 错误码说明

### 3. 统一规范
- 响应格式标准
- HTTP状态码约定
- 错误处理规范
- 认证方式

### 4. 使用示例
- cURL示例
- 客户端代码示例
- 常见场景演示
```

---

## 3. 代码规范提示词

### 3.1 代码风格规范模板

```yaml
代码风格规范定义:

语言特定:
  Python:
    - 遵循: PEP 8
    - 格式化工具: black
    - 检查工具: flake8
    - 类型注解: 推荐使用

  JavaScript/TypeScript:
    - 遵循: Airbnb Style Guide
    - 格式化工具: Prettier
    - 检查工具: ESLint
    - 类型: TypeScript优先

通用规范:
  命名:
    - 变量: camelCase / snake_case
    - 常量: UPPER_CASE
    - 类: PascalCase
    - 函数: camelCase / snake_case

  注释:
    - 模块级: docstring/JSDoc
    - 函数级: 参数和返回值说明
    - 复杂逻辑: 行内注释

  文件组织:
    - 每个文件单一职责
    - 相关功能就近放置
    - 避免循环依赖
```

---

### 3.2 Git提交规范模板

```
Git提交信息规范:

格式:
<type>(<scope>): <subject>

<body>

<footer>

类型(type):
- feat: 新功能
- fix: Bug修复
- docs: 文档更新
- style: 代码格式(不影响功能)
- refactor: 重构
- test: 测试相关
- chore: 构建/工具/依赖

范围(scope):
- api: API接口
- ui: 用户界面
- db: 数据库
- cache: 缓存
- config: 配置

示例:
feat(api): 添加用户认证接口

实现了基于JWT的用户认证机制
- 添加登录接口
- 添加Token验证中间件
- 添加刷新Token接口

Closes #123
```

---

## 4. 项目初始化提示词

### 4.1 后端项目初始化模板

```bash
# Python + Flask 项目初始化

## 目录结构
mkdir -p backend/{app/{api,services,models,utils},tests,config}

## 创建核心文件
touch backend/app/__init__.py
touch backend/app/api/__init__.py
touch backend/app/api/routes.py
touch backend/app/services/__init__.py
touch backend/app/models/__init__.py
touch backend/requirements.txt
touch backend/run.py

## 虚拟环境
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

## 安装依赖
pip install flask flask-cors redis requests apscheduler
pip freeze > requirements.txt

## 配置文件
cp config.example.yml config.yml
```

---

### 4.2 前端项目初始化模板

```bash
# React + Vite 项目初始化

## 创建项目
npm create vite@latest frontend -- --template react

## 安装依赖
cd frontend
npm install

## 安装UI库和工具
npm install antd axios zustand
npm install -D eslint prettier

## 目录结构
mkdir -p src/{components,pages,services,utils,hooks}

## 配置文件
touch .eslintrc.json
touch .prettierrc
touch .env.example
```

---

## 5. 配置管理提示词

### 5.1 配置文件设计模板

```yaml
# 配置文件结构设计

配置分层:
  1. 环境配置(.env):
     - 敏感信息(密钥、token)
     - 环境差异项(数据库连接)

  2. 应用配置(config.yml):
     - 业务参数
     - 功能开关
     - 默认值

  3. 常量定义(constants):
     - 不变的业务常量
     - 枚举值
     - 魔法数字

安全要求:
  - 敏感信息不提交代码库
  - 提供example文件作为模板
  - 使用环境变量覆盖
  - 配置验证和默认值

示例结构:
config/
├── .env.example          # 环境变量模板
├── config.yml.example    # 配置文件模板
├── config.py             # 配置加载逻辑
└── constants.py          # 常量定义
```

---

### 5.2 环境配置提示词模板

```bash
# 环境配置清单

## 开发环境
export FLASK_ENV=development
export FLASK_DEBUG=1
export REDIS_HOST=localhost
export REDIS_PORT=6379
export LOG_LEVEL=DEBUG

## 测试环境
export FLASK_ENV=testing
export FLASK_DEBUG=0
export REDIS_HOST=redis-test
export LOG_LEVEL=INFO

## 生产环境
export FLASK_ENV=production
export FLASK_DEBUG=0
export REDIS_HOST=redis-prod
export LOG_LEVEL=WARNING
export SECRET_KEY=${SECRET_KEY}  # 从密钥管理系统获取
```

---

## 6. 错误处理提示词

### 6.1 统一错误处理模板

```python
# 错误处理规范

## 错误分类
1. 业务错误(4xx)
   - 参数错误(400)
   - 认证失败(401)
   - 权限不足(403)
   - 资源不存在(404)
   - 请求冲突(409)
   - 限流(429)

2. 系统错误(5xx)
   - 服务器内部错误(500)
   - 网关错误(502)
   - 服务不可用(503)

## 错误响应格式
{
  "code": 400,
  "message": "参数错误: 缺少必需参数 'user_id'",
  "error_type": "VALIDATION_ERROR",
  "details": {
    "field": "user_id",
    "constraint": "required"
  },
  "timestamp": "2025-10-19T12:00:00Z",
  "request_id": "req_123456"
}

## 错误处理原则
1. 明确的错误信息
2. 帮助用户解决问题
3. 避免暴露敏感信息
4. 记录详细日志
5. 提供联系方式(如需要)
```

---

### 6.2 降级策略提示词模板

```yaml
服务降级策略:

层级降级:
  L1_缓存失败:
    策略: 降级到实时查询
    影响: 响应时间增加
    监控: 缓存命中率

  L2_外部API失败:
    策略: 返回默认数据或错误提示
    影响: 功能受限
    监控: API成功率

  L3_数据库不可用:
    策略: 只读模式或完全降级
    影响: 服务中断
    监控: 数据库连接状态

降级开关:
  配置项: features.degradation
  触发方式:
    - 自动: 错误率阈值触发
    - 手动: 配置中心切换

恢复机制:
  - 自动重试(指数退避)
  - 熔断器(Circuit Breaker)
  - 健康检查(Health Check)
```

---

## 7. 测试相关提示词

### 7.1 测试策略模板

```markdown
测试策略定义:

## 测试分层

### 1. 单元测试
- 覆盖率: ≥80%
- 工具: pytest / Jest
- 运行频率: 每次提交

### 2. 集成测试
- 覆盖: 关键业务流程
- 工具: pytest / Supertest
- 运行频率: 每次合并

### 3. 端到端测试
- 覆盖: 核心用户路径
- 工具: Playwright / Cypress
- 运行频率: 发布前

## 测试数据管理
- 使用固定的测试数据集
- 测试数据独立于生产环境
- 每次测试后清理数据

## 测试命令
\`\`\`bash
# 运行所有测试
pytest

# 运行单个测试
pytest tests/test_api.py::test_get_projects

# 生成覆盖率报告
pytest --cov=app --cov-report=html
\`\`\`
```

---

### 7.2 测试用例模板

```python
# 测试用例结构模板

import pytest

class TestProjectAPI:
    """项目API测试类"""

    @pytest.fixture
    def client(self):
        """测试客户端"""
        # 初始化测试客户端
        pass

    @pytest.fixture
    def sample_data(self):
        """测试数据"""
        return {
            "project_id": "test_001",
            "name": "测试项目"
        }

    def test_get_projects_success(self, client):
        """测试获取项目列表-成功"""
        # Given: 准备数据

        # When: 执行操作
        response = client.get('/api/projects')

        # Then: 验证结果
        assert response.status_code == 200
        assert 'data' in response.json()

    def test_get_projects_invalid_token(self, client):
        """测试获取项目列表-Token无效"""
        # Given: 无效Token

        # When: 执行操作
        response = client.get('/api/projects?token=invalid')

        # Then: 验证错误响应
        assert response.status_code == 401
        assert '失效' in response.json()['message']

    def test_get_projects_with_cache(self, client, mocker):
        """测试获取项目列表-使用缓存"""
        # Given: Mock缓存
        mock_cache = mocker.patch('app.cache.get')
        mock_cache.return_value = {"cached": True}

        # When: 执行操作
        response = client.get('/api/projects')

        # Then: 验证使用了缓存
        assert mock_cache.called
```

---

## 8. 部署相关提示词

### 8.1 Docker部署模板

```dockerfile
# Dockerfile 模板

# 后端 Dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "run.py"]
```

```yaml
# docker-compose.yml 模板
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - REDIS_HOST=redis
    depends_on:
      - redis
    volumes:
      - ./config.yml:/app/config.yml

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

---

### 8.2 Nginx配置模板

```nginx
# nginx.conf 模板

server {
    listen 80;
    server_name zsxq.dc401.com;

    # 前端静态资源
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # API反向代理
    location /api/ {
        proxy_pass http://backend:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 9. 监控和日志提示词

### 9.1 日志规范模板

```python
# 日志规范

import logging

# 日志级别使用
logging.debug("详细的调试信息")
logging.info("关键业务流程信息")
logging.warning("警告但不影响运行")
logging.error("错误但服务继续")
logging.critical("严重错误,服务中断")

# 日志格式
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 结构化日志
logger.info("API调用", extra={
    "method": "GET",
    "path": "/api/projects",
    "status": 200,
    "duration_ms": 150,
    "user_id": "user_123"
})

# 错误日志(包含堆栈)
try:
    # 操作
    pass
except Exception as e:
    logger.error("操作失败", exc_info=True, extra={
        "operation": "get_projects",
        "error_type": type(e).__name__
    })
```

---

### 9.2 监控指标模板

```yaml
监控指标定义:

业务指标:
  - API调用次数
  - API成功率
  - API平均响应时间
  - API P95/P99响应时间
  - 缓存命中率
  - 用户活跃度

系统指标:
  - CPU使用率
  - 内存使用率
  - 磁盘使用率
  - 网络流量

依赖服务:
  - Redis连接状态
  - Redis内存使用
  - 外部API可用性
  - 外部API响应时间

告警规则:
  - API错误率 > 5%
  - API响应时间 > 3s
  - Redis连接失败
  - CPU使用率 > 80%
  - 内存使用率 > 90%
```

---

## 10. 文档维护提示词

### 10.1 文档更新检查清单

```markdown
文档更新检查清单:

## 何时更新文档

### 架构变更
- [ ] 更新架构图
- [ ] 更新技术栈说明
- [ ] 更新模块划分

### API变更
- [ ] 更新接口列表
- [ ] 更新请求/响应格式
- [ ] 更新错误码

### 配置变更
- [ ] 更新配置示例
- [ ] 更新环境变量说明
- [ ] 更新部署文档

### 流程变更
- [ ] 更新开发流程
- [ ] 更新发布流程
- [ ] 更新常用命令

## 文档质量检查
- [ ] 所有命令可执行
- [ ] 所有链接可访问
- [ ] 配置示例准确
- [ ] 没有过时信息
- [ ] 格式规范统一
```

---

## 使用说明

### 如何使用这些模板

1. **识别场景**: 确定当前任务属于哪个类别
2. **选择模板**: 找到对应的提示词模板
3. **定制化**: 根据具体项目调整模板
4. **执行验证**: 执行后验证输出质量
5. **持续优化**: 根据效果优化模板

### 模板组合使用

复杂任务可以组合多个模板:
- 项目初始化 = 代码库分析 + 项目初始化 + 配置管理
- API开发 = API文档生成 + 错误处理 + 测试策略
- 部署上线 = Docker部署 + Nginx配置 + 监控日志

### 模板扩展

根据项目特点可以扩展模板:
- 添加特定领域的规范
- 增加团队特有的约定
- 补充常见问题FAQ
- 记录最佳实践

---

## 模板索引

### 按场景分类
- **项目初始化**: 1.1, 4.1, 4.2, 5.1
- **代码开发**: 3.1, 3.2, 6.1, 7.1
- **文档编写**: 2.1, 2.2, 10.1
- **部署运维**: 5.2, 8.1, 8.2, 9.1, 9.2

### 按角色分类
- **开发人员**: 3.1, 4.1, 4.2, 7.1
- **架构师**: 1.1, 2.1, 6.2
- **运维人员**: 5.2, 8.1, 8.2, 9.2
- **技术写作**: 2.1, 2.2, 10.1

### 按优先级分类
- **必需**: 1.1, 2.1, 3.1, 5.1
- **推荐**: 3.2, 6.1, 7.1, 8.1
- **可选**: 9.1, 9.2, 10.1
