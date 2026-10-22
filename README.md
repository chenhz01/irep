<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# IREP — Industrial Reverse-Engineering Protocol

[![Code: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-blue.svg)](LICENSE) [![Spec: CC BY 4.0](https://img.shields.io/badge/spec%20%26%20docs-CC%20BY%204.0-lightgrey.svg)](LICENSE-SPEC) [![Python 3.10+ · numpy for 2 proofs](https://img.shields.io/badge/python-3.10%2B%20%C2%B7%20numpy%20for%202%20proofs-3776AB.svg)](requirements.txt) [![7 tools · exit 0](https://img.shields.io/badge/7%20tools-exit%200-brightgreen.svg)](#reproduce-everything) [![Self-judged BREAKTHROUGH · r = 1.143](https://img.shields.io/badge/self--judged-BREAKTHROUGH%20%C2%B7%20r%20%3D%201.143-success.svg)](docs/FEYNMAN-4ALIGN.en.md) [![Docs · 10k zh · 2.2k en](https://img.shields.io/badge/docs-10k%20zh%20%C2%B7%202.2k%20en-informational.svg)](docs/FEYNMAN-4ALIGN.en.md)

> **We built a ruler that can judge a system to death. The first thing it measured was itself.**

Status: spec v1.1.0 · repo v1.3.0 · License: Apache-2.0 (code) + CC BY 4.0 (spec & docs) · Self-judgment: `BREAKTHROUGH` (r = 1.143) · All numbers below are re-runnable.

> **v1.1.0 adds scales 5 and 6.** Scale 5 asks whether *generated* reasoning is new and earned, or just recitation (`HALLUCINATION / DRIFT / ECHO / EMERGENT / UNKNOWN`). Scale 6 asks whether the judgment was formed *before* the work, and proves it with a receipt: `manifest in → exit code out`, plus a sha256 lock on the ruler file so it cannot be shrunk right before the run. The four v1.0 scales are unchanged. Start at [`spec/G9-emergence-and-do-right-v1.1.md`](spec/G9-emergence-and-do-right-v1.1.md); the Chinese methodology with every measured number is [`docs/EMERGENCE-v1.1.zh-CN.md`](docs/EMERGENCE-v1.1.zh-CN.md).
>
> **Honest status: these two scales ship as specification.** Their reference implementations were written and exercised, but they are **not yet in this repository** — see §4 of G9. Treat the numbers in that document as unverified until the code lands. Nothing in the v1.0 gate is affected; it remains fully runnable.

**Three ways in — pick one, thirty seconds each**

- **Here to save money** → the sibling repo cuts AI-video acceptance sampling by a measured 9.82×, with a safety layer that never trades away: [`irep-video-acceptance-ci`](https://github.com/chenhz01/irep-video-acceptance-ci)
- **Here to integrate** → one command, standard library only: `python gate/irep_gate.py` (four scales, one verdict); then `gate/irep_gate_reversed.py` points the ruler back at you.
- **Here to doubt it** → read §10–§11 of the contract (how the mechanism fails, and when it does not apply), or run the checker that returns 1 when a piece is missing: [`docs/FEYNMAN-4ALIGN.en.md`](docs/FEYNMAN-4ALIGN.en.md)


---

## Feynman guide — read this first (60 seconds)

**What is this?**
IREP is a ruler. Point it at any system — open-source code, binary firmware, even a whole physical theory — and it answers three questions with measurable scales instead of opinions: *Am I legally allowed to touch it? If I absorb its ideas, must I say so? Is what I build a genuine second generation, or a respray?* The ruler ships as a runnable gate (`gate/irep_gate.py`) plus a written rulebook (`spec/`).

**Why should you care?**
"Can I build on this without being called a plagiarist?" is a question most teams answer with vibes, lawyers' bills, or luck. IREP answers it with four scales (license / attribution / difference-degree / industrial acceptance) and four public proofs you can re-run in minutes. One of those proofs is the ruler measuring **itself**.

**What should you do?**
Clone this repo, run `python gate/irep_gate.py`, then point the ruler at your own next project. If it says `BLOCKED`, believe it — that is the sieve working, not the ruler failing.

<!-- FRA:layer -->
**The same three questions, for every section**

A repository this long has one failure mode: you read the top, get interested,
and never reach the part that is actually about you. So every major section gets
the same three answers. Skim the table, jump to the one row that is yours.

<!-- FRA:start -->
| Section | What is this | Why should you care | What to do |
|---|---|---|---|
| [The three questions](#user-content-three-questions) | The protocol in one line: may I build on this, and is my build a second generation? | This decides, before you write code, whether the project is lawful and worth claiming. | Run `python gate/irep_gate.py` on your candidate and read the one-word verdict. |
| [Proof 1 — double slit](#user-content-proof-double-slit) | Four axioms rebuild quantum predictions those axioms never mentioned | "Compress it, then rebuild it" is a slogan almost everywhere; here it is a printed number with an error bar. | Run `python proofs/anchor_codec.py` and check the 14 held-out predictions. |
| [Proof 2 — owners and sieves](#user-content-proof-owners) | Most targets have owners; `BLOCKED` is a sieve, not a wall | It cuts ninety owned candidates in a minute — that is your legal personality, not just time saved. | Read the four orphan preconditions before assuming "abandoned" means "ownerless". |
| [Proof 3 — Fermat's Last Theorem](#user-content-proof-flt) | 358 years of withheld proof, re-derived from constraints alone | Proves the transferable thing is constraints, not source code — and why attribution is not politeness. | Run `python proofs/flt_rederive.py`; watch node H3 predict primes it never computed. |
| [Appendix — flight control](#user-content-appendix-flight) | A hidden industrial controller rebuilt from step responses only | Shows which layers of a real system transfer (constraints, tuning) and which never do (ten thousand flight hours). | Run `python proofs/ctrl_rederive.py`; read the asymptote warning before over-claiming. |
| [Scale 5 and 6 — generated work](#user-content-emergence-scales) | Two scales that judge something just generated: is it new, was the ruler set before the work | Automated research loops generate all day and cannot tell new from replayed; this is the missing ruler. | Read `spec/G9-emergence-and-do-right-v1.1.md` — and treat its numbers as unverified until code lands. |
| [Reversed mode](#user-content-reversed-mode) | The same gate pointed at somebody building on your public face | The day you publish, you become the reference system someone else gets measured against. | Run `python gate/irep_gate_reversed.py` and see what a minimum-cost cloner scores. |
| [Use boundary (G8)](#user-content-use-boundary) | What this protocol refuses to be pointed at, ever | It is the first page, not the last: weapons, malware, surveillance fail closed regardless of intent. | Check your target against these four items before anything else. |
<!-- FRA:end -->

Check the layer itself in one line (fail-closed — a missing row never returns 0):

```bash
python gate/feynman_read_assist.py --repo .
```

<!-- FGA4:axes -->
**Four-axis alignment — and this guide is checked by a machine, not by taste**

Every claim in this README has to align on four axes. The structural part is enforced by a runnable checker, because "answer-style steps that never enter the pipeline get skipped by inertia".

| Axis | What it pins down | How it is checked here | Where the evidence lives |
|---|---|---|---|
| **Result** | every number has a basis, a command, and a boundary | numbers ledger, long-form doc §4.3 | `proofs/*.py`, all exit 0 |
| **Mechanism** | every mechanism is named, has input → output, and a stated failure condition | four-part ledger, §5.2 | `spec/`, `gate/` |
| **Code** | every command was actually run; exit codes are contracts | six commands, one optional dependency (numpy), deterministic | `## Reproduce everything` |
| **Direction** | what this repo refuses to do, and for whom | negative scope + G8 on the first page | `## Use boundary` |

Full contract — 10,000+ Chinese characters, 14 worked examples, 6 analogies, sourced reference list, and the four ways this mechanism itself fails: [`docs/FEYNMAN-4ALIGN.zh-CN.md`](docs/FEYNMAN-4ALIGN.zh-CN.md).

English condensed edition (about 2,200 words) — same four definitions, same scorecard, same failure conditions: [`docs/FEYNMAN-4ALIGN.en.md`](docs/FEYNMAN-4ALIGN.en.md).

Check it yourself in one line (fails closed — a missing piece never returns 0):

```bash
python gate/feynman_align_check.py --repo .
```

---

<a id="three-questions"></a>
<!-- FRA:sec:three-questions -->
## The three questions, and the machine that answers them

You find a system worth building on. The hard part was never understanding it. The hard part is three questions:

1. **Legally, may I touch it?** (license gate)
2. **If I use its mechanisms, do I say so?** (attribution gate)
3. **Is what I ship a second generation, or a respray?** (difference-degree gate)

`irep_gate.py` measures all four scales — L1 license matrix, L2 attribution completeness, L3 difference degree `r = added / preserved`, L4 industrial acceptance artifacts — and returns exactly one word: `BREAKTHROUGH` / `DERIVATIVE` / `REPLICA` / `BLOCKED`.

**The first thing the ruler measured was itself:**

| Candidate | L1 license | L3 difference | Verdict |
|---|---|---|---|
| IREP second generation (this protocol) | MIT ALLOW | r = 1.143 (7 preserved / 8 added) | **BREAKTHROUGH** |
| Respray clone of `morluto/rea` (negative control) | MIT ALLOW | r = 0.053 (19 preserved / 1 added: "Chinese UI") | **REPLICA** |

Note the second row: it is **perfectly legal** — and still judged a respray. This ruler does not measure courts. It measures craft.

---

<a id="proof-double-slit"></a>
<!-- FRA:sec:proof-double-slit -->
## Proof 1 — Feynman's double slit: "prediction equivalence" is provable

Runnable: `proofs/anchor_codec.py` · held-out validation, re-runs with exit 0.

**Input: four axioms only** — superposition, phase factor exp(iS/ℏ), Born rule, unitarity. **Explicitly forbidden:** the Schrödinger equation, the Hamiltonian operator, energy quantization. From those four lines, rebuild the entire quantum machine.

**Then predict phenomena the axioms never mentioned (held-out):**

| Held-out phenomenon | Prediction vs truth | Relative error |
|---|---|---|
| Pöschl-Teller bound spectrum | −9.787791 vs −9.78774 | 4×10⁻⁸ |
| Harmonic oscillator zero-point energy ½ℏω | all pass | 2×10⁻⁶ |
| Free wave-packet dispersion | all pass | 1.8×10⁻¹⁵ (machine precision) |
| Quartic anharmonic ½x²+0.1x⁴ (no closed form) | three-way cross-check | 1×10⁻⁷ |

**14 held-out predictions all pass, maximum relative error 1.97×10⁻⁶.**

This answers a foundational question: bit-perfect lossless restoration is forbidden by Shannon/Kolmogorov lower bounds — but **prediction equivalence is not**. The information is not in the anchor; it is in the constraints. Store the anchor without its constraints and loss is guaranteed. The double slit happens to be a generator-level anchor of quantum mechanics (Feynman already paved the road: double slit → N slits → path integral → Schrödinger → Heisenberg), so at this one point, "compress to what a 12-year-old understands, then rebuild without loss" is not rhetoric. It is a number the machine printed.

Builder's confession, kept in the record: the machine was more reliable than its builder three separate times — a missing ½ normalization in the reference formula, a mislabeled convergence order, a constant bias introduced by the measurement method. The machine has no "I feel this is right" stage.

---

<a id="proof-owners"></a>
<!-- FRA:sec:proof-owners -->
## Proof 2 — Most systems have owners: judging to death is a sieve, rebuilding is the road

Most systems worth reverse-engineering **have owners**: active vendors, EULAs that forbid reverse engineering, legal departments that never sleep. For those, the word "reverse-engineer" reads badly on a resume.

The gate's verdict on an active-vendor proprietary image editor is two lines: L1 DENY (proprietary EULA forbids reverse engineering, copyright holder actively enforcing), scenario gate G6: owner active — no orphan exemption. **`BLOCKED` — the problem is not that the ruler is too soft; the scenario is wrong.**

**So `BLOCKED` is not a wall. It is a sieve.** A hundred candidates go in; the gate cuts ninety "owned" ones in a minute. What it saves is not time — it is your legal personality. A ruler that always says PASS is furniture. A gate that can kill deserves the name.

Point the same ruler at a different object and it lives: an orphaned industrial firmware (original vendor bankrupt, equipment holder authorized) → `CONDITIONAL-BREAKTHROUGH`, with four preconditions, each required: orphan fact provable, holder authorization, interoperability-maintenance purpose only (no copying or distributing original code), original copyright notice retained. Remember one line: **"no longer maintained" ≠ "ownerless."**

But the third road — clean even for owned systems — is the protocol's core mechanism:

> **Re-derivation: never read its code, only its behavior. Extract constraints. Satisfy the same held-out predictions with your own implementation.**

Four steps, none optional:

```
① Observation surface → black-box observable behavior (I/O, public specs), zero code contact
② Constraint extraction → invariants that "must hold", not implementations
③ Native rebuild → new implementation; no reference, no derivation, not one line of the original rewritten
④ Held-out comparison → prove prediction equivalence with phenomena outside the anchor
```

Legal boundary, stated honestly: black-box observation for interoperability has *conditional* legal space in many jurisdictions (EU Software Directive §6, DMCA §1201 interoperability exception), but the boundary depends heavily on scenario and jurisdiction. **This is an engineering protocol, not legal advice — confirm with counsel before acting.** What is certain: a rebuild that never touches code has no copyright-derivation problem at the source, because you wrote your own implementation.

---

<a id="proof-flt"></a>
<!-- FRA:sec:proof-flt -->
## Proof 3 — Fermat's Last Theorem: 358 years of "knowledge monopoly", re-derived

Runnable: `proofs/flt_rederive.py` · four nodes all PASS, zero lookup tables, re-runs with exit 0.

The hardest "patent" in the history of mathematics: in 1637 Fermat wrote the theorem in a margin and withheld the proof. Humanity guessed for **358 years**. IREP ran a complete reverse-derivation on it: **copy no one's proof — extract the constraints each generation of mathematicians extracted, and let the machine recompute them.**

| Node | Constraint (an invariant, not a proof) | Machine recomputation (held-out) |
|---|---|---|
| H1 Fermat 1637 | n=4 infinite descent — any solution spawns a smaller one | descent machine has no input to descend in a no-solution environment — consistent |
| H2 Kummer 1850 | when unique factorization dies in cyclotomic fields | Bernoulli numbers computed live: p<100 only 37 irregular (37\|B₃₂); the famous "irrational divisibility" 691\|B₁₂ re-verified |
| H3 Frey → Taniyama-Shimura → Wiles | arithmetic statement ⟺ modularity of a geometric object | the machine saw **only point-count sequences**, taught itself CM structure, predicted primes p∈[41,100) it had never computed: **13/13 correct** |
| H4 Germain 1823 | case-1 criterion + a name erased by a pen name | 15 Germain primes below p<200 computed live; 7 primes case-1 mechanically verified |

H3 is the sharpest cut: **the machine was never told any CM theory.** It saw only the point-counting behavior of elliptic curves, induced the constraint "the two halves of p = a²+b² determine a_p", then predicted primes it had never touched.

What came back is not a copy of a proof but five **knowledge points** (recombined, not transcribed): the real difficulty starts at n=4; Kummer's turn from "how to add" to "when unique factorization dies"; Frey's leap from arithmetic to geometry; Wiles' seven hidden years; and the iron evidence of knowledge democratization — **once published, anyone can independently verify. A theorem cannot be monopolized. Only "who came first" can.**

That last point is why node H4 exists: Sophie Germain's contribution was real, yet her name was erased by a pen name and the rules of her era (Gauss addressed her as "Monsieur Le Blanc"). **IREP's attribution gate (L2) is not politeness — it is a patch history wrote in blood.** Whoever re-derives must attribute whose constraints they absorbed, and must let those who come after attribute yours.

**A theorem cannot be monopolized; process and attribution can. IREP splits the two: process enters the public domain (held-out comparisons anyone can re-run), attribution enters the ledger (THIRD_PARTY_NOTICES, not one line missing).**

---

<a id="appendix-flight"></a>
<!-- FRA:sec:appendix-flight -->
## Appendix — black-box flight-control rebuild (industrial face)

Runnable: `proofs/ctrl_rederive.py` · held-out three scenarios RMSE < 9.1 mm, re-runs with exit 0.

A hidden altitude-hold controller (Kp=2.2, Ki=1.4, rate limit 1.50 m/s, integral clamp ±5) sits on a bench. The rebuilder sees **only step responses** — zero firmware contact. The rebuild recovers a PI controller fitting Kp=2.2, Ki=1.4, limit 1.49; held-out setpoints (2.5 m / 4.0 m / 2 m + gust) all pass. Two builder measurement errors were killed by the machine along the way (steady-state error is not evidence of integral action on a first-order plant; the slope minimum is not the rate-limit platform — the maximum is).

**Asymptote warning, mandatory:** behavior equivalence passing everything ≠ parameter recovery — many (Kp, Ki, rl) triples produce the same trajectories. What IREP transfers is prediction equivalence, not source code. The re-derivable coverage of an industrial control system splits into three layers: constraints (public), tuning (re-derivable), data (ten thousand flight hours — not re-derivable, it lives in time, not in constraints). This appendix demonstrates which layers are transferable in theory. It is not permission to touch any vendor's product — the scenario gate still judges those DENY.

---

## The protocol, five stages

```
① Authorization gate  → target legality (license matrix + G6 scenario gate + orphan four preconditions)
② Mechanism extraction → two legs: authorized-system mechanism extraction / black-box behavior-constraint extraction
③ Constraint rebuild  → write "why this must hold" as executable constraints
④ Recombination & differentiation → r = added / preserved ≥ 0.5 to claim second generation
⑤ Acceptance & attribution → industrial artifacts: obligation ledger / coverage gate / readiness gate / error ledger
```

<a id="reversed-mode"></a>
<!-- FRA:sec:reversed-mode -->
## Reversed mode — the ruler's second cut

> The first thing the ruler measured was itself. The second cut measures its own public face — because the moment you publish, your repo becomes somebody else's reference system.

Flip the chair: the same gate, roles swapped — the candidate is now *their* build on top of *our* public face. Three verdicts, all re-runnable:

| Reversed candidate | L2 attribution | L3 difference | Verdict |
|---|---|---|---|
| Sloppy clone (11 preserved + 1 shell, no source tracking) | 82% → FAIL | r = 0.091 | **DERIVATIVE** — not shippable until attribution is fixed |
| Clean clone (same, paperwork complete, patent intent declared) | 100% PASS | r = 0.091 | **REPLICA** — legal, complete, still a respray; prior-art warning fires |
| Genuine second generation (4 preserved + 6 new dimensions) | 100% PASS | r = 1.5 | **BREAKTHROUGH** — welcomed, by design |

The protocol does not block learning; it blocks respray claims. The publisher's journey is the five stages run backwards:

```
R5 attribution audit → R4 difference-degree defense → R3 constraints in public
→ R2 exposure inventory → R1 release conditions
```

The load-bearing arithmetic: a minimum-cost cloner preserves all 11 public mechanisms and adds one shell, landing at r = 1/11 ≈ 0.091 — deep in the REPLICA band. The public face is the moat.

Runnable: `gate/irep_gate_reversed.py` (stdlib only; exit code is CI-usable — 0 = all five checks pass). Full text: `spec/REVERSED-MODE-v1.0.md`, including hard gate **R-G1**: the exposure audit must be machine-produced — "I think nothing leaked" is the same disease G7 cures.

<a id="emergence-scales"></a>
<!-- FRA:sec:emergence-scales -->
## Scale 5 and 6 — judging what the machine generated (spec v1.1.0)

The four v1.0 scales judge a system that **already exists**. These two judge something that was **just generated** — by you, or by an automated research loop.

- **Scale 5 — emergence.** Does a reasoning chain contain an atom the reference did not have? Five verdicts: `HALLUCINATION` (steps carrying premises that were never earned) / `DRIFT` (left the reference without arriving anywhere) / `ECHO` (re-derived from atoms already present) / `EMERGENT` (carries a new, earned atom) / `UNKNOWN` (the evidence does not settle it — say so instead of guessing).
- **Scale 6 — do-right.** Was the judgment formed *before* the work? The contract is `manifest in → exit code out`, five questions Q1–Q5, and a sha256 lock on the ruler file so the ruler cannot be quietly shrunk just before the run.

**Both ship as specification only.** Their reference implementations were written and exercised but are **not in this repository**; §4 of [`spec/G9-emergence-and-do-right-v1.1.md`](spec/G9-emergence-and-do-right-v1.1.md) states this, and every number in that document is marked unverified until the code lands. The full Chinese methodology, with the measured distributions and the boundary exhibit where the gate green-lit a case it should not have, is [`docs/EMERGENCE-v1.1.zh-CN.md`](docs/EMERGENCE-v1.1.zh-CN.md).

---

## Hard gates (G1–G8, full text in `spec/`)

G1 no-source statements banned from external text · G2 r < 0.5 banned from "second generation" claims · G3 unknown license = fail-closed · G4 public repo = prior art, patent intent requires search first · G5 publicly available ≠ authorized · G6 scenario gate: active copyright holder = DENY, orphan = conditional · G7 re-derivation must pass held-out comparison — an uncompared "native rebuild" is only a self-claim · **G8 danger-domain ban (below)**.

<a id="use-boundary"></a>
<!-- FRA:sec:use-boundary -->
## Use boundary — G8, the first page of this protocol

IREP and the knowledge-interconversion protocol must never be pointed at:

1. Weapons of mass destruction (nuclear / biological / chemical / radiological) and their delivery, triggering, dissemination
2. Malware, vulnerability weaponization, unauthorized-access tooling
3. Surveillance, tracking, or profiling of unauthorized individuals
4. Other dual-use lethal domains (when in doubt: fail-closed)

Touching any of the above = `FAIL-CLOSED`, regardless of whether the target is public, whether the purpose is private, or whether it is "just discussion". **Any re-derivation scenario passes G8 before G1–G7.** Private discussion is not an exception: platform policies tolerate zero WMD-class content, a public repo touching weapons topics means takedown plus legal plus regulatory attention, and fear-type content produces spectators, not return visitors.

## What is NOT in this repo (the honest split)

| Layer | Contents | Where |
|---|---|---|
| 🌱 Open | protocol, gate, four proofs, G-rules, task-card template — every number re-runnable | this repo |
| 🔑 Partner | industrial acceptance playbooks, obligation-ledger templates for client engagements, engagement scoring | on request, under NDA |
| 💎 Never shipped | client data, calibration ledgers, internal amplifiers, identity assets | never, in any repo |

The public layer is deliberately the *criteria*, not the *recipe*: you can always see what we check, never how we adjudicate a specific engagement. Criteria in public = a standard; recipes in public = a toll booth.

## No-patent statement

Within the scope of our prior-art search (completed 2026-10-15; eight comparable public efforts located), no identical prior work was found for two components: the quantified difference-degree ruler and the fail-closed license gate. We do **not** claim global first-ness — full patent-text corpora were not covered. We publish the specification, not a patent: public disclosure within the search scope is the defensive timestamp.

## Reproduce everything

```bash
python gate/irep_gate.py        # stdlib only — four contrast verdicts
python proofs/flt_rederive.py   # stdlib only — four nodes, zero lookup tables
pip install numpy               # only needed by the two simulation proofs
python proofs/anchor_codec.py   # 14 held-out checks, max rel err 1.97e-6
python proofs/ctrl_rederive.py  # black-box flight-control rebuild, RMSE < 9.1mm
python gate/irep_gate_reversed.py  # stdlib only — reversed mode: 3 verdicts + R1–R5 self-checks
```

## The repo next door — and why we don't trade stars

<!-- FGA4:sister -->
Two repos, two different questions. They are complementary by content, not by numbers.

| | **`chenhz01/irep`** (you are here) | **`chenhz01/irep-video-acceptance-ci`** |
|---|---|---|
| The question it answers | "May I stand on this system — and is my build a second generation?" | "How much does luck cost me per finished video?" |
| Unit of value | a verdict (one word, four scales) | a multiple (9.82× generation, 3.2× frame-check) |
| What you get in 30 seconds | four contrast verdicts from one command | a measured sampling-reduction number you can hand-check |
| Best if you are | shipping something derived from someone else's system | paying GPU bills or reviewers' hours for AI video |
| Star it when | you want a pre-build gate, not a lawyer's invoice | you want the money-side proof that the gate has teeth |

**Star the pair if you want both halves of the argument:** this repo proves the ruler is honest (it judged itself); the sibling proves the ruler is useful (it saves a measurable amount). Either one alone is an opinion; together they are a case.

**What we will NOT do:** star-for-star exchanges, bought placements, "follow back" schemes, or asking you to star before you have run anything. Star counts are the only feedback signal that cannot be faked — trading them away would be trading away our own instrument.

**What a star actually gets you:** release notes when a new held-out proof lands, priority on issue replies (still 48h target, but issues from stargazers get read first), and a vote on which of the five roadmap directions ships next.

## Trending pledge — a guarantee we can actually keep

<!-- FGA4:trending -->
"Guaranteed to trend" is not a promise anyone can keep: ranking is decided by a platform algorithm, not by the author. Promising an outcome you do not control is marketing; promising one you do control is a contract. So here is the falsifiable version.

| # | Commitment | Measurable test | If we break it |
|---|---|---|---|
| 1 | Every number in this repo is re-runnable | any claim lacking a command is a bug — report it | fixed or deleted within 7 days |
| 2 | Every verdict can be contested by re-running the gate | you can disagree with a verdict using the same tool | published errata in `docs/`, credited to you |
| 3 | Issues get a first response within 48 h | timestamp of issue vs first reply | we say so publicly if we miss the window |
| 4 | No claim of adoption we cannot evidence | we do not publish usage numbers we cannot source | claim retracted |
| 5 | Unstar at any time, no argument | your star is not a contract with us | — (this is the point) |

**What "trending" means here, honestly:** we do not promise a chart position, a star count, or an algorithm boost — we cannot control those, and a repo that promises them is telling you something about its relationship with evidence. What we promise is the part that *causes* trending when it happens: a first screen worth reading, numbers that survive a hand-check, and a maintainer who answers. If the repo does not deserve a star after you run it, the correct action is to not give one — and to tell us why in an issue.

**The falsification test, stated up front:** run the three commands in `## Reproduce everything`. If any of them fails on a clean Python 3.10+ install, this pledge is void and the repo is wrong — not your environment.

## Collaboration — the part that isn't in this repo

Everything here is free: read it, run it, fork it. We will never chase you.

| Layer | What you get | How |
|---|---|---|
| 🌱 Open | everything in this repo, Apache-2.0 (code) / CC BY 4.0 (spec & docs), forever | clone and run |
| 🔑 Partner | industrial acceptance playbooks, obligation-ledger templates, engagement scoring, held-out calibration support | write us, under NDA |
| 💎 Never shipped | client data, calibration ledgers, internal amplifiers, identity assets | not negotiable, in any repo |

**Why the locked layer exists:** the gate in this repo judges *candidates*; what it cannot give you is the calibrated adjudication record for a specific engagement — the obligation ledger, the coverage evidence, the readiness gates. That is the part that takes a real project to earn, and it is deliberately not downloadable.

**How to ask (two pieces of information):** ① what you are building and what role the referenced system plays in it; ② which item you want and what you have already tried. A one-line message gets a one-line reply — that rule protects both sides' time.

**Not a fit:** requests to judge a specific vendor's product as BREAKTHROUGH without running the gate; requests for the locked layer without an engagement; anything touching G8. **A fit:** teams standing on a real system with a real second-generation build, who want the ruler pointed at it before shipping.

**Open loop:** open an issue describing a failure mode — the sharpest ones get fixed in the next version with credit in the release notes.

Contact: `hcac4735@agent.qq.com` (primary; 50 messages/day cap) · `shanlun2029@outlook.com` (overseas alternative). Response target: 48 hours.

## License & notices

**Dual-licensed, split by file type — MIT is not offered here.**

| Scope | Files | Licence |
|---|---|---|
| Code | `gate/*.py`, `proofs/*.py` — anything tagged `Apache-2.0` | **Apache License 2.0** — [`LICENSE`](LICENSE) |
| Specification & documentation | `spec/*.md`, `docs/*.md`, both READMEs, `INDEX.md`, `THIRD_PARTY_NOTICES.md` — anything tagged `CC-BY-4.0` | **CC BY 4.0** — [`LICENSE-SPEC`](LICENSE-SPEC) |

Every file carries an `SPDX-License-Identifier` tag; **the tag on the file wins**. Attribution obligations and suggested credit strings are in [`NOTICE`](NOTICE).

Third-party mechanisms and dependencies are registered in `THIRD_PARTY_NOTICES.md` (including `morluto/rea`, MIT: mechanisms referenced from its public docs, no code copied; difference judgment r = 1.143). This tool and this document are engineering self-checks, not legal advice.
