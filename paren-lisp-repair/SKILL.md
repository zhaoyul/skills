---
name: paren-lisp-repair
description: 使用捆绑的 Babashka 脚本修复 Emacs Lisp、Scheme、Common Lisp 等 Lisp 文件的括号/分隔符错误. 当用户提到 Lisp 括号错配、Paren Edit Death Loop、`.el/.lisp/.scm` 文件修复，或想在 Claude Code、Codex、Gemini 中批量修复非 Clojure Lisp 文件时使用.
---

# Paren Lisp Repair

用这个技能把“手工补括号”的循环变成一次脚本调用。

## 快速开始

先确认 `bb` 可用：

```bash
bb --version
```

捆绑脚本位于: [scripts/paren-lisp-repair.bb](scripts/paren-lisp-repair.bb)

直接处理文件：

```bash
bb /absolute/path/to/paren-lisp-repair.bb path/to/file.el
bb /absolute/path/to/paren-lisp-repair.bb foo.scm bar.lisp
```

也可以通过 stdin 修复并写回你自己的目标位置：

```bash
cat broken.el | bb /absolute/path/to/paren-lisp-repair.bb
```

## 适用范围

- **Emacs Lisp**: `.el`, `.elisp`
- **Scheme / Racket**: `.scm`, `.ss`, `.sld`, `.sls`, `.rkt`
- **Common Lisp**: `.lisp`, `.lsp`, `.cl`, `.asd`
- **通用 S-expression 文件**: `.sexp`

对其他扩展名可加 `--force` 强制处理。

## 工作流程

1. 先确认目标文件是 Lisp 方言文本，而不是生成文件或二进制文件
2. 优先直接运行捆绑脚本，不要反复手工补括号
3. 单文件失败时，查看 stderr；必要时改用 stdin 模式缩小范围
4. 批量文件时一次传多个路径，让脚本逐个原地修复
5. 修复后再运行项目本身的解释器、测试或格式化工具

## 常用命令

```bash
bb /absolute/path/to/paren-lisp-repair.bb path/to/file.el
bb /absolute/path/to/paren-lisp-repair.bb src/a.scm lib/b.lisp
bb /absolute/path/to/paren-lisp-repair.bb --force path/to/file.l
cat broken.lisp | bb /absolute/path/to/paren-lisp-repair.bb
```

## 注意事项

- 这是**分隔符修复工具**，不是某个方言专属 formatter
- 它基于 parinfer 思路，最适合“缩进大体可信，但括号错了”的场景
- 如果文件扩展名不在支持列表中，默认拒绝处理，避免误改非 Lisp 文件
- 对于极度损坏或缩进本身不可信的代码，可能无法自动修复
