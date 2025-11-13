
This repo is meant for keeping my nontrivial changes to arXiv submissions, 
so that the source compiles and the resulting document is something I consider usable.

# 1110.0466v3 - Wall-crossing, Rogers dilogarithm, and the QK/HK correspondence - Sergei Alexandrov, Daniel Persson, Boris Pioline

[PDF](./1110.0466v3/)

This used the document class `JHEP3`. Crucially, the pdf did not have bookmarks.
It appears that this document class is outdated, and incompatible with `hyperref`.

The modern JHEP approach is to use the `jheppub` package instead.

I had to convert `\email{}` to `\emailAdd{}` and `\affiliation[]{}`.

File had special characters (`<CA>`) that prevented compilation. Had to remove them.
Had a messed up href in the bib.

Needed to add things to `\preprint{}` to support multiple identifiers.


