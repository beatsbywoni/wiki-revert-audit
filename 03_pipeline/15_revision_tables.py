"""Revision tables (post-review round 1). Reads 02_derived/<wiki>_anchors.parquet (full cohort) and <wiki>_decomp.parquet (page-history sample).

Outputs (04_output/):
  rev_composition.csv   who made the first revert of newcomer first edits within 24 h / unbounded (dump flag, full cohort):
                        bot, one-click tool, self, anonymous, other manual; with the strict effect of excluding each class
                        (identity: p x class share) and bootstrap-free Wilson intervals on shares
  rev_retention.csv     retention (edit on days 2-60) by class of first revert within 24 h, odds ratio vs not reverted within 24 h,
                        Woolf interval; plus the all-reverts OR and the OR with tool-reverted anchors moved to "not reverted"
  rev_followup.csv      follow-up manual revert after the first revert, by class of first reverter, both attribution rules (sample)
  rev_window.csv        R = replace effect(unbounded or 180 d) / replace effect(24 h) by attribution rule, with 2,000-replicate bootstrap
  rev_S_by_year.csv     S(24 h) by edition and year, both rules, with bootstrap intervals (new Figure 2)
  rev_taggap.csv        share of within-radius identity reverts whose anchor has no mw-reverted tag, by class of reverter
  rev_h4_boot2000.csv   max/min retention OR ratio across the nine registered strict cells with 2,000 paired bootstrap replicates
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
CLASSES = ["bot", "tool", "self", "anon", "manual_other"]
SEED = 20261110; B = 2000


def wilson(k, n, z=1.959964):
    if n == 0: return (np.nan, np.nan)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def inw(sec, w):
    s = sec.astype(float)
    return (s.notna() & ((s <= w) if w is not None else True)).to_numpy()


def woolf(x, r):
    a = (x & r).sum() + .5; b = (x & ~r).sum() + .5; c = (~x & r).sum() + .5; d = (~x & ~r).sum() + .5
    lor = np.log(a * d / (b * c)); se = np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    return np.exp(lor), np.exp(lor - 1.96 * se), np.exp(lor + 1.96 * se)


def full_cohort(wiki, min_year=2019):
    cols = ["anchor_rank", "anchor_year", "created_by_self", "user_id", "is_reverted_d1", "sec_to_revert", "reverter_user_id", "reverter_is_anon",
            "reverter_is_bot", "reverter_is_tool", "reverter_is_undo", "retained_2_60"]
    A = pd.read_parquet(os.path.join(D, f"{wiki}_anchors.parquet"), columns=cols)
    A = A[(A.anchor_rank == 1) & (A.anchor_year >= min_year) & A.created_by_self.fillna(False).astype(bool)].reset_index(drop=True)
    rev = A.is_reverted_d1.astype(bool).to_numpy()
    bot = A.reverter_is_bot.fillna(False).astype(bool).to_numpy(); tool = A.reverter_is_tool.fillna(False).astype(bool).to_numpy()
    self_ = (A.reverter_user_id.astype(float) == A.user_id.astype(float)).fillna(False).to_numpy() & A.reverter_user_id.notna().to_numpy()
    anon = A.reverter_is_anon.fillna(False).astype(bool).to_numpy()
    cls = np.select([~rev, bot, tool, self_, anon], ["none", "bot", "tool", "self", "anon"], default="manual_other")
    A["cls"] = cls; A["undo"] = A.reverter_is_undo.fillna(False).astype(bool)
    return A


def composition(wiki, rows, rows_ret, rows_h4):
    for label, min_year in [("2019+", 2019), ("2021+", 2021)]:
        A = full_cohort(wiki, min_year); n = len(A); ret = A.retained_2_60.astype(bool).to_numpy()
        for wn, ws in [("W24h", 86400), ("Winf", None)]:
            f0 = A.is_reverted_d1.astype(bool).to_numpy() & inw(A.sec_to_revert, ws); k0 = int(f0.sum())
            r = dict(wiki=wiki, role=ROLE[wiki], cohort=label, W=wn, n=n, p_F0=k0 / n)
            for c in CLASSES:
                kc = int((f0 & (A.cls.to_numpy() == c)).sum()); lo, hi = wilson(kc, k0)
                r[f"share_{c}"] = kc / k0; r[f"share_{c}_lo"] = lo; r[f"share_{c}_hi"] = hi; r[f"delta_excl_{c}_pp"] = kc / n * 100
            ku = int((f0 & A.undo.to_numpy() & np.isin(A.cls.to_numpy(), ["manual_other", "anon", "self"])).sum())
            r["share_undo_button_among_manual"] = ku / max(int((f0 & np.isin(A.cls.to_numpy(), ["manual_other", "anon", "self"])).sum()), 1)
            r["delta_excl_undo_pp"] = ku / n * 100
            rows.append(r)
            if label == "2019+" and wn == "W24h":
                notrev = ~f0
                for c in CLASSES + ["any"]:
                    x = f0 if c == "any" else (f0 & (A.cls.to_numpy() == c))
                    m = x | notrev
                    if x.sum() < 30: continue
                    o, lo, hi = woolf(x[m], ret[m])
                    rows_ret.append(dict(wiki=wiki, first_revert_class=c, n_class=int(x.sum()), retained_share=float(ret[x].mean()),
                                         retained_share_not_reverted=float(ret[notrev].mean()), OR_vs_not_reverted=o, lo=lo, hi=hi))
                x = f0 & ~np.isin(A.cls.to_numpy(), ["bot", "tool"])
                o, lo, hi = woolf(x, ret)
                rows_ret.append(dict(wiki=wiki, first_revert_class="registered strict F2 (bot/tool-reverted moved to not reverted)", n_class=int(x.sum()),
                                     retained_share=float(ret[x].mean()), retained_share_not_reverted=float(ret[~x].mean()), OR_vs_not_reverted=o, lo=lo, hi=hi))
    # H4 with 2,000 paired bootstrap replicates (registered nine strict cells); exact multinomial bootstrap over joint patterns
    A = full_cohort(wiki, 2019); n = len(A); ret = A.retained_2_60.astype(bool).to_numpy(); cl = A.cls.to_numpy()
    cells = []
    for ws in [86400, 604800, None]:
        f0 = A.is_reverted_d1.astype(bool).to_numpy() & inw(A.sec_to_revert, ws)
        cells += [f0, f0 & (cl != "bot"), f0 & ~np.isin(cl, ["bot", "tool"])]
    X = np.stack(cells + [ret]).astype(np.int64)             # 10 x n
    code = (X * (1 << np.arange(10))[:, None]).sum(axis=0)
    pats, counts = np.unique(code, return_counts=True)
    bits = ((pats[:, None] >> np.arange(10)) & 1).astype(bool)   # patterns x 10
    def ratio(cnt):
        ors = []
        for j in range(9):
            x = bits[:, j]; r_ = bits[:, 9]
            a = cnt[x & r_].sum() + .5; b = cnt[x & ~r_].sum() + .5; c = cnt[~x & r_].sum() + .5; d = cnt[~x & ~r_].sum() + .5
            ors.append(a * d / (b * c))
        return max(ors) / min(ors)
    rng = np.random.default_rng(SEED); est = ratio(counts)
    bs = np.array([ratio(rng.multinomial(n, counts / n)) for _ in range(B)])
    lo, hi = np.percentile(bs, [2.5, 97.5])
    rows_h4.append(dict(wiki=wiki, role=ROLE[wiki], n=n, ratio=est, lo=lo, hi=hi, one_sided_lower_95=np.percentile(bs, 5), replicates=B))


def sample_tables(wiki, rows_fu, rows_win, rows_sy, rows_tag):
    A = pd.read_parquet(os.path.join(D, f"{wiki}_decomp.parquet"))
    A = A[A.created_by_self.fillna(False).astype(bool) & (A.anchor_year >= 2019)].reset_index(drop=True); n = len(A)
    rng = np.random.default_rng(SEED)
    for rule in ["d3", "d3r"]:
        fs = A[f"{rule}_first_sec"]; fbot = A[f"{rule}_first_bot"].fillna(False).astype(bool).to_numpy(); ftool = A[f"{rule}_first_tool"].fillna(False).astype(bool).to_numpy()
        fself = A[f"{rule}_first_self"].fillna(False).astype(bool).to_numpy(); fanon = A[f"{rule}_first_anon"].fillna(False).astype(bool).to_numpy()
        cls = np.select([fs.isna().to_numpy(), fbot, ftool, fself, fanon], ["none", "bot", "tool", "self", "anon"], default="manual_other")
        auto = fbot | ftool
        nt_sec = pd.Series(np.where(fs.isna(), np.nan, np.where(auto, A[f"{rule}_ntaf_sec"].astype(float), fs.astype(float))))
        # follow-up manual revert by class
        for wn, ws in [("W24h", 86400), ("W7d", 604800), ("W180d", 15552000), ("Winf", None)]:
            f_in = inw(fs, ws); fol = inw(A[f"{rule}_ntaf_sec"], ws)
            for c in CLASSES + ["bot_or_tool", "any_manual"]:
                m = f_in & (auto if c == "bot_or_tool" else np.isin(cls, ["manual_other", "anon"]) if c == "any_manual" else (cls == c))
                k = int(m.sum())
                if k == 0: continue
                kf = int((fol & m).sum()); lo, hi = wilson(kf, k)
                ra = A[f"{rule}_ntaf_reinst_anchor"].fillna(False).astype(bool).to_numpy(); gap = A[f"{rule}_ntaf_gap"].to_numpy()
                rs_ = A[f"{rule}_ntaf_reinst_span"].fillna(False).astype(bool).to_numpy()
                ff = fol & m
                rows_fu.append(dict(wiki=wiki, rule=rule, W=wn, first_class=c, n_first=k, followup=kf / k, lo=lo, hi=hi,
                                    followup_after_reinstatement=int((ff & ra).sum()) / k,
                                    followup_immediate_deeper=int((ff & (gap == 0) & ~rs_).sum()) / k,
                                    followup_other=int((ff & ~ra & ~((gap == 0) & ~rs_)).sum()) / k))
        # window ratio R with 2,000 replicates
        r0 = {w: inw(fs, s) for w, s in [("W24h", 86400), ("W180d", 15552000), ("Winf", None)]}
        r2 = {w: inw(nt_sec, s) for w, s in [("W24h", 86400), ("W180d", 15552000), ("Winf", None)]}
        d = {w: (r0[w].astype(np.int8) - r2[w].astype(np.int8)) for w in r0}
        for num in ["Winf", "W180d"]:
            est = d[num].mean() / d["W24h"].mean()
            bs = []
            for _ in range(B):
                ix = rng.integers(0, n, n); bs.append(d[num][ix].mean() / d["W24h"][ix].mean())
            lo, hi = np.percentile(bs, [2.5, 97.5])
            rows_win.append(dict(wiki=wiki, role=ROLE[wiki], rule=rule, ratio=f"{num}/W24h", n=n, delta24_pp=d["W24h"].mean() * 100, delta_num_pp=d[num].mean() * 100,
                                 R=est, lo=lo, hi=hi, D_pp=(d["W24h"].mean() - d[num].mean()) * 100,
                                 D_lo=np.percentile([(d["W24h"][ix_].mean() - d[num][ix_].mean()) * 100 for ix_ in (rng.integers(0, n, n) for _ in range(500))], 2.5)))
        # S by year
        yrs = A.anchor_year.to_numpy()
        for y in sorted(set(yrs.tolist())) + ["all"]:
            m = np.ones(n, bool) if y == "all" else (yrs == y)
            f_in = inw(fs, 86400) & m; k = int((f_in & auto).sum())
            if k < 30: continue
            kf = int((f_in & auto & inw(A[f"{rule}_ntaf_sec"], 86400)).sum()); lo, hi = wilson(kf, k)
            km = int((f_in & np.isin(cls, ["manual_other", "anon"])).sum())
            kmf = int((f_in & np.isin(cls, ["manual_other", "anon"]) & inw(A[f"{rule}_ntaf_sec"], 86400)).sum()); lom, him = wilson(kmf, km)
            rows_sy.append(dict(wiki=wiki, rule=rule, year=y, n_anchors=int(m.sum()), n_auto_first=k, S=kf / k, lo=lo, hi=hi,
                                share_auto=k / max(int(f_in.sum()), 1), n_manual_first=km, followup_manual_first=kmf / max(km, 1), m_lo=lom, m_hi=him))
        if rule == "d3r":
            g = (A.anchor_ts >= pd.Timestamp("2020-10-01", tz=A.anchor_ts.dt.tz)).to_numpy() & fs.notna().to_numpy()
            d2 = A.is_reverted_d2.fillna(False).astype(bool).to_numpy()
            for c in CLASSES + ["all"]:
                m = g & (np.ones(n, bool) if c == "all" else (cls == c)); k = int(m.sum())
                if k == 0: continue
                ku = int((m & ~d2).sum()); lo, hi = wilson(ku, k)
                rows_tag.append(dict(wiki=wiki, reverter_class=c, n=k, untagged=ku / k, lo=lo, hi=hi, share_of_untagged=ku / max(int((g & ~d2).sum()), 1)))


def main():
    wikis = sys.argv[1:] or WIKIS
    R = {k: [] for k in ["comp", "ret", "h4", "fu", "win", "sy", "tag"]}
    for w in wikis:
        composition(w, R["comp"], R["ret"], R["h4"])
        if os.path.exists(os.path.join(D, f"{w}_decomp.parquet")):
            sample_tables(w, R["fu"], R["win"], R["sy"], R["tag"])
        print("done", w, flush=True)
    names = dict(comp="rev_composition", ret="rev_retention", h4="rev_h4_boot2000", fu="rev_followup", win="rev_window", sy="rev_S_by_year", tag="rev_taggap")
    for k, rows in R.items():
        path = os.path.join(O, names[k] + ".csv"); new = pd.DataFrame(rows)
        if len(wikis) < len(WIKIS) and os.path.exists(path):
            old = pd.read_csv(path); new = pd.concat([old[~old.wiki.isin(wikis)], new], ignore_index=True)
        new.to_csv(path, index=False)
    print("written")


if __name__ == "__main__":
    main()
