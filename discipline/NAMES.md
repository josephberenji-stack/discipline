# NAMES.md -- the v10 registry, resolved (AXIOMS-v10.md section Names; TAXONOMY-v10.md section 2).
# One word | one canonical definition | one file.  Adopted from NAMES-PROPOSAL.md with its section-4 decisions taken as recommended.
# word | canonical definition | file
Grace | flasqueness: every restriction map of the orbit presheaf is surjective (Boolean) | thm.py grace_bool; Flasque.lean
Grace depth | the skeleton at which extension of a local section first fails (a level) | engine-v1/naming.py; seedshape.py G4
averaging operator | N = (1/card(G)) sum g, the Reynolds idempotent onto the constants (an operator; NOT Grace -- the identification is OPEN, T7'') | gproj.py H1-H2
twirl | the uniform average of the Pauli group action, QIIT's noising channel (an operator; not Grace) | iit.py I1
closure element | 0 in Z/3, the non-unit, the origin the stabiliser fixes, the augmentation's target (a ring element; not Grace) | arrow.py A3-A4; everywhere.py Q3
Freedom | card(Sec) = card(lim D), the number of global sections (a count) | thm.py; values.py W1
Freedom = 1 class | models with exactly one global section (a class of models) | patch.py P1
Sec = empty class | models with no global section (a class of models) | patch.py P1-P2
seed | A0's carrier: the three inhabitants (a set of size 3); as quantities use 'reading' | AXIOMS A0; derive.py E2
carrier | A0's three inhabitants (a set); preferred over 'seed' for the set | AXIOMS A0
band | the ring-side generation object of IDEA-018/019: S_0 = {g^i - 1} in Z[Z/N], S_(k+1) = {x.y : x, y in S_k, x.y != 0} -- squares included, the product and not the pair (a set of ring elements; = D_(2^k) by IDEA-019 P2).  NOT A1a's 'level', whose objects are the unordered pairs of DISTINCT objects and whose count is C(n,2) (#177) | IDEA-018-levelcost-2.py band_sets; IDEA-019-freedomgate-2.py P2
arity | P1's 2: images per object under generation (an integer, k) | binary.py B1; derive.py E1
reading | a quantity computed on a model: Grace, Freedom, the magnitude, CF (four functions) | values.py W2
magnitude | abs(theta - 1/2) = theta_maj - 1/2 (a real in [0,1/2], defined iff Sec nonempty); in bits, R(theta) = 1 - H(theta) | thm.py T1-T5; mem.py M2
node magnitude | the magnitude read at a node of the partition lattice (a function on the lattice) | mem.py M4
kappa | kappa = max_C d_C, d_C = log2(card(A_C)/card(reach(C))) (a bit count, possibly infinite; ENGINE line; GLOSSARY spells it k); never 'the magnitude' until related to abs(theta - 1/2) | torus.py; reach.py; GLOSSARY
CF | the contextual fraction by LP (a real in [0,1], defined on every model); CF = 1 - 2^(-kappa), kappa = v_2(NCF) | patch.py P2; values.py W3; reach.py
Attention | A_pot: mean pairwise mutual information over compatible pairs (a real); ENGINE line only; not used in v10 | attention.py
compatibility deficit | log2(TOTAL/Freedom), zero over an index with a top (the v7 'Attention' formula; a different quantity) | three_seeds.py; ENGINE-v7 C13
Observation | axiom A4: objects carry labels in O; identity is bisimulation w.r.t. O and theta | AXIOMS A4; T8; exist.py X6
observer | a position (C, s) at which kappa is read (a point of the presheaf); ENGINE line | observer.py; GLOSSARY
witness | Abramsky's sense only: a term realising an existential / an LP dual witness; never the observer | witness.py
theta | A3's branch weight in [0,1]; T26's theta = 1/(1+rho) is a modelling identification [DEF] | AXIOMS A3
initial object | 0; retired word 'base' | ENGINE-v7 section 1
terminal object | 1; retired word 'base' | ENGINE-v7 section 1
base of the cover | the base space of the binary covering (the 3-cycle); retired word 'base' | pnp.py N4; binary.py B1
reach | reach(C) = { t restricted to C : t in Sec }, the realised sections at a context (a set) | GLOSSARY; torus.py
presentation | a point of the G-torsor P(S) | transcat.py D
presentation torsor | P(S), the G-torsor of a system's languages | transcat.py
self-presentation | an equivariant map eta : S -> P(S) (sigma in selfpres.py); exists iff every orbit is free | selfpres.py C5
definable | an element fixed by every automorphism, equivalently isolated by an automorphism-invariant subset | definable.py D1
translation category | TRANS(S) = P(S)//G, equivalent to the point (T22) | transcat.py A-B
translation subgroup | the regular normal subgroup of fixed-point-free elements plus identity, on the base points | arrow.py A3
torsor cost | card(G), T22 F's cost; equal to card(B^1)/card(H^1) at n = 3 with the complex built from torsors, and to card(H^0) on the trivial holonomy class (T31); P(S) := H^0 for a model class is a DEF | gproj.py F; values.py W6; onecost.py K1-K4
memory cost | R(theta) = 1 - H(theta), the forced memory in bits | mem.py M2
loop cost | m * R(theta) over a period-m loop (was 'topological debt') | mem.py M3
site | the canonical coverage by complements of points {X minus {a}} = the translation-orbit of the unit set {1,2}, selected by the obstruction (a Grothendieck topology; a measurement scenario); the unique obstructed antichain cover of 9 | site.py S1-S3; coverage.py V2-V3
deck | the deck transformation of the binary cover = the antipodal rotation +3 = the point/line duality (an involution) | genesis.py G1
psi_2 | inversion x -> -x; on the hexagon the reflection fixing p0 and l12 (an involution; not the deck; owns hand.py's residual bit) | genesis.py G3; v10check.py G3
incompleteness | a predicate no element represents (Lawvere's diagonal); its relation to the magnitude is OPEN | ENGINE-v1 E3; selfpres.py C1
forced memory | R(theta) = 1 - H(theta) bits per branch; T9's retention under a new name | mem.py M1
generative chain | the six arrows of T29: three objects -> binary generation -> incidence -> ring -> site -> torus -> three objects | site.py S6
Kav | (book term) not a framework term until a file computes it |
atom of the divisibility poset | an index with exactly one proper divisor; the index set of every multiplicative family the framework carries (an integer). The BARE word 'atom' is not a term: IDEA-025 uses it for the atoms of a lattice | AXIOMS-v10-CLEAN.md A5; lambda.out N1
autocorrelation | (Joseph's prose name) the order-dependence of a derivation: two derivations of one object agreeing in length, start, last state and step multiset carry different prefix-span flags (a property, NOT an operator; none is exhibited) | AXIOMS-v10-CLEAN.md A6; IDEA-057-coordinate-2.py:527 PF1
assignment poset | for a member of the repair system, the locally consistent subsets of its realised triples ordered by inclusion, where a subset is locally consistent when no edge of the member's 2-complex lies on more than two of its triples (a poset; a lattice on 52509 of 111288 members and not on 58779). The BARE phrase 'assignment lattice' is NOT a term: AXIOMS-v10-CLEAN.md line 430 and line 710 use it for the partition lattice carrying the magnitude, a different object | AXIOMS-v10-CLEAN.md A7; IDEA-077-assignment-1.py:410 AP1
Alexandrov topology | on a finite poset, the topology whose opens are the UP-sets, under which sheaves of sets are equivalent to functors on the poset by L(F)(x) = F(up x) and G(A)(U) = the limit over U (a topology; the equivalence is T34 and is CITED, not this space's). The down-set convention gives functors on the OPPOSITE poset and is not used here | AXIOMS-v10-CLEAN.md T34; ALEXANDROV-2026-09-13.md; IDEA-072-alexandrov-1.py:420 AL1
measure window | the interval [lo,hi] on the repair measure mu = gap + duplication that a box's enumeration admits; together with the cap on the top-level start it forms the measure cut, whose whole effect on a shape is the set of triple counts it admits (IDEA-078 derivation 6).  An interval on a measure, never a threshold and never a quantity carried by a member | IDEA-078-window-1.py:669 WS1; AXIOMS-v10-CLEAN.md
measure cut | the pair (measure window, top-level start cap); the two enter admissibility only through one expression, lo <= n + k - 2d <= hi, so they are parameters of ONE cut and not independent axes (#209).  The complement of the cut is the SHAPE CAPS, which decide which triple sets exist at all | IDEA-078-window-1.py:669 WS1
window-forced | of an observation that holds on a box: it fails on the box obtained by relaxing the measure cut alone, the shape caps held fixed.  The only reading under which the window names a cause rather than a co-occurrence; a property of an observation-and-box pair, never of a quantity by itself | IDEA-078-window-1.py:669 WS1
joint image | of an observation on a box: the set of values its deciding statistic takes there; what the observation asserts is one equation per value, a number that does not grow with the size of the box | IDEA-078-window-1.py:689 WS2
