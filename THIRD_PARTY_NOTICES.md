# Third-Party Notices

This file registers third-party mechanisms and dependencies referenced or used by this repository, per the attribution gate (L2) and MIT obligations. Every entry states what was used and what was not.

## morluto/rea — MIT

- **Repository:** https://github.com/morluto/rea
- **License:** MIT (copyright and permission notice preserved by this file; this file also serves as the contribution statement required by the MIT terms)
- **What was used:** mechanisms extracted from the public `docs/` directory — `reconstruction-coverage.md`, `reconstruction-obligation-ledgers.md`, `reconstruction-readiness.md`, `tool-design.md` — 20 mechanisms, each with a source pointer, listed in `gate/irep_gate.py` (`REFERENCE_REA`, ids M01–M20).
- **What was NOT used:** no source code was copied, forked, or modified. The relationship is mechanism-level inspiration, not code-level derivation.
- **Relationship disclosure:** inspiration is not equivalence. The difference-degree judgment for IREP as a second generation is r = 1.143 (7 preserved / 8 added), computed and re-runnable via `python gate/irep_gate.py`; the negative control (a respray clone) scores r = 0.053 and is judged REPLICA by the same gate.
- **Quoted disclaimer honored:** public availability, possession of a file, or access to a debug port does not itself constitute authorization for any operation (G5).

## numpy — BSD 3-Clause

- **Project:** https://numpy.org
- **License:** BSD 3-Clause (https://numpy.org/license.html)
- **Used by:** `proofs/anchor_codec.py` and `proofs/ctrl_rederive.py` — simulation numerics only (array math, FFT). `gate/irep_gate.py` and `proofs/flt_rederive.py` use the Python standard library only.
- **Notice:** required by the BSD 3-Clause terms; no numpy source is vendored in this repository.

## Prior-art references (read, not used)

Eight comparable public efforts were located in the prior-art search completed 2026-10-15 (obligation ledgers, authorization gates, differential replay, e-commerce acceptance services). They informed the no-patent statement in the README; none contributed code or mechanisms to this repository. The full search record is an internal document and is not shipped here.
