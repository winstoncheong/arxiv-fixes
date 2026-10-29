# math/9807049v3 — conversion notes

Hirschowitz–Simpson, *Descente pour les n-champs (Descent for n-stacks)*,
arXiv:math/9807049v3 (13 March 2001).

## Source

The e-print is a **single gzipped `.tex`**, not a tarball:

```bash
curl -sL -o src.gz https://arxiv.org/e-print/math/9807049v3
file src.gz          # gzip compressed data, was "2001new2.tex"
gunzip -c src.gz > math_9807049v3.tex
```

It is pure ASCII, 16 983 lines, LaTeX 2.09 (`\documentstyle[12pt]{article}`),
with a long commented errata header for v2/v3 preserved at the top.

Structure: 21 `\numero` sections, 71 `\subnumero` subheads, one
`thebibliography` (122 `\bibitem`s), 667 `\cite`s. No figures, no
`\includegraphics`, no `\input`/`\include`.

## Changes

- `\documentstyle[12pt]{article}` → `\documentclass[12pt]{article}`; added
  `amsmath` and `amssymb`.
- `\numero{#1}` → `\newpage\section{#1}`. The old macro manually incremented
  `section`, reset `subsection` and reset the `lemma` counter; `\section`
  does all three because the theorems are declared `[section]`.
- `\subnumero{#1}` → `\subsection*{#1}\phantomsection\addcontentsline{toc}{subsection}{#1}`,
  so the unnumbered subheads get PDF bookmarks.
- `hyperref` with color links, bookmarks, `pagebackref`; PDF title/author
  metadata set.
- The single `eqnarray*` (around the proof in section 16) → `align*`.
- Math in section/subsection titles wrapped in `\texorpdfstring`, with ASCII
  PDF strings (`$n$` → `n`, `$\infty$` → `infini`, `$\emptyset$` →
  `l'ensemble vide`, `$\Xx/X$` → `X/X`, `$M_f$` → `M\_f`).
- `\boxtimes` changed from `\newcommand` to `\renewcommand`; `amssymb`
  already defines it.

The hand-written `Sommaire` is kept as-is. Its `\pageref` labels sit right
after the new `\section`s, so the page numbers track the new pagination.

## Verification

```bash
cd math_9807049v3
latexmk -pdf -interaction=nonstopmode math_9807049v3.tex
grep -c '^!' math_9807049v3.log                  # 0
grep -c 'Token not allowed' math_9807049v3.log   # 0
grep -ci undefined math_9807049v3.log            # 0
pdfinfo math_9807049v3.pdf | grep Pages          # 253
```

The official arXiv PDF has 251 pages. The two extra pages come from the
standard article heading layout and the longer bibliography produced by
`pagebackref`; content and theorem numbering were spot-checked against the
official PDF (title page, Sommaire, Introduction, a theorem-heavy page, and
the bibliography).

PDF outline: 92 entries (21 sections + 71 subheads). Spot-check with
`fitz`:

```python
import fitz
d = fitz.open("math_9807049v3.pdf")
print(len(d.get_toc()))
```

## Known differences

- Printed section headings are standard left-aligned LaTeX headings
  (`1 Introduction`) instead of the original centered `1. Introduction`.
  Section and theorem numbering are unchanged.
- The hand-written Sommaire still says `1. Introduction` while the heading
  says `1 Introduction`; this is cosmetic.
- Text extraction is OT1: `é` extracts as `´e`. A future T1 + `lmodern`
  pass would fix it but would change metrics and pagination.

See [`../MEMORIES.md`](../MEMORIES.md) and
[`../docs/tex-modernization-pitfalls.md`](../docs/tex-modernization-pitfalls.md)
for the general lessons from this conversion.
