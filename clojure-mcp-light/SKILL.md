---
name: clojure-mcp-light
description: 在 Clojure 项目中组合使用 `clj-nrepl-eval`、`clj-paren-repair-claude-hook` 和 `clj-paren-repair` 来完成 nREPL 求值与分隔符修复. 当用户提到 Clojure、nREPL、括号/分隔符错误、Paren Edit Death Loop、Claude hooks，或想在 Claude Code、Codex、Gemini 中验证和修复 `.clj/.cljs/.cljc/.bb` 文件时使用.
---

# Clojure MCP Light 工具集

把 `clj-nrepl-eval`、`clj-paren-repair-claude-hook` 和 `clj-paren-repair` 视为一套配合使用的工作流，而不是三个孤立命令。

## 何时用哪个工具

- **需要 REPL 求值或验证代码**：使用 `clj-nrepl-eval`
- **在 Claude Code 中自动修复括号/分隔符**：使用 `clj-paren-repair-claude-hook`
- **在 Codex、Gemini 或 Bash 编辑后手动修复文件**：使用 `clj-paren-repair`

## 1. 先确认依赖

先检查是否已安装：

```bash
bb --version
bbin --version
```

缺失时先让用户安装 **Babashka** 和 **bbin**。

## 2. 安装命令行工具

按需安装，或直接安装全套：

```bash
bbin install https://github.com/bhauman/clojure-mcp-light.git --tag v0.2.2
bbin install https://github.com/bhauman/clojure-mcp-light.git --tag v0.2.2 --as clj-nrepl-eval --main-opts '["-m" "clojure-mcp-light.nrepl-eval"]'
bbin install https://github.com/bhauman/clojure-mcp-light.git --tag v0.2.2 --as clj-paren-repair --main-opts '["-m" "clojure-mcp-light.paren-repair"]'
```

## 3. 按客户端选择接入方式

### Claude Code

优先配置 `clj-paren-repair-claude-hook --cljfmt` 到 `~/.claude/settings.json` 的 `PreToolUse`、`PostToolUse` 和 `SessionEnd` hooks，让 Clojure 文件在写入前后自动修复分隔符。

同时保留 `clj-paren-repair`，因为 agent 也可能通过 Bash 修改文件，此时 hooks 覆盖不到。

### Codex / Gemini / 其他有 shell 的客户端

在 `AGENTS.md`、`GEMINI.md`、`CLAUDE.md` 等自定义说明里明确写明：

- 用 `clj-nrepl-eval` 做 nREPL 求值
- 遇到分隔符错误时不要陷入手工修括号循环，直接运行 `clj-paren-repair`

## 4. 推荐日常工作流

1. 先启动项目自己的 nREPL
2. 用 `clj-nrepl-eval --discover-ports` 找到当前项目端口
3. 用 `clj-nrepl-eval -p <PORT>` 验证命名空间是否可加载、函数是否工作
4. 编辑 `.clj/.cljs/.cljc/.bb` 文件后：
   - Claude Code + hooks：让 hook 自动修复
   - 其他客户端或 Bash 编辑：运行 `clj-paren-repair <files>`
5. 重新 `require` 时总是带 `:reload`

## 5. 常用命令

```bash
clj-nrepl-eval --discover-ports
clj-nrepl-eval -p <PORT> "(require '[my.ns :as ns] :reload)"
clj-nrepl-eval -p <PORT> <<'EOF'
(ns/my-fn ...)
EOF
clj-nrepl-eval -p <PORT> --reset-session
clj-paren-repair path/to/file.clj
clj-paren-repair src/core.clj test/core_test.clj
```

## 关键注意事项

- `clj-nrepl-eval` 的 session 会跨调用持久化
- 传多行 Clojure 代码时优先使用 heredoc，避免 shell 转义问题
- `clj-nrepl-eval` 会自动尝试修复轻微分隔符错误，但它的目标是 **求值**
- `clj-paren-repair` 和 Claude hook 的目标是 **修复文件**
- 当模型出现括号错配时，不要反复手工修复；优先调用工具脱离 “Paren Edit Death Loop”
