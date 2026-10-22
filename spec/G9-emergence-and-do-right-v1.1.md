<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# G9 — Emergence and Do-Right: the fifth and sixth scales (v1.1)

Status: **specification published; reference implementation not yet open-sourced.**
Applies to: IREP v1.0.0 (four scales) → v1.1.0 (six scales).
License of this document: see `LICENSE` and `LICENSE-SPEC` (if present). Default: same terms as the repository.

---

## 0. Why this exists

IREP v1.0 answers four questions about **something that already exists**: am I legally allowed to touch it, must I attribute it, is my build a genuine second generation, will industry accept it.

None of those answer a more basic question that appears the moment a model generates its own reasoning:

> Is this middle reasoning an achievement, or just retrieval wearing a costume?

A system that only recites existing chains is a search engine. A system that invents freely is a liar. Only the third kind is worth paying for: **new, but earned**.

So v1.1 adds two scales that point at **generated** artifacts rather than existing ones:

| Scale | Question it answers | Verdict space |
|---|---|---|
| **5 — Emergence** | Given a reference chain, does the produced chain carry an atom the reference does not have, and can that atom be cashed out? | HALLUCINATION / DRIFT / ECHO / EMERGENT / UNKNOWN |
| **6 — Do-Right (DR)** | Did the process that produced the artifact actually do the right thing, or did it produce a plausible receipt after the fact? | PASS / FAIL (exit 0 / 1) |

---

## 1. Scale 5 — Emergence

### 1.1 Five verdicts, evaluated in fixed order

Order is not negotiable. Hallucination first (an invented step makes every later question moot), arrival second (correct-but-irrelevant is not an answer), novelty last.

| Verdict | Meaning | Trigger condition |
|---|---|---|
| `HALLUCINATION` | Invented | Any step cannot be cashed out: cited lemma not in table / symbol absent from AST / anchor does not resolve / a cited lemma's premises are not discharged in its **ancestors** |
| `DRIFT` | Correct but irrelevant | Every step is grounded, but no step arrives at the conclusion |
| `ECHO` | Recitation | Arrives at the conclusion, but every atom on the conclusion's ancestor path also appears in the reference |
| `EMERGENT` | New, and earned | Arrives at the conclusion, and the conclusion's **ancestor path** contains an atom the reference lacks that the casher recognises |
| `UNKNOWN` | Not measurable | No reference supplied, or the reference itself does not reach the conclusion |

`UNKNOWN` is deliberately ranked last. **"Could not establish" must never be allowed to masquerade as "new".**

### 1.2 Novelty is an atomic closed-set difference, not text similarity

`novelty = atoms(path) − atoms(reference)`

Text similarity was tried and paid for: using bigram similarity as the novelty judge misclassified correct answers that were phrased differently, at 14% noise. Rephrasing does not create an atom. Taking one extra step does not create an atom. **Only actually using a different theorem does.**

Two anti-gaming conditions, both mandatory — remove either and the scale is void:

1. **On the conclusion path.** An unrelated theorem parked as decoration does not count. (Measured: judged `ECHO`.)
2. **Cashable.** An invented lemma name does not count. (Caught earlier, as `HALLUCINATION`.)

### 1.3 Three carriers, three cashers — never mixed

| Carrier | Cashes out by | Atoms drawn from |
|---|---|---|
| `LAW` | Lemma table lookup + premise discharge over the ancestor set | formal lemma table |
| `CODE` | AST symbol lookup; a subset is additionally executed | symbols actually defined in the module |
| `TASK` | Real deliverable must be anchorable | anchors in the artifact; bare numbers are not atoms |

Computing `TASK` atoms from a mathematics lemma table produces `UNKNOWN` on all cases. The three atom spaces are disjoint. This was a design error, recorded, not a tuning problem.

### 1.4 Self-validation without self-congratulation

100/100 on a corpus and an `expect` file written by the same author proves only that the author wrote the corpus correctly. Two perturbations the author cannot control are therefore required:

- **Perturbation A** — replace the reference with the middle chain itself → the atom sets coincide, so every `EMERGENT` must collapse to `ECHO`.
- **Perturbation B** — replace one step's `basis` with a nonexistent theorem → every affected case must collapse to `HALLUCINATION`.

If A holds, novelty is not coming from the comparison. If B holds, the casher is not decorative.

**What perturbations cannot do:** they rule out "not comparing at all". They do **not** rule out "the author and the corpus are wrong together". This limit belongs in the code comments, not in a private notebook.

---

## 2. Scale 6 — Do-Right (DR)

A judgment produced after the work is indistinguishable, from the outside, from a judgment produced before it. DR makes the difference machine-checkable: **manifest in, exit code out.**

### 2.1 Five quantities

| Quantity | Machine criterion |
|---|---|
| `Q1` Judgment first | Timestamp of the judgment record precedes the start of execution |
| `Q2` Root-cause grounded | After `source + digest` deduplication, ≥ 3 distinct sources remain |
| `Q3` Process written | Substantive-diff gate — a comment-only bump is `FAIL`; a zero-diff change is legal only through an explicit `no_change` + reason channel |
| `Q4` Acceptance green | Baseline preserved **and** self-check negative samples ≥ 1 (zero negative samples ⇒ `FAIL`) |
| `Q5` Review / sycophancy | Review backlog within SLA; justification may not cite authority utterances as grounds |

### 2.2 Two structural locks

**Ruler hash lock.** The manifest registers the `sha256` of the ruler file at submission time. Acceptance recomputes it. Mismatch ⇒ `FAIL`. Without this, the most profitable attack is to shrink the ruler immediately before running it — every light turns green and the standard has silently changed.

**Three-way carrier check.** Every claimed deliverable must (a) exist on disk and (b) be tracked by git. A file cited three times in the spec but never committed is not a deliverable; it is a rumour.

### 2.3 Tiering, because cost is part of correctness

`S / M / L`. A one-line change does not justify a full re-run. Anything else makes the standard economically self-defeating and guarantees it will be bypassed.

### 2.4 Negative samples are the point

A self-check suite that only contains cases expected to pass tests nothing. The suite ships negative samples that **must** fail or warn. A standard whose own self-check is 100% green on the first run is a standard that has not been tested.

---

## 3. Known boundaries — what these scales cannot judge

Written down so the scales are not mistaken for universal ones.

| Cannot judge | Why |
|---|---|
| **Semantic misuse** | Using a theorem that is recognised and whose premises are discharged, but in the wrong place. The machine sees a cashing-out. |
| **Path quality** | Two chains can both be `EMERGENT`; which is more elegant is not a machine question. |
| **Premise truth** | The scale checks that premises are discharged from ancestors, not that they are true. |
| **Tradeoff calls, taste** | Machine output is "grounded / not grounded", never "good / bad". |

The first row is not hypothetical. A case that proved "continuous image of compact is compact" using Tychonoff's theorem was originally written as a hallucination sample; **the machine judged it `EMERGENT`** — in the machine's view the lemma was recognised and the premises were discharged. It was not a wrong verdict, it was a verdict outside reach. It was reclassified as "premise not discharged" before entering the corpus.

> **A green IREP verdict is not proof of semantic correctness.** Artifacts produced by the lengthen/replace operators carry a mandatory human semantic review before they may be marked done.

---

## 4. Reference implementation status

Stated plainly, because a specification without a runnable gate is a wish:

| Component | Status |
|---|---|
| Five-verdict emergence judge (`free_middle`) | Written and exercised (100 cases + 2 perturbations). **Not yet in this repository.** |
| Chain-optimisation operators — shorten / lengthen / hold / replace (`optimize_ops`) | Written and exercised. **Not yet in this repository.** |
| Do-Right gate (`do_right_check`) | Written; self-judged `PASS` after one genuine `FAIL`. **Not yet in this repository.** |
| Meta-ruler over 12 gates (`meta_ruler`) | Written and exercised. **Not yet in this repository.** |

Until those land, this document is a **specification**, and any claim about reproducing the numbers above must be treated as unverified. The v1.0 gates (`gate/irep_gate.py` et al.) remain fully runnable and unaffected.

**Carrier loss is a known failure mode of this project, not a hypothetical.** A 23 KB operator module was written, used, and then vanished from the working tree with zero git trace within one hour. That is why §2.2 exists and why this table is explicit.

---

## 5. Relationship to the four v1.0 scales

No v1.0 scale is modified, relaxed, or reinterpreted. Licences, attribution, difference-degree and industrial acceptance behave exactly as before. The new scales are **additive** and are evaluated only when the artifact under judgment is *generated* rather than *existing*.

Version note: this is **spec `v1.1.0` / repo `v1.3.0`**, not `v2.0`.

Two numbering series exist and both are stated here so they cannot drift apart again. The **spec series** (`spec/G-*.md`) had only `v1.0`; this document is the second spec entry. The **repository series** was at `v1.2.1` at the time of writing (no git tags exist, so the series is recorded only in commit subjects). Adding two scales to a protocol whose four scales are unchanged is an increment in both series, not a replacement.

`v2.0` would be wrong for a second, independent reason: it implies a `1.x` line of *published releases* that never existed outside `v1.0.0`, and it would announce a continuation of the four-scale protocol while actually introducing something the four scales do not cover at all. The honest label for "same ruler, two new scales" is a minor bump.
