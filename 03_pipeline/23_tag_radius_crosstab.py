"""Tag rule against radius rule, cell by cell (round 6; exploratory).

For first edits of self-created accounts from October 2020 (page-history samples) the script reports, per edition and per period,
  the two-by-two table of the mw-reverted tag on the measured edit by the 15-revision radius rule;
  the tag-only cell split by the dump's own identity-revert flag (computed by Wikimedia on the complete page history) and,
    where the dump names a reverting revision, by the revert tags that revision carries;
  for English, how often the dump's flag (complete history) and the recomputation (history loaded from 2018) disagree,
    which bounds what the truncated history can hide from the radius rule;
  the share of radius-rule reverts without the tag by period and class of first reverter;
  the decomposition of the change in the gap to English between the two rules into its four cells.
Outputs: 04_output/rev_tag_radius_crosstab.csv, 04_output/rev_taggap_period.csv, 04_output/rev_tag_only_tags.csv, 04_output/rev_example_decomposition.csv
"""
import os
import warnings
import numpy as np, pandas as pd
warnings.simplefilter("ignore", FutureWarning)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "02_derived"); OUT = os.path.join(ROOT, "04_output")
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]
PERIODS = {"from 2020-10": ("2020-10-01", "2100-01-01"), "2020-10 to 2024-12": ("2020-10-01", "2025-01-01"), "from 2025-01": ("2025-01-01", "2100-01-01")}
COLS = ["user_id", "d3r_first_user", "d3r_first_anon", "d3r_first_bot", "d3r_first_tool", "created_by_self", "anchor_ts", "is_reverted_d1", "is_reverted_d2", "reverting_rev_id", "d3_first_sec", "d3r_first_sec", "page_revs_before", "anchor_creates_page"]


def b(s): return s.fillna(False).astype(bool)


def main():
    cross, tags, dec, gap = [], [], [], []
    cells = {}
    for w in WIKIS:
        A = pd.read_parquet(os.path.join(D, f"{w}_decomp.parquet"), columns=COLS)
        A = A[b(A.created_by_self)].copy()
        A["tag"] = b(A.is_reverted_d2); A["rad"] = A.d3r_first_sec.notna(); A["dumpflag"] = b(A.is_reverted_d1); A["recomp"] = A.d3_first_sec.notna()
        G = pd.read_csv(os.path.join(D, f"{w}_revgroups.tsv"), sep="\t", usecols=["revision_id", "revision_tags"], dtype={"revision_tags": str})
        G = G.drop_duplicates("revision_id").set_index("revision_id").revision_tags.fillna("")
        tz = A.anchor_ts.dt.tz
        for pname, (lo, hi) in PERIODS.items():
            S = A[(A.anchor_ts >= pd.Timestamp(lo, tz=tz)) & (A.anchor_ts < pd.Timestamp(hi, tz=tz))]
            n = len(S); t, r, f, c = S.tag.to_numpy(), S.rad.to_numpy(), S.dumpflag.to_numpy(), S.recomp.to_numpy()
            to = t & ~r; ro = ~t & r
            row = dict(wiki=w, period=pname, n=n, both=int((t & r).sum()), tag_only=int(to.sum()), radius_only=int(ro.sum()), neither=int((~t & ~r).sum()),
                       p_tag=t.mean(), p_radius=r.mean(), tag_only_pp=to.mean() * 100, radius_only_pp=ro.mean() * 100,
                       tag_only_dumpflag_yes=int((to & f).sum()), tag_only_dumpflag_no=int((to & ~f).sum()),
                       tag_only_dumpflag_yes_recomputed_no=int((to & f & ~c).sum()),
                       dumpflag_yes_recomputed_no=int((f & ~c).sum()), dumpflag_no_recomputed_yes=int((~f & c).sum()),
                       dumpflag_yes_radius_no=int((f & ~r).sum()))
            cross.append(row); cells[(w, pname)] = row
            R = S[r]; anon = b(R.d3r_first_anon).to_numpy(); selfr = (R.d3r_first_user == R.user_id).to_numpy() & ~anon
            bot = b(R.d3r_first_bot).to_numpy(); tool = b(R.d3r_first_tool).to_numpy() & ~bot
            cls = np.where(bot, "bot", np.where(tool, "tool", np.where(selfr, "self", np.where(anon, "unregistered", "other manual"))))
            for k in ["all", "bot", "tool", "other manual", "unregistered", "self"]:
                m = np.ones(len(R), bool) if k == "all" else cls == k
                gap.append(dict(wiki=w, period=pname, reverter=k, radius_reverts=int(m.sum()), share_of_radius_reverts=m.mean() if len(R) else np.nan,
                                untagged=int((m & ~R.tag.to_numpy()).sum()), untagged_share=(~R.tag.to_numpy())[m].mean() if m.sum() >= 50 else np.nan))
            if pname == "from 2020-10":
                T = S[to & f & S.reverting_rev_id.notna().to_numpy()]
                tg = T.reverting_rev_id.astype("int64").map(G)
                found = tg.notna(); tg = tg.fillna("")
                tags.append(dict(wiki=w, tag_only=int(to.sum()), dump_names_reverting_revision=int(len(T)), reverting_revision_found=int(found.sum()),
                                 undo=int(tg.str.contains("mw-undo").sum()), rollback=int(tg.str.contains("mw-rollback").sum()),
                                 manual_revert=int(tg.str.contains("mw-manual-revert").sum()),
                                 none_of_three=int((found & ~tg.str.contains("mw-undo|mw-rollback|mw-manual-revert")).sum())))
        print("done", w, flush=True)
    for pname in PERIODS:
        e = cells[("enwiki", pname)]
        for w in WIKIS[1:]:
            x = cells[(w, pname)]
            dec.append(dict(wiki=w, period=pname, gap_tag_pp=(e["p_tag"] - x["p_tag"]) * 100, gap_radius_pp=(e["p_radius"] - x["p_radius"]) * 100,
                            change_pp=((e["p_tag"] - x["p_tag"]) - (e["p_radius"] - x["p_radius"])) * 100,
                            english_tag_only_pp=e["tag_only_pp"], english_radius_only_pp=-e["radius_only_pp"],
                            other_radius_only_pp=x["radius_only_pp"], other_tag_only_pp=-x["tag_only_pp"]))
    pd.DataFrame(cross).to_csv(os.path.join(OUT, "rev_tag_radius_crosstab.csv"), index=False)
    pd.DataFrame(gap).to_csv(os.path.join(OUT, "rev_taggap_period.csv"), index=False)
    pd.DataFrame(tags).to_csv(os.path.join(OUT, "rev_tag_only_tags.csv"), index=False)
    pd.DataFrame(dec).to_csv(os.path.join(OUT, "rev_example_decomposition.csv"), index=False)


if __name__ == "__main__":
    main()
