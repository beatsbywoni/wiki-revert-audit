# Which reverts count? Reverter populations, attribution rules and observation windows behind a Wikipedia indicator of information quality work

Hongwon Jeong

Center for Creative Convergence Education, Hanyang University ERICA, Ansan, Republic of Korea. ORCID 0009-0003-7908-7478. Email: beatsbywoni@hanyang.ac.kr

## Abstract

Whether an edit was reverted is a standard trace of information quality work in Wikipedia, read as quality judgment, conflict, rejection and human effort. It depends on seldom-reported choices: who counts as a reverter, how a later revision is attributed to an earlier edit, and how long the edit is observed. In a review of 45 studies, coded with language-model assistance and checked by the author, 35 do not say whether bot reverts are counted, 39 state no window, and none varies the reverter population as a sensitivity analysis. The choices are measured on the first edits of 3.2 million newcomers in seven language editions. Bots, one-click tools, other editors and the newcomers each make an edition-specific share of first reverts, and newcomers reverted by different classes differ in later activity. MediaWiki's revert tag omits most reverts by unregistered and newly registered editors in the two editions that patrol recent changes; measured with the tag, the gap between English and Italian revert rates grows from 3.6 to 7.4 points. Whether a filter's effect fades over longer windows depends on the attribution rule. Registered tests in three held-out editions concern a secondary question; the main analyses are exploratory. Reporting items follow.

**Keywords:** information quality; trace data; measurement validity; Wikipedia; reverts; bots; operationalization

## Introduction

When Stvilia et al. (2007) proposed a framework for information quality assessment in this journal, two of the measures they derived for Wikipedia articles were built from reverts. The number of reverts entered the measure of authority and reputation, and the median time to revert defined volatility. The article does not say how a revert was identified or whose reverts were counted. Nearly two decades later the revert is a standard trace of what Stvilia et al. (2008) called information quality work in Wikipedia, and the omission is common: of 45 studies reviewed below, none states all of the choices on which a revert count depends.

Because every revert is recorded, "was this edit reverted" serves as a general-purpose indicator. It is read as a judgment on the quality of an edit and as a label for training quality-prediction models (Trokhymovych et al., 2023), as a measure of conflict (Kittur et al., 2007; Yasseri et al., 2012), as the rejection a newcomer experiences (Halfaker et al., 2011, 2013), as an outcome in onboarding experiments (Warncke-Wang et al., 2023) and as evidence about how humans and automated agents share quality work (Geiger & Halfaker, 2013; Zheng et al., 2019). These uses presuppose different constructs, and information science has long held that what an indicator of quality means depends on the activity and context in which it is used (Stvilia et al., 2007; Mai, 2013). A judgment on an edit, a dispute, an experience of rejection and a quantity of human effort are not carried by the same reverts.

A revert is a relation between an edit and a later revision, so the analyst has to decide which later revisions count. The first decision is the reverter population. Wikipedia's quality work is done by bots, by trusted editors using one-click tools such as rollback, Huggle and Twinkle, by other registered and unregistered editors who use the undo function or edit by hand, and by authors who take back their own edits (Geiger & Ribes, 2010; Halfaker & Riedl, 2012; de Laat, 2015). The second is the attribution rule that links a later revision to the edit it undoes: the Wikimedia history dumps search a page's entire history, the mwreverts library (Halfaker, n.d.) searches the last 15 revisions, and since 2020 the MediaWiki software tags reverted revisions itself. The third is the observation window. Research on digital trace data has shown that such preprocessing decisions, often undocumented, can drive results (Howison et al., 2011; Hill & Shaw, 2014; Geiger & Halfaker, 2017; Sen et al., 2021), and measurement theory asks that an operationalization be justified against the construct it claims (Jacobs & Wallach, 2021). For reverts, the accuracy of detection has been examined (Ekstrand & Riedl, 2009; Flöck et al., 2012), and Geiger and Halfaker (2017) showed for reverts between bots that the operationalization changes the conclusion. That reverters are of different kinds is also established for the English edition (Halfaker & Riedl, 2012; Halfaker et al., 2013). What has not been measured is how far the indicator, and conclusions drawn from it, move with the three decisions across language editions and attribution rules.

This study asks how the three decisions are handled in published work; how far, with the measured edits held fixed, the newcomer revert rate, editor rankings and the association between being reverted and staying move when the decisions change; and whether reverts by different classes of reverter are the same kind of event. The first question is answered with a structured review of practice, the others with a fixed-edit audit of 3.2 million newcomer first edits in seven language editions, in the spirit of a multiverse or specification-curve analysis (Steegen et al., 2016; Simonsohn et al., 2020).

The contribution is a specification of what this indicator of quality work indicates. One finding concerns a documented behavior of the software whose extent has not, to my knowledge, been measured (Endnote 2): its revert tag records a revert only when the reverting edit is trusted or patrolled, so its coverage depends on who reverted and on the edition's patrolling regime, enough to double a cross-edition difference. Two are measured compositions: the shares of reverts made by each class of reverter in each edition, and the differing later activity of the newcomers each class reverts. A fourth concerns method: whether excluding a class of reverts matters less with a longer window depends on the attribution rule. The paper ends with proposed reporting items tied to the construct an analyst intends to measure.

## Conceptual background

### One trace, four constructs

If quality is relative to activity and context (Stvilia et al., 2007; Mai, 2013), a trace produced by quality work is not itself a quality score. The constructs for which the revert is used were coded for every study in the review reported in the next section (Table 1); four account for 38 of 45 studies. As a *quality judgment on the edit*, every revert that removes the edit counts, whoever made it, though a self-revert is a different judgment from a rejection by others. As *conflict* between editors or over an article (Kittur et al., 2007; Yasseri et al., 2012), reverts by bots and reverts of vandalism are not disputes, and mutual or repeated reverts matter more than single ones. As *the contributor's experience of rejection*, in research on newcomer socialization and retention (Choi et al., 2010; Halfaker et al., 2013; Morgan & Halfaker, 2018), self-reverts should not count and the mode of rejection matters. As *human quality-work effort*, in studies of how communities and algorithms share governance (Müller-Birn et al., 2013; Zheng et al., 2019), bot reverts are a separate category and the status of one-click tools has to be decided, because a tool revert is a human judgment delivered with machine assistance (Halfaker & Riedl, 2012).

**Table 1.** Constructs a revert is used to indicate in 45 reviewed studies, the reverter population each implies, and how many studies using the construct leave the relevant choices unstated. Seven studies use the revert for other purposes. Quality judgment covers the quality of an edit or, as in Stvilia et al. (2007), of an article.

| Construct | Studies | Reverter population implied | No statement on bot, tool or self-reverts | No observation window stated |
|---|---|---|---|---|
| Quality judgment on the edit | 11 | All reverters; self-reverts reported separately | 6 | 8 |
| Conflict | 15 | Human reverters other than the author; vandalism reverts set apart | 6 | 14 |
| Contributor's experience of rejection | 9 | Others only; mode (bot, tool, manual) distinguished | 3 | 7 |
| Human quality-work effort | 3 | Humans; bots separate; tools decided explicitly | 1 | 3 |

### Detecting and attributing reverts

The identity revert, an edit that returns a page to a byte-identical earlier state, is the standard operationalization (Kittur et al., 2007). Two implementations dominate. The mwreverts library searches a window of 15 revisions by default. The `mediawiki_history` dataset (Wikimedia Foundation, 2026) instead marks a revision as reverted if any later revision of the page restores a state that preceded it, with no radius and no time limit. A third source is the `mw-reverted` change tag, enabled on all Wikimedia wikis on 15 September 2020 (Endnote 2), which the software applies when it recognizes the reverting edit as an undo, a rollback or a manual revert within 15 revisions.

The rules differ in what they attribute. Under the unbounded rule, an edit removed once can be "reverted" again years later by any revision that returns the page to a still earlier state.

### Automation and edition differences

Language editions differ in institutions that shape reverting: some hold edits by new users for review through FlaggedRevs (Tran et al., 2022), some patrol recent changes, the rollback right is granted on different terms, and norms of interaction differ (Hara et al., 2010). An indicator compared across editions inherits these differences. Nor does discarding a bot's reverts after the fact show what humans would have done without the bot, a question that needs evidence such as the bot outage studied by Geiger and Halfaker (2013).

## How reverts are operationalized in published work

### Procedure

I reviewed empirical studies and official Wikimedia analyses from 2005 to 2026 in which a revert-based measure is an outcome, an exposure, a label, a conflict indicator or a key descriptive quantity. The search had two stages. The first followed the citation networks of the methodological works cited above and keyword searches of OpenAlex, and yielded 34 studies (for one, Priedhorsky et al., 2007, the codes rest on an extract). Because that stage favored computing venues, the second searched OpenAlex for information science and neighboring journals (1,169 records, 79 assessed) and screened the full text of 242 articles in this journal that mention Wikipedia and reverting. With institutional access, 45 of 54 candidates first available only as abstracts were read in full. Eleven studies were added in this stage, six of them from this journal, the Journal of Documentation and First Monday; nine candidates, none in an information science journal, could not be read. The set is a structured sample of 45 studies (26 published before 2019, 19 since; 26 on the English edition only), not a census.

Each study was coded for detection rule, treatment of reverts made by bots, by one-click tools and by the author, observation window, sensitivity analysis over these choices, and the construct the revert stands for. Codes describe what the article and its supplement report for the main analysis: a choice is coded as stated only if a passage establishes it (recorded in Table S1), and settings found only in released code, in a cited procedure or in a sub-analysis are noted but not coded as reported. First-pass coding was produced by a language model (Claude; versions in the AI assistance log) and re-checked in a second model pass; a separate model instance coding a random 13 studies blind agreed on 72 of 78 judgments (κ = 1.00 for the three reverter choices, .78 for detection, .61 for window, .59 for sensitivity analysis). I then checked the codes of the 41 studies coded to that point against the source texts. The check corrected one misreading and sharpened the rules, which changed 16 further codes in 13 studies: "eventually reverted" is not a stated window, a detection scan range is not an observation window, a rule of a sub-analysis is not the study's rule, and a definition that requires another editor counts as excluding self-reverts. The four studies added last were coded from the full text under the final rules. The counts of unstated choices remain judgments about absence and are best read as orders of magnitude.

### Findings

**Table 2.** Reporting of revert operationalization in 45 studies, 2005 to 2026.

| Choice | Stated | Not stated |
|---|---|---|
| Detection rule | 34 (identity of content, by hash 15 or by definition 5; identity plus edit summaries 3; dump field 3; rollback or undo actions only 2; other 6) | 11 |
| Search radius, in the 23 studies using an identity rule | 1 (3 more cite a library without reporting its setting) | 19 |
| Reverts made by bots | 10 (modeled separately 6; excluded 2; counted 2) | 35 |
| Reverts made with one-click tools | 5 (counted 3; modeled separately 2) | 40 |
| Self-reverts | 16 (excluded, 6 of them by definition) | 29 |
| Observation window | 6 (time-bounded 5; revision-bounded 1) | 39 |
| Sensitivity analysis over any revert choice | 8 (full 2; partial 6) | 37 |
| Sensitivity analysis over the reverter population | 0 | 45 |

Eleven studies do not state how reverts were detected, and of the 23 that use an identity rule one reports a search radius (Table 2). Thirty-five do not say whether reverts made by bots are counted. Where bots are mentioned it is usually as authors: thirteen studies remove bot-authored edits from the sample, and eleven of these are silent on reverts that bots perform. Two studies exclude bot reverts from the measure (West et al., 2010; Tsvetkova et al., 2016), six treat the type of reverter as a variable or focus on it, and forty say nothing about one-click tools. Thirty-nine studies state no observation window; of the five with a time bound, three use 48 hours. Twenty-one studies state nothing about bot, tool or self-reverts, no study reports all the choices together, and none varies the reverter population as a sensitivity analysis. The six studies from information science venues follow the pattern: five say nothing on bot reverts and five state no window.

Two features of this record shape the audit. First, the exclusions actually made are of self-reverts, commonly, and of bot reverts, rarely; no study excludes tool-assisted reverts, although two model them separately (Geiger & Halfaker, 2013; Halfaker et al., 2013). The audit therefore sizes every reverter class and treats tool exclusion as hypothetical. Second, one study builds its indicator on the software's revert tags (Ariel, 2026), and none notes the conditions under which the `mw-reverted` tag is applied.

## Method

### Data and cohort

The data are the `mediawiki_history` dumps of version 2026-09 (Wikimedia Foundation, 2026). Each row is a revision, page or user event; the column order was taken from the source code of the Wikimedia Analytics Refinery (Endnote 1). Seven editions were processed: English from January 2018 to September 2026 (so reverts to states older than 2018 are not detected) and the complete histories of Italian, Korean, German, Polish, French and Japanese.

The unit is a registered editor whose first edit in any namespace was made in the article namespace; that edit is the measured edit. Editors whose first edit was elsewhere (6.5 to 13.1 percent of first-time editors) are outside the cohort, as are unregistered and temporary accounts and accounts flagged as bots. The primary cohort is self-created accounts whose first edit dates from 1 January 2019 to 31 March 2026, leaving at least 180 days of follow-up: 3,246,958 editors (Table 3). One edit per editor makes the editor the unit of inference. First edits that create a page can be removed only by deletion; their share is reported (Table S2).

### Attribution rules

Three rules are compared. The *dump rule* is the `revision_is_identity_reverted` flag with the identifier of and delay to the first reverting revision. The refinery source shows that the flag groups a page's revisions by content hash over its entire history; the first occurrence of a hash is a base, later occurrences are reverts to that base, and a revision is reverted if a later revert has a base that precedes it (Endnote 1). I reimplemented the rule from the hashes on all Korean first edits and on year-stratified samples of 60,000 first edits in each other edition; status agreed with the flag on at least 99.9 percent of edits in every edition. The *radius rule* applies the mwreverts convention of 15 revisions to the same recomputation. The *tag rule* is the `mw-reverted` tag on the measured edit.

### Reverter classes

The first revert of each measured edit is assigned to one class, in this order: *bot* (the dump's bot flags, current or historical); *one-click tool* (the reverting revision carries the `mw-rollback`, `huggle` or `twinkle` change tag); *self* (the reverting account is the author); *unregistered* (no account, including temporary accounts where an edition has introduced them); and *other manual* (any other registered account, including those using the undo function). The tool class is defined by tags, not by a common institution: the rollback right is appointed in some editions and comes with the reviewer status of FlaggedRevs in German and Polish. Tag availability differs: rollback is tagged in all seven editions throughout; Huggle is tagged in English and French and Twinkle only in English, from September 2020 (Table S9). In five editions the tool class is therefore the exercise of the rollback right; tags of other tools are counted in Table S3. Class shares are reported with the number of reverting accounts and with intervals that resample those accounts.

### Quantities

For a window W, p(W) is the share of measured edits reverted within W. Excluding a class in the *strict* sense recodes edits first reverted by that class as not reverted; the change in p equals the class's share of first reverts times p, an identity. The *replace* variant, the object of the registered tests, instead looks for the first later revert by a non-excluded reverter. To learn what such later reverts are, I record for every first revert the next manual revert of the same edit by a registered third party (an account that is neither the author nor the first reverter), by class of the first reverter and under both rules, with the clock started at the first revert, and compare bot and tool first reverts with manual first reverts by registered editors, also within strata of the page's revision count before the measured edit.

Downstream quantities are the share of editors who edit again between day 2 and day 60, by class of first revert within 24 hours, with accounts blocked within 60 days separated; the rank agreement of editor-level success rates (one minus the reverted share of an editor's article edits in the first 90 days, for editors with at least ten) with and without tool and bot reverts; and tag coverage, the share of reverts found by the radius rule whose measured edit carries no `mw-reverted` tag, for first edits from October 2020, by class of reverter, by whether the reverting account held a user group carrying the autopatrol right at the time, and by the edition's patrolling regime (Endnote 2). User groups and block events were extracted afterwards by streaming the same dump version. Intervals are Wilson intervals for shares and percentile intervals from 2,000 bootstrap resamples of editors for ratios; because reverts cluster in reverting accounts, key quantities are recomputed with resampling of those accounts (Table S10). Quantities that need page histories use the 60,000-edit samples (all 47,629 Korean first edits with a usable history). Cells with fewer than 50 edits are not reported, as registered.

### Registration and its limits

Design, hypotheses and code were registered on Zenodo (https://doi.org/10.5281/zenodo.23720117) after English, Korean, French and German had been analyzed and before the outputs for Japanese, Polish and Italian were opened. It is a hold-out replication with thresholds set from the exploratory editions, not a blind preregistration: the held-out editions had already been processed, and that their outputs were unopened is documented only by my own logs (Section S1 of the supplement, which lists all deviations). Four hypotheses were registered. H1: the replace effect of excluding bots and tools is larger within 24 hours than in the unbounded window (ratio R of unbounded to 24-hour effect below 1, with R of .75 or more read as most of the effect persisting). H2: the share of bot- or tool-reverted edits later reverted by a human within 24 hours is below .25. H3, a descriptive criterion: the tag and radius rules agree on at least 95 percent of edits, and more than half of the edits the dump rule marks reverted but the tag does not lie beyond the radius. H4: the odds ratio of retention for reverted versus non-reverted edits varies by a factor of at least 1.5 across nine filter-by-window cells. Decisions use one-sided 95 percent bootstrap bounds with Holm adjustment within edition (registered over H1 to H4; applied to H1, H2 and H4 because H3 has no test). All four outcomes are reported; a registered negative control and a simulation were withdrawn as uninformative (Section S1). Every other analysis was designed after the first results and is exploratory in all seven editions; tables and figures are labeled accordingly.

### Transparency

Code, cell-level aggregates, the review table, figure data, logs and the deviation log are public (https://github.com/beatsbywoni/wiki-revert-audit; archived release, Jeong, 2026). Editor-level files are not released, a recorded departure from the registration, and usernames of reverting accounts are not retained in outputs. The study uses public edit histories, reports aggregates only and involved no interaction with editors; it was not submitted for ethics review on that ground. Generative AI (Claude, Anthropic; model versions and dated tasks are in the public AI assistance log) was used for three tasks: drafting analysis code, drafting and editing prose, and first-pass and reliability coding of the literature review as described above. Model agents were also used to critique drafts before submission. The model was not used to generate, alter or impute data; every number of the audit is produced by the released deterministic code from unmodified dumps, and the review tallies are counts over the released coding table. I specified the design, made the analytic decisions, checked the code against the primary sources cited and against the independent recomputation reported above, and am responsible for every statement. The study received no funding, and I declare no competing interests.

## Results

### What a revert rate is made of

Within 24 hours, 14.0 percent (Japanese) to 37.0 percent (English) of newcomer first edits were reverted (Table 3, Figure 1). Outside English, 9 to 20 percent of first edits create a page and cannot be reverted in this sense; among edits to existing pages the rate is 15.5 to 40.3 percent (Table S2). The first revert came from a bot in 12.2 percent of cases in English and 4.2 percent in French, in each case almost entirely from a single bot account, and in at most 0.3 percent elsewhere. One-click tools made 24.7 percent (Japanese) to 52.5 percent (Italian) of first reverts. Manual reverts by other registered editors made up 28.9 to 64.3 percent, 49 to 78 percent of them through the undo function; unregistered editors and the newcomers themselves made the rest.

**Table 3.** Cohorts and composition of first reverts within 24 hours (dump rule, first edits of self-created accounts, 2019 to March 2026). Shares are of first reverts; the strict effect of excluding a class, in percentage points, is its share times p. Tool accounts: accounts that made the tool reverts, with the share of the most active. Editions marked * were held out for registered tests. Composition is exploratory.

| Edition | First edits | p(24 h) | Bot | One-click tool | Other manual | Unregistered | Self | Tool accounts (top share) |
|---|---|---|---|---|---|---|---|---|
| English | 2,189,284 | .370 | .122 | .448 | .364 | .023 | .044 | 6,596 (.06) |
| Italian* | 135,400 | .342 | .000 | .525 | .407 | .024 | .044 | 201 (.06) |
| Korean | 47,633 | .216 | .003 | .516 | .289 | .096 | .096 | 93 (.19) |
| German | 236,903 | .256 | .001 | .410 | .545 | .017 | .027 | 1,286 (.09) |
| Polish* | 67,755 | .222 | .001 | .315 | .616 | .030 | .038 | 341 (.11) |
| French | 346,938 | .243 | .042 | .255 | .643 | .012 | .047 | 316 (.12) |
| Japanese* | 223,045 | .140 | .001 | .247 | .558 | .080 | .114 | 103 (.23) |

[Figure 1 here]

**Figure 1.** Newcomer first edits reverted within 24 hours, by who made the first revert, as a percentage of all first edits. Segment widths are the strict effects of excluding each class. Exploratory.

The practices found in the literature thus have small, edition-specific effects. Excluding bot reverts lowers the 24-hour rate by 4.5 points in English, 1.0 in French and less than 0.1 elsewhere. Excluding self-reverts lowers it by 0.7 (German) to 2.1 points (Korean). Excluding one-click tools would lower it by 3.4 (Japanese) to 17.9 points (Italian).

Two qualifications apply to the tool share. Outside English and German it is produced by few people: 93 accounts made the tool reverts in Korean and 103 in Japanese, the most active alone 19 and 23 percent, and intervals that resample reverting accounts are correspondingly wide (Korean .35 to .62, Japanese .15 to .34; Table S2). And it is a lower bound where other tools are tagged: reverts carrying only the tags of LiveRC in French, or of RedWarn, Ultraviolet, STiki and an anti-vandalism script in English, would add 8.5 and 3.9 points to the tool share (Table S3).

### Later reverts and the window

If a class of reverts is excluded, does a later revert by someone else take its place? Under the registered definition, the share of bot- or tool-reverted first edits with a later non-bot, non-tool revert within 24 hours (H2, threshold .25) was .145 in Japanese (one-sided 95 percent upper bound .157), .111 in Polish (.119) and .114 in Italian (.119), supporting H2 in the three held-out editions. That definition counted any later reverter, including the author and the first reverter. Restricted to registered third parties, and with the 24 hours counted from the first revert, a manual revert followed 5.7 to 9.7 percent of bot and tool first reverts under the dump rule and 0.9 to 2.9 percent under the radius rule (Table 4, Figure 2).

**Table 4.** Follow-up manual reverts by a registered third party within 24 hours of the first revert, by who made the first revert, and the window ratio R, under two attribution rules. Manual: first revert by another registered editor without a tool. Denominators are all first reverts by the class shown. R: replace effect of excluding bots and tools in the unbounded window divided by the effect within 24 hours, with 95 percent bootstrap intervals. Follow-up shares are exploratory; R under the dump rule is the effect size of the registered H1.

| Edition | Dump rule: after bot or tool | Dump rule: after manual | Radius rule: after bot or tool | Radius rule: after manual | R, dump rule | R, radius rule |
|---|---|---|---|---|---|---|
| English | .077 | .066 | .010 | .006 | .92 [.91, .93] | 1.05 [1.04, 1.05] |
| Italian* | .079 | .082 | .013 | .010 | .84 [.83, .85] | 1.02 [1.02, 1.03] |
| Korean | .069 | .068 | .017 | .010 | .77 [.76, .79] | 1.07 [1.06, 1.08] |
| German | .057 | .041 | .009 | .003 | .92 [.91, .93] | 1.04 [1.03, 1.04] |
| Polish* | .060 | .035 | .013 | .002 | .88 [.86, .89] | 1.07 [1.06, 1.08] |
| French | .090 | .070 | .013 | .005 | .86 [.84, .87] | 1.04 [1.03, 1.05] |
| Japanese* | .097 | .091 | .029 | .013 | .92 [.90, .94] | 1.05 [1.04, 1.06] |

[Figure 2 here]

**Figure 2.** First edits with a later manual revert by a registered third party, by who made the first revert, under the dump rule (top) and the 15-revision radius rule (bottom), within 24 hours of the first revert (left) and unbounded (right). Bars are 95 percent Wilson intervals. Exploratory.

Such follow-up is somewhat more frequent after bot and tool reverts than after manual ones: under the dump rule in English, German, Polish and French, with no difference in Italian, Korean and Japanese, and under the radius rule in all seven editions, on small bases. The pattern holds within strata of the page's prior revision count (Table S4). What the data bound is the yield of the replace variant. An analyst who drops bot and tool reverts and looks for the next human revert recovers 9 to 15 percent of the dropped events within a day under the registered definition and 6 to 10 percent when only registered third parties count, and under the dump rule mostly later reverts that reach back past the measured edit or undo unrelated edits, which that rule attributes to every revision they span; only 1.0 to 12.2 percent of bot- or tool-reverted first edits were reverted again after their content had been reinstated (Table S4).

The registered H1 predicted that the replace effect of excluding bots and tools is larger within 24 hours than in the unbounded window. Under the dump rule it was, in all three held-out editions: the difference was 0.24 points in Japanese (one-sided 95 percent lower bound 0.19), 0.77 in Polish (0.68) and 2.49 in Italian (2.36), with R of .92, .88 and .84, all above the registered .75 (Table 4). Under the radius rule R is 1.02 to 1.07 in all seven editions, with every interval above 1. The reversal is close to arithmetic. A longer window adds first reverts by bots and tools and adds follow-up; under the radius rule follow-up is rare, so the effect grows, while under the dump rule deep reverts accumulate and the effect shrinks. H1 is thus supported as registered, with intervals that also hold when reverting accounts are resampled (Table S10); it concerns a filter that published studies do not use and describes the unbounded rule more than it describes reverting.

### Reverts by different classes reach different newcomers

Newcomers whose first edit was not reverted within 24 hours edited again on days 2 to 60 in 17.1 to 26.6 percent of cases (Figure 3). Of those reverted with a one-click tool, 3.5 to 8.6 percent did; of those reverted manually by another registered editor, 10.4 to 14.2 percent; of those who reverted themselves, 11.3 to 19.9 percent. As odds ratios against non-reverted newcomers, tool reverts range from 0.10 to 0.38, manual reverts by others from 0.41 to 0.71 and self-reverts from 0.55 to 0.68 (Table S5). Blocking does not produce the contrast: with accounts blocked within 60 days removed, the odds ratios are 0.09 to 0.38 for tool reverts and 0.40 to 0.70 for manual ones. These are associations between groups of newcomers, not effects of the mode of reverting: tools are aimed at vandalism, and intent, repeat accounts, accompanying warnings and first-day activity are not controlled. The point for measurement is that a single "reverted" category averages over events whose relation to the contributor's later activity differs by a factor of 1.4 to 4 in odds, in proportions that vary by edition.

[Figure 3 here]

**Figure 3.** Newcomers who edited again on days 2 to 60, by who made the first revert of their first edit within 24 hours. Bars are 95 percent Wilson intervals; the grey line spans the classes within an edition. Exploratory.

This is what moves downstream estimates when the reverter population changes. The registered H4 compared the odds ratio of retention across nine cells (all reverts, without bots, without bots and tools; 24 hours, 7 days, unbounded). The ratio of the largest to the smallest was 1.84 [1.79, 1.89] in Japanese and 1.78 [1.72, 1.85] in Italian, at or above the registered point value of 1.5, and 1.43 [1.37, 1.49] in Polish, below it; H4 is met in two of three held-out editions. The exploratory editions gave 1.51 to 1.78, and 3.01 in Korean. The movement is compositional: recoding tool-reverted newcomers, the group least likely to return, as not reverted raises the odds ratio. Across the three 24-hour cells alone, which do not overlap the outcome period, the ratio is 1.30 to 1.50 (1.93 in Korean). Editor-level rankings shift for the same reason: among editors with at least ten article edits in 90 days, the rank correlation between success rates with and without bot and tool reverts was .75 to .93, and 25 to 56 percent of the lowest decile changed membership.

### The tag records a revert only when the reverter is trusted or patrolled

The tag and radius rules agreed on 98.6 percent of first edits in Japanese, 97.9 in Polish and 95.4 in Italian, meeting the first clause of H3. The second clause was rejected in all three: of the edits that the dump rule marked reverted and the tag did not, 42, 9 and 7 percent lay beyond the radius, against the registered expectation of more than half. The registered window began before the tag was enabled everywhere; from October 2020 the shares are 75 percent in Japanese, where the clause would be met, and 13 and 9 percent in Polish and Italian (Table S10).

The exploratory follow-up locates the gap. MediaWiki applies the tag only once the reverting edit counts as approved: at once if the reverter holds the autopatrol right (exemption from patrol), and otherwise when someone patrols the edit, so that, in the words of the manual, "reverts that are not patrolled will not be marked with the reverted tag" (MediaWiki, n.d.; Endnote 2). For first edits from October 2020, the share of radius-rule reverts whose measured edit carries no tag was 0.3 to 1.0 percent in English, Korean and Japanese, which do not patrol edits; 2.4 and 3.9 percent in German and Polish, which use FlaggedRevs; and 9.6 and 7.0 percent in Italian and French, which patrol recent changes (Figure 4). In Italian and French, 79 and 71 percent of reverts by unregistered editors and 71 and 73 percent of newcomers' self-reverts were untagged, against under 1 percent of tool reverts. In German and Polish the figures were 23 and 29 percent for unregistered reverters and 13 percent for self-reverts, the latter not explained by the documented rule, under which a self-revert to a reviewed version is approved automatically.

The user groups held by the reverting account at the time of the revert test the mechanism directly (Table S6). Where the reverter held a group that carries the autopatrol right, 0.2 to 2.2 percent of reverts were untagged in every edition. Where a registered reverter held no group, 70 percent were untagged in Italian, 14 and 16 percent in German and Polish, and about 1 percent in English, Korean and Japanese. French looked like an exception, with 12 percent, and resolves into the rule: that edition grants the autopatrolled status automatically at 500 edits and 90 days without recording a group (Endnote 2), and among manual reverters with no recorded group 60 to 70 percent of reverts were untagged below 500 edits, 3.4 percent between 500 and 4,999 and 0.1 percent above.

[Figure 4 here]

**Figure 4.** Reverts found by the 15-revision radius rule whose reverted edit carries no `mw-reverted` tag, first edits from October 2020, by who made the revert and by the edition's patrolling regime. Bars are 95 percent Wilson intervals. Exploratory.

The consequence for a comparison can be computed directly. For first edits from October 2020, the share reverted under the radius rule is 39.5 percent in English and 35.9 percent in Italian, a difference of 3.6 points; measured with the tag it is 40.1 and 32.7 percent, a difference of 7.4 points (change 3.8 points, 95 percent bootstrap interval 3.6 to 4.0; Table S6). The French gap to English grows from 13.7 to 15.8 points, the German and Polish gaps by 1.1 and 1.5, and the Korean and Japanese gaps do not change. The association of being reverted with retention is unaffected (odds ratios within .02 of each other under the two rules), because the missing reverts are few relative to all reverts; what moves is any quantity that depends on who reverted. The example is a favorable case, a small gap between two large editions; 0.6 of the 3.8 points comes from English, where the tag marks slightly more edits than the radius rule; and coverage is a snapshot, since tags arrive when a revert is patrolled.

## Discussion

### What the indicator indicates

For each construct the audit shows what the unreported choices contain. As a *quality judgment on the edit*, the revert flag performs as intended only in its most inclusive form, and even then 3 to 11 percent of the judgments are the authors' own. As *conflict*, it needs its largest component set apart: a quarter to a half of first reverts are one-click responses by holders of the rollback right. As *the contributor's experience of rejection*, it mixes encounters that differ in what follows them, and the edition determines which is typical: a tool in Italian, Korean and English, a manual revert in German, Polish, French and Japanese. As *human quality-work effort*, it needs the least adjustment where it is most often adjusted, since bots make a material share of first reverts only in English and French, while the unsettled question, whether a rollback is human work, concerns a quarter to a half of reverts everywhere.

That bots, tools and other editors revert differently, and that tool reverts go with lower retention, was known for English (Halfaker & Riedl, 2012; Geiger & Halfaker, 2013; Halfaker et al., 2013), and that operational choices can reverse a conclusion about reverts was shown for bots (Geiger & Halfaker, 2017). The audit adds measurement: the size of each component in seven editions on one operational definition, the size and location of the tag's documented omissions, and the dependence of timing results on the attribution rule. Neither rule is wrong: the unbounded rule answers whether content was ever removed, the radius rule who removed it, and analysts who use the history dumps for the second question inherit the first rule unless they recompute.

### Implications

For studies of quality work in the tradition of Stvilia et al. (2007, 2008), the practical consequence is to report the composition of reverts by reverter class alongside any rate and to choose exclusions from the construct.

The tag result is the most immediately usable. The `mw-reverted` tag is the cheapest revert indicator, and in the two editions that patrol recent changes it omits most reverts made by people without patrol-exempt status, who are disproportionately unregistered and new; under FlaggedRevs the omission is smaller, 13 to 29 percent for the same groups. Tag-based indicators are entering the literature (Ariel, 2026). A comparison of tag-based revert rates across such editions reads a configuration difference as a difference in reception, as the English and Italian example shows, and the direction of the bias is known: reverts by the least established editors are the ones missing.

### Proposed reporting items

Table 5 separates what any study can state from what requires recomputation, in the manner of documentation standards with a low entry cost (Gebru et al., 2021). The items are a proposal from one audit, not a consensus guideline, and complement error frameworks for trace data (Sen et al., 2021). Among the 45 reviewed studies, 34 state a detection rule (item 2), 6 a window (item 3) and one the treatment of all three reverter classes (item 4); the items completed for this study are in Table S11.

**Table 5.** Proposed reporting items for revert-based indicators.

| Tier | Item |
|---|---|
| Always (no extra computation) | 1. The construct the revert stands for (Table 1). |
| | 2. The attribution rule: source field, library and radius, or tag. |
| | 3. The observation window and its justification for the editions studied. |
| | 4. Whether reverts by bots, by one-click tools and by the author are counted. |
| When reverter data are available | 5. The share of reverts made by each reverter class, and how many accounts make the tool reverts. |
| | 6. Outcomes separately by reverter class when the construct is the contributor's experience. |
| When page histories are available | 7. Results under both an unbounded and a radius rule if timing or the identity of the reverter matters. |
| For tag-based indicators | 8. The edition's patrolling regime and autopatrol rules, the period of tag availability, and a coverage check against a hash-based rule. |

### Limitations

The measured edits are first edits of self-created accounts, so the audit says nothing directly about established editors or article-level conflict measures, where shares will differ. Reverter classes rest on bot flags and change tags: unflagged bots are few (reverts within 5 seconds by registered non-bot accounts are at most 0.15 percent of first reverts), but tools without a tag are counted as manual, and the English tags are incomplete before 2021. Edit filters (Vaseva & Müller-Birn, 2020), deletions and, under FlaggedRevs, rejections of pending edits remove or relabel cases. Partial reverts are missed by all hash-based rules, and 0.5 to 4.2 percent of tagged first edits had no identity revert within the radius. Intervals resample editors; resampling reverting accounts widens them without changing a decision (Table S10), and clustering in pages is not modeled. The registration cannot demonstrate that the held-out outputs were unseen, and the most informative analyses are exploratory and should be replicated on other editions and later dumps; Wikimedia hosts only recent dump versions, so once version 2026-09 is retired exact reproduction starts from the released aggregates. Finally, the review is a structured sample coded with the assistance of a language model and checked by one person, and it describes what articles report, not what their code does.

### Conclusion

A revert is evidence of information quality work, and like other evidence it depends on who produced it and by what procedure it was recorded. A newcomer revert rate is a mixture of acts by bots, tool users, other editors and the newcomers themselves, in proportions that differ across language editions; the software's own record of reverts depends on the rights of the person who reverted, enough to double a difference between editions; and what a longer window shows depends on the attribution rule. Stating the construct, the reverter population and the rule costs a sentence each, and it is what makes revert-based findings comparable.

## Data availability statement

The data that support the findings are openly available from the Wikimedia Foundation at https://dumps.wikimedia.org/other/mediawiki_history/ (version 2026-09 was used; only recent versions remain hosted). Code, aggregates, the review table, figure data, logs and the registration (https://doi.org/10.5281/zenodo.23720117; the registered text is also in the repository) are available at https://github.com/beatsbywoni/wiki-revert-audit and archived at Zenodo (https://doi.org/10.5281/zenodo.24054641). Editor-level derived data are not released because they could be re-identified from public edit histories; the code regenerates them from the dumps.

## Endnotes

1. Column order and the identity-revert rule were read from the Wikimedia Analytics Refinery source (`MediawikiEvent.scala`; `DenormalizedRevisionsBuilder.scala`), master branch on 26 October 2026. A revision whose parent is the previous revision with the same hash is not counted as a revert, a filter added in commits of 28 May and 3 June 2026; earlier dump versions may count such revisions.
2. Patrolling configuration was read from the Wikimedia configuration repository operations/mediawiki-config on 28 October and 12 November 2026: `wgUseRCPatrol` is enabled for French and Italian; FlaggedRevs is installed on German, Polish and English (on English for a small set of protected pages; the edition is grouped with those that do not patrol edits); Japanese and Korean have neither; French promotes accounts to autopatrolled implicitly at 500 edits and 90 days. The `mw-reverted` tag was enabled on all Wikimedia wikis on 15 September 2020 (Phabricator task T164307). Its conditions are in the MediaWiki manual: approval of the reverting edit through autopatrol, patrol or FlaggedRevs review, and no tagging if the reverting edit has itself been reverted or deleted by the time it is approved. The maximum depth of 15 revisions is the default of the core setting `$wgRevertedTagMaxDepth`. A comparison of the tag with the dumps' identity-revert field was planned at the Wikimedia Foundation in 2020 (Phabricator task T266374); I found no published result.

## References

Ariel, Y. (2026). Crisis documentation on Hebrew Wikipedia: Revision dynamics and epistemic stabilization in wartime articles. Journal of Documentation. Advance online publication. https://doi.org/10.1108/JD-04-2026-0232

Choi, B., Alexander, K., Kraut, R. E., & Levine, J. M. (2010). Socialization tactics in Wikipedia and their effects. In Proceedings of the 2010 ACM Conference on Computer Supported Cooperative Work (pp. 107–116). ACM. https://doi.org/10.1145/1718918.1718940

de Laat, P. B. (2015). The use of software tools and autonomous bots against vandalism: Eroding Wikipedia's moral order? Ethics and Information Technology, 17(3), 175–188. https://doi.org/10.1007/s10676-015-9366-9

Ekstrand, M. D., & Riedl, J. T. (2009). rv you're dumb: Identifying discarded work in wiki article history. In Proceedings of the 5th International Symposium on Wikis and Open Collaboration (pp. 1–10). ACM. https://doi.org/10.1145/1641309.1641317

Flöck, F., Vrandečić, D., & Simperl, E. (2012). Revisiting reverts: Accurate revert detection in Wikipedia. In Proceedings of the 23rd ACM Conference on Hypertext and Social Media (pp. 3–12). ACM. https://doi.org/10.1145/2309996.2310000

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé, H., III, & Crawford, K. (2021). Datasheets for datasets. Communications of the ACM, 64(12), 86–92. https://doi.org/10.1145/3458723

Geiger, R. S., & Halfaker, A. (2013). When the levee breaks: Without bots, what happens to Wikipedia's quality control processes? In Proceedings of the 9th International Symposium on Open Collaboration (pp. 1–6). ACM. https://doi.org/10.1145/2491055.2491061

Geiger, R. S., & Halfaker, A. (2017). Operationalizing conflict and cooperation between automated software agents in Wikipedia: A replication and expansion of "Even good bots fight". Proceedings of the ACM on Human-Computer Interaction, 1(CSCW), 1–33. https://doi.org/10.1145/3134684

Geiger, R. S., & Ribes, D. (2010). The work of sustaining order in Wikipedia: The banning of a vandal. In Proceedings of the 2010 ACM Conference on Computer Supported Cooperative Work (pp. 117–126). ACM. https://doi.org/10.1145/1718918.1718941

Halfaker, A. (n.d.). mwreverts: A set of utilities for detecting reverts in MediaWiki revision data [Computer software]. Retrieved November 12, 2026, from https://github.com/mediawiki-utilities/python-mwreverts

Halfaker, A., Geiger, R. S., Morgan, J. T., & Riedl, J. (2013). The rise and decline of an open collaboration system: How Wikipedia's reaction to popularity is causing its decline. American Behavioral Scientist, 57(5), 664–688. https://doi.org/10.1177/0002764212469365

Halfaker, A., Kittur, A., & Riedl, J. (2011). Don't bite the newbies: How reverts affect the quantity and quality of Wikipedia work. In Proceedings of the 7th International Symposium on Wikis and Open Collaboration (pp. 163–172). ACM. https://doi.org/10.1145/2038558.2038585

Halfaker, A., & Riedl, J. (2012). Bots and cyborgs: Wikipedia's immune system. Computer, 45(3), 79–82. https://doi.org/10.1109/MC.2012.82

Hara, N., Shachaf, P., & Hew, K. F. (2010). Cross-cultural analysis of the Wikipedia community. Journal of the American Society for Information Science and Technology, 61(10), 2097–2108. https://doi.org/10.1002/asi.21373

Hill, B. M., & Shaw, A. (2014). Consider the redirect: A missing dimension of Wikipedia research. In Proceedings of the International Symposium on Open Collaboration (pp. 1–4). ACM. https://doi.org/10.1145/2641580.2641616

Howison, J., Wiggins, A., & Crowston, K. (2011). Validity issues in the use of social network analysis with digital trace data. Journal of the Association for Information Systems, 12(12), 767–797. https://doi.org/10.17705/1jais.00282

Jacobs, A. Z., & Wallach, H. (2021). Measurement and fairness. In Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency (pp. 375–385). ACM. https://doi.org/10.1145/3442188.3445901

Jeong, H. (2026). wiki-revert-audit: Code, aggregates and logs for "Which reverts count?" [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.24054641

Kittur, A., Suh, B., Pendleton, B. A., & Chi, E. H. (2007). He says, she says: Conflict and coordination in Wikipedia. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (pp. 453–462). ACM. https://doi.org/10.1145/1240624.1240698

Mai, J.-E. (2013). The quality and qualities of information. Journal of the American Society for Information Science and Technology, 64(4), 675–688. https://doi.org/10.1002/asi.22783

MediaWiki. (n.d.). Manual:Reverts. Retrieved November 10, 2026, from https://www.mediawiki.org/wiki/Manual:Reverts

Morgan, J. T., & Halfaker, A. (2018). Evaluating the impact of the Wikipedia Teahouse on newcomer socialization and retention. In Proceedings of the 14th International Symposium on Open Collaboration (pp. 1–7). ACM. https://doi.org/10.1145/3233391.3233544

Müller-Birn, C., Dobusch, L., & Herbsleb, J. D. (2013). Work-to-rule: The emergence of algorithmic governance in Wikipedia. In Proceedings of the 6th International Conference on Communities and Technologies (pp. 80–89). ACM. https://doi.org/10.1145/2482991.2482999

Priedhorsky, R., Chen, J., Lam, S. K., Panciera, K., Terveen, L., & Riedl, J. (2007). Creating, destroying, and restoring value in Wikipedia. In Proceedings of the 2007 International ACM Conference on Supporting Group Work (pp. 259–268). ACM. https://doi.org/10.1145/1316624.1316663

Sen, I., Flöck, F., Weller, K., Weiß, B., & Wagner, C. (2021). A total error framework for digital traces of human behavior on online platforms. Public Opinion Quarterly, 85(S1), 399–422. https://doi.org/10.1093/poq/nfab018

Simonsohn, U., Simmons, J. P., & Nelson, L. D. (2020). Specification curve analysis. Nature Human Behaviour, 4(11), 1208–1214. https://doi.org/10.1038/s41562-020-0912-z

Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W. (2016). Increasing transparency through a multiverse analysis. Perspectives on Psychological Science, 11(5), 702–712. https://doi.org/10.1177/1745691616658637

Stvilia, B., Gasser, L., Twidale, M. B., & Smith, L. C. (2007). A framework for information quality assessment. Journal of the American Society for Information Science and Technology, 58(12), 1720–1733. https://doi.org/10.1002/asi.20652

Stvilia, B., Twidale, M. B., Smith, L. C., & Gasser, L. (2008). Information quality work organization in Wikipedia. Journal of the American Society for Information Science and Technology, 59(6), 983–1001. https://doi.org/10.1002/asi.20813

Tran, C., Champion, K., Hill, B. M., & Greenstadt, R. (2022). The risks, benefits, and consequences of prepublication moderation: Evidence from 17 Wikipedia language editions. Proceedings of the ACM on Human-Computer Interaction, 6(CSCW2), 1–25. https://doi.org/10.1145/3555225

Trokhymovych, M., Aslam, M., Chou, A.-J., Baeza-Yates, R., & Saez-Trumper, D. (2023). Fair multilingual vandalism detection system for Wikipedia. In Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (pp. 4981–4990). ACM. https://doi.org/10.1145/3580305.3599823

Tsvetkova, M., García-Gavilanes, R., & Yasseri, T. (2016). Dynamics of disagreement: Large-scale temporal network analysis reveals negative interactions in online collaboration. Scientific Reports, 6, Article 36333. https://doi.org/10.1038/srep36333

Vaseva, L., & Müller-Birn, C. (2020). You shall not publish: Edit filters on English Wikipedia. In Proceedings of the 16th International Symposium on Open Collaboration (pp. 1–10). ACM. https://doi.org/10.1145/3412569.3412580

Warncke-Wang, M., Ho, R., Miller, M., & Johnson, I. (2023). Increasing participation in peer production communities with the Newcomer Homepage. Proceedings of the ACM on Human-Computer Interaction, 7(CSCW2), 1–26. https://doi.org/10.1145/3610071

West, A. G., Kannan, S., & Lee, I. (2010). Detecting Wikipedia vandalism via spatio-temporal analysis of revision metadata? In Proceedings of the Third European Workshop on System Security (pp. 22–28). ACM. https://doi.org/10.1145/1752046.1752050

Wikimedia Foundation. (2026). MediaWiki history dumps (Version 2026-09) [Data set]. https://dumps.wikimedia.org/other/mediawiki_history/

Yasseri, T., Sumi, R., Rung, A., Kornai, A., & Kertész, J. (2012). Dynamics of conflicts in Wikipedia. PLoS ONE, 7(6), Article e38869. https://doi.org/10.1371/journal.pone.0038869

Zheng, L., Albano, C. M., Vora, N. M., Mai, F., & Nickerson, J. V. (2019). The roles bots play in Wikipedia. Proceedings of the ACM on Human-Computer Interaction, 3(CSCW), 1–20. https://doi.org/10.1145/3359317
