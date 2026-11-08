"""09_robustness.py 산출물을 7개 위키에 걸쳐 모아 보충자료 표(S1–S6)와 급증 점검 그림을 만든다.

출력  04_output/robust_cross_windows.csv    표 S1: 창 7개 × 위키, Δ(replace), R(창)/R(24h), S(창)
      04_output/robust_cross_variants.csv   표 S2: 봇·도구 정의 변형별 strict Δ(24h), 위키별
      04_output/robust_cross_cohorts.csv    표 S3: 코호트 변형별 strict Δ(F2, 24h), 상대 Δ
      04_output/robust_cross_tests.csv      표 S4: H1·H2·H4 정규근사 p, Holm
      04_output/robust_cross_logit.csv      표 S5: 로지스틱 상호작용(F2r×W∞ 등) 계수·클러스터 SE
      04_output/robust_kowiki_anchor_alt.csv 표 S6: kowiki 앵커 정의(첫 편집 vs 첫 ns0 편집) 비교
      04_output/fig5_monthly_surge.(png|pdf) kowiki·enwiki 월별 앵커 수와 24h 되돌림률
      04_output/robustness_summary.md
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(ROOT, "04_output"); D = os.path.join(ROOT, "02_derived")
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]
ROLE = {"kowiki": "expl", "enwiki": "expl", "frwiki": "expl", "dewiki": "expl", "jawiki": "conf", "plwiki": "conf", "itwiki": "conf"}


def inw(sec, w):
    s = sec.astype(float)
    return s.notna() & ((s <= w) if w is not None else True)


def main():
    win = pd.concat([pd.read_csv(os.path.join(O, f"robust_{w}_windows.csv")).assign(wiki=w) for w in WIKIS])
    win.to_csv(os.path.join(O, "robust_cross_windows.csv"), index=False)
    var = pd.concat([pd.read_csv(os.path.join(O, f"robust_{w}_variants.csv")).assign(wiki=w) for w in WIKIS])
    var.to_csv(os.path.join(O, "robust_cross_variants.csv"), index=False)
    coh = pd.concat([pd.read_csv(os.path.join(O, f"robust_{w}_cohorts.csv")).assign(wiki=w) for w in WIKIS])
    coh.to_csv(os.path.join(O, "robust_cross_cohorts.csv"), index=False)
    tst = pd.concat([pd.read_csv(os.path.join(O, f"robust_{w}_tests.csv")).assign(wiki=w) for w in WIKIS])
    tst.to_csv(os.path.join(O, "robust_cross_tests.csv"), index=False)
    lg = pd.concat([pd.read_csv(os.path.join(O, f"robust_{w}_logit.csv")).assign(wiki=w) for w in WIKIS])
    lg.to_csv(os.path.join(O, "robust_cross_logit.csv"), index=False)

    # kowiki 앵커 정의 비교
    rows = []
    for label, fn in [("first edit (registered)", "kowiki_anchors.parquet"), ("first ns0 edit (pilot)", "kowiki_anchors_firstns0.parquet")]:
        A = pd.read_parquet(os.path.join(D, fn), columns=["anchor_rank", "anchor_year", "created_by_self", "is_reverted_d1", "sec_to_revert",
                                                          "reverter_is_bot", "reverter_is_tool", "retained_2_60"])
        g = A[(A.anchor_rank == 1) & (A.anchor_year >= 2019) & A.created_by_self.fillna(False).astype(bool)]
        for wn, ws in [("W24h", 86400), ("W7d", 604800), ("Winf", None)]:
            f0 = g.is_reverted_d1.astype(bool) & inw(g.sec_to_revert, ws)
            f2 = f0 & ~g.reverter_is_bot.fillna(False).astype(bool) & ~g.reverter_is_tool.fillna(False).astype(bool)
            d = (f0.astype(float) - f2.astype(float)); m = d.mean() * 100; se = d.std(ddof=1) / np.sqrt(len(d)) * 100
            rows.append(dict(anchor=label, W=wn, n=len(g), p_F0=f0.mean(), p_F2=f2.mean(), delta_pp=m, ci_lo=m - 1.96 * se, ci_hi=m + 1.96 * se,
                             rel_delta=m / 100 / f0.mean()))
    alt = pd.DataFrame(rows); alt.to_csv(os.path.join(O, "robust_kowiki_anchor_alt.csv"), index=False)

    # 그림 5: 월별 급증 점검
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 4.6), sharex=True)
    for w, c in [("kowiki", "tab:red"), ("enwiki", "tab:blue"), ("jawiki", "tab:green")]:
        M = pd.read_csv(os.path.join(O, f"robust_{w}_monthly.csv"), parse_dates=["month"])
        M = M[(M.month >= "2019-01-01") & (M.month <= "2026-03-01")]
        axes[0].plot(M.month, M.n_anchors / M.n_anchors.median(), color=c, lw=1, label=f"{w} (median = {int(M.n_anchors.median()):,})")
        axes[1].plot(M.month, M.p_F0_24h * 100, color=c, lw=1, label=f"{w} all reverts")
        axes[1].plot(M.month, M.p_F2_24h * 100, color=c, lw=1, ls="--", label=f"{w} excl. bots and tools")
    axes[0].axhline(1, color="grey", lw=0.5, ls=":")
    axes[0].set_ylabel("First-edit anchors per month\n(ratio to wiki median)"); axes[0].legend(fontsize=7, frameon=False)
    axes[1].set_ylabel("Reverted within 24 h (%)"); axes[1].legend(fontsize=6.5, frameon=False, ncol=3)
    axes[1].set_xlabel("Month of first edit")
    for ax in axes: ax.grid(lw=0.3, alpha=0.5); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    for ext in ("png", "pdf"): fig.savefig(os.path.join(O, f"fig5_monthly_surge.{ext}"), dpi=300)
    plt.close(fig)

    # 요약 md
    L = ["# Robustness summary (09/10)", ""]
    piv = win.pivot(index="W", columns="wiki", values="R_vs_24h").loc[["W12h", "W24h", "W48h", "W7d", "W30d", "W180d", "Winf"], WIKIS]
    L += ["## S1 R(W) = Δ_replace(W)/Δ_replace(24h)", piv.round(3).to_markdown(), ""]
    pivS = win.pivot(index="W", columns="wiki", values="S").loc[["W24h", "W7d", "Winf"], WIKIS]
    L += ["## S1b substitution S(W)", pivS.round(3).to_markdown(), ""]
    v24 = var[var.W == "W24h"].pivot(index="variant", columns="wiki", values="delta_pp")[WIKIS]
    L += ["## S2 strict Δ(24h) by exclusion definition (pp)", v24.round(2).to_markdown(), ""]
    c24 = coh[coh.W == "W24h"].pivot(index="cohort", columns="wiki", values="rel_delta")[WIKIS]
    L += ["## S3 relative Δ(F2 strict, 24h) by cohort", c24.round(3).to_markdown(), ""]
    L += ["## S4 normal-approximation tests", tst[["wiki", "test", "estimate", "se", "p_one_sided", "p_holm"]].round(4).to_markdown(index=False), ""]
    li = lg[lg.term.isin(["F2r", "F2r_x_W7d", "F2r_x_Winf", "F1r", "F1r_x_Winf"])].pivot(index="term", columns="wiki", values="coef")[WIKIS]
    lse = lg[lg.term.isin(["F2r", "F2r_x_W7d", "F2r_x_Winf", "F1r", "F1r_x_Winf"])].pivot(index="term", columns="wiki", values="se_cluster")[WIKIS]
    L += ["## S5 logistic coefficients (cluster SE in parentheses)",
          (li.round(3).astype(str) + " (" + lse.round(3).astype(str) + ")").to_markdown(), ""]
    L += ["## S6 kowiki anchor definition", alt.round(3).to_markdown(index=False), ""]
    with open(os.path.join(O, "robustness_summary.md"), "w", encoding="utf-8") as fh: fh.write("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
