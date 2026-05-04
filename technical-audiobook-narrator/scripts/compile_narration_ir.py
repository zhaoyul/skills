#!/usr/bin/env python3
"""
Compile a simple technical audiobook narration IR into portable SSML.

Usage:
    python scripts/compile_narration_ir.py input.json > output.ssml
    python scripts/compile_narration_ir.py input.yaml > output.ssml

YAML support requires PyYAML. JSON works with the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable
from xml.sax.saxutils import escape

RATE_MAP = {
    "x-slow": "x-slow",
    "slow": "slow",
    "medium": "medium",
    "fast": "fast",
    "x-fast": "x-fast",
}


def load_ir(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()

    if suffix == ".json":
        return json.loads(text)

    if suffix in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise SystemExit(
                "YAML input requires PyYAML. Install it with: pip install pyyaml\n"
                "Alternatively, provide a JSON IR file."
            ) from exc
        data = yaml.safe_load(text)
        if not isinstance(data, dict):
            raise SystemExit("IR root must be a mapping/object.")
        return data

    raise SystemExit("Unsupported input format. Use .json, .yaml, or .yml.")


def normalize_rate(value: Any, default: str = "medium") -> str:
    if not isinstance(value, str):
        return default
    return RATE_MAP.get(value, default)


def paragraph(text: str, rate: str | None = None) -> str:
    safe = escape(text.strip())
    if not safe:
        return ""
    if rate and rate != "medium":
        return f'<p><prosody rate="{rate}">{safe}</prosody></p>'
    return f"<p>{safe}</p>"


def pause(ms: Any) -> str:
    try:
        value = int(ms)
    except (TypeError, ValueError):
        return ""
    if value <= 0:
        return ""
    return f'<break time="{value}ms"/>'


def compile_segment(segment: Dict[str, Any]) -> Iterable[str]:
    speech = segment.get("speech", "")
    if not isinstance(speech, str) or not speech.strip():
        return []

    hint = segment.get("ssml_hint", {})
    if not isinstance(hint, dict):
        hint = {}

    seg_type = segment.get("type", "prose")
    default_rate = "slow" if seg_type in {"math", "code"} else "medium"
    rate = normalize_rate(hint.get("rate"), default_rate)

    parts = [paragraph(speech, rate)]
    pause_markup = pause(hint.get("pause_after_ms"))
    if pause_markup:
        parts.append(pause_markup)
    return parts


def compile_ssml(ir: Dict[str, Any]) -> str:
    segments = ir.get("segments")
    if not isinstance(segments, list):
        raise SystemExit("IR must contain a 'segments' array.")

    body = []
    for item in segments:
        if isinstance(item, dict):
            body.extend(compile_segment(item))

    return "<speak>\n" + "\n".join(f"  {line}" for line in body if line) + "\n</speak>\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile narration IR to SSML.")
    parser.add_argument("input", type=Path, help="Path to narration IR, JSON or YAML.")
    args = parser.parse_args()

    ir = load_ir(args.input)
    sys.stdout.write(compile_ssml(ir))


if __name__ == "__main__":
    main()
