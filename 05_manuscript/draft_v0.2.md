# Which reverts count? Successor filtering and observation windows in Wikipedia revert-based metrics

<!-- Draft v0.2, 2026-11-08. JASIST Research Article. Numbers transcribed from 04_output/*.csv (cross_wiki_table, <wiki>_grid, <wiki>_confirmatory, h3_tag_coverage, robust_*). No number is typed from memory. Items in [brackets] are editorial placeholders to be resolved before submission. -->

## Abstract

Whether an edit was reverted is one of the most widely used indicators of information quality work in Wikipedia, feeding measures of editorial conflict, newcomer reception and editor retention. Its construct validity depends on two choices that analysts rarely examine: which later revisions may count as a revert (all, or only those made by humans rather than bots and semi-automated tools) and how long the edit is observed. This study audits both choices with a fixed-anchor design. The first edits of newcomers in seven language editions are held constant while the successor filter and the observation window are varied across three revert definitions available in the Wikimedia history dumps. Four editions were examined before registration; three were held out for confirmatory tests of four registered hypotheses. Excluding bot and tool reverts lowers the newcomer revert rate by an amount that tracks the local share of automated reverting, reorders editor success rankings substantially, and changes the estimated revert-to-retention odds ratio by a factor of 1.4 to 3. Most of this effect persists in an unbounded window, because humans rarely re-revert what a tool has already removed. The tag-based definition depends on the reverting editor's patrol status. A reporting checklist is proposed.

[Abstract: 200 words]

**Keywords:** information quality; measurement validity; Wikipedia; reverts; bots; peer production; preregistration

## Introduction

Information science has long insisted that quality is not observed but operationalized: an indicator of information quality is a construct, and its validity rests on decisions about what the indicator admits and excludes (Stvilia et al., 2008; Mai, 2013). In Wikipedia, the revert is the elementary indicator of quality work. When an editor restores a page to an earlier state, the intervening contribution has been judged, at least implicitly, to have lowered the quality of the article, and the judgement leaves a trace in the revision history. Researchers and the Wikimedia Foundation alike therefore use "was this edit reverted" as a proxy for quality control (Stvilia et al., 2008), for conflict (Kittur et al., 2007; Arazy et al., 2013), for the reception newcomers receive (Halfaker et al., 2011, 2013), for the balance of control and openness in peer production (Rozas & Huckle, 2021) and, most recently, for the division of labor between humans and bots in knowledge communities (Gao et al., 2026). Revert rates are outcome variables in onboarding experiments, predictors in retention models and descriptive statistics in cross-language comparisons (Jemielniak & Wilamowski, 2017; Formisano et al., 2026).

Yet "reverted" is not a property of an edit. It is a property of an edit together with two decisions the analyst makes about later events. The first is who may count as a reverter. Wikipedia's quality control is partly automated: anti-vandalism bots such as ClueBot NG on the English edition revert within seconds, and semi-automated tools such as rollback, Huggle and Twinkle let trusted editors revert with one click (Geiger & Halfaker, 2013). Published practice varies. Some studies count every revert regardless of who made it (Formisano et al., 2026); others separate reverts by bots and tools from manual ones and model them as distinct exposures (Halfaker et al., 2013; TeBlunthuis et al., 2018); the Wikimedia metric definition is silent on the question (Wikimedia Research, n.d.). The second decision is how long to watch. The Wikimedia Growth team counts an edit as reverted only within 48 hours, on the ground that almost all reverts happen by then (Warncke-Wang et al., 2023), whereas the history dumps flag a revert whenever it happens. These two decisions interact with a third, less visible one: the operational definition of a revert itself. The dumps flag "identity reverts" detected by content hashing over a page's entire history; the mwreverts library used in much published work searches only the last 15 revisions (Halfaker, n.d.); and since 2020 MediaWiki tags reverted revisions itself, but only under conditions that, as shown below, depend on who performed the revert.

The problem is an instance of what a companion study calls successor selection (Author, under review). An event-based metric asks whether a later event of some kind followed an earlier one. Holding the earlier events fixed, the metric can be moved by changing only which later events are allowed to count. That study showed, for software repository mining, that excluding one class of successor events moved an outcome metric by several percentage points with no change in the underlying behavior. Wikipedia reverts are a natural second case: the successor filter and the window are both routinely varied across studies, and the dumps allow the audit to be run at scale with the anchors held constant.

I therefore ask a measurement question rather than a behavioral one. Given the same newcomers and the same first edits, how far do the cohort revert rate, the editor-level success rate and the downstream revert-to-retention estimate move when the successor filter and the observation window change? Where does the sensitivity come from, and how much of it survives an unbounded window? Do the three revert definitions agree, and when they disagree, why? The audit is only possible with a revert definition computed over complete page histories, which the dumps provide and radius-limited libraries cannot, and a seven-edition comparison of this kind has not been reported. Four editions were analyzed before registration; the design, hypotheses and code were then registered on Zenodo (DOI 10.5281/zenodo.23720117), and three further editions were opened only after registration.

The contribution is threefold. First, across seven editions and 56 edition-year cells, the audit quantifies the dose-response relation between the local share of automated reverting and the sensitivity of revert metrics to the successor filter. Second, it shows that the sensitivity is mostly not a window artefact: because humans rarely re-revert what a bot or tool has already removed, the filter effect persists in the unbounded window. This qualifies a common reading of the natural experiment of Geiger and Halfaker (2013), not that study's own finding. Third, it documents from the MediaWiki source and the data that the tag-based definition depends on the reverting editor's patrol status, so the three definitions are not interchangeable even in principle. The study ends with a six-item reporting checklist.

## Background

### Reverts and newcomers

Halfaker et al. (2011) showed that being reverted reduces newcomers' subsequent activity, and Halfaker et al. (2013) argued that the rising rate at which newcomer contributions were rejected, often by bots and semi-automated tools, contributed to the decline of the English Wikipedia's editor population; they recorded whether a newcomer's first-session edits were reverted and, separately, whether the revert was made with a tool. TeBlunthuis et al. (2018) replicated the pattern across many peer production wikis with the same two-variable structure. Boté-Vericad (2026) audited four decisions involved in constructing newcomer cohorts from Wikimedia logs and reported that newcomers whose first edit was reverted had odds of leaving after one edit about 1.2 times those of other newcomers. That audit varied the cohort; the present one holds the cohort fixed and varies the successor.

### Bots, tools and the counterfactual

Geiger and Halfaker (2013) used the unplanned outage of ClueBot NG as a natural experiment. Without the bot, vandalism was still reverted, but more slowly: the proportion of damaging edits eventually reverted was unchanged while the time to revert lengthened. The result is sometimes read as licence to treat bot reverts as interchangeable with human reverts for final-state metrics, so that dropping them costs little in an unbounded window. That reading concerns a counterfactual in which the bot is absent. In observational data the bot is present, and excluding its reverts after the fact removes the event rather than the actor: the content is already gone, so no human needs to revert it. Whether the two readings diverge is an empirical question, answered below with a substitution rate. Geiger and Halfaker (2017) separately showed that redefining what counts as a bot-bot "fight" changed the conclusions of Tsvetkova et al. (2017), an early demonstration that operationalization choices can reverse findings in this domain.

### Revert definitions

The identity revert, an edit that returns a page to a byte-identical earlier state, is the most common definition (Kittur et al., 2007; Wikimedia Research, n.d.). Implementations differ. The mwreverts library detects identity reverts within a radius of 15 revisions by default (Halfaker, n.d.). The Wikimedia `mediawiki_history` dataset flags a revision as reverted if any later revision of the page restores a state that preceded it, with no radius and no time limit; this was verified in the source code of the Analytics Refinery (see Method). Since MediaWiki 1.36 (2020) the software tags reverted revisions with `mw-reverted` when it recognizes the reverting edit as an undo, a rollback or a manual revert within 15 revisions, but, where recent-changes patrolling is enabled, only once the reverting edit has been patrolled or was made by an autopatrolled user (MediaWiki, n.d.). Formisano et al. (2026) used a content-hash definition and listed the absence of a sensitivity analysis across definitions as a limitation. The present study treats the definition as a third axis of the audit.

## Method

### Design

The design holds a set of anchor edits fixed and varies only the set of later revisions allowed to count as reverts (Table 2 lists the symbols). Three successor filters are crossed with three observation windows. F0 counts all identity reverts. F1 does not count reverts made by bots. F2 does not count reverts made by bots or by semi-automated tools, identified by the `mw-rollback`, `huggle` and `twinkle` change tags where those tags exist in the edition. The registered windows are 24 hours, 7 days and unbounded, the last meaning the final state at the dump date; because the unbounded window is longer for older anchors, a fixed 180-day window, available for every anchor, is reported alongside it, together with 12-hour, 48-hour and 30-day windows.

Each filter is applied in two variants. In the strict variant, an anchor whose first revert was made by an excluded actor counts as not reverted; this reproduces the common preprocessing practice of dropping bot or tool reverts. The strict difference is an identity: p(F0, W) − p(F2 strict, W) equals p(F0, W) times the share of first reverts within W made by bots or tools. It is therefore reported descriptively, as the size of the practice's effect, and is not tested. In the replace variant, the anchor counts as reverted at the time of the first revert by a non-excluded actor, if any, recomputed from the page's revision history; this asks whether a human would have reverted the edit anyway, and when. Hypotheses are tested on the replace variant and on the contrast between the two.

**Table 2.** Symbols.

| Symbol | Meaning |
|---|---|
| F0, F1, F2 | Successor filters: all reverts; excluding bot reverts; excluding bot and tool reverts |
| strict, replace | Excluded revert counts as no revert; or the next non-excluded revert, if any, is used instead |
| W24h, W7d, W∞ | Observation windows (registered); W12h, W48h, W30d, W180d added for robustness |
| D1, D3r15, D2 | Revert definitions: dump flag (unbounded hash search); 15-revision radius; `mw-reverted` tag |
| Δ(F, W) | p(F0, W) − p(F, W), in percentage points, on the same anchors |
| R | Δ(F2 replace, W∞) / Δ(F2 replace, W24h): share of the filter effect that survives the unbounded window |
| S | 1 − Δ(F2 replace, W) / Δ(F2 strict, W): share of bot- or tool-reverted anchors that a human also reverted within W |
| OR | Odds ratio of retention (an edit on days 2 to 60) for reverted versus non-reverted anchors |

### Data

The data are the `mediawiki_history` dumps of version 2026-09, released monthly by the Wikimedia Foundation. Each row is a revision, page or user event with 78 tab-separated columns; the column order was taken from the refinery source because the published documentation listed an older 70-column schema (Endnote 1). Seven editions were processed. Korean (kowiki), French (frwiki), German (dewiki), Japanese (jawiki), Polish (plwiki) and Italian (itwiki) were downloaded in full. English (enwiki) was downloaded for January 2018 to September 2026 (105 monthly files, 643 million revision rows); the anchor definition below makes this sufficient. The exploratory editions (kowiki, enwiki, frwiki, dewiki) were analyzed before registration, as the registration document discloses. The confirmatory editions (jawiki, plwiki, itwiki) were processed by the same batch driver on 27 to 28 October 2026 but their output files were not opened until after the registered commit (7fcff3d, 28 October 2026, 04:39 UTC) and the Zenodo deposit; the batch log timestamps, the commit timestamps and the work log in the repository document the sequence.

### Cohort and anchors

The unit is a registered editor whose very first edit, in any namespace, was in the main (article) namespace; that edit is the anchor. The definition can be evaluated from a single dump row (`event_user_first_edit_timestamp`) and so does not require an edition's complete history. Editors whose first edit was elsewhere are excluded; they were 6.5 percent (jawiki) to 13.1 percent (plwiki) of first-time editors. Anonymous and temporary accounts are excluded, as are editors flagged as bots by current or historical username pattern or bot group. The primary cohort consists of self-created accounts with anchors dated 1 January 2019 to 31 March 2026, so that every anchor has at least 180 days of follow-up before the dump date. Table 1 gives the cohort sizes. Three cohort variants are reported for robustness: all registered accounts including those created automatically through unified login, anchors from 2021 onward, and the editor's second to fifth edits within 91 days as secondary anchors.

### Revert definitions and their verification

D1 is the dump's own `revision_is_identity_reverted` flag together with the identifier of, and the delay to, the first reverting revision. Reading the refinery source established that the flag is computed per page over the entire history by grouping revisions by content hash: the first occurrence of a hash is the base, later occurrences are reverts to that base, a revision is reverted if a revert whose base precedes it occurs later, and reverts to the same base do not count as reverting each other; no radius or time limit is applied (Endnote 1). I reimplemented this rule from the hashes in the dump and compared it with D1 on all kowiki anchors and on 60,000 sampled anchors in each other edition. Agreement on reverted status was complete in the five editions with full histories (0 or 1 disagreement each), 99.98 percent in kowiki and 99.9 percent in enwiki, where the downloaded period is partial. D3r15 applies the mwreverts convention of a 15-revision radius to the same recomputation. D2 is the `mw-reverted` tag on the anchor, usable for anchors from August 2020 onward.

### Bot and tool identification

A reverting editor is a bot if `event_user_is_bot_by` or its historical counterpart is non-empty; the dump sets these when the username matches the pattern `(?i)^.*bot([^a-z].*$|$)` or the account is in the bot group. The union of the two columns is used; the historical column alone and the current column alone are robustness variants. Tool reverts are revisions tagged `mw-rollback`, `huggle` or `twinkle`. Tag availability was checked per edition from the data: `mw-rollback` appears from December 2017 and `mw-undo` from January 2018 in all seven editions; `huggle` appears in enwiki and frwiki, but in enwiki it is almost absent in 2021 and 2022 (1,631 and 2,409 tagged revisions against 150,000 or more in adjacent years); `twinkle` appears only in enwiki and only from September 2020. F2 is therefore "excluding the tools identifiable by tag in that edition and period", and enwiki tool shares before September 2020 are understated. Undo is not treated as a tool, because it is the ordinary manual revert; including it is reported as a variant. Reverts made within 5 seconds by non-bot accounts, a check for unflagged bots, were 0.1 to 0.7 percent of non-bot reverts and concentrated in a few accounts; treating them as bots is a further variant.

### Outcomes

Three outcomes are computed in every cell. The cohort revert proportion p(F, W) is the share of anchors reverted under filter F within window W, with Wilson intervals. The editor success rate is one minus the reverted share of the editor's main-namespace edits in the first 90 days, for editors with at least ten such edits; rankings under F0 and F2 are compared by Spearman correlation and by the share of the bottom decile that changes membership. The downstream estimate is the odds ratio of retention, defined as at least one edit between day 2 and day 60 after the anchor, for reverted versus non-reverted anchors, the quantity reported by Boté-Vericad (2026) and by many retention studies; it is a descriptive association, not a causal effect, and the question asked of it is only how far the definition moves it.

Paired differences Δ(W) are computed on the same anchors with 2,000 bootstrap resamples; one editor contributes one primary anchor, so the resampling unit is the editor. Replace-variant quantities use a year-stratified random sample of 60,000 anchors per edition (all 47,633 in kowiki), because they require the page histories. As a model-based complement, the registered mixed model was replaced by a logistic regression of reverted status on filter, window and their interaction in the replace sample, with standard errors clustered by editor (Deviation 1 in the repository's deviation log).

### Registered hypotheses

Four hypotheses were registered before the confirmatory editions were opened and are tested within edition with Holm adjustment. H1 (window): in the replace variant the filter effect is larger in the 24-hour than in the unbounded window, Δ(24h) − Δ(∞) > 0, by a one-sided bootstrap bound, with R = Δ(∞)/Δ(24h) as effect size and R ≥ .75 read as "most of the effect survives". H2 (substitution): S, the share of anchors first reverted by a bot or tool that a human also reverted within 24 hours, is below .25. H3 (definitions): D2 and D3r15 agree on at least 95 percent of anchors, and more than half of the anchors that D1 marks reverted but D2 does not lie beyond the 15-revision radius. H4 (downstream): the retention odds ratio varies across the nine strict cells by a factor of at least 1.5. The thresholds .75, .25 and 1.5 were set from the exploratory editions and are stated in the registration. A negative control requires that in edition-year cells where bots make under 1 percent of first reverts, the bot-only filter moves the 24-hour rate by less than half a percentage point; no analogous control exists for the tool axis, because tool reverts are present in every edition-year once the tags exist.

### Transparency

Code, cell-level aggregates with at least 50 anchors, robustness tables, simulation outputs, figure data, the deviation log and the AI-assistance log are released on GitHub and archived on Zenodo [repository URL and release DOI at submission]. Editor-level derived data carry random identifiers; usernames of reverting accounts are not released. The study analyzes public edit histories and was not submitted for ethics review. Generative AI (Claude, Anthropic) was used to draft analysis code, documents and prose under the author's direction. All computations were performed by the released deterministic code on the unmodified dumps; the AI did not analyze or alter data; every claim about the dump format and the MediaWiki software was checked against the primary source; all figures in the text were transcribed from the output files; and the author reviewed and takes responsibility for the whole manuscript.

## Results

### Seven editions

Table 1 summarizes the editions. Newcomer first edits were reverted within 24 hours at rates from 14 percent (jawiki) to 37 percent (enwiki). Automated reverting differs sharply. Bots made 12 percent of first reverts in enwiki (median delay 8 seconds, consistent with ClueBot NG) and 4 percent in frwiki (Salebot, median 3 seconds), but 0.3 percent or less elsewhere, where the few bot reverts were slow maintenance edits. Tool reverts, mostly rollback, ranged from a quarter of first reverts in jawiki and frwiki to more than half in kowiki, itwiki and enwiki.

**Table 1.** Cohorts, automated reverting and the main audit quantities by edition. First-edit anchors of self-created accounts, 2019 to March 2026; replace-variant quantities from the 60,000-anchor samples (all anchors in kowiki). Role: expl. = exploratory, conf. = confirmatory. Tags = tool tags available: R = rollback, H = Huggle, T = Twinkle (from 2020-09). Δ = p(F0) − p(F2) in percentage points for the strict and replace variants. ρ = Spearman correlation between editor success rates under F0 and F2 (strict); "moved" = share of the bottom decile under one filter not in it under the other; OR range = retention odds ratios across the nine strict cells.

| Edition | Role | Anchors | Tags | p(F0, 24 h) | Bot share | Tool share | Δ strict 24 h | Δ replace 24 h | Δ replace ∞ | R | ρ | Moved | OR range |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| enwiki | expl. | 2,189,284 | R H T | .370 | .122 | .562 | 21.1 | 18.8 | 17.4 | .92 | .75 | 55% | 0.43–0.77 |
| itwiki | conf. | 135,400 | R | .342 | .000 | .525 | 17.9 | 15.9 | 13.4 | .84 | .80 | 48% | 0.40–0.71 |
| kowiki | expl. | 47,633 | R | .216 | .003 | .517 | 11.2 | 9.8 | 7.6 | .78 | .76 | 56% | 0.32–0.95 |
| dewiki | expl. | 236,903 | R | .256 | .001 | .410 | 10.5 | 9.6 | 8.8 | .92 | .90 | 31% | 0.52–0.84 |
| plwiki | conf. | 67,755 | R | .222 | .001 | .315 | 7.0 | 6.2 | 5.5 | .88 | .92 | 31% | 0.54–0.77 |
| frwiki | expl. | 346,938 | R H | .243 | .042 | .255 | 7.2 | 6.4 | 5.5 | .86 | .93 | 25% | 0.47–0.72 |
| jawiki | conf. | 223,045 | R | .140 | .001 | .247 | 3.5 | 3.0 | 2.7 | .92 | .94 | 28% | 0.36–0.66 |

### The successor filter moves every metric

Excluding bot and tool reverts lowered the 24-hour revert rate by 3.5 percentage points in jawiki and 21.1 points in enwiki in the strict variant, and by 3.0 to 18.8 points in the replace variant (Table 1, Figure 1). The bot-only filter mattered only where anti-vandalism bots operate: 4.5 points strict and 3.0 replace in enwiki, 1.0 and 0.6 in frwiki, and under 0.1 points elsewhere. Editor-level success rankings moved with the filter: the Spearman correlation between success rates under F0 and F2 ranged from .75 (enwiki) to .94 (jawiki), and 25 to 56 percent of the editors in the bottom decile under one filter were not in it under the other. The retention odds ratio ranged across the nine strict cells by a factor of 3.0 in kowiki, 1.8 in enwiki, jawiki and itwiki, 1.6 in dewiki and 1.4 to 1.5 in plwiki and frwiki; the lowest value was always a 24-hour cell with bot reverts counted (the all-reverts and no-bots cells coincide where bots are absent) and the highest the no-bots-no-tools, unbounded cell. Within single years in kowiki the association crossed one: in 2021 the all-reverts 24-hour odds ratio was 0.74 [0.62, 0.89] while the no-bots-no-tools unbounded odds ratio was 1.14 [0.98, 1.34], and the same crossing appears in 2020 and 2026.

### Most of the effect survives the unbounded window (H1)

In the strict variant Δ rose slightly with the window, because the base rate rises while the share of first reverts made by bots and tools is roughly constant (Figure 1, left). In the replace variant Δ fell with the window, as H1 predicts, but modestly (Figure 1, right). In the confirmatory editions Δ(24h) − Δ(∞) was 0.24 points in jawiki (one-sided 95 percent lower bound 0.19), 0.77 in plwiki (0.68) and 2.49 in itwiki (2.36), so H1 was supported in each; R was .92 [.90, .94], .88 [.86, .89] and .84 [.83, .85], above the registered .75. The exploratory editions gave R from .78 (kowiki) to .92 (enwiki, dewiki). The result is not sensitive to the registered boundaries: relative to the 24-hour cell, Δ at 12 and 48 hours was within 2 percent in every edition, and the fixed 180-day window retained .81 (kowiki) to .93 (dewiki) of the 24-hour effect, within .04 of the unbounded value in each edition (Supplementary Table S1). The logistic model gave the same picture: the filter-by-window interaction for F2 in the unbounded window was positive in every edition, from 0.07 (jawiki) to 0.31 (kowiki) on the log-odds scale with cluster-robust standard errors of at most 0.008 (Table S5).

[Figure 1 here]

**Figure 1.** Filter effect Δ = p(F0) − p(F2) by observation window, strict (left) and replace (right) variants, seven editions; solid lines are confirmatory editions. Error bars are 95 percent bootstrap intervals. In the strict variant Δ equals p(F0) times the bot-and-tool share of first reverts by construction.

### Why: humans rarely re-revert (H2)

The substitution rate S within 24 hours was .145 (one-sided 95 percent upper bound .157) in jawiki, .111 (.119) in plwiki and .114 (.119) in itwiki, supporting H2; the exploratory values were .09 to .12. Roughly nine in ten edits removed by a bot or tool were never reverted again by a person within a day, because there was nothing left to revert. Substitution grows with the window but stays a minority: at 7 days S was .12 to .21, and in the unbounded window .20 to .39, highest in kowiki (Table S1). The natural experiment of Geiger and Halfaker (2013) describes what humans do when the bot is absent; the substitution rate describes what they do when the bot has already acted.

Because the strict difference equals the revert rate times the bot-and-tool share, the relative replace difference, Δ/p(F0), should track that share minus S. Figure 2 shows that it does across the seven editions and 56 edition-year cells with at least 200 sampled anchors (Spearman ρ = .98 across cells; cells are point estimates). The relation is not carried by any one edition: leaving each edition out in turn gave ρ between .976 and .987, and within single editions, across their eight years, ρ ranged from .91 to 1.00. The points lie below the identity line by an amount equal to S. A parameter-grid simulation of an excluded fast actor, a human re-revert probability and a human delay reproduced the observed R of .78 to .92 only when the re-revert probability was between .1 and .2 with delays of days to a week; with no re-reverting R is 1, and with a re-revert probability of .5 and week-long delays R falls to about .5 (Table S7). The simulated actor stands for any excluded class of reverters, bots or tools alike.

[Figure 2 here]

**Figure 2.** Relative filter effect in the 24-hour window, Δ(F2 replace)/p(F0), against the bot-and-tool share of first reverts, for seven editions (large markers; circles confirmatory, squares exploratory) and 56 edition-year cells with at least 200 sampled anchors (open markers). The dotted line is the identity, which the strict variant attains by construction; the vertical distance below it is the substitution rate.

### Downstream estimates (H4)

The ratio of the largest to the smallest retention odds ratio across the nine strict cells was 1.84 [1.79, 1.88] in jawiki and 1.78 [1.72, 1.84] in itwiki, supporting H4, and 1.43 [1.38, 1.49] in plwiki, below the registered 1.5, so H4 held in two of three confirmatory editions; the exploratory frwiki value, 1.51, also sits at the threshold. In every edition the all-reverts, 24-hour definition produced the strongest negative association between being reverted and staying (odds ratios .32 to .54) and the no-bots-no-tools, unbounded definition the weakest (.66 to .95; Figure 3). Relative to the single point estimate of about 1.2 reported by Boté-Vericad (2026) for the odds of leaving, the definition chosen moves the estimate by more than sampling error does.

[Figure 3 here]

**Figure 3.** Range of the retention odds ratio (reverted versus not reverted) across the nine strict filter-by-window cells, by edition. The left end of each bar is the all-reverts, 24-hour cell and the right end the no-bots-no-tools, unbounded cell; whiskers are 95 percent intervals of the two cells, and the label is their ratio. In every edition these are the lowest and highest of the nine cells (in jawiki and kowiki the no-bots 24-hour cell is lower by less than .002). The nine cells per edition are shown in Figure S1.

### Definitions (H3): one clause rejected, and a patrol gate in the tag

D2 agreed with D3r15 on 98.6 percent of anchors in jawiki, 97.9 percent in plwiki and 95.4 percent in itwiki, satisfying the first clause of H3; the MediaWiki search radius for manual reverts is 15 revisions, so the agreement is expected. The second clause was rejected in all three editions. Among anchors that D1 marked reverted but D2 did not, only 42 percent (jawiki), 9 percent (plwiki) and 7 percent (itwiki) were reverted beyond the 15-revision radius, against 76 percent in the exploratory kowiki data on which the clause had been based. The hypothesis had generalized a feature of one edition.

A post-registration exploratory analysis asked where the remaining untagged anchors came from. They were identity-reverted within the radius, and the reverting edit itself carried an undo, rollback or manual-revert tag in more than 99 percent of cases, so the software had recognized the revert but had not tagged the reverted revision. The MediaWiki documentation explains the gap: the `mw-reverted` tag is applied by a deferred job that waits for the reverting edit to be approved, which on wikis with recent-changes patrolling means patrolled or made by an autopatrolled user, and "reverts that are not patrolled will not be marked with the reverted tag" (MediaWiki, n.d.). Figure 4 shows the share of within-radius identity reverts of anchors that carry no tag, against each edition's configuration in the Wikimedia settings repository (Endnote 2): 12.0 percent in itwiki and 8.8 percent in frwiki, the two editions with recent-changes patrolling enabled; 4.6 and 5.8 percent in dewiki and plwiki, which use FlaggedRevs; 2.4 to 4.2 percent in kowiki, enwiki and jawiki. Untagged cases had far higher shares of anonymous reverters than tagged ones (itwiki: 20 versus 1 percent). With seven editions the configuration pattern is descriptive and hypothesis-generating, but the mechanism is documented in the software. The tag definition is therefore not a revert definition alone; it is a revert definition conditioned on the reverting editor's trust status, and its coverage varies with local configuration.

[Figure 4 here]

**Figure 4.** Share of identity reverts within 15 revisions whose reverted anchor carries no `mw-reverted` tag, anchors from August 2020, by edition and by the edition's patrolling configuration. Post-registration exploratory analysis.

### Negative control and robustness

In all 24 edition-year cells of the confirmatory editions where bots made under 1 percent of first reverts, the bot-only filter moved the 24-hour rate by less than half a percentage point, as required. Normal approximations to the bootstrap tests gave Holm-adjusted one-sided p below .001 for H1 and H2 in every edition and for H4 wherever the point estimate exceeded 1.5 (Table S4).

The definition of the excluded class matters far more than how bots are identified (Table S2). Treating 5-second non-bot reverts as bots changed Δ by at most 0.05 points, and the historical and current bot flags gave the same result to two decimals. Adding undo to the tool set, by contrast, raised the strict Δ in the 24-hour window from 21.1 to 32.3 points in enwiki, from 7.2 to 18.9 in frwiki and from 3.5 to 9.2 in jawiki, a factor of 1.5 to 2.6; adding anonymous reverters to the excluded class raised it by 0.3 to 2.1 points. The cohort variants left the ordering of editions unchanged (Table S3): with all registered accounts, with anchors from 2021 onward and with the second to fifth edits as anchors, the relative 24-hour effect ran from .56 to .65 in enwiki down to .25 to .30 in jawiki. In kowiki, taking the first main-namespace edit rather than the first edit as anchor, the pilot definition, changed Δ by at most 0.08 points (Table S6). Restricting enwiki to anchors from 2021, when Twinkle reverts are tagged, raised its relative effect from .57 to .65, so Table 1 understates enwiki.

One edition-specific pattern deserves notice. From June 2023 to December 2024 kowiki received up to 1.9 times its median monthly number of first-edit anchors, and their 24-hour revert rate rose from about .15 to between .30 and .47 with tool reverts making up to 80 percent of first reverts (Figure S2). Outside those months kowiki's R was .87, in line with the other editions; within them it was .69. The low kowiki value in Table 1 therefore reflects a period of concentrated tool reverting that was later partly re-reverted by hand, not a stable property of the edition.

## Discussion

### What the audit shows

Holding newcomers and their first edits fixed, the choice of which reverts count moves the cohort revert rate by 3 to 21 percentage points, reorders editor success rankings enough to replace a quarter to a half of the bottom decile, and changes the estimated revert-to-retention odds ratio by a factor of 1.4 to 3. The size of the movement is predictable from one local quantity, the share of first reverts made by bots and tools, minus a substitution rate of about one in ten. The observation window changes much less: 78 to 92 percent of the filter effect remains when the window is unbounded, and 81 to 93 percent at a fixed 180 days. The intuition that final-state metrics are robust to how bot reverts are handled is not supported in observational data, and the reason is mechanical. A filter applied after the fact removes events, not actors; the natural experiment that motivated the intuition removed an actor.

### Implications for information quality measurement

For information science the result is a reminder that an indicator of quality work is defined by the population of workers it admits. Studies of quality control in Wikipedia (Stvilia et al., 2008; Jemielniak & Wilamowski, 2017) and of human-bot collaboration in knowledge communities (Gao et al., 2026) should state the successor population explicitly and, where automated reverting is substantial, report the strict and replace variants side by side. The substitution rate is itself informative: it says how often a community's human members confirm what its automated members did, and within 24 hours it was stable at 9 to 15 percent across editions that differ by an order of magnitude in size and in bot presence. The boundary of the excluded class is the largest lever of all: whether undo counts as a tool changes the filter effect by more than any other decision examined, so "tool-assisted" needs a definition, not a label.

The tag finding has a practical edge. The `mw-reverted` tag is the most convenient definition because it needs no recomputation, and it is used in Wikimedia's own dashboards. It undercounts reverts of newcomer edits by 2 to 12 percent depending on the edition's patrolling configuration, and the undercount is not random: it falls on reverts made by anonymous and non-autopatrolled editors. Analysts comparing editions by tag-based revert rates will attribute configuration differences to community differences unless they correct for this.

The mechanics generalize beyond Wikipedia. Any content-moderation indicator built from later events, a post removed, a comment flagged, a commit reverted, an answer deleted, is a successor metric, and platforms increasingly mix automated and human moderators. Excluding the automated actions after the fact does not recover what human moderators would have done; it removes the cases the automation handled, and the human moderators, having had nothing left to act on, appear to have acted less. The substitution rate and the paired strict-replace comparison are portable tools for auditing such indicators wherever the event logs allow both to be computed.

### A reporting checklist

Studies that use revert-based metrics should report: (1) the revert definition, naming the detection method and its radius or absence of one; (2) the successor population, stating which reverters are excluded and how bots and tools were identified, including which change tags were available in the period; (3) the observation window; (4) for any exclusion, both the strict and the replace variant, or the substitution rate; (5) the share of first reverts made by the excluded actors in the data, since it predicts the sensitivity; and (6) for tag-based definitions, the edition's patrolling and FlaggedRevs configuration.

### Limitations

The anchors are first edits of self-created accounts, the population for which revert metrics are most often computed; the audit does not cover established editors or the article-level revert rates used in conflict research, where the same mechanics apply but the shares may differ. A revert is treated as rejection, although some reverts undo an editor's own test edit or are later reversed themselves. The replace variant treats any later restoration of a pre-anchor state as a revert of the anchor, following the dump's own definition, so some replace-variant reverts are wider reverts that happened to span the anchor; editor-level success rates were compared for the strict variant only. Tool identification depends on change tags whose availability differs by edition and period, most visibly for Twinkle and Huggle in enwiki, so the tool axis is measured as "tool reverts identifiable by tag". The exploratory editions shaped the hypotheses and thresholds; the confirmatory editions were untouched until registration but share the pipeline. Only two editions have active anti-vandalism bots, so the bot-axis evidence rests on enwiki and frwiki; extending the audit to editions with other bots is the natural next step. Finally, the dump's revert flag is itself an operationalization, verified here against an independent recomputation but not against human judgement of whether a revert was warranted.

### Conclusion

A revert is a relation between an edit and a later editor, and the metric inherits whatever the analyst decides about that later editor. The audit shows that the decision is consequential, that its consequence is predictable from the local share of automated reverting, that it does not fade with a longer window, and that one of the three standard definitions silently encodes the reverting editor's trust status. None of this makes revert metrics unusable. It makes them reportable.

## Data availability statement

The data that support the findings of this study are openly available from the Wikimedia Foundation at https://dumps.wikimedia.org/other/mediawiki_history/ (version 2026-09). The analysis code, cell-level aggregates, robustness tables, figure data, logs and the preregistration (https://doi.org/10.5281/zenodo.23720117) are available at [GitHub URL] and archived at Zenodo [release DOI]. Derived editor-level data are not released because they could be re-identified from public edit histories; the code regenerates them from the dumps.

## Endnotes

1. Column order and the identity-revert rule were read from the Wikimedia Analytics Refinery source, files `MediawikiEvent.scala` (method `toTSVLine`, 78 fields) and `DenormalizedRevisionsBuilder.scala`, repository wikimedia/analytics-refinery-source, master branch as of 26 October 2026. Content hashes were reduced to 64-bit values for the recomputation; the collision probability at the page level is negligible.
2. Patrolling configuration was read from the Wikimedia configuration repository operations/mediawiki-config (`wmf-config/InitialiseSettings.php`, setting `wgUseRCPatrol`; `dblists/flaggedrevs.dblist`) on 28 October 2026. The tag job and its approval condition are described in the MediaWiki manual page Manual:Reverts and implemented in the core class `RevertedTagUpdateManager`.

## References

Arazy, O., Yeo, L., & Nov, O. (2013). Stay on the Wikipedia task: When task-related disagreements slip into personal and procedural conflicts. Journal of the American Society for Information Science and Technology, 64(8), 1634–1648. https://doi.org/10.1002/asi.22869

Author. (under review). Auditing successor selection in software repository mining: Evidence from filtering AI-attributed commits. [companion manuscript; details withheld for review]

Boté-Vericad, J.-J. (2026). Constructing newcomer cohorts from Wikimedia logs: Account creation type, deleted contributions, observation windows, and the behavioural threshold (Version 2). Zenodo. https://doi.org/10.5281/zenodo.23435553

Formisano, G., Hine, E., Juneja, P., Laitila, J., Novelli, C., Chiu, E., Dejanikus, E., Levin, M., Schroder, T., West, A., & Floridi, L. (2026). Editorial governance under pressure: Wikipedia's revert dynamics during the 2024 US election. Humanities and Social Sciences Communications, 13, Article 1459. https://doi.org/10.1057/s41599-026-06810-2

Gao, S., Qiu, J., Zhang, F., & Zhao, J. (2026). From divergence to convergence: How human–bot collaboration influences the evolution of collective knowledge in online knowledge communities. Journal of the Association for Information Science and Technology. Advance online publication. https://doi.org/10.1002/asi.70123

Geiger, R. S., & Halfaker, A. (2013). When the levee breaks: Without bots, what happens to Wikipedia's quality control processes? In Proceedings of the 9th International Symposium on Open Collaboration (WikiSym '13) (Article 6, pp. 1–6). ACM. https://doi.org/10.1145/2491055.2491061

Geiger, R. S., & Halfaker, A. (2017). Operationalizing conflict and cooperation between automated software agents in Wikipedia: A replication and expansion of "Even Good Bots Fight". Proceedings of the ACM on Human-Computer Interaction, 1(CSCW), Article 49, 1–33. https://doi.org/10.1145/3134684

Halfaker, A. (n.d.). mwreverts: Revert detection for MediaWiki [Computer software]. https://github.com/mediawiki-utilities/python-mwreverts

Halfaker, A., Geiger, R. S., Morgan, J. T., & Riedl, J. (2013). The rise and decline of an open collaboration system: How Wikipedia's reaction to popularity is causing its decline. American Behavioral Scientist, 57(5), 664–688. https://doi.org/10.1177/0002764212469365

Halfaker, A., Kittur, A., & Riedl, J. (2011). Don't bite the newbies: How reverts affect the quantity and quality of Wikipedia work. In Proceedings of the 7th International Symposium on Wikis and Open Collaboration (WikiSym '11) (pp. 163–172). ACM. https://doi.org/10.1145/2038558.2038585

Jemielniak, D., & Wilamowski, M. (2017). Cultural diversity of quality of information on Wikipedias. Journal of the Association for Information Science and Technology, 68(10), 2460–2470. https://doi.org/10.1002/asi.23901

Kittur, A., Suh, B., Pendleton, B. A., & Chi, E. H. (2007). He says, she says: Conflict and coordination in Wikipedia. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI '07) (pp. 453–462). ACM. https://doi.org/10.1145/1240624.1240698

Mai, J.-E. (2013). The quality and qualities of information. Journal of the American Society for Information Science and Technology, 64(4), 675–688. https://doi.org/10.1002/asi.22783

MediaWiki. (n.d.). Manual:Reverts. Retrieved October 28, 2026, from https://www.mediawiki.org/wiki/Manual:Reverts

Rozas, D., & Huckle, S. (2021). Loosen control without losing control: Formalization and decentralization within commons-based peer production. Journal of the Association for Information Science and Technology, 72(2), 204–223. https://doi.org/10.1002/asi.24393

Stvilia, B., Twidale, M. B., Smith, L. C., & Gasser, L. (2008). Information quality work organization in Wikipedia. Journal of the American Society for Information Science and Technology, 59(6), 983–1001. https://doi.org/10.1002/asi.20813

TeBlunthuis, N., Shaw, A., & Hill, B. M. (2018). Revisiting "The rise and decline" in a population of peer production projects. In Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems (Paper 355, pp. 1–7). ACM. https://doi.org/10.1145/3173574.3173929

Tsvetkova, M., García-Gavilanes, R., Floridi, L., & Yasseri, T. (2017). Even good bots fight: The case of Wikipedia. PLOS ONE, 12(2), Article e0171774. https://doi.org/10.1371/journal.pone.0171774


Warncke-Wang, M., Ho, R., Miller, M., & Johnson, I. (2023). Increasing participation in peer production communities with the Newcomer Homepage. Proceedings of the ACM on Human-Computer Interaction, 7(CSCW2), Article 280, 1–26. https://doi.org/10.1145/3610071

Wikimedia Foundation. (2026). MediaWiki history dumps (Version 2026-09) [Data set]. https://dumps.wikimedia.org/other/mediawiki_history/

Wikimedia Research. (n.d.). Research:Metrics/revert rate. Meta-Wiki. Retrieved October 28, 2026, from https://meta.wikimedia.org/wiki/Research:Metrics/revert_rate
