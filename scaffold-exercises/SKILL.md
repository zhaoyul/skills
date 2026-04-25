---
name: scaffold-exercises
description: 创建包含章节, 问题, 解决方案和通过 linting 的说明的练习目录结构. 当用户想要搭建练习, 创建练习存根, 设置新课程章节, 提到 "练习脚手架" 或 "生成练习目录" 时使用.
---

# 搭建练习结构

创建通过 `pnpm ai-hero-cli internal lint` 的练习目录结构, 然后使用 `git commit` 提交.

## 目录命名

- **章节**: `exercises/` 内的 `XX-section-name/`(例如, `01-retrieval-skill-building`)
- **练习**: 章节内的 `XX.YY-exercise-name/`(例如, `01.03-retrieval-with-bm25`)
- 章节编号 = `XX`, 练习编号 = `XX.YY`
- 名称采用短横线命名法(小写, 连字符)

## 练习变体

每个练习至少需要以下子文件夹之一:

- `problem/` - 带有 TODO 的学生工作区
- `solution/` - 参考实现
- `explainer/` - 概念材料, 无 TODO

在创建存根时, 默认为 `explainer/`, 除非计划另有说明.

## 必需文件

每个子文件夹(`problem/`, `solution/`, `explainer/`)需要一个 `readme.md`:

- **不为空**(必须有真实内容, 即使是单个标题行也可以)
- 没有损坏的链接

在创建存根时, 创建一个包含标题和描述的最小 readme:

```md
# 练习标题

在此填写描述
```

如果子文件夹有代码, 它还需要一个 `main.ts`(>1 行). 但对于存根, 只有 readme 的练习也可以.

## 工作流程

1.** 解析计划** - 提取章节名称, 练习名称和变体类型
2.** 创建目录** - 为每个路径使用 `mkdir -p`
3.** 创建存根 readmes** - 每个变体文件夹一个带标题的 `readme.md`
4.** 运行 lint** - `pnpm ai-hero-cli internal lint` 以验证
5.** 修复任何错误** - 迭代直到 lint 通过

## Lint 规则摘要

linter(`pnpm ai-hero-cli internal lint`)检查:

- 每个练习都有子文件夹(`problem/`, `solution/`, `explainer/`)
- 至少存在 `problem/`, `explainer/` 或 `explainer.1/` 之一
- 主子文件夹中存在 `readme.md` 且不为空
- 没有 `.gitkeep` 文件
- 没有 `speaker-notes.md` 文件
- readmes 中没有损坏的链接
- readmes 中没有 `pnpm run exercise` 命令
- 每个子文件夹需要 `main.ts`, 除非它是仅 readme

## 移动/重命名练习

重新编号或移动练习时:

1. 使用 `git mv`(而非 `mv`)重命名目录 - 保留 git 历史
2. 更新数字前缀以维持顺序
3. 移动后重新运行 lint

示例:

```bash
git mv exercises/01-retrieval/01.03-embeddings exercises/01-retrieval/01.04-embeddings
```

## 示例: 从计划创建存根

给定如下计划:

```
第 05 节: 记忆技能构建
- 05.01 记忆简介
- 05.02 短期记忆(explainer + problem + solution)
- 05.03 长期记忆
```

创建:

```bash
mkdir -p exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer
mkdir -p exercises/05-memory-skill-building/05.02-short-term-memory/{explainer,problem,solution}
mkdir -p exercises/05-memory-skill-building/05.03-long-term-memory/explainer
```

然后创建 readme 存根:

```
exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer/readme.md -> "# 记忆简介"
exercises/05-memory-skill-building/05.02-short-term-memory/explainer/readme.md -> "# 短期记忆"
exercises/05-memory-skill-building/05.02-short-term-memory/problem/readme.md -> "# 短期记忆"
exercises/05-memory-skill-building/05.02-short-term-memory/solution/readme.md -> "# 短期记忆"
exercises/05-memory-skill-building/05.03-long-term-memory/explainer/readme.md -> "# 长期记忆"
```
