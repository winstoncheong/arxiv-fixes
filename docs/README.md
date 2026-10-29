# docs/

Cross-cutting notes from modernizing and fixing arXiv sources. These are the
long-form companions to the one-line lessons in [`../MEMORIES.md`](../MEMORIES.md)
and the operating rules in [`../AGENTS.md`](../AGENTS.md).

Per-paper conversion logs do **not** live here; they stay in
`<paper>/readme.md` (e.g. [`../math_9807049v3/readme.md`](../math_9807049v3/readme.md),
[`../hep-th_9408074v2/readme.md`](../hep-th_9408074v2/readme.md)).

## Index

| Note | What it covers |
| --- | --- |
| [tex-modernization-pitfalls.md](./tex-modernization-pitfalls.md) | `documentstyle`, package clashes, fake headings, `eqnarray`, numbering, page-count drift |
| [hyperref-and-bookmarks.md](./hyperref-and-bookmarks.md) | hyperref options, starred-heading anchors, `\texorpdfstring`, PDF-string traps, verification |
| [plain-tex-and-harvmac.md](./plain-tex-and-harvmac.md) | converting plain TeX/harvmac sources, bibliography reconstruction, known losses |

## Conventions

- One topic per file, kebab-case, Markdown.
- Write for the next person who hits the same build error: symptom, cause,
  fix, and how to verify.
- If a note is paper-specific, put it in that paper's `readme.md` instead.
- When you add a note, add one line to `MEMORIES.md` and, if it changes the
  operating rules, update `AGENTS.md`.
- Keep code snippets copy-pasteable and name the file/line they came from
  when that helps.
