# The Feynman Guide Contract — Four-Axis Alignment (English condensed edition)

> Condensed from the Chinese contract (`FEYNMAN-4ALIGN.zh-CN.md`, 10,000+ characters): definitions, scorecard and failure conditions kept intact, fourteen worked examples cut to three. Every number below is re-runnable from this repository.

**What is this?**
A contract for the first sixty seconds of a repository: a guide must align on four independent axes — **result, mechanism, code, direction** — and "it reads convincingly" is not evidence that any of them is present. One part of the contract is machine-checked, because a rule that lives only in prose is a rule that gets skipped.

**Why should you care?**
Readers decide in under a minute, running four silent queries: *does it work, how does it work, can I run it, when should I not use it?* Failing any one loses the reader without producing an error message — the most expensive failure mode in technical writing.

**What should you do?**
Read §2.2 (the four definitions), then run `python gate/feynman_align_check.py --repo .`. A 1 means a structural piece is missing; a 0 means the machine's part passed, and the prose is still yours to defend.

---

## 1. The disease: three kinds of bad guides

| Pattern | Symptom | The tell | Reader concludes |
|---|---|---|---|
| **The Brag** | adjectives where numbers belong | no baseline, no seed, no boundary | probably not measured |
| **The Vapor** | architecture diagrams, no runnable entry point | the quickstart cannot be finished | probably not built |
| **The Drift** | repo does one thing, README claims five | feature list outruns the file tree | aspirational, or abandoned |

Each is a missing axis in costume — Brag: result, Vapor: code, Drift: direction. Naming the axis makes the problem fixable: "write better" is not an instruction, "add a boundary" is.

---

## 2. Why four axes

Remove one axis and a specific collapse follows:

- no **result** → cannot say what it achieves → an *idea*;
- no **mechanism** → cannot say how → *magic*;
- no **code** → cannot say where it runs → a *legend*;
- no **direction** → cannot say where it stops → *universal*, which means useless.

Four is not ours: it matches what a human already asks of an unfamiliar system — *Is it effective? How? Can I run it? When should I not use it?* The contract only fixes the order, so the flattering question is not answered first.

### 2.1 The same four axes appear elsewhere

The author's working system has a separate rule, *model four-axis alignment*, used when swapping language models so that "we changed models" cannot substitute for "here is what changed". It runs the same four axes over a different object — result: score gap on one test pack; mechanism: reasoning and tool-call differences; code: runnable rate of generated code; direction: whether the advice points the same way — with the same premise, *trust the comparison, not the self-report*.

**Borrowed:** the orthogonal-four structure and the "one missing axis collapses the claim" rule. **Not borrowed:** its thresholds and probe batteries. Those belong to model evaluation; transplanted into documentation they produce ritual, not rigor.

### 2.2 The four definitions

These four sentences are the whole contract. The right-hand column is the self-check to run on your own draft.

| Axis | Definition | Self-check |
|---|---|---|
| **Result** | every number traces to a command, and that command reproduces the same number | "Which line of output produced this 9.82×?" |
| **Mechanism** | every mechanism has a name, input, output and failure condition | "Under what input does it stop being true?" |
| **Code** | every command was run; the exit code is a contract, not rhetoric | "If I paste this line, will it fail?" |
| **Direction** | the guide states what it does not do, who it is not for, what it does not guarantee | "What is this most likely to be misused as?" |

None asks "is this well written?" All four ask something falsifiable — the difference between a guide that can be reviewed and one that can only be admired.

---

## 3. Axis zero: language

Before the four axes there is a zeroth: language aligned to a smart outsider. Skip it and the other four are wasted, because the reader leaves before reaching them.

1. **The three questions come first, in plain words.** If they need jargon, the author does not yet understand the artifact well enough to document it.
2. **Spend terminology deliberately.** Every new term costs attention and must be repaid in precision; a term used once is a tax with no return.
3. **Prefer the concrete sentence.** "Sampling cut 9.82× at base rate 8%, verifier Se 0.978 / Sp 0.977" beats "significantly improves efficiency" — and is shorter to defend.

---

## 4. Axis one: result

Four rules, in the order they are usually broken: every quantitative claim is reproducible by a command or states why it is not; every number carries a **basis** (method, sample size, seed); every number carries a **boundary** (where it stops holding); unit-free multiples are banned ("ten times faster" without a baseline is a slogan).

Why it fails most is incentive, not skill: "ten times faster" takes half a second, the basis takes five minutes, and someone else pays later. That asymmetry is why the check must be a gate, not a habit.

| Number | Meaning | Basis | Command | Boundary |
|---|---|---|---|---|
| 1.97e-6 | max relative error, anchor reconstruction | 14 held-out predictions, max per-item error | `proofs/anchor_codec.py` | this anchor set only; re-anchor and re-measure |
| 14 | held-out prediction count | withheld from reconstruction, used only for comparison | same | few items → weak power, no extrapolation |
| 4 | Fermat re-derivation nodes | constraints from four generations of mathematicians | `proofs/flt_rederive.py` | four passing nodes ≠ all proof paths |
| < 9.1 mm | trajectory RMSE, black-box rebuild | position error at unseen setpoints | `proofs/ctrl_rederive.py` | passing comparisons ≠ recovering parameters |

The table converts a claim into an account: a sceptic says "row three, re-run it", and the argument ends in one command.

---

## 5. Axis two: mechanism

Four items must coexist: a **name** (citable), an **input → output** (a one-line black box), a **reason it works** (causal, not "the algorithm is advanced"), and a **failure condition** (the input that returns something wrong). A mechanism missing the fourth is not a mechanism; it is a belief.

| Mechanism | Input → output | Why it works | Failure condition |
|---|---|---|---|
| Four-scale verdict | candidate → one verdict word | splits "looks alike" into orthogonal checks, defeating holistic bias | distorted description → distorted verdict |
| Baseline stripping | reference + candidate → difference rate r | item-by-item comparison; low r means a respray | an incomplete reference description inflates r |
| Constraint extraction | system → constraints, not implementations | constraints are portable; implementations are copyrighted | wrong constraint → you rebuild a different thing, which can still pass |
| Anchor reduction | system + few anchors → low-dimensional anchor set | reconstructibility implies compressible knowledge | badly chosen anchors reconstruct only a local patch |

Counter-example: *"Adopts an advanced multi-stage verification architecture that significantly improves accuracy."* No name, no input/output, no causation, no failure condition — zero content, and it reads as competent, which is what makes it dangerous.

Why the failure condition sits near the top: readers judge a tool by when it will hurt them, not by what it can do. Disclosing the limit is the cheapest way to turn a one-shot transaction into a repeated game — the reader learns it either from you or from an incident, and only the first keeps them.

---

## 6. Axis three: code

Three rules: every command in the guide was executed and its exit code reported; dependencies are stated, and "zero third-party dependencies" must match the actual import list; output is deterministic — fixed seeds, no network, no wall-clock values in asserted numbers. `exit 0` means "ran on a clean machine", not "this is good". `exit 1` means "refused" — often the more valuable signal, since a check that can only return success is not a check.

Two fake passes: **the tautology** (the check compares a value with a constant derived from the same computation, so it cannot fail) and **the silent skip** (the test skips itself when a dependency is missing and the runner still reports success). Both are preventable: run each checker once where it *must* fail. This repo's checker ran against a repo missing its anchors and a nonexistent path; it returned 1 both times.

---

## 7. Axis four: direction

Three parts, all mandatory: **what it does not do** (it does not grant legal permission — a `BREAKTHROUGH` verdict is a technical and attribution judgement, not a licence to ship); **who it is not for** (teams wanting a compliance checklist for counsel); **what is not guaranteed** (difference rate measures distance from a reference, not quality — a high r makes something distinguishable, not good).

This is the only section the author cannot gain by overstating, which is why it is read more carefully than the feature list.

---

## 8. The scorecard

| Axis | Weight | 5 | 3 | 1 |
|---|---|---|---|---|
| Result | 30% | basis + command + boundary | command, no boundary | adjectives only |
| Mechanism | 25% | all four items | name and input/output | nouns only |
| Code | 25% | ran, deterministic, zero deps | ran, special environment | never ran |
| Direction | 20% | all three refusals | "does not do X" only | no boundary |

Thresholds: **≥ 4.0** publishable, **3.0–3.9** internal, **< 3.0** back to the workshop.

**The cap rule.** Any axis ≤ 2 sets the total to zero. A threshold is not a weight: averaging lets a strong axis buy forgiveness for a fatal one. A document with a fabricated number should not publish because its mechanism section is elegant; a repo that does not run should not reach the front page because its positioning is sharp.

**Self-scoring must include the deduction**, or it fails the result axis in the act of self-assessment. This repo's v1.0.0 self-score: 4.7 — result 5, mechanism 4 (constraint extraction's failure condition is still abstract), code 5, direction 5. The 4 is the honest part; 4.7 is arithmetic.

---

## 9. Three worked examples

**Double-slit reconstruction.** 14 held-out predictions pass, max relative error 1.97e-6, via `proofs/anchor_codec.py`; four assumptions, no equations copied. Direction: this proves *predictive equivalence transfers*, not that the theory is understood — the sentence that makes it credible by lowering its own claim.

**A proprietary image format.** `DENY`: active copyright holder plus proprietary licence; compliance vetoes before difference-degree runs. Direction: **a DENY is not a prohibition on learning** — the documented format may be studied, the implementation may not be copied.

**AI-video acceptance, 9.82× (sibling).** Sampling cut 9.82× at base rate q = 8%, verifier Se 0.978 / Sp 0.977, fixed seed. Expected generations fall from `1/q` to `1/PPV`, so the multiple is `PPV/q`; PPV, not accuracy, decides economics at low base rates. Hand-checkable: `0.978×0.08 / (0.978×0.08 + 0.023×0.92) = 0.7871`, so `0.7871/0.08 = 9.84` — the simulation prints 9.82, and the 0.2% gap is reported as Monte Carlo noise rather than tuned away. Drop the verifier to Se/Sp 0.874/0.818 and the same pipeline yields 3.68×: a 62% loss from a change no README would mention.

---

## 10. How this mechanism fails

1. **Formalism.** Four headings, four empty sections, a ledger full of "to be filled". A checker verifies structure, not sincerity. Countermeasure: mandatory deduction reasons plus a published periodic human review.
2. **Word inflation.** Length becomes the goal; this document has a floor and is therefore exposed. The floor prevents underspecification, not bad prose: every 500 words must add one verifiable information point.
3. **Table worship.** Dense tables, no causation. Every table needs a "why" column or a paragraph after it; otherwise it is layout, not argument.
4. **Self-certification.** The author scores 4.7, the reader measures 2.1. Countermeasure: one external comparison before publication — someone who did not write the guide follows it and records where they got stuck.

---

## 11. Failure conditions of this contract

- **Not legal advice.** `CONDITIONAL` means "ask a lawyer", not "ask again later".
- **Structure is not quality.** A document can pass the checker and still be wrong, boring or dishonest.
- **It assumes a runnable artifact.** For specs, datasets and design documents the code axis degrades to "every claim has an inspectable source" — weaker.
- **It assumes an external reader and network-free reproducibility.** Incident notes written under time pressure, and claims depending on a live third-party API, belong outside this contract.
- **It can be gamed.** Four headings and no content still passes the structural check; the cap rule raises the cost of gaming but does not eliminate it.
- **It does not measure usefulness.** A perfectly aligned guide to a useless tool scores 5/5.

---

## 12. References

| Source | Year | Borrowed | Not borrowed |
|---|---|---|---|
| Feynman, *Cargo Cult Science* | 1974 | honesty as "not fooling yourself" | its critique of institutional education |
| Feynman, *Lectures on Physics* | 1963–65 | restating in outsider-legible language | the physics |
| Popper, *Conjectures and Refutations* | 1963 | falsifiability as the line a promise must cross | his political philosophy |
| Diátaxis (Procida) | 2017– | four documentation modes must not be mixed | its enforced directory structure |
| RFC 2119 | 1997 | graded strength of MUST / SHOULD / MAY | protocol context |
| Hyrum's Law (attrib. H. Wright; Google SRE) | 2010s | observable behaviour gets depended upon | the misreading that docs are pointless |
| Chesterton, *The Thing* | 1929 | ask why the fence exists before removing it | — |
| *The Art of War*, "Estimates" | pre-Qin | temple reckoning: self-audit before committing | military framing |
| *Record of Learning* (《礼记·学记》) | pre-Qin | teaching reveals what you do not know | — |

**Citation discipline:** no unverifiable statistics are cited here — no "X% of developers never read the README". Such numbers circulate widely with no traceable origin, and once cited they drag down every verifiable number beside them. Resisting that is what the result axis is for.

---

## 13. Change log

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-20 | First English condensed edition: definitions preserved, scorecard and cap rule, three worked examples, four failure modes, contract-level failure conditions, sourced references |

**How this file is checked.** The checker guards both editions with a language-appropriate measure: `*.en.md` is counted in words (floor 1,800) and must contain the four English axis names, a failure-condition section and a reference list; CJK editions are counted in Chinese characters (floor 10,000). One counter for both would let either edition borrow the other's volume — the metric error this repo already logged once.

```bash
python gate/feynman_align_check.py --repo .
```
