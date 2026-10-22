#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""feynman_read_assist.py — 费曼助读层结构检查器（FRA, Feynman Reading Assist）。

费曼导读：一份介绍（README）如果读的人要翻到第三屏才知道"这东西跟我有什么关系"，
它就是不合格交付。所以本仓库要求每个主章节都配一行「费曼三问」——
这是什么 / 为什么和你有关 / 你该怎么办。本脚本用机器判这一层在不在，
而不是靠作者自觉。

输入：仓库根目录（--repo）。输出：PASS / FAIL + 逐条缺失原因。
退出码：0 = 助读层完整；1 = 缺失（熔断，禁止推送）；2 = 用法错误。
失效条件：只查结构，不查语义——三问填得对不对它管不了，那是人的活。

引用：费曼转译铁律（2026-09-15）；本仓库 FGA-4 四轴契约中的「结果轴」。
"""

from __future__ import annotations

import argparse
import os
import re
import sys

LAYER = "<!-- FRA:layer -->"
START = "<!-- FRA:start -->"
END = "<!-- FRA:end -->"
SEC = re.compile(r"<!--\s*FRA:sec:([a-z0-9][a-z0-9-]*)\s*-->")

HEADERS_EN = ("What is this", "Why should you care", "What to do")
HEADERS_ZH = ("这是什么", "为什么和你有关", "你该怎么办")

MIN_ROWS = 6
MIN_CELL = 8
MIN_SLUGS = 5
COLS = 4  # section | what is this | why should you care | what to do


def is_english(name: str) -> bool:
    base = os.path.basename(name)
    return ".zh" not in base.lower()


def read(path: str) -> str:
    with open(path, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def find_readmes(repo: str) -> list[str]:
    out = []
    for name in ("README.md", "README.zh-CN.md"):
        p = os.path.join(repo, name)
        if os.path.isfile(p):
            out.append(p)
    return out


def parse_rows(block: str) -> list[list[str]]:
    """Data rows of the first markdown table in the block, header/separator removed."""
    rows: list[list[str]] = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells:
            continue
        if all(re.fullmatch(r":?-{2,}:?", c.replace(" ", "")) for c in cells):
            continue  # separator row
        if all(c.replace("-", "").replace(" ", "") == "" for c in cells):
            continue
        rows.append(cells)
    return rows[1:]  # drop header row


def check_readme(path: str) -> list[str]:
    base = os.path.basename(path)
    text = read(path)
    errs: list[str] = []

    if LAYER not in text:
        errs.append(f"{base}: missing Feynman reading-layer anchor {LAYER}")
    if START not in text or END not in text:
        errs.append(f"{base}: missing {START} / {END} block delimiters")
        return errs

    block = text.split(START, 1)[1].split(END, 1)[0]
    headers = HEADERS_EN if is_english(path) else HEADERS_ZH
    for h in headers:
        if h not in block:
            errs.append(f"{base}: reading layer missing column '{h}'")

    rows = parse_rows(block)
    if len(rows) < MIN_ROWS:
        errs.append(f"{base}: reading layer has {len(rows)} rows < required {MIN_ROWS}")
    for i, cells in enumerate(rows, start=1):
        if len(cells) != COLS:
            errs.append(f"{base}: row {i} has {len(cells)} cells, need {COLS} (section/what/why/do)")
            continue
        for j, c in enumerate(cells[1:], start=1):
            plain = re.sub(r"[\[\]()#*`]", "", c).strip()
            if len(plain) < MIN_CELL:
                errs.append(f"{base}: row {i} answer {j} too thin ({len(plain)} chars) — not a reading aid")

    slugs = SEC.findall(text)
    if len(slugs) < MIN_SLUGS:
        errs.append(f"{base}: {len(slugs)} FRA:sec markers < required {MIN_SLUGS}")
    joined = "\n".join(" ".join(r) for r in rows)
    for slug in slugs:
        if slug not in joined:
            errs.append(f"{base}: section marker FRA:sec:{slug} has no row in the reading layer")

    return errs


def main() -> int:
    ap = argparse.ArgumentParser(description="FRA — Feynman reading-assist layer checker (fail-closed)")
    ap.add_argument("--repo", default=".", help="repository root to check")
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

    name = os.path.basename(repo.rstrip("\\/"))
    if errs:
        print(f"FAIL  {name} — {len(errs)} issue(s)")
        for e in errs:
            print("  -", e)
        return 1

    total = sum(len(parse_rows(read(r).split(START, 1)[1].split(END, 1)[0])) for r in readmes)
    print(f"PASS  {name} — {len(readmes)} README(s), {total} reading-aid rows, all sections covered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
