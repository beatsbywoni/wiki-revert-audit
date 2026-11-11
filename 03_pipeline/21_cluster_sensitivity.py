"""Sensitivity of intervals to clustering in reverting accounts (round 4; exploratory).

The registered intervals resample editors (one first edit each). Reverts cluster in reverting accounts. For the page-history
samples this script recomputes key quantities with a bootstrap that resamples clusters, where a cluster is the account that
made the first revert (dump rule); non-reverted edits and edits first reverted by an unregistered editor are singletons.
Quantities: H1 difference D and ratio R (dump and radius rule), H2 share S (registered definition), odds ratio of retention
for tool-reverted versus non-reverted newcomers (24 h), untagged share of radius-rule reverts (first edits from October 2020).
Also (b) H3 second clause under the registered window (August 2020) and the October 2020 window.
Output: 04_output/rev_cluster_sensitivity.csv, 04_output/rev_h3_windows.csv
"""
import os, sys
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "02_derived"); OUT = os.path.join(ROOT, "04_output")
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]; SEED = 20261112; B = 1000


def b(s): return s.fillna(False).astype(bool).to_numpy()


def inw(x, w):
    x = np.asarray(x, float); return ~np.isnan(x) & ((x <= w) if w is not None else True)


def main():
    rows, h3 = [], []
    for w in WIKIS:
        A = pd.read_parquet(os.path.join(D, f"{w}_decomp.parquet"))
        A = A[A.created_by_self.fillna(False).astype(bool) & (A.anchor_year >= 2019)].reset_index(drop=True); n = len(A)
        rng = np.random.default_rng(SEED)
        fu = A.d3_first_user.astype(float).to_numpy(); cl = np.where(np.isnan(fu), -np.arange(1, n + 1), fu)  # singletons get unique negative ids
        codes, inv = np.unique(cl, return_inverse=True); G = len(codes)
        order = np.argsort(inv, kind="stable"); starts = np.searchsorted(inv[order], np.arange(G)); ends = np.r_[starts[1:], n]
        Q = {}
        for rule in ["d3", "d3r"]:
            fs = A[f"{rule}_first_sec"].astype(float).to_numpy(); auto = b(A[f"{rule}_first_bot"]) | b(A[f"{rule}_first_tool"])
            nt = np.where(np.isnan(fs), np.nan, np.where(auto, A[f"{rule}_nt1_sec"].astype(float).to_numpy(), fs))
            d24 = inw(fs, 86400).astype(float) - inw(nt, 86400); dinf = inw(fs, None).astype(float) - inw(nt, None)
            Q[rule] = (d24, dinf)
            if rule == "d3":
                a24 = inw(fs, 86400) & auto; s24 = a24 & inw(A.d3_nt1_sec.astype(float).to_numpy(), 86400)
                tool24 = inw(fs, 86400) & b(A.d3_first_tool) & ~b(A.d3_first_bot); notrev = ~inw(fs, 86400); ret = b(A.retained_2_60)
        late = (A.anchor_ts >= pd.Timestamp("2020-10-01", tz=A.anchor_ts.dt.tz)).to_numpy(); rr = A.d3r_first_sec.notna().to_numpy() & late; un = rr & ~b(A.is_reverted_d2)

        def stats(ix):
            o = {}
            for rule in ["d3", "d3r"]:
                d24, dinf = Q[rule]; o[f"D_{rule}_pp"] = (d24[ix].mean() - dinf[ix].mean()) * 100; o[f"R_{rule}"] = dinf[ix].mean() / d24[ix].mean()
            o["S_registered"] = s24[ix].sum() / max(a24[ix].sum(), 1)
            a_ = (tool24 & ret)[ix].sum() + .5; b_ = (tool24 & ~ret)[ix].sum() + .5; c_ = (notrev & ret)[ix].sum() + .5; d_ = (notrev & ~ret)[ix].sum() + .5
            o["OR_retention_tool"] = (a_ / b_) / (c_ / d_); o["untagged_all"] = un[ix].sum() / max(rr[ix].sum(), 1)
            return o
        est = stats(np.arange(n)); ed, clu = [], []
        for _ in range(B):
            ed.append(stats(rng.integers(0, n, n)))
            g = rng.integers(0, G, G); ix = np.concatenate([order[starts[k]:ends[k]] for k in g]); clu.append(stats(ix))
        ed = pd.DataFrame(ed); clu = pd.DataFrame(clu)
        for k, v in est.items():
            rows.append(dict(wiki=w, quantity=k, estimate=v, editor_lo=ed[k].quantile(.025), editor_hi=ed[k].quantile(.975),
                             cluster_lo=clu[k].quantile(.025), cluster_hi=clu[k].quantile(.975), cluster_lo_one_sided=clu[k].quantile(.05), cluster_hi_one_sided=clu[k].quantile(.95),
                             n=n, clusters=G, largest_cluster_share_of_first_reverts=float(np.max(ends - starts)[None][0] / max(np.isfinite(fu).sum(), 1))))
        # H3 second clause under two windows: of edits reverted under the dump rule but untagged, share whose first revert lies beyond the radius
        d1 = A.d3_first_sec.notna().to_numpy(); tag = b(A.is_reverted_d2); within = A.d3r_first_sec.notna().to_numpy()
        for lab, t0 in [("registered window (from 2020-08-01)", "2020-08-01"), ("from 2020-10-01", "2020-10-01")]:
            m = (A.anchor_ts >= pd.Timestamp(t0, tz=A.anchor_ts.dt.tz)).to_numpy() & d1 & ~tag
            h3.append(dict(wiki=w, window=lab, n_dump_only=int(m.sum()), share_beyond_radius=float((m & ~within).sum() / max(m.sum(), 1))))
        print("done", w, flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "rev_cluster_sensitivity.csv"), index=False)
    pd.DataFrame(h3).to_csv(os.path.join(OUT, "rev_h3_windows.csv"), index=False)


if __name__ == "__main__":
    main()
