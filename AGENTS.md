# AGENTS.md — arxiv-fixes repo guide

Branch: `master`. This repo keeps nontrivial fixes to arXiv sources so each
paper compiles under stock TeX Live with working bookmarks, colored
hyperlinks, and readable diagrams. Fixes are cosmetic/structural only:
never change the mathematics. Design authority is `plan.html`
(§1 goal/non-goals, §2 layout, §3 "fixed" checklist, §4 git tracking,
§5 CI design, §6 index contract, §7 cleanup queue). Durable cross-paper
lessons live in `MEMORIES.md`, with detail in `docs/`; paper-specific logs
live in `<paper>/readme.md`.

## Directory layout (plan.html §2)

- One directory per paper: arXiv id with `/` → `_`, version appended.
  E.g. `0910.4460v2/`, `alg-geom_9507012v2/`, `hep-th_9402147v2/`.
- Canonical entry point: `<dirname>.tex` at the directory root.
  Grandfathered exceptions (don't replicate): `1110.0466v3/dilognotes.tex`,
  `math_0701269v2/6-1-07cmplx4.tex`, and `hep-th_9408074v2/` (two entry
  points plus `convert.py`/`body.tex`/`converted.tex` pending consolidation).
- Beside the entry point live only real inputs: `\include`d/`\input` `.tex`
  files, figures (`.eps`/etc.), a committed `.bbl` when upstream `.bib` is
  absent (e.g. `math_0701269v2/bibcmplx.bbl`), and `readme.md` for lasting
  conversion notes (e.g. `hep-th_9408074v2/readme.md`,
  `math_9807049v3/readme.md`).
- Conversion helpers and intermediates (`convert.py`, `body.tex`,
  `converted.tex`) are work logs, not deliverables: remove before marking
  an entry done.
- `common/` holds shared TeX inputs TeX Live doesn't ship (currently just
  `jheppub.sty`). A paper declares what it needs via the `"common"` list in
  its `paper.json`; CI copies those files into the paper dir before building.
  Local builds: `cp common/<file> <paper-dir>/` by hand.

## `paper.json` (source of truth for the index)

Required: `arxiv`, `title`, `entries` (non-empty list of `{"tex", "pdf"}`
plus optional `"engine"`). Optional: `authors`, `abstract`, `status`,
`changes`, `warnings`, `common`. Examples:

- Minimal canonical: `0910.4460v2/paper.json`.
- `"common": ["jheppub.sty"]`: `1110.0466v3/paper.json`.
- `"engine": "pdftex"` entry (plain-TeX/harvmac): `hep-th_9408074v2`.
- Figure-heavy with `.bbl` + `.eps`: `math_0701269v2`.
- Committed xr `.aux` snapshots with per-dir `.gitignore` negations:
  `0905.0462v2/` (see below).

`status` vocabulary in use: `done`, `done; non-canonical entry-point stem
grandfathered`, `builds locally; first CI candidate`, `in conversion; ...`.

## The "fixed" checklist (plan.html §3)

Converge every entry on this list; record each change plus any known
remaining defect in `paper.json` (`changes`/`warnings`, surfaced in the index):

1. `documentstyle` → `documentclass`; compiles under current TeX Live.
2. Fake headings (`\noindent{\it ...}`, `\centerline`) → real `\section`
   structure so TOC/bookmarks work. Keep an intentionally-unnumbered intro
   as `\section*` + `\phantomsection\addcontentsline{toc}{section}{...`
   (numbering unchanged); see `0905.0462v2/bicategories.tex`.
3. `hyperref` with color links + back refs, e.g.
   `\usepackage[colorlinks,allcolors=blue,pagebackref]{hyperref}` (load last).
   With `xr`'s `\externaldocument`, use `xr-hyper`, not `xr`.
4. `eqnarray*` → `align*`; ad-hoc proof envs → `proof` (amsthm).
5. Broken diagrams → `tikz-cd` first, general `tikz` fallback; fix picture
   overlaps/obscured labels. Working `xypic` diagrams stay as-is.
6. Missing bibliography reconstructed and committed as `.bbl`.
7. Math in section titles wrapped in `\texorpdfstring{...}{ascii}` so PDF
   bookmarks are clean. Escape `_` as `\_` in the second argument; see
   `docs/hyperref-and-bookmarks.md`.
8. Pin the title date to the arXiv date of the pinned version (e.g.
   `\date{May 8, 2009}` for `0905.0462v2`), never `\today` — a build date
   makes every CI rebuild produce a different PDF. Mechanism depends on the
   class: `\date{...}` for article/amsart, a date row in `\preprint` for
   jheppub (its `\maketitle` prints no `\date`), `\Date{...}` for harvmac
   plain-TeX.
9. Typos, errata, and obvious errors: follow the rules in the next section.
   Every fix goes in `changes`; every unfixed issue goes in `warnings`.

## Typos, errata, and obvious errors

These rules are part of the fixing process, not a separate cleanup pass.
Record every judgement call: fixes in `paper.json` `changes`, unfixed issues
in `warnings`, and the reasoning in `<paper>/readme.md` when it is not
obvious.

1. **Textual typos, spelling, grammar** — fix them, and record the fix in
   `changes`.
2. **Mathematical errors** — do not silently fix. Preserve the source text;
   record the issue in `warnings` (and explain it in `<paper>/readme.md` if
   needed); keep the authors' own errata text in the source.
3. **Obvious bibliographic errors** — missing or duplicate entries, wrong
   years, broken `\bibitem`s — fix only when confident, and state the
   inference in `changes` (e.g. "supplied what I think is the correct
   reference").
4. **Never "improve" notation, claims, or exposition** — out of scope even
   if it looks wrong. If an issue affects correctness, treat it under
   point 2 rather than rewriting the passage.

## What git tracks (plan.html §4, `.gitignore`)

- Tracked: `.tex`, `.bbl`, figures, `readme.md`, `paper.json`, per-dir
  `.gitignore`, CI workflow, `plan.html`, `AGENTS.md`, `MEMORIES.md`,
  `docs/`, generated `index.md`/`index.html` (committed; see below).
- Ignored (root `.gitignore`): `*.aux *.log *.out *.toc *.lof *.lot *.fls
  *.fdb_latexmk *.brf *.blg *.bcf *.run.xml *.synctex.* *.tmp
  *.idx *.ilg *.ind`, `*.pdf`, `__pycache__/`.
- Exceptions need a per-directory `.gitignore` with `!` negations, since the
  root ignore would otherwise block them:
  - Figure-input PDF: `1110.0466v3/.gitignore` (`!QKHKcorrespondence3.pdf`).
  - xr inputs (`.aux` snapshots of companion volumes that
    `\externaldocument` reads; generated `.aux` stay ignored):
    `0905.0462v2/.gitignore`.
- PDFs are CI build products: never `git add` a PDF. A locally built PDF in
  the working tree is fine (it's ignored) but optional.

## Building locally

- Canonical: `cd <paper-dir> && latexmk -pdf -interaction=nonstopmode
  <dirname>.tex` (copy `common/` files in first if declared).
- `engine: pdftex` entries are plain TeX (see `papers.yml` build step for the
  exact two-pass `\read`-shadowing invocation); don't try `latexmk` on them.
- Success bar: exit 0, zero `^! ` lines in the `.log`, zero `undefined`
  references/citations after reruns. `Token not allowed in a PDF string`
  hyperref warnings point at math in titles → fix with `\texorpdfstring`.
- This machine has TeX Live 2023 (`pdflatex`, `latexmk` 4.83). CI builds in
  `ghcr.io/xu-cheng/texlive-debian:latest`, so a local pass is indicative,
  CI is authoritative.

## Index (plan.html §6)

- `index.md` + `index.html` are GENERATED by `scripts/generate_index.py`
  from `*/paper.json`. Never hand-edit them.
- After any `paper.json` change (including adding a paper): run
  `python3 scripts/generate_index.py`, and verify with
  `python3 scripts/generate_index.py --check` (CI enforces this).
- PDF links use absolute `SITE_URL` (`https://winstoncheong.github.io/arxiv-fixes`);
  keep in sync with `SITE_URL` in `.github/workflows/papers.yml`.

## Memory and notes (`MEMORIES.md`, `docs/`)

- `MEMORIES.md` is the short, curated cross-paper memory: invariants,
  recurring pitfalls, per-paper pointers, open questions. Keep it short; if
  an entry grows into a procedure, move the procedure to `docs/`.
- `docs/` holds long-form cross-cutting notes. Start at `docs/README.md`;
  current topics are TeX modernization pitfalls, hyperref/bookmarks, and
  plain TeX/harvmac conversion.
- Paper-specific conversion logs stay in `<paper>/readme.md`. Do not
  duplicate them in `docs/`; link to them.
- When a fix generalizes: add or update a note in `docs/`, add one line to
  `MEMORIES.md`, and update this file if the operating rules changed.
- When a paper is added or finished: write or refresh `<paper>/readme.md`,
  and add a per-paper pointer in `MEMORIES.md` if it has lasting lessons.

## CI (`.github/workflows/papers.yml`, plan.html §5)

- `push` to `master`: diff against base commit → build only changed paper
  dirs (plus dependents of changed `common/` files). `workflow_dispatch`:
  build all. `fail-fast: false`: one broken paper doesn't block others.
- `check` job: `generate_index.py --check`.
- `build` job (matrix over changed dirs): copy declared `common/` files,
  `latexmk -pdf` per `entries` (or the `pdftex` two-pass path), upload
  `pdf-<dir>` artifact. Timeout 25 min/job.
- `deploy` job: `scripts/assemble_site.py --fresh _fresh --out public
  --site-url "$SITE_URL"` merges fresh artifacts with previously deployed
  PDFs (unchanged papers keep old files), publishes `public/` (index pages +
  PDFs + readmes) to Pages. Never the whole repo, so intermediates never ship.
  Fresh-PDF lookup accepts the nested (`_fresh/pdf-<dir>/<pdf>`), flat
  (single matching artifact extracts with no per-artifact directory), and
  recursively-nested layouts.

## Adding a new paper (workflow)

1. `curl -sL https://arxiv.org/src/<id> -o <id>.tar.gz`, extract, inspect.
   Keep real inputs only; drop author-side junk (`.log`, stray `.toc`,
   unused `.cls`). Keep any material trailing `\end{document}`: it is
   unrendered but still source, and worth keeping for reference.
2. Directory `<id with / → _>/`, entry point renamed to `<dirname>.tex`
   (adjust `\include`/`\input` stems, not content). Pin the version in the name.
3. Modernize per the checklist above; minimal diff, mathematics untouched.
4. Write `paper.json` (abstract from the arXiv abs page; honest `status`;
   every fix in `changes`, every known defect in `warnings`) and
   `<paper>/readme.md` if the conversion has lasting quirks. Add per-dir
   `.gitignore` negations only if the build needs otherwise-ignored inputs.
5. `latexmk` build → zero errors/undefined refs → `generate_index.py` →
   `--check` → `git status` shows only intended files (PDF must not appear
   as a new tracked file). If a lesson generalizes, update `docs/` and
   `MEMORIES.md`.
