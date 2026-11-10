"""Figures for the revised manuscript (v0.3). Reads 04_output/rev_*.csv; writes 05_manuscript/figures_v03/Figure1..4.(png|pdf) at 300 dpi.

Figure 1  Who makes the first revert of a newcomer's first edit within 24 hours (stacked, in percent of all first edits)
Figure 2  Follow-up manual reverts after the first revert, by who reverted first, under two attribution rules
Figure 3  Retention (an edit on days 2 to 60) by who made the first revert within 24 hours
Figure 4  Reverts whose reverted edit carries no mw-reverted tag, by reverter class and patrolling regime
Palette: validated categorical order (blue, orange, aqua, yellow, magenta); identity is never colour-alone (hatching, markers, direct labels).
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(ROOT, "04_output"); FIG = os.path.join(ROOT, "05_manuscript", "figures_v03")
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]
NAME = {"enwiki": "English", "itwiki": "Italian", "kowiki": "Korean", "dewiki": "German", "plwiki": "Polish", "frwiki": "French", "jawiki": "Japanese"}
CONF = {"jawiki", "plwiki", "itwiki"}
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREY, INK = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#8a8a85", "#222222"
plt.rcParams.update({"font.size": 8.5, "font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False, "savefig.dpi": 300,
                     "axes.edgecolor": "#888888", "axes.linewidth": 0.6, "xtick.color": "#444444", "ytick.color": INK, "hatch.linewidth": 0.5})


def lab(w):
    return NAME[w] + ("*" if w in CONF else "")


def save(fig, name):
    os.makedirs(FIG, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIG, f"{name}.{ext}"), bbox_inches="tight")
    plt.close(fig)


def fig1():
    c = pd.read_csv(os.path.join(O, "rev_composition.csv")); c = c[(c.cohort == "2019+") & (c.W == "W24h")].set_index("wiki").loc[WIKIS[::-1]]
    classes = [("bot", "Bot", BLUE, ""), ("tool", "One-click tool (rollback, Huggle, Twinkle)", ORANGE, "////"), ("manual_other", "Other registered editor, manual", AQUA, ""),
               ("anon", "Unregistered editor", YELLOW, "...."), ("self", "The newcomer (self-revert)", MAGENTA, "xxxx")]
    fig, ax = plt.subplots(figsize=(7.0, 3.2)); y = np.arange(len(c)); left = np.zeros(len(c))
    for key, label, col, hatch in classes:
        w = c[f"delta_excl_{key}_pp"].to_numpy()
        ax.barh(y, w, left=left, height=0.62, color=col, edgecolor="white", linewidth=1.2, hatch=hatch, label=label)
        for yi, (l, wi) in enumerate(zip(left, w)):
            if wi >= 2.0:
                ax.text(l + wi / 2, yi, f"{wi:.1f}", ha="center", va="center", fontsize=7, color=INK,
                        bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
        left += w
    for yi, tot in enumerate(left):
        ax.text(tot + 0.4, yi, f"{tot:.1f}%", va="center", fontsize=8, color=INK)
    ax.set_yticks(y); ax.set_yticklabels([lab(w) for w in c.index]); ax.set_xlim(0, 42)
    ax.set_xlabel("Newcomer first edits reverted within 24 hours, by who made the first revert (% of all first edits)")
    ax.xaxis.grid(True, lw=0.3, color="#dddddd"); ax.set_axisbelow(True)
    ax.legend(fontsize=7, frameon=False, loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=3, handlelength=1.6, columnspacing=1.2)
    save(fig, "Figure1")


def fig2():
    f = pd.read_csv(os.path.join(O, "rev_followup.csv"))
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 4.6), sharey=True)
    for i, (rule, rname) in enumerate([("d3", "History-dump rule (no radius)"), ("d3r", "15-revision radius rule")]):
        for j, (wn, wname) in enumerate([("W24h", "within 24 hours"), ("Winf", "unbounded")]):
            ax = axes[i, j]
            for k, w in enumerate(WIKIS[::-1]):
                for cls, col, mk, dy, label in [("bot_or_tool", ORANGE, "o", 0.16, "First revert by a bot or one-click tool"),
                                                ("any_manual", AQUA, "s", -0.16, "First revert manual, by another editor")]:
                    r = f[(f.wiki == w) & (f.rule == rule) & (f.W == wn) & (f.first_class == cls)]
                    if r.empty: continue
                    r = r.iloc[0]
                    ax.errorbar(r.followup * 100, k + dy, xerr=[[(r.followup - r.lo) * 100], [(r.hi - r.followup) * 100]], fmt=mk, ms=4.5, color=col,
                                ecolor=col, elinewidth=1, capsize=0, label=label if k == 0 else None, markeredgecolor="white", markeredgewidth=0.6)
            ax.set_title(f"{rname}, {wname}", fontsize=8); ax.xaxis.grid(True, lw=0.3, color="#dddddd"); ax.set_axisbelow(True)
            ax.set_xlim(0, 46 if rule == "d3" else 9); ax.set_yticks(range(len(WIKIS))); ax.set_yticklabels([lab(w) for w in WIKIS[::-1]])
            if i == 1: ax.set_xlabel("Anchors with a later manual revert (%)")
    h, l = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, l, fontsize=7.5, frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.03))
    fig.tight_layout(rect=(0, 0, 1, 0.97)); save(fig, "Figure2")


def wilson(p, n, z=1.96):
    d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d


def fig3():
    r = pd.read_csv(os.path.join(O, "rev_retention.csv"))
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    spec = [("tool", "Reverted with a one-click tool", ORANGE, "o"), ("manual_other", "Reverted manually by another registered editor", AQUA, "s"),
            ("self", "Self-reverted", MAGENTA, "D")]
    for k, w in enumerate(WIKIS[::-1]):
        g = r[r.wiki == w]
        nr = g.retained_share_not_reverted.iloc[0] * 100
        ax.plot(nr, k, marker="|", ms=12, mew=2, color=INK, label="Not reverted within 24 hours" if k == 0 else None, ls="")
        xs = [nr]
        for cls, label, col, mk in spec:
            q = g[g.first_revert_class == cls]
            if q.empty: continue
            q = q.iloc[0]; lo, hi = wilson(q.retained_share, q.n_class)
            ax.errorbar(q.retained_share * 100, k, xerr=[[(q.retained_share - lo) * 100], [(hi - q.retained_share) * 100]], fmt=mk, ms=5, color=col, ecolor=col,
                        elinewidth=1, label=label if k == 0 else None, markeredgecolor="white", markeredgewidth=0.6)
            xs.append(q.retained_share * 100)
        ax.plot([min(xs), max(xs)], [k, k], color="#cccccc", lw=0.8, zorder=0)
    ax.set_yticks(range(len(WIKIS))); ax.set_yticklabels([lab(w) for w in WIKIS[::-1]]); ax.set_xlim(0, 30)
    ax.set_xlabel("Newcomers who edited again on days 2 to 60 (%)"); ax.xaxis.grid(True, lw=0.3, color="#dddddd"); ax.set_axisbelow(True)
    ax.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.22), ncol=2)
    save(fig, "Figure3")


def fig4():
    t = pd.read_csv(os.path.join(O, "rev_taggap.csv"))
    regimes = [("No edit patrolling", ["enwiki", "kowiki", "jawiki"]), ("FlaggedRevs", ["dewiki", "plwiki"]), ("Recent-changes patrolling", ["itwiki", "frwiki"])]
    classes = [("tool", "One-click tool"), ("manual_other", "Other registered,\nmanual"), ("self", "Newcomer\n(self-revert)"), ("anon", "Unregistered\neditor")]
    cols = [BLUE, ORANGE, AQUA]; mks = ["o", "s", "D"]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.9), sharey=True)
    for ax, (rname, ws) in zip(axes, regimes):
        for wi, w in enumerate(ws):
            for ci, (cls, _) in enumerate(classes):
                q = t[(t.wiki == w) & (t.reverter_class == cls)]
                if q.empty: continue
                q = q.iloc[0]
                ax.errorbar(q.untagged * 100, len(classes) - 1 - ci + (wi - (len(ws) - 1) / 2) * 0.22, xerr=[[(q.untagged - q.lo) * 100], [(q.hi - q.untagged) * 100]],
                            fmt=mks[wi], ms=4.5, color=cols[wi], ecolor=cols[wi], elinewidth=1, label=lab(w) if ci == 0 else None,
                            markeredgecolor="white", markeredgewidth=0.6)
        ax.set_title(rname, fontsize=8.5); ax.set_xlim(-3, 100); ax.xaxis.grid(True, lw=0.3, color="#dddddd"); ax.set_axisbelow(True)
        ax.legend(fontsize=7, frameon=False, loc="upper right")
    axes[0].set_yticks(range(len(classes))); axes[0].set_yticklabels([c[1] for c in classes[::-1]])
    axes[0].set_ylabel("Who made the revert")
    fig.supxlabel("Reverts within 15 revisions whose reverted edit carries no mw-reverted tag (%)", fontsize=8.5)
    fig.tight_layout(); save(fig, "Figure4")


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); print("figures written to", FIG)
