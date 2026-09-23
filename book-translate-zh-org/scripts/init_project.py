#!/usr/bin/env python3
import argparse, hashlib, json, re, shutil
from pathlib import Path


def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()


def slugify(s):
    s=re.sub(r'[^A-Za-z0-9._-]+','_',s).strip('_.')
    return s or 'book'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('source')
    ap.add_argument('--out', required=True)
    ap.add_argument('--title', default='')
    ap.add_argument('--author', default='')
    args=ap.parse_args()
    src=Path(args.source).resolve()
    out=Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out/'images').mkdir(exist_ok=True)
    (out/'.translation').mkdir(exist_ok=True)
    (out/'source').mkdir(exist_ok=True)
    digest=sha256(src)
    typ=src.suffix.lower().lstrip('.')
    slug=slugify(out.name)
    org=out/f'{slug}_zh.org'
    if not org.exists():
        org.write_text(
            f'#+TITLE: {args.title or src.stem}
#+AUTHOR: {args.author}
#+LANGUAGE: zh-CN
#+OPTIONS: toc:t num:nil
#+STARTUP: overview

'
            '#+begin_comment
'
            f'- 来源: {src.name}
- Source SHA-256: {digest}
'
            '- 正文采用简体中文和 ASCII 标点.
'
            '- 图片使用相对路径 images/ 并回插原书语义位置.
'
            '- 独立显示公式使用 equation 环境; 无原始编号时添加 \notag.
'
            '- 不使用 \[ ... \].
'
            '#+end_comment

', encoding='utf-8')
    state={
        'source_sha256':digest,'source_type':typ,'current_unit':'','last_heading':'',
        'last_source_locator':'','translated_blocks':0,'image_count':0,'footnote_count':0,
        'status':'in_progress','next_action':'inspect source and begin first natural unit'
    }
    sp=out/'.translation/state.json'
    if not sp.exists(): sp.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'
',encoding='utf-8')
    tp=out/'terminology.tsv'
    if not tp.exists(): tp.write_text('source_term	zh_term	note
',encoding='utf-8')
    rp=out/'README.org'
    if not rp.exists():
        rp.write_text(f'#+TITLE: 翻译工程说明
#+LANGUAGE: zh-CN

* 来源
- 文件: ={src.name}=
- SHA-256: ={digest}=
- 类型: {typ}

* 当前进度
- 下一步: 预检并开始第一自然单元.
',encoding='utf-8')
    print(org)

if __name__=='__main__': main()
