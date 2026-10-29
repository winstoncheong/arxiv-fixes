# Plain TeX and harvmac sources

Some old high-energy papers are plain TeX with the `harvmac` macro package,
not LaTeX. Converting them is close to a rewrite of the markup, so treat it
as a separate workflow from the LaTeX modernizations.

The reference conversion in this repo is
[`hep-th_9408074v2`](../hep-th_9408074v2/readme.md) (Vafa–Witten). Read that
log before starting another one.

## What harvmac does

- `\nref\label{...}` defines a bibliography entry **without** citing it.
- `\ref\label{...}` defines an entry **and** cites it.
- `\eqn\eqlabel{...}` defines an equation and a label; it is roughly
  `\begin{equation}\label{eqlabel}...\end{equation}` plus `\eqref`.
- `\newsec{...}` / `\subsec{...}` are the sectioning commands, not
  `\section` / `\subsection`.
- Headings are often faked with `\noindent{\it ...}` or `\centerline`.

## Conversion strategy

1. Keep the original file and work on a copy. A script is fine, but the
   output is a draft, not a deliverable.
2. Map the structural macros to real LaTeX structure first
   (`\newsec` → `\section`, `\subsec` → `\subsection`, fake headings →
   `\section*` or `\section`).
3. Reconstruct the bibliography from the `\nref`/`\ref`/`\refs` commands.
   Ordering in the source appears to be citation order, so the numbering can
   differ from the arXiv/preprint version. Record the shift.
4. Fix duplicate labels and missing entries by hand. The automated pass
   cannot tell a genuine duplicate from a distinct result with the same
   label.
5. Delete the conversion script and intermediate files before marking the
   entry done; keep the lasting notes in `<paper>/readme.md`.

## Known failure modes

- **Duplicate labels.** Multiple `\eqn\defk{...}` definitions produce
  “Label `defk' multiply defined” and the wrong equation is referenced.
- **Missing bibliography entries.** A `\nref\switten` that repeats an
  earlier `\ref\switten` is dropped as a duplicate; if the first occurrence
  was not the intended entry, the bibliography is one item short and later
  numbers shift.
- **Heading style drift.** Harvmac headings do not look like LaTeX headings;
  the PDF will not match the published layout.
- **Numbering drift.** Bibliography order and equation numbers can differ
  from the published version. Document it; do not silently renumber.
- **Lossy math.** Plain-TeX idioms (`\over`, `\matrix`, `\cases`,
  `\eqalign`) need hand conversion; check the output, do not trust the
  script.

## Verification

- Compare the bibliography against the published PDF entry by entry when the
  conversion touched it.
- Grep the log for multiply-defined labels and undefined citations.
- Spot-check equation-heavy pages against the official PDF.
- Keep the paper's `readme.md` honest about what is still lossy; the index
  surfaces it as a warning.
