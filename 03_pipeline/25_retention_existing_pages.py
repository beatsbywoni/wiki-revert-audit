"""Retention by class of first reverter, with page-creating first edits removed (round 8; exploratory; page-history samples).

A first edit that creates a page cannot be identity-reverted, so it sits in the "not reverted" reference group; such edits are
0 percent of English first edits and 9 to 20 percent elsewhere. The script recomputes, on the page-history samples, the share of
newcomers who edit again on days 2 to 60 by class of first revert within 24 hours (dump rule), and the odds ratios against
non-reverted newcomers, for all sampled first edits and for first edits to existing pages only.
Output: 04_output/rev_retention_existing_pages.csv
"""
import os, warnings
import numpy as np, pandas as pd
warnings.simplefilter("ignore", FutureWarning)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "02_derived"); OUT = os.path.join(ROOT, "04_output")
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]


def b(s): return s.fillna(False).astype(bool).to_numpy()


def main():
    rows = []
    for w in WIKIS:
        A = pd.read_parquet(os.path.join(D, f"{w}_decomp.parquet"), columns=["user_id", "created_by_self", "anchor_year", "anchor_creates_page", "retained_2_60",
                                                                             "d3_first_sec", "d3_first_user", "d3_first_anon", "d3_first_bot", "d3_first_tool"])
        A = A[b(A.created_by_self) & (A.anchor_year >= 2019)].reset_index(drop=True)
        rev = (A.d3_first_sec <= 86400).fillna(False).to_numpy(); ret = b(A.retained_2_60); cp = b(A.anchor_creates_page)
        bot = rev & b(A.d3_first_bot); tool = rev & b(A.d3_first_tool) & ~bot; selfr = rev & (A.d3_first_user == A.user_id).to_numpy() & ~bot & ~tool
        anon = rev & b(A.d3_first_anon) & ~bot & ~tool & ~selfr; man = rev & ~bot & ~tool & ~selfr & ~anon
        for scope, keep in (("all first edits", np.ones(len(A), bool)), ("first edits to existing pages", ~cp)):
            base = keep & ~rev; p0 = ret[base].mean(); o0 = p0 / (1 - p0)
            row = dict(wiki=w, scope=scope, n=int(keep.sum()), share_creating_page=float(cp.mean()), retained_not_reverted=p0)
            for name, m in (("tool", tool), ("manual", man), ("self", selfr)):
                mm = keep & m; p = ret[mm].mean(); row[f"retained_{name}"] = p; row[f"OR_{name}"] = (p / (1 - p)) / o0
            rows.append(row)
        print("done", w, flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "rev_retention_existing_pages.csv"), index=False)


if __name__ == "__main__":
    main()
