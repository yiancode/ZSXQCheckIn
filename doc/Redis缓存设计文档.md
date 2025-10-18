# Redis缓存设计文档

## 缓存架构概述

### 设计原则
1. **仅用于Web页面访问**: API直接调用时不使用缓存,实时查询知识星球接口
2. **定时刷新策略**: 使用APScheduler定时刷新缓存,而非被动过期
3. **降级容错**: Redis故障时自动降级到实时查询
4. **统一键命名**: 使用可配置的键前缀,方便多实例部署

### 缓存流程

```
用户请求 -> Flask路由 -> 服务层 -> 缓存层检查
                                    |
                    +--------------+---------------+
                    |                              |
                存在缓存                         缓存未命中
                    |                              |
                返回缓存数据                  调用知识星球API
                                                  |
                                            更新缓存 + 返回数据
```

## 缓存键设计

### 键命名规范

格式: `{prefix}:{resource}:{id}:{subresource}`

- **prefix**: 可配置前缀(默认: `zsxq`)
- **resource**: 资源类型(如: `project`, `projects`)
- **id**: 资源ID
- **subresource**: 子资源类型

### 缓存键列表

| 缓存键模板 | 说明 | 示例 | TTL |
|----------|------|------|-----|
| `zsxq:projects:list:{scope}` | 项目列表(按scope分组) | `zsxq:projects:list:ongoing` | 2小时 |
| `zsxq:project:{id}:info` | 项目详情 | `zsxq:project:1141152412:info` | 2小时 |
| `zsxq:project:{id}:stats` | 项目统计数据 | `zsxq:project:1141152412:stats` | 1小时 |
| `zsxq:project:{id}:daily_stats` | 每日统计数据 | `zsxq:project:1141152412:daily_stats` | 30分钟 |
| `zsxq:project:{id}:leaderboard:{type}` | 排行榜数据 | `zsxq:project:1141152412:leaderboard:continuous` | 1小时 |
| `zsxq:project:{id}:topics` | 话题列表 | `zsxq:project:1141152412:topics` | 10分钟 |

### 键模式匹配

清除项目相关所有缓存:
```
zsxq:project:{project_id}:*
```

## 缓存策略

### 1. 项目列表缓存

**缓存键**: `zsxq:projects:list:{scope}`

**数据结构**:
```json
{
  "projects": [
    {
      "project_id": "1141152412",
      "title": "2025年打卡挑战",
      "status": "ongoing",
      "total_members": 150,
      "total_checkins": 3500
    }
  ],
  "cached_at": "2025-01-15T10:30:00Z"
}
```

**刷新策略**:
- TTL: 7200秒 (2小时)
- 定时刷新: 每小时
- 失效条件: 无(定时刷新覆盖)

### 2. 排行榜缓存

**缓存键**: `zsxq:project:{project_id}:leaderboard:{type}`

**数据结构**:
```json
{
  "type": "continuous",
  "rankings": [
    {
      "rank": 1,
      "user": {
        "user_id": 585221282158424,
        "name": "伊雪儿",
        "avatar": "https://..."
      },
      "days": 10
    }
  ],
  "total": 100,
  "cached_at": "2025-01-15T10:30:00Z"
}
```

**刷新策略**:
- TTL: 3600秒 (1小时)
- 定时刷新: 每30分钟
- 失效条件: 无(定时刷新覆盖)

### 3. 项目统计缓存

**缓存键**: `zsxq:project:{project_id}:stats`

**数据结构**:
```json
{
  "total_members": 150,
  "total_checkins": 3500,
  "today_checkins": 120,
  "continuous_rate": 0.85,
  "cached_at": "2025-01-15T10:30:00Z"
}
```

**刷新策略**:
- TTL: 3600秒 (1小时)
- 定时刷新: 每30分钟
- 失效条件: 无(定时刷新覆盖)

### 4. 每日统计缓存

**缓存键**: `zsxq:project:{project_id}:daily_stats`

**数据结构**:
```json
{
  "date": "2025-01-15",
  "total_checkins": 120,
  "new_members": 5,
  "active_members": 115,
  "cached_at": "2025-01-15T10:30:00Z"
}
```

**刷新策略**:
- TTL: 1800秒 (30分钟)
- 定时刷新: 每15分钟
- 失效条件: 跨天时强制刷新

### 5. 话题列表缓存

**缓存键**: `zsxq:project:{project_id}:topics`

**数据结构**:
```json
{
  "topics": [
    {
      "topic_id": "123456",
      "title": "今日打卡",
      "create_time": "2025-01-15 08:30:00",
      "user": {
        "user_id": 585221282158424,
        "name": "张三"
      }
    }
  ],
  "cached_at": "2025-01-15T10:30:00Z"
}
```

**刷新策略**:
- TTL: 600秒 (10分钟)
- 定时刷新: 每5分钟
- 失效条件: 无(定时刷新覆盖)

## 定时任务设计

### 使用APScheduler实现定时刷新

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

# 每小时刷新项目列表
scheduler.add_job(refresh_projects_list, 'interval', hours=1)

# 每30分钟刷新排行榜
scheduler.add_job(refresh_leaderboards, 'interval', minutes=30)

# 每15分钟刷新每日统计
scheduler.add_job(refresh_daily_stats, 'interval', minutes=15)

# 每5分钟刷新话题列表
scheduler.add_job(refresh_topics, 'interval', minutes=5)

scheduler.start()
```

### 任务优先级

1. **高频刷新** (每5-10分钟): 话题列表
2. **中频刷新** (每15-30分钟): 每日统计、排行榜、项目统计
3. **低频刷新** (每小时): 项目列表、项目详情

## 缓存降级策略

### Redis故障处理

```python
def get_with_fallback(cache_key, fetch_func):
    """
    带降级的缓存获取

    Args:
        cache_key: 缓存键
        fetch_func: 实时获取函数

    Returns:
        数据
    """
    # 尝试从缓存获取
    if CacheService.is_enabled():
        data = CacheService.get(cache_key)
        if data:
            return data

    # 缓存未命中或Redis故障,调用实时接口
    data = fetch_func()

    # 尝试写入缓存
    if CacheService.is_enabled():
        CacheService.set(cache_key, data)

    return data
```

### 错误处理

- **连接失败**: 自动降级到无缓存模式,记录警告日志
- **读取失败**: 忽略缓存,直接查询API,记录错误日志
- **写入失败**: 忽略写入错误,保证业务正常,记录错误日志

## 缓存监控

### 监控指标

1. **命中率**: 缓存命中次数 / 总请求次数
2. **刷新成功率**: 定时刷新成功次数 / 总刷新次数
3. **Redis连接状态**: 正常/故障
4. **缓存键数量**: 当前Redis中的键总数
5. **内存使用量**: Redis内存占用

### 日志记录

需要记录以下日志:
- 缓存命中: `DEBUG` 级别
- 缓存未命中: `INFO` 级别
- 定时刷新完成: `INFO` 级别
- Redis连接失败: `WARNING` 级别
- 缓存操作异常: `ERROR` 级别

## 配置示例

```yaml
缓存配置:
  enabled: true
  interval: 3600  # 默认刷新间隔(秒)
  redis:
    host: "localhost"
    port: 6379
    db: 0
    password: ""
    key_prefix: "zsxq:"
    default_ttl: 7200  # 默认2小时

  # 定时任务配置
  scheduler:
    projects_list: 3600      # 每小时
    leaderboard: 1800        # 每30分钟
    project_stats: 1800      # 每30分钟
    daily_stats: 900         # 每15分钟
    topics: 300              # 每5分钟
```

## 最佳实践

1. **避免缓存穿透**: 所有API返回的空数据也要缓存(TTL较短)
2. **避免缓存雪崩**: 不同类型数据使用不同的TTL
3. **避免热key问题**: 使用定时刷新而非被动过期
4. **数据一致性**: 通过定时刷新保证最终一致性
5. **错误容忍**: 缓存层故障不影响核心业务流程

## 性能优化

### 批量操作

对于需要获取多个项目数据的场景,使用Redis Pipeline:

```python
def get_multiple_projects(project_ids):
    """批量获取项目信息"""
    if not CacheService.is_enabled():
        return [fetch_project(pid) for pid in project_ids]

    pipe = CacheService.get_client().pipeline()
    keys = [CacheKeys.project_info(pid) for pid in project_ids]

    for key in keys:
        pipe.get(key)

    results = pipe.execute()
    # ... 处理结果
```

### 内存优化

- 限制排行榜缓存数量(最多100条)
- 话题列表只缓存最新20条
- 定期清理过期键(Redis自动处理)

## 安全考虑

1. **敏感数据**: 不缓存用户Token等敏感信息
2. **访问控制**: Redis配置密码(生产环境)
3. **数据隔离**: 使用key_prefix实现多实例隔离
