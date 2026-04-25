# 好的测试和坏的测试

## 好的测试

**集成风格**：通过真实接口测试，而不是内部部分的模拟。

```typescript
// 好：测试可观察的行为
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

特点：

- 测试用户/调用者关心的行为
- 仅使用公共 API
- 在内部重构后存活
- 描述做什么，而不是如何做
- 每个测试一个逻辑断言

## 坏的测试

**实现细节测试**：耦合到内部结构。

```typescript
// 坏：测试实现细节
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

危险信号：

- 模拟内部协作者
- 测试私有方法
- 断言调用计数/顺序
- 在没有行为改变的重构时测试中断
- 测试名称描述如何做而不是做什么
- 通过外部方式而不是接口进行验证

```typescript
// 坏：绕过接口进行验证
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// 好：通过接口验证
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```
