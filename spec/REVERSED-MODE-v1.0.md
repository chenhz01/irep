# Reversed mode — task reversal + process reversal (v1.0)

> **Feynman guide (60 seconds).** *What is this?* The gate's original job is pointing at somebody else's system. This document flips the chair: once you publish, **your** repository is the reference system somebody else points at. Same four rulers, opposite direction. *Why should you care?* Every public repo is already a reference system — the only question is whether anyone has ever measured its exposure surface. *What should you do?* Run `python gate/irep_gate_reversed.py`: three reversed verdicts, an exposure audit, and five mechanical self-checks (R1–R5). Any FAIL: fix it before shipping.

Companion to `G-rules-reverse-engineering-and-attribution-v1.0.md` (G1–G8). The reversed mode inherits every G-gate and adds one of its own (R-G1, §3).

---

## 1 · Task reversal — the ruler's second cut

The first thing the ruler measured was itself: `gate/irep_gate.py` case 1 takes an external system as the reference and the protocol's own output as the candidate — verdict `BREAKTHROUGH` (r = 1.143).

The second cut turns the chair around. The moment a repository is public, it **is** a reference system: its mechanism list is exactly what an outsider would extract. Task reversal runs the identical `evaluate()` — same four scales, same thresholds — with the roles swapped:

| # | Reversed candidate (built **on IREP's public face**) | L2 attribution | L3 difference | Verdict |
|---|---|---|---|---|
| R1 | Sloppy clone: preserves all 11 public mechanisms, adds one shell, tracks no sources, offers no attribution | 82% → **FAIL** | r = 0.091 | **DERIVATIVE** — attribution incomplete; not shippable until fixed |
| R2 | Clean clone: same 11 + 1 shell, sources tracked, attribution complete, patent intent declared | 100% PASS | r = 0.091 | **REPLICA** — perfectly legal, complete paperwork, still a respray; prior-art warning fires |
| R3 | Genuine second generation: preserves 4 core mechanisms with attribution, adds 6 new dimensions | 100% PASS | r = 1.5 | **BREAKTHROUGH** — welcomed, by design |

What each one teaches:

- **R1** — the difference-degree ruler never gets to speak when attribution fails. Paperwork first, craft second.
- **R2** — the same disease the ruler caught in itself (case 1's negative control), now caught in someone else's build of *us*. Legality and completeness do not make a second generation. G4's prior-art warning fires the moment patent intent is declared against a public repo.
- **R3** — the protocol is not a wall around itself. Knowledge democratization only means something if a genuine second generation built on top of your work is *judged and welcomed*. A ruler that could only judge others downward would be a toll booth, not a standard.

All three cases are produced by `gate/irep_gate_reversed.py` (re-runnable, `--json` available). No verdict in this document is hand-written.

## 2 · Process reversal — the five stages, run backwards

Forward ①→⑤ is the learner's journey: authorize → extract → rebuild → differentiate → accept. Reversed ⑤→① is the publisher's journey. Each reversed stage is a real check with a mechanical status, computed by the tool — never a self-assessment.

| Forward (learn) | Reversed (publish) | The publisher's question | This repo's mechanical status |
|---|---|---|---|
| ⑤ Acceptance & attribution | **R5 Attribution audit** | Have I attributed everything I absorbed — before demanding attribution from anyone building on me? (The Sophie Germain lesson: a name erased by a pen name is the failure mode the ledger exists to prevent.) | PASS — `THIRD_PARTY_NOTICES.md` in place, REA acknowledged |
| ④ Recombination & differentiation | **R4 Difference-degree defense** | Is my public preserved layer thick, and is the recipe layer actually held back? The thicker the public face, the lower a cloner's `r` floor — the public face is the moat. | PASS — 11 public mechanisms registered; 4 held-back items registered (OpenCore) |
| ③ Constraint rebuild | **R3 Constraints in public** | Are my "why this must hold" statements published as runnable comparators? Process in public = anyone can verify equivalence; recipe in public = a toll booth. | PASS — three held-out proofs in place, re-runnable exit 0 |
| ② Mechanism extraction | **R2 Exposure inventory** | What exactly can an outsider extract from my public repo? That list *is* their reference-system manifest. | PASS — 11 mechanisms, each with an in-repo source pointer |
| ① Authorization gate | **R1 Release conditions** | As a reference system, what license and attribution do I require of others? MIT + notices: learn freely, ship commercially, leave the name. | PASS — `LICENSE` in place, MIT |

The reversed pipeline, as the tool prints it:

```
R5 attribution audit → R4 difference-degree defense → R3 constraints in public
→ R2 exposure inventory → R1 release conditions
```

The exposure audit (R2) is the load-bearing artifact. Its arithmetic is the point: a minimum-cost cloner preserves all 11 public mechanisms and adds one shell, landing at `r = 1/11 ≈ 0.091` — deep inside the REPLICA band. Escaping that band requires ≥ 6 genuinely new mechanisms (r ≥ 0.5), and reaching BREAKTHROUGH additionally requires the industrial acceptance artifacts. The protocol does not block learning; it blocks respray claims.

## 3 · Hard gate R-G1 (reversed-mode only)

**The exposure audit must be produced by a runnable tool, never by a feeling.** "I think nothing sensitive leaked" is the same disease G7 cures: an uncompared self-claim. R1–R5 statuses are computed from the repository's actual files; a hand-written ✅ in this document is a defect, not documentation.

Corollary: the tool is fail-closed outside a repository layout (no `README.md` at the computed root → exit 1). An audit with no object gets no PASS.

## 4 · Honest boundary — what reversed mode is not

- **Not anti-copy protection.** MIT permits commercial reuse. The reversed mode does not prevent cloning and does not try to; it manages positioning and attribution.
- **Not a legal opinion.** Same boundary as the forward protocol: engineering self-check, counsel before acting.
- **What it actually defends** is the split the README already declares: the criteria are public, the recipe is not. The gate judges candidates; the calibrated adjudication record for a specific engagement — obligation ledgers, coverage evidence, readiness gates — is deliberately not downloadable. Reversed mode measures whether that split still holds.

## 5 · Relation to the OpenCore split

Reversed mode is the auditing half of "half publish, half hold back":

- **Publish (measured here):** protocol, gate, three proofs, G-rules, this document — every number re-runnable.
- **Hold back (registered, not published):** internal verifier assemblies, skill fabric, breakthrough-count gates, client data and calibration ledgers.

R4 is the check that the held-back half has not quietly leaked into the public face; R3 is the check that the published half is verifiable by anyone. Publish without R3 = claims nobody can check. Hold back without R4 = a moat nobody has measured.

---

*Tool: `gate/irep_gate_reversed.py` (stdlib only, exit code CI-usable: 0 = R1–R5 all pass). This document and the tool are engineering self-checks, not legal advice.*
