# hep-th/9408074v2 — conversion notes

Cumrun Vafa and Edward Witten, *A Strong Coupling Test of S-Duality*,
arXiv:hep-th/9408074v2 (1 September 1994).

## Source

The e-print is plain TeX using the `harvmac` macros (`\input harvmac`,
`\newsec`, `\subsec`, `\eqn\label{...}`, `\nref`/`\ref` bibliography
commands, `\over`, `\pmatrix`, `\eqalign`, `\cr`). No figures were
shipped and none are referenced (the `\fig` macro is defined but never
used); the official PDF has no images either.

## Conversion

The original `hep-th_9408074v2.tex` (plain TeX) is preserved in git
history. Conversion ran in two stages:

1. `convert.py` (work log, removed) mapped the harvmac constructs to
   LaTeX over the extracted `body.tex`: `\newsec`/`\subsec` →
   `\section`/`\subsection`, `\eqn\lbl{...}` → `equation` + `\label`,
   `\nref`/`\ref`/`\refs` → `thebibliography` + `\cite`, `\pmatrix` /
   `\eqalign` / `{... \over ...}` / `\cr` → `amsmath` environments,
   `\foot` → `\footnote`, plus the one-off `\semi` → `;\` fix.
   Output went to `converted.tex` (intermediate, removed).
2. Manual consolidation: the generated body was proofread and fixed
   (see below), then merged with a cleaned `main.tex` preamble into
   the single canonical entry point `hep-th_9408074v2.tex`. All
   helpers and intermediates (`convert.py`, `body.tex`,
   `converted.tex`, `main.tex`) were removed; the entry point is
   self-contained.

## Changes

- Single self-contained entry point `hep-th_9408074v2.tex`
  (preamble + body + `thebibliography`); two engine paths collapsed
  to plain `latexmk -pdf`.
- Preamble trimmed to what the document uses (`amsmath`, `amssymb`,
  `cite`, `geometry`, `setspace` for `\singlespacing`); dropped
  `graphicx`, `authblk`, `mathtools`, `amsthm`, `amsfonts` (all
  unused — no figures, manual title block, no proof environments).
- Added `T1` fontenc and `lmodern` (the approved default), plus
  `hyperref` with color links, bookmarks, and `pagebackref`, with
  PDF title/author metadata. The manual title page is kept as-is,
  including its printed `September, 1994` date.
- Fake heading `\noindent{\it{Generalization}}` → `\subsection*`
  with a bookmark/TOC entry (numbering unchanged).
- Math in section titles wrapped in `\texorpdfstring`
  (`$S$`, `$N=4$`, `$K3$`, `${\bf CP}^2$`, `$N=1$`); zero `Token
  not allowed` warnings.
- Kept `\numberwithin{equation}{section}`: matches the official
  PDF's `(1.1)` numbering.
- Bibliography: the two `\switten` definitions shared one key, so
  the script merged them and dropped the second text. Split back
  into two entries — `switten` (line-451 text = official [35]) and
  `switten58` (line-3814 text = official [58]) — and repointed the
  14 later `\cite{switten}` uses to `switten58`; the defining use
  (Donaldson-theory sentence) keeps `[35]`. Verified against the
  official PDF's citation contexts.
- Proofreading pass over comment-stripped prose: no textual typos,
  doubled punctuation, or spacing slips found.

Deliberately left as-is: the hand-written centered title block
(instead of `\maketitle`); the `\def\tilde`/`\def\bar` aliases;
`{\Bbb P}`-style blackboard bold (renders fine).

## Verification

```bash
cd hep-th_9408074v2
latexmk -pdf -interaction=nonstopmode hep-th_9408074v2.tex
grep -c '^!' hep-th_9408074v2.log                  # 0
grep -ci undefined hep-th_9408074v2.log            # 0
grep -c 'Token not allowed' hep-th_9408074v2.log   # 0
grep -c 'multiply defined' hep-th_9408074v2.log    # 0
pdfinfo hep-th_9408074v2.pdf | grep Pages          # 78
```

The official arXiv PDF has 100 pages and no bookmarks; this build has
78 pages with a 25-entry outline (7 sections + 18 subheads). The text
is complete (35,723 vs 35,869 words extracted; the gap is hyphenation
artifacts). Spot-checked against the official PDF: title page, the
`(1.1)` equation, a theorem-heavy page, and the bibliography
(`[35]`/`[58]` now distinct with correct texts).

## Known differences

- 78 vs 100 pages: the `article` layout is denser than harvmac's;
  content is identical (see word counts above).
- One benign `pdfTeX warning (ext4)`: the titlepage environment
  ships out two logical page 1s (`duplicate ignored`); no visible
  effect.
- `REFERENCES`-style hand TOC: none in the original; the PDF
  outline comes from the real sectioning.

See [`../MEMORY.md`](../MEMORY.md) and
[`../docs/tex-modernization-pitfalls.md`](../docs/tex-modernization-pitfalls.md)
for the general lessons from this conversion.
