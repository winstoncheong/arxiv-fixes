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
  `\input amssymb.sty` → `\usepackage{amsmath,amssymb,graphicx}`; dropped
  `\input epsf` (covered by `graphicx`). Kept the manual page geometry
  (`\textheight` etc.) and the `titlepage`-env title block as-is.
- Converted the three plain-TeX `\matrix{...\cr}` blocks (lines 3221, 4196,
  5201) to `\begin{matrix}` environments with `\` separators. Required:
  `amsmath` rejects the old form. `\cr` occurred only inside these three
  blocks (11 uses), so the conversion is contained.
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

Deliberately left as-is (documented here rather than changed):

- The 66 ad-hoc `{\bf Proof}.` paragraphs: the source has no QED markers, so
  proof ends cannot be determined without editorial judgement. Converting to
  `amsthm` `proof` environments would reformat 66 passages by guesswork
  (`amsthm` is therefore not loaded).
- Plain-TeX `\choose` (17 active uses plus 2 in comments): identical output
  under `amsmath`, one compat warning (`Foreign command \atopwithdelims`).
  Restructuring 17 instances into `\binom` buys nothing rendered.
- `\Bbb` (obsolete, kept): renders correctly with one `amsfonts` warning per
  build; replacing it throughout would touch every blackboard-bold symbol for
  no visible change.

## Duplicate labels (preserved, not fixed)

Four labels are defined twice in the source. `\ref` resolves to the last
definition, so three references print the wrong number. Per the errata rules
these stay as the author wrote them:

| label | first use | second use | affected ref | intended target |
| --- | --- | --- | --- | --- |
| `1.1.01.1` | equation `h_F` (l. 3316) | proposition (l. 5533) | lemma l. 3321 ("the Hopf algebra map ... is injective") shows the *proposition* number | the equation just above it |
| `12.1.00.2` | proposition (l. 1231) | lemma (l. 1248) | none (no `\ref` to it; log warning only) | — |
| `2**` | `I(a_0;...)` definition (l. 798) | regularized integral (l. 1602) | lemma 2.9 (l. 2148) shows the l. 1602 number | the l. 798 definition |
| `4.22.01.1` | differential equation (l. 4483) | lemma (l. 4680) | proof l. 4694 ("satisfies the differential equation ...") shows the *lemma* number | the equation |

## Verification

```bash
cd math_0103059v4
latexmk -pdf -interaction=nonstopmode math_0103059v4.tex
grep -c '^!' math_0103059v4.log                  # 0
grep -ci undefined math_0103059v4.log            # 0
grep -c 'Token not allowed' math_0103059v4.log   # 0
pdfinfo math_0103059v4.pdf | grep Pages          # 82
```

The log's only content warnings are the 4 multiply-defined labels above (plus
the benign `amsfonts` `\Bbb` and `amsmath` `\choose` compat notes).

The official arXiv PDF has 82 pages and no bookmarks; this build has 82 pages
with an 8-entry outline (7 sections + REFERENCES). Spot-checked against the
official PDF: title page (title, author, pinned date, dedication, Contents),
a theorem-heavy page in section 2, the Hopf-algebra formula pages, and the
last bibliography page. All 13 EPS figures convert and embed
(`-eps-converted-to.pdf` in the build log).

## Known differences

- The title page now prints `May 15, 2001` (source had an empty date).
- Section TOC/outline page numbers run +1/+2 ahead of the official PDF (date
  line plus T1/lmodern metrics); the total is 82 pages either way.
- `REFERENCES` appears in the TOC and bookmarks (new entry, no number).
- Accented French/German in the bibliography now renders with proper glyphs
  (e.g. Über, Résolution, réguliers); text extraction is clean T1.

See [`../MEMORIES.md`](../MEMORIES.md) and
[`../docs/tex-modernization-pitfalls.md`](../docs/tex-modernization-pitfalls.md)
for the general lessons from this conversion.
