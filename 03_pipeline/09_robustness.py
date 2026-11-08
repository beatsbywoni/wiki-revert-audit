"""강건성·보충 분석 (내부 심사 보고서 review_internal_v0.1.md 의 R2·R4·R5·R9·R10·W3·W4·M3 대응).

입력  02_derived/<wiki>_anchors.parquet (03·06 산출)
출력  04_output/robust_<wiki>_windows.csv     창 12h/24h/48h/7d/30d/180d/∞ 별 Δ(F2 strict, F2r replace), R, S(W)
      04_output/robust_<wiki>_variants.csv    봇·도구 정의 변형(F1, F1h, F1fast, F2, F2s, F2fast) 의 strict Δ(24h, ∞), 전수 코호트
      04_output/robust_<wiki>_cohorts.csv     코호트 변형(self-created 주 / 전체 등록 / K=5 보조 앵커 / 2021+) 의 strict Δ(F2)
      04_output/robust_<wiki>_tests.csv       H1·H2·H4 정규근사 단측 p 와 Holm 조정(확증 위키)
      04_output/robust_<wiki>_logit.csv       reverted ~ 필터×창 (replace 변형, 표본) 로지스틱, 편집자 클러스터 SE(1인 1앵커라 HC1 과 동일)
      04_output/robust_<wiki>_monthly.csv     월별 앵커 수·24h 되돌림률(급증 점검)
짝지은 차이의 SE 는 행 단위 분석적 SE(sd(a−b)/√n; 1 편집자 1 앵커). 부트스트랩과 동일한 해석.
사용법: python 03_pipeline/09_robustness.py kowiki
"""
import argparse
import os
import sys
from importlib import import_module

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
schema = import_module("01_schema")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WINS = [("W12h", 43200), ("W24h", 86400), ("W48h", 172800), ("W7d", 604800), ("W30d", 2592000), ("W180d", 15552000), ("Winf", None)]
Z = 1.959964


def inw(sec, w):
    s = sec.astype(float)
    return s.notna() & ((s <= w) if w is not None else True)


def paired(a, b):
    a = a.astype(float).to_numpy(); b = b.astype(float).to_numpy()
    d = a - b; n = len(d)
    m = d.mean() * 100; se = d.std(ddof=1) / np.sqrt(n) * 100 if n > 1 else np.nan
    return m, m - Z * se, m + Z * se, se


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("wiki"); a = ap.parse_args()
    d = os.path.join(ROOT, "02_derived"); o = os.path.join(ROOT, "04_output"); os.makedirs(o, exist_ok=True)
    cols = ["anchor_rank", "anchor_ts", "anchor_year", "created_by_self", "anchor_on_allrevs", "d3_sample", "user_id",
            "is_reverted_d1", "sec_to_revert", "reverter_is_bot", "reverter_is_bot_hist", "reverter_is_bot_cur",
            "reverter_is_tool", "reverter_is_tool_sens", "reverter_is_undo", "reverter_is_anon",
            "d3_sec_to_revert", "d3nb_sec_to_revert", "d3nt_sec_to_revert", "retained_2_60"]
    A = pd.read_parquet(os.path.join(d, f"{a.wiki}_anchors.parquet"), columns=cols)
    A["is_reverted_d1"] = A["is_reverted_d1"].astype(bool)
    for c in ["reverter_is_bot", "reverter_is_bot_hist", "reverter_is_bot_cur", "reverter_is_tool", "reverter_is_tool_sens", "reverter_is_undo"]:
        A[c] = A[c].fillna(False).astype(bool)
    A["reverter_is_anon"] = A["reverter_is_anon"].fillna(False).astype(bool)
    A["reverter_fast"] = A["is_reverted_d1"] & (A["sec_to_revert"].astype(float) <= 5) & ~A["reverter_is_anon"] & ~A["reverter_is_bot"]
    first = A[(A["anchor_rank"] == 1) & (A["anchor_year"] >= 2019)]
    prim = first[first["created_by_self"].fillna(False)]
    samp = prim[prim["anchor_on_allrevs"].fillna(False).astype(bool)]

    # ---- A/B. 창별 Δ, R, S (replace 는 표본, strict 는 표본과 전수) ----
    rows = []
    for wn, ws in WINS:
        f0 = prim["is_reverted_d1"] & inw(prim["sec_to_revert"], ws)
        f2 = f0 & ~prim["reverter_is_bot"] & ~prim["reverter_is_tool"]
        ds, dslo, dshi, _ = paired(f0, f2)
        f0s = samp["is_reverted_d1"] & inw(samp["sec_to_revert"], ws)
        f2s = f0s & ~samp["reverter_is_bot"] & ~samp["reverter_is_tool"]
        dss, _, _, _ = paired(f0s, f2s)
        r0 = inw(samp["d3_sec_to_revert"], ws); r2 = inw(samp["d3nt_sec_to_revert"], ws)
        dr, drlo, drhi, _ = paired(r0, r2)
        rows.append(dict(W=wn, n_full=len(prim), p_F0=f0.mean(), delta_strict_full_pp=ds, strict_ci_lo=dslo, strict_ci_hi=dshi,
                         n_sample=len(samp), p_F0d3=r0.mean(), delta_strict_sample_pp=dss, delta_replace_pp=dr, replace_ci_lo=drlo, replace_ci_hi=drhi,
                         S=1 - dr / dss if dss > 0 else np.nan))
    W = pd.DataFrame(rows)
    base = W.set_index("W").loc["W24h", "delta_replace_pp"]
    W["R_vs_24h"] = W["delta_replace_pp"] / base if base > 0 else np.nan
    W.to_csv(os.path.join(o, f"robust_{a.wiki}_windows.csv"), index=False)

    # ---- C. 봇·도구 정의 변형 (strict, 전수 주 코호트) ----
    rows = []
    for wn in ["W24h", "Winf"]:
        ws = dict(WINS)[wn]
        f0 = prim["is_reverted_d1"] & inw(prim["sec_to_revert"], ws)
        variants = {
            "F1 bots (current or historical)": f0 & ~prim["reverter_is_bot"],
            "F1h bots (historical only)": f0 & ~prim["reverter_is_bot_hist"],
            "F1c bots (current only)": f0 & ~prim["reverter_is_bot_cur"],
            "F1fast bots + <=5 s registered": f0 & ~prim["reverter_is_bot"] & ~prim["reverter_fast"],
            "F2 bots + tools (rollback/huggle/twinkle)": f0 & ~prim["reverter_is_bot"] & ~prim["reverter_is_tool"],
            "F2s bots + tools + undo": f0 & ~prim["reverter_is_bot"] & ~prim["reverter_is_tool_sens"],
            "F2fast bots + tools + <=5 s": f0 & ~prim["reverter_is_bot"] & ~prim["reverter_is_tool"] & ~prim["reverter_fast"],
            "F3 bots + tools + anonymous reverters": f0 & ~prim["reverter_is_bot"] & ~prim["reverter_is_tool"] & ~prim["reverter_is_anon"],
        }
        for name, col in variants.items():
            m, lo, hi, _ = paired(f0, col)
            rows.append(dict(W=wn, variant=name, n=len(prim), p_F0=f0.mean(), p_F=col.mean(), delta_pp=m, ci_lo=lo, ci_hi=hi))
    pd.DataFrame(rows).to_csv(os.path.join(o, f"robust_{a.wiki}_variants.csv"), index=False)

    # ---- D. 코호트 변형 (strict F2) ----
    rows = []
    cohorts = {
        "self-created first edits 2019+ (primary)": prim,
        "all registered first edits 2019+": first,
        "self-created, anchors 2021+ (all tags available)": prim[prim["anchor_year"] >= 2021],
        "self-created, secondary anchors (edits 2-5 within 91 d)": A[(A["anchor_rank"] >= 2) & (A["anchor_year"] >= 2019) & A["created_by_self"].fillna(False)],
    }
    for name, g in cohorts.items():
        for wn in ["W24h", "Winf"]:
            ws = dict(WINS)[wn]
            f0 = g["is_reverted_d1"] & inw(g["sec_to_revert"], ws)
            f2 = f0 & ~g["reverter_is_bot"] & ~g["reverter_is_tool"]
            m, lo, hi, _ = paired(f0, f2)
            rows.append(dict(cohort=name, W=wn, n=len(g), p_F0=f0.mean(), p_F2=f2.mean(), delta_pp=m, ci_lo=lo, ci_hi=hi,
                             rel_delta=(m / 100) / f0.mean() if f0.mean() > 0 else np.nan))
    pd.DataFrame(rows).to_csv(os.path.join(o, f"robust_{a.wiki}_cohorts.csv"), index=False)

    # ---- E. H1·H2·H4 정규근사 p 와 Holm (표본) ----
    from math import erf, sqrt
    def p_one_sided(est, se, null=0.0, greater=True):
        if not np.isfinite(se) or se == 0: return np.nan
        z = (est - null) / se
        p = 0.5 * (1 - erf(z / sqrt(2)))
        return p if greater else 1 - p
    r0_24 = inw(samp["d3_sec_to_revert"], 86400).astype(float); r2_24 = inw(samp["d3nt_sec_to_revert"], 86400).astype(float)
    r0_inf = inw(samp["d3_sec_to_revert"], None).astype(float); r2_inf = inw(samp["d3nt_sec_to_revert"], None).astype(float)
    Dvec = ((r0_24 - r2_24) - (r0_inf - r2_inf)).to_numpy(); n = len(Dvec)
    D = Dvec.mean() * 100; seD = Dvec.std(ddof=1) / np.sqrt(n) * 100
    f0s_24 = (samp["is_reverted_d1"] & inw(samp["sec_to_revert"], 86400)).astype(float)
    f2s_24 = (f0s_24.astype(bool) & ~samp["reverter_is_bot"] & ~samp["reverter_is_tool"]).astype(float)
    ds = (f0s_24 - f2s_24).to_numpy(); dr = (r0_24 - r2_24).to_numpy()
    S = 1 - dr.mean() / ds.mean()
    # delta method for S = 1 - mean(dr)/mean(ds)
    cov = np.cov(dr, ds); md, ms = dr.mean(), ds.mean()
    varS = (cov[0, 0] / ms**2 + md**2 * cov[1, 1] / ms**4 - 2 * md * cov[0, 1] / ms**3) / n
    seS = np.sqrt(max(varS, 0))
    # H4: OR ratio (strict 9 cells, 전수) — 로그 OR 최대/최소, 정규근사
    cells = []
    for wn, ws in [("W24h", 86400), ("W7d", 604800), ("Winf", None)]:
        f0 = prim["is_reverted_d1"] & inw(prim["sec_to_revert"], ws)
        for fname, col in [("F0", f0), ("F1", f0 & ~prim["reverter_is_bot"]), ("F2", f0 & ~prim["reverter_is_bot"] & ~prim["reverter_is_tool"])]:
            ret = prim["retained_2_60"].astype(bool)
            a_ = (col & ret).sum() + .5; b_ = (col & ~ret).sum() + .5; c_ = (~col & ret).sum() + .5; d_ = (~col & ~ret).sum() + .5
            lor = np.log(a_ * d_ / (b_ * c_)); se = np.sqrt(1 / a_ + 1 / b_ + 1 / c_ + 1 / d_)
            cells.append((fname, wn, lor, se))
    hi = max(cells, key=lambda t: t[2]); lo = min(cells, key=lambda t: t[2])
    lratio = hi[2] - lo[2]; se_lr = np.sqrt(hi[3]**2 + lo[3]**2)
    tests = pd.DataFrame([
        dict(test="H1 D=Δ(24h)−Δ(∞) > 0", estimate=D, se=seD, p_one_sided=p_one_sided(D, seD, 0, True)),
        dict(test="H2 S < 0.25", estimate=S, se=seS, p_one_sided=p_one_sided(S, seS, 0.25, False)),
        dict(test="H4 OR_max/OR_min >= 1.5 (log ratio vs log 1.5)", estimate=np.exp(lratio), se=se_lr, p_one_sided=p_one_sided(lratio, se_lr, np.log(1.5), True)),
    ])
    ps = tests["p_one_sided"].to_numpy(); order = np.argsort(ps); adj = np.empty_like(ps); m_ = len(ps)
    running = 0
    for rank, idx in enumerate(order):
        running = max(running, (m_ - rank) * ps[idx]); adj[idx] = min(running, 1.0)
    tests["p_holm"] = adj
    tests["note"] = "normal approximation to the registered bootstrap test; H3 is a descriptive agreement criterion (see confirmatory.csv)"
    tests.to_csv(os.path.join(o, f"robust_{a.wiki}_tests.csv"), index=False)

    # ---- F. 로지스틱 (표본, long format: 앵커 × 3창 × 3필터 replace) ----
    def logit_cluster(y, X, groups, iters=60):
        """IRLS 로지스틱 + 편집자 클러스터 샌드위치 SE (statsmodels 미설치 환경용; CR1 소표본 보정)."""
        y = y.astype(float); Xm = X.to_numpy(float); beta = np.zeros(Xm.shape[1])
        for _ in range(iters):
            p = 1 / (1 + np.exp(-(Xm @ beta))); w = p * (1 - p)
            step = np.linalg.solve((Xm * w[:, None]).T @ Xm, Xm.T @ (y - p)); beta = beta + step
            if np.abs(step).max() < 1e-9: break
        p = 1 / (1 + np.exp(-(Xm @ beta))); w = p * (1 - p)
        bread = np.linalg.inv((Xm * w[:, None]).T @ Xm)
        G = pd.DataFrame(Xm * (y - p)[:, None]).groupby(groups).sum().to_numpy()
        ng, (n_, k_) = G.shape[0], Xm.shape
        V = bread @ (G.T @ G * (ng / (ng - 1)) * ((n_ - 1) / (n_ - k_))) @ bread
        return beta, np.sqrt(np.diag(V))
    recs = []
    for wn, ws in [("W24h", 86400), ("W7d", 604800), ("Winf", None)]:
        for fname, seccol in [("F0", "d3_sec_to_revert"), ("F1r", "d3nb_sec_to_revert"), ("F2r", "d3nt_sec_to_revert")]:
            y = inw(samp[seccol], ws).astype(int).to_numpy()
            recs.append(pd.DataFrame({"y": y, "F": fname, "W": wn, "uid": samp["user_id"].to_numpy()}))
    L = pd.concat(recs, ignore_index=True)
    X = pd.DataFrame({"const": 1.0,
                      "F1r": (L["F"] == "F1r").astype(float), "F2r": (L["F"] == "F2r").astype(float),
                      "W7d": (L["W"] == "W7d").astype(float), "Winf": (L["W"] == "Winf").astype(float)})
    for f_ in ["F1r", "F2r"]:
        for w_ in ["W7d", "Winf"]:
            X[f"{f_}_x_{w_}"] = X[f_] * X[w_]
    groups = pd.factorize(L["uid"])[0]
    beta, se = logit_cluster(L["y"].to_numpy(), X, groups)
    z = beta / se; pv = 2 * (1 - 0.5 * (1 + np.vectorize(erf)(np.abs(z) / sqrt(2))))
    out = pd.DataFrame({"term": X.columns, "coef": beta, "se_cluster": se, "z": z, "p": pv, "OR": np.exp(beta)})
    out["n_rows"] = len(L); out["n_editors"] = len(samp)
    out.to_csv(os.path.join(o, f"robust_{a.wiki}_logit.csv"), index=False)
    logit_note = f"logit ok (rows {len(L):,}, clusters {len(samp):,})"

    # ---- G. 월별 추이 ----
    mth = prim.assign(month=prim["anchor_ts"].dt.to_period("M").astype(str))
    f0 = mth["is_reverted_d1"] & inw(mth["sec_to_revert"], 86400)
    f2 = f0 & ~mth["reverter_is_bot"] & ~mth["reverter_is_tool"]
    M = mth.assign(f0=f0, f2=f2, tool=mth["reverter_is_tool"] & f0, bot=mth["reverter_is_bot"] & f0).groupby("month").agg(
        n_anchors=("f0", "size"), p_F0_24h=("f0", "mean"), p_F2_24h=("f2", "mean"), tool_share=("tool", "sum"), bot_share=("bot", "sum"))
    M["tool_share"] = M["tool_share"] / (M["p_F0_24h"] * M["n_anchors"]).replace(0, np.nan)
    M["bot_share"] = M["bot_share"] / (M["p_F0_24h"] * M["n_anchors"]).replace(0, np.nan)
    M.to_csv(os.path.join(o, f"robust_{a.wiki}_monthly.csv"))

    print(f"[{a.wiki}] windows/variants/cohorts/tests/monthly written; {logit_note}")
    print(W[["W", "p_F0", "delta_strict_full_pp", "delta_replace_pp", "R_vs_24h", "S"]].round(3).to_string(index=False))
    print(tests[["test", "estimate", "p_one_sided", "p_holm"]].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
