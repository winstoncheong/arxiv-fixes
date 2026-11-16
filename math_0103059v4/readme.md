# math/0103059v4 — conversion notes

A. B. Goncharov, *Multiple polylogarithms and mixed Tate motives*,
arXiv:math/0103059v4 (15 May 2001).

## Source

The e-print is a tarball:

```bash
curl -sL -o src https://arxiv.org/e-print/math/0103059
tar xzf src   # mp.tex + 13 .eps figures
```

LaTeX 2.09: `\documentstyle[10pt]{article}` with `\input amssymb.sty` and
`\input epsf`. Seven real `\section`s plus `\tableofcontents`; 198 `equation`
environments; 284 `\label`s; no `\cite` (citations are manual bracket keys
like [G0-5], bibliography is a 55-item `itemize` list, so there is no `.bbl`
to reconstruct). Proofs are ad-hoc `{\bf Proof}.` paragraphs. Figures are
13 EPS files included with `\epsffile`.

## Changes

- `\documentstyle[10pt]{article}` → `\documentclass[10pt]{article}`;
  `\input amssymb.sty` → `\usepackage{amsmath,amssymb,amsthm,graphicx}`; dropped
  `\input epsf` (covered by `graphicx`). Kept the manual page geometry
  (`\textheight` etc.) and the `titlepage`-env title block as-is.
- Converted the three plain-TeX `\matrix{...\cr}` blocks (lines 3221, 4196,
  5201) to `\begin{matrix}` environments with `\` separators. Required:
  `amsmath` rejects the old form. `\cr` occurred only inside these three
  blocks (11 uses), so the conversion is contained.
- Converted plain-TeX `\choose` (16 uses) to `\binom` (identical output; removes the `amsmath` compat warning; 2 uses in comments left alone).
- Converted all 13 `\epsffile{...}` inclusions to `\includegraphics{...}`
  (`epsf` specials do not embed under `pdflatex`; `epstopdf` converts
  automatically under `latexmk -pdf`).
- Added `\usepackage[T1]{fontenc}` and `\usepackage{lmodern}` (the approved
  default), then `hyperref` with color links, bookmarks, and `pagebackref`,
  plus `\hypersetup{pdftitle=...,pdfauthor=...}`. `hyperref` loads last.
- Wrapped `$S$` in the section-3 title with `\texorpdfstring{$S$}{S}` (the
  only math in any section title; zero `Token not allowed` warnings).
- Promoted the manual `REFERENCES` head to
  `\section*{REFERENCES}\phantomsection\addcontentsline{toc}{section}{REFERENCES}`,
  so the bibliography gets a bookmark and a TOC entry without changing
  numbering.
- Pinned the title date to the v4 arXiv date (`\date{May 15, 2001}`) instead
  of the empty `\date{}`.
- Converted all 75 ad-hoc proof heads to `amsthm` `proof` environments, closing each at the next section, theorem-like environment, or bold head. The six `First/Second/Third proof` variants and three `Proof of ...` heads use the optional argument (qualifier in parentheses). The one proof whose run contains its supporting lemma (the second proof of the theorem) keeps the lemma inside the proof environment. Two proofs end exactly at section boundaries; none spans a section (verified by segmenting all runs).
- Replaced obsolete `\Bbb` with `\mathbb` (57 active uses; 3 uses inside `%` comments left alone).
- Fixed the four duplicate labels by renaming the less-referenced side (`1.1.01.1-eq`, `12.1.00.2lem`, `2**reg`, `4.22.01.1lem`) and repointing the one affected `\ref`; every other ref already meant the kept definition, so all three previously-wrong reference numbers now print correctly.

## Proofreading pass

Fixed under the typo/errata rules in `AGENTS.md` (fixes in `paper.json`,
unfixed issues in `warnings` here and there):

- Text: `filed` → `field` (twice, section 3, "arbitrary filed $F$").
- Bibliography:
  - `[D]` Deligne title: `Le group fondamental ... moine trois points` →
    `Le groupe fondamental ... moins trois points` (the well-known MSRI 16
    title).
  - `[Ku]` Kummer title: `Uber die Transcendeten` → `\"Uber die Transcendenten`
    (verified against the Crelle 1840 record, doi:10.1515/crll.1840.21.74).
  - `[LD]`: `Resolution` → `R\'esolution`, ``probl\`em es`` → ``probl\`emes``,
    `reguliers` → `r\'eguliers`, `Poincare` → `Poincar\'e`.
  - `[Kr]`: `Renotmalisation` → `Renormalisation`.
  - `[Dr]`: `clousely` → `closely`.
  - `[W1]`, `[W2]`: `Woitkowiyak` → `Wojtkowiak` (verified: the DOI records
    for the Lewin volume and the Durham proceedings both read
    Zdzisław Wojtkowiak).
  - `[HM]`: `Matsumoto M..:` → `Matsumoto M.:`; `[Sh]`: `Shiho, A.:.` →
    `Shiho, A.:` (doubled periods).
- Scans run over comment-stripped prose: repeated words, doubled punctuation,
  apostrophe spacing, and a common-typo list — all clean otherwise.

## Duplicate labels (fixed, with owner approval)

Four labels are defined twice in the source. `\ref` resolves to the last
definition, so three references printed the wrong number. With the owner's approval these are now fixed by renaming the less-referenced side:


| label | collision | resolution |
| --- | --- | --- |
| `1.1.01.1` | equation `h_F` (l. 3319) vs proposition (l. 5536); lemma l. 3324 printed the proposition's number | equation renamed `1.1.01.1-eq` and its ref repointed; now prints the equation number |
| `12.1.00.2` | proposition (l. 1234) vs lemma (l. 1251); no refs | lemma renamed `12.1.00.2lem` |
| `2**` | `I(a_0;...)` definition (l. 801) vs regularized integral (l. 1605); lemma 2.9 (l. 2151) printed the wrong number | integral renamed `2**reg`; now prints the definition's number |
| `4.22.01.1` | differential equation (l. 4486) vs lemma (l. 4683); proof l. 4697 printed the lemma's number | lemma renamed `4.22.01.1lem`; now prints the equation's number |

## Verification

```bash
cd math_0103059v4
latexmk -pdf -interaction=nonstopmode math_0103059v4.tex
grep -c '^!' math_0103059v4.log                  # 0
grep -ci undefined math_0103059v4.log            # 0
grep -c 'Token not allowed' math_0103059v4.log   # 0
pdfinfo math_0103059v4.pdf | grep Pages          # 85
```

The log's only content warnings are the 4 multiply-defined labels above (plus
The log is fully clean: zero errors, zero undefined refs, zero `Token not allowed` warnings, zero multiply-defined labels, and none of the old `amsfonts`/`amsmath` compat notes.

The official arXiv PDF has 82 pages and no bookmarks; this build has 85 pages
with an 8-entry outline (7 sections + REFERENCES). Spot-checked against the
official PDF: title page (title, author, pinned date, dedication, Contents),
a theorem-heavy page in section 2, the Hopf-algebra formula pages, and the
last bibliography page. All 13 EPS figures convert and embed
(`-eps-converted-to.pdf` in the build log).

## Known differences

- The title page now prints `May 15, 2001` (source had an empty date).
- Section TOC/outline page numbers run +1/+2 ahead of the official PDF (date
  line, T1/lmodern metrics, plus `amsthm` proof spacing and QED boxes); the total is 85 pages vs 82 official.
- `REFERENCES` appears in the TOC and bookmarks (new entry, no number).
- Accented French/German in the bibliography now renders with proper glyphs
  (e.g. Über, Résolution, réguliers); text extraction is clean T1.

See [`../MEMORY.md`](../MEMORY.md) and
[`../docs/tex-modernization-pitfalls.md`](../docs/tex-modernization-pitfalls.md)
for the general lessons from this conversion.
