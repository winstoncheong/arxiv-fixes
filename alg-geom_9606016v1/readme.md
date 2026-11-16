# alg-geom/9606016v1 — Cox, *Recent developments in toric geometry*

Survey (50 pages AMSTeX 2.1 in the arXiv comment) for the 1995 Santa Cruz
Summer Institute proceedings. Single gzipped `.tex` source, AMSTeX `amsppt`
markup throughout: `\input amstex` + `\documentstyle{amsppt}`, `\topmatter`,
`\head`/`\subhead`, `\proclaim`/`\demo`, `\roster`, `\Refs`, `$$` displays
with manual `\tag`s, 149-entry bibliography, 321 citations.

## AMSTeX → amsart mapping

- Preamble follows the `hep-th/9402147` + `hep-th/9405035` precedent (both
  were also `\input amstex` + `\documentstyle{amsppt}` → `amsart`): old
  `\input`/`\documentstyle`/`\NoBlackBoxes` lines kept as comments,
  `amssymb`/`amsthm` + T1/`lmodern` + `hyperref` (color links, pagebackref).
- `\head \S1. Title\endhead` → `\section{Title}` — the `\S1.` prefixes are
  author-side manual numbering, stripped so LaTeX numbers sections 1–11
  identically. `Introduction`/`Conclusion` → `\section*` (unnumbered, as in
  the original); amsart lists starred sections in the TOC on its own, so no
  manual `\addcontentsline` (an early draft had both and produced duplicate
  TOC lines).
- Added `\tableofcontents`; the original has no TOC. Recorded in
  `paper.json`.
- `\proclaim{Theorem 2.1}` etc. → numbered `theorem`/`proposition`/`lemma`/
  `conjecture` sharing one `[section]` counter — the 23 original numbers
  (2.1 through 9.3, sequential within each section) come out identical.
  `\demo{Proof}` → `proof`; `\demo{Example(s)}` → `example`;
  `\demo{Remarks...}` → `remark`. The two manual `\qed`s sit in example
  environments (no auto-QED there) and were kept.
- `\roster` → `itemize` (both the `"{$\bullet$}"` and bare-`\item` variants).
- Displays: 135 `$$` spans → `\[...\]`, or `\begin{equation}` keeping the
  manual `\tag` verbatim plus an added `\label{eq:...}` (44 tagged, all
  unique); `\thetag{X}` → `\eqref{eq:X}` (42 uses; 8.3/8.4 are tagged but
  never referenced, as in the source). `\align` → `align*` (5, one with
  `\intertext`), `\aligned` → `aligned` (3), `\cases` → `cases` (1).
- Font switches expanded: `{\Bbb X}` (with and without space, sometimes
  split across lines) → `\mathbb`, `\Cal` → `\mathcal`, `\bold` →
  `\mathbf`, `{\frak g}` → `\mathfrak`, `\roman` → `\mathrm`,
  `{\hbox{\smc lt}}` (also split across lines) → `\text{\textsc{lt}}`.
- Four `$\mathcal{A}$-…` subsection titles wrapped in `\texorpdfstring`.

## Bibliography notes

- `\Refs` → `thebibliography` with `\bibitem[KEY]{KEY}` alpha labels (the
  `hep-th/9402147` pattern), so `\cite{Ful}` still prints `[Ful]`.
  `\bysame` → em dash; the Hu entry's `\moreref` became an Erratum note.
- Citation ranges split: `BB1--3`, `BB2-3`, `Mor1--3`, `Mor2-3`, `HLY1-2`;
  `{\\rm, …}` note text moved outside the `\cite`.
- Three key problems, all judgement calls (see `paper.json` `changes`):
  `GKZ` → `GKZ1` (the four uses all cite book chapters of the GKZ book);
  `KMMS` → `KKMS` (transposed letters of the toroidal-embeddings entry,
  cited next to AMRT in a torus-embeddings sentence); `GMS` had no entry at
  all, so a new one was supplied (Greene–Morrison–Strominger, *Black hole
  condensation and the unification of string vacua*, Nucl. Phys. B451
  (1995) 109–120) — the conifold/black-hole-condensation context matches
  exactly.
- Key `W\l o` renamed to ASCII `Wlo` (a control sequence in a citation key
  breaks `\bibcite`); the printed label stays `[W\l o]`.
- Entry `SI` has no `\by` in the source; left authorless (guessing felt
  wrong — see `warnings`).
- Bibliography typos fixed: `Torodial` → `Toroidal` (KKMS), `integerals` →
  `integrals` (GKZ2), `homogenous` → `homogeneous` (Alt2).

## Verification

- `latexmk -pdf`: exit 0; zero `^!` lines; zero undefined citations/refs;
  zero `Token not allowed` warnings.
- 49 pages vs 48 for the official arXiv PDF (pagebackref lengthens the
  bibliography; expected drift).
- Outline: 14 top-level (11 sections + Introduction + Conclusion +
  References, the last auto-added by amsart) + 51 subsections, no
  duplicates; math subsheads read cleanly.
- 150 `\bibitem`s (149 source + GMS); 321 `\cite`s all resolve, none
  orphaned either direction; 44 equation labels, 42 `\eqref`s.
- Known cosmetic wart: hyperref emits duplicate-`equation.1`-destination
  warnings for the manual `\tag`s; the `\eqref` targets themselves are
  distinct (`AMS.1`…`AMS.44` in the `.aux`), so links land correctly.
