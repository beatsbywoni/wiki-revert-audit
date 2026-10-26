"""시뮬레이션 골격: 봇 속도·점유율·사람 되돌림 지연·기저 되돌림 확률 격자에서 3×3 감사 격자를 생성한다.

목적: 관측된 kowiki/enwiki 격자가 어떤 파라미터 영역에 놓이는지 보이고, "창이 있는 지표만 민감" 패턴이
어떤 조건에서 깨지는지(예: 사람 되돌림 지연이 창보다 길 때) 미리 지도화한다. 22번의 500회 격자 방식.

사용법: python 03_pipeline/05_simulation_skeleton.py --n 20000 --reps 200
"""
import argparse
import itertools
import os

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WINDOWS = {"W24h": 86400, "W7d": 604800, "Winf": np.inf}


def simulate(n, p_revert, bot_share, bot_speed_s, human_delay_median_s, rng,
             p_human_follow_after_bot=0.0):
    """앵커 n개. 되돌림 확률 p_revert. 되돌림 중 bot_share는 봇(지연 ~ Exp(bot_speed)), 나머지는 사람
    (지연 ~ LogNormal(median)). 봇 되돌림을 F1에서 제외할 때 사람이 뒤이어 되돌릴 확률 p_human_follow_after_bot
    (strict 변형은 0, replace 변형은 >0)."""
    reverted = rng.random(n) < p_revert
    is_bot = reverted & (rng.random(n) < bot_share)
    delay = np.where(is_bot, rng.exponential(bot_speed_s, n),
                     rng.lognormal(np.log(human_delay_median_s), 1.2, n))
    # replace 변형: 봇 되돌림 뒤 사람이 다시 되돌릴 경우 그 시점으로 대체
    follow = is_bot & (rng.random(n) < p_human_follow_after_bot)
    delay_h = np.where(follow, rng.lognormal(np.log(human_delay_median_s), 1.2, n), np.inf)
    out = {}
    for w, ws in WINDOWS.items():
        f0 = reverted & (delay <= ws)
        f1_strict = f0 & ~is_bot
        f1_replace = (reverted & ~is_bot & (delay <= ws)) | (follow & (delay_h <= ws))
        out[("F0", w)] = f0.mean()
        out[("F1s", w)] = f1_strict.mean()
        out[("F1r", w)] = f1_replace.mean()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--reps", type=int, default=100)
    ap.add_argument("--seed", type=int, default=20261026)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    grid = dict(
        p_revert=[0.10, 0.25, 0.40],
        bot_share=[0.0, 0.2, 0.5, 0.8],
        bot_speed_s=[5, 60],
        human_delay_median_s=[600, 3600, 86400, 604800],
        p_human_follow_after_bot=[0.0, 0.5],
    )
    rows = []
    for combo in itertools.product(*grid.values()):
        params = dict(zip(grid.keys(), combo))
        acc = []
        for _ in range(a.reps):
            acc.append(simulate(a.n, rng=rng, **params))
        df = pd.DataFrame(acc)
        for (f, w), col in df.items():
            rows.append(dict(**params, F=f, W=w, p_mean=col.mean(), p_sd=col.std()))
    res = pd.DataFrame(rows)
    piv = res.pivot_table(index=list(grid.keys()) + ["W"], columns="F", values="p_mean").reset_index()
    piv["delta_F0_F1s_pp"] = (piv["F0"] - piv["F1s"]) * 100
    piv["delta_F0_F1r_pp"] = (piv["F0"] - piv["F1r"]) * 100
    os.makedirs(os.path.join(ROOT, "04_output"), exist_ok=True)
    out = os.path.join(ROOT, "04_output", "simulation_grid.csv")
    piv.to_csv(out, index=False)
    print(piv.groupby(["W", "bot_share"])[["delta_F0_F1s_pp", "delta_F0_F1r_pp"]].mean().round(2))
    print("→", out)


if __name__ == "__main__":
    main()
