<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# INDEX — repository map

| Path | What it is | Dependencies | Re-run |
|---|---|---|---|
| `README.md` | protocol + four proofs (English) | — | — |
| `README.zh-CN.md` | protocol + four proofs (Chinese) | — | — |
| `gate/irep_gate.py` | the judgment gate: four scales, one verdict | stdlib only | `python gate/irep_gate.py` |
| `gate/irep_gate_reversed.py` | reversed mode: task reversal (3 verdicts on builds *on* IREP) + process reversal (R1–R5 self-checks); exit code CI-usable | stdlib only | `python gate/irep_gate_reversed.py` |
| `proofs/anchor_codec.py` | Proof 1: double-slit → quantum mechanics, 14 held-out | numpy | `python proofs/anchor_codec.py` |
| `proofs/flt_rederive.py` | Proof 3: Fermat's Last Theorem re-derivation, 4 nodes | stdlib only | `python proofs/flt_rederive.py` |
| `proofs/ctrl_rederive.py` | Appendix: black-box flight-control rebuild | numpy | `python proofs/ctrl_rederive.py` |
| `spec/G-rules-reverse-engineering-and-attribution-v1.0.md` | the rulebook: G1–G8, license matrix, re-derivation four steps | — | — |
| `spec/REVERSED-MODE-v1.0.md` | reversed mode: task reversal, process reversal R1–R5, hard gate R-G1 | — | — |
| `spec/task-card-template-v1.0.md` | task-card template with the H-GATE pre-work hard gate | — | — |
| `docs/FEYNMAN-4ALIGN.zh-CN.md` | the guide contract: four-axis alignment, scorecard, 14 worked examples, 6 analogies, sourced references, 4 self-failure modes (≥10,000 Chinese chars) | — | — |
| `docs/FEYNMAN-4ALIGN.en.md` | English condensed edition: the four definitions verbatim in substance, scorecard + cap rule, 3 worked examples, 4 failure modes, contract-level failure conditions, references (~2,200 words) | — | — |
| `gate/feynman_align_check.py` | structural checker for the four-axis contract (markers, long-form doc, every script's guide head); fails closed | stdlib only | `python gate/feynman_align_check.py --repo .` |
| `spec/G9-emergence-and-do-right-v1.1.md` | scales 5–6: five-verdict emergence judge + Do-Right gate (Q1–Q5, ruler sha256 lock, carrier check, S/M/L). **Specification only — implementation not in this repo** | — | — |
| `docs/EMERGENCE-v1.1.zh-CN.md` | Chinese methodology for scales 5–6: 100-case corpus results, two perturbations, four operators, 12-gate meta-ruler, 19 recorded failure modes, machine boundaries | — | — |
| `gate/feynman_read_assist.py` | Feynman reading-assist layer (FRA): every major section must answer what / why / what-to-do; fails closed | stdlib only | `python gate/feynman_read_assist.py --repo .` |
| `THIRD_PARTY_NOTICES.md` | third-party mechanisms and dependencies register | — | — |
| `LICENSE` | **Apache License 2.0** — covers code (`gate/*.py`, `proofs/*.py`) | — | — |
| `LICENSE-SPEC` | **CC BY 4.0** — covers specification and documentation (full legal code reproduced) | — | — |
| `NOTICE` | dual-licence attribution: scope split, attribution trigger, suggested credit strings | — | — |

**Licence rule:** dual, split by file type — MIT is not offered. Every file carries an `SPDX-License-Identifier` tag; the tag on the file wins over its directory.

Proof 2 (the sieve: active-vendor DENY vs orphan CONDITIONAL, plus the Re-derivation four steps) is demonstrated by `gate/irep_gate.py` cases 3 and 4 — it is a verdict pattern, not a standalone tool.

**Reading order for maintainers:** `README.md` (first screen) → `docs/FEYNMAN-4ALIGN.zh-CN.md` (the contract this repo is judged by) → `gate/feynman_align_check.py` (the machine that enforces it). English readers can take the same path through `docs/FEYNMAN-4ALIGN.en.md`. Any contribution that adds a claim must also add the command that produces it — see §4 of the contract.

Sibling repository: `chenhz01/irep-video-acceptance-ci` (AI-video acceptance sampling reduction, 9.82× measured).

Not in this repository, by design: client data, calibration ledgers, internal amplifiers, identity assets. See "What is NOT in this repo" in the README.
