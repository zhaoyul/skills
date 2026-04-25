---
name: setup-pre-commit
description: 在当前仓库中使用 lint-staged（Prettier）、类型检查和测试设置 Husky pre-commit hooks。当用户想要添加 pre-commit hooks、设置 Husky、配置 lint-staged 或添加提交时格式化/类型检查/测试时使用。
---

# 设置 Pre-Commit Hooks

## 这将设置什么

- **Husky** pre-commit hook
- 在所有暂存文件上运行 **lint-staged** 和 Prettier
- **Prettier** 配置（如果缺失）
- pre-commit hook 中的 **typecheck** 和 **test** 脚本

## 步骤

### 1. 检测包管理器

检查 `package-lock.json`（npm）、`pnpm-lock.yaml`（pnpm）、`yarn.lock`（yarn）、`bun.lockb`（bun）。使用存在的任何一个。如果不清楚，默认使用 npm。

### 2. 安装依赖

作为 devDependencies 安装：

```
husky lint-staged prettier
```

### 3. 初始化 Husky

```bash
npx husky init
```

这会创建 `.husky/` 目录并将 `prepare: "husky"` 添加到 package.json。

### 4. 创建 `.husky/pre-commit`

编写此文件（Husky v9+ 不需要 shebang）：

```
npx lint-staged
npm run typecheck
npm run test
```

**适配**：将 `npm` 替换为检测到的包管理器。如果仓库在 package.json 中没有 `typecheck` 或 `test` 脚本，省略这些行并告知用户。

### 5. 创建 `.lintstagedrc`

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

### 6. 创建 `.prettierrc`（如果缺失）

仅在没有 Prettier 配置存在时创建。使用这些默认值：

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

### 7. 验证

- [ ] `.husky/pre-commit` 存在且可执行
- [ ] `.lintstagedrc` 存在
- [ ] package.json 中的 `prepare` 脚本是 `"husky"`
- [ ] `prettier` 配置存在
- [ ] 运行 `npx lint-staged` 以验证其工作

### 8. 提交

暂存所有更改/创建的文件并使用消息提交：`Add pre-commit hooks (husky + lint-staged + prettier)`

这将通过新的 pre-commit hooks 运行——一个很好的冒烟测试，证明一切正常工作。

## 注意事项

- Husky v9+ 在 hook 文件中不需要 shebang
- `prettier --ignore-unknown` 跳过 Prettier 无法解析的文件（图像等）
- pre-commit 首先运行 lint-staged（快速，仅暂存），然后是完整的 typecheck 和 tests
