# Agent 技能

一个跨规划、开发和工具的 agent 技能集合，用于扩展能力。

在安装了 Node.js 的情况下，使用 `npx` 安装指定技能：

```bash
npx skills@latest add zhaoyul/skills --skill <skill-name>
```

## 规划与设计

这些技能帮助你在编写代码之前思考问题。

- **to-prd** — 将当前对话上下文转化为 PRD 并作为 GitHub issue 提交。无需访谈——仅综合你已经讨论的内容。

  ```
  npx skills@latest add zhaoyul/skills --skill to-prd
  ```

- **to-issues** — 使用垂直切片将任何计划、规格或 PRD 分解为可独立认领的 GitHub issues。

  ```
  npx skills@latest add zhaoyul/skills --skill to-issues
  ```

- **grill-me** — 对计划或设计进行无情的访谈，直到决策树的每个分支都得到解决。

  ```
  npx skills@latest add zhaoyul/skills --skill grill-me
  ```

- **design-an-interface** — 使用并行子代理为模块生成多个截然不同的接口设计。

  ```
  npx skills@latest add zhaoyul/skills --skill design-an-interface
  ```

- **request-refactor-plan** — 通过用户访谈创建包含微小提交的详细重构计划，然后将其归档为 GitHub issue。

  ```
  npx skills@latest add zhaoyul/skills --skill request-refactor-plan
  ```

## 开发

这些技能帮助你编写、重构和修复代码。

- **clojuredart-dev-skill** — ClojureDart 开发技能，包含跨平台移动开发的标准命令、互操作惯用法和调试检查清单。

  ```
  npx skills@latest add zhaoyul/skills --skill clojuredart-dev-skill
  ```

- **clojure-mcp-light** — 在 Clojure 项目中组合使用 `clj-nrepl-eval`、`clj-paren-repair-claude-hook` 和 `clj-paren-repair` 进行 nREPL 求值与分隔符修复。

  ```
  npx skills@latest add zhaoyul/skills --skill clojure-mcp-light
  ```

- **paren-lisp-repair** — 使用捆绑的 Babashka 脚本修复 Emacs Lisp、Scheme、Common Lisp 等 Lisp 文件中的括号/分隔符错误。

  ```
  npx skills@latest add zhaoyul/skills --skill paren-lisp-repair
  ```

- **tdd** — 使用红-绿-重构循环的测试驱动开发。每次构建一个垂直切片的功能或修复 bug。

  ```
  npx skills@latest add zhaoyul/skills --skill tdd
  ```

- **triage-issue** — 通过探索代码库调查 bug，识别根本原因，并提交包含基于 TDD 的修复计划的 GitHub issue。

  ```
  npx skills@latest add zhaoyul/skills --skill triage-issue
  ```

- **improve-codebase-architecture** — 在代码库中寻找深化机会，参考 `CONTEXT.md` 中的领域语言和 `docs/adr/` 中的决策。

  ```
  npx skills@latest add zhaoyul/skills --skill improve-codebase-architecture
  ```

- **migrate-to-shoehorn** — 将测试文件从 `as` 类型断言迁移到 @total-typescript/shoehorn。

  ```
  npx skills@latest add zhaoyul/skills --skill migrate-to-shoehorn
  ```

- **scaffold-exercises** — 创建包含章节、问题、解决方案和说明的练习目录结构。

  ```
  npx skills@latest add zhaoyul/skills --skill scaffold-exercises
  ```

## 工具与设置

- **setup-pre-commit** — 使用 lint-staged、Prettier、类型检查和测试设置 Husky pre-commit hooks。

  ```
  npx skills@latest add zhaoyul/skills --skill setup-pre-commit
  ```

- **git-guardrails-claude-code** — 设置 Claude Code hooks 以在执行前阻止危险的 git 命令（push、reset --hard、clean 等）。

  ```
  npx skills@latest add zhaoyul/skills --skill git-guardrails-claude-code
  ```

## 写作与知识

- **write-a-skill** — 创建具有适当结构、渐进披露和捆绑资源的新技能。

  ```
  npx skills@latest add zhaoyul/skills --skill write-a-skill
  ```

- **edit-article** — 通过重组章节、提高清晰度和精简文字来编辑和改进文章。

  ```
  npx skills@latest add zhaoyul/skills --skill edit-article
  ```

- **ubiquitous-language** — 从当前对话中提取 DDD 风格的通用语言术语表。

  ```
  npx skills@latest add zhaoyul/skills --skill ubiquitous-language
  ```

- **obsidian-vault** — 使用 wikilinks 和索引笔记在 Obsidian vault 中搜索、创建和管理笔记。

  ```
  npx skills@latest add zhaoyul/skills --skill obsidian-vault
  ```
