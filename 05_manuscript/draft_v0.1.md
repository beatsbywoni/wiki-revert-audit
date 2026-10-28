# Which reverts count? Successor filtering and observation windows in Wikipedia revert-based metrics

Draft v0.1, 2026-10-28. Target: JASIST Research Article (7,000 words body; abstract 200 words; APA; single-blind). Word budget check at the end. Items marked [TBD] need a number or a verified reference before v0.2. Numbers come from `04_output/cross_wiki_table.csv`, `<wiki>_gonogo_report.md`, `<wiki>_confirmatory.csv`, `h3_tag_coverage.csv` and the WORKLOG; none is typed from memory.

## Abstract

Whether a Wikipedia edit was reverted is one of the most widely used indicators of information quality control, editorial conflict and the newcomer experience. The indicator depends on two choices that analysts rarely vary: which later revisions count as a revert (all of them, or only those made by humans rather than bots and semi-automated tools) and how long the edit is observed. This study audits those choices with a fixed-anchor design. The first main-namespace edits of newcomers in seven language editions of Wikipedia are held constant while the successor filter and the observation window are varied, across three revert definitions available in the Wikimedia history dumps. Four editions were examined before registration and three were held out for confirmatory tests of four registered hypotheses. Excluding bot and tool reverts lowers the newcomer revert rate by an amount that tracks the local share of automated reverting, moves editor-level success rankings substantially, and changes the estimated association between being reverted and staying active by a factor of 1.4 to 3. Most of this effect persists when the observation window is unbounded, because humans rarely re-revert what a tool has already removed. The tag-based definition is shown to depend on the reverting editor's patrol status. A reporting checklist for revert-based metrics is proposed.

[Abstract word count: about 195]

**Keywords:** Wikipedia; reverts; information quality; measurement validity; bots; peer production; preregistration

## Introduction

Reverts are the smallest observable unit of quality control in Wikipedia. When an editor restores a page to an earlier state, the intervening contributions are judged, at least implicitly, to have reduced the quality of the article. Because this judgement leaves a trace in the revision history, researchers and the Wikimedia Foundation alike have treated the revert as a proxy for information quality work (Stvilia et al., 2008), for conflict between editors (Kittur et al., 2007; Arazy et al., 2013), and for the reception that newcomers receive (Halfaker et al., 2011, 2013). Revert rates appear as outcome variables in experiments on newcomer onboarding, as predictors of editor retention, and as descriptive statistics in cross-language comparisons of editorial governance (Lewoniewski et al., 2017; Formisano et al., 2026).

Yet "reverted" is not a property of an edit. It is a property of an edit together with two decisions that the analyst makes. The first decision is who gets to count as a reverter. Wikipedia's quality control is partly automated: anti-vandalism bots such as ClueBot NG on the English edition and Salebot on the French edition revert within seconds, and semi-automated tools such as rollback, Huggle and Twinkle let trusted editors revert with a single click (Geiger & Halfaker, 2013). Many studies exclude bot reverts, some also exclude tool-assisted reverts, and others count everything; the choice is usually stated in a sentence and never examined. The second decision is how long to watch. An edit reverted within 24 hours and an edit reverted after three months are both "reverted" under an unbounded window, but only the first counts under the 24-hour or 48-hour windows that the Wikimedia Growth team and many researchers use. These two decisions interact with a third, less visible one: the operational definition of a revert itself. The Wikimedia history dumps flag "identity reverts" detected by content hashing over a page's entire history, the mwreverts library used in much published work searches only the last 15 revisions, and since 2020 MediaWiki itself tags reverted revisions, but only under conditions that depend on who performed the revert.

The problem is a special case of what a companion study calls successor selection (Author, under review). An event-based metric asks whether a later event of a certain kind followed an earlier one. Holding the earlier events fixed, the metric can be moved by changing only the set of later events that are allowed to count. That companion study showed, for software repository mining, that excluding one class of successor events moved an outcome metric by several percentage points without any change in the underlying behavior. Wikipedia reverts are a natural second case, because the successor filter (bots, tools) and the observation window are both routinely varied across studies and because the dumps allow the audit to be run at scale with the anchors held constant.

I therefore ask a measurement question rather than a behavioral one. Given the same newcomers and the same first edits, how far do the cohort revert rate, the editor-level success rate and the downstream estimate of the revert-to-retention association move when the successor filter and the observation window change? Where does the sensitivity come from, and how much of it survives the unbounded window? Do the three revert definitions agree, and when they disagree, why? The study is a measurement audit of public secondary data. Four Wikipedia editions were analyzed before registration; the design, hypotheses and analysis code were then registered on Zenodo (DOI 10.5281/zenodo.23720117), and three further editions were processed and opened only after registration.

The contribution is threefold. First, the audit quantifies, across seven editions and 56 edition-year cells, the dose-response relation between the local share of automated reverting and the sensitivity of revert metrics to the successor filter. Second, it shows that the sensitivity is mostly not a window artefact: because humans rarely re-revert what a bot or tool has already removed, the filter effect persists in the unbounded window, which overturns an intuition drawn from the natural experiment of Geiger and Halfaker (2013). Third, it documents, from the MediaWiki source and from the data, that the tag-based definition depends on the reverting editor's patrol status, so that the three definitions are not interchangeable even in principle. The study ends with a six-item reporting checklist.

## Background

### Information quality work and its indicators

Information science has long treated quality as a property that must be operationalized before it can be studied (Illari & Floridi, 2013). In Wikipedia, Stvilia et al. (2008) described quality work as an organized activity with its own roles, tools and signals, and later studies have modeled article quality from content and process features (Lewoniewski et al., 2017; Wang & Li, 2019). The revert is the elementary signal of that work: it marks a contribution that another participant judged to be unacceptable and removed. Reverts therefore enter studies of conflict (Arazy et al., 2013), of the balance between control and openness in peer production (Author et al. [JASIST 2020 "Loosen control"; verify authors]), and of the increasingly automated division of labor between humans and bots in online knowledge communities ([JASIST 2026 "From divergence to convergence"; verify authors]).

### Reverts and newcomers

Halfaker et al. (2011) showed that being reverted reduces the subsequent activity of newcomers, and Halfaker et al. (2013) argued that the rising rate at which newcomer edits were rejected, often by automated and semi-automated tools, contributed to the decline of the English Wikipedia's editor population. TeBlunthuis et al. (2018) replicated the pattern across many peer production wikis. Boté-Vericad (2026) recently audited four decisions involved in constructing newcomer cohorts from Wikimedia logs and reported that newcomers whose first edit was reverted had odds of leaving after one edit about 1.2 times those of other newcomers. That audit varied the cohort; the present one varies the successor and holds the cohort fixed.

### Bots, tools and the counterfactual

Geiger and Halfaker (2013) used the unplanned outage of ClueBot NG as a natural experiment. Without the bot, vandalism was still reverted, but more slowly: the proportion of damaging edits eventually reverted was unchanged while the time to revert lengthened. The result is often read as licence to treat bot reverts as interchangeable with human reverts for final-state metrics. That reading concerns a counterfactual in which the bot is absent. In observational data the bot is present, and excluding its reverts after the fact removes the event rather than the actor: the content is already gone, so no human needs to revert it. Whether the two readings diverge is an empirical question that this study answers with the substitution rate defined below. Geiger and Halfaker (2017) separately showed that redefining what counts as a bot-bot "fight" changed the conclusions of Tsvetkova et al. (2017), an early demonstration that operationalization choices can reverse findings in this domain.

### Revert definitions

The identity revert, an edit that returns a page to a byte-identical earlier state, is the most common definition (Kittur et al., 2007; Wikimedia Research, n.d.). Implementations differ. The mwreverts library detects identity reverts within a radius of 15 revisions by default. The Wikimedia `mediawiki_history` dataset, which this study uses, flags a revision as reverted if any later revision of the page restores a state that preceded it, with no radius and no time limit; this was verified in the source code of the Analytics Refinery (see Method). Since MediaWiki 1.36 (2020), the software tags reverted revisions with `mw-reverted` when it recognizes the reverting edit as an undo, a rollback or a manual revert within 15 revisions, but, where recent-changes patrolling is enabled, only once the reverting edit has been patrolled or was made by an autopatrolled user (MediaWiki, n.d.). Formisano et al. (2026) used a content-hash definition and listed the lack of a sensitivity analysis across definitions as a limitation. The present study treats the three definitions as a third axis of the audit.

## Method

### Design

The design holds a set of anchor edits fixed and varies only the set of later revisions that are allowed to count as reverts. Three successor filters are crossed with three observation windows. F0 counts all identity reverts. F1 does not count reverts made by bots. F2 does not count reverts made by bots or by semi-automated tools, identified by the `mw-rollback`, `huggle` and `twinkle` change tags where those tags exist in the edition. The windows are 24 hours, 7 days and unbounded (any time before the dump date). Each filter is applied in two variants. In the strict variant, an anchor whose first revert was made by an excluded actor counts as not reverted; this reproduces the common preprocessing practice of dropping bot or tool reverts. In the replace variant, the anchor counts as reverted at the time of the first revert by a non-excluded actor, if any, recomputed from the page's revision history; this asks whether a human would have reverted the edit anyway, and when.

### Data

The data are the `mediawiki_history` dumps of version 2026-09, released monthly by the Wikimedia Foundation. Each row is a revision, page or user event with 78 tab-separated columns; the column order was taken from the refinery source (`MediawikiEvent.toTSVLine`) because the published documentation listed an older 70-column schema. Seven editions were processed. Korean (kowiki), French (frwiki), German (dewiki), Japanese (jawiki), Polish (plwiki) and Italian (itwiki) were downloaded in full. English (enwiki) was downloaded for January 2018 to September 2026 (105 monthly files, 643 million revision rows); the anchor definition below makes this sufficient. Processing kowiki, enwiki, frwiki and dewiki before registration is disclosed in the registration document; jawiki, plwiki and itwiki were processed before registration but their outputs were not opened until the registered commit and the Zenodo deposit existed.

### Cohort and anchors

The unit is a registered editor whose very first edit, in any namespace, was in the main (article) namespace; that first edit is the anchor. This definition can be evaluated from a single dump row (`event_user_first_edit_timestamp`) and so does not require an edition's complete history. Editors whose first edit was elsewhere are excluded; they were 8 to 10 percent of first-time editors in the exploratory editions ([TBD: shares for jawiki, plwiki, itwiki]). Anonymous (IP) editors and temporary accounts are excluded, as are editors flagged as bots by current or historical username pattern or bot group. The primary cohort consists of self-created accounts with anchors dated from 1 January 2019 to 31 March 2026, so that every anchor has at least 180 days of follow-up before the dump date. Table 1 gives the cohort sizes.

### Revert definitions and their verification

D1 is the dump's own `revision_is_identity_reverted` flag together with the identifier of, and the delay to, the first reverting revision. Reading the refinery source (`DenormalizedRevisionsBuilder.scala`) established that the flag is computed per page over the entire history by grouping revisions by content hash: the first occurrence of a hash is the base, later occurrences are reverts to that base, a revision is reverted if a revert whose base precedes it occurs later, and reverts to the same base do not count as reverting each other. No radius or time limit is applied. I reimplemented this rule from the hashes in the dump and compared it with D1 on the full set of kowiki anchors and on 60,000 sampled anchors in each other edition. Agreement on reverted status was complete in the five editions with full histories (frwiki, dewiki, jawiki, plwiki, itwiki: 0 or 1 disagreement each) and 99.98 percent on kowiki; on enwiki, where the downloaded period is partial, 99.9 percent. D3r15 applies the mwreverts convention of a 15-revision radius to the same recomputation. D2 is the `mw-reverted` tag on the anchor, usable for anchors from August 2020 onward.

### Bot and tool identification

A reverting editor is a bot if `event_user_is_bot_by` or its historical counterpart is non-empty; the dump sets these when the username matches the pattern `(?i)^.*bot([^a-z].*$|$)` or the account is in the bot group. The two columns differ for accounts that gained or lost the flag, so their union is used, with the historical flag alone as a sensitivity analysis. Tool reverts are revisions tagged `mw-rollback`, `huggle` or `twinkle`. Tag availability was checked per edition: `mw-rollback` appears from December 2017 and `mw-undo` from January 2018 in all seven editions, `huggle` only in enwiki and frwiki, and `twinkle` only in enwiki (from September 2020). Undo is not treated as a tool, because it is the ordinary manual revert; including it is a sensitivity analysis. Reverts made within 5 seconds by non-bot accounts were examined as a check for unflagged bots: they were 0.1 to 0.7 percent of non-bot reverts and concentrated in a few accounts, so no further adjustment was made.

### Outcomes

Three outcomes are computed in every cell of the grid. The cohort revert proportion p(F, W) is the share of anchors reverted under filter F within window W, with Wilson intervals. The editor success rate is one minus the reverted share of the editor's main-namespace edits in the first 90 days, for editors with at least ten such edits; rankings under F0 and F2 are compared by Spearman correlation and by the share of the bottom decile that changes membership. The downstream estimate is the odds ratio of retention, defined as at least one edit between day 2 and day 60 after the anchor, for reverted versus non-reverted anchors; this is the quantity reported by Boté-Vericad (2026) and by many retention studies.

Paired differences Δ(W) = p(F0, W) − p(F, W) are computed on the same anchors, with 2,000 editor-cluster bootstrap resamples. Replace-variant quantities use a year-stratified random sample of 60,000 anchors per edition (all anchors in kowiki), because they require the page histories.

### Registered hypotheses

Four hypotheses were registered before the confirmatory editions were opened; each is tested within edition with Holm adjustment. H1 (window): in the replace variant the filter effect is larger in the 24-hour than in the unbounded window, Δ(24h) − Δ(∞) > 0, tested by a one-sided bootstrap bound, with the ratio R = Δ(∞)/Δ(24h) reported as the effect size and R of at least 0.75 interpreted as "most of the effect survives". H2 (substitution): the substitution rate S = 1 − Δ(F2 replace, 24h)/Δ(F2 strict, 24h), the share of anchors first reverted by a bot or tool that a human also reverted within 24 hours, is below 0.25. H3 (definitions): the tag and radius-15 definitions agree on at least 95 percent of anchors, and more than half of the anchors that D1 marks reverted but D2 does not lie beyond the 15-revision radius. H4 (downstream): the retention odds ratio varies across the nine strict cells by a factor of at least 1.5. A negative control requires that, in edition-year cells where bots make less than 1 percent of first reverts, the bot-only filter moves the 24-hour rate by less than half a percentage point. The strict-variant difference equals the revert rate times the bot-and-tool share by construction, so dose-response is reported descriptively rather than tested.

### Transparency

Code, cell-level aggregates with at least 50 anchors, simulation outputs, figure data and the deviation log are released on GitHub and archived on Zenodo [TBD: repository URL and release DOI]. Editor-level derived data carry random identifiers; usernames of reverting accounts are not released. The study analyzes public edit histories and was not submitted for ethics review. Generative AI (Claude, Anthropic) was used to draft analysis code, documents and language; all code was tested against synthetic and real data, every claim about the dump and the software was checked against the primary source, and the assistance log is part of the repository.

## Results

### Seven editions

Table 1 summarizes the seven editions. Newcomer first edits were reverted within 24 hours at rates from 14 percent (jawiki) to 37 percent (enwiki). Automated reverting differs sharply across editions. Bots made 12 percent of first reverts in enwiki (median delay 8 seconds, consistent with ClueBot NG) and 4 percent in frwiki (Salebot, median 3 seconds), but 0.3 percent or less elsewhere, where the few bot reverts were slow maintenance edits rather than anti-vandalism. Tool reverts, mostly rollback, ranged from a quarter of first reverts in jawiki and frwiki to more than half in kowiki, itwiki and enwiki.

**Table 1.** Cohorts, automated reverting and the main audit quantities by edition (first-edit anchors of self-created accounts, 2019 to 2026; replace-variant quantities from the 60,000-anchor samples). [TBD: typeset from `cross_wiki_table.csv`]

| Edition | Role | Anchors | p(F0, 24 h) | Bot share | Tool share | Δ F2 strict, 24 h (pp) | Δ F2 replace, 24 h (pp) | Δ F2 replace, ∞ (pp) | R | Spearman ρ, success | Bottom decile moved | OR range |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| enwiki | exploratory | 2,189,284 | .370 | .122 | .562 | 21.1 | 18.8 | 17.4 | .92 | .749 | 55% | 0.43–0.77 |
| itwiki | confirmatory | 135,400 | .342 | .000 | .525 | 17.9 | 15.9 | 13.4 | .84 | .798 | 48% | 0.40–0.71 |
| kowiki | exploratory | 47,633 | .216 | .003 | .517 | 11.2 | 9.8 | 7.6 | .78 | .764 | 56% | 0.32–0.95 |
| dewiki | exploratory | 236,903 | .256 | .001 | .410 | 10.5 | 9.6 | 8.8 | .92 | .895 | 31% | 0.52–0.84 |
| plwiki | confirmatory | 67,755 | .222 | .001 | .315 | 7.0 | 6.2 | 5.5 | .88 | .915 | 31% | 0.54–0.77 |
| frwiki | exploratory | 346,938 | .243 | .042 | .255 | 7.2 | 6.4 | 5.5 | .86 | .926 | 25% | 0.47–0.72 |
| jawiki | confirmatory | 223,045 | .140 | .001 | .247 | 3.5 | 3.0 | 2.7 | .92 | .935 | 28% | 0.36–0.66 |

### The successor filter moves every metric

Excluding bot and tool reverts (F2) lowered the 24-hour revert rate by 3.5 percentage points in jawiki and by 21.1 points in enwiki in the strict variant, and by 3.0 to 18.8 points in the replace variant (Table 1, Figure 1). The bot-only filter (F1) mattered only where anti-vandalism bots operate: 4.5 points strict and 3.0 points replace in enwiki, 1.0 and 0.6 in frwiki, and under 0.1 points in the other five editions. Editor-level success rankings moved with the filter. The Spearman correlation between success rates under F0 and F2 ranged from .75 (enwiki) to .94 (jawiki), and between 25 and 56 percent of the editors in the bottom decile under one filter were not in it under the other. The retention odds ratio ranged across the nine strict cells by a factor of 3.0 in kowiki, 1.8 in enwiki and jawiki, 1.8 in itwiki, 1.6 in dewiki and 1.5 in frwiki and plwiki; the lowest value was always the all-reverts, 24-hour cell and the highest the no-bots-no-tools, unbounded cell. In kowiki the association changed sign across cells within single years ([TBD: cite by-year table]).

### Most of the effect survives the unbounded window (H1)

In the strict variant Δ rose slightly with the window, because the base rate rises while the share of first reverts made by bots and tools is roughly constant (Figure 1, left). In the replace variant Δ fell with the window, as H1 predicts, but only modestly (Figure 1, right). In the three confirmatory editions the difference Δ(24h) − Δ(∞) was 0.24 points in jawiki (one-sided 95 percent lower bound 0.19), 0.77 in plwiki (0.68) and 2.49 in itwiki (2.36), so H1 was supported in each; the ratio R was .92 [.90, .94], .88 [.86, .89] and .84 [.83, .85], above the registered threshold of .75 in all three. The exploratory editions gave R between .78 (kowiki) and .92 (enwiki, dewiki). In no edition did widening the window remove more than a quarter of the filter effect.

[Figure 1 here: fig1_window_by_filter]

### Why: humans rarely re-revert (H2)

The substitution rate S, the share of anchors first reverted by a bot or tool that a human also reverted within 24 hours, was .145 (one-sided 95 percent upper bound .157) in jawiki, .111 (.119) in plwiki and .114 (.119) in itwiki, supporting H2 in each edition; the exploratory values were .09 to .12. Roughly nine in ten edits removed by a tool were never reverted again by a person, because there was nothing left to revert. The levee of Geiger and Halfaker (2013) describes what humans do when the bot is absent; the substitution rate describes what they do when the bot has already acted, and it is small.

Because the strict-variant difference equals the revert rate times the bot-and-tool share, the relative replace-variant difference, Δ/p(F0), should track that share minus the substitution rate. Figure 2 shows that it does, across the seven editions and 56 edition-year cells with at least 200 sampled anchors (Spearman ρ = .98 across cells). The points lie just below the identity line by an amount equal to S. A parameter-grid simulation (bot speed, bot share, human re-revert probability and delay) reproduced the observed R of .78 to .92 only when the human re-revert probability was between .1 and .2 with delays of days to a week; with no re-reverting R equals 1 and with a re-revert probability of .5 and week-long delays R falls to .5 ([TBD: cite simulation table]).

[Figure 2 here: fig2_dose_response]

### Downstream estimates (H4)

The ratio of the largest to the smallest retention odds ratio across the nine strict cells was 1.84 [1.79, 1.88] in jawiki and 1.78 [1.72, 1.84] in itwiki, supporting H4, and 1.43 [1.38, 1.49] in plwiki, below the registered threshold of 1.5, so H4 was supported in two of three confirmatory editions. In every edition the all-reverts, 24-hour definition produced the strongest negative association between being reverted and staying (odds ratios .32 to .54) and the no-bots-no-tools, unbounded definition the weakest (.66 to .95). Figure 3 shows the nine cells per edition. Relative to the point estimate reported by Boté-Vericad (2026), the definition chosen moves the estimate by more than sampling error does.

[Figure 3 here: fig3_or_cells]

### Definitions (H3) and a patrol gate in the tag

The tag definition D2 agreed with the radius-15 recomputation D3r15 on 98.6 percent of anchors in jawiki, 97.9 percent in plwiki and 95.4 percent in itwiki, satisfying the first part of H3; the MediaWiki search radius for manual reverts is 15 revisions, so the agreement is expected. The second part of H3 was rejected in all three editions: among anchors that D1 marked reverted but D2 did not, only 42 percent (jawiki), 9 percent (plwiki) and 7 percent (itwiki) were reverted beyond the 15-revision radius, against 76 percent in the exploratory kowiki data on which the hypothesis had been based. The remaining anchors were identity-reverted within the radius, and the reverting edit itself carried an undo, rollback or manual-revert tag in more than 99 percent of cases, so the software had recognized the revert but had not tagged the reverted revision.

The MediaWiki documentation explains the gap: the `mw-reverted` tag is applied by a deferred job that waits for the reverting edit to be approved, which on wikis with recent-changes patrolling means patrolled or made by an autopatrolled user, and "reverts that are not patrolled will not be marked with the reverted tag" (MediaWiki, n.d.). Figure 4 shows the share of within-radius identity reverts that carry no tag, by edition, against the editions' configuration in the Wikimedia settings repository: 12.0 percent in itwiki and 8.8 percent in frwiki, the two editions with recent-changes patrolling enabled; 4.6 and 5.8 percent in dewiki and plwiki, which use FlaggedRevs; 2.4 to 4.2 percent in kowiki, enwiki and jawiki. Untagged cases had higher shares of anonymous and manual reverters than tagged ones (itwiki: 20 versus 1 percent anonymous). The tag definition is therefore not a revert definition alone; it is a revert definition conditioned on the reverting editor's trust status, and its coverage varies with local configuration.

[Figure 4 here: fig4_tag_coverage]

### Negative control and robustness

In all 24 edition-year cells of the confirmatory editions where bots made less than 1 percent of first reverts, the bot-only filter moved the 24-hour rate by less than half a percentage point, as required. [TBD: robustness paragraph: K = 5 anchors; all registered accounts; historical-only bot flag; undo as tool; 5-second latency as bot indicator; alternative window boundaries; the former anchor definition in kowiki; leave-one-edition-out. These are implemented in the pipeline flags but not yet tabulated.]

## Discussion

### What the audit shows

Holding newcomers and their first edits fixed, the choice of which reverts count moves the cohort revert rate by 3 to 21 percentage points, reorders editor success rankings enough to replace a quarter to a half of the bottom decile, and changes the estimated revert-to-retention odds ratio by a factor of 1.4 to 3. The size of the movement is predictable from one local quantity, the share of first reverts made by bots and tools, minus a substitution rate of about one in ten. The observation window, by contrast, changes little: between 78 and 92 percent of the filter effect remains when the window is unbounded. The common assumption that final-state metrics are robust to how bot reverts are handled is not supported in observational data, and the reason is mechanical. A filter applied after the fact removes events, not actors. The natural experiment that motivated the assumption removed an actor.

### Implications for information quality measurement

For information science the result is a reminder that an indicator of quality work is defined by the population of workers it admits. Studies of quality control in Wikipedia and other peer production systems (Stvilia et al., 2008; Lewoniewski et al., 2017) and of human-bot collaboration in knowledge communities ([JASIST 2026; verify]) should state the successor population explicitly and, where automated reverting is substantial, report the strict and replace variants side by side. The substitution rate is itself an informative statistic: it says how often the community's human members confirm what its automated members did, and it was remarkably stable, at 9 to 15 percent, across editions that differ by an order of magnitude in size and in bot presence.

The tag finding has a practical edge. The `mw-reverted` tag is the most convenient definition because it needs no recomputation, and it is used in Wikimedia's own dashboards. It undercounts reverts of newcomer edits by 2 to 12 percent depending on the edition's patrolling configuration, and the undercount is not random: it falls on reverts made by anonymous and non-autopatrolled editors. Analysts comparing editions by tag-based revert rates will attribute configuration differences to community differences unless they correct for this.

### A reporting checklist

Studies that use revert-based metrics should report: (1) the revert definition, naming the detection method and its radius or absence of one; (2) the successor population, stating which reverters are excluded and how bots and tools were identified, including which change tags were available in the period; (3) the observation window; (4) for any exclusion, both the strict and the replace variant, or the substitution rate; (5) the share of first reverts made by the excluded actors in the data, since it predicts the sensitivity; and (6) for tag-based definitions, the edition's patrolling and FlaggedRevs configuration.

### Limitations

The anchors are first edits of self-created accounts, which is the population for which revert metrics are most often computed, but the audit does not cover established editors or the article-level revert rates used in conflict research, where the same mechanics apply but the shares may differ. The replace variant treats any later restoration of a pre-anchor state as a revert of the anchor, following the dump's own definition, so some replace-variant reverts are wider reverts that happened to span the anchor. The exploratory editions were examined before registration, and the hypotheses, including the thresholds, were shaped by them; the three confirmatory editions were untouched until registration, but they share the same pipeline. Only two of the seven editions have active anti-vandalism bots, so the bot-axis findings rest on enwiki and frwiki. Finally, the dump's revert flag is itself an operationalization, verified here against an independent recomputation but not against human judgement of whether a revert was warranted.

### Conclusion

A revert is a relation between an edit and a later editor, and the metric inherits whatever the analyst decides about that later editor. The audit shows that the decision is consequential, that its consequence is predictable from the local share of automated reverting, that it does not fade with a longer window, and that one of the three standard definitions silently encodes the reverting editor's trust status. None of this makes revert metrics unusable. It makes them reportable.

## Data availability statement

The data that support the findings of this study are openly available from the Wikimedia Foundation at https://dumps.wikimedia.org/other/mediawiki_history/ (version 2026-09). Code, aggregates and the preregistration are available at [TBD: GitHub URL] and Zenodo (10.5281/zenodo.23720117 for the preregistration; [TBD] for the release).

## Endnotes

1. [TBD: note on the 78-column schema and the refinery source commit consulted on 2026-10-26.]
2. [TBD: note on the Wikimedia configuration repository paths consulted for wgUseRCPatrol and the FlaggedRevs dblist.]

## References

[APA; verify every DOI before v0.2]

Arazy, O., Yeo, L., & Nov, O. (2013). Stay on the Wikipedia task: When task-related disagreements slip into personal and procedural conflicts. Journal of the American Society for Information Science and Technology, 64(8), 1634–1648. https://doi.org/10.1002/asi.22869

Author. (under review). Auditing successor selection in software repository mining: Evidence from filtering AI-attributed commits. [companion manuscript]

Boté-Vericad, J.-J. (2026). Constructing newcomer cohorts from Wikimedia logs: Account creation type, deleted contributions, observation windows, and the behavioural threshold (Version 2). Zenodo. https://doi.org/10.5281/zenodo.23435553 [verify DOI form]

Formisano, G., Hine, E., Juneja, P., Laitila, J., Novelli, C., Chiu, E., Dejanikus, E., Levin, M., Schroder, T., West, A., & Floridi, L. (2026). Editorial governance under pressure: Wikipedia's revert dynamics during the 2024 US election. Humanities and Social Sciences Communications, 13, 1459. https://doi.org/10.1057/s41599-026-06810-2

Geiger, R. S., & Halfaker, A. (2013). When the levee breaks: Without bots, what happens to Wikipedia's quality control processes? In Proceedings of the 9th International Symposium on Open Collaboration (WikiSym '13). ACM. https://doi.org/10.1145/2491055.2491061 [verify]

Geiger, R. S., & Halfaker, A. (2017). Operationalizing conflict and cooperation between automated software agents in Wikipedia: A replication and expansion of "Even Good Bots Fight". Proceedings of the ACM on Human-Computer Interaction, 1(CSCW), 49. https://doi.org/10.1145/3134684 [verify]

Halfaker, A., Geiger, R. S., Morgan, J. T., & Riedl, J. (2013). The rise and decline of an open collaboration system: How Wikipedia's reaction to popularity is causing its decline. American Behavioral Scientist, 57(5), 664–688. https://doi.org/10.1177/0002764212469365

Halfaker, A., Kittur, A., & Riedl, J. (2011). Don't bite the newbies: How reverts affect the quantity and quality of Wikipedia work. In Proceedings of the 7th International Symposium on Wikis and Open Collaboration (WikiSym '11) (pp. 163–172). ACM. https://doi.org/10.1145/2038558.2038585 [verify]

Illari, P., & Floridi, L. (2013). The quality and qualities of information. Journal of the American Society for Information Science and Technology, 64(11), 2363–2374 [verify pages]. https://doi.org/10.1002/asi.22783 [verify authors]

Kittur, A., Suh, B., Pendleton, B. A., & Chi, E. H. (2007). He says, she says: Conflict and coordination in Wikipedia. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI '07) (pp. 453–462). ACM. https://doi.org/10.1145/1240624.1240698

Lewoniewski, W., Węcel, K., & Abramowicz, W. (2017). Cultural diversity of quality of information on Wikipedias. Journal of the Association for Information Science and Technology [verify authors and volume]. https://doi.org/10.1002/asi.23901

MediaWiki. (n.d.). Manual:Reverts. https://www.mediawiki.org/wiki/Manual:Reverts (accessed 28 October 2026)

Stvilia, B., Twidale, M. B., Smith, L. C., & Gasser, L. (2008). Information quality work organization in Wikipedia. Journal of the American Society for Information Science and Technology, 59(6), 983–1001. https://doi.org/10.1002/asi.20813

TeBlunthuis, N., Shaw, A., & Hill, B. M. (2018). Revisiting "The rise and decline" in a population of peer production projects. In Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems (Paper 355). ACM. https://doi.org/10.1145/3173574.3173929 [verify]

Tsvetkova, M., García-Gavilanes, R., Floridi, L., & Yasseri, T. (2017). Even good bots fight: The case of Wikipedia. PLOS ONE, 12(2), e0171774. https://doi.org/10.1371/journal.pone.0171774

Wang, P., & Li, X. (2019). Assessing the quality of information on Wikipedia: A deep-learning approach [verify authors]. Journal of the Association for Information Science and Technology. https://doi.org/10.1002/asi.24210

Wikimedia Foundation. (2026). MediaWiki history dumps (Version 2026-09) [Data set]. https://dumps.wikimedia.org/other/mediawiki_history/

Wikimedia Research. (n.d.). Research:Metrics/revert rate. Meta-Wiki. https://meta.wikimedia.org/wiki/Research:Metrics/revert_rate

[JASIST 2020] Loosen control without losing control: Formalization and decentralization within commons-based peer production. https://doi.org/10.1002/asi.24393 [verify authors]

[JASIST 2026] From divergence to convergence: How human-bot collaboration influences the evolution of collective knowledge in online knowledge communities. https://doi.org/10.1002/asi.70123 [verify authors]
