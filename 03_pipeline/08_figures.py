"""원고용 그림 (7개 위키 격자 결과에서).

입력  04_output/<wiki>_grid.csv, <wiki>_grid_by_year.csv, cross_wiki_table.csv, h3_tag_coverage.csv
출력  04_output/fig1_window_by_filter.(png|pdf)   창별 Δ(F0−F2), strict 대 replace, 위키별 선
      04_output/fig2_dose_response.(png|pdf)      봇·도구 점유율 대 상대 Δ(replace 24h), 위키×연도 셀 + 위키 전체
      04_output/fig3_or_cells.(png|pdf)           9셀 되돌림→잔존 OR(strict), 위키별
      04_output/fig4_tag_coverage.(png|pdf)       반경 15 안 identity revert 중 mw-reverted 미태그율, patrol/FlaggedRevs 표시
      04_output/fig_data_*.csv                    그림 데이터(재현용)
사용법: python 03_pipeline/08_figures.py [--outdir 04_output]
"""
import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]  # 도구 점유율 내림차순
ROLE = {"kowiki": "exploratory", "enwiki": "exploratory", "frwiki": "exploratory", "dewiki": "exploratory",
        "jawiki": "confirmatory", "plwiki": "confirmatory", "itwiki": "confirmatory"}
GATE = {"frwiki": "RC patrol", "itwiki": "RC patrol", "dewiki": "FlaggedRevs", "plwiki": "FlaggedRevs", "enwiki": "FlaggedRevs (few pages)", "kowiki": "none", "jawiki": "none"}
WLAB = {"W24h": "24 h", "W7d": "7 d", "Winf": "unbounded"}
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
COLORS = plt.get_cmap("tab10").colors


def load(outdir):
    grids = {w: pd.read_csv(os.path.join(outdir, f"{w}_grid.csv")) for w in WIKIS}
    years = {w: pd.read_csv(os.path.join(outdir, f"{w}_grid_by_year.csv")) for w in WIKIS}
    cross = pd.read_csv(os.path.join(outdir, "cross_wiki_table.csv")).set_index("wiki")
    cov = pd.read_csv(os.path.join(outdir, "h3_tag_coverage.csv")).set_index("wiki")
    return grids, years, cross, cov


def fig1(grids, outdir):
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    rows = []
    for i, w in enumerate(WIKIS):
        g = grids[w]
        for ax, variant, f in zip(axes, ["strict", "replace"], ["F2", "F2r"]):
            s = g[(g.variant == variant) & (g.F == f)].set_index("W").loc[["W24h", "W7d", "Winf"]]
            ax.errorbar(range(3), s.delta_vs_F0_pp, yerr=[s.delta_vs_F0_pp - s.delta_ci_lo, s.delta_ci_hi - s.delta_vs_F0_pp],
                        marker="o", ms=3.5, lw=1.2, capsize=2, color=COLORS[i], label=w,
                        ls="-" if ROLE[w] == "confirmatory" else "--")
            for wn, r in s.iterrows():
                rows.append(dict(wiki=w, variant=variant, W=wn, delta_pp=r.delta_vs_F0_pp, ci_lo=r.delta_ci_lo, ci_hi=r.delta_ci_hi))
    for ax, title in zip(axes, ["Strict variant (bot or tool revert = not reverted)", "Replace variant (next non-excluded revert)"]):
        ax.set_xticks(range(3)); ax.set_xticklabels([WLAB[k] for k in ["W24h", "W7d", "Winf"]])
        ax.set_title(title, fontsize=9); ax.set_xlabel("Observation window"); ax.grid(axis="y", lw=0.3, alpha=0.5)
    axes[0].set_ylabel("Δ = p(F0) − p(F2), percentage points")
    axes[1].legend(fontsize=7, frameon=False, ncol=2, title="solid = confirmatory, dashed = exploratory", title_fontsize=7)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(outdir, f"fig1_window_by_filter.{ext}"))
    pd.DataFrame(rows).to_csv(os.path.join(outdir, "fig_data_fig1.csv"), index=False)
    plt.close(fig)


def fig2(grids, years, outdir):
    fig, ax = plt.subplots(figsize=(5.2, 3.8))
    rows = []
    for i, w in enumerate(WIKIS):
        y = years[w]
        for yr, g in y.groupby("label"):
            r = g[(g.variant == "replace")].set_index(["F", "W"])
            if ("F0d3", "W24h") not in r.index or ("F2r", "W24h") not in r.index:
                continue
            base = r.loc[("F0d3", "W24h")]
            if base.n_anchor < 200 or base.p_reverted <= 0:
                continue
            share = base.bot_share + base.tool_share
            rel = r.loc[("F2r", "W24h"), "delta_vs_F0_pp"] / 100 / base.p_reverted
            ax.scatter(share, rel, s=8 + 40 * np.sqrt(base.n_anchor / 60000), facecolors="none", edgecolors=COLORS[i], lw=0.8, alpha=0.8)
            rows.append(dict(wiki=w, year=yr, n=base.n_anchor, share=share, rel_delta=rel, level="wiki-year"))
        g = grids[w]
        r = g[g.variant == "replace"].set_index(["F", "W"])
        base = r.loc[("F0d3", "W24h")]
        share = base.bot_share + base.tool_share
        rel = r.loc[("F2r", "W24h"), "delta_vs_F0_pp"] / 100 / base.p_reverted
        ax.scatter(share, rel, s=70, color=COLORS[i], edgecolors="black", lw=0.6, zorder=5,
                   marker="o" if ROLE[w] == "confirmatory" else "s")
        ax.annotate(w, (share, rel), xytext=(5, 4), textcoords="offset points", fontsize=8)
        rows.append(dict(wiki=w, year="all", n=base.n_anchor, share=share, rel_delta=rel, level="wiki"))
    d = pd.DataFrame(rows)
    yy = d[d.level == "wiki-year"]
    rho = yy[["share", "rel_delta"]].corr(method="spearman").iloc[0, 1]
    ax.plot([0, 0.7], [0, 0.7], ls=":", color="grey", lw=0.8)
    ax.set_xlabel("Bot or tool share of first reverts within 24 h")
    ax.set_ylabel("Relative Δ = (p(F0) − p(F2r)) / p(F0), 24 h window")
    ax.set_title(f"{len(WIKIS)} wikis (large: circle = confirmatory, square = exploratory)\n"
                 f"and {len(yy)} wiki-year cells (open); dotted = Δ equal to share; cell Spearman ρ = {rho:.2f}", fontsize=8)
    ax.set_xlim(0, 0.75); ax.set_ylim(0, 0.75); ax.grid(lw=0.3, alpha=0.5)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(outdir, f"fig2_dose_response.{ext}"))
    d.to_csv(os.path.join(outdir, "fig_data_fig2.csv"), index=False)
    plt.close(fig)
    return rho, len(yy)


def fig3(grids, outdir):
    fig, axes = plt.subplots(1, len(WIKIS), figsize=(10.5, 3.0), sharey=True)
    rows = []
    cells = [(f, w) for w in ["W24h", "W7d", "Winf"] for f in ["F0", "F1", "F2"]]
    for ax, w in zip(axes, WIKIS):
        g = grids[w][grids[w].variant == "strict"].set_index(["F", "W"])
        for k, (f, wn) in enumerate(cells):
            r = g.loc[(f, wn)]
            ax.errorbar(k, r.or_retention, yerr=[[r.or_retention - r.or_lo], [r.or_hi - r.or_retention]], fmt="o", ms=3, capsize=2,
                        color=["#1f77b4", "#ff7f0e", "#2ca02c"][k % 3], lw=1)
            rows.append(dict(wiki=w, F=f, W=wn, OR=r.or_retention, lo=r.or_lo, hi=r.or_hi))
        ax.axhline(1, color="grey", lw=0.6, ls=":")
        ax.set_xticks([1, 4, 7]); ax.set_xticklabels(["24 h", "7 d", "∞"])
        ax.set_title(f"{w}\n({ROLE[w][:4]}.)", fontsize=8)
        for xline in (2.5, 5.5):
            ax.axvline(xline, color="lightgrey", lw=0.5)
    axes[0].set_ylabel("Odds ratio of retention\n(reverted vs not), strict cells")
    axes[0].legend(handles=[plt.Line2D([], [], marker="o", ls="", color=c, label=l) for c, l in
                            zip(["#1f77b4", "#ff7f0e", "#2ca02c"], ["F0 all reverts", "F1 excl. bots", "F2 excl. bots and tools"])],
                   fontsize=6.5, frameon=False, loc="upper left")
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(outdir, f"fig3_or_cells.{ext}"))
    pd.DataFrame(rows).to_csv(os.path.join(outdir, "fig_data_fig3.csv"), index=False)
    plt.close(fig)


def fig4(cov, outdir):
    c = cov.loc[WIKIS].sort_values("untagged_share")
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    cols = ["#d62728" if GATE[w] == "RC patrol" else "#ff7f0e" if GATE[w].startswith("FlaggedRevs") else "#7f7f7f" for w in c.index]
    ax.barh(c.index, c.untagged_share * 100, color=cols)
    for i, (w, r) in enumerate(c.iterrows()):
        ax.text(r.untagged_share * 100 + 0.2, i, f"{r.untagged_share*100:.1f}%  ({GATE[w]}; n = {int(r.within_radius_reverted):,})", va="center", fontsize=7)
    ax.set_xlabel("Identity reverts within 15 revisions that carry no mw-reverted tag (%)")
    ax.set_xlim(0, c.untagged_share.max() * 100 + 9)
    ax.set_title("Tag coverage gap by wiki, first edits from 2020-08\n(red = RC patrol enabled, orange = FlaggedRevs, grey = neither)", fontsize=8)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(outdir, f"fig4_tag_coverage.{ext}"))
    c.assign(gate=[GATE[w] for w in c.index]).to_csv(os.path.join(outdir, "fig_data_fig4.csv"))
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=os.path.join(ROOT, "04_output"))
    a = ap.parse_args()
    grids, years, cross, cov = load(a.outdir)
    fig1(grids, a.outdir)
    rho, ncells = fig2(grids, years, a.outdir)
    fig3(grids, a.outdir)
    fig4(cov, a.outdir)
    print(f"figures written to {a.outdir}; dose-response cells {ncells}, Spearman {rho:.3f}")


if __name__ == "__main__":
    main()
