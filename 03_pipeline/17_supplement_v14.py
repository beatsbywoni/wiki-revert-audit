"""Supplementary Material, generated from released aggregates in 04_output/.

Output: 05_manuscript/supplement_v0.14.md. Cells with fewer than 50 edits are not shown (registered minimum cell size).
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

Decisions. H1, H2 and H4 are tested with one-sided 95 percent bootstrap bounds (editors resampled), Holm-adjusted over the three tests within an edition. With three tests the Holm procedure compares the smallest p value with .05/3, the next with .05/2 and the largest with .05. In every supported decision in Table S7 none of the 2,000 bootstrap replicates fell on the wrong side of the threshold. This is a count, not an exact p value: with 2,000 replicates the smallest attainable bootstrap p value is 1/2,001, which is below the strictest Holm level of .05/3, so the adjustment changes no decision. The one unsupported decision (H4, Polish) is unsupported without adjustment. H3 is a descriptive criterion without a test.

Specification of the registered hypotheses (registered text, Section 4; registered code at commit 7fcff3d; outputs `04_output/<wiki>_confirmatory.csv` and, for H4 with 2,000 replicates, `04_output/rev_h4_boot2000.csv`). Strict: edits first reverted by an excluded class are recoded as not reverted. Replace: the first later revert by a non-excluded reverter is sought.

| | Estimand | Data | Variant | Window | Registered criterion | Resampling |
|---|---|---|---|---|---|---|
| H1 | D = Δ(24 h) − Δ(unbounded), where Δ is the revert rate with all reverts minus the rate with bots and tools excluded; R = Δ(unbounded)/Δ(24 h) reported | Page-history sample | Replace | 24 hours and unbounded | One-sided 95 percent lower bound of D above 0 (R of .75 or more read as most of the effect persisting) | Editors, 2,000 |
| H2 | S = 1 − Δ(replace)/Δ(strict), the share of bot- or tool-reverted edits with a later non-bot, non-tool revert | Page-history sample | Replace against strict | 24 hours | One-sided 95 percent upper bound of S below .25 | Editors, 2,000 |
| H3 | Agreement of the tag rule with the radius rule; share of edits reverted under the dump rule and untagged whose first revert lies beyond the radius | Page-history sample, first edits from 1 August 2020 as registered | Neither (detection rules) | Unbounded | Agreement of at least .95; share above .5. Descriptive, no test | None |
| H4 | Ratio of the largest to the smallest odds ratio of retention (reverted against not reverted) across nine cells: all reverts, without bots, without bots and tools, by 24 hours, 7 days and unbounded | Full cohort | Strict | 24 hours, 7 days, unbounded | Ratio of at least 1.5 with a 95 percent lower bound above 1.0 | Editors; 500 in the registered code, recomputed with 2,000 |

Holm adjustment is applied over H1, H2 and H4 within an edition.

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
| 11 | Minimum cell size 50 | Applied in all tables of the manuscript; an earlier public draft showed some smaller cells | None |
| 12 | Holm adjustment "across H1 to H4" | Applied over H1, H2 and H4; H3 has no test statistic. H1: all three R values are at or above the registered .75, read as registered ("most of the filter effect persists"). H4: registered as a point ratio of at least 1.5 with a lower bound above 1.0; reported so | None |
| 13 | Model used for coding assistance | The review coding by a language model and its checks are described in the manuscript; an internal pre-submission check of drafts by language-model reviewers led to several of the changes above and is recorded in the work log | None |
"""


def main():
    L = ["# Supplementary Material", "",
         "Which reverts count? Reverter populations, attribution rules and observation windows behind a Wikipedia indicator of information quality work", "",
         "Tables are generated by `03_pipeline/17_supplement_v14.py` from the aggregates in `04_output/` of the public repository. Editions marked * were held out "
         "for the registered tests. Dump rule: the history dumps' unbounded identity-revert rule. Radius rule: the same hashes with the 15-revision radius of the mwreverts library. "
         "Except for Table S7 and the registered rows of Table S8, all analyses are exploratory. Shares based on fewer than 50 edits are not shown; counts are.", "", S1, ""]

    RA = rd("practice_review.csv").fillna(""); R = RA[RA.in_tallies == "yes"]; NS = "not stated"; n = len(R)
    keep = ["short_cite", "venue", "editions", "construct", "detection", "radius_or_rule", "bot_reverts", "tool_reverts", "self_reverts", "window", "sensitivity_over_revert_choices", "source"]
    CON = {"Q": "quality judgment", "C": "conflict", "R": "rejection", "E": "effort", "O": "other"}
    R2 = R[keep].copy(); R2["construct"] = R2.construct.map(CON)
    idr = R.detection.str.contains("identity")
    def two(col, rc, sub=None):
        S = R if sub is None else R[sub]; s = S[col] == NS if col != "radius_or_rule" else ~S[col].str.contains("revisions")
        return int((~s).sum()), int((s & (S[rc] != "")).sum()), int((s & (S[rc] == "")).sum())
    tal = [("Detection rule",) + two("detection", "detection_recoverable"), (f"Search radius, in the {int(idr.sum())} studies using an identity rule",) + two("radius_or_rule", "radius_recoverable", idr),
           ("Reverts made by bots",) + two("bot_reverts", "bot_recoverable"), ("Reverts made with one-click tools", int((R.tool_reverts != NS).sum()), 0, int((R.tool_reverts == NS).sum())),
           ("Self-reverts",) + two("self_reverts", "self_recoverable"), ("Observation window",) + two("window", "window_recoverable")]
    T2 = pd.DataFrame(tal, columns=["Choice", "Stated in the article", "Not stated, but recoverable", "Neither"])
    EL = R.role.isin(["outcome", "exposure", "ML label"]) & (R.id != "L01")
    T2.loc[T2.Choice == "Observation window", "Choice"] = "Observation window, all studies"
    T2.loc[len(T2)] = (f"Observation window, in the {int(EL.sum())} studies with an edit-level measure (outcome, exposure or label; Stvilia et al., 2007, whose measures are article-level aggregates, is not among them)",) + two("window", "window_recoverable", EL)
    n3 = (R.bot_reverts == NS) & (R.tool_reverts == NS) & (R.self_reverts == NS); n3c = n3 & (R.bot_recoverable == "") & (R.self_recoverable == "")
    w = R.window == NS; wc = w & (R.window_recoverable == "")
    T1 = pd.DataFrame({"Studies": R.groupby("construct").size(), "No statement on bot, tool or self-reverts": n3.groupby(R.construct).sum(), "No window stated": w.groupby(R.construct).sum()}).loc[["Q", "C", "R", "E", "O"]]
    T1.index = [CON[k] for k in T1.index]; T1.loc["all"] = T1.sum()
    rc = ["detection_recoverable", "radius_recoverable", "bot_recoverable", "self_recoverable", "window_recoverable"]
    RC = R[(R[rc] != "").any(axis=1)][["short_cite"] + rc].rename(columns={k: k.replace("_recoverable", "") for k in rc})
    NT = RA[RA.in_tallies != "yes"][["short_cite", "venue", "tally_exclusion", "notes"]].copy()
    NT["reason"] = [e if e else ("full text could not be read" if "unreadable" in x or "binary" in x else "same sample and measures as Stvilia et al. (2007)") for e, x in zip(NT.tally_exclusion, NT.notes)]
    L += [f"## Table S1. Survey of reporting practice: how {n} studies using a revert-based measure operationalize it", "",
          "One row per study. The coding table with the passage supporting each code, URLs, evidence levels, the author's check of each study and the earlier model-to-model comparison is `04_output/practice_review.csv` and the files beside it. "
          "Search record: `04_output/practice_review_LIS_search.md`.", "",
          "**Inclusion.** A study is tallied if a revert measure computed from revision histories is an outcome, an exposure, a label or a conflict indicator in its main analysis, or is itself the object of description. "
          "Studies in which reverting is one category in a coding of editing activity, or enters only as a control variable, are listed below and not tallied, because radius, window and reverter population are not choices their authors faced in the same form. "
          "This criterion was narrowed after a first version of the review had tallied those four studies; the narrowing lowers the counts of unstated choices.", "",
          "**Flow of studies.** Stage 1 (citation networks of the methodological works and keyword searches; the number of records screened was not logged): 36 eligible studies, of which 34 were tallied and 2 are listed but not tallied because the full text could not be read. "
          "Stage 2a (OpenAlex, information science and neighboring journals): 911 records from six queries and 258 from a title search (1,169 in all); 79 assessed for eligibility; "
          "54 candidates could at first be read only as abstracts or not at all. Stage 2b (12 November 2026, publisher full texts through institutional access and open-access copies): 45 of those 54 candidates were read in full (JASIST 9, Journal of Information Science 3, Information Processing & Management 3, Library & Information Science Research 1, Journal of Documentation 2, Online Information Review 5, New Media & Society 5, Social Science Computer Review 2, Information, Communication & Society 3, Journal of Computer-Mediated Communication 2, Computers in Human Behavior 1, First Monday 5, PLoS ONE 3, Royal Society Open Science 1), and the full text of 242 JASIST and ASIS&T proceedings articles returned by a search for Wikipedia and revert terms was screened by term counts, with every article mentioning Wikipedia at least eight times and reverting at least twice inspected. "
          "Retrieval and term-count screening in both stages were run through a language-model tool and a scripted browser session; eligibility was decided on the retrieved text. "
          "Stage 2 yielded 12 studies with a revert-based quantity: 7 are tallied, 4 are listed but not tallied under the inclusion criterion above, and 1 (an earlier conference report of the same sample as Stvilia et al., 2007) is listed but not tallied. "
          "The other candidates read contain no revert-based measure or use reverts only as background, as a described example, as one hand-coded category on policy pages without a reported quantity, or as a sample filter. "
          "Eleven texts could not be read: the two eligible studies of stage 1 named above, and nine candidates of stage 2 (four PLoS ONE articles and one Physical Review E article that could not be retrieved by the tools used, one New Media & Society article whose file could not be parsed, and three ACM proceedings papers). "
          f"Total tallied: {n}. The codes of one tallied study (Priedhorsky et al., 2007) were proposed from an extract made in the first pass, because no copy could be retrieved for the model's second pass (recorded in `notes`).", "",
          "**Reading and coding.** A language model (Claude, Anthropic; model versions and dates in `04_logs/AI_ASSISTANCE_LOG.md`) extracted candidate passages and proposed codes, instructed to code a choice as stated only on finding an establishing passage and to record it. "
          "The author checked the codes of every tallied study against the source text and, where available, released code or author copies (column `author_check`); for four studies, two of them tallied, the check was assisted by a second language model (ChatGPT, OpenAI). Eligibility was proposed by the model on the retrieved text; the author confirmed the list of included studies and did not re-read the candidates the model excluded. "
          "The `notes` and `evidence_level` columns record where a code rests on an extracted passage and not on a re-read of the full text. "
          "No second human coder took part, and no reliability coefficient is claimed for the final codes. For the record of the process: before the coding rules were final, a separate model instance coded a random 13 studies blind and agreed with the first pass on 72 of 78 judgments "
          "(kappa 1.00 for the three reverter choices, .78 for detection, .61 for window, .59 for sensitivity analysis); that comparison is between two runs of the same model family on superseded codes and says nothing about the final table. The construct codes were assigned by the author and were not part of it.", "",
          "**Tallies.** The article reports one tally (its Table 2): a choice counts as stated only if the article or its supplement states it for the main analysis. A rule stated only for a sub-analysis is not the study's rule. A detection principle named in the text counts as stated even if its implementation is deferred to a citation (Halfaker et al., 2013); detection given only by citation does not (Lam et al., 2011). "
          "The observation window is tallied in the article only for studies whose revert measure is an edit-level outcome, exposure or label, because for conflict measures computed over whole article histories and for descriptive studies it does not apply in the same form. "
          "For information, the table below also shows in how many studies an unstated choice can be recovered from a cited procedure, a named library default, the named data source, released code or the design of the measure "
          "(the wording \"eventually reverted\"; a measure built on mutual reverts between two editors). "
          "These entries were derived from the notes of the author's check and confirmed by the author; they are the last column of Table 2 of the article. The whole-history design is marked only where the study states it. "
          "Removing bot accounts or bot-authored edits from the sample is not counted as recoverable for reverts made by bots: it concerns who wrote the observed edits, not who reverted them. The ten studies concerned are listed below.", "",
          T2.to_markdown(index=False), "",
          f"Studies that state nothing on bots, tools or self-reverts: {int(n3.sum())} ({int(n3c.sum())} if recoverable choices are counted). Some sensitivity analysis over a revert choice: {int((R.sensitivity_over_revert_choices != 'no').sum())}; over the reverter population: 0.", "",
          "**By construct (constructs assigned by the author; four studies that evaluate detection methods or report descriptive rates are under other).**", "", T1.to_markdown(), "",
          "**Codes.**", "", R2.to_markdown(index=False), "",
          "**Studies that remove bots from the sample without stating how reverts made by bots are treated.** Refers to: authors (the accounts whose edits are observed) or unclear.", "",
          R[R.bot_exclusion_refers_to != ""][["short_cite", "bot_exclusion_refers_to", "bot_exclusion_evidence"]].rename(columns={"short_cite": "Study", "bot_exclusion_refers_to": "Exclusion refers to", "bot_exclusion_evidence": "Basis in the coding notes"}).to_markdown(index=False), "",
          "**Choices recoverable from outside the article's own statement.**", "", RC.to_markdown(index=False), "",
          "**Listed, not tallied.**", "", NT[["short_cite", "venue", "reason"]].to_markdown(index=False), "",
          "**Reporting items 1 to 4 (Table 4 of the article) applied to the reviewed studies.** Item 1 (construct) could be assigned by the author for all studies but is seldom named by the study itself; "
          f"item 2 (attribution rule) is stated in {int((R.detection != NS).sum())} of {n}; item 3 (window) in {int((R.window != NS).sum())}; "
          f"item 4 (bots, tools and self-reverts, all three) in {int(((R.bot_reverts != NS) & (R.tool_reverts != NS) & (R.self_reverts != NS)).sum())}, "
          f"at least one of the three in {int(((R.bot_reverts != NS) | (R.tool_reverts != NS) | (R.self_reverts != NS)).sum())}.", "",

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
                        "First reverts made by the revision that follows the measured edit": ctx.d3_share_first_span_1.round(3).values}).to_markdown(index=False), ""]

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
    L += ["**By user group of the reverting account.** The groups are those recorded for the account at the time of the revert (`event_user_groups_historical`). Whether a group carries the autopatrol right "
          "(recent-changes patrolling) or the autoreview right (FlaggedRevs) is taken from each edition's configuration as read in November 2026 (Endnote 1 of the article); the configuration history was not reconstructed, "
          "so the classification is a proxy for the rights an account held when it reverted, and patrol or review actions themselves were not observed. Implicit groups such as autoconfirmed, and the automatic French promotion, are not recorded in this field. "
          "The table with account-resampled intervals further below gives the cells.", ""]
    e = rd("rev_taggap_editcount.csv"); e["cell"] = [f"{u:.3f} [{a:.3f}, {b:.3f}]; n = {n:,}" for u, a, b, n in zip(e.untagged, e.lo, e.hi, e.n)]
    L += ["**Registered manual reverters other than the author with no explicit group, by the account's edit count at the time of the revert.** "
          "On the French edition the autopatrolled status is granted automatically at 500 edits and 90 days and is not recorded as an explicit group. Account age at the time of the revert was not extracted, so the edit count is a proxy for that status, not a determination of it.", "",
          piv(e, "reverter_edit_count", "cell", fmt="", order=["under 50", "50 to 499", "500 to 4,999", "5,000 or more"]), ""]
    g = t[(t.breakdown == "year") & (t.reverter_class == "all")]
    L += ["**All reverters, by year of the first edit.**", "", piv(g.assign(year=g.year.astype(int)), "year", "untagged"), ""]

    ex = rd("rev_example_tag_vs_hash.csv").set_index("wiki").loc[WIKIS]; exc = rd("rev_example_cluster.csv").set_index("wiki")
    L += ["**Worked example: one cross-edition comparison computed with the tag and with the radius rule** (first edits from October 2020; share of first edits counted as reverted; "
          "gap to English in percentage points; odds ratio of retention for reverted against non-reverted newcomers).", "",
          pd.DataFrame({"Edition": [NAME[x] for x in ex.index], "n": ex.n.map("{:,}".format).values, "Reverted, tag": ex.p_tag.round(3).values, "Reverted, radius rule": ex.p_radius.round(3).values,
                        "Gap to English, tag": ex.gap_to_english_tag_pp.round(1).values, "Gap to English, radius rule": ex.gap_to_english_radius_pp.round(1).values,
                        "Change in gap [95% interval, editors resampled]": ["" if pd.isna(a) else f"{a:.1f} [{b:.1f}, {c:.1f}]" for a, b, c in zip(ex.gap_change_pp, ex.gap_change_lo, ex.gap_change_hi)],
                        "[95% interval, reverting accounts resampled]": ["" if w == "enwiki" else "[{:.1f}, {:.1f}]".format(*exc.loc[w, ["cluster_lo", "cluster_hi"]]) for w in ex.index],
                        "OR retention, tag": ex.OR_retention_tag.round(2).values, "OR retention, radius rule": ex.OR_retention_radius.round(2).values}).to_markdown(index=False), ""]

    ct = rd("rev_tag_radius_crosstab.csv"); ct = ct[ct.period == "from 2020-10"].set_index("wiki").loc[WIKIS]
    L += ["**Tag by radius rule, cell by cell** (first edits from October 2020). The two rules are not nested: MediaWiki records an edit made through the undo function as a revert whether or not the result is identical to an earlier revision, "
          "so the tag also marks edits that no hash-based rule finds. Dump flag: the dumps' own identity-revert field, computed by Wikimedia on the complete page history. "
          "The last column bounds the effect of loading the English history from 2018: edits that the dumps' flag marks reverted and the recomputation on the loaded history does not.", "",
          pd.DataFrame({"Edition": [NAME[x] for x in ct.index], "n": ct.n.map("{:,}".format).values, "Both": ct.both.map("{:,}".format).values, "Tag only": ct.tag_only.values, "Radius rule only": ct.radius_only.map("{:,}".format).values,
                        "Neither": ct.neither.map("{:,}".format).values, "Tag only, % of first edits": ct.tag_only_pp.round(2).values, "Radius rule only, % of first edits": ct.radius_only_pp.round(2).values,
                        "Tag only: reverted under the dump flag": ct.tag_only_dumpflag_yes.values, "Tag only: not reverted under the dump flag": ct.tag_only_dumpflag_no.values,
                        "Dump flag yes, recomputation no": ct.dumpflag_yes_recomputed_no.values}).to_markdown(index=False), ""]
    dc = rd("rev_example_decomposition.csv"); dc["Edition"] = dc.wiki.map(NAME)
    L += ["**Decomposition of the change in the gap to English between the two rules, by period of the first edit** (percentage points). "
          "Change = radius-only share in the edition, minus its tag-only share, plus the English tag-only share, minus the English radius-only share.", "",
          dc.rename(columns={"period": "Period", "gap_tag_pp": "Gap, tag", "gap_radius_pp": "Gap, radius rule", "change_pp": "Change", "other_radius_only_pp": "Radius only, edition", "other_tag_only_pp": "Tag only, edition (minus)",
                             "english_tag_only_pp": "Tag only, English", "english_radius_only_pp": "Radius only, English (minus)"})[
              ["Edition", "Period", "Gap, tag", "Gap, radius rule", "Change", "Radius only, edition", "Tag only, edition (minus)", "Tag only, English", "Radius only, English (minus)"]].to_markdown(index=False, floatfmt=".2f"), ""]
    gp = rd("rev_taggap_period.csv"); gp = gp[gp.wiki.isin(["itwiki", "frwiki", "dewiki", "plwiki"]) & (gp.period != "from 2020-10")].copy()
    gp["cell"] = ["" if pd.isna(u) else f"{u:.3f} (share of reverts {sh:.3f})" for u, sh in zip(gp.untagged_share, gp.share_of_radius_reverts)]
    gp["col"] = gp.wiki.map(NAME) + ", " + gp.period
    L += ["**Untagged share of radius-rule reverts by class of first reverter and period, editions with patrolling or FlaggedRevs.** Classes with fewer than 50 reverts are blank.", "",
          gp.pivot(index="reverter", columns="col", values="cell").loc[["all", "tool", "other manual", "unregistered", "self"]].to_markdown(), "",
          "Notes. The tag sits on the reverted edit and is set by any approved revert within its depth, including a later one by another account, while rows are classified by the first reverter under the radius rule; "
          "the class-specific untagged shares are therefore lower bounds on the omission per revert. Holders of global rights (global rollbackers, global sysops, stewards) have no local group in `event_user_groups_historical` and fall under \"no group\". "
          "Manual patrol actions are recorded in the public logging table, which was not used; a join of reverting revisions to patrol log entries would test the mechanism directly.", ""]
    cl = rd("rev_taggap_cluster.csv"); cl["Edition"] = cl.wiki.map(NAME)
    cl["Untagged [Wilson]; [reverting accounts resampled]"] = [f"{u:.3f} [{a:.3f}, {b:.3f}]; [{c:.3f}, {d:.3f}]" for u, a, b, c, d in zip(cl.untagged, cl.wilson_lo, cl.wilson_hi, cl.cluster_lo, cl.cluster_hi)]
    L += ["**Untagged share with intervals that resample reverting accounts** (2,000 resamples; unregistered reverters and self-reverts are their own clusters). Here the group is one that carries the autopatrol right (Italian: autopatrolled, botadmin, rollbacker, sysop, bot; French: autopatrolled, sysop, bot) or the autoreview right (German, Polish: editor, reviewer, autoreview, sysop, bot) in the edition's own configuration; in English, Korean and Japanese, where neither regime applies to ordinary pages, a common list of administrative and patrol groups is used. Intervals here and in Table S10 come from separate bootstrap runs and can differ in the third decimal.", "",
          cl.rename(columns={"cell": "Reverter", "reverts": "Reverts", "accounts": "Accounts", "top_account_share": "Share of the most active account"})[
              ["Edition", "Reverter", "Reverts", "Accounts", "Share of the most active account", "Untagged [Wilson]; [reverting accounts resampled]"]].to_markdown(index=False, floatfmt=".3f"), ""]

    h = rd("rev_h4_boot2000.csv")
    rows = [rd(f"{wk}_confirmatory.csv").assign(edition=NAME[wk]) for wk in ["jawiki", "plwiki", "itwiki"]]
    rx = rd("rev_retention_existing_pages.csv"); rx["Edition"] = rx.wiki.map(NAME)
    L += ["**With first edits that create a page removed from the reference group (page-history samples, dump rule, exploratory).** Odds ratios of editing again on days 2 to 60 against newcomers not reverted within 24 hours.", "",
          rx.rename(columns={"scope": "Scope", "n": "n", "retained_not_reverted": "Retained, not reverted", "retained_tool": "Retained, tool", "retained_manual": "Retained, manual", "retained_self": "Retained, self",
                             "OR_tool": "OR tool", "OR_manual": "OR manual", "OR_self": "OR self"}).assign(n=lambda x: x.n.map("{:,}".format))[["Edition", "Scope", "n", "Retained, not reverted", "OR tool", "OR manual", "OR self"]].to_markdown(index=False, floatfmt=".3f"), ""]
    S7LAB = {"n": "H1: first edits in the sample", "delta24_pp": "H1: replace effect within 24 hours (points)", "deltainf_pp": "H1: replace effect, unbounded (points)",
             "D_pp": "H1: difference D (points)", "D_ci90_lo": "H1: D, 90% lower bound", "D_ci95_lo": "H1: D, one-sided 95% lower bound", "D_ci95_hi": "H1: D, 95% upper bound",
             "R": "H1: ratio R", "R_ci_lo": "H1: R, 95% lower bound", "R_ci_hi": "H1: R, 95% upper bound",
             "h2_n": "H2: first edits in the sample", "h2_delta_strict_pp": "H2: strict effect within 24 hours (points)", "h2_delta_replace_pp": "H2: replace effect within 24 hours (points)",
             "h2_S": "H2: share S", "h2_S_ci95_hi_onesided": "H2: S, one-sided 95% upper bound", "h2_S_ci_lo": "H2: S, 95% lower bound", "h2_S_ci_hi": "H2: S, 95% upper bound",
             "h3_n": "H3: first edits from 1 August 2020", "h3_agree_d2_d3r15": "H3: agreement, tag and radius rule", "h3_agree_d1_d2": "H3: agreement, tag and dump rule",
             "h3_n_d1only": "H3: reverted under the dump rule, untagged (n)", "h3_d1only_beyond_radius": "H3: of these, share beyond the radius",
             "h4_or_ratio": "H4: largest over smallest odds ratio, nine strict cells", "h4_or_ratio_ci_lo": "H4: ratio, 95% lower bound", "h4_or_ratio_ci_hi": "H4: ratio, 95% upper bound", "h4_boot": "H4: bootstrap replicates in the registered code"}
    S7T = pd.concat(rows).set_index("edition").T.loc[list(S7LAB)]
    S7T = S7T.apply(lambda r: [f"{int(round(v)):,}" if r.name in ("n", "h2_n", "h3_n", "h3_n_d1only", "h4_boot") else f"{v:.3f}" for v in r], axis=1, result_type="expand")
    S7T.columns = [NAME[w] for w in ["jawiki", "plwiki", "itwiki"]]; S7T.index = [S7LAB[k] for k in S7T.index]
    L += ["## Table S7. Registered tests in the held-out editions, as produced by the registered code", "",
          "Bootstrap replicates in the registered code: 2,000 for H1 and H2, 500 for H4 (H4 intervals recomputed with 2,000 replicates are given below).", "",
          S7T.to_markdown(disable_numparse=True), "",
          "Output names in `<wiki>_confirmatory.csv`, in row order: " + ", ".join(f"`{k}`" for k in S7LAB) + ".", ""]
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
          "Editor-resampled intervals here and in Table S4 come from separate bootstrap runs and can differ in the third decimal. "
          "Coverage of account resampling: done for H1 (D and R under both rules), H2, the odds ratio of retention for tool-reverted against non-reverted newcomers, the untagged share (this table and Table S6) and the worked example (Table S6); "
          "not done for H4, for the odds ratios of manual and self-reverts, or for the direct contrast between manual and tool reverts, which the article reports as a descriptive range over complete cohorts.", "",
          "Cells: estimate; 95 percent percentile interval resampling editors; 95 percent percentile interval resampling the accounts that made the first revert "
          "(non-reverted edits and edits first reverted by an unregistered editor are their own clusters; 1,000 replicates). No registered decision changes: under account resampling the one-sided 95 percent lower bound of D "
          "is above 0 and the upper bound of S below .25 in the three held-out editions.", "",
          piv(cs.assign(quantity=cs.quantity.map(QN)), "quantity", "cell", fmt="", order=list(QN.values())), "",
          "**H3, second clause: of first edits reverted under the dump rule but not tagged, the share whose first revert lies beyond the 15-revision radius.**", "",
          piv(h3, "window", "share_beyond_radius"), ""]
    L += ["## Table S11. The proposed reporting items (Table 4 of the article) completed for this study", "",
          "| Item | This study |", "|---|---|",
          "| 1. Construct | The audit is not tied to one construct; it reports what the indicator contains under each of four (Table 1). The cohort of newcomer first edits and the retention outcome correspond to the contributor's experience of rejection. |",
          "| 2. Attribution rule | Three, compared: the `revision_is_identity_reverted` field of the history dumps (unbounded); the same hashes with a 15-revision radius; the `mw-reverted` tag. |",
          "| 3. Window | 24 hours, 7 days, 180 days and unbounded, all reported; 12 hours, 48 hours and 30 days in Table S8. No window is treated as validated for the non-English editions. |",
          "| 4. Bots, tools, author | Each counted and reported as a separate class; exclusions shown as variants (Table 3, Table S3). |",
          "| 5. Shares and accounts | Table 3 and Table S2, with the number of accounts making tool reverts and the share of the most active. |",
          "| 6. Outcomes by class | Retention by class of first reverter (Figure 3, Table S5). |",
          "| 7. Both rules | Follow-up and window results under the unbounded and the radius rule (Tables S4 and S10). |",
          "| 8. Tag | Patrolling regime and autopatrol rules per edition (Endnote 1 of the article); tag used for first edits from October 2020; coverage against the radius rule (Table S6). |", "",
          "## Figure S1. Odds ratio of retention in the nine registered cells, by edition", "", "![](figures/FigureS1.png)", "",
          "Reverted versus non-reverted first edits under three reverter filters (all reverts; without bots; without bots and one-click tools, strict recoding) and three windows. "
          "The movement across cells is compositional (see the article).", "",
          "## Figure S2. Monthly newcomer first edits and 24-hour revert rates in Korean, English and Japanese, 2019 to March 2026", "", "![](figures/FigureS2.png)", "",
          "Upper panel: first edits per month relative to the edition's median. Lower panel: share reverted within 24 hours, all reverts (solid) and without bots and one-click tools (dashed). "
          "The drop of the dashed English line in September 2020 marks the start of Twinkle tagging.", "",
          "## Figure S3. First edits with a later manual revert by a registered third party, by who made the first revert", "", "![](figures/FigureS3.png)", "",
          "Dump rule (top) and 15-revision radius rule (bottom), within 24 hours of the first revert (left) and unbounded (right). Bars are 95 percent Wilson intervals, which ignore clustering in reverting accounts. Exploratory.", ""]
    fl = rd("rev_sample_flow.csv"); fe = fl.groupby("wiki")[["eligible", "sampled", "usable"]].sum().loc[WIKIS]; ct2 = rd("rev_tag_radius_crosstab.csv"); ct2 = ct2[ct2.period == "from 2020-10"].set_index("wiki").loc[WIKIS]
    av = rd("rev_attribution_validation.csv").set_index("wiki").loc[WIKIS]; fx = rd("rev_radius_fixture.csv")
    L += ["## Table S12. Page-history samples and validation of the attribution of first reverts", "",
          "**Sample flow.** Eligible: first edits of self-created accounts, 1 January 2019 to 31 March 2026 (the primary cohort). Sampled: stratified by calendar year of the first edit with proportional allocation "
          "(the same sampling fraction in every year; all eligible edits in Korean), seed 20261026, so unweighted sample shares estimate cohort shares. Usable: the measured edit is found in the loaded page history and, for an edit to an existing page, so is the revision preceding it; first edits that create a page are retained (their shares are in Table S2). "
          "Tag analyses use the usable first edits from 1 October 2020 to 31 March 2026. Year-level counts are in `04_output/rev_sample_flow.csv`.", "",
          pd.DataFrame({"Edition": [NAME[x] for x in fe.index], "Eligible": fe.eligible.map("{:,}".format).values, "Sampled": fe.sampled.map("{:,}".format).values, "Sampling fraction": (fe.sampled / fe.eligible).round(4).values,
                        "Usable": fe.usable.map("{:,}".format).values, "Usable, from 1 Oct 2020": ct2.n.map("{:,}".format).values,
                        "Of these, radius-reverted": (ct2.both + ct2.radius_only).map("{:,}".format).values}).to_markdown(index=False), "",
          "**Which analysis uses which data.**", "",
          "| Analysis | Data | First edits | Revert window | Other window |", "|---|---|---|---|---|",
          "| Composition of first reverts (Table 3, Figure 1, Table S2) | Full cohort | 1 January 2019 to 31 March 2026 | 24 hours (7 days and unbounded in Table S3) | |",
          "| Retention by class (Figure 3, Table S5) | Full cohort | same | 24 hours | Activity on days 2 to 60; blocks within 60 days |",
          "| Tag omission, worked example (Figure 2, Table S6) | Page-history sample | 1 October 2020 to 31 March 2026 | Unbounded to the dump (September 2026) | |",
          "| Follow-up reverts, R, H1, H2 (Tables S4, S7, S10) | Page-history sample | 1 January 2019 to 31 March 2026 | 24 hours and unbounded | |",
          "| H3 (Table S7) | Page-history sample | 1 August 2020 to 31 March 2026 as registered | Unbounded | |",
          "| H4 (Table S7, Figure S1) | Full cohort | 1 January 2019 to 31 March 2026 | 24 hours, 7 days, unbounded | Activity on days 2 to 60 |", "",
          "**Dump fields against the independent recomputation (dump rule, usable samples).** Status: `revision_is_identity_reverted` against the recomputation from content hashes. "
          "Among first edits reverted under both, the first reverting revision and the delay to it are compared, and the class of the first reverter derived from each.", "",
          "Status.", "",
          pd.DataFrame({"Edition": [NAME[x] for x in av.index], "n": av.n.map("{:,}".format).values, "Reverted under both": av.both_reverted.map("{:,}".format).values, "Flag only": av.flag_only.values,
                        "Recomputation only": av.recomputed_only.values, "Neither": av.neither.map("{:,}".format).values, "Status agreement (%)": (av.status_agreement * 100).map("{:.3f}".format).values}).to_markdown(index=False, disable_numparse=True), "",
          "First revert, among first edits reverted under both. Percentages are rounded to three decimals, so a value of 100.000 can stand beside a non-zero count; the counts are exact.", "",
          pd.DataFrame({"Edition": [NAME[x] for x in av.index], "Reverted under both": av.both_reverted.map("{:,}".format).values, "Same first reverting revision (%)": (av.same_first_reverting_revision * 100).map("{:.3f}".format).values,
                        "Different revision (n)": av.different_first_reverting_revision.values, "Crossing 24 hours (n)": av.crosses_24h_boundary.values,
                        "Different class (n)": av.different_reverter_class.values}).to_markdown(index=False, disable_numparse=True), "",
          "Flag-only cases in English are reverts to states older than the loaded history (from 2018); elsewhere there are at most nine cases. No case moves across the 24-hour boundary, and the class of the first reverter differs in at most one case per edition.", "",
          "**Radius rule against python-mwreverts (version 0.1.5, Detector with radius 15) on synthetic page histories.** For every revision, the first reverting revision under the implementation used here is compared with the first revert in which mwreverts lists the revision as reverted.", "",
          pd.concat([fx, pd.DataFrame([dict(fixture="Total", pages=fx.pages.sum(), revisions_checked=fx.revisions_checked.sum(), reverted_under_mwreverts=fx.reverted_under_mwreverts.sum(), mismatches=fx.mismatches.sum())])]).assign(**{c: (lambda c: lambda x: x[c].map("{:,}".format))(c) for c in ["pages", "revisions_checked", "reverted_under_mwreverts", "mismatches"]}).rename(columns={"fixture": "Synthetic histories", "pages": "Pages", "revisions_checked": "Revisions checked", "reverted_under_mwreverts": "Reverted under mwreverts", "mismatches": "Mismatches"}).to_markdown(index=False, disable_numparse=True), "",
          "Not covered by this validation: partial reverts, which no hash-based rule detects, and the tag rule, which is taken from the dumps as recorded.", ""]
    with open(os.path.join(M, "supplement_v0.14.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    print("supplement v0.14 written")


if __name__ == "__main__":
    main()
