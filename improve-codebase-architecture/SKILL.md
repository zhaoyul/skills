---
name: improve-codebase-architecture
description: 在代码库中寻找深化机会，参考 CONTEXT.md 中的领域语言和 docs/adr/ 中的决策。当用户想要改进架构、寻找重构机会、整合紧密耦合的模块或使代码库更可测试和 AI 可导航时使用。
---

# 改进代码库架构

浮出架构摩擦并提出**深化机会**——将浅层模块转变为深度模块的重构。目标是可测试性和 AI 可导航性。

## 术语表

在每个建议中准确使用这些术语。一致的语言是重点——不要漂移到 "component"、"service"、"API" 或 "boundary"。完整定义在 [LANGUAGE.md](LANGUAGE.md) 中。

- **Module** — 任何具有接口和实现的东西（函数、类、包、切片）。
- **Interface** — 调用者使用模块必须知道的一切：类型、不变量、错误模式、顺序、配置。不仅仅是类型签名。
- **Implementation** — 内部的代码。
- **Depth** — 接口处的杠杆：小接口后面有大量行为。**Deep** = 高杠杆。**Shallow** = 接口几乎与实现一样复杂。
- **Seam** — 接口所在的位置；可以改变行为而无需就地编辑的地方。（使用这个，而不是 "boundary"。）
- **Adapter** — 在 seam 处满足接口的具体事物。
- **Leverage** — 调用者从深度获得的东西。
- **Locality** — 维护者从深度获得的东西：更改、bug、知识集中在一个地方。

关键原则（完整列表见 [LANGUAGE.md](LANGUAGE.md)）：

- **删除测试**：想象删除模块。如果复杂性消失，它是一个传递。如果复杂性在 N 个调用者中重新出现，它就在发挥作用。
- **接口是测试表面。**
- **一个 adapter = 假设的 seam。两个 adapters = 真实的 seam。**

此技能受项目领域模型的_影响_——`CONTEXT.md` 和任何 `docs/adr/`。领域语言为好的 seams 命名；ADRs 记录技能不应重新争论的决策。见 [CONTEXT-FORMAT.md](../domain-model/CONTEXT-FORMAT.md) 和 [ADR-FORMAT.md](../domain-model/ADR-FORMAT.md)。

## 流程

### 1. 探索

首先阅读现有文档：

- `CONTEXT.md`（或 `CONTEXT-MAP.md` + 多上下文仓库中的每个 `CONTEXT.md`）
- `docs/adr/` 中的相关 ADRs（以及任何上下文范围的 `docs/adr/` 目录）

如果这些文件不存在，请默默继续——不要标记它们的缺席或建议预先创建它们。

然后使用 Agent 工具（`subagent_type=Explore`）遍历代码库。不要遵循严格的启发式——有机地探索并注意你遇到摩擦的地方：

- 理解一个概念需要在许多小模块之间跳转的地方在哪里？
- 模块**浅层**的地方在哪里——接口几乎与实现一样复杂？
- 纯函数仅为了可测试性而提取的地方在哪里，但真正的 bug 隐藏在它们如何被调用（没有**locality**）？
- 紧密耦合的模块在其 seams 泄漏的地方在哪里？
- 代码库的哪些部分未经测试，或通过其当前接口难以测试？

对你怀疑是浅层的任何东西应用**删除测试**：删除它会集中复杂性，还是只是移动它？"是的，集中"是你想要的信号。

### 2. 呈现候选

呈现深化机会的带编号列表。对于每个候选：

- **文件** — 涉及哪些文件/模块
- **问题** — 为什么当前架构导致摩擦
- **解决方案** — 将发生什么变化的简单英语描述
- **好处** — 用 locality 和 leverage 解释，以及测试如何改进

**对领域使用 CONTEXT.md 词汇，对架构使用 [LANGUAGE.md](LANGUAGE.md) 词汇。** 如果 `CONTEXT.md` 定义了 “Order”，就说 “Order intake module”——而不是 “FooBarHandler”，也不是 “Order service”。

**ADR 冲突**：如果候选与现有 ADR 矛盾，仅当摩擦足够真实以值得重新审视 ADR 时浮出它。清楚标记它（例如 _“与 ADR-0007 冲突——但值得重新开启讨论，因为……”_）。不要列出 ADR 禁止的每个理论重构。

还不要提出接口。询问用户："你想探索其中哪一个？"

### 3. 质询循环

一旦用户选择了候选，进入质询对话。与他们一起遍历设计树——约束、依赖、深化模块的形状、seam 后面是什么、什么测试存活。

副作用在决策具体化时内联发生：

- **根据 `CONTEXT.md` 中没有的概念命名深化模块？** 将术语添加到 `CONTEXT.md`——与 `/domain-model` 相同的纪律（见 [CONTEXT-FORMAT.md](../domain-model/CONTEXT-FORMAT.md)）。如果不存在则懒惰创建文件。
- **在对话期间锐化模糊术语？** 就在那里更新 `CONTEXT.md`。
- **用户以承重原因拒绝候选？** 提供 ADR，框定为：_“要我把这记录成 ADR 吗，这样以后的架构评审就不会再次建议它？”_ 仅在原因实际上需要未来探索者避免重新建议相同事物时提供——跳过短暂的原因（“现在不值得做”）和不言而喻的原因。见 [ADR-FORMAT.md](../domain-model/ADR-FORMAT.md)。
- **想要探索深化模块的替代接口？** 见 [INTERFACE-DESIGN.md](INTERFACE-DESIGN.md)。
