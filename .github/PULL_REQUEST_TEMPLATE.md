## 这个 PR 改了什么

<!-- 一句话。如果是文档改动，请说明改的是英文版、中文版，还是两份都要同步。 -->

## 复跑证据（必填）

本仓契约：每个数字可复跑、每个判决可被同一把尺子质疑。请贴出你实际跑过的命令与退出码：

```bash
python gate/irep_gate.py            # exit ?
python gate/feynman_align_check.py --repo .   # exit ?
```

- [ ] 7 个工具全部跑过且 exit 0
- [ ] 若改了 `spec/` 或 `docs/`，英文与中文两份一致性已检查
- [ ] 若改了 `gate/` 或 `proofs/`，`docs/FEYNMAN-4ALIGN.*` 的四轴账本已同步
- [ ] 新增/修改文件都带 `SPDX-License-Identifier`（代码 Apache-2.0，规范与文档 CC BY 4.0）

## 使用边界

- [ ] 本次改动没有削弱 G8（武器 / 恶意软件 / 未授权监控一律 fail-closed）

## 许可确认

本仓**不提供 MIT**。代码 Apache-2.0，规范与文档 CC BY 4.0，以文件上的 SPDX 标记为准。
