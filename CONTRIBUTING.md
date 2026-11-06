# Contributing to IREP

谢谢愿意花时间。这个仓的规矩只有一条核心：**尺子不能因为改了它自己而变短。**

## 三条红线

1. **每个数字必须可复跑。** README、`spec/`、`docs/` 里出现的任何数值，都要能指到一条命令、一个输入、一个退出码。加数字却不加复跑方式 = 视为 bug。
2. **零依赖是默认值。** `gate/irep_gate.py` 与 `proofs/flt_rederive.py` 只用标准库；只有两个模拟证明需要 `numpy`（`proofs/anchor_codec.py`、`proofs/ctrl_rederive.py`），别把它们变成硬依赖。
3. **G8 使用边界不可削弱。** 武器、恶意软件、未授权监控一律 fail-closed；任何让判定「放宽」的改动都会被拒。

## 上手

```bash
git clone https://github.com/chenhz01/irep
cd irep
python gate/irep_gate.py                    # 四尺度，一个词判决
python gate/irep_gate_reversed.py           # 把尺子掉头对准自己
python gate/feynman_align_check.py --repo . # 四轴对齐结构自检
python gate/feynman_read_assist.py --repo . # 阅读辅助层自检
pip install "numpy>=1.20"                   # 仅两个模拟证明需要
python proofs/anchor_codec.py               # 14 个 held-out 预测
python proofs/flt_rederive.py
python proofs/ctrl_rederive.py
```

**七条命令全部 exit 0 才算绿。** CI 在 Python 3.10 / 3.12 / 3.13 上跑同一组命令（`.github/workflows/ci.yml`）。

## 许可（重要，别踩）

本仓**不提供 MIT**，按文件类型双许可：

| 范围 | 文件 | 许可 |
|---|---|---|
| 代码 | `gate/*.py`、`proofs/*.py` | Apache-2.0 |
| 规范与文档 | `spec/*.md`、`docs/*.md`、两份 README、`INDEX.md` | CC BY 4.0 |

每个文件头都有 `SPDX-License-Identifier`，**以文件上的标记为准**。新增文件请照抄同类文件的标记。第三方机制与依赖登记在 `THIRD_PARTY_NOTICES.md`。

## 提 issue / PR

- 复现不了、数字对不上 → `Bug report` 模板，贴命令、Python 版本、完整输出与退出码
- 认为某一尺度本身不成立 → `Protocol RFC` 模板，请给可复跑反例；被采纳会出 errata 并署名致谢
- 想聊「能不能用在你的场景」→ 去 Discussions，不必开 issue
- PR 请把 CI 七个工具的实跑结果贴进描述

## 响应目标

Issue 首次回应 **48 小时**。若超时，我们会在公开处说明，不悄悄跳过。

> 本工具是工程自检与差异度度量，不是法律意见。对外主张前请人工过一遍边界。
