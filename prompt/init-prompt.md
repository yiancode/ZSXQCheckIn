# /init 命令的结构化提示词

## 提示词完整内容

```
Please analyze this codebase and create a CLAUDE.md file, which will be given to future instances of Claude Code to operate in this repository.

What to add:
1. Commands that will be commonly used, such as how to build, lint, and run tests. Include the necessary commands to develop in this codebase, such as how to run a single test.
2. High-level code architecture and structure so that future instances can be productive more quickly. Focus on the "big picture" architecture that requires reading multiple files to understand.

Usage notes:
- If there's already a CLAUDE.md, suggest improvements to it.
- When you make the initial CLAUDE.md, do not repeat yourself and do not include obvious instructions like "Provide helpful error messages to users", "Write unit tests for all new utilities", "Never include sensitive information (API keys, tokens) in code or commits".
- Avoid listing every component or file structure that can be easily discovered.
- Don't include generic development practices.
- If there are Cursor rules (in .cursor/rules/ or .cursorrules) or Copilot rules (in .github/copilot-instructions.md), make sure to include the important parts.
- If there is a README.md, make sure to include the important parts.
- Do not make up information such as "Common Development Tasks", "Tips for Development", "Support and Documentation" unless this is expressly included in other files that you read.
- Be sure to prefix the file with the following text:

```
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```
```

---

## 提示词结构分析

### 1. 核心目标
**创建 CLAUDE.md 文件**,为未来的 Claude Code 实例提供代码库操作指南

### 2. 必须包含的内容

#### A. 常用命令
- 构建命令
- 代码检查(lint)命令
- 测试命令
- 运行单个测试的方法
- 其他开发必需的命令

#### B. 高层架构
- 项目的"大局观"架构
- 需要阅读多个文件才能理解的架构设计
- 聚焦整体结构而非细节

### 3. 使用注意事项

#### 如果已存在 CLAUDE.md
- 提出改进建议而非重写

#### 创建新 CLAUDE.md 时的限制
**不要包含**:
- 显而易见的指令(如"提供有用的错误信息")
- 通用的开发实践(如"为工具编写单元测试")
- 安全常识(如"不要提交API密钥")
- 容易发现的文件结构列表
- 通用开发实践

**不要编造**:
- 常见开发任务
- 开发技巧
- 支持和文档
- 除非这些内容明确存在于已读取的文件中

#### 必须整合的内容
如果存在以下文件,需要包含其重要部分:
- `.cursor/rules/` 或 `.cursorrules` (Cursor规则)
- `.github/copilot-instructions.md` (Copilot规则)
- `README.md` (项目说明)

#### 必须的文件前缀
```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```

---

## 提示词设计原则

### 1. 实用主义
- 聚焦实际开发中最常用的命令
- 提供可操作的指导

### 2. 避免冗余
- 不重复显而易见的内容
- 不包含容易通过工具发现的信息

### 3. 真实性
- 基于实际文件内容
- 不编造不存在的信息

### 4. 架构优先
- 重点在"大局观"
- 帮助快速理解整体设计

### 5. 未来导向
- 为未来的 Claude Code 实例服务
- 提高后续开发效率

---

## 提示词执行流程

### 第一步:探索代码库
1. 搜索各类文件(代码、配置、文档)
2. 识别项目类型和技术栈
3. 查找已有的配置和规则文件

### 第二步:读取关键文档
1. README.md
2. 需求/设计文档
3. Cursor/Copilot 规则
4. 已存在的 CLAUDE.md

### 第三步:分析项目特征
1. 识别技术栈
2. 理解架构设计
3. 提取开发流程
4. 识别常用命令

### 第四步:生成 CLAUDE.md
1. 添加必需的文件头
2. 编写项目概述
3. 记录技术栈和架构
4. 整理常用命令
5. 说明开发规范
6. 标注重要约束

### 第五步:验证和优化
1. 确保没有编造内容
2. 检查是否包含所有必需部分
3. 验证实用性和可操作性

---

## 适用场景

### 适合使用 /init 的情况
1. 新项目初始化
2. 接手已有项目
3. 项目架构重大变更
4. 需要为团队成员提供指导
5. 准备开源项目

### 不适合使用 /init 的情况
1. 项目已有完善的 CLAUDE.md
2. 只是小的代码修改
3. 临时性的实验项目

---

## 输出质量标准

### 优秀的 CLAUDE.md 应该具备

#### 1. 完整性
- [ ] 包含项目概述
- [ ] 包含技术栈说明
- [ ] 包含架构设计
- [ ] 包含常用命令
- [ ] 包含开发规范
- [ ] 包含重要约束

#### 2. 准确性
- [ ] 基于实际文件内容
- [ ] 没有编造信息
- [ ] 命令可以实际执行
- [ ] 架构描述准确

#### 3. 实用性
- [ ] 聚焦高频操作
- [ ] 提供可操作指导
- [ ] 帮助快速上手
- [ ] 避免冗余信息

#### 4. 清晰性
- [ ] 结构清晰
- [ ] 分类合理
- [ ] 易于查阅
- [ ] 重点突出

---

## 常见模式和最佳实践

### 项目概述部分
```markdown
## 项目概述
- 项目类型(Web应用、CLI工具、库等)
- 核心功能
- 技术栈
- 当前状态
```

### 架构说明部分
```markdown
## 系统架构
- 架构图或文字描述
- 关键设计决策
- 模块划分
- 数据流向
```

### 命令部分
```markdown
## 常用命令

### 开发
\`\`\`bash
npm run dev
\`\`\`

### 测试
\`\`\`bash
npm test
npm test -- path/to/test.js
\`\`\`

### 构建
\`\`\`bash
npm run build
\`\`\`
```

### 规范部分
```markdown
## 开发规范
- 代码风格
- Git提交规范
- 分支策略
- 测试要求
```

---

## 与用户自定义指令的关系

### 集成点
本提示词会自动查找并集成:
1. **Cursor规则**: `.cursor/rules/` 或 `.cursorrules`
2. **Copilot规则**: `.github/copilot-instructions.md`
3. **用户全局配置**: `~/.claude/CLAUDE.md`

### 优先级
```
项目特定的 CLAUDE.md
> Cursor/Copilot规则
> 用户全局配置
> 默认行为
```

---

## 示例:不同类型项目的 CLAUDE.md

### Web应用项目
- 前后端技术栈
- API接口规范
- 数据库设计
- 部署流程

### CLI工具项目
- 命令行参数
- 配置文件格式
- 发布流程
- 测试方法

### 库/SDK项目
- API设计
- 版本管理
- 发布流程
- 文档生成

### 全栈项目
- 前后端架构
- 数据流向
- 状态管理
- 构建流程

---

## 提示词的局限性

### 无法处理的场景
1. 代码库过于庞大(文件数万个)
2. 架构过于复杂(需要专家知识)
3. 缺少文档(无法理解设计意图)

### 需要人工补充的部分
1. 业务领域知识
2. 团队特定约定
3. 隐性知识
4. 历史遗留问题的说明

---

## 持续优化建议

### CLAUDE.md 应该随项目演进
1. 架构变更时更新
2. 新增重要功能时更新
3. 开发流程变化时更新
4. 发现常见问题时补充

### 定期审查
- 每个大版本发布后审查
- 新成员加入后收集反馈
- 季度性回顾更新

---

## 参考资源

- Claude Code 官方文档: https://docs.claude.com/en/docs/claude-code
- CLAUDE.md 最佳实践: (项目内部文档)
- 示例项目: (待补充)
