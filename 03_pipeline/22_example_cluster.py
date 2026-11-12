"""Worked example (tag vs radius rule): interval for the change in the gap to English when reverting accounts are resampled (round 5; exploratory).
Clusters: the account that made the first revert under the radius rule; non-reverted edits and edits first reverted by an unregistered editor are singletons.
Output: 04_output/rev_example_cluster.csv
"""
import os
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "02_derived"); OUT = os.path.join(ROOT, "04_output")
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]; SEED = 20261112; B = 1000


def load(w):
    A = pd.read_parquet(os.path.join(D, f"{w}_decomp.parquet"), columns=["created_by_self", "anchor_ts", "is_reverted_d2", "d3r_first_sec", "d3r_first_user"])
    A = A[A.created_by_self.fillna(False).astype(bool) & (A.anchor_ts >= pd.Timestamp("2020-10-01", tz=A.anchor_ts.dt.tz))].reset_index(drop=True)
    n = len(A); t = A.is_reverted_d2.fillna(False).astype(bool).to_numpy().astype(float); r = A.d3r_first_sec.notna().to_numpy().astype(float)
    u = A.d3r_first_user.astype(float).to_numpy(); cl = np.where(np.isnan(u), -np.arange(1, n + 1), u)
    codes, inv = np.unique(cl, return_inverse=True); G = len(codes)
    ct = np.bincount(inv, weights=t, minlength=G); cr = np.bincount(inv, weights=r, minlength=G); cn = np.bincount(inv, minlength=G).astype(float)
    return ct, cr, cn


def main():
    rng = np.random.default_rng(SEED); X = {w: load(w) for w in WIKIS}; rows = []
    def draw(w):
        ct, cr, cn = X[w]; g = rng.integers(0, len(cn), len(cn)); N = cn[g].sum(); return ct[g].sum() / N, cr[g].sum() / N
    for w in WIKIS[1:]:
        bs = []
        for _ in range(B):
            et, er = draw("enwiki"); wt, wr = draw(w); bs.append(((et - wt) - (er - wr)) * 100)
        ct, cr, cn = X[w]; e = X["enwiki"]
        est = ((e[0].sum() / e[2].sum() - ct.sum() / cn.sum()) - (e[1].sum() / e[2].sum() - cr.sum() / cn.sum())) * 100
        lo, hi = np.percentile(bs, [2.5, 97.5]); rows.append(dict(wiki=w, gap_change_pp=est, cluster_lo=lo, cluster_hi=hi)); print(w, round(est, 2), round(lo, 2), round(hi, 2), flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "rev_example_cluster.csv"), index=False)


if __name__ == "__main__":
    main()
