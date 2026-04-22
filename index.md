# arxiv-fixes index

# hep-th/9402147v2 Gromov-Witten classes, quantum cohomology, and enumerative geometry - M. Kontsevich, Yu. Manin

**Abstract**: The paper is devoted to the mathematical aspects of topological
quantum field theory and its applications to enumerative problems of algebraic
geometry. In particular, it contains an axiomatic treatment of Gromov-Witten
classes, and a discussion of their properties for Fano varieties. Cohomological
Field Theories are defined, and it is proved that tree level theories are
determined by their correlation functions. Applications to counting rational
curves on del Pezzo surfaces and projective spaces are given.



# alg-geom/9405035v2 - Enumeration of rational curves via torus actions - M. Kontsevich

[PDF](./hep-th_9405035v2/hep-th_9405035v2.pdf)

**Abstract:** This paper contains an attempt to formulate rigorously and to check predictions in enumerative geometry of curves following from Mirror Symmetry. The main tool is a new notion of stable map. We give an outline of a construction of Gromov-Witten invariants for all algebraic projective or closed symplectic manifolds. Mirror Symmetry in the basic example of rational curves on a quintic 3-folds is reduced to certain complicated but explicit identity. The strategy of computations can be described as follows: 1) we reduce counting problems to questions concerning Chern classes on spaces of curves on the ambient projective space, 2) using Bott's residue formula we pass to the space of (degenerate) curves invariant under the action of the group of diagonal matrices, 3) we get a sum over trees and evaluate it using the technique of Feynman diagrams. Our computation scheme gives ``closed'' formulas for generating functions in topological sigma-model for a wide class of manifolds, covering many Calabi-Yau and Fano varieties.

Changes:
* documentstyle -> documentclass
* resectioning



# alg-geom/9601011v1 - Gromov-Witten invariants in algebraic geometry - K. Behrend

**Abstract:** Gromov-Witten invariants for arbitrary projective varieties and
arbitrary genus are constructed using the techniques from K. Behrend, B.
Fantechi: The intrinsic normal cone.

Changes:
* documentstyle -> documentclass
* resection for bookmarks and toc to work
* convert some diagrams to use tikzcd
* some eqnarray* -> align*
* pf env -> proof

Warning: In the original paper, the sections were unnumbered. This is also the
case with the published version.

# 0910.4460v2 - Lectures on canonical and crystal bases of Hall algebras - Olivier Schiffmann

[PDF](./0910.4460v2/0910.4460v2.pdf)

**Abstract:** These are the notes for a series of lectures given on the theory of canonical and crystal bases for Hall algebras (for a summer school in Grenoble in 2008). It may be viewed as a follow-up to arXiv:math/0611617. It covers the construction, due to Lusztig, of the canonical bases for the Hall algebra of a quiver Q in terms of a certain category of perverse sheaves over the moduli space of representations of Q. It also contains an exposition of Kashiwara and Saito's geometric construction of the crystal graph in terms of irreducible components of Lusztig's lagrangian in the cotangent bundle to the above moduli spaces. The last section deals with the Hall algebras of curves. It contains a few new results and conjectures. Apart from these, the text is purely expositional. 

Changes:
* Changed fake sections into real ones.
* Hyperlinks, bookmarks, pagebackref

# math/0611617v2 - Lectures on Hall Algebras - Olivier Schiffmann

[PDF](./math_0611617v2/math_0611617v2.pdf)

**Abstract:** These are notes for a minicourse on Hall algebras given at the ICTP in Trieste in January 2006. After giving the definition and first properties of Hall algebras, we study in some details the classical Hall algebra, the Hall algebra of quivers, and the Hall algebra of coherent sheaves on smooth projective curves. The last section deals with the Hall algebras in the context of derived categories. (The figures only seem to come out nicely in the .ps file)

Changes:
* Changed fake sections into real ones.
* Hyperlinks, bookmarks, pagebackref
* Fix spelling, typos, picture env overlap with header
* Fix poor spacing before table on page 73
* Fix obscured equation label 4.18


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
