# Troubleshooting

## pandoc not found
Install with Homebrew:

```bash
brew install pandoc
```

## Output has too much noise
- Lower chunk size: `--chunk_chars 1200`
- Re-run cleaner and inspect `*.clean.txt`
- Remove remaining front/back matter manually if needed

## TTS crashes on long text
- Use chunking and synthesize per chunk
- Reduce chunk size
- Close heavy apps when running on MPS

## Prosody sounds flat
- Preserve punctuation and paragraph breaks
- Keep chapter/section boundaries clear
- Re-clean text if there is too much boilerplate or markup noise
