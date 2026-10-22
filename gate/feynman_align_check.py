#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""feynman_align_check.py — Feynman Guide Four-Axis Alignment checker (FGA-4).

费曼导读（60 秒）：
    这是什么——一个结构校验器：检查一份仓库的导读是否「不缺件」——费曼三问、四对齐长文、星标互推、热门承诺、每个脚本的导读头。
    为什么和你有关——导读缺件不会报错，只会让读者默默离开；人会在赶时间时跳过自检，机器不会。这把「写没写」变成门禁。
    你该怎么办——python gate/feynman_align_check.py --repo .  返 0 = 齐全，返 1 = 缺件（fail-closed）。

Design notes
------------
* stdlib only, no network, deterministic output.
* FAIL-CLOSED: if the target repo does not exist, or a required file is missing,
  the checker exits 1. It never returns 0 for "could not check".
* It checks STRUCTURE, not quality. A document can pass and still be bad prose;
  that part is a human job. See docs/FEYNMAN-4ALIGN.zh-CN.md §13.
* Structural anchors are HTML comments (<!-- FGA4:xxx -->) so they are invisible
  to readers but stable for the machine.
* Bilingual by construction: `*.en.md` is measured in words (default 1800) and
  checked against the English axis names; every other edition is measured in CJK
  characters (default 10000). One counter for both languages would let an edition
  pass on the other edition's volume — the exact metric error logged in §13.4.
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys

CJK = re.compile(r"[\u4e00-\u9fff]")

REQUIRED_MARKERS = ("sister", "trending", "axes")
FEYNMAN_ZH = ("这是什么", "为什么", "怎么办")
FEYNMAN_EN = ("what is this", "why should you care", "what should you do")
AXES_ZH = ("结果", "技术", "代码", "方向")
AXES_EN = ("result", "mechanism", "code", "direction")
WORD = re.compile(r"[A-Za-z][A-Za-z'\u2019-]*")


def is_english(name: str) -> bool:
    """An English edition is any docs file tagged `.en.md` (case-insensitive)."""
    return name.lower().endswith(".en.md")


def read(path: str) -> str:
    with io.open(path, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def find_readmes(repo: str) -> list[str]:
    names = ("README.md", "README.zh-CN.md", "README.zh.md")
    return [os.path.join(repo, n) for n in names if os.path.isfile(os.path.join(repo, n))]


def find_py(repo: str) -> list[str]:
    out = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        out.extend(os.path.join(root, f) for f in files if f.endswith(".py"))
    return sorted(out)


def check_readme(path: str) -> list[str]:
    errs = []
    text = read(path)
    low = text.lower()
    base = os.path.basename(path)

    has_zh = all(k in text for k in FEYNMAN_ZH)
    has_en = all(k in low for k in FEYNMAN_EN)
    if not (has_zh or has_en):
        errs.append(f"{base}: missing Feynman trio (what / why / what-to-do)")

    for marker in REQUIRED_MARKERS:
        if f"<!-- FGA4:{marker} -->" not in text:
            errs.append(f"{base}: missing structural anchor <!-- FGA4:{marker} -->")

    if "<!-- FGA4:axes -->" in text:
        hit = sum(1 for a in AXES_ZH if a in text)
        if hit < 4 and not all(k in low for k in ("result", "mechanism", "code", "direction")):
            errs.append(f"{base}: four-axis block present but axes incomplete ({hit}/4 Chinese)")

    if "docs/FEYNMAN-4ALIGN" not in text:
        errs.append(f"{base}: does not link docs/FEYNMAN-4ALIGN (the long-form contract)")
    return errs


def check_docs(repo: str, min_chars: int, min_words: int) -> list[str]:
    errs = []
    docs_dir = os.path.join(repo, "docs")
    if not os.path.isdir(docs_dir):
        return ["docs/: directory missing (four-axis long-form contract not shipped)"]
    cands = [f for f in os.listdir(docs_dir) if f.startswith("FEYNMAN-4ALIGN")]
    if not cands:
        return ["docs/: no FEYNMAN-4ALIGN* file found"]
    for name in sorted(cands):
        path = os.path.join(docs_dir, name)
        text = read(path)
        if is_english(name):
            # English edition: words, English axis names, English anchors.
            words = len(WORD.findall(text))
            if words < min_words:
                errs.append(f"docs/{name}: {words} words < required {min_words}")
            low = text.lower()
            missing = [a for a in AXES_EN if a not in low]
            if missing:
                errs.append(f"docs/{name}: four-axis sections missing: {', '.join(missing)}")
            for anchor in ("failure condition", "references"):
                if anchor not in low:
                    errs.append(f"docs/{name}: required section missing: {anchor}")
        else:
            cjk = len(CJK.findall(text))
            if cjk < min_chars:
                errs.append(f"docs/{name}: {cjk} Chinese chars < required {min_chars}")
            missing = [a for a in AXES_ZH if a not in text]
            if missing:
                errs.append(f"docs/{name}: four-axis sections missing: {', '.join(missing)}")
            for anchor in ("失效条件", "引用"):
                if anchor not in text:
                    errs.append(f"docs/{name}: required section missing: {anchor}")
    return errs


def check_scripts(repo: str) -> list[str]:
    errs = []
    for path in find_py(repo):
        text = read(path)
        head = text.split('"""')[1] if text.count('"""') >= 2 else ""
        ok = "费曼导读" in head or "feynman" in head.lower()
        if not ok:
            errs.append(f"{os.path.relpath(path, repo)}: module docstring lacks a Feynman guide")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser(description="FGA-4 structural checker (fail-closed)")
    ap.add_argument("--repo", default=".", help="repository root to check")
    ap.add_argument("--min-chars", type=int, default=10000, help="min Chinese chars in a CJK long-form doc")
    ap.add_argument("--min-words", type=int, default=1800, help="min words in an English (.en.md) edition")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        print(f"FAIL  repo not found: {repo}")
        return 1

    readmes = find_readmes(repo)
    if not readmes:
        print("FAIL  no README.md / README.zh-CN.md found")
        return 1

    errs: list[str] = []
    for r in readmes:
        errs.extend(check_readme(r))
    errs.extend(check_docs(repo, args.min_chars, args.min_words))
    errs.extend(check_scripts(repo))

    name = os.path.basename(repo.rstrip("\\/"))
    if errs:
        print(f"FAIL  {name} — {len(errs)} issue(s)")
        for e in errs:
            print("  -", e)
        return 1

    print(f"PASS  {name} — {len(readmes)} README(s), docs contract, all scripts carry a Feynman guide")
    return 0


if __name__ == "__main__":
    sys.exit(main())
