---
name: to-issues
description: 使用追踪弹式垂直切片将计划、规格或 PRD 分解为可独立认领的 GitHub issues。当用户想要将计划转换为 issues、创建实现工单或将工作分解为 issues 时使用。
---

# 转为 Issues

使用垂直切片（追踪弹）将计划分解为可独立认领的 GitHub issues。

## 流程

### 1. 收集上下文

使用对话上下文中已有的任何内容。如果用户传递 GitHub issue 编号或 URL 作为参数，使用 `gh issue view <number>`（带评论）获取它。

### 2. 探索代码库（可选）

如果尚未探索代码库，请探索以了解代码的当前状态。

### 3. 起草垂直切片

将计划分解为**追踪弹** issues。每个 issue 都是一个薄的垂直切片，端到端地贯穿所有集成层，而不是一个层的水平切片。

切片可能是 'HITL' 或 'AFK'。HITL 切片需要人工交互，例如架构决策或设计审查。AFK 切片可以在无人工交互的情况下实现和合并。在可能的情况下优先选择 AFK 而非 HITL。

<vertical-slice-rules>
- 每个切片通过每个层（schema、API、UI、tests）提供一条狭窄但完整的路径
- 完成的切片本身是可演示或可验证的
- 优先选择多个薄切片而非少数厚切片
</vertical-slice-rules>

### 4. 询问用户

将提议的分解作为带编号的列表呈现。对于每个切片，显示：

- **标题**：简短描述性名称
- **类型**：HITL / AFK
- **阻塞者**：哪些其他切片（如果有）必须首先完成
- **涵盖的用户故事**：这解决了哪些用户故事（如果源材料有的话）

询问用户：

- 粒度是否合适？（太粗/太细）
- 依赖关系是否正确？
- 是否应该合并或进一步拆分任何切片？
- 正确的切片是否标记为 HITL 和 AFK？

迭代直到用户批准分解。

### 5. 创建 GitHub issues

对于每个已批准的切片，使用 `gh issue create` 创建 GitHub issue。使用下面的 issue 正文模板。

按依赖顺序创建 issues（阻塞者优先），以便你可以在 "Blocked by" 字段中引用真实的 issue 编号。

<issue-template>
## 父 issue

#<parent-issue-number>（如果源是 GitHub issue，否则省略此部分）

## 要构建的内容

此垂直切片的简明描述。描述端到端行为，而非逐层实现。

## 验收标准

- [ ] 标准 1
- [ ] 标准 2
- [ ] 标准 3

## 阻塞于

- Blocked by #<issue-number>（如果有）

或“无——可以立即开始”，如果没有阻塞者。

</issue-template>

不要关闭或修改任何父 issue。
