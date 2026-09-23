---
name: book-translate-zh-org
description: >-
  Translate user-provided PDF or EPUB books into high-quality Simplified Chinese Emacs Org-mode,
  preserving the original structure, images, footnotes, formulas, code, tables, links and reading order.
  Produces a primary .org file plus an images/ directory, with resumable chapter-by-chapter processing
  and strict structural/semantic QA. Use for PDF/EPUB -> zh-CN Org translation, book localization,
  image extraction/reinsertion, formula preservation, translation continuation, and final publication audit.
tools: Bash
risk: low
source: local
date_added: '2026-09-23'
---

# PDF/EPUB -> 简体中文 Org + images

## 1. 目标

把用户提供的 PDF 或 EPUB 图书转换为可长期维护的简体中文 Emacs Org-mode 工程. 最终主交付至少包含:

```text
<book-slug>/
├── <book-slug>_zh.org
└── images/
    ├── ...
    └── ...
```

默认同时保留可审计的工程文件:

```text
<book-slug>/
├── <book-slug>_zh.org
├── images/
├── README.org
├── terminology.tsv
├── image-manifest.json
├── VALIDATION_REPORT.txt
└── .translation/
    └── state.json
```

核心原则不是“把英文换成中文”, 而是得到一个结构完整, 图片位置正确, 公式可导出, 可断点续跑, 可机器验证, 可以继续精校的 Org 主版本.

## 2. 不可妥协的硬规则

1. 中文使用简体中文.
2. 正文采用语义翻译, 禁止逐词机械替换.
3. 中文正文默认使用 ASCII/英文标点: `, . : ; ? ! ( ) " '`. 不使用 `，。；：！？`.
4. 保留原书章节层级, 章节顺序, 脚注关系, 引用关系, 图表顺序和重要锚点.
5. 图片必须进入 `images/` 并使用相对链接 `[[file:images/...]]`.
6. PDF 图片不得用“整页截图”代替精确插图. 必须按图形边界裁切, 去除无关页眉, 页脚, 页码和正文.
7. EPUB 优先使用原始图片二进制, 不重新截图, 不无意义转码.
8. 图片必须插回原书对应语义位置. 不得集中堆到章节末尾.
9. 原书没有描述性图注时, 不凭空发明 `#+CAPTION`.
10. 公式必须在 Org/LaTeX 导出链路中有效. 独立显示公式默认使用 `equation` 环境. 原式无编号时添加 `\notag`. 禁止使用 `\[ ... \]`.
11. 行内公式使用 `\( ... \)`.
12. 代码主体, 命令, 路径, 文件名, API, URL, 标识符不得翻译. 代码注释可按语义翻译.
13. 不得重排或擅自重新编号脚注. 原书即使存在非常规编号顺序也应忠实保留.
14. 不得因为“英文比例高”就机械删除英文. 人名, 机构名, 拉丁学名, 论文/书名, 参考文献, 缩写, 技术标识, 双关所需原词应按语义保留.
15. 每次继续任务必须从 `.translation/state.json` 恢复, 防止重复翻译, 漏段或覆盖已精校内容.
16. 所有“通过”结论必须来自实际执行的检查. 环境没有 Emacs 时不得声称执行过 `org-lint`; 没有 Pandoc 时不得声称 Pandoc 解析通过.

## 3. 首次执行: Preflight

收到 PDF/EPUB 后先执行预检, 不要立即从第一页开始翻译.

### 3.1 识别源文件

记录:

- 文件名.
- 类型: PDF / EPUB.
- SHA-256.
- 文件大小.
- 书名, 作者, 语言.
- PDF 总页数, 或 EPUB spine 项数量.
- 是否存在目录.
- 是否包含大量图片.
- 是否包含数学公式.
- 是否包含代码.
- 是否包含脚注/尾注.
- 是否包含扫描页.
- 是否存在双栏或复杂版式.

优先运行:

```bash
python scripts/inspect_book.py <source-file>
```

### 3.2 判断 PDF 文本质量

PDF 先检查文本层覆盖率:

- 文本层完整: 直接提取文本 + 页面版式/图像定位.
- 文本层局部损坏: 对问题页做局部修复, 不对整书 OCR.
- 扫描型 PDF: OCR 只能作为最后手段. OCR 后仍需回看页面图像校对专名, 数字, 公式, 连字符和脚注.

不要用 OCR 覆盖本来质量良好的 PDF 文本层.

### 3.3 建立工程

```text
<book-slug>/
├── source/                 # 可选, 原书或来源记录
├── <book-slug>_zh.org
├── images/
├── terminology.tsv
├── image-manifest.json
├── README.org
├── VALIDATION_REPORT.txt
└── .translation/state.json
```

`state.json` 至少记录:

```json
{
  "source_sha256": "...",
  "source_type": "pdf|epub",
  "current_unit": "chapter/spine/page identifier",
  "last_heading": "...",
  "last_source_locator": "...",
  "translated_blocks": 0,
  "image_count": 0,
  "footnote_count": 0,
  "status": "in_progress",
  "next_action": "..."
}
```

每完成一个稳定批次立即更新状态.

## 4. EPUB 工作流

EPUB 是结构化来源, 优先保留其原始语义结构.

### 4.1 解包与 spine

1. 读取 `META-INF/container.xml`.
2. 找到 OPF.
3. 读取 manifest, spine, nav/NCX.
4. 以 spine 顺序作为正文主顺序, 不按文件名猜章节顺序.
5. 保存每个正文块的来源 XHTML id / href, 便于断点和锚点校验.

可运行:

```bash
python scripts/extract_epub.py <book.epub> --out <project-dir>
```

### 4.2 EPUB 图片

- 从 EPUB 直接提取原始图片到 `images/`.
- 尽量保留原图格式. 为稳定链接可以重命名, 但必须在 `image-manifest.json` 记录原 href -> 新路径.
- 图片顺序必须与 spine 中 `<img>` 出现顺序一致.
- 对 SVG, 若 Emacs/导出链路可直接使用则保留 SVG; 若必须栅格化, 需同时保留来源映射.
- 不要把 EPUB 插图重新截图成低质量 PNG.

### 4.3 XHTML -> Org 结构映射

推荐映射:

| EPUB/XHTML | Org |
|---|---|
| `h1..h6` | `* .. ******` |
| `p` | 普通段落 |
| `blockquote` | `#+begin_quote` |
| `pre/code` | `#+begin_src <lang>` 或 `#+begin_example` |
| `em/i` | Org 斜体, 必要时保留原格式 |
| `strong/b` | Org 粗体 |
| `img` | `[[file:images/...]]` |
| `ol/ul` | Org 列表 |
| footnote/endnote | `[fn:id]` |
| table | Org table 或复杂表格保真策略 |

不要为了“格式整齐”合并原本独立的段落.

## 5. PDF 工作流

PDF 没有可靠语义 DOM, 必须同时处理文本层和页面视觉层.

### 5.1 阅读顺序

对每页确认:

- 单栏 / 双栏 / 多栏.
- 页眉 / 页脚 / 页码.
- 边注.
- 图注.
- 图片与正文穿插关系.
- 跨页段落.
- 连字符断词.

双栏文档不得直接按 PDF 内部对象顺序串接. 必须恢复人类阅读顺序.

### 5.2 图片抽取策略

优先级:

1. 若 PDF 内嵌图片对象完整且就是目标插图, 直接提取原图.
2. 若一幅图由多个对象, 矢量元素或文字组成, 渲染页面后按图形边界裁切.
3. 默认以约 288 DPI 渲染, 兼顾清晰度和文件体积.
4. 裁切区域只包含图形本体. 图注若要翻译为 Org 文本, 则不要重复裁进图片.
5. 若图形与正文/图注穿插成多个碎片, 分别裁切后按照原布局在白色画布上重组.
6. 不得使用整页图片代替独立插图, 除非该页本身就是不可拆解的版式对象, 例如高度公式化的答案页/海报/整版图谱, 并在 README 说明原因.

先列出候选图片区域:

```bash
python scripts/pdf_extract_assets.py <book.pdf> --out <project-dir>/images --manifest <project-dir>/image-manifest.json
```

自动区域只是候选. 复杂页面必须人工/Agent 视觉复核.

### 5.3 图片命名

优先使用稳定语义名:

```text
images/cover.png
images/fig_01_01_perceptron.png
images/fig_01_02_nyt_1958.png
images/ch03_p142_diagram_01.png
```

无法识别图号时使用章节 + 来源页 + 顺序, 不使用随机 UUID 作为最终文件名.

## 6. 翻译规范

### 6.1 翻译目标

要求“信, 达, 雅”中的前两项绝不能牺牲, 第三项服务于原作者语气.

- 忠实信息和论证关系.
- 中文自然, 不保留不必要的英语句法.
- 保留作者语气, 幽默, 讽刺, 学术谨慎程度.
- 不扩写原文没有的观点.
- 不替作者“纠正”立场.
- 不把注释内容偷偷并入正文.

### 6.2 术语表

`terminology.tsv` 至少三列:

```text
source_term	zh_term	note
gradient descent	梯度下降	机器学习通行译法
feedforward	前馈	与 feedback/反馈 成对
hippocampus	海马	不混用 海马体
```

规则:

1. 首次出现前检查术语表.
2. 新术语确定译法后立即加入.
3. 同一语义在全书中保持一致.
4. 作者有意区分的近义词必须分别翻译, 不得统一成一个词.
5. 通俗词与后文严格术语存在递进关系时, 保留这种递进.

### 6.3 数值与数量关系

数字是高风险区. 翻译后必须单独复核:

- 倍数.
- 百分比.
- 范围.
- 单位.
- 正负号.
- 指数.
- 年代.
- 图表数值.

例如 `dropped seventeenfold` 不宜机械译为“下降了十七倍”, 应根据上下文译为“降至原来的约十七分之一”等不会产生数学歧义的中文.

### 6.4 英文保留白名单

通常保留:

- 人名.
- 机构名/产品名, 尤其没有稳定中文名时.
- 拉丁学名.
- API, CLI, 命令, 代码, 文件名, 路径.
- URL.
- 缩写: DNA, RNA, ATP, LLM 等.
- 论文/书名和参考文献检索信息.
- 作者正在分析的英语词语或双关.
- 技术术语首次出现时必要的英文原词.

其余普通叙述中的英文残留需要逐项判断, 禁止用全局字符串替换“清英文”.

## 7. Org-mode 输出规范

### 7.1 文件头

推荐:

```org
#+TITLE: 中文书名
#+SUBTITLE: 副标题
#+AUTHOR: Author Name
#+LANGUAGE: zh-CN
#+OPTIONS: toc:t num:nil
#+STARTUP: overview
```

可加入翻译说明:

```org
#+begin_comment
翻译说明:
- 依据 ... 版本翻译.
- 正文使用简体中文和 ASCII 标点.
- 图片来自原 EPUB 原图 / PDF 对应页面精确裁切.
- 复杂显示公式使用 equation 环境; 无原始编号时添加 \notag.
#+end_comment
```

### 7.2 标题层级

- 严格按原书语义层级.
- 禁止标题跳级, 除非源书本身如此且有充分理由保留.
- Part / Chapter / Section 不得因为视觉字号相近而混为同一级.

### 7.3 图片

原书有正式图注时:

```org
#+CAPTION: 图 1.1 | 一个感知机
#+ATTR_ORG: :width 900
[[file:images/fig_01_01_perceptron.png]]
```

原书没有描述性图注时:

```org
[[file:images/ch01_p023_01.png]]
```

不得臆造 caption.

### 7.4 公式

行内公式:

```org
质量为 \(m\), 加速度为 \(a\).
```

无原编号的独立公式:

```org
\begin{equation}
E = mc^2
\notag
\end{equation}
```

原书有公式编号时保留编号语义, 不添加 `\notag`.

禁止:

```text
\[ ... \]
```

如果无法高置信度恢复公式为 LaTeX:

1. 优先保留原公式截图在正确位置.
2. 可以额外提供转录候选, 但不得用错误 LaTeX 替换可靠图片.
3. 后续精校再恢复文本公式.

### 7.5 代码与终端输出

代码:

```org
#+begin_src python
print("hello")
#+end_src
```

未知语言或纯输出:

```org
#+begin_example
...
#+end_example
```

代码主体不翻译. 只有自然语言注释可翻译.

### 7.6 引文

```org
#+begin_quote
翻译后的引文.

- Author
#+end_quote
```

### 7.7 脚注

使用 Org 原生脚注:

```org
正文引用.[fn:12]

[fn:12] 脚注内容.
```

必须保证:

- 每个引用都有定义.
- 没有悬空定义, 除非源书确实如此并在 QA 报告说明.
- 编号/命名与原书稳定对应.

### 7.8 表格

简单结构表格转换为 Org table.

复杂表格若存在以下风险, 优先保真而不是强行文本化:

- 多层表头.
- 合并单元格.
- 数学排版密集.
- 单元格内复杂图形.
- 文本抽取导致列错位.

这类表格可以使用精确图片 + 必要的中文说明. 若同时提供文本转录, 必须逐格校验.

## 8. 分批翻译与断点续跑

大型图书必须“同一主文件 + 增量追加”, 不创建互相漂移的多个最终版本.

建议批次单位:

- 优先按章.
- 超长章节按自然小节切分.
- 不在句子, 脚注, 代码块, 表格或图注中间切断.

每批结束执行:

1. 保存 Org.
2. 更新术语表.
3. 保存新图片.
4. 更新 image manifest.
5. 运行验证器.
6. 更新 `.translation/state.json`.
7. 在 README 记录本批覆盖范围和下一起点.

恢复任务时首先读取 state + Org 文件末尾 + 原书对应定位, 三者一致后再继续.

禁止只凭“上次大概做到第几章”继续.

## 9. 图片 Manifest

`image-manifest.json` 推荐记录:

```json
{
  "images": [
    {
      "path": "images/fig_01_01.png",
      "source": "pdf",
      "page": 23,
      "bbox": [72.1, 104.2, 512.8, 430.6],
      "sha256": "...",
      "width": 1800,
      "height": 1200,
      "semantic_anchor": "chapter-1/perceptron"
    }
  ]
}
```

EPUB 记录原 href:

```json
{
  "path": "images/ch01_fig03.jpg",
  "source": "epub",
  "source_href": "OEBPS/images/fig03.jpg",
  "sha256": "..."
}
```

## 10. 自动质量门禁

每批至少运行:

```bash
python scripts/validate_org.py <book_zh.org> --images images
```

最终版再运行完整审核.

### 10.1 结构硬校验

必须检查:

- UTF-8 replacement char 数量为 0.
- NUL 为 0.
- CR 为 0.
- 行尾空格为 0.
- `#+begin_* / #+end_*` 平衡.
- Org 链接括号基本平衡.
- 图片引用全部存在.
- 图片全部可解码.
- 标题没有异常跳级.
- 脚注引用与定义匹配.
- 不使用 `\[ ... \]`.
- `equation` 环境平衡.
- 中文全角标点残留可报告并审查.
- 不出现明显重复章节块.

### 10.2 来源一致性校验

EPUB 最终审核优先比较:

- Part 数.
- Chapter 数.
- 小节数.
- spine 顺序.
- 图片锚点总数和顺序.
- 脚注/尾注数量.
- 本地链接/锚点.

PDF 最终审核优先比较:

- 目录章节是否全部覆盖.
- 来源页范围是否连续.
- 插图是否遗漏.
- 图号是否连续/与原书一致.
- 公式高密度页是否存在抽取损坏.
- 跨页段落是否重复或漏失.

### 10.3 解析校验

如果安装 Pandoc:

```bash
pandoc -f org -t native <book_zh.org> -o /dev/null
```

如果安装 Emacs:

运行 `org-mode` 解析或 `org-lint`.

必须区分:

- 实际执行且通过.
- 工具未安装, 因此未执行.

### 10.4 语义终校

机器验证不能证明翻译质量. 最终还要专项回看:

- 章节标题和双关.
- 核心术语.
- 数字与倍数.
- 否定关系.
- 比较级.
- 因果关系.
- 引文.
- 讽刺/幽默.
- 高英文残留段落.
- OCR 高风险段落.
- 公式附近正文.
- 图注.

采用“机器穷举硬校验 + 高风险表达回看原文 + 术语表约束”.

## 11. 最终 VALIDATION_REPORT.txt

至少写清:

```text
Book: ...
Source SHA-256: ...
Org SHA-256: ...

Structure:
- Parts: source/target
- Chapters: source/target
- Sections: source/target

Images:
- Source image anchors: ...
- Org image refs: ...
- Existing files: .../...
- Decodable: .../...

Footnotes:
- refs: ...
- definitions: ...
- missing: 0
- orphan: 0

Org:
- block balance: PASS
- heading jumps: 0
- broken local image links: 0
- forbidden display delimiters \[...\]: 0
- fullwidth Chinese punctuation: ...

Parser:
- Pandoc: PASS / NOT RUN
- Emacs org-lint: PASS / NOT RUN

Semantic audit:
- terminology reviewed: YES
- numeric expressions reviewed: YES
- high-risk English residue reviewed: YES
```

不要把“NOT RUN”写成“PASS”.

## 12. README.org

README 用于人类交接和继续翻译. 至少记录:

- 原书文件和版本.
- 当前主 Org 文件.
- 图片目录.
- 翻译规则.
- 公式规则.
- 图片处理规则.
- 当前覆盖范围.
- 最后来源页/章节/spine item.
- 下一批从哪里开始.
- 已知问题.
- 已执行验证.

## 13. 完成定义 Definition of Done

只有同时满足以下条件才可声明“全书翻译完成”:

1. 原书所有正文范围已覆盖.
2. 主 Org 不存在批次断裂.
3. 章节/小节结构与源书一致或差异有明确说明.
4. 图片全部提取并回插正确语义位置.
5. 图片链接全部存在且可解码.
6. 公式没有明显缺失/损坏, 高风险公式已回看.
7. 脚注引用/定义闭环.
8. 代码/终端内容未被错误翻译.
9. 术语一致性审查完成.
10. 数字/倍数专项审查完成.
11. 英文残留专项审查完成, 保留项均有语义理由.
12. Org 静态验证通过.
13. Pandoc/Emacs 可用时已执行对应解析检查.
14. `VALIDATION_REPORT.txt` 已生成.
15. `.translation/state.json` 标记 `status: complete`.

## 14. 禁止的捷径

不得:

- 把 PDF 每页整页截图塞进 Org 后声称完成.
- 只翻译 PDF 抽出的纯文本而忽略图片位置.
- 用 OCR 覆盖质量良好的文本层.
- 自动生成不存在的图注.
- 删除“看起来多余”的原书脚注编号.
- 对代码/路径做翻译替换.
- 把复杂公式猜成错误 LaTeX.
- 用正则全局替换处理文学语义.
- 为追求中文比例删除必要英文术语.
- 创建多个无法确定哪个才是主版本的“final-v2-final2”文件.
- 未执行验证就声称“全部通过”.

## 15. 推荐执行顺序

```text
inspect source
  -> initialize project/state
  -> extract structure/assets
  -> construct Org skeleton
  -> translate one chapter/natural unit
  -> insert images/formulas/notes in place
  -> update terminology
  -> validate batch
  -> checkpoint state
  -> repeat
  -> whole-book structural comparison
  -> semantic final audit
  -> parser checks
  -> final validation report
  -> release package
```

当“忠实保真”和“自动化便利”冲突时, 选择忠实保真. 对书籍翻译而言, 一处图片错位或公式误转, 往往比少自动化一步更昂贵.
