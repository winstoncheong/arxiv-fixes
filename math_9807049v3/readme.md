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
`thebibliography` (119 `\bibitem`s), 667 `\cite`s. No figures, no
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
- Added `T1` encoding and `lmodern` (the approved default), so text
  extraction is clean (`é`, not `´e`) and fonts are scalable Type 1. This
  changes the metrics and pagination.

The hand-written `Sommaire` is kept as-is. Its `\pageref` labels sit right
after the new `\section`s, so the page numbers track the new pagination.

## Proofreading pass

The typo/errata rules in `AGENTS.md` were applied in a second pass over the
whole source. The scans (comments excluded) covered repeated words, doubled
punctuation, French accent macros, spaces after apostrophes, unmatched
parentheses/brackets in math, and bibliography keys/titles.

Fixed:

- Accent/spelling slips: `c\^ot\'es`, `l'\'epoque`, `n\'ecessaire`,
  `r\'ef\'erences principales`, `tr\`es`, `cl\^oture`, `pr\'echamp`,
  `groupo\"{\i}de(s)`, `l\'eger`, `appliqu\'ee`, `d\'efinit`, `d\'efini`,
  `au-dessus`, and `groupo\"{\i}des` in two bibliography titles.
- Eight `\'a` (acute) that should be `` \`a `` (grave) in the preposition
  “à”.
- Eight stray spaces after apostrophes (`qu' on` → `qu'on`, `d' un` →
  `d'un`, etc.), plus `aue` → `que`, `commme` → `comme`, and one doubled
  comma.
- Agreement: `chacune des ensembles` → `chacun des ensembles`; `Ces deux
  étapes seront traités chacun` → `... traitées chacune`; `la terme` →
  `le terme`.
- Unbalanced delimiters in formulas: `A(Y_j,g_j))`,
  `A'|_{\Xx/\iota})`, `nSePSh(\Xx^{\Gg}`, `\epsilon_0,\ldots,\epsilon_p)`,
  `/\sim )`, two `deg(y_{i+1}`, `L\mm(y))'`, and
  `((y_i),(z_i)\rightarrow`. These are delimiter repairs; the mathematics
  is unchanged.

Deliberately left alone:

- The `Cpx_{\Oo}^{[0,a\}}` notation (a brace in the upper bound) is
  consistent across its occurrences and may be intentional; changing it
  would be a notation change, not a typo fix.
- `[0,\infty)` is a half-open interval, so its closing `)` is not an
  unmatched delimiter.
- The v3 errata header is the authors' text and is preserved.
- Typos inside `%` comment blocks are not rendered and were not changed.

## Verification

```bash
cd math_9807049v3
latexmk -pdf -interaction=nonstopmode math_9807049v3.tex
grep -c '^!' math_9807049v3.log                  # 0
grep -c 'Token not allowed' math_9807049v3.log   # 0
grep -ci undefined math_9807049v3.log            # 0
pdfinfo math_9807049v3.pdf | grep Pages          # 250
```

The official arXiv PDF has 251 pages; the current build has 250. The
one-page difference comes from the standard article heading layout, the
longer bibliography produced by `pagebackref`, and the T1/lmodern metrics.
Content and theorem numbering were spot-checked against the official PDF
(title page, Sommaire, Introduction, a theorem-heavy page, and the
bibliography).

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
- The PDF uses Latin Modern (T1) instead of the original Computer Modern;
  text extraction is clean, but metrics and pagination differ slightly from
  the published version.
- The source's v3 errata header records an error in Lemma 6.2/Proposition
  6.1 and the resulting changes to 10.11, 12.1, 14.4, 15.8, 19.4 and 21.1.
  That header is preserved; the mathematical content was not independently
  checked.

See [`../MEMORIES.md`](../MEMORIES.md) and
[`../docs/tex-modernization-pitfalls.md`](../docs/tex-modernization-pitfalls.md)
for the general lessons from this conversion.
