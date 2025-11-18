# arxiv-fixes index


# math/9912158v1 - Quiver varieties and finite dimensional representations of quantum affine algebra - Hiraku Nakajima

[PDF](./math_9912158v1/math_9912158v1.pdf)

**Abstract:** We study finite dimensional representations of the quantum affine algebra, using geometry of quiver varieties introduced by the author. As an application, we obtain character formulas expressed in terms of intersection cohomologies of quiver varieties.

Changes: Added `hyperref` so that the pdf has bookmarks. Color links also.

# 1110.0466v3 - Wall-crossing, Rogers dilogarithm, and the QK/HK correspondence - Sergei Alexandrov, Daniel Persson, Boris Pioline

[PDF](./1110.0466v3/dilognotes.pdf)

This used the document class `JHEP3`. Crucially, the pdf did not have bookmarks.
It appears that this document class is outdated, and incompatible with `hyperref`.

The modern JHEP approach is to use the `jheppub` package instead.

I had to convert `\email{}` to `\emailAdd{}` and `\affiliation[]{}`.

File had special characters (`<CA>`) that prevented compilation. Had to remove them.
Had a messed up href in the bib.

Needed to add things to `\preprint{}` to support multiple identifiers.

# hep-th/9408074v2 - A strong coupling test of $S$-duality - Cumrun Vafa and Edward Witten

[PDF](./hep-th_9408074v2/main.pdf)

Original file uses TeX and harvmac. 

Wrote a script to aid conversion from TeX to LaTeX.

More info on conversion [here](./hep-th_9408074v2/readme.md)

# alg-geom/9507012v2 - Heisenberg Algebra and Hilbert Schemes on Projective Surfaces - Hiraku Nakajima

[PDF](./alg-geom_9507012v2/alg-geom_9507012v2.pdf)

Original file was in AMS-LaTeX.
