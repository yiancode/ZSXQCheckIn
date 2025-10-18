# 知识星球打卡API接口文档

**文档版本**: v1.0
**创建日期**: 2025-10-19
**数据来源**: Charles抓包知识星球APP

---

## 目录
1. [基础信息](#基础信息)
2. [打卡项目接口](#打卡项目接口)
3. [数据结构](#数据结构)
4. [业务逻辑分析](#业务逻辑分析)

---

## 基础信息

### 接口域名
```
https://api.zsxq.com
```

### 请求头(Headers)
```
Host: api.zsxq.com
Content-Type: application/json; charset=utf-8
Accept: */*
Authorization: {token}  # 关键认证信息
X-Timestamp: {timestamp}
X-Signature: {signature}  # 签名验证
X-Version: 2.82.0
Accept-Language: zh-Hans-US;q=1
User-Agent: xiaomiquan/5.28.1 iOS/phone/26.0.1 iPhone Mobile
```

**关键参数说明**:
- `Authorization`: 用户认证Token (格式: `{UUID}_{HASH}`)
- `X-Signature`: 请求签名,用于防篡改验证
- `X-Timestamp`: 请求时间戳

---

## 打卡项目接口

### 1. 获取打卡项目列表

**接口地址**:
```
GET /v2/groups/{group_id}/checkins
```

**路径参数**:
- `group_id`: 星球ID (示例: `15555411412112`)

**查询参数**:
| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| scope | string | 是 | 项目状态过滤 | `closed`/`over`/`ongoing` |
| count | integer | 否 | 返回数量 | `30` (默认30,最大100) |

**scope参数说明**:
- `ongoing`: 进行中的项目
- `closed`: 已关闭的项目(显示为"进行中",但不再接受新成员)
- `over`: 已结束的项目

**请求示例**:
```bash
# 获取进行中的项目
curl "https://api.zsxq.com/v2/groups/15555411412112/checkins?scope=ongoing&count=100" \
  -H "Authorization: YOUR_TOKEN"

# 获取已结束的项目
curl "https://api.zsxq.com/v2/groups/15555411412112/checkins?scope=over&count=30" \
  -H "Authorization: YOUR_TOKEN"
```

**响应示例**:
```json
{
  "succeeded": true,
  "resp_data": {
    "checkins": [
      {
        "checkin_id": 8424481182,
        "group": {
          "group_id": 15555411412112,
          "name": "AI私域赚钱",
          "background_url": "https://..."
        },
        "owner": {
          "user_id": 582884445452854,
          "name": "深圳大冲",
          "avatar_url": "https://...",
          "description": "..."
        },
        "title": "2510 AI写作(软件文档)",
        "text": "1、#AI私域赚钱星球打卡后...",
        "checkin_days": 9,
        "validity": {
          "long_period": false,
          "expiration_time": "2025-10-26T23:59:59.999+0800"
        },
        "show_topics_on_timeline": false,
        "create_time": "2025-10-17T19:43:42.339+0800",
        "status": "ongoing",
        "type": "accumulated",
        "joined_count": 83,
        "statistics": {
          "joined_count": 83,
          "completed_count": 0,
          "today_checkined_count": 0
        },
        "joined_users": [...],
        "user_specific": {
          "joined": false
        },
        "min_words_count": 30
      }
    ]
  }
}
```

---

## 数据结构

### CheckinProject (打卡项目)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| checkin_id | long | 打卡项目ID | `8424481182` |
| group | Group | 所属星球信息 | 见Group结构 |
| owner | User | 项目发起人 | 见User结构 |
| title | string | 项目标题 | "2510 AI写作(软件文档)" |
| text | string | 项目规则说明 | "1、#AI私域赚钱星球..." |
| checkin_days | integer | 打卡天数要求 | `9` |
| validity | Validity | 有效期 | 见Validity结构 |
| show_topics_on_timeline | boolean | 是否在时间线显示话题 | `false` |
| create_time | datetime | 创建时间 | "2025-10-17T19:43:42.339+0800" |
| status | string | 项目状态 | `ongoing`/`closed`/`over` |
| type | string | 打卡类型 | `accumulated`/`continuous` |
| joined_count | integer | 参与人数 | `83` |
| statistics | Statistics | 统计数据 | 见Statistics结构 |
| joined_users | User[] | 参与用户列表(最多5个头像) | [...] |
| user_specific | UserSpecific | 当前用户相关信息 | 见UserSpecific结构 |
| min_words_count | integer | 最少字数要求 | `30` |

### Group (星球信息)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| group_id | long | 星球ID | `15555411412112` |
| name | string | 星球名称 | "AI私域赚钱" |
| background_url | string | 背景图URL | "https://..." |

### User (用户信息)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| user_id | long | 用户ID | `582884445452854` |
| name | string | 用户昵称 | "深圳大冲" |
| alias | string | 用户别名(可选) | "深圳大冲" |
| avatar_url | string | 头像URL | "https://..." |
| description | string | 用户简介(可选) | "AI私域赚钱星球主理人..." |

### Validity (有效期)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| long_period | boolean | 是否长期有效 | `false` |
| expiration_time | datetime | 过期时间(如果不是长期) | "2025-10-26T23:59:59.999+0800" |

### Statistics (统计信息)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| joined_count | integer | 参与人数 | `83` |
| completed_count | integer | 完成人数 | `0` |
| today_checkined_count | integer | 今日打卡人数 | `0` |

### UserSpecific (用户特定信息)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| joined | boolean | 当前用户是否已加入 | `false` |

---

## 业务逻辑分析

### 项目状态(status)说明

1. **ongoing** (进行中)
   - 项目正在进行
   - 接受新成员加入
   - 可以打卡
   - 未到截止日期

2. **closed** (已关闭)
   - 项目已关闭新成员加入
   - 已加入的成员可以继续打卡
   - 未到截止日期
   - APP中显示为"进行中"(但不能新加入)

3. **over** (已结束)
   - 项目已到截止日期
   - 不再接受打卡
   - 可以查看统计数据
   - APP中显示为"已结束"

### 打卡类型(type)说明

1. **accumulated** (累计打卡)
   - 统计累计打卡次数
   - 不要求连续
   - 完成指定次数即可
   - 示例: "完成10次打卡"

2. **continuous** (连续打卡)
   - 要求连续打卡
   - 中断后重新计算
   - 完成连续N天即可
   - 示例: "连续打卡21天"

### 排行榜逻辑推断

**连续打卡排行榜**:
- 排序依据: 连续打卡天数(降序)
- 数据来源: `type=continuous` 的项目
- 统计字段: 用户的连续天数

**累计打卡排行榜**:
- 排序依据: 累计打卡次数(降序)
- 数据来源: `type=accumulated` 的项目
- 统计字段: 用户的累计次数

### 2. 获取打卡项目详情

**接口地址**:
```
GET /v2/groups/{group_id}/checkins/{checkin_id}
```

**路径参数**:
- `group_id`: 星球ID
- `checkin_id`: 打卡项目ID

**请求示例**:
```bash
curl "https://api.zsxq.com/v2/groups/15555411412112/checkins/8424481182" \
  -H "Authorization: YOUR_TOKEN"
```

**响应示例**:
```json
{
  "succeeded": true,
  "resp_data": {
    "is_valid_member": true,
    "checkin": {
      "checkin_id": 8424481182,
      "title": "2510 AI写作(软件文档)",
      "text": "1、#AI私域赚钱星球打卡后...",
      "checkin_days": 9,
      "status": "ongoing",
      "type": "accumulated",
      "joined_count": 83,
      "statistics": {
        "joined_count": 83,
        "completed_count": 0,
        "today_checkined_count": 0
      },
      "min_words_count": 30,
      ...
    },
    "group": {
      "name": "AI私域赚钱"
    }
  }
}
```

---

### 3. 获取打卡项目统计(含排行榜预览)

**接口地址**:
```
GET /v2/groups/{group_id}/checkins/{checkin_id}/statistics
```

**路径参数**:
- `group_id`: 星球ID
- `checkin_id`: 打卡项目ID

**请求示例**:
```bash
curl "https://api.zsxq.com/v2/groups/15555411412112/checkins/8424481182/statistics" \
  -H "Authorization: YOUR_TOKEN"
```

**响应示例**:
```json
{
  "succeeded": true,
  "resp_data": {
    "statistics": {
      "joined_count": 83,
      "completed_count": 0,
      "checkined_count": 129,
      "ranking_list": [
        {
          "avatar_url": "https://images.zsxq.com/..."
        },
        {
          "avatar_url": "https://images.zsxq.com/..."
        }
        // 最多返回前6名用户头像
      ]
    }
  }
}
```

**字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| joined_count | integer | 参与人数 |
| completed_count | integer | 完成人数 |
| checkined_count | integer | 总打卡次数 |
| ranking_list | array | 排行榜前6名用户头像列表 |

**⚠️ 重要**: 此接口的ranking_list只返回用户头像,不包含用户名、打卡次数、排名等详细信息

---

### 4. 获取每日打卡统计

**接口地址**:
```
GET /v2/groups/{group_id}/checkins/{checkin_id}/statistics/daily
```

**路径参数**:
- `group_id`: 星球ID
- `checkin_id`: 打卡项目ID

**查询参数**:
| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| date | datetime | 是 | 查询日期(URL编码) | `2025-10-19T04:58:12.889+0800` |

**请求示例**:
```bash
curl "https://api.zsxq.com/v2/groups/15555411412112/checkins/8424481182/statistics/daily?date=2025-10-19T04%3A58%3A12.889%2B0800" \
  -H "Authorization: YOUR_TOKEN"
```

**响应示例**:
```json
{
  "succeeded": true,
  "resp_data": {
    "checkined_count": 0
  }
}
```

**字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| checkined_count | integer | 指定日期的打卡人数 |

---

### 5. 获取打卡相关话题

**接口地址**:
```
GET /v2/groups/{group_id}/checkins/{checkin_id}/topics
```

**路径参数**:
- `group_id`: 星球ID
- `checkin_id`: 打卡项目ID

**查询参数**:
| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| count | integer | 否 | 返回数量 | `20` |

**请求示例**:
```bash
curl "https://api.zsxq.com/v2/groups/15555411412112/checkins/8424481182/topics?count=20" \
  -H "Authorization: YOUR_TOKEN"
```

**响应示例**:
```json
{
  "succeeded": true,
  "resp_data": {
    "topics": [
      {
        "topic_id": 14588242284258122,
        "type": "talk",
        "talk": {
          "owner": {
            "user_id": 818882241118112,
            "name": "热心市民老黄",
            "avatar_url": "https://...",
            "location": "广东"
          },
          "text": "今天听了星狩老师的直播分享..."
        },
        "likes_count": 1,
        "comments_count": 1,
        "reading_count": 1,
        "create_time": "2025-10-18T23:59:28.117+0800",
        "checkin": {
          "title": "2510 AI写作(软件文档)",
          "checkin_id": 8424481182,
          "min_words_count": 30
        }
      }
    ]
  }
}
```

**用途**: 获取用户打卡后发布的内容/讨论,用于展示打卡记录列表

---

### 6. 获取排行榜 ✅ **核心接口**

**接口地址**:
```
GET /v2/groups/{group_id}/checkins/{checkin_id}/ranking_list
```

**路径参数**:
- `group_id`: 星球ID
- `checkin_id`: 打卡项目ID

**查询参数**:
| 参数 | 类型 | 必填 | 说明 | 可选值 |
|------|------|------|------|--------|
| type | string | 是 | 排行榜类型 | `continuous`(连续打卡) / `accumulated`(累计打卡) |
| index | integer | 否 | 分页索引 | 默认`0`,支持分页 |

**请求示例**:
```bash
# 连续打卡排行榜
curl "https://api.zsxq.com/v2/groups/15555411412112/checkins/1141152412/ranking_list?type=continuous&index=0" \
  -H "Authorization: YOUR_TOKEN"

# 累计打卡排行榜
curl "https://api.zsxq.com/v2/groups/15555411412112/checkins/1141152412/ranking_list?type=accumulated&index=0" \
  -H "Authorization: YOUR_TOKEN"
```

**响应示例**:
```json
{
  "succeeded": true,
  "resp_data": {
    "ranking_list": [
      {
        "user": {
          "user_id": 585221282158424,
          "name": "伊雪儿",
          "alias": "",
          "avatar_url": "https://images.zsxq.com/..."
        },
        "rankings": 1,
        "checkined_days": 10
      },
      {
        "user": {
          "user_id": 814545421115142,
          "name": "林研",
          "alias": "",
          "avatar_url": "https://images.zsxq.com/..."
        },
        "rankings": 2,
        "checkined_days": 10
      }
      // ... 更多用户
    ],
    "user_specific": {
      "user": {
        "user_id": 184444848828412,
        "name": "易安",
        "alias": "",
        "avatar_url": "https://images.zsxq.com/..."
      },
      "rankings": 0,
      "checkined_days": 0
    }
  }
}
```

**字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| ranking_list | array | 排行榜列表 |
| ranking_list[].user | object | 用户信息 |
| ranking_list[].rankings | integer | 排名(1开始) |
| ranking_list[].checkined_days | integer | 打卡天数(continuous:连续天数, accumulated:累计次数) |
| user_specific | object | 当前登录用户的排名信息 |

**⚠️ 重要说明**:
1. **checkined_days字段含义**:
   - `type=continuous`: 表示**连续打卡天数**
   - `type=accumulated`: 表示**累计打卡次数**
2. **分页机制**:
   - `index=0`: 第一页
   - 每页返回约20-30条数据
   - 可通过增加index获取更多数据
3. **当前用户信息**:
   - `user_specific` 包含当前登录用户的排名
   - 如果用户未参与,`rankings`为0

---

### 需要额外接口(待抓包) ⚠️

根据业务需求,还可能需要:

1. **用户打卡详细记录** 🟡 **低优先级**
   - 功能: 获取单个用户的所有打卡时间记录
   - 预期接口: `GET /v2/groups/{group_id}/checkins/{checkin_id}/users/{user_id}/records`
   - **备注**: 可通过topics接口获取打卡内容,此接口优先级较低

---

## API接口完成度

### ✅ 已完成接口 (6个核心接口)

| # | 接口名称 | 路径 | 完成度 | 备注 |
|---|---------|------|--------|------|
| 1 | 获取项目列表 | `GET /checkins?scope={scope}` | ✅ 100% | 支持3种状态过滤 |
| 2 | 获取项目详情 | `GET /checkins/{id}` | ✅ 100% | 包含完整项目信息 |
| 3 | 获取项目统计 | `GET /checkins/{id}/statistics` | ✅ 100% | 包含前6名头像 |
| 4 | 获取每日统计 | `GET /checkins/{id}/statistics/daily` | ✅ 100% | 按日期查询 |
| 5 | 获取打卡话题 | `GET /checkins/{id}/topics` | ✅ 100% | 打卡内容列表 |
| 6 | **获取排行榜** | `GET /checkins/{id}/ranking_list` | ✅ 100% | **核心接口** |

### 📊 接口覆盖率

- **核心功能**: 100% ✅ (项目列表、详情、排行榜全部完成)
- **统计功能**: 100% ✅ (项目统计、每日统计完成)
- **内容展示**: 100% ✅ (打卡话题/记录完成)

### 🎯 可实现的功能

基于已有接口,可以完整实现:

1. ✅ **项目列表页**
   - 显示所有打卡项目(进行中/已结束/已关闭)
   - 项目基本信息(标题、天数、参与人数)
   - 快速排行榜预览(前6名头像)

2. ✅ **项目详情页**
   - 项目完整信息
   - 统计卡片(参与人数、完成人数、总打卡次数)
   - 每日打卡统计

3. ✅ **排行榜页面** (核心功能)
   - 连续打卡排行榜(完整列表+分页)
   - 累计打卡排行榜(完整列表+分页)
   - 用户排名、打卡天数、头像、昵称
   - 当前用户排名高亮

4. ✅ **打卡记录流**
   - 用户打卡内容展示
   - 打卡时间、点赞数、评论数

### 待办事项

- [x] ~~抓取项目列表接口~~ ✅
- [x] ~~抓取项目详情接口~~ ✅
- [x] ~~抓取排行榜接口~~ ✅ **完成!**
- [x] ~~抓取统计接口~~ ✅
- [x] ~~抓取打卡内容接口~~ ✅
- [ ] 设计后端API接口 (下一步)
- [ ] 设计Redis缓存结构 (下一步)
- [ ] 实现Flask后端 (下一步)
- [ ] 实现React前端 (下一步)
- [ ] 验证Token有效期和刷新机制 (可选)
- [ ] 测试签名(X-Signature)生成算法 (可选)

---

## 附录

### 示例数据摘录

**进行中项目示例**:
```json
{
  "checkin_id": 8424481182,
  "title": "2510 AI写作(软件文档)",
  "checkin_days": 9,
  "status": "ongoing",
  "type": "accumulated",
  "joined_count": 83,
  "statistics": {
    "joined_count": 83,
    "completed_count": 0,
    "today_checkined_count": 0
  }
}
```

**已结束项目示例**:
```json
{
  "checkin_id": 8424485212,
  "title": "2510 AI编程",
  "checkin_days": 9,
  "status": "over",
  "type": "accumulated",
  "joined_count": 75,
  "statistics": {
    "joined_count": 75,
    "completed_count": 8,
    "today_checkined_count": 0
  }
}
```

### 星球信息

- **星球ID**: `15555411412112`
- **星球名称**: AI私域赚钱
- **抓包时间**: 2025-10-19

---

**文档更新日志**:
- 2025-10-19: v1.0 初始版本,记录打卡项目列表接口
