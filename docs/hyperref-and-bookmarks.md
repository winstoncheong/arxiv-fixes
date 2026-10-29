# hyperref and bookmarks

Notes on making old papers linkable and navigable without changing their
content. See also [tex-modernization-pitfalls.md](./tex-modernization-pitfalls.md).

## Preamble

Load `hyperref` last (after `amsmath`/`amssymb` and any font/encoding
packages). The repo convention is:

```tex
\usepackage[colorlinks,allcolors=blue,pagebackref]{hyperref}
```

`pagebackref` is what produces the “cited on pages …” lists in the
bibliography. It makes the bibliography longer; see the page-count note in
[tex-modernization-pitfalls.md](./tex-modernization-pitfalls.md).

Set metadata when the visible title block is manual:

```tex
\hypersetup{pdftitle={Descente pour les n-champs},
            pdfauthor={Andr\'e Hirschowitz and Carlos Simpson}}
```

## What becomes a bookmark

- `\section`, `\subsection`, ... are bookmarked automatically, including
  their numbers.
- `\section*` / `\subsection*` are **not**. Add an anchor and a TOC line:

  ```tex
  \subsection*{Heading}%
  \phantomsection
  \addcontentsline{toc}{subsection}{Heading}
  ```

  `\phantomsection` must come before `\addcontentsline` so the link target
  is the heading, not the previous anchor.

- If the paper has an unnumbered introduction that should still appear in
  the PDF outline, use the same pattern with `{section}`.

## Math in headings: `\texorpdfstring`

A heading is also written into the PDF outline, where TeX math is not
available. The build warns:

```text
Package hyperref Warning: Token not allowed in a PDF string (Unicode):
(hyperref)                removing `math shift' on input line 951.
```

Wrap the math:

```tex
\subsection{Les \texorpdfstring{$n$}{n}-champs de Segal}
```

The second argument is a PDF string, not typeset text. Rules:

- Escape `_` as `\_` (`\texorpdfstring{$M_f$}{M\_f}`); a bare `_` still
  triggers “removing `subscript'”.
- Replace symbols with words: `$\infty$` → `infini`, `$\emptyset$` →
  `l'ensemble vide`, `$\ast$` → `*`.
- `\ref` inside a heading is resolved to the number in the bookmark (e.g.
  “Démonstration du théorème 2.3”), but verify it; `\ref` in a PDF string is
  fragile.
- `\underline{Hom}` loses the underline; write `Hom`.
- Nested braces are fine; keep the second argument simple.

The success bar for this repo is **zero** `Token not allowed in a PDF string`
warnings. They are easy to grep:

```bash
grep -c 'Token not allowed' paper.log
```

## Cross-document references

If a paper uses `xr`'s `\externaldocument`, switch to `xr-hyper`, not plain
`xr`, or the imported links will not be hyperlinked (see `0905.0462v2`).

## Verifying

Extract the outline and inspect it for mojibake or empty entries:

```python
import fitz
d = fitz.open("paper.pdf")
for level, title, page in d.get_toc():
    print(level, title, page)
```

Check that:

- every top-level section is present;
- subheads with math have readable titles (no `Les -champs`);
- page numbers are plausible;
- the count is what you expect (e.g. 21 sections + 71 subheads).

Rendered spot checks catch link colours and broken headings:

```bash
pdftoppm -f 4 -l 4 -r 70 -png paper.pdf page
```

## Common PDF-string removals

| Token | Cause | Fix |
| --- | --- | --- |
| `math shift` | `$...$` in heading | `\texorpdfstring{$x$}{x}` |
| `subscript` | bare `_` in the text argument | `\_` |
| `superscript` | `^` or `'` in math | simplify the text argument |
| `\infty` | symbol in math | `infini` |
| `\emptyset` | symbol in math | `l'ensemble vide` |
| `\@@underline` | `\underline{...}` | plain text |
| `\hbox`, `\z@` | layout macros leaked into the heading | rewrite the heading |
