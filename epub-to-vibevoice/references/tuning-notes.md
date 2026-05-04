# Tuning Notes

- `chunk_chars`: start with `1800`; reduce to `1200` if generation becomes unstable.
- Preserve punctuation and paragraph spacing for better prosody.
- For English narration, `en-soother_woman` is a strong default.
- If long-form generation is unstable, convert first, inspect clean text, then run TTS.
- On Apple Silicon, `--device mps` is the default local choice.
