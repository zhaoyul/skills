---
name: obsidian-vault
description: 在 Obsidian vault 中使用 wikilinks 和索引笔记搜索, 创建和管理笔记. 当用户想要在 Obsidian 中查找, 创建或组织笔记, 提到 "整理笔记" 或 "知识库" 时使用.
---

# Obsidian 知识库

## Vault 位置

`/mnt/d/Obsidian Vault/AI Research/`

大部分在根级别是扁平的.

## 命名约定

- **索引笔记**: 聚合相关主题(例如, `Ralph Wiggum Index.md`, `Skills Index.md`, `RAG Index.md`)
- 所有笔记名称使用**标题大小写**
- 不使用文件夹组织 - 而是使用链接和索引笔记

## 链接

- 使用 Obsidian `[[wikilinks]]` 语法: `[[Note Title]]`
- 笔记在底部链接到依赖项/相关笔记
- 索引笔记只是 `[[wikilinks]]` 的列表

## 工作流程

### 搜索笔记

```bash
# 按文件名搜索
find "/mnt/d/Obsidian Vault/AI Research/" -name "*.md" | grep -i "keyword"

# 按内容搜索
grep -rl "keyword" "/mnt/d/Obsidian Vault/AI Research/" --include="*.md"
```

或直接在 vault 路径上使用 Grep/Glob 工具.

### 创建新笔记

1. 文件名使用**标题大小写**
2. 将内容作为学习单元编写(根据 vault 规则)
3. 在底部添加 `[[wikilinks]]` 到相关笔记
4. 如果是编号序列的一部分, 使用分层编号方案

### 查找相关笔记

在 vault 中搜索 `[[Note Title]]` 以查找反向链接:

```bash
grep -rl "\\[\\[Note Title\\]\\]" "/mnt/d/Obsidian Vault/AI Research/"
```

### 查找索引笔记

```bash
find "/mnt/d/Obsidian Vault/AI Research/" -name "*Index*"
```
