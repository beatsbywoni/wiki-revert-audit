"""Revision tables, version 2 (post-review rounds 1 and 2; exploratory unless marked registered).

Inputs: 02_derived/<wiki>_anchors.parquet (full cohort), <wiki>_decomp.parquet (page-history sample, script 14 v2),
        optional <wiki>_revgroups.tsv and <wiki>_blocks.tsv (script 18).
Outputs in 04_output/ (cells with fewer than 50 observations are suppressed, as registered):
  rev_composition.csv   first reverts by class (bot, one-click tool, other registered manual, unregistered or temporary, self),
                        Wilson intervals and reverter-cluster bootstrap intervals, strict effect of excluding each class,
                        number of distinct reverting accounts and share of the most active account, undo share
  rev_retention.csv     retention (edit on days 2-60) by class of first revert within 24 h; with blocked newcomers removed where available
  rev_followup.csv      later manual revert by a THIRD PARTY (not the author, not the first reverter) after the first revert,
                        by class of first reverter, rule, clock (from the anchor / from the first revert) and window; components;
                        by tercile of page activity; any later revert by class of the second reverter
  rev_window.csv        R = replace effect at the longer window / effect within 24 h, both rules, 2,000 bootstrap resamples
  rev_taggap.csv        untagged share of radius-rule reverts (first edits from October 2020) by class, by year, and by
                        whether the reverting account held an autopatrol-carrying group (where script 18 output exists)
  rev_h4_boot2000.csv   registered H4 ratio with 2,000 replicates, and the same ratio over the three 24-hour cells only
  rev_context.csv       sample context: page-creating first edits, first-revert span, agreement of rules
Usage: python 03_pipeline/15_revision_tables.py [wiki ...]
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "02_derived"); O = os.path.join(ROOT, "04_output")
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]
ROLE = {"kowiki": "exploratory", "enwiki": "exploratory", "frwiki": "exploratory", "dewiki": "exploratory",
        "jawiki": "confirmatory", "plwiki": "confirmatory", "itwiki": "confirmatory"}
CLASSES = ["bot", "tool", "manual_other", "anon", "self"]
AUTOP = {"autopatrolled", "autoreviewer", "sysop", "bot", "rollbacker", "patroller", "editor", "reviewer", "bureaucrat", "interface-admin",
         "checkuser", "suppress", "oversight", "steward", "abusefilter", "flood", "botadmin", "mover"}
SEED = 20261110; B = 2000; MINCELL = 50
WINS = [("W24h", 86400), ("W7d", 604800), ("W180d", 15552000), ("Winf", None)]


def wilson(k, n, z=1.959964):
    if n == 0: return (np.nan, np.nan)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def inw(sec, w):
    s = pd.Series(sec).astype(float)
    return (s.notna() & ((s <= w) if w is not None else True)).to_numpy()


def woolf(x, r):
    a = (x & r).sum() + .5; b = (x & ~r).sum() + .5; c = (~x & r).sum() + .5; d = (~x & ~r).sum() + .5
    lor = np.log(a * d / (b * c)); se = np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    return np.exp(lor), np.exp(lor - 1.96 * se), np.exp(lor + 1.96 * se)


def boolcol(s):
    return s.fillna(False).astype(bool).to_numpy()


def full_cohort(wiki, min_year=2019):
    cols = ["anchor_rank", "anchor_year", "anchor_ts", "created_by_self", "user_id", "is_reverted_d1", "sec_to_revert", "reverter_user_id", "reverter_is_anon",
            "reverter_is_bot", "reverter_is_tool", "reverter_is_undo", "retained_2_60"]
    A = pd.read_parquet(os.path.join(D, f"{wiki}_anchors.parquet"), columns=cols)
    A = A[(A.anchor_rank == 1) & (A.anchor_year >= min_year) & A.created_by_self.fillna(False).astype(bool)].reset_index(drop=True)
    rev = boolcol(A.is_reverted_d1); bot = boolcol(A.reverter_is_bot); tool = boolcol(A.reverter_is_tool); anon = boolcol(A.reverter_is_anon)
    self_ = (A.reverter_user_id.astype(float) == A.user_id.astype(float)).fillna(False).to_numpy() & A.reverter_user_id.notna().to_numpy()
    A["cls"] = np.select([~rev, bot, tool, self_, anon], ["none", "bot", "tool", "self", "anon"], default="manual_other")
    A["undo"] = boolcol(A.reverter_is_undo)
    return A


def composition(wiki, R):
    rng = np.random.default_rng(SEED)
    blocks = None
    bp = os.path.join(D, f"{wiki}_blocks.tsv")
    if os.path.exists(bp):
        bl = pd.read_csv(bp, sep="\t", dtype=str)
        bl = bl[bl.user_blocks_historical.fillna("").ne("") | bl.user_blocks.fillna("").ne("")]
        bl["ts"] = pd.to_datetime(bl.event_timestamp, errors="coerce", utc=True); bl["user_id"] = bl.user_id.astype("int64")
        blocks = bl.groupby("user_id").ts.min()
    for label, min_year in [("2019+", 2019), ("2021+", 2021)]:
        A = full_cohort(wiki, min_year); n = len(A); ret = boolcol(A.retained_2_60); cl = A.cls.to_numpy()
        for wn, ws in [("W24h", 86400), ("Winf", None)]:
            f0 = boolcol(A.is_reverted_d1) & inw(A.sec_to_revert, ws); k0 = int(f0.sum())
            r = dict(wiki=wiki, role=ROLE[wiki], cohort=label, W=wn, n=n, p_F0=k0 / n)
            # reverter-cluster bootstrap: resample reverting accounts (unregistered reverters are singletons)
            g = A.loc[f0, ["reverter_user_id", "cls"]].copy()
            g["acct"] = np.where(g.reverter_user_id.notna(), g.reverter_user_id.astype(float), -np.arange(1, len(g) + 1))
            tab = pd.crosstab(g.acct, g.cls).reindex(columns=CLASSES, fill_value=0).to_numpy()
            w_ = rng.poisson(1.0, size=(B, tab.shape[0])); num = w_ @ tab; shares = num / num.sum(axis=1, keepdims=True)
            for j, c in enumerate(CLASSES):
                kc = int((f0 & (cl == c)).sum()); lo, hi = wilson(kc, k0)
                clo, chi = np.percentile(shares[:, j], [2.5, 97.5])
                accts = g.loc[g.cls == c, "acct"]
                r.update({f"share_{c}": kc / k0, f"share_{c}_lo": lo, f"share_{c}_hi": hi, f"share_{c}_clo": clo, f"share_{c}_chi": chi,
                          f"delta_excl_{c}_pp": kc / n * 100, f"n_accounts_{c}": int(accts.nunique()),
                          f"top_account_share_{c}": float(accts.value_counts().iloc[0] / max(kc, 1)) if kc else np.nan})
            mo = f0 & (cl == "manual_other"); allman = f0 & np.isin(cl, ["manual_other", "anon", "self"])
            r["undo_share_of_other_registered_manual"] = float((mo & A.undo.to_numpy()).sum() / max(mo.sum(), 1))
            r["undo_share_of_all_non_bot_non_tool"] = float((allman & A.undo.to_numpy()).sum() / max(allman.sum(), 1))
            r["delta_excl_undo_pp"] = float((allman & A.undo.to_numpy()).sum() / n * 100)
            R["comp"].append(r)
        if label == "2019+":
            f0 = boolcol(A.is_reverted_d1) & inw(A.sec_to_revert, 86400); notrev = ~f0
            variants = [("all newcomers", np.ones(n, bool))]
            if blocks is not None:
                bts = A.user_id.map(blocks)
                blocked = (bts.notna() & ((bts - A.anchor_ts).dt.total_seconds() <= 60 * 86400)).to_numpy()
                variants.append(("not blocked within 60 days", ~blocked))
                R["ret"].append(dict(wiki=wiki, variant="blocked within 60 days (share)", first_revert_class="all", n_class=int(blocked.sum()),
                                     retained_share=float(blocked.mean())))
                for c in CLASSES:
                    m = f0 & (cl == c)
                    if m.sum() >= MINCELL:
                        R["ret"].append(dict(wiki=wiki, variant="blocked within 60 days (share)", first_revert_class=c, n_class=int(m.sum()),
                                             retained_share=float(blocked[m].mean())))
                R["ret"].append(dict(wiki=wiki, variant="blocked within 60 days (share)", first_revert_class="not reverted", n_class=int(notrev.sum()),
                                     retained_share=float(blocked[notrev].mean())))
            for vname, vm in variants:
                for c in CLASSES + ["any"]:
                    x = (f0 if c == "any" else (f0 & (cl == c))) & vm; base = notrev & vm; m = x | base
                    if x.sum() < MINCELL: continue
                    o, lo, hi = woolf(x[m], ret[m]); slo, shi = wilson(int(ret[x].sum()), int(x.sum()))
                    R["ret"].append(dict(wiki=wiki, variant=vname, first_revert_class=c, n_class=int(x.sum()), retained_share=float(ret[x].mean()),
                                         share_lo=slo, share_hi=shi, retained_share_not_reverted=float(ret[base].mean()), n_not_reverted=int(base.sum()),
                                         OR_vs_not_reverted=o, lo=lo, hi=hi))
    # H4, registered nine cells and the three 24-hour cells; exact multinomial pattern bootstrap = resampling editors
    A = full_cohort(wiki, 2019); n = len(A); ret = boolcol(A.retained_2_60); cl = A.cls.to_numpy()
    cells = []
    for ws in [86400, 604800, None]:
        f0 = boolcol(A.is_reverted_d1) & inw(A.sec_to_revert, ws)
        cells += [f0, f0 & (cl != "bot"), f0 & ~np.isin(cl, ["bot", "tool"])]
    X = np.stack(cells + [ret]).astype(np.int64); code = (X * (1 << np.arange(10))[:, None]).sum(axis=0)
    pats, counts = np.unique(code, return_counts=True); bits = ((pats[:, None] >> np.arange(10)) & 1).astype(bool)
    def ratio(cnt, idx):
        ors = []
        for j in idx:
            x = bits[:, j]; r_ = bits[:, 9]
            a = cnt[x & r_].sum() + .5; b = cnt[x & ~r_].sum() + .5; c = cnt[~x & r_].sum() + .5; d = cnt[~x & ~r_].sum() + .5
            ors.append(a * d / (b * c))
        return max(ors) / min(ors)
    rng = np.random.default_rng(SEED); draws = rng.multinomial(n, counts / n, size=B)
    for name, idx in [("nine registered cells", range(9)), ("three 24-hour cells", [0, 1, 2])]:
        est = ratio(counts, idx); bs = np.array([ratio(d_, idx) for d_ in draws]); lo, hi = np.percentile(bs, [2.5, 97.5])
        R["h4"].append(dict(wiki=wiki, role=ROLE[wiki], cells=name, n=n, ratio=est, lo=lo, hi=hi, one_sided_lower_95=np.percentile(bs, 5), replicates=B))


def sample_tables(wiki, R):
    A = pd.read_parquet(os.path.join(D, f"{wiki}_decomp.parquet"))
    A = A[A.created_by_self.fillna(False).astype(bool) & (A.anchor_year >= 2019)].reset_index(drop=True); n = len(A)
    rng = np.random.default_rng(SEED); author = A.user_id.astype(float).to_numpy()
    groups = None
    gp = os.path.join(D, f"{wiki}_revgroups.tsv")
    if os.path.exists(gp):
        G = pd.read_csv(gp, sep="\t", dtype=str).drop_duplicates("revision_id")
        G["revision_id"] = G.revision_id.astype("int64"); groups = G.set_index("revision_id").event_user_groups_historical.fillna("")
    ctx = dict(wiki=wiki, n_sample=n, share_creates_page=float(boolcol(A.anchor_creates_page).mean()))
    for rule in ["d3", "d3r"]:
        fs = A[f"{rule}_first_sec"].astype(float); fu = A[f"{rule}_first_user"].astype(float).to_numpy()
        fbot = boolcol(A[f"{rule}_first_bot"]); ftool = boolcol(A[f"{rule}_first_tool"]); fanon = boolcol(A[f"{rule}_first_anon"])
        fself = (fu == author) & ~np.isnan(fu)
        cls = np.select([fs.isna().to_numpy(), fbot, ftool, fself, fanon], ["none", "bot", "tool", "self", "anon"], default="manual_other")
        auto = fbot | ftool
        # third-party follow-up: first of nt1..nt5 made neither by the author nor by the account that made the first revert
        tp_sec = np.full(n, np.nan); tp_after = np.full(n, np.nan); tp_gap = np.full(n, np.nan); tp_ra = np.zeros(n, bool); tp_rs = np.zeros(n, bool)
        any_sec = A[f"{rule}_nt1_sec"].astype(float).to_numpy()
        for k in range(1, 6):
            u = A[f"{rule}_nt{k}_user"].astype(float).to_numpy(); s = A[f"{rule}_nt{k}_sec"].astype(float).to_numpy()
            ok = ~np.isnan(s) & np.isnan(tp_sec) & ~((u == author) & ~np.isnan(u)) & ~((u == fu) & ~np.isnan(u))
            tp_sec[ok] = s[ok]; tp_after[ok] = A[f"{rule}_nt{k}_sec_after_first"].astype(float).to_numpy()[ok]
            tp_gap[ok] = A[f"{rule}_nt{k}_gap"].astype(float).to_numpy()[ok]
            tp_ra[ok] = boolcol(A[f"{rule}_nt{k}_reinst_anchor"])[ok]; tp_rs[ok] = boolcol(A[f"{rule}_nt{k}_reinst_span"])[ok]
        act = A[f"{rule}_revs_30d_after_first"].astype(float)
        terc = pd.qcut(act[fs.notna()], 3, labels=False, duplicates="drop").reindex(A.index)
        groupsets = [("bot_or_tool", auto), ("any_manual", np.isin(cls, ["manual_other", "anon"]))] + [(c, cls == c) for c in CLASSES]
        for clock, base_sec in [("from anchor", tp_sec), ("from first revert", tp_after)]:
            for wn, ws in WINS:
                f_in = inw(fs, ws) if clock == "from anchor" else fs.notna().to_numpy()
                fol = inw(base_sec, ws)
                for c, gm in groupsets:
                    m = f_in & gm; k = int(m.sum())
                    if k < MINCELL: continue
                    ff = fol & m; kf = int(ff.sum()); lo, hi = wilson(kf, k)
                    deep = (tp_gap == 0) & ~tp_rs
                    row = dict(wiki=wiki, rule=rule, clock=clock, W=wn, first_class=c, stratum="all", n_first=k, followup_third_party=kf / k, lo=lo, hi=hi,
                               after_reinstatement=int((ff & tp_ra).sum()) / k, immediate_deeper=int((ff & deep).sum()) / k,
                               after_other_edits=int((ff & ~tp_ra & ~deep).sum()) / k,
                               followup_any_account=int((inw(any_sec if clock == "from anchor" else A[f"{rule}_nt1_sec_after_first"], ws) & m).sum()) / k)
                    R["fu"].append(row)
                    if c in ("bot_or_tool", "any_manual") and wn in ("W24h", "Winf") and clock == "from first revert":
                        for t in sorted(terc.dropna().unique()):
                            mt = m & (terc == t).to_numpy(); kt = int(mt.sum())
                            if kt < MINCELL: continue
                            kft = int((fol & mt).sum()); lo, hi = wilson(kft, kt)
                            R["fu"].append(dict(wiki=wiki, rule=rule, clock=clock, W=wn, first_class=c, stratum=f"page activity tercile {int(t)+1}",
                                                n_first=kt, followup_third_party=kft / kt, lo=lo, hi=hi))
        # class of the next revert by anyone
        a2 = A[f"{rule}_any2_sec"].astype(float).notna().to_numpy(); a2bot = boolcol(A[f"{rule}_any2_bot"]); a2tool = boolcol(A[f"{rule}_any2_tool"])
        for c, gm in groupsets[:2]:
            m = fs.notna().to_numpy() & gm; k = int(m.sum())
            if k >= MINCELL:
                R["fu"].append(dict(wiki=wiki, rule=rule, clock="unbounded", W="Winf", first_class=c, stratum="next revert by anyone", n_first=k,
                                    followup_third_party=np.nan, followup_any_account=int((a2 & m).sum()) / k,
                                    next_is_bot=int((a2 & a2bot & m).sum()) / k, next_is_tool=int((a2 & a2tool & ~a2bot & m).sum()) / k,
                                    next_is_manual=int((a2 & ~a2bot & ~a2tool & m).sum()) / k))
        # window ratio R (registered replace definition: first non-bot non-tool revert of the anchor, any account)
        nt_sec = pd.Series(np.where(fs.isna(), np.nan, np.where(auto, any_sec, fs.to_numpy())))
        d = {w: (inw(fs, s).astype(np.int8) - inw(nt_sec, s).astype(np.int8)) for w, s in [("W24h", 86400), ("W180d", 15552000), ("Winf", None)]}
        n_first = {w: int(inw(fs, s).sum()) for w, s in [("W24h", 86400), ("Winf", None)]}
        for num in ["Winf", "W180d"]:
            est = d[num].mean() / d["W24h"].mean(); bs = []
            for _ in range(B):
                ix = rng.integers(0, n, n); bs.append(d[num][ix].mean() / d["W24h"][ix].mean())
            lo, hi = np.percentile(bs, [2.5, 97.5])
            R["win"].append(dict(wiki=wiki, role=ROLE[wiki], rule=rule, ratio=f"{num}/W24h", n=n, delta24_pp=d["W24h"].mean() * 100,
                                 delta_num_pp=d[num].mean() * 100, R=est, lo=lo, hi=hi,
                                 auto_first_24h=int((inw(fs, 86400) & auto).sum()), auto_first_inf=int((fs.notna().to_numpy() & auto).sum())))
        ctx[f"{rule}_p_reverted_inf"] = float(fs.notna().mean()); ctx[f"{rule}_p_reverted_24h"] = float(inw(fs, 86400).mean())
        ctx[f"{rule}_share_first_span_1"] = float((A[f"{rule}_first_span"] == 1).sum() / max(fs.notna().sum(), 1))
        if rule == "d3":
            nc = ~boolcol(A.anchor_creates_page)
            ctx["p_reverted_24h_page_creating"] = float(inw(fs, 86400)[~nc].mean()) if (~nc).sum() else np.nan
            ctx["p_reverted_24h_not_page_creating"] = float(inw(fs, 86400)[nc].mean())
        if rule == "d3r":
            g = (A.anchor_ts >= pd.Timestamp("2020-10-01", tz=A.anchor_ts.dt.tz)).to_numpy() & fs.notna().to_numpy()
            d2 = boolcol(A.is_reverted_d2); yrs = A.anchor_year.to_numpy()
            def add(label, m, **kw):
                k = int(m.sum())
                if k < MINCELL: return
                ku = int((m & ~d2).sum()); lo, hi = wilson(ku, k)
                R["tag"].append(dict(wiki=wiki, breakdown=label, n=k, untagged=ku / k, lo=lo, hi=hi, share_of_untagged=ku / max(int((g & ~d2).sum()), 1), **kw))
            for c in CLASSES + ["all"]:
                add("class", g & (np.ones(n, bool) if c == "all" else (cls == c)), reverter_class=c)
            for y in sorted(set(yrs[g].tolist())):
                add("year", g & (yrs == y), reverter_class="all", year=int(y))
                add("year", g & (yrs == y) & np.isin(cls, ["anon", "self"]), reverter_class="anon_or_self", year=int(y))
            if groups is not None:
                gh = A[f"{rule}_first_rev"].map(groups)
                known = gh.notna().to_numpy(); sets = gh.fillna("").map(lambda s: set(x for x in s.split(",") if x))
                has_ap = sets.map(lambda s: bool(s & AUTOP)).to_numpy(); nogroup = sets.map(lambda s: len(s) == 0).to_numpy()
                reg = np.isin(cls, ["manual_other", "self", "tool"])
                add("groups", g & known & reg & has_ap, reverter_class="registered", groups="autopatrol-carrying group")
                add("groups", g & known & reg & ~has_ap & ~nogroup, reverter_class="registered", groups="other group only")
                add("groups", g & known & reg & nogroup, reverter_class="registered", groups="no group")
                for c in ["manual_other", "self", "tool"]:
                    add("groups", g & known & (cls == c) & has_ap, reverter_class=c, groups="autopatrol-carrying group")
                    add("groups", g & known & (cls == c) & ~has_ap, reverter_class=c, groups="no autopatrol-carrying group")
                ctx["groups_join_rate"] = float(known[g].mean())
            # reverse cell
            allp = (A.anchor_ts >= pd.Timestamp("2020-10-01", tz=A.anchor_ts.dt.tz)).to_numpy()
            ctx["tagged_without_radius_revert_share_of_tagged"] = float((allp & d2 & fs.isna().to_numpy()).sum() / max((allp & d2).sum(), 1))
    R["ctx"].append(ctx)


def main():
    wikis = sys.argv[1:] or WIKIS
    R = {k: [] for k in ["comp", "ret", "h4", "fu", "win", "tag", "ctx"]}
    for w in wikis:
        composition(w, R)
        if os.path.exists(os.path.join(D, f"{w}_decomp.parquet")):
            sample_tables(w, R)
        print("done", w, flush=True)
    names = dict(comp="rev_composition", ret="rev_retention", h4="rev_h4_boot2000", fu="rev_followup", win="rev_window", tag="rev_taggap", ctx="rev_context")
    for k, rows in R.items():
        path = os.path.join(O, names[k] + ".csv"); new = pd.DataFrame(rows)
        if len(wikis) < len(WIKIS) and os.path.exists(path):
            old = pd.read_csv(path)
            if set(old.columns) >= {"wiki"}: new = pd.concat([old[~old.wiki.isin(wikis)], new], ignore_index=True)
        new.to_csv(path, index=False)
    print("written")


if __name__ == "__main__":
    main()
