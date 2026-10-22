#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-
"""
irep_gate.py -- 工业逆推协议门（Industrial Reverse-Engineering Protocol Gate）
费曼导读（60 秒）：
    这是什么——一台判决机：把「站在别人系统上」的候选放进去，四把尺量完只吐一个词：BREAKTHROUGH / DERIVATIVE / REPLICA / BLOCKED。
    为什么和你有关——「会不会被骂抄袭」这个问题，多数团队靠感觉、律师费或运气回答；这台机器用可复跑的尺度回答，其中一个判例是它量它自己。
    你该怎么办——python gate/irep_gate.py，看四组对照判决；然后把它指向你自己的下一个项目。

回答一个问题：把一个参考系统的逆推产物放大到工程/大工业级，会不会被说是抄袭？

不用嘴判决，用四把尺：
  L1 法律尺  许可证兼容矩阵（MIT/Apache/GPL/专有/unknown -> 允许/注意/禁止）
  L2 学术尺  来源署名完备率（每个保留机制必须指到参考系统出处）
  L3 工程尺  机制差异度（新增机制数 / 保留机制数）
  L4 工业尺  验收件完备度（义务台账/覆盖率/就绪度门/错误追踪/沉默哨兵/证据链）

判决：BLOCKED / REPLICA（换皮）/ DERIVATIVE（衍生，合规）/ BREAKTHROUGH（第二代突破）

规则来源：
  - 机制清单从 morluto/rea 的 docs/ 四份文档真实提取（coverage / obligation-ledgers /
    readiness / tool-design），每条带出处，可复核。
  - 许可证矩阵依据各许可证公开条款的通行解读；本工具是合规自检，不是法律意见。

用法：
  python irep_gate.py demo     # 内置两组对照（BREAKTHROUGH vs REPLICA）
  python irep_gate.py --json   # 输出机器可读判决
"""

import json
import sys
import io

# ---------------------------------------------------------------------------
# 一、参考系统机制清单：REA（morluto/rea，MIT）
#    从 docs/ 四份文档真实提取，每条带出处，可逐条复核
# ---------------------------------------------------------------------------

REFERENCE_REA = [
    # -- reconstruction-coverage.md --
    {"id": "M01", "name": "Evidence 认证前置", "src": "docs/reconstruction-coverage.md",
     "desc": "Evidence IDs 与 bundle manifests 必须先认证才进入评估"},
    {"id": "M02", "name": "Authority 四级置信表", "src": "docs/reconstruction-coverage.md",
     "desc": "shipped-artifact / controlled-replay / live-observation / external 四级证据权威"},
    {"id": "M03", "name": "推断不可晋升", "src": "docs/reconstruction-coverage.md",
     "desc": "passing verifier summary 不能把 inferred 证据晋升为 replay observation"},
    {"id": "M04", "name": "矛盾平局判 unknown", "src": "docs/reconstruction-coverage.md",
     "desc": "同一时刻的等价观察冲突时保持 unknown，不强行裁决"},
    {"id": "M05", "name": "反谄媚记录保留", "src": "docs/reconstruction-coverage.md",
     "desc": "不为迎合调用方声明而修改被引记录，缺失权威时返回 unknown"},
    # -- reconstruction-obligation-ledgers.md --
    {"id": "M06", "name": "保守候选义务", "src": "docs/reconstruction-obligation-ledgers.md",
     "desc": "静态图事实只产生候选义务，不证明运行时行为"},
    {"id": "M07", "name": "义务闭合四条件", "src": "docs/reconstruction-obligation-ledgers.md",
     "desc": "唯一 owner + parser/schema/domain type + case fixtures + comparable verifier"},
    {"id": "M08", "name": "未解保持打开", "src": "docs/reconstruction-obligation-ledgers.md",
     "desc": "矛盾/重复定义/残留未知/缺依赖 -> 义务保持 open 或 failed"},
    {"id": "M09", "name": "无源证据永不闭合", "src": "docs/reconstruction-obligation-ledgers.md",
     "desc": "absence of source Evidence never claims closure"},
    # -- reconstruction-readiness.md --
    {"id": "M10", "name": "九阶段就绪度门", "src": "docs/reconstruction-readiness.md",
     "desc": "discover-classify/diagnose-environment/acquire-authority/static-analysis 等九阶段"},
    {"id": "M11", "name": "内部 verifier 不进公共面", "src": "docs/reconstruction-readiness.md",
     "desc": "报告评估器是仓库自有 verifier，不作为公共 CLI/MCP 工具暴露"},
    {"id": "M12", "name": "陈旧重放拒绝证明", "src": "docs/reconstruction-readiness.md",
     "desc": "proves stale/tampered replay rejection"},
    {"id": "M13", "name": "CI 门禁留 artifact", "src": "docs/reconstruction-readiness.md",
     "desc": "CI 跑 verify:readiness，保留完整机器可读报告为 artifact"},
    # -- tool-design.md --
    {"id": "M14", "name": "六种工具形态", "src": "docs/tool-design.md",
     "desc": "inspect/search/trace/compare/workflow/observe 任务形态分类"},
    {"id": "M15", "name": "原语优先组合", "src": "docs/tool-design.md",
     "desc": "primitive 报可复用事实，workflow 仅在重复出现多源结果时组合"},
    {"id": "M16", "name": "反编排语言", "src": "docs/tool-design.md",
     "desc": "自定义编排语言/重放引擎需有原语满足不了的观察需求才引入"},
    {"id": "M17", "name": "缺失覆盖即 unknown", "src": "docs/tool-design.md",
     "desc": "Missing coverage is unknown, not absence"},
    {"id": "M18", "name": "观察推导推断三分", "src": "docs/tool-design.md",
     "desc": "observed / derived / inferred 关系严格分离"},
    {"id": "M19", "name": "反臆测限制", "src": "docs/tool-design.md",
     "desc": "assumed agent budget 不足以成为设置 limit 的理由"},
    {"id": "M20", "name": "能力如实声明", "src": "docs/tool-design.md",
     "desc": "process/filesystem/network/UI/mutation 效果如实声明并强制执行"},
]

# ---------------------------------------------------------------------------
# 二、候选系统机制清单
#    kind=preserved -> 保留并吸收参考机制（必须指源）
#    kind=added     -> 参考系统没有的新增机制（差异度的来源）
# ---------------------------------------------------------------------------

CANDIDATE_IREP = [
    # -- 保留层（来自 REA，正明版实现，全部指源）--
    {"id": "P1", "kind": "preserved", "src_of": "M17", "name": "未知独立成类硬规约",
     "impl": "anchor_codec 四构件之一：未解决必须保持 unknown，禁当不存在"},
    {"id": "P2", "kind": "preserved", "src_of": "M03", "name": "对拍验收（held-out）",
     "impl": "anchor_codec held-out 对拍 + forge-code 差分执行 + render-diff-harness 帧对拍"},
    {"id": "P3", "kind": "preserved", "src_of": "M07", "name": "证据链闭环",
     "impl": "claim_ledger.py + claim-verification-chain：主张->证据->验证全链留痕"},
    {"id": "P4", "kind": "preserved", "src_of": "M11", "name": "半发半留",
     "impl": "GitHub 发表两原则 A藏配方/B送服务，内部 verifier 不进公共面"},
    {"id": "P5", "kind": "preserved", "src_of": "M05", "name": "反谄媚记录",
     "impl": "F11 反谄媚搭档协议 RA-1..RA-5，异议四件套"},
    {"id": "P6", "kind": "preserved", "src_of": "M13", "name": "沉默失败哨兵",
     "impl": "silence_gate.py + silent_failure_sniffer.py：静默失败当日报告"},
    {"id": "P7", "kind": "preserved", "src_of": "M15", "name": "原语优先",
     "impl": "tools/ 30+ 单功能工具，Skill 组合而非大单体"},
    # -- 新增层（REA 完全没有的维度：合规判决 + 差异度量 + 专利预警 + 授权闸）--
    {"id": "N1", "kind": "added", "name": "三把尺抄袭判决机",
     "impl": "本工具：法律/学术/工程/工业四尺量化，REPLICA/DERIVATIVE/BREAKTHROUGH"},
    {"id": "N2", "kind": "added", "name": "机制差异度计算",
     "impl": "新增/保留比率 r，低于门槛禁称第二代"},
    {"id": "N3", "kind": "added", "name": "许可证兼容矩阵",
     "impl": "MIT/Apache/GPL/专有/unknown -> 允许/注意/禁止，unknown 一律 fail-closed"},
    {"id": "N4", "kind": "added", "name": "署名方案生成",
     "impl": "来源声明 + 贡献陈述自动生成，无声明禁入对外文本"},
    {"id": "N5", "kind": "added", "name": "专利 prior-art 预警",
     "impl": "公开仓库=现有技术，申请专利前强制检索参考系统，防新颖性击穿"},
    {"id": "N6", "kind": "added", "name": "逆推授权闸",
     "impl": "DISCLAIMER 原则落成机器：只逆推授权目标，未授权目标一律拒绝"},
    {"id": "N7", "kind": "added", "name": "义务台账正明版",
     "impl": "IREP 台账：每条逆推结论带义务记录，闭合四条件用 held-out 对拍做 verifier"},
    {"id": "N8", "kind": "added", "name": "突破件装配线",
     "impl": "把 tools/30+ 与 skills/130 串成 IREP 五阶段，零件->机器"},
]

# 反面对照：一个把 REA 机制原样打包只加一个壳的候选（应判 REPLICA）
CANDIDATE_CLONE = [
    {"id": "P1", "kind": "preserved", "src_of": "M17", "name": "未知独立成类", "impl": "照搬"},
    {"id": "P2", "kind": "preserved", "src_of": "M03", "name": "对拍验收", "impl": "照搬"},
    {"id": "P3", "kind": "preserved", "src_of": "M07", "name": "证据链闭环", "impl": "照搬"},
    {"id": "P4", "kind": "preserved", "src_of": "M11", "name": "半发半留", "impl": "照搬"},
    {"id": "P5", "kind": "preserved", "src_of": "M05", "name": "反谄媚记录", "impl": "照搬"},
    {"id": "P6", "kind": "preserved", "src_of": "M13", "name": "沉默失败哨兵", "impl": "照搬"},
    {"id": "P7", "kind": "preserved", "src_of": "M15", "name": "原语优先", "impl": "照搬"},
    {"id": "P8", "kind": "preserved", "src_of": "M14", "name": "六种工具形态", "impl": "照搬"},
    {"id": "P9", "kind": "preserved", "src_of": "M16", "name": "反编排语言", "impl": "照搬"},
    {"id": "P10", "kind": "preserved", "src_of": "M18", "name": "观察推导推断三分", "impl": "照搬"},
    {"id": "P11", "kind": "preserved", "src_of": "M19", "name": "反臆测限制", "impl": "照搬"},
    {"id": "P12", "kind": "preserved", "src_of": "M20", "name": "能力如实声明", "impl": "照搬"},
    {"id": "P13", "kind": "preserved", "src_of": "M01", "name": "Evidence 认证前置", "impl": "照搬"},
    {"id": "P14", "kind": "preserved", "src_of": "M02", "name": "Authority 四级置信表", "impl": "照搬"},
    {"id": "P15", "kind": "preserved", "src_of": "M06", "name": "保守候选义务", "impl": "照搬"},
    {"id": "P16", "kind": "preserved", "src_of": "M08", "name": "未解保持打开", "impl": "照搬"},
    {"id": "P17", "kind": "preserved", "src_of": "M09", "name": "无源证据永不闭合", "impl": "照搬"},
    {"id": "P18", "kind": "preserved", "src_of": "M10", "name": "九阶段就绪度门", "impl": "照搬"},
    {"id": "P19", "kind": "preserved", "src_of": "M12", "name": "陈旧重放拒绝证明", "impl": "照搬"},
    {"id": "N1", "kind": "added", "name": "中文界面", "impl": "翻译了界面文案"},
]

# ---------------------------------------------------------------------------
# 二-b、真实场景案例（2026-10-16 加入：孤儿系统/维修权与版权人活跃软件的分界）
# ---------------------------------------------------------------------------

# 场景 A：逆推某头部专有图像软件本体（版权人活跃）
REF_PS = [
    {"id": "S01", "name": "图层/蒙版/混合模式体系", "src": "某头部图像软件公开文档与公开教程"},
    {"id": "S02", "name": "某位图文档格式（公开规格书）", "src": "该格式公开规格文档"},
    {"id": "S03", "name": "工具栏交互布局", "src": "某头部图像软件公开界面"},
]
CAND_PS = [
    {"id": "A1", "kind": "preserved", "src_of": "S01", "name": "图层模型", "impl": "自建图层引擎"},
    {"id": "A2", "kind": "preserved", "src_of": "S02", "name": "位图文档格式读写", "impl": "按公开规格实现"},
    {"id": "A3", "kind": "preserved", "src_of": "S03", "name": "界面布局", "impl": "复刻工作区"},
    {"id": "A4", "kind": "added", "name": "自有滤镜集", "impl": "自研算法"},
]

# 场景 B：孤儿工控固件（原厂破产，设备持有者授权维护）
REF_ORPHAN = [
    {"id": "O01", "name": "专有通信协议报文格式", "src": "原厂随机器交付的私有协议"},
    {"id": "O02", "name": "专有固件镜像格式", "src": "设备内固件"},
    {"id": "O03", "name": "原厂上位机操作逻辑", "src": "原厂配套软件"},
]
CAND_ORPHAN = [
    {"id": "B1", "kind": "preserved", "src_of": "O01", "name": "协议兼容层", "impl": "按报文逆推重实现，仅用于维护通信"},
    {"id": "B2", "kind": "preserved", "src_of": "O02", "name": "固件解析器", "impl": "逆推格式，只读不写原厂签名区"},
    {"id": "B3", "kind": "added", "name": "现代替代上位机", "impl": "重写 UI 与配置管理，跨平台"},
    {"id": "B4", "kind": "added", "name": "数据迁移导出", "impl": "专有格式导出为开放 CSV/Parquet"},
    {"id": "B5", "kind": "added", "name": "远程监控面板", "impl": "原厂没有的功能"},
]

# ---------------------------------------------------------------------------
# 三、许可证矩阵（通行条款解读；合规自检，不是法律意见）
# ---------------------------------------------------------------------------

LICENSE_MATRIX = {
    "MIT":        {"verdict": "ALLOW", "cond": "保留版权声明+许可声明；可闭源商用；建议 THIRD_PARTY_NOTICES 登记"},
    "Apache-2.0": {"verdict": "ALLOW", "cond": "保留版权+许可+NOTICE；专利条款明示；修改文件需声明"},
    "BSD-2/3":    {"verdict": "ALLOW", "cond": "保留版权+许可声明；禁用贡献者姓名背书"},
    "public-knowledge": {"verdict": "ALLOW", "cond": "公版/教科书/学术公开知识无版权负担；学术尺（L2）仍独立判决署名"},
    "mixed":      {"verdict": "CHECK", "cond": "混合来源须逐件登记 THIRD_PARTY_NOTICES；含专有组件则整件 DENY"},
    "orphaned-eula": {"verdict": "CONDITIONAL",
                      "cond": "孤儿系统维修权：须同时满足四前提——①原厂已消亡/破产/停更多年（孤儿事实可证）"
                              "②逆推方是设备持有者或持有者书面授权 ③目的仅限互操作/维护/迁移，"
                              "不复制不分发原代码 ④保留原版权声明。缺一即 BLOCKED；商业分发前仍须律师确认"},
    "GPL-2.0/3.0": {"verdict": "DENY",  "cond": "Copyleft 传染：衍生作品须同许可证开源，闭源商用禁止"},
    "AGPL-3.0":   {"verdict": "DENY",   "cond": "网络使用即分发，SaaS 也传染，闭源商用禁止"},
    "proprietary": {"verdict": "DENY",  "cond": "无授权，禁止任何层级复制"},
    "unknown":    {"verdict": "DENY",   "cond": "许可不明一律 fail-closed，先查清再动"},
}

# 孤儿系统四前提（orphaned-eula 的放行锚点，缺一即 BLOCKED）
ORPHAN_PRECONDITIONS = [
    "孤儿事实可证：原厂已消亡/破产/停更多年（工商注销记录或官方停更公告）",
    "授权链完整：逆推方是设备持有者，或持有者书面授权（范围含互操作/维护）",
    "目的限定：仅互操作/维护/数据迁移；不复制、不分发原代码，不对外销售原系统",
    "声明保留：产物保留原版权与许可声明；商业分发前律师确认",
]

# 工业验收件清单（对照 REA 工业四件 + 正明已有哨兵）
INDUSTRIAL_ARTIFACTS = [
    ("obligation_ledger", "义务台账：每条逆推结论带闭合条件记录"),
    ("coverage_gate",     "覆盖率门：缺失覆盖判 unknown 不是 absence"),
    ("readiness_gate",    "就绪度门：九阶段 conformance，CI 强制执行"),
    ("error_tracking",    "错误追踪：用户可见错误逐条 CSV 台账"),
    ("silence_sentinel",  "沉默哨兵：静默失败当日报告"),
    ("claim_chain",       "证据链：主张->证据->验证全链留痕"),
]


def l1_legal(license_id):
    row = LICENSE_MATRIX.get(license_id)
    if row is None:
        row = LICENSE_MATRIX["unknown"]
    return {"license": license_id, "verdict": row["verdict"], "cond": row["cond"]}


def l2_academic(candidate, reference):
    """每个 preserved 机制必须能指回参考系统的一条机制。"""
    ref_ids = {m["id"] for m in reference}
    preserved = [m for m in candidate if m["kind"] == "preserved"]
    if not preserved:
        return {"rate": 1.0, "n": 0, "orphans": [], "verdict": "PASS"}
    orphans = [m["id"] for m in preserved if m.get("src_of") not in ref_ids]
    rate = 1.0 - len(orphans) / len(preserved)
    verdict = "PASS" if rate >= 0.9 else "FAIL"
    return {"rate": rate, "n": len(preserved), "orphans": orphans, "verdict": verdict}


def l3_engineering(candidate):
    preserved = [m for m in candidate if m["kind"] == "preserved"]
    added = [m for m in candidate if m["kind"] == "added"]
    r = len(added) / max(len(preserved), 1)
    if r < 0.25:
        band = "REPLICA"
    elif r < 0.5:
        band = "DERIVATIVE"
    else:
        band = "BREAKTHROUGH-BAND"
    return {"preserved": len(preserved), "added": len(added), "r": round(r, 3), "band": band}


def l4_industrial(candidate_artifacts):
    have = set(candidate_artifacts)
    got = [name for name, _ in INDUSTRIAL_ARTIFACTS if name in have]
    missing = [name for name, _ in INDUSTRIAL_ARTIFACTS if name not in have]
    score = len(got)
    verdict = "PASS" if score >= 4 else "FAIL"
    return {"score": score, "total": len(INDUSTRIAL_ARTIFACTS),
            "got": got, "missing": missing, "verdict": verdict}


def verdict_of(l1, l2, l3, l4, patent_intent):
    if l1["verdict"] == "DENY":
        return "BLOCKED", "许可证不允许：先解决 L1，其余尺免谈"
    if l2["verdict"] == "FAIL":
        return "DERIVATIVE", "署名不完备：补来源声明后才可对外"
    if l3["band"] == "REPLICA":
        return "REPLICA", "换皮：差异度低于门槛，禁称第二代/突破"
    conditional = l1["verdict"] == "CONDITIONAL"
    if l3["band"] == "BREAKTHROUGH-BAND" and l4["verdict"] == "PASS":
        if conditional:
            return ("CONDITIONAL-BREAKTHROUGH",
                    "孤儿维修权场景：四尺均过，但放行以四前提全锚为条件，缺一即 BLOCKED")
        return "BREAKTHROUGH", "第二代突破候选：差异度达标且工业验收件完备"
    if conditional:
        return "CONDITIONAL-DERIVATIVE", "孤儿维修权场景：可交付，但放行以四前提全锚为条件"
    return "DERIVATIVE", "衍生品：合法可交付，但未达突破门槛"


def evaluate(name, reference, candidate, license_id, artifacts, patent_intent=False,
             attribution=None, scenario="active-vendor"):
    l1 = l1_legal(license_id)
    # 场景闸：专有软件 + 版权人活跃维权 = 死路（换场景，不是换目标）
    #         孤儿系统（原厂消亡）+ 持有者授权 = 有条件放行（orphaned-eula 走 CONDITIONAL）
    if license_id == "proprietary" and scenario == "active-vendor":
        l1 = {"license": license_id, "verdict": "DENY",
              "cond": "专有软件且版权人活跃维权：EULA 禁止逆向工程。"
                      "此时的问题不是尺子够不够严，是场景错了——换场景，不是换目标"}
    l2 = l2_academic(candidate, reference)
    l3 = l3_engineering(candidate)
    l4 = l4_industrial(artifacts)
    v, why = verdict_of(l1, l2, l3, l4, patent_intent)
    warnings = []
    if patent_intent:
        warnings.append("已声明专利意图：参考系统为公开仓库=现有技术（prior art），"
                        "申请前必须检索，否则新颖性可能被击穿")
    if l1["verdict"] == "CHECK":
        warnings.append("混合来源：须逐件登记 THIRD_PARTY_NOTICES；含专有组件则整件 DENY")
    if l1["verdict"] == "CONDITIONAL":
        for i, p in enumerate(ORPHAN_PRECONDITIONS, 1):
            warnings.append(f"孤儿维修权前提{i}/4：{p}")
    if l1["verdict"] == "ALLOW" and (attribution is None):
        warnings.append("未提供署名方案：MIT/Apache 允许商用但须保留版权声明，"
                        "建议生成 THIRD_PARTY_NOTICES 与贡献陈述")
    return {"candidate": name, "license_check": l1, "attribution_check": l2,
            "engineering_diff": l3, "industrial_check": l4,
            "verdict": v, "why": why, "warnings": warnings}


def show(res):
    print("=" * 74)
    print(f"候选系统：{res['candidate']}")
    print("=" * 74)
    l1, l2, l3, l4 = (res["license_check"], res["attribution_check"],
                      res["engineering_diff"], res["industrial_check"])
    print(f"[L1 法律尺] {l1['license']:<12} -> {l1['verdict']}")
    print(f"            {l1['cond']}")
    print(f"[L2 学术尺] 保留机制 {l2['n']} 条，指源完备率 {l2['rate']*100:.0f}%"
          f" -> {l2['verdict']}"
          + (f"  孤儿: {l2['orphans']}" if l2["orphans"] else ""))
    print(f"[L3 工程尺] 保留 {l3['preserved']} / 新增 {l3['added']} -> "
          f"差异度 r={l3['r']} -> {l3['band']}")
    print(f"[L4 工业尺] 验收件 {l4['score']}/{l4['total']} -> {l4['verdict']}"
          + (f"  缺: {l4['missing']}" if l4["missing"] else ""))
    for w in res["warnings"]:
        print(f"[WARN] {w}")
    print(f"\n>>> 判决：{res['verdict']}")
    print(f">>> 理由：{res['why']}")
    print()


def main():
    args = sys.argv[1:]
    as_json = "--json" in args

    irep_artifacts = [n for n, _ in INDUSTRIAL_ARTIFACTS]  # 六件全齐（设计目标）
    clone_artifacts = ["obligation_ledger", "coverage_gate", "readiness_gate",
                       "error_tracking"]

    cases = [
        evaluate("IREP 第二代（正明工业逆推协议）",
                 REFERENCE_REA, CANDIDATE_IREP, "MIT", irep_artifacts,
                 patent_intent=False, attribution="IREP-THIRD-PARTY-NOTICES.md"),
        evaluate("REA 换皮克隆（反面对照）",
                 REFERENCE_REA, CANDIDATE_CLONE, "MIT", clone_artifacts,
                 patent_intent=True, attribution=None),
        evaluate("逆推某头部专有图像软件本体（版权人活跃）",
                 REF_PS, CAND_PS, "proprietary", irep_artifacts,
                 scenario="active-vendor", attribution="无——未授权不得署名商用"),
        evaluate("孤儿工控固件维护（原厂破产+持有者授权）",
                 REF_ORPHAN, CAND_ORPHAN, "orphaned-eula", irep_artifacts,
                 scenario="abandoned-repair", attribution="ORPHAN-THIRD-PARTY-NOTICES.md"),
    ]
    if as_json:
        print(json.dumps({"cases": cases}, ensure_ascii=False, indent=2))
        return 0
    print("IREP Gate -- 工业逆推协议门  判决：抄不抄 / 是不是第二代")
    print("参考系统机制清单来源：morluto/rea docs/ 四份文档真实提取（20 条）\n")
    for c in cases:
        show(c)
    print("注：本工具是合规自检与差异度度量，不构成法律意见；"
          "对外主张前仍须人工过发表五问。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
