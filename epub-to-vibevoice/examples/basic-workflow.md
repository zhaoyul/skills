# Basic Workflow

## Convert EPUB to clean text

```bash
cd ~/VibeVoice
source venv/bin/activate
python scripts/epub_to_vibevoice_text.py \
  --input "/path/to/book.epub" \
  --output "/path/to/book.clean.txt"
```

## Optional: create chunks for review or downstream TTS

```bash
python scripts/epub_to_vibevoice_text.py \
  --input "/path/to/book.epub" \
  --output "/path/to/book.clean.txt" \
  --chunks_dir "/path/to/chunks" \
  --chunk_chars 1800
```

## Generate audiobook

```bash
python scripts/generate_audiobook_en.py \
  --input "/path/to/book.clean.txt" \
  --output "/path/to/book.wav" \
  --voice en-soother_woman \
  --cfg_scale 1.2 \
  --device mps
```
