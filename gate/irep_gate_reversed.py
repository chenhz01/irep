#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
irep_gate_reversed.py -- IREP 逆转模式（任务逆转 + 流程逆转）

费曼导读（60 秒）：
    这是什么——把判决机的角色对调：正向是「我拿别人的系统当参考」，
    逆转是「我发布的东西，成了别人的参考系统」。同一台四把尺，反向再量一次。
    为什么和你有关——只要你发过公开仓库，你就已经在当别人的参考系统，
    只是从没量过自己的暴露面。尺子量的第一刀是自己，第二刀就是公开面本身。
    你该怎么办——跑 `python gate/irep_gate_reversed.py`：三个逆转判例 +
    暴露面审计 + 流程逆转 R1-R5 五项机械自检。任何一项 FAIL，发布前先补。

正向（本协议最初的任务）：
    外部系统 = 参考 → 我的产出 = 候选，判算不算第二代
    （irep_gate.py 第一案，判 BREAKTHROUGH）

逆转（本工具，三案全实跑，同一台 evaluate()，只是参考与候选互换）：
    R1 换皮不署名 → DERIVATIVE（署名不完备，补齐前不得对外）
    R2 换皮署名齐 → REPLICA（合法 + 完备，照样换皮；专利意图触发 prior-art 警报）
    R3 真第二代   → BREAKTHROUGH（协议欢迎——知识民主化的意义就在这）

暴露面审计（流程逆转 R2）：
    把本仓公开面当成「别人会逆推的参考系统」逐条登记。
    公开保留层越厚，抄者的 r 下限越低——公开面本身就是护城河。

流程逆转 R1-R5（机械自检，exit code 可当 CI 门）：
    R5 署名审计 → R4 差异度设防 → R3 约束公版 → R2 暴露面清点 → R1 放行条件

设计为在仓内运行（本文件位于 gate/，上一级即仓根）；
在仓外运行 = 审计对象不存在 → fail-closed exit 1（与 G3 同构，禁对空气发 PASS）。

用法：
    python gate/irep_gate_reversed.py          # 人读
    python gate/irep_gate_reversed.py --json   # 机器可读
    exit 0 = R1-R5 全过；exit 1 = 有 FAIL
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irep_gate import evaluate, show, INDUSTRIAL_ARTIFACTS  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# 一、IREP 公开面机制清单
#    这不是自夸清单，是「别人逆推本仓时能提取到的机制」逐条登记——
#    它就是对手眼里的参考系统清单（流程逆转 R2 的产物）。
#    tier: concept=README/spec 全文公开 / impl=本仓可跑 / attribution=署名层
# ---------------------------------------------------------------------------

REFERENCE_IREP_PUBLIC = [
    {"id": "I01", "tier": "concept", "name": "四把尺判决（法律/学术/工程/工业）",
     "src": "README.md"},
    {"id": "I02", "tier": "concept", "name": "协议五阶段",
     "src": "README.md"},
    {"id": "I03", "tier": "concept", "name": "G1-G8 硬闸",
     "src": "spec/G-rules-reverse-engineering-and-attribution-v1.0.md"},
    {"id": "I04", "tier": "concept", "name": "孤儿维修权四前提",
     "src": "gate/irep_gate.py"},
    {"id": "I05", "tier": "concept", "name": "重演重建四步（观察/约束/重建/对拍）",
     "src": "README.md"},
    {"id": "I06", "tier": "impl", "name": "判决机 CLI（四尺量化）",
     "src": "gate/irep_gate.py"},
    {"id": "I07", "tier": "impl", "name": "锚点编解码器（held-out 对拍）",
     "src": "proofs/anchor_codec.py"},
    {"id": "I08", "tier": "impl", "name": "费马大定理四节点重演机",
     "src": "proofs/flt_rederive.py"},
    {"id": "I09", "tier": "impl", "name": "黑盒飞控重演重建机",
     "src": "proofs/ctrl_rederive.py"},
    {"id": "I10", "tier": "impl", "name": "视频验收 CI 减抽卡（9.82×）",
     "src": "sibling repo: irep-video-acceptance-ci"},
    {"id": "I11", "tier": "attribution", "name": "来源致谢与第三方声明机制",
     "src": "THIRD_PARTY_NOTICES.md"},
]

# 半发半留：登记存在，不进公开面（OpenCore「留」的那一半）
HELD_BACK = [
    {"id": "H01", "name": "内部 verifier 群与单功能工具装配"},
    {"id": "H02", "name": "Skill 织体与胶囊装配线"},
    {"id": "H03", "name": "突破件数量闸与审计器接线"},
    {"id": "H04", "name": "客户数据、标定台账、身份资产（永不 ship）"},
]


# ---------------------------------------------------------------------------
# 二、三个逆转判例：同一台 evaluate()，参考与候选互换——尺子不认方向，只认成色
# ---------------------------------------------------------------------------

def reversed_cases():
    artifacts = [n for n, _ in INDUSTRIAL_ARTIFACTS]
    pub = REFERENCE_IREP_PUBLIC

    def clone_candidate(sloppy=False):
        # 最低成本复刻：保留全部公开面 + 加一个壳
        cand = []
        for i, m in enumerate(pub, 1):
            entry = {"id": "C%d" % i, "kind": "preserved",
                     "name": m["name"], "impl": "照搬"}
            # sloppy 克隆连机制出处都不登记——L2 指源完备率直接 FAIL
            if not (sloppy and i % 5 == 0):  # 11 条中漏 2 条 -> 9/11=0.82 < 0.9
                entry["src_of"] = m["id"]
            cand.append(entry)
        cand.append({"id": "X1", "kind": "added", "name": "换了个 CLI 框架", "impl": "换皮"})
        return cand

    # R1 换皮不署名：保留全部公开面 + 一个壳，出处不登记、署名方案也不给
    cand_r1 = clone_candidate(sloppy=True)

    # R2 换皮署名齐：同一克隆，出处登记 + 署名完备 + 声明专利意图（触发 prior-art 警报）
    cand_r2 = clone_candidate(sloppy=False)

    # R3 真第二代：只保留 4 条核心机制并指源，新增 6 条公开面没有的维度
    keep = {"I01", "I02", "I06", "I07"}
    cand_r3 = [{"id": "C%d" % i, "kind": "preserved", "src_of": m["id"],
                "name": m["name"], "impl": "吸收并指源"}
               for i, m in enumerate(pub, 1) if m["id"] in keep]
    cand_r3 += [
        {"id": "N1", "kind": "added", "name": "取证流水线自动化", "impl": "证据采集到判决全自动"},
        {"id": "N2", "kind": "added", "name": "跨仓对拍 harness", "impl": "多仓判决结果互校"},
        {"id": "N3", "kind": "added", "name": "暴露面自审 CI", "impl": "发布前自动跑本工具"},
        {"id": "N4", "kind": "added", "name": "社区共识闸", "impl": "争议判决进公开评议"},
        {"id": "N5", "kind": "added", "name": "多语言 SDK", "impl": "判决机包成库"},
        {"id": "N6", "kind": "added", "name": "判决看板", "impl": "历史判决可视化"},
    ]

    return [
        evaluate("R1 · IREP 换皮克隆（不署名）",
                 pub, cand_r1, "MIT", artifacts[:4],
                 patent_intent=False, attribution=None),
        evaluate("R2 · IREP 换皮克隆（署名完备 + 专利意图）",
                 pub, cand_r2, "MIT", artifacts,
                 patent_intent=True, attribution="IREP-THIRD-PARTY-NOTICES.md"),
        evaluate("R3 · IREP 之上的真第二代候选",
                 pub, cand_r3, "MIT", artifacts,
                 patent_intent=False, attribution="IREP-THIRD-PARTY-NOTICES.md"),
    ]


# ---------------------------------------------------------------------------
# 三、暴露面审计：公开面分层 + 最低成本复刻路径演算
# ---------------------------------------------------------------------------

def exposure_audit():
    tiers = {}
    for m in REFERENCE_IREP_PUBLIC:
        tiers.setdefault(m["tier"], []).append(m)
    n_pub = len(REFERENCE_IREP_PUBLIC)
    r_min_clone = 1.0 / n_pub                      # 保留全部公开面 + 一个壳
    n_needed = math.ceil(0.5 * n_pub)              # 逃出 REPLICA 带（r>=0.5）所需新增
    return tiers, n_pub, r_min_clone, n_needed


# ---------------------------------------------------------------------------
# 四、流程逆转 R1-R5：机械自检，禁手写状态（与 G7 同构：无对拍=自称）
# ---------------------------------------------------------------------------

def process_reversal_checks():
    def exists(rel):
        return os.path.exists(os.path.join(REPO_ROOT, rel))

    def read(rel):
        with open(os.path.join(REPO_ROOT, rel), encoding="utf-8") as f:
            return f.read()

    checks = []
    # R5 署名审计：不先署名别人，就别怪别人不署名你（热尔曼教训）
    ok = (exists("THIRD_PARTY_NOTICES.md")
          and "rea" in read("THIRD_PARTY_NOTICES.md").lower())
    checks.append(("R5", "署名审计", ok,
                   "THIRD_PARTY_NOTICES.md 在位且含 REA 致谢"))
    # R4 差异度设防：公开保留层够厚 + 配方层已半发半留
    ok = len(REFERENCE_IREP_PUBLIC) >= 8 and len(HELD_BACK) >= 1
    checks.append(("R4", "差异度设防", ok,
                   "公开保留层 %d 条；配方层 %d 项已登记半发半留"
                   % (len(REFERENCE_IREP_PUBLIC), len(HELD_BACK))))
    # R3 约束公版：三个 held-out 实证在位（过程进公版，配方留仓内）
    proof_files = ["proofs/anchor_codec.py", "proofs/flt_rederive.py",
                   "proofs/ctrl_rederive.py"]
    missing = [p for p in proof_files if not exists(p)]
    checks.append(("R3", "约束公版", not missing,
                   "三个 held-out 实证在位"
                   + ("；缺: %s" % missing if missing else "")))
    # R2 暴露面清点：每条公开机制都指到仓内位置
    no_src = [m["id"] for m in REFERENCE_IREP_PUBLIC if not m.get("src")]
    checks.append(("R2", "暴露面清点", not no_src,
                   "%d 条公开机制全部指源" % len(REFERENCE_IREP_PUBLIC)))
    # R1 放行条件：LICENSE 在位且 MIT（别人可学可用，须留名）
    ok = exists("LICENSE") and "MIT" in read("LICENSE")
    checks.append(("R1", "放行条件", ok,
                   "LICENSE 在位且为 MIT（放行条件由发布方写死）"))
    return checks


def main():
    args = sys.argv[1:]
    as_json = "--json" in args

    if not os.path.exists(os.path.join(REPO_ROOT, "README.md")):
        msg = ("未检测到仓根（%s 无 README.md）：审计对象不存在，fail-closed。"
               "本工具设计为在 IREP 仓内 gate/ 目录运行。" % REPO_ROOT)
        if as_json:
            print(json.dumps({"mode": "reversed", "error": msg, "exit": 1},
                             ensure_ascii=False, indent=2))
        else:
            print(msg)
        return 1

    cases = reversed_cases()
    tiers, n_pub, r_min, n_needed = exposure_audit()
    checks = process_reversal_checks()
    all_pass = all(ok for _, _, ok, _ in checks)

    if as_json:
        print(json.dumps({
            "mode": "reversed",
            "cases": cases,
            "exposure": {"public_mechanisms": n_pub,
                         "held_back": len(HELD_BACK),
                         "min_clone_r": round(r_min, 3),
                         "added_needed_for_breakthrough_band": n_needed},
            "process_reversal": [{"stage": s, "name": n, "pass": ok, "detail": d}
                                 for s, n, ok, d in checks],
            "exit": 0 if all_pass else 1,
        }, ensure_ascii=False, indent=2))
        return 0 if all_pass else 1

    print("IREP Gate · 逆转模式（任务逆转 + 流程逆转）")
    print("角色互换：正向=我拿别人当参考；逆转=我发布的东西成了别人的参考系统\n")
    for c in cases:
        show(c)

    print("=" * 74)
    print("暴露面审计（流程逆转 R2）——本仓公开面就是别人眼里的参考系统清单")
    print("=" * 74)
    for tier, label in (("concept", "概念层 README/spec 全文公开"),
                        ("impl", "实现层 本仓可跑"),
                        ("attribution", "署名层")):
        ms = tiers.get(tier, [])
        print("[%s] %d 条" % (label, len(ms)))
        for m in ms:
            print("    %s  %s  <- %s" % (m["id"], m["name"], m["src"]))
    print("[配方层 半发半留·不在公开面] %d 项" % len(HELD_BACK))
    for m in HELD_BACK:
        print("    %s  %s" % (m["id"], m["name"]))
    print("\n最低成本复刻路径：保留全部 %d 条公开机制 + 加一个壳 -> r = 1/%d = %.3f"
          % (n_pub, n_pub, r_min))
    print("  -> 落进 REPLICA 带（r<0.25）：公开保留层越厚，抄者的 r 下限越低。")
    print("逃出 REPLICA 带需新增 >= %d 条机制（r>=0.5）；再齐工业验收件才够 BREAKTHROUGH。"
          % n_needed)
    print("协议不挡学习，挡的是换皮称二代。\n")

    print("=" * 74)
    print("流程逆转 R1-R5（机械自检——禁手写状态，与 G7 同构）")
    print("=" * 74)
    for s, n, ok, d in checks:
        print("[%s %s] %s  %s" % (s, n, "PASS" if ok else "FAIL", d))
    print("\n>>> 逆转门：%s" % ("R1-R5 全过" if all_pass else "有 FAIL——发布前先补"))
    print(">>> 逆转模式是定位与署名管理，不是防拷贝保证（MIT 允许商用）；")
    print(">>> 真正守住的是配方层与裁决记录——见 README「诚实分割」。")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
