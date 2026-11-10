"""Post-review reanalysis (simulated review round 1, 2026-11-10): what the replace variant and S actually measure.

For every sampled first-edit anchor (anchor_on_allrevs) the page history is re-read and, under BOTH attribution rules
(dump rule = unbounded hash search, "d3"; mwreverts rule = 15-revision radius, "d3r"), the script records

  first        the first revert of the anchor by anyone (revision id, seconds, bot, tool, span = revisions undone)
  ntaf         the first non-bot non-tool revert of the anchor that comes AFTER the first revert
               (for bot/tool-first anchors this is the registered replace event; for manually-first anchors it is the
               placebo: a second manual revert of an anchor that a human already reverted)
  between      what happened between first and ntaf: number of intervening revisions, whether the anchor's exact
               content (sha) was reinstated, whether any state from the reverted span was reinstated

Reverting users come from <wiki>_reverters.parquet (join on revision id): self-revert = reverting user is the anchor's
author. Nothing registered is changed; output goes to 02_derived/<wiki>_decomp.parquet and 04_output/decomp_<wiki>_*.csv.

Usage: python 03_pipeline/14_successor_decomposition.py kowiki            (compute + summarise)
       python 03_pipeline/14_successor_decomposition.py kowiki --summary-only
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
D = os.path.join(ROOT, "02_derived"); O = os.path.join(ROOT, "04_output")
WINS = [("W24h", 86400), ("W7d", 604800), ("W180d", 15552000), ("Winf", None)]
RULES = ["d3", "d3r"]
SEED = 20261110


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
        res = {}
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
                     first_span=int(j1 - i), n_cand=int(len(c)))
            later = c[1:]
            later_nt = later[nt[later]]
            if len(later_nt):
                j2 = later_nt[0]
                mid = np.arange(j1 + 1, j2)
                span_sha = set(sha[i:j1].tolist()) - {0}
                r.update(ntaf_rev=int(rid[j2]), ntaf_sec=float(ts[j2] - ts[i]), ntaf_gap=int(len(mid)),
                         ntaf_reinst_anchor=bool(len(mid) and (sha[mid] == sha[i]).any()),
                         ntaf_reinst_span=bool(len(mid) and any(h in span_sha for h in sha[mid].tolist())),
                         ntaf_sec_after_first=float(ts[j2] - ts[j1]))
            res[rule] = r
        out[int(rid[i])] = res
    return out


def compute(wiki, radius):
    t0 = time.time()
    cols = ["anchor_rev_id", "page_id", "user_id", "anchor_ts", "anchor_year", "created_by_self", "anchor_rank", "anchor_on_allrevs",
            "is_reverted_d1", "sec_to_revert", "reverting_rev_id", "reverter_user_id", "reverter_is_anon", "reverter_is_bot", "reverter_is_tool",
            "reverter_is_undo", "reverter_is_manual", "is_reverted_d2", "retained_2_60",
            "d3_sec_to_revert", "d3nt_sec_to_revert", "d3r_sec_to_revert", "d3rnt_sec_to_revert"]
    A = pd.read_parquet(os.path.join(D, f"{wiki}_anchors.parquet"), columns=cols)
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
            res.update(analyze_page(SHA[s:e], RID[s:e], PAR[s:e], TS[s:e], BOT[s:e], TOOL[s:e], apos, radius))
        if b % 50000 == 0:
            print(f"  pages {b:,}/{len(starts):,}  {time.time()-t0:,.0f}s", flush=True)
    fields = ["first_rev", "first_sec", "first_bot", "first_tool", "first_span", "n_cand",
              "ntaf_rev", "ntaf_sec", "ntaf_gap", "ntaf_reinst_anchor", "ntaf_reinst_span", "ntaf_sec_after_first"]
    for rule in RULES:
        recs = []
        for v in A.anchor_rev_id.astype("int64"):
            r = (res.get(int(v)) or {}).get(rule)
            recs.append([np.nan if r is None else r.get(f, np.nan) for f in fields])
        R = pd.DataFrame(recs, columns=[f"{rule}_{f}" for f in fields])
        A = pd.concat([A, R], axis=1)
    # users of reverting revisions
    need = pd.unique(pd.concat([A[f"{r}_{k}"] for r in RULES for k in ("first_rev", "ntaf_rev")]).dropna().astype("int64"))
    rv = pq.read_table(os.path.join(D, f"{wiki}_reverters.parquet"), columns=["revision_id", "event_user_id", "event_user_is_anonymous", "revision_tags"],
                       filters=pc.field("revision_id").isin(need.tolist())).to_pandas().drop_duplicates("revision_id").set_index("revision_id")
    for r in RULES:
        for k in ("first", "ntaf"):
            ids = A[f"{r}_{k}_rev"]
            A[f"{r}_{k}_user"] = ids.map(rv.event_user_id)
            A[f"{r}_{k}_anon"] = ids.map(rv.event_user_is_anonymous)
            A[f"{r}_{k}_joined"] = ids.map(lambda v: (v in rv.index) if pd.notna(v) else np.nan)
            A[f"{r}_{k}_self"] = (A[f"{r}_{k}_user"].astype(float) == A.user_id.astype(float)) & A[f"{r}_{k}_user"].notna()
            tags = ids.map(rv.revision_tags).fillna("")
            A[f"{r}_{k}_undo"] = tags.str.contains(r"(?:^|,)\s*mw-undo\s*(?:,|$)")
            A[f"{r}_{k}_manualtag"] = tags.str.contains(r"(?:^|,)\s*mw-manual-revert\s*(?:,|$)")
    A.to_parquet(os.path.join(D, f"{wiki}_decomp.parquet"), index=False)
    print(f"[{wiki}] decomp written {time.time()-t0:,.0f}s; join rate first {A['d3_first_joined'].mean():.4f}", flush=True)


def inw(sec, w):
    s = sec.astype(float)
    return s.notna() & ((s <= w) if w is not None else True)


def boot_ci(fn, n, B=2000, seed=SEED):
    rng = np.random.default_rng(seed); est = []
    for _ in range(B):
        est.append(fn(rng.integers(0, n, n)))
    return np.nanpercentile(est, [2.5, 97.5])


def summarise(wiki):
    A = pd.read_parquet(os.path.join(D, f"{wiki}_decomp.parquet"))
    A = A[A.created_by_self.fillna(False).astype(bool) & (A.anchor_year >= 2019)].reset_index(drop=True)
    n = len(A)
    rows_rs, rows_cls, rows_dec, rows_self, rows_tag = [], [], [], [], []
    for rule in RULES:
        fs = A[f"{rule}_first_sec"]; fbot = A[f"{rule}_first_bot"].fillna(False).astype(bool); ftool = A[f"{rule}_first_tool"].fillna(False).astype(bool)
        fself = A[f"{rule}_first_self"].fillna(False).astype(bool); fanon = A[f"{rule}_first_anon"].fillna(False).astype(bool)
        cls = np.select([fs.isna(), fbot, ftool, fself, fanon], ["none", "bot", "tool", "self", "anon"], default="manual_other")
        A[f"{rule}_cls"] = cls
        auto = fbot | ftool
        # replace event: first nt revert = first itself if manual, else ntaf
        nt_sec = np.where(auto, A[f"{rule}_ntaf_sec"], fs).astype(float); nt_sec = pd.Series(np.where(fs.isna(), np.nan, nt_sec))
        # ---- R and S with bootstrap CI
        r0 = {w: inw(fs, s).to_numpy() for w, s in WINS}; r2 = {w: inw(nt_sec, s).to_numpy() for w, s in WINS}
        st = {w: (inw(fs, s) & ~auto).to_numpy() for w, s in WINS}   # strict
        for w, _ in WINS:
            d_rep = (r0[w].mean() - r2[w].mean()) * 100; d_str = (r0[w].mean() - st[w].mean()) * 100
            S = 1 - d_rep / d_str if d_str > 0 else np.nan
            lo, hi = boot_ci(lambda ix: 1 - (r0[w][ix].mean() - r2[w][ix].mean()) / (r0[w][ix].mean() - st[w][ix].mean()), n, B=1000)
            rows_rs.append(dict(wiki=wiki, rule=rule, W=w, n=n, p_F0=r0[w].mean(), delta_strict_pp=d_str, delta_replace_pp=d_rep, S=S, S_lo=lo, S_hi=hi))
        Rv = (r0["Winf"].mean() - r2["Winf"].mean()) / (r0["W24h"].mean() - r2["W24h"].mean())
        lo, hi = boot_ci(lambda ix: (r0["Winf"][ix].mean() - r2["Winf"][ix].mean()) / (r0["W24h"][ix].mean() - r2["W24h"][ix].mean()), n, B=1000)
        lo180, hi180 = boot_ci(lambda ix: (r0["W180d"][ix].mean() - r2["W180d"][ix].mean()) / (r0["W24h"][ix].mean() - r2["W24h"][ix].mean()), n, B=1000)
        rows_rs.append(dict(wiki=wiki, rule=rule, W="R_inf_over_24h", n=n, S=Rv, S_lo=lo, S_hi=hi))
        rows_rs.append(dict(wiki=wiki, rule=rule, W="R_180d_over_24h", n=n,
                            S=(r0["W180d"].mean() - r2["W180d"].mean()) / (r0["W24h"].mean() - r2["W24h"].mean()), S_lo=lo180, S_hi=hi180))
        # ---- follow-up manual revert by class of first reverter (placebo)
        for w, s in WINS:
            f_in = inw(fs, s)
            for c in ["bot", "tool", "manual_other", "anon", "self"]:
                m = f_in & (cls == c)
                k = int(m.sum())
                if k == 0:
                    continue
                fol = inw(A[f"{rule}_ntaf_sec"], s) & m
                fol_other = fol & ~A[f"{rule}_ntaf_self"].fillna(False).astype(bool)
                p = fol.sum() / k; se = np.sqrt(p * (1 - p) / k)
                rows_cls.append(dict(wiki=wiki, rule=rule, W=w, first_class=c, n_first=k, share_of_first=k / int(f_in.sum()),
                                     p_followup_manual=p, lo=p - 1.96 * se, hi=p + 1.96 * se,
                                     p_followup_manual_not_self=fol_other.sum() / k,
                                     median_span=float(A.loc[m, f"{rule}_first_span"].median())))
        # ---- what is the follow-up event (for bot/tool-first vs manual-first), by window
        for w, s in WINS:
            for grp, gm in [("auto_first", auto), ("manual_first", (cls == "manual_other") | (cls == "anon"))]:
                m = inw(fs, s) & gm & inw(A[f"{rule}_ntaf_sec"], s)
                k = int(m.sum())
                if k == 0:
                    continue
                gap = A.loc[m, f"{rule}_ntaf_gap"]; ra = A.loc[m, f"{rule}_ntaf_reinst_anchor"].fillna(False).astype(bool)
                rs_ = A.loc[m, f"{rule}_ntaf_reinst_span"].fillna(False).astype(bool); sf = A.loc[m, f"{rule}_ntaf_self"].fillna(False).astype(bool)
                rows_dec.append(dict(wiki=wiki, rule=rule, W=w, group=grp, n_followups=k,
                                     reinstated_anchor=ra.mean(), reinstated_span_not_anchor=(rs_ & ~ra).mean(),
                                     immediate_deeper=((gap == 0) & ~rs_).mean(), other_churn=((gap > 0) & ~rs_).mean(),
                                     followup_by_anchor_author=sf.mean(), median_gap=float(gap.median()),
                                     median_days_after_first=float(A.loc[m, f"{rule}_ntaf_sec_after_first"].median() / 86400)))
        # ---- self-reverts and Table-1 style quantities without them
        for w, s in [("W24h", 86400), ("Winf", None)]:
            f_in = inw(fs, s)
            comp = {c: (f_in & (cls == c)).mean() for c in ["bot", "tool", "self", "anon", "manual_other"]}
            ns = ~(f_in & (cls == "self"))   # drop anchors whose first revert (in window) is a self-revert
            p0 = f_in[ns].mean(); pst = (f_in & ~auto)[ns].mean(); prep = inw(nt_sec, s)[ns.to_numpy()].mean()
            ret = A.retained_2_60.astype(bool)
            def orr(x, mask):
                x = x[mask]; r = ret[mask]
                a = (x & r).sum() + .5; b = (x & ~r).sum() + .5; c_ = (~x & r).sum() + .5; d_ = (~x & ~r).sum() + .5
                return a * d_ / (b * c_)
            allm = pd.Series(True, index=A.index)
            rows_self.append(dict(wiki=wiki, rule=rule, W=w, n=n, p_F0=f_in.mean(), **{f"p_first_{k}": v for k, v in comp.items()},
                                  self_share_of_first=comp["self"] / f_in.mean(), n_excl_self=int(ns.sum()), p_F0_excl_self=p0,
                                  delta_strict_excl_self_pp=(p0 - pst) * 100, delta_replace_excl_self_pp=(p0 - prep) * 100,
                                  S_excl_self=1 - (p0 - prep) / (p0 - pst) if p0 > pst else np.nan,
                                  OR_F0_all=orr(f_in, allm), OR_F0_excl_self=orr(f_in, ns),
                                  OR_F2strict_all=orr(f_in & ~auto, allm), OR_F2strict_excl_self=orr(f_in & ~auto, ns)))
    # ---- tag gap (within-radius identity reverts, anchors from 2020-08) by who reverted
    g = A[(A.anchor_ts >= pd.Timestamp("2020-08-01", tz=A.anchor_ts.dt.tz)) & A.d3r_first_sec.notna()]
    d2 = g.is_reverted_d2.fillna(False).astype(bool)
    def tagrow(label, m):
        k = int(m.sum())
        return dict(wiki=wiki, group=label, n=k, share_of_within_radius=k / len(g), untagged=float((~d2[m]).mean()) if k else np.nan,
                    share_of_all_untagged=float((~d2 & m).sum() / max((~d2).sum(), 1)))
    c15 = g["d3r_cls"]
    rows_tag.append(tagrow("all", pd.Series(True, index=g.index)))
    for c in ["bot", "tool", "self", "anon", "manual_other"]:
        rows_tag.append(tagrow(c, c15 == c))
    mo = c15 == "manual_other"
    rows_tag.append(tagrow("manual_other: undo tag", mo & g.d3r_first_undo.fillna(False).astype(bool)))
    rows_tag.append(tagrow("manual_other: manual-revert tag only", mo & g.d3r_first_manualtag.fillna(False).astype(bool) & ~g.d3r_first_undo.fillna(False).astype(bool)))
    rows_tag.append(tagrow("manual_other: no revert tag", mo & ~g.d3r_first_manualtag.fillna(False).astype(bool) & ~g.d3r_first_undo.fillna(False).astype(bool)))
    rows_tag.append(tagrow("span = 1 (anchor only)", g.d3r_first_span == 1))
    rows_tag.append(tagrow("span 2-15", g.d3r_first_span > 1))
    # reverse cell: tagged but not identity-reverted within radius
    allp = A[A.anchor_ts >= pd.Timestamp("2020-08-01", tz=A.anchor_ts.dt.tz)]
    d2a = allp.is_reverted_d2.fillna(False).astype(bool)
    rows_tag.append(dict(wiki=wiki, group="REVERSE: tagged, no radius-15 identity revert", n=int((d2a & allp.d3r_first_sec.isna()).sum()),
                         share_of_within_radius=float((d2a & allp.d3r_first_sec.isna()).sum() / max(d2a.sum(), 1)), untagged=np.nan, share_of_all_untagged=np.nan))
    for name, rows in [("rs", rows_rs), ("followup_by_class", rows_cls), ("followup_type", rows_dec), ("self", rows_self), ("taggap", rows_tag)]:
        pd.DataFrame(rows).to_csv(os.path.join(O, f"decomp_{wiki}_{name}.csv"), index=False)
    T = pd.DataFrame(rows_rs)
    print(T[T.W.isin(["W24h", "Winf", "R_inf_over_24h", "R_180d_over_24h"])][["rule", "W", "delta_strict_pp", "delta_replace_pp", "S", "S_lo", "S_hi"]].round(3).to_string(index=False))
    C = pd.DataFrame(rows_cls)
    print(C[C.W.isin(["W24h", "Winf"])][["rule", "W", "first_class", "n_first", "share_of_first", "p_followup_manual", "p_followup_manual_not_self"]].round(3).to_string(index=False))
    print(pd.DataFrame(rows_dec).round(3).to_string(index=False))
    print(pd.DataFrame(rows_self)[["rule", "W", "p_F0", "self_share_of_first", "delta_strict_excl_self_pp", "delta_replace_excl_self_pp", "S_excl_self",
                                   "OR_F0_all", "OR_F0_excl_self", "OR_F2strict_all", "OR_F2strict_excl_self"]].round(3).to_string(index=False))
    print(pd.DataFrame(rows_tag).round(3).to_string(index=False))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("wiki"); ap.add_argument("--radius", type=int, default=schema.MWREVERTS_RADIUS)
    ap.add_argument("--summary-only", action="store_true"); a = ap.parse_args()
    if not a.summary_only:
        compute(a.wiki, a.radius)
    summarise(a.wiki)


if __name__ == "__main__":
    main()
