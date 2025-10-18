# Prompt 文档目录

本目录包含了 ZSXQCheckIn 项目的提示词工程相关文档,包括对话过程记录、提示词分析和模板库。

---

## 📁 文件说明

### 1. conversation.md
**完整对话过程记录**

- **内容**: 用户与 Claude Code 的完整对话过程
- **包含**:
  - 5轮对话的详细记录
  - 每一步的工具使用情况
  - Claude的分析思路和决策过程
  - 对话中的关键决策点
  - 工作方法总结
  - 经验教训
- **适合**: 了解如何与 Claude Code 协作,学习提示词工程实践
- **字数**: 约1100行

### 2. init-prompt.md
**/init 命令的结构化分析**

- **内容**: 对 `/init` 命令提示词的深度分析
- **包含**:
  - 完整的提示词内容
  - 提示词结构分解
  - 设计原则解析
  - 执行流程说明
  - 输出质量标准
  - 最佳实践示例
- **适合**: 理解如何使用 `/init` 命令,掌握项目初始化的最佳实践
- **字数**: 约500行

### 3. prompt-templates.md
**结构化提示词模板库**

- **内容**: 10大类通用提示词模板
- **包含**:
  1. 代码库分析提示词
  2. 文档生成提示词
  3. 代码规范提示词
  4. 项目初始化提示词
  5. 配置管理提示词
  6. 错误处理提示词
  7. 测试相关提示词
  8. 部署相关提示词
  9. 监控和日志提示词
  10. 文档维护提示词
- **适合**: 快速查找和复用提示词模板,提高工作效率
- **字数**: 约800行

### 4. README.md (本文件)
**Prompt 目录使用说明**

- **内容**: 目录结构说明和使用指南
- **适合**: 快速了解本目录的内容和使用方法

---

## 🎯 使用场景

### 场景1: 学习 Claude Code 的使用
**推荐阅读顺序**:
1. `conversation.md` - 了解完整的对话流程
2. `init-prompt.md` - 理解 `/init` 命令的工作原理
3. `prompt-templates.md` - 学习各类提示词模板

**收获**:
- 掌握与 Claude Code 的协作方式
- 了解如何有效使用命令和工具
- 学习提示词工程的最佳实践

---

### 场景2: 初始化新项目
**推荐使用**:
1. 执行 `/init` 命令生成 CLAUDE.md
2. 参考 `init-prompt.md` 了解生成逻辑
3. 使用 `prompt-templates.md` 中的"项目初始化"模板

**输出**:
- CLAUDE.md 文件
- 项目结构
- 开发环境配置

---

### 场景3: 编写项目文档
**推荐使用**:
1. `prompt-templates.md` 第2节 - 文档生成提示词
2. `conversation.md` 中的文档编写经验
3. `init-prompt.md` 中的文档质量标准

**可生成**:
- 架构文档
- API文档
- 开发指南
- 部署文档

---

### 场景4: 制定开发规范
**推荐使用**:
1. `prompt-templates.md` 第3节 - 代码规范提示词
2. `init-prompt.md` 中的开发约定部分

**可生成**:
- 代码风格规范
- Git提交规范
- 分支策略
- Code Review清单

---

### 场景5: 配置项目环境
**推荐使用**:
1. `prompt-templates.md` 第5节 - 配置管理提示词
2. `prompt-templates.md` 第8节 - 部署相关提示词

**可生成**:
- 配置文件结构
- Docker配置
- Nginx配置
- 环境变量定义

---

## 🔍 快速查找

### 按关键词查找

| 关键词 | 文件 | 章节 |
|--------|------|------|
| `/init` 命令 | init-prompt.md | 全文 |
| 对话过程 | conversation.md | 对话流程 |
| 项目初始化 | prompt-templates.md | 第4节 |
| 代码规范 | prompt-templates.md | 第3节 |
| API文档 | prompt-templates.md | 第2.2节 |
| Docker部署 | prompt-templates.md | 第8.1节 |
| 错误处理 | prompt-templates.md | 第6节 |
| 测试策略 | prompt-templates.md | 第7节 |
| 日志规范 | prompt-templates.md | 第9.1节 |
| 监控指标 | prompt-templates.md | 第9.2节 |

---

### 按文件类型查找

| 需要生成的文件 | 推荐模板 |
|--------------|---------|
| CLAUDE.md | init-prompt.md |
| README.md | prompt-templates.md 第2.1节 |
| API文档 | prompt-templates.md 第2.2节 |
| Dockerfile | prompt-templates.md 第8.1节 |
| docker-compose.yml | prompt-templates.md 第8.1节 |
| nginx.conf | prompt-templates.md 第8.2节 |
| .gitignore | prompt-templates.md 第5.1节 |
| config.yml | prompt-templates.md 第5.1节 |
| pytest测试 | prompt-templates.md 第7.2节 |

---

## 💡 最佳实践

### 1. 提示词编写原则
基于对话过程总结的原则:

✅ **DO - 应该做的**:
- 明确目标和预期输出
- 提供足够的上下文信息
- 使用结构化的格式
- 包含具体的示例
- 定义质量标准
- 基于事实而非猜测

❌ **DON'T - 不应该做的**:
- 模糊不清的指令
- 缺少上下文的要求
- 编造不存在的信息
- 重复显而易见的内容
- 忽视项目实际情况

---

### 2. 工具使用技巧

**代码库探索**:
```
1. Glob - 搜索文件
2. Read - 读取内容
3. Bash - 执行命令
4. 并行执行独立操作
```

**文档生成**:
```
1. 先探索后生成
2. 基于实际内容
3. 结构化输出
4. 验证准确性
```

**任务管理**:
```
1. 使用 TodoWrite 跟踪进度
2. 及时标记完成状态
3. 分解复杂任务
```

---

### 3. 对话协作技巧

**明确性**:
- 清晰表达需求
- 提供具体细节
- 确认理解一致

**渐进式**:
- 从概览到细节
- 逐步完善输出
- 迭代优化结果

**验证性**:
- 检查输出正确性
- 测试生成的命令
- 确认符合预期

---

## 📚 扩展阅读

### 相关文档
- `../CLAUDE.md` - 本项目的 Claude Code 指南
- `../doc/需求分析文档.md` - 详细需求文档
- `../README.md` - 项目说明

### 外部资源
- [Claude Code 官方文档](https://docs.claude.com/en/docs/claude-code)
- [提示词工程指南](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [最佳实践](https://docs.anthropic.com/claude/docs/best-practices)

---

## 🤝 贡献

### 如何完善这些文档

**发现新的提示词模式**:
1. 记录使用场景
2. 整理提示词内容
3. 添加到 `prompt-templates.md`

**优化现有模板**:
1. 识别改进点
2. 测试新版本
3. 更新文档

**分享经验**:
1. 记录成功案例
2. 总结失败教训
3. 更新最佳实践

---

## 📝 更新日志

### 2025-10-19
- ✅ 创建 prompt/ 目录
- ✅ 添加 conversation.md (完整对话记录)
- ✅ 添加 init-prompt.md (/init 命令分析)
- ✅ 添加 prompt-templates.md (提示词模板库)
- ✅ 添加 README.md (使用说明)

---

## 📞 联系方式

如有问题或建议,请联系:
- **微信**: 20133213
- **项目**: ZSXQCheckIn

---

**最后更新**: 2025-10-19
**维护者**: ZSXQCheckIn Team
