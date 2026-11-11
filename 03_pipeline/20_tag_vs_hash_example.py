"""Worked example (round 3; exploratory): one cross-edition comparison computed twice, with the software's revert tag and with the hash-based radius rule.

For first edits of self-created accounts from October 2020 (page-history samples) the script reports, per edition,
  the share of first edits counted as reverted under the tag rule (mw-reverted on the measured edit) and under the 15-revision radius rule;
  the difference from English under each rule, with a bootstrap interval for the change in that difference between rules;
  the odds ratio of retention (an edit on days 2 to 60) for reverted versus non-reverted newcomers under each rule.
Output: 04_output/rev_example_tag_vs_hash.csv
"""
import os, sys
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "02_derived"); OUT = os.path.join(ROOT, "04_output")
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]; SEED = 20261112; B = 2000


def b(s): return s.fillna(False).astype(bool).to_numpy()


def orci(x, r):
    a = (x & r).sum() + .5; bb = (x & ~r).sum() + .5; c = (~x & r).sum() + .5; d = (~x & ~r).sum() + .5
    o = (a / bb) / (c / d); se = np.sqrt(1 / a + 1 / bb + 1 / c + 1 / d)
    return o, np.exp(np.log(o) - 1.96 * se), np.exp(np.log(o) + 1.96 * se)


def main():
    rng = np.random.default_rng(SEED); X = {}
    for w in WIKIS:
        A = pd.read_parquet(os.path.join(D, f"{w}_decomp.parquet"), columns=["created_by_self", "anchor_year", "anchor_ts", "is_reverted_d2", "d3r_first_sec", "retained_2_60"])
        A = A[A.created_by_self.fillna(False).astype(bool) & (A.anchor_ts >= pd.Timestamp("2020-10-01", tz=A.anchor_ts.dt.tz))]
        X[w] = (b(A.is_reverted_d2), A.d3r_first_sec.notna().to_numpy(), b(A.retained_2_60))
    en_t, en_r, _ = X["enwiki"]; rows = []
    for w in WIKIS:
        t, r, ret = X[w]; n = len(t); ot = orci(t, ret); orr = orci(r, ret)
        row = dict(wiki=w, n=n, p_tag=t.mean(), p_radius=r.mean(), understatement_pp=(r.mean() - t.mean()) * 100,
                   gap_to_english_tag_pp=(en_t.mean() - t.mean()) * 100, gap_to_english_radius_pp=(en_r.mean() - r.mean()) * 100,
                   OR_retention_tag=ot[0], OR_tag_lo=ot[1], OR_tag_hi=ot[2], OR_retention_radius=orr[0], OR_radius_lo=orr[1], OR_radius_hi=orr[2])
        if w != "enwiki":
            bs = []
            for _ in range(B):
                i = rng.integers(0, n, n); j = rng.integers(0, len(en_t), len(en_t))
                bs.append(((en_t[j].mean() - t[i].mean()) - (en_r[j].mean() - r[i].mean())) * 100)
            row["gap_change_pp"] = row["gap_to_english_tag_pp"] - row["gap_to_english_radius_pp"]; row["gap_change_lo"], row["gap_change_hi"] = np.percentile(bs, [2.5, 97.5])
        rows.append(row); print("done", w, flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "rev_example_tag_vs_hash.csv"), index=False)


if __name__ == "__main__":
    main()
