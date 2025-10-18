# ZSXQCheckIn - 知识星球打卡展示工具

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个基于Flask的知识星球打卡数据展示工具,通过逆向分析知识星球APP接口,为星主提供PC端查看打卡数据和排行榜的能力。

## 功能特性

- 📊 **打卡项目管理** - 查看所有打卡项目(进行中/已关闭/已结束)
- 🏆 **排行榜展示** - 支持连续打卡榜和累计打卡榜
- 📈 **统计数据** - 项目统计、每日统计等多维度数据分析
- 💬 **话题浏览** - 查看打卡话题列表
- 🚀 **Redis缓存** - 定时刷新机制,减少API调用频率
- ⚡ **高性能** - 支持高并发访问,响应速度快
- 🔒 **安全可靠** - Token配置化管理,不在代码中硬编码

## 技术栈

### 后端
- **语言**: Python 3.8+
- **框架**: Flask 3.0
- **缓存**: Redis
- **任务调度**: APScheduler
- **HTTP客户端**: requests

### 前端 (待开发)
- **框架**: React 18+
- **UI库**: Ant Design / Material-UI
- **构建工具**: Vite

## 项目结构

```
ZSXQCheckIn/
├── backend/                # 后端代码
│   ├── app/
│   │   ├── __init__.py    # Flask应用工厂
│   │   ├── routes/        # API路由
│   │   │   ├── __init__.py
│   │   │   ├── projects.py     # 项目相关路由
│   │   │   ├── health.py       # 健康检查
│   │   │   └── errors.py       # 错误处理
│   │   ├── services/      # 业务服务层
│   │   │   ├── zsxq_service.py     # 知识星球业务服务
│   │   │   ├── cache_service.py    # 缓存服务
│   │   │   └── scheduler.py        # 定时任务调度
│   │   ├── models/        # 数据模型
│   │   │   └── zsxq_client.py      # 知识星球API客户端
│   │   └── utils/         # 工具函数
│   │       ├── config_loader.py    # 配置加载
│   │       ├── logger.py           # 日志配置
│   │       ├── response.py         # 响应格式化
│   │       └── validators.py       # 参数验证
│   ├── run.py             # 开发环境启动入口
│   ├── wsgi.py            # 生产环境WSGI入口
│   └── requirements.txt   # Python依赖
├── frontend/              # 前端代码 (待开发)
├── doc/                   # 文档
│   ├── 需求分析文档.md
│   ├── 知识星球API接口文档.md
│   └── Redis缓存设计文档.md
├── config.example.yml     # 配置文件示例
├── .gitignore
├── CLAUDE.md              # Claude Code开发指南
└── README.md

```

## 快速开始

### 环境要求

- Python 3.8+
- Redis 6.0+ (可选,用于缓存)
- 知识星球账号和Token

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/ZSXQCheckIn.git
cd ZSXQCheckIn
```

### 2. 配置文件

复制配置示例文件并编辑:

```bash
cp config.example.yml config.yml
```

编辑 `config.yml`,填入你的知识星球Token和星球ID:

```yaml
知识星球:
  # 从Charles抓包获取的Authorization header
  token: "your_token_here"
  # 你的星球ID
  group_id: "your_group_id_here"
  api_base: "https://api.zsxq.com"

缓存配置:
  enabled: true
  redis:
    host: "localhost"
    port: 6379
    db: 0
    password: ""

系统配置:
  contact:
    type: "微信"
    value: "20133213"
  flask:
    host: "0.0.0.0"
    port: 5000
    debug: false
```

### 3. 获取Token

使用Charles或其他抓包工具,从知识星球APP抓取以下信息:

1. 打开Charles,配置SSL代理
2. 在手机上打开知识星球APP
3. 查看请求头中的 `Authorization` 字段,格式为 `UUID_HASH`
4. 从URL中获取 `group_id` (你的星球ID)

详细步骤参考: [doc/知识星球API接口文档.md](doc/知识星球API接口文档.md)

### 4. 安装依赖

#### Linux/Mac

```bash
# 使用启动脚本(推荐)
chmod +x start_dev.sh
./start_dev.sh
```

或手动安装:

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r backend/requirements.txt
```

#### Windows

```bash
# 使用启动脚本(推荐)
start_dev.bat
```

或手动安装:

```bash
# 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r backend\requirements.txt
```

### 5. 启动Redis (可选)

如果要使用缓存功能,需要先启动Redis:

```bash
# Linux/Mac
redis-server

# Windows (使用WSL或Redis for Windows)
redis-server.exe
```

如果Redis未运行,程序会自动降级到无缓存模式。

### 6. 运行应用

```bash
# 开发模式
python backend/run.py

# 或使用Flask CLI
export FLASK_APP=backend/run.py
flask run
```

应用将在 `http://localhost:5000` 启动。

### 7. 测试API

```bash
# 健康检查
curl http://localhost:5000/api/health

# 获取项目列表
curl http://localhost:5000/api/projects

# 获取排行榜
curl http://localhost:5000/api/projects/{project_id}/leaderboard?type=continuous
```

## API接口文档

### 基础信息

- **Base URL**: `http://localhost:5000/api`
- **响应格式**: JSON
- **编码**: UTF-8

### 接口列表

#### 1. 健康检查

```
GET /health
```

响应:
```json
{
  "status": "ok",
  "service": "ZSXQCheckIn API",
  "version": "1.0.0"
}
```

#### 2. 获取项目列表

```
GET /projects?scope=ongoing
```

参数:
- `scope` (可选): 项目范围 `ongoing`(进行中) | `closed`(已关闭) | `over`(已结束)

响应:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "projects": [
      {
        "project_id": "1141152412",
        "title": "2025年打卡挑战",
        "description": "每日打卡记录",
        "status": "ongoing",
        "total_members": 150,
        "total_checkins": 3500
      }
    ],
    "total": 1
  }
}
```

#### 3. 获取项目详情

```
GET /projects/{project_id}
```

#### 4. 获取项目统计

```
GET /projects/{project_id}/stats
```

#### 5. 获取排行榜

```
GET /projects/{project_id}/leaderboard?type=continuous&limit=10
```

参数:
- `type` (可选): 排行榜类型 `continuous`(连续打卡) | `accumulated`(累计打卡)
- `limit` (可选): 返回数量,默认10,最大100

#### 6. 获取每日统计

```
GET /projects/{project_id}/daily-stats
```

#### 7. 获取话题列表

```
GET /projects/{project_id}/topics?count=20
```

完整API文档: [doc/知识星球API接口文档.md](doc/知识星球API接口文档.md)

## 缓存机制

### 缓存策略

项目使用Redis实现缓存,采用**定时刷新**策略:

| 数据类型 | 缓存时长 | 刷新频率 |
|---------|---------|---------|
| 项目列表 | 2小时 | 每小时 |
| 排行榜 | 1小时 | 每30分钟 |
| 项目统计 | 1小时 | 每30分钟 |
| 每日统计 | 30分钟 | 每15分钟 |
| 话题列表 | 10分钟 | 每5分钟 |

### 缓存键设计

```
zsxq:projects:list:{scope}              # 项目列表
zsxq:project:{id}:info                  # 项目详情
zsxq:project:{id}:stats                 # 项目统计
zsxq:project:{id}:daily_stats           # 每日统计
zsxq:project:{id}:leaderboard:{type}    # 排行榜
zsxq:project:{id}:topics                # 话题列表
```

详细设计: [doc/Redis缓存设计文档.md](doc/Redis缓存设计文档.md)

## 部署

### 开发环境

```bash
# Linux/Mac
./start_dev.sh

# Windows
start_dev.bat
```

### 生产环境 (使用Gunicorn)

```bash
# 安装Gunicorn
pip install gunicorn

# 启动应用 (4个worker进程)
gunicorn -w 4 -b 0.0.0.0:5000 backend.wsgi:application
```

### Docker部署 (待完善)

```bash
# 构建镜像
docker build -t zsxq-checkin .

# 运行容器
docker run -d -p 5000:5000 \
  -v $(pwd)/config.yml:/app/config.yml \
  --name zsxq-checkin \
  zsxq-checkin
```

### Nginx反向代理

```nginx
server {
    listen 80;
    server_name zsxq.dc401.com;

    location /api/ {
        proxy_pass http://localhost:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /var/www/zsxq-frontend;
        try_files $uri /index.html;
    }
}
```

## 开发指南

### 代码规范

- Python: 遵循PEP 8规范
- 使用`black`格式化代码: `black backend/`
- 使用`flake8`检查代码: `flake8 backend/`

### 运行测试

项目提供了三种测试方式：

#### 1. 快速测试 (推荐)

```bash
# Windows
run_tests.bat
# 选择 [1] 快速测试

# Linux/Mac
python backend/tests/quick_test.py
```

快速验证所有API接口是否正常工作，输出简洁。

#### 2. 完整测试

```bash
# Windows
run_tests.bat
# 选择 [2] 完整测试

# Linux/Mac
python backend/tests/test_api.py
```

详细测试所有接口，包括错误处理和边界情况。

#### 3. curl测试 (Linux/Mac/Git Bash)

```bash
chmod +x backend/tests/test_curl.sh
./backend/tests/test_curl.sh
```

使用curl手动测试各个接口，适合调试单个接口。

**测试前提**:
- API服务必须已启动 (`start_dev.bat` 或 `python backend/run.py`)
- config.yml配置正确

详细测试文档: [backend/tests/README.md](backend/tests/README.md)

### 添加新的API接口

1. 在 `backend/app/routes/` 中添加路由
2. 在 `backend/app/services/zsxq_service.py` 中添加业务逻辑
3. 如需调用知识星球API,在 `backend/app/models/zsxq_client.py` 中添加方法
4. 更新API文档

## 常见问题

### Q: Token失效怎么办?

A: Token失效时API会返回401错误。需要重新抓包获取新的Token,更新 `config.yml`。

### Q: Redis连接失败?

A: 检查Redis是否运行,或在配置中禁用缓存:

```yaml
缓存配置:
  enabled: false
```

### Q: 如何限制API调用频率?

A: 在 `config.yml` 中配置限流:

```yaml
系统配置:
  rate_limit:
    enabled: true
    max_requests: 100  # 每分钟最大请求数
```

### Q: 如何查看日志?

A: 日志文件位于 `logs/app.log`,也可以在配置中开启控制台输出:

```yaml
日志配置:
  console: true
  level: "DEBUG"  # 调试时使用DEBUG级别
```

## 项目路线图

- [x] 后端API开发
  - [x] 知识星球API客户端封装
  - [x] RESTful API接口设计
  - [x] Redis缓存实现
  - [x] 定时任务调度
- [ ] 前端开发
  - [ ] 项目列表页
  - [ ] 排行榜详情页
  - [ ] 统计数据可视化
- [ ] 功能增强
  - [ ] Docker镜像
  - [ ] API限流
  - [ ] 用户认证
  - [ ] 数据导出功能

## 贡献指南

欢迎提交Issue和Pull Request!

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 微信: 20133213
- 项目地址: https://github.com/yourusername/ZSXQCheckIn
- 部署地址: https://zsxq.dc401.com (开发中)

## 致谢

- 感谢知识星球提供优秀的社区产品
- 本项目仅供学习交流使用,请勿用于商业用途

---

⚡ Generated with [Claude Code](https://claude.com/claude-code)
