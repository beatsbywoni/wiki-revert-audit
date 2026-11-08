"""투고용 그림 파일 (v0.2): Figure1~4 300dpi 개별 PNG + PDF, 보충 그림 S1(9셀 OR 상세)·S2(월별 급증).

그림 3 은 재구성: 위키별 잔존 OR 의 범위(최소 셀 = F0·24h, 최대 셀 = F2·∞)를 막대로, 두 극단 셀의 95% 구간을 수염으로.
기존 08_figures.py 의 fig3(7패널) 은 Figure S1 로 옮긴다.
사용법: python 03_pipeline/11_figures_submission.py
출력  05_manuscript/figures/Figure1.png … Figure4.png, FigureS1.png, FigureS2.png (+ .pdf), fig_data_fig3_v2.csv
"""
import os
import shutil
import sys
from importlib import import_module

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
f8 = import_module("08_figures")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(ROOT, "04_output")
FIG = os.path.join(ROOT, "05_manuscript", "figures")
WIKIS = f8.WIKIS; ROLE = f8.ROLE
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 300, "savefig.dpi": 300,
                     "font.family": "sans-serif"})


def fig3_v2(grids):
    rows = []
    for w in WIKIS:
        g = grids[w][grids[w].variant == "strict"].set_index(["F", "W"])
        lo = g.loc[("F0", "W24h")]; hi = g.loc[("F2", "Winf")]
        mn = g.loc[[(f, wn) for f in ["F0", "F1", "F2"] for wn in ["W24h", "W7d", "Winf"]]]
        rows.append(dict(wiki=w, role=ROLE[w], or_min=lo.or_retention, or_min_lo=lo.or_lo, or_min_hi=lo.or_hi,
                         or_max=hi.or_retention, or_max_lo=hi.or_lo, or_max_hi=hi.or_hi,
                         ratio=hi.or_retention / lo.or_retention,
                         min_cell_is_F0_24h=bool(mn.or_retention.idxmin() == ("F0", "W24h")),
                         max_cell_is_F2_inf=bool(mn.or_retention.idxmax() == ("F2", "Winf"))))
    d = pd.DataFrame(rows).iloc[::-1]
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    y = range(len(d))
    for i, (_, r) in enumerate(d.iterrows()):
        ax.plot([r.or_min, r.or_max], [i, i], color="#9ecae1" if r.role == "exploratory" else "#3182bd", lw=6, solid_capstyle="butt", zorder=1)
        ax.errorbar(r.or_min, i, xerr=[[r.or_min - r.or_min_lo], [r.or_min_hi - r.or_min]], fmt="o", ms=4, color="#d62728", capsize=2, lw=1, zorder=3)
        ax.errorbar(r.or_max, i, xerr=[[r.or_max - r.or_max_lo], [r.or_max_hi - r.or_max]], fmt="s", ms=4, color="#2ca02c", capsize=2, lw=1, zorder=3)
        ax.text(r.or_max + 0.03, i, f"×{r.ratio:.2f}", va="center", fontsize=8)
    ax.axvline(1, color="grey", lw=0.6, ls=":")
    ax.set_yticks(list(y)); ax.set_yticklabels([f"{w} ({ROLE[w][:4]}.)" for w in d.wiki])
    ax.set_xlabel("Odds ratio of retention, reverted vs not reverted (strict cells)")
    ax.set_xlim(0.2, 1.45)
    ax.legend(handles=[plt.Line2D([], [], marker="o", ls="", color="#d62728", label="All reverts, 24 h (lowest cell)"),
                       plt.Line2D([], [], marker="s", ls="", color="#2ca02c", label="Excl. bots and tools, unbounded (highest cell)"),
                       plt.Line2D([], [], color="#3182bd", lw=6, label="range (dark = confirmatory)")],
              fontsize=7, frameon=False, loc="upper right", bbox_to_anchor=(1.0, 1.02))
    ax.set_ylim(-0.6, len(d) - 0.4 + 1.1)
    fig.tight_layout()
    for ext in ("png", "pdf"): fig.savefig(os.path.join(FIG, f"Figure3.{ext}"))
    plt.close(fig)
    d.to_csv(os.path.join(O, "fig_data_fig3_v2.csv"), index=False)
    return d


def main():
    os.makedirs(FIG, exist_ok=True)
    grids, years, cross, cov = f8.load(O)
    # Figure 1, 2, 4: 08 의 함수를 300dpi 로 다시 저장
    f8.fig1(grids, O); f8.fig2(grids, years, O); f8.fig4(cov, O); f8.fig3(grids, O)
    for src, dst in [("fig1_window_by_filter", "Figure1"), ("fig2_dose_response", "Figure2"), ("fig4_tag_coverage", "Figure4"),
                     ("fig3_or_cells", "FigureS1"), ("fig5_monthly_surge", "FigureS2")]:
        for ext in ("png", "pdf"):
            shutil.copyfile(os.path.join(O, f"{src}.{ext}"), os.path.join(FIG, f"{dst}.{ext}"))
    d = fig3_v2(grids)
    print(d[["wiki", "or_min", "or_max", "ratio", "min_cell_is_F0_24h", "max_cell_is_F2_inf"]].round(3).to_string(index=False))
    print("written to", FIG)


if __name__ == "__main__":
    main()
