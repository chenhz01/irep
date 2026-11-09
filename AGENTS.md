<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# AGENTS.md — IREP 仓库契约

> 本文件是**最高优先级工程规范**，所有开发者（含 AI Agent）改动本仓前必须遵守。
> 只放「不能违背的不变量」和「去哪找细节」的指针；长流程不写在这里。
> 分层做法学自 `ranxianglei/billion-context`（Tier A/B + 按需开文件），
> 一致性清单学自 `vercel-labs/agent-browser`（改一处同更 N 处）。

## Tier A — 每会话必读（不变量）

1. **双许可分区**：代码 Apache-2.0（`LICENSE`），规范/文档/模板 CC BY 4.0（`LICENSE-SPEC`）；**本仓不提供 MIT**。新增文件必须带正确 SPDX 标记，分区以 `NOTICE` 为准。
2. **fail-closed**：`gate/feynman_align_check.py` 在费曼标记缺失时**返回非 0**。不得为让 CI 变绿而删标记或放宽检查。
3. **数字必可复跑**：README / spec 中任何数字或宣称都要有对应命令；没有命令支撑的宣称视为 bug。
4. **版本双轨**：`v1.3.0` 是仓库版本，`spec v1.1.0` 是规范版本——两者刻意不同，不要「对齐」成一个。
5. **零外部依赖**：`gate/` 与 `proofs/` 只用 Python 标准库；新增依赖须先改 `requirements.txt` 并说明理由。
6. **隐私边界**：本仓是公开发布的独立协议，**不含任何私有记忆、身份或内部规则**；不要往任何文件里写这类内容。

## Tier B — 按需打开（don't guess at a procedure, open the file）

| 遇到这件事 | 打开 |
|---|---|
| 改判定逻辑 / 四尺度 | `gate/irep_gate.py` + `spec/G-rules-reverse-engineering-and-attribution-v1.0.md` |
| 把尺子对准自己 | `gate/irep_gate_reversed.py` + `spec/REVERSED-MODE-v1.0.md` |
| 四个 held-out 证明 | `proofs/` 三个 re-derivation 脚本 + `spec/G9-emergence-and-do-right-v1.1.md` |
| 费曼写法与检查器 | `docs/FEYNMAN-4ALIGN.en.md` / `.zh-CN.md`、`gate/feynman_align_check.py` |
| 打包 / 命令入口 | `pyproject.toml`（发行名 `irep-protocol`，**尚未发布到 PyPI**） |
| 提 RFC / 报告安全问题 | `CONTRIBUTING.md`、`SECURITY.md`、`.github/ISSUE_TEMPLATE/` |
| 许可分区细则 | `NOTICE`、`THIRD_PARTY_NOTICES.md` |

**规则**：遇到流程性问题，先按上表开文件，不要凭记忆猜步骤；文件里没有的，去 issue 问，不要自行发明。

## 一致性契约（改一处，必须同更 N 处）

| 你改了 | 必须同更 |
|---|---|
| 任何 `gate/*.py` 的判定刻度 | `spec/G-rules-*.md` + 两份 README 的四尺度描述 + `proofs/` 对应证明 |
| 首屏 / 30 秒命令 | `README.md` **和** `README.zh-CN.md`（中英成对） |
| 新增/删除费曼标记 | `docs/FEYNMAN-4ALIGN.*.md` + `gate/feynman_align_check.py` 的期望值 |
| 许可或 SPDX | `LICENSE` / `LICENSE-SPEC` / `NOTICE` / 两份 README 的 badge 行 |
| 版本号 | 两份 README + `pyproject.toml` + `CITATION.cff` + release notes |
| CI 矩阵 | `.github/workflows/ci.yml` + README 的 Python 版本 badge |

提交前自查：动了左列任意一项而右列没动 = 不允许提交。
同源衍生仓 `chenhz01/irep-video-acceptance-ci` 的许可必须与主仓一致，不得单用 MIT。
