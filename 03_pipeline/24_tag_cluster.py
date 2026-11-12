"""Tag coverage with intervals that respect clustering in reverting accounts (round 7; exploratory).

For first edits of self-created accounts from October 2020 that are reverted under the 15-revision radius rule (page-history samples),
the script reports the share whose measured edit carries no mw-reverted tag, by class of first reverter and, for tool and other
manual reverters, by whether the reverting account held, at the time of the revert, a group that carries the autopatrol or autoreview right in that edition. Each cell has the
number of reverts, the number of reverting accounts, the share of reverts made by the most active account, a Wilson interval and a
percentile interval from 2,000 resamples of reverting accounts (unregistered reverters and self-reverts are their own clusters).
Output: 04_output/rev_taggap_cluster.csv
"""
import os, warnings
import numpy as np, pandas as pd
warnings.simplefilter("ignore", FutureWarning)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "02_derived"); OUT = os.path.join(ROOT, "04_output")
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]; SEED = 20261112; B = 2000; MINCELL = 50
AUTOP = {"autopatrolled", "autoreviewer", "sysop", "bot", "rollbacker", "patroller", "editor", "reviewer", "bureaucrat", "interface-admin",
         "checkuser", "suppress", "oversight", "steward", "abusefilter", "flood", "botadmin", "mover"}


# Groups that carry the autopatrol right (recent-changes patrolling) or the autoreview right (FlaggedRevs) in each edition's own
# configuration (operations/mediawiki-config, core-Permissions.php and flaggedrevs.php, read 12 November 2026; sysop and bot by core default).
# Editions without either regime keep the union list, which has no bearing there.
AUTOP_BY_WIKI = {"itwiki": {"autopatrolled", "botadmin", "rollbacker", "sysop", "bot"}, "frwiki": {"autopatrolled", "sysop", "bot"},
                 "dewiki": {"editor", "reviewer", "autoreview", "sysop", "bot"}, "plwiki": {"editor", "reviewer", "autoreview", "sysop", "bot"}}


def b(s): return s.fillna(False).astype(bool).to_numpy()


def wilson(k, n, z=1.959964):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def main():
    rng = np.random.default_rng(SEED); rows = []
    for w in WIKIS:
        A = pd.read_parquet(os.path.join(D, f"{w}_decomp.parquet"), columns=["user_id", "created_by_self", "anchor_ts", "is_reverted_d2", "d3r_first_sec", "d3r_first_rev",
                                                                             "d3r_first_user", "d3r_first_anon", "d3r_first_bot", "d3r_first_tool"])
        A = A[b(A.created_by_self) & (A.anchor_ts >= pd.Timestamp("2020-10-01", tz=A.anchor_ts.dt.tz)) & A.d3r_first_sec.notna()].reset_index(drop=True)
        G = pd.read_csv(os.path.join(D, f"{w}_revgroups.tsv"), sep="\t", dtype=str, usecols=["revision_id", "event_user_groups_historical"]).drop_duplicates("revision_id")
        G["event_user_groups_historical"] = G.event_user_groups_historical.fillna("")
        G.index = G.revision_id.astype("int64"); gh = A.d3r_first_rev.astype("int64").map(G.event_user_groups_historical)
        known = gh.notna().to_numpy(); AP = AUTOP_BY_WIKI.get(w, AUTOP); has_ap = gh.fillna("").map(lambda s: bool(set(x for x in s.split(",") if x) & AP)).to_numpy()
        anon = b(A.d3r_first_anon); bot = b(A.d3r_first_bot) & ~anon; selfr = (A.d3r_first_user == A.user_id).to_numpy() & ~anon & ~bot
        tool = b(A.d3r_first_tool) & ~anon & ~bot & ~selfr; man = ~anon & ~bot & ~selfr & ~tool
        un = ~b(A.is_reverted_d2)
        # cluster id: reverting account; unregistered reverters and self-reverts are singletons
        cid = A.d3r_first_user.fillna(-1).astype("int64").to_numpy().copy(); single = anon | selfr | (cid < 0)
        cid[single] = -(np.arange(len(A))[single] + 2)
        cells = {"all": np.ones(len(A), bool), "bot": bot, "tool": tool, "other manual": man, "unregistered": anon, "self": selfr,
                 "tool, autopatrol-carrying group": tool & known & has_ap, "tool, no such group": tool & known & ~has_ap,
                 "other manual, autopatrol-carrying group": man & known & has_ap, "other manual, no such group": man & known & ~has_ap}
        for name, m in cells.items():
            n = int(m.sum())
            if n < MINCELL: continue
            k = int((m & un).sum()); lo, hi = wilson(k, n)
            df = pd.DataFrame({"c": cid[m], "u": un[m].astype(int)}).groupby("c").agg(n=("u", "size"), k=("u", "sum"))
            nn = df.n.to_numpy(); kk = df.k.to_numpy(); C = len(df)
            idx = rng.integers(0, C, (B, C)); bs = kk[idx].sum(1) / nn[idx].sum(1)
            rows.append(dict(wiki=w, cell=name, reverts=n, accounts=C, top_account_share=nn.max() / n, untagged=k / n, wilson_lo=lo, wilson_hi=hi,
                             cluster_lo=np.percentile(bs, 2.5), cluster_hi=np.percentile(bs, 97.5)))
        print("done", w, flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "rev_taggap_cluster.csv"), index=False)


if __name__ == "__main__":
    main()
