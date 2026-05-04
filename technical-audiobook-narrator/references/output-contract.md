# Output Contract

Use this contract when generating a technical audiobook deliverable.

## Minimal snippet output

```markdown
## Main audiobook script

...

## Detail track

...

## Glossary

| Term | Reading | Note |
|---|---|---|
| ... | ... | ... |
```

## Full chapter output

```markdown
# Technical Audiobook Narration Package

## 1. Narration strategy

- Audience:
- Source assumptions:
- Main-track policy:
- Detail-track policy:

## 2. Main audiobook script

### Section ...

...

## 3. Formula detail track

| Formula id | Mode | Speech |
|---|---|---|

## 4. Code detail track

| Listing id | Language | Mode | Speech |
|---|---|---|---|

## 5. Glossary and pronunciation notes

| Term | Reading | Rule |
|---|---|---|

## 6. Narration IR or SSML

...

## 7. QA checklist

- [ ] Formula scopes preserved.
- [ ] Code operators disambiguated.
- [ ] Long listings not dumped into main track.
- [ ] Glossary covers risky terms.
- [ ] Main track works without looking at page.
```
