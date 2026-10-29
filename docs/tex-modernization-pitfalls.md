# TeX modernization pitfalls

Symptom → cause → fix notes from converting old arXiv sources to current
TeX Live. For hyperref-specific traps see
[hyperref-and-bookmarks.md](./hyperref-and-bookmarks.md).

## Triage order

1. Download the source and identify the format: `file` the e-print. Old
   submissions are sometimes a single gzipped `.tex`, not a tarball.
2. Build once as-is to get the real error list, then modernize in small
   steps. Do not rewrite markup speculatively.
3. Keep the mathematics byte-identical. If a change is not cosmetic or
   structural, it does not belong in this repo.

## `\documentstyle` → `\documentclass`

LaTeX 2.09 sources start with

```tex
\documentstyle[12pt]{article}
```

Change it to

```tex
\documentclass[12pt]{article}
```

and add the packages the source actually needs. Most old sources need only
`amsmath`/`amssymb` plus `hyperref`; add more only when the log asks for
them.

`\documentstyle` also silently loaded packages that a modern preamble must
request explicitly. The first build after the change is where those surface.

## Package clashes

`amssymb` defines many symbols that old preambles also define by hand. The
build aborts with:

```text
! LaTeX Error: Command \boxtimes already defined.
```

Fix: keep the author's drawing if it matters, but change `\newcommand` to
`\renewcommand` (the package is loaded first):

```tex
\renewcommand{\boxtimes}{...}
```

Or delete the local definition and use the package symbol. Check whether the
author's version differs visually before deleting it.

## Fake section headings

Old sources often build headings by hand:

```tex
\newcommand{\numero}[1]{%
  \newpage
  \addtocounter{section}{1}
  \begin{center}{\Large \bf \thesection .\ #1}\end{center}
  \setcounter{subsection}{0}
  \setcounter{lemma}{0}\indent}
```

Replace the body with real structure:

```tex
\newcommand{\numero}[1]{\newpage\section{#1}}
```

Notes:

- Keep `\newpage` if the original forced one; `\section` alone does not start
  a new page in `article`.
- Drop manual `\addtocounter{section}` / `\setcounter{subsection}`: `\section`
  does both.
- Drop manual `\setcounter{lemma}{0}` **only if** the theorem environments are
  declared with `[section]`; then `\section` resets them. If they are not,
  preserve the reset explicitly.
- A `\label` placed right after the old macro now attaches to the section,
  which is what the hand-written table of contents wants.

For unnumbered subheads, use a starred section plus an explicit bookmark
anchor:

```tex
\newcommand{\subnumero}[1]{%
  \subsection*{#1}%
  \phantomsection
  \addcontentsline{toc}{subsection}{#1}}
```

If the paper has an unnumbered introduction that should still be in the
bookmarks, use `\section*{...}\phantomsection\addcontentsline{toc}{section}{...}`.

## Numbering

The goal is to preserve the numbering the published version uses. Check:

- section numbers (`1..N`) match the hand-written Sommaire;
- theorem/lemma numbers still match (`2.3`, `19.4`, ...);
- `\ref`/`\pageref` still resolve, with no `??`.

A useful check is to compare a theorem-heavy page against the official arXiv
PDF, not just the page count.

## `eqnarray*` → `align*`

`eqnarray` is deprecated and spaces relations badly. Convert

```tex
\begin{eqnarray*}
a &=& b\\
&=& c
\end{eqnarray*}
```

to

```tex
\begin{align*}
a &= b\\
&= c
\end{align*}
```

The relation spacing changes slightly; that is the point. Watch for
`& = &` variants and for `\stackrel` on the alignment point.

## Bibliography

- If the source has `thebibliography`, keep it; there is no `.bib` to
  reconstruct.
- If it has only `\bibitem`-free `\cite`s, reconstruct the bibliography and
  commit the resulting `.bbl` (see `math_0701269v2`).
- `pagebackref` adds a page list to every entry and therefore makes the
  bibliography longer. Page-count drift is expected.

## Hand-written tables of contents

Old papers often have a `Sommaire`/`Contents` built from `\pageref`:

```tex
{\bf 1. Introduction}---p. \pageref{intropage}
```

Do not replace it with `\tableofcontents` by default: the blurbs are the
author's text. Keep the block; modernizing the headings is enough for the
page references to keep working. The numbers will follow the new pagination.

## Page-count drift and verification

A modernized build rarely matches the official PDF page-for-page. Check:

```bash
pdfinfo official.pdf | grep Pages
pdfinfo math_9807049v3.pdf | grep Pages
```

A drift of a few pages is normal after class/heading/hyperref changes. A
large drift usually means a `\newpage` was dropped, a heading became
numbered/unnumbered, or the bibliography grew.

Visual spot checks are cheap:

```bash
pdftoppm -f 4 -l 4 -r 70 -png math_9807049v3.pdf ours
pdftoppm -f 4 -l 4 -r 70 -png official.pdf official
```

## Encoding and fonts

The old sources are usually pure ASCII with TeX accents (`\'e`, `\c{c}`), so
UTF-8 handling is not an issue. If you add non-ASCII text (e.g. in
`\texorpdfstring`), the file is UTF-8 and modern pdfLaTeX reads it by
default.

This repo uses `\usepackage[T1]{fontenc}` and `\usepackage{lmodern}` by
default (approved 2026-10-29), loaded before `hyperref`. T1 gives correct
text extraction (`é`, not `´e`); `lmodern` gives scalable Type 1 fonts.
Expect metrics and pagination to change from an OT1 build, so re-check the
page count and spot-check a few pages.

## Proofreading scans

Old sources carry accent and delimiter slips that a successful build will not
catch. A second pass is cheap; run it on the comment-stripped source.

- **Accent macros.** `\'a` (á) is almost always a typo for `` \`a `` (à) in
  French; `cot\'e` is usually `c\^ot\'e`; `l'epoque` → `l'\'epoque`;
  `necessaire` → `n\'ecessaire`; `clot\^ure` → `cl\^oture`.
- **Apostrophes.** `qu' on`, `d' un`, `l' \'el\'ement` are spacing typos;
  French has no space after the apostrophe.
- **Repeated words.** Strip comments and `\cite`/`\ref` arguments first, or
  citation keys look like repeated words.
- **Delimiters.** Count `(`/`)` per math segment. Half-open intervals such as
  `[0,\infty)` legitimately close with `)`, so filter those out; an extra
  `)` in `A(Y_j,g_j))` or a missing one in `deg(y_{i+1}` is real.
- **Punctuation.** `,,`, `..`, `;;`, and `etc` without a period.
- **Bibliography.** Duplicate keys/titles, and missing accents in French
  titles.

Do not “fix” notation or claims. A consistent oddity (for example
`Cpx^{[0,a\}}`) is a notation question, not a typo; record it and leave it.

## Title blocks and dates

- Keep a manual title block if the paper has one; do not invent a
  `\maketitle` layout that the authors did not use.
- Never use `\today` in a title. If the class prints a date, pin it to the
  arXiv date of the pinned version (see `AGENTS.md`).
- Set PDF metadata even when the visible title block is manual:
  `\hypersetup{pdftitle=...,pdfauthor=...}`.
