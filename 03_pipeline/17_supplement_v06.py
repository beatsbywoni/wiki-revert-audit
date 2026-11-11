"""Supplementary Material for manuscript v0.6, generated from released aggregates in 04_output/.

Output: 05_manuscript/supplement_v0.6.md. Cells with fewer than 50 edits are not shown (registered minimum cell size).
"""
import os, re
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(ROOT, "04_output"); M = os.path.join(ROOT, "05_manuscript")
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]
NAME = {"enwiki": "English", "itwiki": "Italian*", "kowiki": "Korean", "dewiki": "German", "plwiki": "Polish*", "frwiki": "French", "jawiki": "Japanese*"}
WL = {"W24h": "24 h", "W7d": "7 d", "W180d": "180 d", "Winf": "unbounded", "W12h": "12 h", "W48h": "48 h", "W30d": "30 d"}
CL = {"bot": "Bot", "tool": "One-click tool", "manual_other": "Other registered, manual", "anon": "Unregistered", "self": "Self",
      "bot_or_tool": "Bot or one-click tool", "any_manual": "Manual, not the author", "any": "Any revert", "all": "All reverters", "not reverted": "Not reverted"}
MIN = 50


def rd(name): return pd.read_csv(os.path.join(O, name))


def piv(df, index, values, fmt=".3f", order=None):
    p = df.pivot_table(index=index, columns="wiki", values=values, aggfunc="first").reindex(columns=WIKIS)
    p.columns = [NAME[c] for c in p.columns]
    if order: p = p.loc[[o for o in order if o in p.index]]
    return p.fillna("").to_markdown(floatfmt=fmt) if fmt == "" else p.to_markdown(floatfmt=fmt).replace(" nan ", "     ")


S1 = """## S1. Registration, sequence of events and deviations

The registered document (Zenodo, https://doi.org/10.5281/zenodo.23720117; commit 7fcff3d, 28 October 2026, 04:39 UTC) fixed the cohort, the three attribution rules, the reverter filters, the windows, four hypotheses with thresholds, and the code. The sequence was as follows.

1. English, Korean, French and German were analyzed without restriction. The thresholds of H1 to H4 were chosen from these four editions.
2. A batch driver downloaded and processed Japanese, Polish and Italian on 27 and 28 October 2026. The driver wrote its output files to disk and printed progress lines; the summary lines for H1 and H2 were among the lines printed to the terminal log. I did not open the output files or read those lines before the registered commit. This is recorded in the work log and by file and commit timestamps, and it cannot be verified by a reader.
3. The registration was committed and deposited. The results for the held-out editions were committed 11 minutes later, which reflects that they had already been computed.
4. Section 1 of the registered text says that the held-out editions "had not been downloaded". That sentence is wrong (deviation 4 below); the header of the same document states the actual sequence.

The registration is therefore a hold-out replication with thresholds fixed in advance on other editions. It protects against choosing thresholds after seeing the held-out results only to the extent that the reader accepts step 2.

Decisions. H1, H2 and H4 are tested with one-sided 95 percent bootstrap bounds (editors resampled), Holm-adjusted over the three tests within an edition. With three tests the Holm procedure compares the smallest p value with .05/3, the next with .05/2 and the largest with .05. All supported decisions in Table S7 have bootstrap p values below .0005 (no replicate on the wrong side of the threshold in 2,000), so the adjustment changes none; the one unsupported decision (H4, Polish) is unsupported without adjustment. H3 is a descriptive criterion without a test.

Deviations (full log: `04_logs/DEVIATION_LOG.md` in the repository).

| # | Registered | Done | Effect |
|---|---|---|---|
| 1 | Mixed model as an exploratory complement | Not reported; a per-edition logistic model was run and withdrawn as uninformative | None |
| 2 | Robustness list (12 h, 48 h, 30 d windows; five anchors; all registered accounts; historical-only bot flag; undo as a tool; 5-second latency; leave-one-edition-out; by year; Korean former anchor definition) | All run; reported in Table S8. Added: 180-day window, current-only bot flag, exclusion of unregistered reverters, cohort from 2021, Korean surge split | None |
| 3 | H3, second clause | Rejected in all three editions and reported as rejected; mechanism examined afterwards (exploratory) | Decision unchanged |
| 4 | Text: held-out editions "had not been downloaded" | They had been downloaded and processed; outputs unopened (see above) | Weakens the evidential status of the tests |
| 5 | 2,000 bootstrap replicates | Registered code used 2,000 for H1 and H2, 500 for H4; H4 recomputed with 2,000 | No decision changes |
| 6 | Negative control; simulation | Withdrawn: the control cannot fail and the simulation restates a closed form. Outputs remain in the repository | None |
| 7 | Interpretation of H2 as human substitution for automation | Withdrawn. Follow-up reverts redefined as reverts by a third party; radius rule, reverter classes, retention by class added (exploratory) | Decisions unchanged; interpretation changed |
| 8 | Tag analyses for first edits from August 2020 | Coverage analyses restricted to first edits from October 2020 (tag enabled on all wikis 15 September 2020); H3 reported with the registered window | First clause unaffected. Second clause: rejected in all three editions with the registered window; with the October window it would be met in Japanese (Table S10) |
| 9 | "Successor filters" F0, F1, F2 | Reverter classes; tool exclusion presented as hypothetical | None |
| 10 | Release of editor-level derived data with randomized identifiers | Not released: one first edit per editor with its timestamp and edition re-identifies the account from the public history whatever the identifier. Code regenerates the files | Reduces direct reusability; aggregates and code are public |
| 11 | Minimum cell size 50 | Applied in all tables of manuscript v0.6; an earlier public draft showed some smaller cells | None |
| 12 | Holm adjustment "across H1 to H4" | Applied over H1, H2 and H4; H3 has no test statistic. H1: all three R values are at or above the registered .75, read as registered ("most of the filter effect persists"). H4: registered as a point ratio of at least 1.5 with a lower bound above 1.0; reported so | None |
| 13 | Model used for coding assistance | The review coding by a language model and its checks are described in the manuscript; an internal pre-submission check of drafts by language-model reviewers led to several of the changes above and is recorded in the work log | None |
"""


def main():
    L = ["# Supplementary Material", "",
         "Which reverts count? Reverter populations, attribution rules and observation windows behind a Wikipedia indicator of information quality work", "",
         "Tables are generated by `03_pipeline/17_supplement_v06.py` from the aggregates in `04_output/` of the public repository. Editions marked * were held out "
         "for the registered tests. Dump rule: the history dumps' unbounded identity-revert rule. Radius rule: the same hashes with the 15-revision radius of the mwreverts library. "
         "Except for Table S7 and the registered rows of Table S8, all analyses are exploratory. Cells with fewer than 50 edits are not shown.", "", S1, ""]

    R = rd("practice_review.csv"); R = R[R.in_tallies == "yes"]
    keep = ["short_cite", "venue", "editions", "construct", "detection", "radius_or_rule", "bot_reverts", "tool_reverts", "self_reverts", "window", "sensitivity_over_revert_choices", "source"]
    R2 = R[keep].copy(); R2["construct"] = R2.construct.map({"Q": "quality judgment", "C": "conflict", "R": "rejection", "E": "effort", "O": "other"})
    L += ["## Table S1. Structured review of practice: how 41 studies using a revert-based measure operationalize it", "",
          "One row per study. \"Not stated\" means that no sentence establishing the choice was found in the article or its supplement. The full table with the establishing "
          "sentences, URLs, evidence levels, the corrections made on re-verification and the second-pass codes is `04_output/practice_review.csv` and the files beside it. "
          "Search record: `04_output/practice_review_LIS_search.md`.", "",
          "**Flow of studies.** Stage 1 (citation networks of the methodological works and keyword searches; the number of records screened was not logged): 36 eligible studies, of which 34 were coded and tallied and 2 are listed but not tallied because the full text could not be read. "
          "Stage 2 (OpenAlex, information science and neighboring journals): 911 records from six queries and 258 from a title search (1,169 in all); 79 assessed for eligibility; 40 not assessable because the full text was not accessible; "
          "8 eligible, of which 7 were coded and tallied and 1 (an earlier conference report of the same sample as Stvilia et al., 2007) is listed but not tallied. Total tallied: 41.", "",
          "**Coding procedure.** First-pass and re-check coding were done with Claude (Anthropic; model versions and dates in `04_logs/AI_ASSISTANCE_LOG.md`), instructed to code a choice as stated only on finding an establishing passage and to record that passage. "
          "The `notes` and `evidence_level` columns record, per study, where a code rests on an extracted passage or an earlier extract and not on a re-read of the full text. No human second coder was used.", "", R2.to_markdown(index=False), "",
          "**Checklist items 1 to 4 (Table 5 of the article) applied to the reviewed studies.** Item 1 (construct) could be assigned by the coder for all studies but is seldom named by the study itself; "
          f"item 2 (attribution rule) is stated in {int((R.detection != 'not stated').sum())} of 41; item 3 (window) in {int((R.window != 'not stated').sum())}; "
          f"item 4 (bots, tools and self-reverts, all three) in {int(((R.bot_reverts != 'not stated') & (R.tool_reverts != 'not stated') & (R.self_reverts != 'not stated')).sum())}, "
          f"at least one of the three in {int(((R.bot_reverts != 'not stated') | (R.tool_reverts != 'not stated') | (R.self_reverts != 'not stated')).sum())}.", "",
          "**References for Table S1**", ""] + [re.sub(r"\s*\[[^\]]*\]\s*$", "", str(x)).strip() + "\n" for x in sorted(R.apa_reference.dropna())]

    c = rd("rev_composition.csv"); ctx = rd("rev_context.csv").set_index("wiki").loc[WIKIS]
    L += ["## Table S2. Composition of first reverts of newcomer first edits (dump rule, full cohorts)", ""]
    for coh in ["2019+", "2021+"]:
        for w in ["W24h", "Winf"]:
            g = c[(c.cohort == coh) & (c.W == w)].set_index("wiki").loc[WIKIS]
            t = pd.DataFrame({"Edition": [NAME[x] for x in g.index], "First edits": g.n.map("{:,}".format).values, "p reverted": g.p_F0.round(3).values})
            for k in ["bot", "tool", "manual_other", "anon", "self"]:
                t[CL[k]] = [f"{a:.3f} [{b:.3f}, {d:.3f}]" for a, b, d in zip(g[f"share_{k}"], g[f"share_{k}_clo"], g[f"share_{k}_chi"])]
            L += [f"**First edits {coh.replace('+', ' onward')}, window {WL[w]}.** Shares of first reverts; intervals are 95 percent percentile intervals from 2,000 bootstrap resamples of reverting accounts "
                  "(each revert by an unregistered editor counted as its own account).", "", t.to_markdown(index=False), ""]
    g = c[(c.cohort == "2019+") & (c.W == "W24h")].set_index("wiki").loc[WIKIS]
    t = pd.DataFrame({"Edition": [NAME[x] for x in g.index]})
    for k in ["bot", "tool", "manual_other"]:
        t[f"{CL[k]}: accounts"] = g[f"n_accounts_{k}"].map("{:,.0f}".format).values; t[f"{CL[k]}: share of the most active account"] = g[f"top_account_share_{k}"].round(3).values
    L += ["**Concentration of reverting, first edits 2019 onward, 24 hours.**", "", t.to_markdown(index=False), "",
          "**First edits that create a page (page-history samples).** Such edits cannot be identity-reverted; removal is by deletion, which is outside the indicator. "
          "English restricts article creation to autoconfirmed accounts.", "",
          pd.DataFrame({"Edition": [NAME[x] for x in ctx.index], "Share of first edits that create a page": ctx.share_creates_page.round(3).values,
                        "p reverted within 24 h, all": ctx.d3_p_reverted_24h.round(3).values, "p reverted within 24 h, edits to existing pages": ctx.p_reverted_24h_not_page_creating.round(3).values,
                        "First reverts that undo one revision only": ctx.d3_share_first_span_1.round(3).values}).to_markdown(index=False), ""]

    L += ["## Table S3. Change in the revert rate when a class of first reverts is recoded as not reverted, and what the tool class can see", "",
          "Percentage points; by identity, the class's share of first reverts times the rate.", ""]
    for coh in ["2019+", "2021+"]:
        g = c[(c.cohort == coh) & (c.W == "W24h")].set_index("wiki").loc[WIKIS]
        t = pd.DataFrame({"Edition": [NAME[x] for x in g.index]})
        for k, lab in [("bot", "Bots"), ("tool", "One-click tools"), ("self", "Self-reverts"), ("anon", "Unregistered reverters"), ("undo", "Undo-button reverts (if counted as a tool)")]:
            t[lab] = g[f"delta_excl_{k}_pp"].round(2).values
        t["Undo share of manual reverts by other registered editors"] = g.undo_share_of_other_registered_manual.round(3).values
        L += [f"**First edits {coh.replace('+', ' onward')}, 24-hour window.**", "", t.to_markdown(index=False), ""]
    tw = rd("rev_toolwide.csv"); tw["Edition"] = tw.wiki.map(NAME)
    tw = tw.set_index("wiki").loc[WIKIS].reset_index()
    L += ["**Wider tool tags.** Share of first reverts within 24 hours carrying a tag of RedWarn, Ultraviolet, AntiVandal script, STiki, LiveRC or MassRollback but outside the tool class used in the article "
          "(rollback, Huggle, Twinkle). Adding them would raise the tool share by the amount shown.", "",
          tw[["Edition", "cohort", "n_first_reverts_24h", "share_tool_registered", "share_wide_tag_outside_tool_class"]].rename(columns={"cohort": "First edits", "n_first_reverts_24h": "First reverts within 24 h",
              "share_tool_registered": "Tool class as used", "share_wide_tag_outside_tool_class": "Wider tags, outside the tool class"}).to_markdown(index=False, floatfmt=".3f"), ""]
    tt = rd("rev_tooltags.csv"); tt["Edition"] = tt.wiki.map(NAME)
    L += ["**Tool-related change tags on reverting revisions in the article namespace, whole period, by edition** (tags matching rollback, Huggle, Twinkle, RedWarn, Ultraviolet, STiki, AntiVandal, SWViewer, LiveRC and similar names; "
          "tags not listed for an edition do not occur there).", "",
          tt[["Edition", "tag", "reverting_revisions"]].rename(columns={"tag": "Tag", "reverting_revisions": "Reverting revisions"}).to_markdown(index=False, floatfmt=",.0f"), ""]

    f = rd("rev_followup.csv"); w = rd("rev_window.csv")
    f = f[f.n_first >= MIN]
    L += ["## Table S4. Follow-up manual reverts by a third party, and the window ratio R, under two attribution rules (page-history samples)", "",
          "Share of first edits first reverted by the class shown that were later reverted manually (no bot flag, no tool tag) by a registered account that is neither the author nor the account that made the first revert. "
          "The window is counted from the first revert. Unregistered follow-up reverters are not counted, because they cannot be compared with the first reverter; tables that count them are marked.", ""]
    order = [CL[k] for k in ["bot_or_tool", "any_manual", "bot", "tool", "manual_other", "anon", "self"]]
    for rule, rn in [("d3", "Dump rule"), ("d3r", "Radius rule")]:
        for wn in ["W24h", "W7d", "Winf"]:
            g = f[(f.rule == rule) & (f.W == wn) & (f.clock == "from first revert") & (f.stratum == "all")]
            L += [f"**{rn}, {WL[wn]}.**", "", piv(g.assign(first_class=g.first_class.map(CL)), "first_class", "followup_registered_third_party", order=order), ""]
        g = f[(f.rule == rule) & (f.W == "Winf") & (f.clock == "from first revert") & (f.stratum == "all") & f.first_class.isin(["bot_or_tool", "any_manual"])]
        for col, lab in [("after_reinstatement", "after the first edit's content had been reinstated"), ("immediate_deeper", "immediately, restoring a still earlier state"),
                         ("after_other_edits", "after other intervening edits")]:
            L += [f"**{rn}, unbounded: follow-up by any third party, registered or not, {lab}** (share of first edits first reverted by the class).", "",
                  piv(g.assign(first_class=g.first_class.map(CL)), "first_class", col), ""]
    for rule, rn in [("d3", "Dump rule"), ("d3r", "Radius rule")]:
        g = f[(f.rule == rule) & (f.clock == "from first revert") & f.stratum.str.startswith("prior revisions") & f.first_class.isin(["bot_or_tool", "manual_other"]) & (f.W == "W24h")]
        g = g.assign(key=g.stratum.map({"prior revisions under 50": "1. under 50", "prior revisions 50 to 499": "2. 50 to 499", "prior revisions 500 or more": "3. 500 or more"}) + ", " + g.first_class.map(CL))
        L += [f"**{rn}, 24 hours, by the number of revisions on the page before the measured edit** (fixed before the first revert).", "", piv(g, "key", "followup_registered_third_party"), ""]
    g = f[(f.rule == "d3") & (f.clock == "from anchor") & (f.stratum == "all") & (f.W == "W24h")]
    L += ["**Dump rule, 24 hours counted from the measured edit** (the registered clock; follow-up by any third party, registered or not).", "", piv(g.assign(first_class=g.first_class.map(CL)), "first_class", "followup_third_party", order=order), ""]
    t = w.assign(R_ci=[f"{r:.3f} [{a:.3f}, {b:.3f}]" for r, a, b in zip(w.R, w.lo, w.hi)])
    t["key"] = t.rule.map({"d3": "Dump rule", "d3r": "Radius rule"}) + ", " + t.ratio.map({"Winf/W24h": "unbounded / 24 h", "W180d/W24h": "180 d / 24 h"})
    L += ["**Window ratio R** (replace effect of excluding bots and tools at the longer window divided by the effect within 24 hours; 2,000 bootstrap resamples of editors). "
          "With N(W) the number of first edits first reverted by a bot or tool within W and S(W) the share of them with a later non-bot, non-tool revert within W, the replace effect is N(W)(1 − S(W))/n, "
          "so R = N(∞)(1 − S(∞)) / [N(24 h)(1 − S(24 h))]. R falls below 1 when follow-up accumulates faster than first reverts by bots and tools, and rises above 1 when it does not.", "",
          piv(t, "key", "R_ci", fmt=""), ""]

    r = rd("rev_retention.csv"); r = r[(r.n_class >= MIN)]
    for var, lab in [("all newcomers", "All newcomers"), ("not blocked within 60 days", "Newcomers not blocked within 60 days of the first edit")]:
        g = r[r.variant == var].copy()
        g["cell"] = [f"{s:.3f}; OR {o:.2f} [{a:.2f}, {b:.2f}]; n = {n:,.0f}" for s, o, a, b, n in zip(g.retained_share, g.OR_vs_not_reverted, g.lo, g.hi, g.n_class)]
        if var == "all newcomers":
            L += ["## Table S5. Retention (an edit on days 2 to 60) by who made the first revert within 24 hours", "",
                  "Cells: share retained; odds ratio against newcomers not reverted within 24 hours with 95 percent interval; number of newcomers.", ""]
        L += [f"**{lab}.**", "", piv(g.assign(first_revert_class=g.first_revert_class.map(CL)), "first_revert_class", "cell", fmt="", order=[CL[k] for k in ["any", "bot", "tool", "manual_other", "anon", "self"]]), "",
              "Share retained among newcomers not reverted within 24 hours: " + "; ".join(f"{NAME[k]} {v:.3f}" for k, v in g.groupby("wiki").retained_share_not_reverted.first().reindex(WIKIS).items()) + ".", ""]
    g = r[r.variant.str.startswith("blocked")]
    L += ["**Share of newcomers blocked within 60 days of the first edit, by class of first revert within 24 hours.**", "",
          piv(g.assign(first_revert_class=g.first_revert_class.map(CL)), "first_revert_class", "retained_share", order=[CL[k] for k in ["all", "not reverted", "bot", "tool", "manual_other", "anon", "self"]]).replace("All reverters", "All newcomers"), ""]

    t = rd("rev_taggap.csv"); t = t[t.n >= MIN].copy()
    t["cell"] = [f"{u:.3f} [{a:.3f}, {b:.3f}]; n = {n:,}" for u, a, b, n in zip(t.untagged, t.lo, t.hi, t.n)]
    g = t[t.breakdown == "class"]
    L += ["## Table S6. Tag coverage: radius-rule reverts whose reverted first edit carries no `mw-reverted` tag, first edits from October 2020 (page-history samples)", "",
          "Patrolling regime: English, Korean, Japanese none; German, Polish FlaggedRevs; Italian, French recent-changes patrolling. Cells: untagged share with 95 percent Wilson interval; number of reverts.", "",
          "**By class of reverter.**", "",
          piv(g.assign(reverter_class=g.reverter_class.map(CL)), "reverter_class", "cell", fmt="", order=[CL[k] for k in ["all", "bot", "tool", "manual_other", "anon", "self"]]), ""]
    g = t[(t.breakdown == "groups") & (t.reverter_class == "registered")]
    L += ["**Registered reverters (tool, other manual and self), by the user groups the reverting account held at the time of the revert** (`event_user_groups_historical`). "
          "Autopatrol-carrying groups: autopatrolled, autoreviewer, sysop, bot, rollbacker, patroller, editor, reviewer and other administrative groups. Implicit groups such as autoconfirmed are not recorded in this field.", "",
          piv(g, "groups", "cell", fmt="", order=["autopatrol-carrying group", "other group only", "no group"]), ""]
    e = rd("rev_taggap_editcount.csv"); e["cell"] = [f"{u:.3f} [{a:.3f}, {b:.3f}]; n = {n:,}" for u, a, b, n in zip(e.untagged, e.lo, e.hi, e.n)]
    L += ["**Registered manual reverters other than the author with no explicit group, by the account's edit count at the time of the revert.** "
          "On the French edition the autopatrolled status is granted automatically with experience and is not recorded as an explicit group.", "",
          piv(e, "reverter_edit_count", "cell", fmt="", order=["under 50", "50 to 499", "500 to 4,999", "5,000 or more"]), ""]
    g = t[(t.breakdown == "year") & (t.reverter_class == "all")]
    L += ["**All reverters, by year of the first edit.**", "", piv(g.assign(year=g.year.astype(int)), "year", "untagged"), ""]

    ex = rd("rev_example_tag_vs_hash.csv").set_index("wiki").loc[WIKIS]
    L += ["**Worked example: one cross-edition comparison computed with the tag and with the radius rule** (first edits from October 2020; share of first edits counted as reverted; "
          "gap to English in percentage points; odds ratio of retention for reverted against non-reverted newcomers).", "",
          pd.DataFrame({"Edition": [NAME[x] for x in ex.index], "n": ex.n.map("{:,}".format).values, "Reverted, tag": ex.p_tag.round(3).values, "Reverted, radius rule": ex.p_radius.round(3).values,
                        "Gap to English, tag": ex.gap_to_english_tag_pp.round(1).values, "Gap to English, radius rule": ex.gap_to_english_radius_pp.round(1).values,
                        "Change in gap [95% interval]": ["" if pd.isna(a) else f"{a:.1f} [{b:.1f}, {c:.1f}]" for a, b, c in zip(ex.gap_change_pp, ex.gap_change_lo, ex.gap_change_hi)],
                        "OR retention, tag": ex.OR_retention_tag.round(2).values, "OR retention, radius rule": ex.OR_retention_radius.round(2).values}).to_markdown(index=False), ""]

    h = rd("rev_h4_boot2000.csv")
    rows = [rd(f"{wk}_confirmatory.csv").assign(edition=NAME[wk]) for wk in ["jawiki", "plwiki", "itwiki"]]
    L += ["## Table S7. Registered tests in the held-out editions, as produced by the registered code", "",
          "Bootstrap replicates in the registered code: 2,000 for H1 and H2, 500 for H4 (H4 intervals recomputed with 2,000 replicates are given below).", "",
          pd.concat(rows).set_index("edition").T.to_markdown(floatfmt=".3f"), ""]
    for cells in h.cells.unique():
        g = h[h.cells == cells].set_index("wiki").loc[WIKIS]
        L += [f"**H4 recomputed with 2,000 paired bootstrap replicates, {cells}** (ratio of the largest to the smallest odds ratio of retention across cells).", "",
              pd.DataFrame({"Edition": [NAME[x] for x in g.index], "max/min odds ratio": g.ratio.round(3).values,
                            "95% interval": [f"[{a:.3f}, {b:.3f}]" for a, b in zip(g.lo, g.hi)], "one-sided 95% lower bound": g.one_sided_lower_95.round(3).values}).to_markdown(index=False), ""]

    win = rd("robust_cross_windows.csv"); var = rd("robust_cross_variants.csv"); coh = rd("robust_cross_cohorts.csv")
    L += ["## Table S8. Registered robustness analyses (bots and one-click tools excluded together, as registered)", "",
          "**Replace effect in percentage points by window (dump rule, page-history samples).**", "", piv(win.assign(W=win.W.map(lambda x: WL.get(x, x))), "W", "delta_replace_pp", fmt=".2f", order=["12 h", "24 h", "48 h", "7 d", "30 d", "180 d", "unbounded"]), "",
          "**Strict effect in percentage points by filter variant, 24 hours (full cohorts).**", "", piv(var[var.W == "W24h"], "variant", "delta_pp", fmt=".2f"), "",
          "**Bot-or-tool share of first reverts within 24 hours by cohort variant.**", "", piv(coh[coh.W == "W24h"], "cohort", "rel_delta"), ""]
    ks = rd("robust_kowiki_surge.csv")
    L += ["**Korean, with and without the surge of June 2023 to December 2024.**", "",
          ks.rename(columns={"cohort": "Cohort", "n": "First edits", "p_F0_W24h": "p reverted, 24 h", "rel_W24h": "Bot-or-tool share, 24 h", "p_F0_Winf": "p reverted, unbounded", "R": "R, dump rule"})[
              ["Cohort", "First edits", "p reverted, 24 h", "Bot-or-tool share, 24 h", "p reverted, unbounded", "R, dump rule"]].to_markdown(index=False, floatfmt=".3f"), "",
          "Leave-one-edition-out and by-year results are in `04_output/robust_dose_response_loo.csv` and `04_output/<edition>_grid_by_year.csv`.", ""]

    tags = rd("tag_availability_by_wiki.csv")
    L += ["## Table S9. Change tags on reverting revisions by edition and year (all namespaces)", ""]
    for tag in ["mw-rollback", "huggle", "twinkle", "mw-undo"]:
        g = tags[tags.tag == tag].set_index("wiki").loc[WIKIS, [f"y{y}" for y in range(2018, 2027)]]
        g.columns = [x[1:] for x in g.columns]; g.index = [NAME[x] for x in g.index]
        L += [f"**{tag}**", "", g.to_markdown(floatfmt=",.0f"), ""]
    cs = rd("rev_cluster_sensitivity.csv"); QN = {"D_d3_pp": "H1 difference D, dump rule (points)", "R_d3": "R, dump rule", "R_d3r": "R, radius rule", "S_registered": "H2 share S (registered definition)",
                                              "OR_retention_tool": "Odds ratio of retention, tool-reverted vs not reverted", "untagged_all": "Untagged share of radius-rule reverts"}
    cs = cs[cs.quantity.isin(QN)].copy()
    cs["cell"] = [f"{e:.3f}; editors [{a:.3f}, {b:.3f}]; accounts [{c:.3f}, {d:.3f}]" for e, a, b, c, d in zip(cs.estimate, cs.editor_lo, cs.editor_hi, cs.cluster_lo, cs.cluster_hi)]
    h3 = rd("rev_h3_windows.csv")
    L += ["## Table S10. Sensitivity of intervals to clustering in reverting accounts, and H3 under two windows (page-history samples)", "",
          "Cells: estimate; 95 percent percentile interval resampling editors; 95 percent percentile interval resampling the accounts that made the first revert "
          "(non-reverted edits and edits first reverted by an unregistered editor are their own clusters; 1,000 replicates). No registered decision changes: under account resampling the one-sided 95 percent lower bound of D "
          "is above 0 and the upper bound of S below .25 in the three held-out editions.", "",
          piv(cs.assign(quantity=cs.quantity.map(QN)), "quantity", "cell", fmt="", order=list(QN.values())), "",
          "**H3, second clause: of first edits reverted under the dump rule but not tagged, the share whose first revert lies beyond the 15-revision radius.**", "",
          piv(h3, "window", "share_beyond_radius"), ""]
    L += ["## Table S11. The proposed reporting items (Table 5 of the article) completed for this study", "",
          "| Item | This study |", "|---|---|",
          "| 1. Construct | None adopted; the study compares what the indicator contains under each of four constructs (Table 1). |",
          "| 2. Attribution rule | Three, compared: the `revision_is_identity_reverted` field of the history dumps (unbounded); the same hashes with a 15-revision radius; the `mw-reverted` tag. |",
          "| 3. Window | 24 hours, 7 days, 180 days and unbounded, all reported; 12 hours, 48 hours and 30 days in Table S8. No window is treated as validated for the non-English editions. |",
          "| 4. Bots, tools, author | Each counted and reported as a separate class; exclusions shown as variants (Table 3, Table S3). |",
          "| 5. Shares and accounts | Table 3 and Table S2, with the number of accounts making tool reverts and the share of the most active. |",
          "| 6. Outcomes by class | Retention by class of first reverter (Figure 3, Table S5). |",
          "| 7. Both rules | Follow-up and window results under the unbounded and the radius rule (Table 4, Table S4). |",
          "| 8. Tag | Patrolling regime and autopatrol rules per edition (Endnote 2); tag used for first edits from October 2020; coverage against the radius rule (Table S6). |", "",
          "## Figure S1. Odds ratio of retention in the nine registered cells, by edition", "", "![](figures/FigureS1.png)", "",
          "Reverted versus non-reverted first edits under three reverter filters (all reverts; without bots; without bots and one-click tools, strict recoding) and three windows. "
          "The movement across cells is compositional (see the article).", "",
          "## Figure S2. Monthly newcomer first edits and 24-hour revert rates in Korean, English and Japanese, 2019 to March 2026", "", "![](figures/FigureS2.png)", "",
          "Upper panel: first edits per month relative to the edition's median. Lower panel: share reverted within 24 hours, all reverts (solid) and without bots and one-click tools (dashed). "
          "The drop of the dashed English line in September 2020 marks the start of Twinkle tagging.", ""]
    with open(os.path.join(M, "supplement_v0.6.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    print("supplement v0.6 written")


if __name__ == "__main__":
    main()
