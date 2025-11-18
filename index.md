# arxiv-fixes index

# math/0701269v2 - The number of smooth 4-manifolds with a fixed complexity - Dave Auckly

[PDF](./math_0701269v2/6-1-07cmplx4.pdf)

**Abstract:** One can define the complexity of a smooth 4-manifold as the minimal sum of the number of disks, strands and crossings in a Kirby diagram. Martelli proved that the number of homeomorphism classes of complexity less than n grows as $n^2$. In this paper we prove that the number of diffeomorphism classes grows at least as fast as $n^{c\sqrt[3]{n}}$. Along the way we construct complete kirby diagrams for a large family of knot surgery manifolds.

Changes: 
* Fix missing bibliography (previous version has a `.bbl` file). One entry 'fm' was missing. I supplied what I think is the correct reference.
* add `hyperref` with colorlinks, pagebackref.
* Make some equations more readable (better indentation, `\left\{ ... \middle| ... \right}`), 
* fix spacing, prevent some bad line-breaks (`\nobreakdash-`, `~`)

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
