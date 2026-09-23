#!/usr/bin/env python3
import argparse, hashlib, json, sys, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def local(tag):
    return tag.rsplit('}', 1)[-1]


def inspect_pdf(path: Path):
    try:
        import fitz
    except Exception as e:
        raise SystemExit('PyMuPDF is required: pip install PyMuPDF') from e
    doc = fitz.open(path)
    text_pages = 0
    chars = 0
    image_refs = 0
    pages = []
    for i, p in enumerate(doc):
        text = p.get_text('text') or ''
        c = len(text.strip())
        if c >= 40:
            text_pages += 1
        chars += c
        imgs = p.get_images(full=True)
        image_refs += len(imgs)
        pages.append({'page': i+1, 'text_chars': c, 'image_refs': len(imgs)})
    return {
        'type': 'pdf',
        'pages': len(doc),
        'pages_with_text_40plus_chars': text_pages,
        'text_page_ratio': round(text_pages / max(1, len(doc)), 4),
        'total_text_chars': chars,
        'embedded_image_refs': image_refs,
        'likely_scan_only': text_pages / max(1, len(doc)) < 0.15,
        'page_stats': pages,
    }


def inspect_epub(path: Path):
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        container = ET.fromstring(z.read('META-INF/container.xml'))
        rootfile = next(e for e in container.iter() if local(e.tag) == 'rootfile')
        opf_name = rootfile.attrib['full-path']
        opf = ET.fromstring(z.read(opf_name))
        base = Path(opf_name).parent
        manifest = {}
        spine = []
        metadata = {}
        for e in opf.iter():
            t = local(e.tag)
            if t == 'item':
                manifest[e.attrib.get('id')] = {
                    'href': e.attrib.get('href'),
                    'media_type': e.attrib.get('media-type'),
                    'properties': e.attrib.get('properties', '')
                }
            elif t == 'itemref':
                spine.append(e.attrib.get('idref'))
            elif t in {'title','creator','language'} and (e.text or '').strip():
                metadata.setdefault(t, []).append((e.text or '').strip())
        image_items = [v for v in manifest.values() if (v.get('media_type') or '').startswith('image/')]
        html_items = [v for v in manifest.values() if v.get('media_type') in {'application/xhtml+xml','text/html'}]
        return {
            'type': 'epub',
            'opf': opf_name,
            'metadata': metadata,
            'manifest_items': len(manifest),
            'spine_items': len(spine),
            'html_items': len(html_items),
            'image_items': len(image_items),
            'spine': [manifest.get(i, {'idref': i}) for i in spine],
            'zip_entries': len(names),
        }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source')
    ap.add_argument('--json', dest='json_out')
    args = ap.parse_args()
    p = Path(args.source)
    if not p.exists():
        raise SystemExit(f'not found: {p}')
    ext = p.suffix.lower()
    if ext == '.pdf':
        data = inspect_pdf(p)
    elif ext == '.epub':
        data = inspect_epub(p)
    else:
        raise SystemExit('source must be .pdf or .epub')
    result = {
        'source': str(p),
        'size_bytes': p.stat().st_size,
        'sha256': sha256(p),
        **data,
    }
    s = json.dumps(result, ensure_ascii=False, indent=2)
    print(s)
    if args.json_out:
        Path(args.json_out).write_text(s + '
', encoding='utf-8')

if __name__ == '__main__':
    main()
