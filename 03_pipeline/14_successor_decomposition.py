"""Successor decomposition, version 2 (post-review rounds 1 and 2; exploratory, registered code untouched).

For every sampled first-edit anchor the page history is re-read and, under BOTH attribution rules
(dump rule = unbounded hash search, "d3"; mwreverts rule = 15-revision radius, "d3r"), the script records

  first      the first revert of the anchor (revision id, seconds after the anchor, bot, tool, span = revisions undone)
  any2       the next revert of the anchor by anyone (any class), after the first
  nt1..nt5   the next five non-bot, non-tool reverts of the anchor after the first, each with: seconds after the anchor and
             after the first revert, number of intervening revisions, whether the anchor's exact content (hash) was reinstated
             in between, whether any state from the reverted span was reinstated
  context    whether the anchor created the page, revisions on the page before the anchor, revisions in the 30 days after the first revert

Users of all recorded reverting revisions are joined from <wiki>_reverters.parquet, so that a follow-up "by a third party"
(neither the anchor's author nor the account that made the first revert) can be selected afterwards (15_revision_tables.py).
Also written: 02_derived/<wiki>_target_revs.txt (reverting revision ids) and <wiki>_cohort_users.txt (cohort user ids),
the inputs of 18_stream_extract.py.

Usage: python 03_pipeline/14_successor_decomposition.py kowiki
"""
import argparse
import os
import sys
import time
from importlib import import_module

import numpy as np
import pandas as pd
import pyarrow.compute as pc
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(__file__))
schema = import_module("01_schema")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "02_derived")
RULES = ["d3", "d3r"]; K = 5; DAY30 = 30 * 86400


def analyze_page(sha, rid, parent, ts, bot, tool, anchor_pos, radius):
    n = len(sha)
    first_occ, prev_id, prev_idx = {}, {}, {}
    base_idx = np.full(n, -1, dtype=np.int64); noop = np.zeros(n, dtype=bool); mw_prev = np.full(n, -1, dtype=np.int64)
    for i in range(n):
        h = sha[i]
        if h == 0:
            continue
        if h in first_occ:
            mw_prev[i] = prev_idx[h]
            if parent[i] == prev_id[h]:
                noop[i] = True
            else:
                base_idx[i] = first_occ[h]
        else:
            first_occ[h] = i
        prev_id[h] = rid[i]; prev_idx[h] = i
    idx = np.arange(n); nt = ~bot & ~tool
    out = {}
    for i in anchor_pos:
        res = {"ctx": dict(anchor_creates_page=bool(parent[i] <= 0), page_revs_before=int(i))}
        cand = (idx > i) & (base_idx >= 0) & (base_idx < i)
        if not noop[i]:
            cand &= (sha != sha[i])
        candr = (idx > i) & (mw_prev >= 0) & (mw_prev < i) & ((idx - mw_prev - 1) <= radius)
        for rule, c in (("d3", np.flatnonzero(cand)), ("d3r", np.flatnonzero(candr))):
            if len(c) == 0:
                res[rule] = None
                continue
            j1 = c[0]
            r = dict(first_rev=int(rid[j1]), first_sec=float(ts[j1] - ts[i]), first_bot=bool(bot[j1]), first_tool=bool(tool[j1]),
                     first_span=int(j1 - i), n_cand=int(len(c)),
                     revs_30d_after_first=int(np.searchsorted(ts, ts[j1] + DAY30, side="right") - (j1 + 1)))
            later = c[1:]
            if len(later):
                j = later[0]
                r.update(any2_rev=int(rid[j]), any2_sec=float(ts[j] - ts[i]), any2_sec_after_first=float(ts[j] - ts[j1]), any2_bot=bool(bot[j]), any2_tool=bool(tool[j]))
            span_sha = set(sha[i:j1].tolist()) - {0}
            for k, j2 in enumerate(later[nt[later]][:K], start=1):
                mid_sha = sha[j1 + 1:j2]
                r.update({f"nt{k}_rev": int(rid[j2]), f"nt{k}_sec": float(ts[j2] - ts[i]), f"nt{k}_sec_after_first": float(ts[j2] - ts[j1]),
                          f"nt{k}_gap": int(len(mid_sha)), f"nt{k}_reinst_anchor": bool(len(mid_sha) and (mid_sha == sha[i]).any()),
                          f"nt{k}_reinst_span": bool(len(mid_sha) and any(h in span_sha for h in mid_sha.tolist()))})
            res[rule] = r
        out[int(rid[i])] = res
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("wiki"); ap.add_argument("--radius", type=int, default=schema.MWREVERTS_RADIUS); a = ap.parse_args()
    wiki = a.wiki; t0 = time.time()
    cols = ["anchor_rev_id", "page_id", "user_id", "anchor_ts", "anchor_year", "created_by_self", "anchor_rank", "anchor_on_allrevs",
            "is_reverted_d1", "sec_to_revert", "reverting_rev_id", "reverter_user_id", "reverter_is_anon", "reverter_is_bot", "reverter_is_tool",
            "reverter_is_undo", "is_reverted_d2", "retained_2_60"]
    A = pd.read_parquet(os.path.join(D, f"{wiki}_anchors.parquet"), columns=cols)
    full = A[(A.anchor_rank == 1) & (A.anchor_year >= 2019)]
    np.savetxt(os.path.join(D, f"{wiki}_cohort_users.txt"), full.user_id.dropna().astype("int64").unique(), fmt="%d")
    full_revs = full.reverting_rev_id.dropna().astype("int64").unique()
    A = A[(A.anchor_rank == 1) & A.anchor_on_allrevs.fillna(False).astype(bool)].reset_index(drop=True)
    pages = A.page_id.astype("int64").unique(); aids = set(A.anchor_rev_id.astype("int64").tolist())
    print(f"[{wiki}] anchors {len(A):,} on {len(pages):,} pages", flush=True)
    ar = pq.read_table(os.path.join(D, f"{wiki}_ns0_all_revs.parquet"), columns=["page_id", "revision_id", "parent", "sha", "ts", "is_bot", "is_tool"],
                       filters=pc.field("page_id").isin(pages.tolist())).to_pandas()
    print(f"  all_revs rows {len(ar):,}  {time.time()-t0:,.0f}s", flush=True)
    ar["is_anchor"] = ar.revision_id.isin(aids)
    ar = ar.sort_values(["page_id", "ts", "revision_id"], kind="mergesort").reset_index(drop=True)
    P = ar.page_id.to_numpy(); SHA = ar.sha.to_numpy(); RID = ar.revision_id.to_numpy(); PAR = ar.parent.to_numpy()
    TS = ar.ts.to_numpy().astype(np.int64); BOT = ar.is_bot.to_numpy().astype(bool); TOOL = ar.is_tool.to_numpy().astype(bool); ANC = ar.is_anchor.to_numpy()
    del ar
    starts = np.flatnonzero(np.r_[True, P[1:] != P[:-1]]); ends = np.r_[starts[1:], len(P)]
    res = {}
    for b, (s, e) in enumerate(zip(starts, ends)):
        apos = np.flatnonzero(ANC[s:e])
        if len(apos):
            res.update(analyze_page(SHA[s:e], RID[s:e], PAR[s:e], TS[s:e], BOT[s:e], TOOL[s:e], apos, a.radius))
        if b % 50000 == 0:
            print(f"  pages {b:,}/{len(starts):,}  {time.time()-t0:,.0f}s", flush=True)
    ids = A.anchor_rev_id.astype("int64").tolist()
    ctx = pd.DataFrame([(res.get(v) or {}).get("ctx", {}) for v in ids]); A = pd.concat([A, ctx], axis=1)
    fields = ["first_rev", "first_sec", "first_bot", "first_tool", "first_span", "n_cand", "revs_30d_after_first",
              "any2_rev", "any2_sec", "any2_sec_after_first", "any2_bot", "any2_tool"]
    for k in range(1, K + 1):
        fields += [f"nt{k}_{x}" for x in ["rev", "sec", "sec_after_first", "gap", "reinst_anchor", "reinst_span"]]
    for rule in RULES:
        recs = []
        for v in ids:
            r = (res.get(v) or {}).get(rule)
            recs.append([np.nan if r is None else r.get(f, np.nan) for f in fields])
        A = pd.concat([A, pd.DataFrame(recs, columns=[f"{rule}_{f}" for f in fields])], axis=1)
    revcols = [f"{r}_{k}_rev" for r in RULES for k in ["first", "any2"] + [f"nt{i}" for i in range(1, K + 1)]]
    need = pd.unique(pd.concat([A[c] for c in revcols]).dropna().astype("int64"))
    rv = pq.read_table(os.path.join(D, f"{wiki}_reverters.parquet"), columns=["revision_id", "event_user_id", "event_user_is_anonymous", "revision_tags"],
                       filters=pc.field("revision_id").isin(need.tolist())).to_pandas().drop_duplicates("revision_id").set_index("revision_id")
    for c in revcols:
        p = c[:-4]
        A[p + "_user"] = A[c].map(rv.event_user_id)
        A[p + "_anon"] = A[c].map(rv.event_user_is_anonymous)
        tags = A[c].map(rv.revision_tags).fillna("")
        A[p + "_undo"] = tags.str.contains(r"(?:^|,)\s*mw-undo\s*(?:,|$)")
        A[p + "_manualtag"] = tags.str.contains(r"(?:^|,)\s*mw-manual-revert\s*(?:,|$)")
    A["join_rate_first"] = A["d3_first_rev"].map(lambda v: (v in rv.index) if pd.notna(v) else np.nan)
    A.to_parquet(os.path.join(D, f"{wiki}_decomp.parquet"), index=False)
    np.savetxt(os.path.join(D, f"{wiki}_target_revs.txt"), np.unique(np.r_[need, full_revs]), fmt="%d")
    print(f"[{wiki}] decomp v2 written {time.time()-t0:,.0f}s; anchors {len(A):,}; join rate {A.join_rate_first.mean():.4f}; "
          f"target revisions {len(np.unique(np.r_[need, full_revs])):,}; cohort users {full.user_id.nunique():,}", flush=True)


if __name__ == "__main__":
    main()
