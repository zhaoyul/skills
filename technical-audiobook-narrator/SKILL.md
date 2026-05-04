---
name: technical-audiobook-narrator
description: Convert technical book chapters, papers, tutorials, or lecture notes into precise but listenable audiobook narration scripts, especially when the source contains LaTeX formulas and code in Lisp, C, Java, C#, or similar languages. Use this skill for math/code narration, SSML scripts, audiobook production plans, synchronized transcripts, and compact-vs-precise reading policies.
---

# Technical Audiobook Narrator Skill

## Job to be done

Turn technical written material into an audio-native script that remains accurate without becoming a symbol soup. This skill is for producing:

- Main audiobook narration that explains concepts smoothly.
- Optional detail tracks for formulas, code listings, proofs, and syntax-heavy sections.
- SSML-ready speech text, pronunciation glossaries, and synchronized transcript structures.
- Consistent rules for reading LaTeX formulas and source code.

The default output language is Simplified Chinese with English punctuation. Keep technical identifiers, APIs, method names, library names, and most code symbols in English unless the user asks for full Chinese localization.

## When to use this skill

Use this skill when the user asks for any of the following:

- Create an audiobook version of a technical book, article, course, spec, or documentation.
- Convert LaTeX formulas into spoken narration.
- Convert code blocks into spoken narration.
- Generate SSML for technical content.
- Design a workflow, style guide, or production pipeline for technical audiobooks.
- Decide when to read formulas/code exactly and when to summarize them.
- Produce a narration IR, transcript, chapter script, glossary, or QA checklist for technical audio.

Do not use this skill for ordinary fiction, marketing voiceovers, or non-technical narration unless formulas, code, algorithms, schemas, or dense technical notation are central to the task.

## Default assumptions

If the user does not specify details, assume:

- Audience: technical readers who understand the field but are listening without seeing the page.
- Language: Simplified Chinese narration, with code identifiers and common technical acronyms in English.
- Output: main audiobook script plus optional detail notes for formulas and code.
- Formula policy: use compact semantic reading in the main track, precise structural reading only for short or important formulas.
- Code policy: explain intent and structure in the main track, read exact syntax only for short or syntax-critical code.
- TTS target: SSML-capable engine, but avoid engine-specific SSML unless requested.

Ask a clarifying question only if a blocker prevents useful work. Otherwise make reasonable defaults and state them briefly.

## Core principle

Never dump raw LaTeX or raw code directly into TTS. First compile the source into an audio-native narration script:

```text
source text + LaTeX + code
  -> technical narration IR
  -> main narration + detail track + glossary
  -> optional SSML
```

The main track should optimize for understanding. Exactness belongs in short controlled passages, detail tracks, synchronized text, and appendices.

## Required output structure

For full requests, produce sections in this order:

1. `Narration strategy`: what will be read semantically, precisely, or skipped into detail track.
2. `Main audiobook script`: listenable narration.
3. `Formula detail track`: precise readings for important formulas, if any.
4. `Code detail track`: precise readings for important code, if any.
5. `Glossary and pronunciation notes`: acronyms, identifiers, Greek letters, symbols, APIs.
6. `SSML or narration IR`: only when requested or clearly useful.
7. `QA checklist`: accuracy checks, pronunciation checks, listening checks.

For small snippets, produce only the relevant script, detail notes, and glossary.

## Formula narration policy

Classify each formula into one of these modes:

### Mode F1: Compact semantic reading, default for main track

Use for most formulas. Name the formula first, then read the meaning or compact structure.

Example:

```latex
L(\theta) = -\sum_{i=1}^{n} y_i \log p_\theta(y_i \mid x_i)
```

Main reading:

```text
这里定义交叉熵损失. L theta 等于负的, 对 i 从 1 到 n 求和, y 下标 i 乘以 log p 下标 theta, 条件是 y 下标 i 给定 x 下标 i.
```

### Mode F2: Precise structural reading

Use for short, important, or ambiguity-prone formulas. Explicitly mark numerator, denominator, limits, bracket scope, and conditioning.

Example:

```text
分式, 分子 e 的 z 下标 i 次方, 分母是对 j 从 1 到 K 求和 e 的 z 下标 j 次方.
```

### Mode F3: Verbatim LaTeX reading, rare

Use only when teaching LaTeX syntax or when the literal source is the object of discussion.

Avoid in normal audiobook flow.

## Formula handling rules

- Always introduce long formulas with a name or purpose before reading symbols.
- For nested expressions, read from outer structure to inner structure.
- For fractions, prefer `分式, 分子..., 分母...` over ambiguous `over` phrasing.
- For summations and integrals, include limits and variable of summation/integration.
- For probability, read `\mid` as `given` or `条件是`, not `vertical bar` unless syntax matters.
- For matrices, tensors, long derivations, and multi-line alignments, summarize in the main track and move exact reading to detail track.
- Never silently omit a mathematical condition if it changes the meaning.

More detailed rules are in `references/math-speech-style.md`.

## Code narration policy

Classify each code block into one of these modes:

### Mode C1: Semantic reading, default for main track

Explain what the code does, its control flow, data flow, and key API calls. Do not read punctuation unless it matters.

Example:

```c
for (int i = 0; i < n; i++) {
    sum += a[i];
}
```

Main reading:

```text
这是一个 for 循环. i 从 0 开始, 当 i 小于 n 时继续, 每轮 i 自增. 循环体把 a 下标 i 累加到 sum.
```

### Mode C2: Exact compact reading

Use for short snippets, syntax teaching, or code whose exact shape matters.

```text
for, 括号内三段: int i 赋值 0; i 小于 n; i 自增. 块内: sum 加等于 a 方括号 i.
```

### Mode C3: Token reading, rare

Use only for operators, regex, macros, pointer expressions, or syntax puzzles where every token matters.

Avoid full-line token dumps in the main track.

## Code handling rules

- Do not read long listings line by line in the main track.
- For 1 to 5 lines, exact compact reading may be appropriate.
- For 6 to 20 lines, summarize first and read only key lines if needed.
- For 20+ lines, describe structure, modules, functions, branches, and key invariants. Put exact reading in detail track.
- Preserve differences among `=`, `==`, `===`, `=>`, `->`, `&`, `*`, `&&`, `||`, `?`, and `!` when relevant.
- For C pointers, distinguish declaration, dereference, and address-of by context.
- For Java/C# generics, read semantic types rather than angle brackets unless teaching syntax.
- For Lisp-like languages, read S-expression intent, not every parenthesis.
- Never invent behavior. If code meaning is uncertain, say what is syntactically visible and mark uncertainty.

More detailed rules are in `references/code-speech-style.md`.

## Narration IR

When the user requests a reusable pipeline, machine-readable output, or SSML, create a narration IR. Prefer YAML unless the user asks for JSON.

Recommended segment fields:

```yaml
segments:
  - id: ch01-p001
    type: prose | math | code | figure | table | aside
    source_ref: optional source location
    language: optional code language
    mode: main | formula-compact | formula-precise | code-semantic | code-exact | code-token
    source: original source text, LaTeX, or code
    speech: final spoken text
    ssml_hint:
      rate: medium | slow | x-slow
      pause_after_ms: 300
    detail_track: optional precise reading or note
```

Use `templates/narration-ir.yaml` as the default shape.

## SSML policy

When producing SSML:

- Escape XML entities correctly.
- Use paragraphs and sentences for structure.
- Add pauses before and after formulas/code.
- Slightly slow formulas and code.
- Do not overuse emphasis.
- Keep SSML portable unless the user names a specific engine.
- Put pronunciation decisions in a glossary rather than scattering one-off hacks everywhere.

The optional helper script `scripts/compile_narration_ir.py` can compile a simple JSON/YAML IR into portable SSML.

## Glossary policy

Always create or update a glossary for:

- Acronyms: SQL, HTTP, GUID, AST, JVM, CLR.
- Greek letters and math symbols: theta, lambda, nabla, argmax.
- Code identifiers: `getUserById`, `IEnumerable`, `malloc`, `cdr`.
- Operators whose reading depends on language: `*`, `&`, `?`, `!`, `=>`, `->`.
- Domain-specific terms whose TTS pronunciation is likely to fail.

For Chinese narration, prefer this style:

```text
结构词用中文, 标识符和 API 名称保留英文或近似英文读法.
```

Example:

```text
users dot Where, lambda u, 条件是 u dot IsActive.
```

## Quality checklist

Before finalizing, check:

- Formula speech preserves variables, limits, conditions, and scopes.
- Code speech preserves assignment vs comparison, pointer/address semantics, generic types, and lambda syntax.
- Long formulas and long code are not dumped into the main track.
- Glossary covers all risky pronunciations.
- Main track can be understood without looking at the page.
- Detail track or synchronized transcript preserves exact source where needed.
- No hallucinated interpretation has been added to code or math.

## Response style

Be practical and production-oriented. Prefer complete scripts, templates, and rules over vague advice. Use concise labels, clear sections, and copyable blocks. Keep the tone relaxed but technically exact.
