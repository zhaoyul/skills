#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('images'); ap.add_argument('--out',required=True); args=ap.parse_args()
    root=Path(args.images); rows=[]
    try: from PIL import Image
    except Exception: Image=None
    for p in sorted(root.rglob('*')):
        if not p.is_file(): continue
        rec={'path':str(p.relative_to(root.parent)),'bytes':p.stat().st_size,'sha256':sha(p)}
        if Image and p.suffix.lower()!='.svg':
            try:
                with Image.open(p) as im: rec.update(width=im.width,height=im.height,format=im.format)
            except Exception: rec['decode_error']=True
        rows.append(rec)
    Path(args.out).write_text(json.dumps({'images':rows},ensure_ascii=False,indent=2)+'
',encoding='utf-8')
    print(f'{len(rows)} images')
if __name__=='__main__': main()
