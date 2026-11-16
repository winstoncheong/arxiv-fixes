# alg-geom/9506012v1 — conversion notes

A. Bondal and D. Orlov, *Semiorthogonal decomposition for algebraic
varieties*, arXiv:alg-geom/9506012v1 (19 June 1995).

## Source

The e-print is a tarball:

```bash
curl -sL -o bo.tar.gz https://arxiv.org/e-print/alg-geom/9506012
tar xzf bo.tar.gz   # pq1.tex (2176 lines) + 10 .eps figures
```

LaTeX 2.09: `\documentstyle[12pt]{article}` with `\input epsf`. Custom
theorem macro `\th{Type}\label{...} ... \eth` (34 instances:
Theorem/Lemma/Proposition/Definition) over a single per-section counter
THNO with `\theTHNO` = section.THNO and `\setcounter{section}{-1}`
(Introduction is section 0, so the first chapter's results are numbered
1.x — matches the official PDF). 23 ad-hoc `\pr` proof heads, 3 `eqnarray`
environments (fib, res, R), a `thebibliography` with 17 `\bibitem`s, and a
manual centered title block dated March 6, 1995.

## Changes

- Preamble modernization per the checklist (full list in `paper.json`).
- `\b` rename: `\def\b{\; \epsffile{k.eps}\;}` redefined the LaTeX accent
  `\b`, but the source never uses the accent form — all 13 uses are the
  macro as a boxtimes-like binary operator in math
  (`{\cal O}(-1)\b {\cal O}(-1)`), where k.eps (a 7x7pt xfig box) is the
  glyph. Renamed to `\diagk` (definition and all uses) and kept the figure,
  so the printed symbol is unchanged. `amssymb`'s `\boxtimes` was *not*
  substituted — that would change the glyph.
- Proof ends were curated individually: 14 of the 23 proofs are followed by
  body text that introduces the next result (e.g. the proof of Lemma isof
  ends before "Let $X, Y, Z$ be smooth projective varieties..."; the proof
  of Proposition flat ends with "This finishes the proof of theorem
  \ref{mai}." before the Mukai examples; the proof of Theorem efl ends
  before the `{\sc Remark.}`), so each `\end{proof}` was placed before that
  text rather than at the next `\th`. The proof at original line 1088
  (unlabeled lemma) runs through the rest of the Theorem qdq argument to
  "...then $Z$ is quasi-isomorphic to zero itself."
- Duplicate `\label{inv}`: Lemma inv (ch.1) and Definition inv (ch.4).
  The only `\ref{inv}` (line 674) means the lemma, so the definition's
  label became `invdef` with no ref repointed.
- `pagebackref` requires a blank line after every `\bibitem`
  (`\BR@@lbibitem[#1]#2#3\par` scans to the next `\par`; consecutive
  entries with no blank line fatal with "File ended while scanning").
  Blank lines added between entries — whitespace only. This generalizes
  the "blank-line separated bibitems" pattern already used by
  `alg-geom_9507012v2`/`0910.4460v2`; candidate for `docs/`.
- Proofreading scan (comment-stripped source: accent/delimiter/typo checks)
  found 5 textual typos, all fixed and recorded; repeated-word and
  paren-balance hits were all false positives (macros in arrays, citation
  keys, `\Bigl(`...`\Bigr)` split across `$$`). No mathematical errors
  found, so `warnings` is empty.

## Verification

- `latexmk -pdf` exits 0; zero `^!` lines; zero undefined
  refs/citations; zero `Token not allowed` warnings (no math in section
  titles). One cosmetic Underfull `\hbox` (badness 1838).
- All 10 EPS figures convert (`-eps-converted-to.pdf` in the log) and
  embed (figure pages 7, 9, 11, 12, 17, 23, 36, 39, 40, plus the k.eps
  symbol on p.36).
- 54 pages vs official PDF's 55 (1-page drift from T1/lmodern metrics and
  the pagebackref page lists).
- PDF outline: the 5 numbered sections with correct titles. Theorem/lemma/
  proposition/definition numbers extracted from both PDFs match exactly
  (35 heads, same numbers in order; the official PDF's "Definition" heads
  use a fi-ligature in the text layer, verified via `nition` count).
