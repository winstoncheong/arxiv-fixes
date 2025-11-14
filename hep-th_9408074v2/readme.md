
`\nref` defines a bib entry, without citing.

`\ref` defines a bib entry and cites it.

Equations are defined with `\eqn\eqlabel{...}`
This defines a label `\eqlabel` that can be referred to in the text.
It is equivalent to `\begin{equation}\label{eqlabel}\end{equation}` and `\eqref{eqlabel}`.

---

After automated conversion, some issues remain:

```
 Latexmk: ====Undefined refs and citations with line #s in .tex file:
    Label `longo' multiply defined
    Label `defk' multiply defined
    Label `hphi' multiply defined
    Label `zeq' multiply defined
```


There are multiple `\eqn\defk`'s such as 

`\eqn\defk{k={1\over 8\pi^2}\int_M\Tr\, F\wedge F,}` on line 1259
`\eqn\defk{k_j=D^iB^+{}_{ij}+D_jC.}` on line 1401

---

Bibliography is reconstructed from commands `\nref`, `\ref`, `\refs`. 
Ordering appears to be citation ordering.

There may have numbering differences from arxiv preprint version.

Heading style is different from TeX (harvmac) to plain LaTeX.
`\newsec{}` versus `\section{}`
`\subsec{}` versus `\subsection{}`

Some fake sections with `\noindent{\it{...}}`

---

Automated conversion misses

> [58] E. Witten, “Supersymmetry Yang-Mills Theory On A Four-Manifold,” IASSNS-HEP-
94/5

which was defined on line 3814 with `\nref\switten{...}`.
This label was already used on line 451: `\ref\switten{..}`, which is the same reference. 
It is a duplicate entry to [35] on the arxiv preprint.

This shifts bib entries [59]--[62] over.

--- 

Manual taloring needed..
