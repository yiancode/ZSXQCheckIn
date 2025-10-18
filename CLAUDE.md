# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

知识星球项目打卡展示工具 - 通过逆向知识星球APP接口,为星主提供PC端打卡数据查看和排行榜展示能力。

**当前状态**: 项目初始化阶段,仅有设计文档,无实际代码
**部署域名**: zsxq.dc401.com
**联系方式**: 微信 20133213

## 技术栈与架构

### 技术选型
```
后端: Python 3.8+ + Flask + Redis + APScheduler + requests
前端: React 18+ + (Ant Design/Material-UI) + axios + Vite
部署: Docker + Nginx
```

### 系统架构
```
用户 -> Nginx -> React前端 (zsxq.dc401.com)
              -> Flask后端 (/api/*) -> 知识星球API
                                    -> Redis缓存
                                    -> 定时任务(APScheduler)
```

**关键设计**:
- 单星主单部署(每个星主独立部署一套)
- 前后端分离
- API实时数据,Web页面使用Redis缓存(1小时刷新)
- Redis故障时降级到实时查询

## 目录结构规划

```
ZSXQCheckIn/
├── backend/                 # Flask后端
│   ├── app/
│   │   ├── __init__.py     # Flask应用初始化
│   │   ├── api/            # RESTful API路由
│   │   ├── services/       # 业务逻辑层
│   │   ├── clients/        # 知识星球API客户端
│   │   ├── cache/          # Redis缓存封装
│   │   └── config/         # 配置加载
│   ├── tests/              # pytest单元测试
│   ├── requirements.txt
│   └── run.py              # 启动入口
├── frontend/               # React前端
│   ├── src/
│   │   ├── components/     # 可复用组件
│   │   ├── pages/          # 页面:首页、详情页
│   │   ├── services/       # API请求封装
│   │   └── utils/
│   ├── public/
│   └── package.json
├── deploy/
│   ├── nginx.conf          # Nginx配置
│   ├── Dockerfile
│   └── docker-compose.yml
├── doc/
│   └── 需求分析文档.md      # 详细需求文档
├── config.example.yml      # 配置示例(不含真实token)
└── .gitignore              # 必须包含 config.yml
```

## API设计规范

### 接口列表
```
GET  /api/projects                            # 获取所有打卡项目
GET  /api/projects/{id}/stats                 # 项目统计数据
GET  /api/projects/{id}/leaderboard/continuous # 连续打卡榜
GET  /api/projects/{id}/leaderboard/total     # 累计打卡榜
GET  /api/projects/{id}/checkins              # 打卡记录
GET  /api/users/{user_id}/stats?project_id=   # 用户统计
```

### 统一响应格式
```json
成功:
{
  "code": 200,
  "message": "success",
  "data": { /* 业务数据 */ },
  "timestamp": "2025-10-19T12:00:00Z"
}

失败:
{
  "code": 401,
  "message": "Token已失效,请联系管理员更新。微信:20133213",
  "data": null,
  "timestamp": "2025-10-19T12:00:00Z"
}
```

### HTTP状态码规范
- `200`: 成功
- `400`: 参数错误
- `401`: Token失效(提示联系微信:20133213)
- `429`: API限流
- `500`: 系统错误

## Redis Key设计

```
zsxq:projects:list                            # 项目列表
zsxq:project:{project_id}:info                # 项目详情
zsxq:project:{project_id}:leaderboard:continuous # 连续打卡榜
zsxq:project:{project_id}:leaderboard:total   # 累计打卡榜
zsxq:project:{project_id}:checkins            # 打卡记录
zsxq:user:{user_id}:stats:{project_id}        # 用户统计
```

**过期策略**: 定时任务刷新,TTL设置为2小时(缓存间隔1小时+1小时容错)

## 配置管理

**config.yml** (不提交到Git):
```yaml
知识星球:
  token: "your_zsxq_token"        # 从APP抓包获取
  group_id: "your_group_id"

缓存配置:
  enabled: true
  interval: 3600                  # 刷新间隔(秒)
  host: "localhost"
  port: 6379
  db: 0

系统配置:
  contact:
    type: "微信"
    value: "20133213"
  rate_limit:
    enabled: true
    max_requests: 100             # 每分钟限制

排行榜配置:
  max_items: 100                  # API最大返回数
  homepage_preview: 10            # 首页预览条数
```

**安全要求**:
- Token禁止硬编码,必须从配置文件读取
- `config.yml` 必须在 `.gitignore` 中
- 提供 `config.example.yml` 作为模板

## 开发环境设置

### 后端开发
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py                   # 启动Flask开发服务器(默认5000端口)
```

### 前端开发
```bash
cd frontend
npm install                     # Node.js 16+
npm run dev                     # 启动Vite开发服务器(默认5173端口)
```

### Redis服务
```bash
docker run -d -p 6379:6379 redis:alpine
# 或本地: redis-server
```

## 常用命令

### 后端
```bash
# 测试
cd backend
python -m pytest tests/ -v

# 代码格式化
black app/
flake8 app/

# 运行服务
python run.py
```

### 前端
```bash
# 开发
npm run dev

# 构建
npm run build

# 代码检查
npm run lint

# 测试
npm test
```

### Docker部署
```bash
# 构建并启动(前端+后端+Redis)
docker-compose up --build -d

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 停止
docker-compose down
```

## 代码规范

### Python (PEP 8)
- 使用 `black` 格式化
- 使用 `flake8` 检查
- 类型注解(可选但推荐)
- 每个模块添加docstring

### JavaScript/React
- ESLint + Prettier
- 函数组件优先
- Hooks使用规范
- PropTypes或TypeScript(待定)

### Git提交规范
```
<type>(<scope>): <subject>

类型:
- feat: 新功能
- fix: Bug修复
- docs: 文档
- style: 格式
- refactor: 重构
- test: 测试
- chore: 构建/工具

示例:
feat(api): 添加获取项目列表接口
fix(cache): 修复Redis连接超时
docs(readme): 更新部署说明
```

### 分支策略
- `main`: 生产环境
- `develop`: 开发主分支
- `feature/*`: 新功能
- `fix/*`: Bug修复

## 日志规范

需要记录的日志:
- API调用日志(请求/响应/耗时)
- 错误日志(异常堆栈/上下文)
- 缓存操作日志(刷新时间/数据量)
- 知识星球API调用日志(频率监控)

## 测试要求

- 后端API必须有单元测试
- 关键业务逻辑需要测试覆盖
- 缓存降级逻辑需要测试
- API错误处理需要测试

## 功能边界(明确不做)

- ❌ 多星球统一管理
- ❌ 历史数据深度分析
- ❌ 打卡编辑/删除/补卡
- ❌ 打卡提醒功能
- ❌ 社区互动(评论、点赞)
- ❌ 复杂权限系统(当前完全公开)
- ❌ 移动端APP

## 技术风险与应对

### 知识星球API变更 (高风险)
- 定期监控接口变化
- 接口调用失败时及时告警
- 保持API客户端代码的灵活性

### 接口限流 (中风险)
- 实现Redis缓存降低调用频率
- 添加请求频率限制
- 监控API调用次数

### Token过期 (中风险)
- 配置化管理
- Token失效时明确提示联系方式(微信:20133213)
- 未来考虑自动Token刷新机制

## 下一步工作清单

1. ✅ 需求分析完成
2. ⏭️ 使用Charles抓包知识星球APP接口
3. ⏭️ 整理完整API列表和数据结构
4. ⏭️ 初始化Flask项目结构
5. ⏭️ 实现知识星球API客户端
6. ⏭️ 实现Redis缓存层
7. ⏭️ 实现Flask API接口
8. ⏭️ 初始化React项目
9. ⏭️ 实现前端页面(首页+详情页)
10. ⏭️ 前后端联调
11. ⏭️ Docker部署配置
12. ⏭️ 部署到 zsxq.dc401.com
13. ⏭️ 编写README和部署文档
14. ⏭️ 代码开源发布

## 参考文档

- **详细需求**: `doc/需求分析文档.md`
- **Flask文档**: https://flask.palletsprojects.com/
- **React文档**: https://react.dev/
- **Redis文档**: https://redis.io/
