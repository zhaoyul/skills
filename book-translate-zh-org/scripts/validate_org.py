#!/usr/bin/env python3
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

FULLWIDTH='，。；：！？（）“”‘’'
IMG_RE=re.compile(r'\[\[file:([^\]\n]+\.(?:png|jpe?g|gif|webp|svg|bmp|tiff?))(?:\]\[[^\]]*\])?\]\]',re.I)
HEADING_RE=re.compile(r'^(\*+)\s+(.+)$',re.M)
FOOT_REF_RE=re.compile(r'\[fn:([^\]\s]+)\]')
FOOT_DEF_RE=re.compile(r'^\[fn:([^\]\s]+)\]\s+',re.M)
BEGIN_RE=re.compile(r'^#\+begin_([A-Za-z0-9_-]+)\b',re.I)
END_RE=re.compile(r'^#\+end_([A-Za-z0-9_-]+)\b',re.I)

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def check_blocks(lines):
    stack=[]; errors=[]
    for n,line in enumerate(lines,1):
        m=BEGIN_RE.match(line)
        if m: stack.append((m.group(1).lower(),n)); continue
        m=END_RE.match(line)
        if m:
            typ=m.group(1).lower()
            if not stack: errors.append(f'line {n}: end_{typ} without begin'); continue
            top,ln=stack.pop()
            if top!=typ: errors.append(f'line {n}: end_{typ} closes begin_{top} from line {ln}')
    for typ,n in stack: errors.append(f'line {n}: unclosed begin_{typ}')
    return errors

def run_cmd(cmd):
    try:
        p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=120)
        return p.returncode, p.stdout[-6000:]
    except Exception as e: return 999, repr(e)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('org')
    ap.add_argument('--images', default=None)
    ap.add_argument('--report', default=None)
    ap.add_argument('--json', dest='json_out', default=None)
    ap.add_argument('--skip-external', action='store_true')
    args=ap.parse_args()
    org=Path(args.org).resolve(); root=org.parent
    raw=org.read_bytes(); text=raw.decode('utf-8',errors='replace'); lines=text.splitlines()
    issues=[]; warnings=[]
    replacement=text.count('\ufffd'); nul=text.count('\x00'); cr=raw.count(b'\r'); trailing=sum(1 for l in text.split('\n') if l.endswith(' ') or l.endswith('\t'))
    if replacement: issues.append(f'UTF-8 replacement chars: {replacement}')
    if nul: issues.append(f'NUL chars: {nul}')
    if cr: warnings.append(f'CR bytes: {cr}')
    if trailing: warnings.append(f'trailing whitespace lines: {trailing}')
    block_errors=check_blocks(lines); issues.extend(block_errors)
    forbidden=len(re.findall(r'\\\[|\\\]',text))
    if forbidden: issues.append(f'forbidden \\[ or \\] delimiters: {forbidden}')
    eq_begin=len(re.findall(r'\\begin\{equation\*?\}',text)); eq_end=len(re.findall(r'\\end\{equation\*?\}',text))
    if eq_begin!=eq_end: issues.append(f'equation environments unbalanced: {eq_begin} begin vs {eq_end} end')
    headings=HEADING_RE.findall(text); jumps=[]; prev=None
    for stars,title in headings:
        level=len(stars)
        if prev is not None and level>prev+1: jumps.append((prev,level,title[:80]))
        prev=level
    if jumps: warnings.append(f'heading jumps: {len(jumps)}')
    refs=FOOT_REF_RE.findall(text); defs=FOOT_DEF_RE.findall(text)
    refset=set(refs); defset=set(defs); missing=sorted(refset-defset); orphan=sorted(defset-refset)
    if missing: issues.append(f'missing footnote definitions: {missing[:20]}')
    if orphan: warnings.append(f'orphan footnote definitions: {orphan[:20]}')
    image_links=IMG_RE.findall(text); missing_images=[]; bad_images=[]
    for rel in image_links:
        p=(root/rel).resolve()
        if not p.exists(): missing_images.append(rel); continue
        if p.suffix.lower()=='.svg':
            try:
                if '<svg' not in p.read_text(encoding='utf-8',errors='ignore')[:5000]: bad_images.append(rel)
            except Exception: bad_images.append(rel)
        else:
            try:
                from PIL import Image
                with Image.open(p) as im: im.verify()
            except Exception: bad_images.append(rel)
    if missing_images: issues.append(f'missing image files: {missing_images[:20]}')
    if bad_images: issues.append(f'undecodable image files: {bad_images[:20]}')
    punct={ch:text.count(ch) for ch in FULLWIDTH if text.count(ch)}
    if punct: warnings.append('fullwidth Chinese punctuation present: '+json.dumps(punct,ensure_ascii=False))
    # high-English-residue prose candidates, excluding directives, links and obvious code blocks.
    candidates=[]; in_block=False
    for i,l in enumerate(lines,1):
        if BEGIN_RE.match(l): in_block=True
        if in_block:
            if END_RE.match(l): in_block=False
            continue
        s=l.strip()
        if not s or s.startswith('#+') or s.startswith('[[') or s.startswith('|') or s.startswith(':'): continue
        letters=len(re.findall(r'[A-Za-z]',s)); cjk=len(re.findall(r'[\u4e00-\u9fff]',s))
        if letters>=60 and letters>cjk*2: candidates.append({'line':i,'text':s[:220]})
    external={}
    if not args.skip_external:
        if shutil.which('pandoc'):
            rc,out=run_cmd(['pandoc','-f','org','-t','native',str(org),'-o',os.devnull])
            external['pandoc']={'status':'PASS' if rc==0 else 'FAIL','output':out}
            if rc!=0: issues.append('pandoc parse failed')
        else: external['pandoc']={'status':'NOT RUN','output':'pandoc not installed'}
        if shutil.which('emacs'):
            elisp=("(progn (require 'org) (find-file \""+str(org).replace('\\','\\\\').replace('"','\\"')+"\") "
                   "(let ((r (org-lint))) (princ (format \"%S\" r)) (kill-emacs (if r 2 0))))")
            rc,out=run_cmd(['emacs','--batch','--eval',elisp])
            external['emacs_org_lint']={'status':'PASS' if rc==0 else 'FAIL','output':out}
            if rc!=0: warnings.append('emacs org-lint reported findings')
        else: external['emacs_org_lint']={'status':'NOT RUN','output':'emacs not installed'}
    status='PASS' if not issues else 'FAIL'
    result={
        'status':status,'org':str(org),'org_sha256':sha256(org),'bytes':len(raw),'lines':len(lines),
        'headings':len(headings),'heading_jumps':jumps,'image_refs':len(image_links),
        'missing_images':missing_images,'bad_images':bad_images,'footnote_refs':len(refs),'footnote_defs':len(defs),
        'missing_footnotes':missing,'orphan_footnotes':orphan,'replacement_chars':replacement,'nul_chars':nul,
        'cr_bytes':cr,'trailing_whitespace_lines':trailing,'forbidden_display_delimiters':forbidden,
        'equation_begin':eq_begin,'equation_end':eq_end,'fullwidth_punctuation':punct,
        'high_english_residue_candidates':candidates[:100],'issues':issues,'warnings':warnings,'external':external
    }
    report=[]
    report += [f'Status: {status}',f'Org: {org}',f'Org SHA-256: {result["org_sha256"]}','']
    report += ['Structure:',f'- headings: {len(headings)}',f'- heading jumps: {len(jumps)}','']
    report += ['Images:',f'- Org image refs: {len(image_links)}',f'- missing: {len(missing_images)}',f'- undecodable: {len(bad_images)}','']
    report += ['Footnotes:',f'- refs: {len(refs)}',f'- definitions: {len(defs)}',f'- missing: {len(missing)}',f'- orphan: {len(orphan)}','']
    report += ['Org:',f'- block errors: {len(block_errors)}',f'- forbidden \\[...\\] tokens: {forbidden}',f'- equation begin/end: {eq_begin}/{eq_end}',f'- fullwidth punctuation kinds: {len(punct)}',f'- high English residue candidates: {len(candidates)}','']
    if external:
        report += ['Parser:']+[f'- {k}: {v["status"]}' for k,v in external.items()]+['']
    report += ['Issues:'] + ([f'- {x}' for x in issues] or ['- none']) + ['', 'Warnings:'] + ([f'- {x}' for x in warnings] or ['- none'])
    report_text='\n'.join(report)+'\n'
    print(report_text,end='')
    if args.report: Path(args.report).write_text(report_text,encoding='utf-8')
    if args.json_out: Path(args.json_out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if status=='PASS' else 2)

if __name__=='__main__': main()
