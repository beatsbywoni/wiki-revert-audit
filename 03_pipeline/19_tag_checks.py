"""Two exploratory checks added in review round 2 (registered code untouched).

(1) rev_taggap_editcount.csv: untagged share of radius-rule first reverts (first edits from October 2020) made by
    registered accounts with NO explicit user group (not the author, not a bot, no tool tag), by the reverting account's
    edit count at the time of the revert. Tests whether implicit, edit-count-based promotion (as on the French edition,
    where the autopatrolled status is granted automatically) accounts for tagged reverts by accounts without a group.
(2) rev_tooltags.csv: number of reverting revisions (all recorded reverters of cohort first edits) carrying each
    change tag that names a semi-automated tool, by edition, to show which tools the "one-click tool" class can see.

Usage: python 03_pipeline/19_tag_checks.py [wiki ...]   |   python 03_pipeline/19_tag_checks.py toolwide [wiki ...]
"""
import os, sys, re
from collections import Counter
import numpy as np, pandas as pd, pyarrow.parquet as pq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "02_derived"); OUT = os.path.join(ROOT, "04_output")
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]
TOOLPAT = re.compile(r"rollback|huggle|twinkle|redwarn|ultraviolet|stiki|antivandal|swviewer|liverc|igloo|lupin|popups|fastbuttons|revertbot|cluebot", re.I)
MINCELL = 50


def wilson(k, n, z=1.959964):
    if n == 0: return (np.nan, np.nan)
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def b(s): return s.fillna(False).astype(bool).to_numpy()


def main():
    wikis = sys.argv[1:] or WIKIS; rows, tags = [], []
    for w in wikis:
        A = pd.read_parquet(os.path.join(D, f"{w}_decomp.parquet"))
        A = A[A.created_by_self.fillna(False).astype(bool) & (A.anchor_year >= 2019)]
        A = A[(A.anchor_ts >= pd.Timestamp("2020-10-01", tz=A.anchor_ts.dt.tz)) & A.d3r_first_sec.notna()].reset_index(drop=True)
        G = pd.read_csv(os.path.join(D, f"{w}_revgroups.tsv"), sep="\t", dtype=str).drop_duplicates("revision_id")
        G.index = G.revision_id.astype("int64"); r = A.d3r_first_rev.astype("int64")
        gh = r.map(G.event_user_groups_historical).fillna("").to_numpy()
        rc = pd.to_numeric(r.map(G.event_user_revision_count), errors="coerce")
        m = (gh == "") & ~b(A.d3r_first_anon) & ~(A.d3r_first_user == A.user_id).to_numpy() & ~b(A.d3r_first_bot) & ~b(A.d3r_first_tool) & rc.notna().to_numpy()
        un = ~b(A.is_reverted_d2)
        bins = pd.cut(rc, [-1, 49, 499, 4999, 1e12], labels=["under 50", "50 to 499", "500 to 4,999", "5,000 or more"])
        for lab in bins.cat.categories:
            mm = m & (bins == lab).to_numpy(); n = int(mm.sum())
            if n < MINCELL: continue
            k = int((mm & un).sum()); lo, hi = wilson(k, n)
            rows.append(dict(wiki=w, reverter_edit_count=lab, n=n, untagged=k / n, lo=lo, hi=hi))
        cnt = Counter(); tot = 0
        pf = pq.ParquetFile(os.path.join(D, f"{w}_reverters.parquet"))
        for batch in pf.iter_batches(columns=["revision_tags"], batch_size=500000):
            s = batch.column(0).to_pylist(); tot += len(s)
            for t in s:
                if t and TOOLPAT.search(t):
                    for x in t.split(","):
                        x = x.strip()
                        if TOOLPAT.search(x): cnt[x] += 1
        for k, v in sorted(cnt.items(), key=lambda kv: -kv[1]):
            tags.append(dict(wiki=w, tag=k, reverting_revisions=v, share_of_recorded_reverts=v / tot))
        print("done", w, flush=True)
    for name, new in (("rev_taggap_editcount", rows), ("rev_tooltags", tags)):
        path = os.path.join(OUT, name + ".csv"); new = pd.DataFrame(new)
        if len(wikis) < len(WIKIS) and os.path.exists(path):
            old = pd.read_csv(path); new = pd.concat([old[~old.wiki.isin(wikis)], new])
        new.to_csv(path, index=False)




# (3) rev_toolwide.csv: share of first reverts within 24 hours (full cohort, dump rule) that carry a wider set of tool tags
#     (RedWarn, Ultraviolet, AntiVandal script, STiki, LiveRC, MassRollback) but were NOT in the registered tool class.
WIDE = re.compile(r"redwarn|ultraviolet|antivandal|stiki|liverc|massrollback", re.I)


def toolwide():
    wikis = sys.argv[2:] or WIKIS; rows = []
    for w in wikis:
        cols = ["anchor_rank", "anchor_year", "created_by_self", "is_reverted_d1", "sec_to_revert", "reverting_rev_id", "reverter_is_bot", "reverter_is_tool"]
        A = pd.read_parquet(os.path.join(D, f"{w}_anchors.parquet"), columns=cols)
        A = A[(A.anchor_rank == 1) & (A.anchor_year >= 2019) & A.created_by_self.fillna(False).astype(bool)]
        A = A[A.is_reverted_d1.fillna(False).astype(bool) & (A.sec_to_revert <= 86400)]
        G = pd.read_csv(os.path.join(D, f"{w}_revgroups.tsv"), sep="\t", dtype=str, usecols=["revision_id", "revision_tags"]).drop_duplicates("revision_id")
        G.index = G.revision_id.astype("int64"); tg = A.reverting_rev_id.astype("int64").map(G.revision_tags).fillna("")
        wide = tg.str.contains(WIDE).to_numpy(); tool = b(A.reverter_is_tool); bot = b(A.reverter_is_bot); n = len(A)
        for y, m in [("2019+", np.ones(n, bool)), ("2021+", (A.anchor_year >= 2021).to_numpy())]:
            k = int(m.sum())
            rows.append(dict(wiki=w, cohort=y, n_first_reverts_24h=k, share_tool_registered=float((tool & ~bot & m).sum() / k),
                             share_wide_tag_outside_tool_class=float((wide & ~tool & ~bot & m).sum() / k),
                             share_wide_tag_any=float((wide & m).sum() / k)))
        print("done", w, flush=True)
    path = os.path.join(OUT, "rev_toolwide.csv"); new = pd.DataFrame(rows)
    if len(wikis) < len(WIKIS) and os.path.exists(path):
        old = pd.read_csv(path); new = pd.concat([old[~old.wiki.isin(wikis)], new])
    new.to_csv(path, index=False)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "toolwide":
        toolwide()
    else:
        main()
