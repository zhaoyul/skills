#!/usr/bin/env python3
import argparse, hashlib, json, mimetypes, posixpath, re, zipfile
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET


def local(tag): return tag.rsplit('}',1)[-1]
def sha(b): return hashlib.sha256(b).hexdigest()

def safe_name(idx, href, data):
    ext=Path(href).suffix.lower()
    if not ext:
        ext=mimetypes.guess_extension(mimetypes.guess_type(href)[0] or '') or '.bin'
    stem=re.sub(r'[^A-Za-z0-9._-]+','_',Path(href).stem).strip('_') or 'image'
    return f'epub_{idx:04d}_{stem}{ext}'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('epub')
    ap.add_argument('--out', required=True)
    args=ap.parse_args()
    src=Path(args.epub)
    out=Path(args.out); images=out/'images'; raw=out/'.translation'/'epub-xhtml'
    images.mkdir(parents=True,exist_ok=True); raw.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(src) as z:
        container=ET.fromstring(z.read('META-INF/container.xml'))
        rootfile=next(e for e in container.iter() if local(e.tag)=='rootfile')
        opf_name=rootfile.attrib['full-path']
        opf=ET.fromstring(z.read(opf_name)); base=PurePosixPath(opf_name).parent
        manifest={}; spine=[]
        for e in opf.iter():
            if local(e.tag)=='item':
                manifest[e.attrib.get('id')]={'href':e.attrib.get('href'),'media_type':e.attrib.get('media-type'),'properties':e.attrib.get('properties','')}
            elif local(e.tag)=='itemref': spine.append(e.attrib.get('idref'))
        img_entries=[]; href_map={}; n=0
        for iid,item in manifest.items():
            mt=item.get('media_type') or ''
            if not mt.startswith('image/'): continue
            href=item.get('href')
            full=posixpath.normpath(str(base / PurePosixPath(href)))
            if full not in z.namelist(): continue
            data=z.read(full); n+=1
            name=safe_name(n, href, data); (images/name).write_bytes(data)
            rec={'id':iid,'source_href':full,'path':f'images/{name}','media_type':mt,'bytes':len(data),'sha256':sha(data)}
            img_entries.append(rec); href_map[full]=rec['path']
        spine_entries=[]
        for order,iid in enumerate(spine,1):
            item=manifest.get(iid,{})
            href=item.get('href')
            if not href: continue
            full=posixpath.normpath(str(base / PurePosixPath(href)))
            if full not in z.namelist(): continue
            data=z.read(full)
            suffix=Path(href).suffix or '.xhtml'
            raw_name=f'{order:04d}_{re.sub(r"[^A-Za-z0-9._-]+","_",Path(href).stem)}{suffix}'
            (raw/raw_name).write_bytes(data)
            spine_entries.append({'order':order,'idref':iid,'source_href':full,'raw_path':str(Path('.translation/epub-xhtml')/raw_name)})
    manifest_out={'source':str(src),'images':img_entries,'spine':spine_entries,'href_to_image':href_map}
    (out/'image-manifest.json').write_text(json.dumps(manifest_out,ensure_ascii=False,indent=2)+'
',encoding='utf-8')
    (out/'.translation'/'epub-structure.json').write_text(json.dumps({'spine':spine_entries,'manifest':manifest},ensure_ascii=False,indent=2)+'
',encoding='utf-8')
    print(f'extracted {len(img_entries)} images, {len(spine_entries)} spine items')

if __name__=='__main__': main()
