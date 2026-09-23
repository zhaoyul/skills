# book-translate-zh-org

将用户提供的 PDF/EPUB 图书翻译为高质量简体中文 Emacs Org-mode 工程, 输出主 `.org` 文件和同级 `images/` 目录, 并提供断点续跑、图片定位、公式保真、脚注闭环和出版级 QA.

## 安装

```bash
npx skills@latest add zhaoyul/skills --skill book-translate-zh-org
```

如果需要直接使用随 Skill 附带的 Python 工具:

```bash
python -m pip install -r requirements.txt
```

可选系统工具:

- `pandoc`: 独立 Org 解析/导出 smoke test.
- `emacs`: `org-mode` / `org-lint` 校验.
- OCR 工具: 仅用于扫描型 PDF 或文本层严重损坏的局部页面, 不作为默认 PDF 路径.

## 核心能力

- PDF/EPUB 两条独立处理链路.
- EPUB 优先复用原始图片资源.
- PDF 优先提取内嵌原图, 复杂矢量图按页面视觉边界精确裁切.
- 保留章节、小节、图表、脚注、引文、代码、公式和阅读顺序.
- 独立公式统一使用 Org/LaTeX `equation` 环境, 原式无编号时使用 `\notag`.
- `.translation/state.json` 支持长书分批翻译和可靠断点续跑.
- `terminology.tsv` 维护全书术语一致性.
- `image-manifest.json` 记录图片来源页、裁切框和哈希.
- `validate_org.py` 对 Org 结构、图片、脚注、公式、英文残留候选和外部解析器进行自动 QA.

## 典型流程

PDF:

```bash
python scripts/inspect_book.py input.pdf
python scripts/pdf_extract_assets.py input.pdf --out project/images --manifest project/image-manifest.json
python scripts/validate_org.py project/book_zh.org --images project/images --report project/VALIDATION_REPORT.txt
python scripts/package_release.py project --out project-release.zip
```

EPUB:

```bash
python scripts/inspect_book.py input.epub
python scripts/extract_epub.py input.epub --out project
python scripts/validate_org.py project/book_zh.org --images project/images --report project/VALIDATION_REPORT.txt
```

这些脚本不替代翻译模型. 它们负责把抽取、断点、资源管理和质量验证变成可重复执行的工程流程.
