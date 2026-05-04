# EPUB -> VibeVoice Text Prep

Prepare EPUB books into pure, narration-friendly text for VibeVoice.

## Use this skill when

- You have an `.epub` and want local TTS/audiobook generation.
- You need cleaner text (remove markdown/noise/watermarks) before synthesis.
- You want optional chunk files for stable long-form generation.

## Commands

### 1) Convert EPUB to clean text

```bash
cd ~/VibeVoice
source venv/bin/activate
python scripts/epub_to_vibevoice_text.py \
  --input "/path/to/book.epub" \
  --output "/path/to/book.clean.txt" \
  --start_regex "^(Chapter|CHAPTER|Prologue|PROLOGUE|To you\.|When Red wins\.)"
```

### 2) Convert + chunk for TTS

```bash
cd ~/VibeVoice
source venv/bin/activate
python scripts/epub_to_vibevoice_text.py \
  --input "/path/to/book.epub" \
  --output "/path/to/book.clean.txt" \
  --chunks_dir "/path/to/chunks" \
  --chunk_chars 1800 \
  --start_regex "^(Chapter|CHAPTER|Prologue|PROLOGUE|To you\.|When Red wins\.)"
```

### 3) Run VibeVoice audiobook generation on clean text

```bash
cd ~/VibeVoice
source venv/bin/activate
python scripts/generate_audiobook_en.py \
  --input "/path/to/book.clean.txt" \
  --output "/path/to/book.wav" \
  --voice en-soother_woman \
  --cfg_scale 1.2 \
  --device mps
```

## Notes

- `chunk_chars`: 1200–2200 is usually stable.
- Keep punctuation and paragraph breaks for better prosody.
- This workflow is optimized for English narration with VibeVoice Realtime.
