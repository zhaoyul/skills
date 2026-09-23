#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path


def file_sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()


def main():
    ap=argparse.ArgumentParser(description='Extract PDF image-region candidates using image rectangles. Visual review is still required.')
    ap.add_argument('pdf')
    ap.add_argument('--out', required=True)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--dpi', type=int, default=288)
    ap.add_argument('--min-width-pt', type=float, default=40)
    ap.add_argument('--min-height-pt', type=float, default=40)
    args=ap.parse_args()
    try:
        import fitz
    except Exception as e: raise SystemExit('pip install PyMuPDF') from e
    try:
        from PIL import Image
    except Exception as e: raise SystemExit('pip install Pillow') from e
    src=Path(args.pdf); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    doc=fitz.open(src); records=[]; idx=0; scale=args.dpi/72.0
    seen=set()
    for pi,page in enumerate(doc,1):
        for img in page.get_images(full=True):
            xref=img[0]
            try: rects=page.get_image_rects(xref)
            except Exception: rects=[]
            for ri,rect in enumerate(rects,1):
                if rect.width < args.min_width_pt or rect.height < args.min_height_pt: continue
                key=(pi,round(rect.x0,2),round(rect.y0,2),round(rect.x1,2),round(rect.y1,2))
                if key in seen: continue
                seen.add(key); idx+=1
                pix=page.get_pixmap(matrix=fitz.Matrix(scale,scale),clip=rect,alpha=False)
                name=f'p{pi:04d}_img{idx:04d}.png'; path=out/name
                pix.save(path)
                try:
                    with Image.open(path) as im: wh=[im.width,im.height]
                except Exception: wh=[pix.width,pix.height]
                records.append({'path':str(Path(out.name)/name),'source':'pdf','page':pi,'xref':xref,
                                'bbox':[round(rect.x0,3),round(rect.y0,3),round(rect.x1,3),round(rect.y1,3)],
                                'dpi':args.dpi,'width':wh[0],'height':wh[1],'sha256':file_sha(path),
                                'review_status':'candidate_needs_visual_review'})
    Path(args.manifest).write_text(json.dumps({'source':str(src),'dpi':args.dpi,'images':records},ensure_ascii=False,indent=2)+'
',encoding='utf-8')
    print(f'wrote {len(records)} candidate crops; visual review/recomposition may still be required')

if __name__=='__main__': main()
