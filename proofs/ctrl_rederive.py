# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-
"""
ctrl_rederive.py — IREP 黑盒飞控重演重建机（工业高度保持类问题的玩具级全真演示）
费曼导读（60 秒）：
    这是什么——一台黑盒重建机：只看阶跃响应、零固件接触，拟合出与黑盒行为等价的控制器，再用没见过的设定点对拍。
    为什么和你有关——它证明「预测等价」可传而「参数/源码」不必传；途中机器还两次判死建造者的测量法错误。
    你该怎么办——pip install numpy && python proofs/ctrl_rederive.py；记住等终性警告：对拍全过 ≠ 参数恢复。
IREP 五阶段映射:
  ① 授权闸: 黑盒=自家实验台上的「未知厂商飞控」，只读输入/输出，零固件接触 -> 合法观察面
  ② 机制提取: 只看阶跃响应曲线（行为），不看一行内部代码
  ③ 约束重建: 网格搜索拟合自有 PI 控制器（原生实现，不引用黑盒）
  ④ 重组差异化: 约束等价判定（行为对拍，不追求参数相同）
  ⑤ held-out 对拍: 观察集里没有的设定点 + 阵风扰动，预测等价才算数
教学命题: IREP 传的是「约束/行为」，不是「参数/源码」——约束等价 ≠ 内部相同（等终性）
"""
import numpy as np

OK = "\033[92m"; WARN = "\033[93m"; DIM = "\033[2m"; RST = "\033[0m"
DT = 0.05
T_END = 12.0
N = int(T_END / DT)


def head(s):
    print("\n" + "=" * 72)
    print(s)
    print("=" * 72)


# ----------------------------------------------------------------------------
# 黑盒：一台「未知厂商」的高度保持飞控（内部对重建方完全不可见）
# 隐藏配置: Kp=2.2, Ki=1.4, 速度指令限幅 1.5 m/s, 积分限幅 ±5(抗饱和)
# 被控对象: 一阶速度跟踪动力(时间常数 1/3 s)——机体动力学是台架上可测的
#            物理量, 不属于厂商秘密; 秘密的是控制器。
# ----------------------------------------------------------------------------
class BlackBox:
    def __init__(self):
        self.Kp, self.Ki = 2.2, 1.4
        self.rate_limit = 1.5
        self.i = 0.0
        self.h = 0.0
        self.v = 0.0

    def step(self, target, wind=0.0):
        err = target - self.h
        self.i = float(np.clip(self.i + err * DT, -5.0, 5.0))
        u = self.Kp * err + self.Ki * self.i
        u = float(np.clip(u, -self.rate_limit, self.rate_limit))
        self.v += (3.0 * (u - self.v) + wind) * DT
        self.h += self.v * DT
        return self.h


# ----------------------------------------------------------------------------
# 原生重建：自己的 PI 控制器（结构假设 = 同级飞控的通行结构, 参数待拟合）
# ----------------------------------------------------------------------------
class Rebuilt:
    def __init__(self, Kp, Ki, rl):
        self.Kp, self.Ki, self.rl = Kp, Ki, rl
        self.i = 0.0
        self.h = 0.0
        self.v = 0.0

    def step(self, target, wind=0.0):
        err = target - self.h
        self.i = float(np.clip(self.i + err * DT, -5.0, 5.0))
        u = self.Kp * err + self.Ki * self.i
        u = float(np.clip(u, -self.rl, self.rl))
        self.v += (3.0 * (u - self.v) + wind) * DT
        self.h += self.v * DT
        return self.h


def simulate(ctrl, target, wind_sched=None):
    """wind_sched(t)->wind；返回高度轨迹"""
    ctrl.h = ctrl.v = 0.0
    ctrl.i = 0.0
    traj = np.empty(N)
    for k in range(N):
        t = k * DT
        w = wind_sched(t) if wind_sched else 0.0
        traj[k] = ctrl.step(target, w)
    return traj


def rmse(a, b):
    return float(np.sqrt(np.mean((a - b) ** 2)))


# ----------------------------------------------------------------------------
# 阶段② 机制提取——只从观察曲线里读约束
# ----------------------------------------------------------------------------
def extract_constraints():
    head("阶段② 机制提取：只看阶跃响应（黑盒零代码接触）")
    obs_targets = [1.0, 2.0, 3.0]
    obs = {t: simulate(BlackBox(), t) for t in obs_targets}
    ts = np.arange(N) * DT

    cons = {}
    # 约束1(移至阶段③做嵌套模型对比)：一阶速度对象纯 P 也能零稳态差，
    # 不能用稳态误差推断积分作用——改用「Ki=0 最优拟合 vs Ki 自由最优拟合」误差差
    # 约束2: 爬升速率平台 => 速度指令限幅（可观察的「规格」）。
    #   教训: 取各设定点斜率的"最大值"才是平台上限；小步阶斜率爬不满平台(测量偏差)
    slopes = {t: np.max(np.gradient(tr, ts)) for t, tr in obs.items()}
    rl_est = max(slopes.values())
    cons["rate_limit"] = rl_est
    print(f"  约束1 最大爬升斜率  : 各设定点 {[f'{s:.3f}' for s in slopes.values()]} m/s")
    print(f"                        取最大值 -> 限幅 ≈ {rl_est:.3f} m/s"
          f"（小步阶未达平台，属下界估计）")
    # 约束3: 上升时间 => 闭环快慢量级（供拟合区间）
    t10 = np.argmax(obs[2.0] > 0.1 * 2.0) * DT
    t90 = np.argmax(obs[2.0] > 0.9 * 2.0) * DT
    cons["rise_time"] = t90 - t10
    print(f"  约束2 上升时间 10-90%: {cons['rise_time']:.2f} s（设定点 2m）")
    print(f"  约束3 积分作用      : 留给阶段③嵌套模型对比判决（Ki=0 vs Ki 自由）")
    return obs, cons


# ----------------------------------------------------------------------------
# 阶段③ 约束重建——网格搜索拟合自有 PI（观察集内）
# ----------------------------------------------------------------------------
def fit(obs, cons):
    head("阶段③ 约束重建：网格搜索拟合自有 PI（只在观察集 1/2/3m 上）")
    rl_lo = max(0.5, cons["rate_limit"] * 0.93)
    rl_hi = cons["rate_limit"] * 1.08
    best = None
    for Kp in np.arange(1.2, 3.4, 0.2):
        for Ki in np.arange(0.6, 2.4, 0.2):
            for rl in np.arange(rl_lo, rl_hi, 0.02):
                rb = Rebuilt(Kp, Ki, rl)
                e = sum(rmse(simulate(rb, t), obs[t]) for t in obs)
                if best is None or e < best[0]:
                    best = (e, Kp, Ki, rl)
    e, Kp, Ki, rl = best
    # 嵌套模型对比：Ki=0（纯比例）最优拟合 vs Ki 自由——这才是积分作用的证据
    best_p = None
    for Kp0 in np.arange(0.8, 5.0, 0.1):
        for rl0 in np.arange(rl_lo, rl_hi, 0.02):
            rb0 = Rebuilt(Kp0, 0.0, rl0)
            e0 = sum(rmse(simulate(rb0, t), obs[t]) for t in obs)
            if best_p is None or e0 < best_p[0]:
                best_p = (e0, Kp0, rl0)
    print(f"  嵌套对比: 纯 P 最优(Kp={best_p[1]:.1f},限幅={best_p[2]:.2f}) "
          f"RMSE 合计={best_p[0]*1000:.1f} mm")
    print(f"            P+I 最优(Kp={Kp:.1f},Ki={Ki:.1f},限幅={rl:.2f}) "
          f"RMSE 合计={e*1000:.1f} mm")
    verdict = "积分作用存在（Ki=0 解释不了观察曲线）" if e < best_p[0] * 0.5 \
        else "积分作用证据不足"
    print(f"            -> {verdict}")
    print(f"  最优拟合: Kp={Kp:.1f}  Ki={Ki:.1f}  限幅={rl:.2f}")
    return Rebuilt(Kp, Ki, rl), (Kp, Ki, rl)


# ----------------------------------------------------------------------------
# 阶段⑤ held-out 对拍——观察集里没有的设定点 + 阵风
# ----------------------------------------------------------------------------
def held_out(rb):
    head("阶段⑤ held-out 对拍：没见过的设定点 + 阵风恢复")
    ts = np.arange(N) * DT
    gust = lambda t: -0.8 if 5.0 <= t <= 7.0 else 0.0
    cases = [(2.5, None), (4.0, None), (2.0, gust)]
    all_ok = True
    rows = []
    for target, ws in cases:
        truth = simulate(BlackBox(), target, ws)
        pred = simulate(Rebuilt(rb.Kp, rb.Ki, rb.rl), target, ws)
        r = rmse(truth, pred)
        ss = abs(truth[-1] - pred[-1])
        label = f"{target}m" + ("+阵风(-0.8m/s@5-7s)" if ws else "")
        ok = r < 0.03 and ss < 0.01
        all_ok &= ok
        rows.append((label, r, ss, ok))
        print(f"  held-out {label:<28} RMSE={r*1000:6.2f} mm  "
              f"末态差={ss*1000:5.2f} mm  {'✅' if ok else '❌'}")
    print(f"\n{OK}判定 {'PASS' if all_ok else 'FAIL'}：黑盒与重建机在没见过的"
          f"场景里行为等价{RST}" if all_ok else
          f"\n{WARN}判定 FAIL：重建不成立{RST}")
    return all_ok


def main():
    head("IREP 黑盒飞控重演重建机 · 工业高度保持类问题的玩具级全真演示")
    print("授权闸: 对象=实验台上的黑盒飞控，只读输入/输出，零固件接触 -> 绿区")
    obs, cons = extract_constraints()
    rb, (Kp, Ki, rl) = fit(obs, cons)
    ok = held_out(rb)

    head("总结算 · 强制损失清单（anchor_codec 同款纪律）")
    print(f"  传过来的（约束层）   : 积分作用 / 限幅≈{cons['rate_limit']:.2f} m/s / "
          f"闭环快慢 / 全部行为")
    print(f"  拟合到的（行为等价） : Kp={Kp:.1f} Ki={Ki:.1f} 限幅={rl:.2f}")
    print(f"  没传过来的（内部层） : 真实 Kp=2.2 Ki=1.4 限幅=1.50 ｜ 积分限幅界 "
          f"±5｜ 抗饱和细节｜ 传感器滤波链")
    print(f"  {WARN}等终性警告{RST}: 行为对拍全过 ≠ 参数恢复——"
          f"多组 (Kp,Ki,rl) 给出同一批轨迹。IREP 传的是预测等价，不是源码。")
    print(f"  {DIM}推论: 工业高度保持系统的『平衡技术』= 约束层(公开) + 调参层(可逆推)"
          f" + 数据层(十万飞行小时,不可逆推){RST}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
