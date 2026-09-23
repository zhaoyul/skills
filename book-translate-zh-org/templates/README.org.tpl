#+TITLE: 翻译工程说明
#+LANGUAGE: zh-CN
#+OPTIONS: toc:nil num:nil

* 来源
- 文件: ={{SOURCE_NAME}}=
- SHA-256: ={{SOURCE_SHA256}}=
- 类型: {{SOURCE_TYPE}}

* 主文件
- ={{ORG_FILE}}=
- =images/=

* 处理规范
- 简体中文语义翻译.
- 中文正文使用 ASCII 标点.
- 图片按原书语义位置插入.
- PDF 图片精确裁切, 不使用无关整页截图.
- EPUB 图片优先保留原始二进制.
- 独立公式使用 =equation=, 无原始编号时加 =\notag=.
- 不使用 =\[ ... \]=.

* 当前进度
- 已覆盖: {{CURRENT_RANGE}}
- 最后定位: {{LAST_LOCATOR}}
- 下一步: {{NEXT_ACTION}}

* 验证
{{VALIDATION_SUMMARY}}
