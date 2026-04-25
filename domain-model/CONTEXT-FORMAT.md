# CONTEXT.md 格式

## 结构

```md
# {上下文名称}

{一两句话描述这个上下文是什么以及它为什么存在。}

## 语言

**Order**:
客户购买一个或多个项目的请求。
_避免_：Purchase、transaction

**Invoice**:
交付后发送给客户的付款请求。
_避免_：Bill、payment request

**Customer**:
下订单的个人或组织。
_避免_：Client、buyer、account

## 关系

- 一个 **Order** 产生一个或多个 **Invoices**
- 一个 **Invoice** 恰好属于一个 **Customer**

## 示例对话

> **Dev:** "当 **Customer** 下 **Order** 时，我们立即创建 **Invoice** 吗？"
> **领域专家:** "不——**Invoice** 仅在 **Fulfillment** 确认后生成。"

## 标记的歧义

- "account" 被用来表示 **Customer** 和 **User**——已解决：这些是不同的概念。
```

## 规则

- **要有主见。** 当同一概念存在多个词时，选择最好的一个并列出其他作为要避免的别名。
- **明确标记冲突。** 如果一个术语被歧义使用，在 "标记的歧义" 中用明确的解决方案调用它。
- **保持定义紧凑。** 最多一句话。定义它**是**什么，而不是它做什么。
- **显示关系。** 使用粗体术语名称并在明显的地方表达基数。
- **仅包含特定于此项目上下文的术语。** 通用编程概念（超时、错误类型、实用程序模式）不属于，即使项目广泛使用它们。在添加术语之前，问：这是这个上下文独有的概念，还是通用编程概念？只有前者属于。
- **在自然集群出现时将术语分组在子标题下**。如果所有术语属于单个内聚区域，扁平列表就可以。
- **编写示例对话。** 开发人员和领域专家之间的对话，展示术语如何自然交互并阐明相关概念之间的边界。

## 单上下文 vs 多上下文仓库

**单上下文（大多数仓库）：** 仓库根目录的一个 `CONTEXT.md`。

**多上下文：** 仓库根目录的 `CONTEXT-MAP.md` 列出上下文、它们的位置以及它们如何相互关联：

```md
# 上下文地图

## 上下文

- [Ordering](./src/ordering/CONTEXT.md) — 接收和跟踪客户订单
- [Billing](./src/billing/CONTEXT.md) — 生成发票和处理付款
- [Fulfillment](./src/fulfillment/CONTEXT.md) — 管理仓库拣选和运输

## 关系

- **Ordering → Fulfillment**：Ordering 发出 `OrderPlaced` 事件；Fulfillment 消费它们以开始拣选
- **Fulfillment → Billing**：Fulfillment 发出 `ShipmentDispatched` 事件；Billing 消费它们以生成发票
- **Ordering ↔ Billing**：`CustomerId` 和 `Money` 的共享类型
```

技能推断适用哪种结构：

- 如果 `CONTEXT-MAP.md` 存在，读取它以查找上下文
- 如果仅存在根 `CONTEXT.md`，单上下文
- 如果两者都不存在，在第一个术语解决时懒惰创建根 `CONTEXT.md`

当存在多个上下文时，推断当前主题与哪一个相关。如果不清楚，请询问。
