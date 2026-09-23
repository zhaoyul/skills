#!/usr/bin/env python3
import argparse, zipfile
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('project')
    ap.add_argument('--out', required=True)
    ap.add_argument('--exclude-source', action='store_true')
    args=ap.parse_args()
    root=Path(args.project).resolve(); out=Path(args.out).resolve()
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(root.rglob('*')):
            if not p.is_file(): continue
            rel=p.relative_to(root)
            if args.exclude_source and rel.parts and rel.parts[0]=='source': continue
            z.write(p, arcname=str(Path(root.name)/rel))
    print(out)
if __name__=='__main__': main()
