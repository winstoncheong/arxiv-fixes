# MEMORIES

Durable, curated memory for this repo: the lessons that are worth not
rediscovering. This is not a diary and not a duplicate of `plan.html` or
`AGENTS.md`. Start with [`AGENTS.md`](./AGENTS.md) for the operating rules
and [`plan.html`](./plan.html) for the architecture; this file is the memory
behind them.

Where things go:

- **`MEMORIES.md`** (this file) — short, cross-paper lessons and decisions.
  One line per lesson, with a pointer to the detail.
- **`docs/`** — long-form, cross-cutting notes (techniques, pitfalls,
  tooling). See [`docs/README.md`](./docs/README.md).
- **`<paper>/readme.md`** — paper-specific conversion log and remaining
  defects (e.g. [`hep-th_9408074v2/readme.md`](./hep-th_9408074v2/readme.md),
  [`math_9807049v3/readme.md`](./math_9807049v3/readme.md)).

Keep this file short. If an entry grows into a procedure, move the detail to
`docs/` and leave a pointer here.

## Invariants

- **Never change the mathematics.** Fixes are cosmetic and structural only.
- **Pin the version.** The directory name carries the arXiv version
  (`math_9807049v3`); do not silently track a newer one.
- **Canonical entry point.** `<dirname>.tex` at the directory root; adjust
  `\include`/`\input` stems, never content.
- **PDFs are build products.** CI builds them; never `git add` a PDF. A local
  PDF is fine in the working tree (it is ignored).
- **The index is generated.** Edit `paper.json`, then run
  `scripts/generate_index.py`; never hand-edit `index.md`/`index.html`.
- **Success bar:** exit 0, zero `^!` lines in the log, zero undefined
  references/citations after reruns, and no `Token not allowed in a PDF
  string` warnings.

## Recurring pitfalls

- **LaTeX 2.09 sources** usually need only `\documentstyle` →
  `\documentclass`, but the first build exposes package clashes (see next
  item). Detail: [`docs/tex-modernization-pitfalls.md`](./docs/tex-modernization-pitfalls.md).
- **`amssymb` already defines symbols** such as `\boxtimes`. An author
  `\newcommand` for the same name aborts the build; use `\renewcommand`
  (or drop the local definition).
- **Fake section macros** (`\numero`, `\subnumero`, `\noindent{\it ...}`)
  become real `\section`/`\subsection*` structure so bookmarks work. Keep the
  numbering scheme: if the old macro did `\addtocounter{section}` plus
  `\setcounter{lemma}{0}`, plain `\section` already does both when theorems
  are declared `[section]`.
- **Starred subheads need an anchor** for bookmarks:
  `\subsection*{#1}\phantomsection\addcontentsline{toc}{subsection}{#1}`.
- **Math in a heading breaks PDF strings.** Wrap it:
  `\texorpdfstring{$n$}{n}`. The second argument is a PDF string, so escape
  `_` as `\_` and replace symbols with words (`∞` → `infini`, `∅` →
  `l'ensemble vide`). Detail:
  [`docs/hyperref-and-bookmarks.md`](./docs/hyperref-and-bookmarks.md).
- **A hand-written Sommaire survives** modernization if its `\pageref`
  labels sit after the new `\section`; page numbers follow the new
  pagination. Do not replace it with `\tableofcontents` unless dropping the
  author's descriptive blurbs is acceptable.
- **`eqnarray*` → `align*`:** rewrite `&=&` as `&=`; alignment spacing
  changes slightly.
- **`pagebackref` lengthens the bibliography** (each entry gains a page
  list), so total page count can grow even when the body shrinks. Compare
  against the official arXiv PDF and expect a few pages of drift.
- **Old arXiv e-prints may be a single gzipped `.tex`**, not a tarball. Run
  `file` on the download before extracting.
- **T1 + `lmodern` are the default** (approved 2026-10-29): add
  `\usepackage[T1]{fontenc}` and `\usepackage{lmodern}` before `hyperref`.
  Text extraction becomes correct (`é`, not `´e`) and fonts are scalable;
  metrics and pagination change, so re-check the page count.
- **Old sources carry accent and delimiter typos** that compile fine:
  `\'a` for `` \`a ``, `cot\'e` for `c\^ot\'e`, spaces after apostrophes,
  unmatched parentheses. Run a comment-stripped proofreading scan; see
  [`docs/tex-modernization-pitfalls.md`](./docs/tex-modernization-pitfalls.md).

## Per-paper notes

- `math/9807049v3` — Hirschowitz–Simpson, *Descente pour les n-champs*.
  Fake `\numero`/`\subnumero` headings, one `eqnarray*`, `\boxtimes` clash.
  Conversion log: [`math_9807049v3/readme.md`](./math_9807049v3/readme.md).
- `hep-th/9408074v2` — Vafa–Witten, plain TeX/harvmac. Script-assisted
  conversion; lossy in places. Log:
  [`hep-th_9408074v2/readme.md`](./hep-th_9408074v2/readme.md).
- `0905.0462v2` — Lurie, `(∞,2)`-categories I. `xr-hyper` plus committed
  companion `.aux` snapshots; draft material after `\end{document}` kept.
  See `paper.json` and `AGENTS.md`.
- `1110.0466v3` — outdated `JHEP3` class replaced by `jheppub`; shared style
  file declared in `common/`. See `paper.json`.

## Tooling

- Build: `cd <paper-dir> && latexmk -pdf -interaction=nonstopmode <dir>.tex`.
- Log triage: `grep -c '^!'`, `grep -i undefined`, `grep 'Token not allowed'`.
- Compare with the official PDF: `curl -L -o official.pdf
  https://arxiv.org/pdf/<id>` then `pdfinfo` (page count) and `pdftoppm`
  (visual spot checks). `PyMuPDF` (`fitz`) is handy for outlines and spans.
- Source check: `curl -L -o src
  https://arxiv.org/e-print/<id>`; `file src` before unpacking.

## Open questions

- Retrofit T1 + `lmodern` to the older entries when they are next touched;
  the default applies to new and touched entries.
- Bookmark policy: sections only, or sections + unnumbered subheads? Current
  practice is both where the paper has a deep structure.
- How much of a hand-written table of contents should be preserved when a
  real `\tableofcontents` would be cleaner?

## Adding to this file

- Paper-specific discovery → `<paper>/readme.md`.
- Cross-cutting discovery → `docs/<topic>.md`, plus one line here.
- If a line here becomes a procedure, move the procedure to `docs/`.
