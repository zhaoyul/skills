# Scripts

## compile_narration_ir.py

Compiles a simple narration IR into portable SSML.

Run with JSON:

```bash
python scripts/compile_narration_ir.py examples/sample-output.json > sample.ssml
```

Run with YAML, if PyYAML is installed:

```bash
python scripts/compile_narration_ir.py examples/sample-output.yaml > sample.ssml
```

The script intentionally does not choose voices or vendor-specific SSML. Add those in a downstream build step after choosing a TTS engine.
