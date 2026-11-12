# Which reverts count? Reverter populations, attribution rules and observation windows behind a Wikipedia indicator of information quality work

Hongwon Jeong

Center for Creative Convergence Education, Hanyang University ERICA, 55 Hanyangdaehak-ro, Sangnok-gu, Ansan, Gyeonggi-do 15588, Republic of Korea. Telephone +82-31-400-5786. Email: beatsbywoni@hanyang.ac.kr. ORCID 0009-0003-7908-7478

## Abstract

Whether an edit was reverted is a standard trace of information quality work in Wikipedia, read as a judgment of quality, as conflict, as the rejection a contributor experiences and as human effort. What the trace records depends on three seldom-reported choices: who counts as a reverter, how a later revision is attributed to an earlier edit, and how long edits are observed. This study measures what those choices contain, holding the measured edits fixed, on the first edits of 3.2 million newcomers in seven language editions. Bots, one-click tools, other editors and the newcomers themselves each make an edition-specific share of first reverts, and newcomers reverted by different classes differ in later activity. The software's own record of reverts is conditional on trust: in the two editions that patrol recent changes, the revert tag is missing for most reverts made by editors without patrol-exempt status, enough to change a measured difference between editions. Whether excluding a class of reverters matters less over longer windows depends on the attribution rule. Most analyses are exploratory; registered tests concern a secondary question. The study contributes a specification of what a revert indicates and reporting items tied to the construct an analyst intends.

**Keywords:** information quality; trace data; measurement validity; provenance; Wikipedia; reverts; bots

## Introduction

When Stvilia et al. (2007) proposed a framework for information quality assessment in this journal, two of the measures they derived for Wikipedia articles were built from reverts. The number of reverts entered the measure of authority and reputation, and the median time to revert defined volatility. The article does not say how a revert was identified or whose reverts were counted. Nearly two decades later the revert is a standard trace of what Stvilia et al. (2008) called information quality work in Wikipedia, and the choices on which a revert count depends are still seldom reported (Table 2).

Because every revert is recorded, "was this edit reverted" serves as a general-purpose indicator. It is read as a judgment on the quality of an edit and as a label for training quality-prediction models (Trokhymovych et al., 2023), as a measure of conflict (Kittur et al., 2007; Yasseri et al., 2012), as the rejection a newcomer experiences (Halfaker et al., 2011, 2013), as an outcome in onboarding experiments (Warncke-Wang et al., 2023) and as evidence about how humans and automated agents share quality work (Geiger & Halfaker, 2013; Zheng et al., 2019). These uses presuppose different constructs, and information science has long held that what an indicator of quality means depends on the activity and context in which it is used (Stvilia et al., 2007; Mai, 2013). A judgment on an edit, a dispute, an experience of rejection and a quantity of human effort are not carried by the same reverts.

A revert is a relation between an edit and a later revision, so the analyst has to decide which later revisions count. The first decision is the reverter population. Wikipedia's quality work is done by bots, by trusted editors using one-click tools such as rollback, Huggle and Twinkle, by other registered and unregistered editors who use the undo function or edit by hand, and by authors who take back their own edits (Geiger & Ribes, 2010; Halfaker & Riedl, 2012; de Laat, 2015). The second is the attribution rule that links a later revision to the edit it undoes, on which the Wikimedia history dumps, the mwreverts library (Halfaker, n.d.) and the software's own revert tag differ. The third is the observation window. Research on digital trace data has shown that such preprocessing decisions, often undocumented, can drive results (Howison et al., 2011; Hill & Shaw, 2014; Geiger & Halfaker, 2017; Sen et al., 2021), and measurement theory asks that an operationalization be justified against the construct it claims (Jacobs & Wallach, 2021). For reverts, the accuracy of detection has been examined (Ekstrand & Riedl, 2009; Flöck et al., 2012), Geiger and Halfaker (2017) showed for reverts between bots that the operationalization changes the conclusion, and that reverters are of different kinds is established for the English edition (Halfaker & Riedl, 2012; Halfaker et al., 2013). Reviews of Wikipedia scholarship in this journal organize it by readership and content (Okoli et al., 2014; Mesgari et al., 2015). What the trace contains under each decision, across language editions and attribution rules, has not been measured.

This study asks four questions about the reverts of newcomer first edits. What share of first reverts does each class of reverter make in each edition? How completely does the software's own record of reverts, the `mw-reverted` tag, cover them, and on what does its coverage depend? Do newcomers reverted by different classes differ in later activity? And does the effect of excluding a class of reverters depend on the observation window and the attribution rule? The questions are answered with a fixed-edit audit of 3.2 million newcomer first edits in seven language editions, in the spirit of a multiverse or specification-curve analysis (Steegen et al., 2016; Simonsohn et al., 2020). A survey of reporting practice in 41 studies motivates the audit; it is not offered as a systematic review.

The contribution is a specification of what this indicator of quality work indicates. For information science its central result concerns documentation. The tag is a record that the system itself produces about quality work, and its coverage follows the system's hierarchy of trust: where an edition patrols recent changes, a revert enters the record at once if the reverter is exempt from patrol and otherwise only if someone approves it. The condition is documented in the software manual; its extent has not, to my knowledge, been measured (Endnote 2). The other results are measured compositions (the share of each class of reverter in each edition and the later activity of the newcomers each class reverts) and the dependence of window results on the attribution rule. The paper ends with proposed reporting items tied to the construct an analyst intends to measure.

## Background

### One trace, four readings

If quality is relative to activity and context (Stvilia et al., 2007; Mai, 2013), a trace produced by quality work is not itself a quality score. Stvilia et al. (2008) describe information quality work in Wikipedia as a division of labor among agents in different roles. A revert is the trace of one act in that work, the removal of a contribution, and the constructs for which it is used read that act from four positions (Table 1): its object (was the edit acceptable), the relation between the parties (are they in dispute), its recipient (what the contributor experienced) and its performer (who did the work). The typology is my reading of how the trace is used, and the reverter population each construct calls for is an argument, not a finding.

As a *quality judgment on the edit*, every revert that removes the edit counts, whoever made it, though a self-revert is a different judgment from a rejection by others. As *conflict* between editors or over an article (Kittur et al., 2007; Yasseri et al., 2012), reverts by bots and reverts of vandalism are not disputes, and mutual or repeated reverts matter more than single ones. As *the contributor's experience of rejection*, in research on newcomer socialization and retention (Choi et al., 2010; Halfaker et al., 2013; Morgan & Halfaker, 2018), self-reverts should not count and the mode of rejection matters. As *human quality-work effort*, in studies of how communities and algorithms share governance (Müller-Birn et al., 2013; Zheng et al., 2019), bot reverts are a separate category and the status of one-click tools has to be decided, because a tool revert is a human judgment delivered with machine assistance (Halfaker & Riedl, 2012).

**Table 1.** Four constructs a revert is used to indicate, the position from which each reads the act, and the reverter population each calls for (the author's reading).

| Construct | Position | Example | Reverter population called for |
|---|---|---|---|
| Quality judgment on the edit | Object | Trokhymovych et al. (2023) | All reverters; self-reverts reported separately |
| Conflict | Relation | Yasseri et al. (2012) | Human reverters other than the author; vandalism reverts set apart |
| Contributor's experience of rejection | Recipient | Halfaker et al. (2013) | Others only; mode (bot, tool, manual) distinguished |
| Human quality-work effort | Performer | Geiger and Halfaker (2013) | Humans; bots separate; tools decided explicitly |

### Detecting and attributing reverts

The identity revert, an edit that returns a page to a byte-identical earlier state, is the standard operationalization (Kittur et al., 2007). Two implementations dominate. The mwreverts library searches a window of 15 revisions by default, a value its source attributes to Priedhorsky et al. (2007). The `mediawiki_history` dataset (Wikimedia Foundation, 2026) instead marks a revision as reverted if any later revision of the page restores a state that preceded it, with no radius and no time limit, so that an edit removed once can be "reverted" again years later by any revision that returns the page to a still earlier state. A third source is the `mw-reverted` change tag, enabled on all Wikimedia wikis on 15 September 2020 (Endnote 2), which the software applies to edits undone by an undo, a rollback or a manual revert, to a depth of 15 revisions. An edit made through the undo function is recorded as a revert whether or not its result is identical to an earlier revision, so the tag and the hash-based rules are not nested.

### A record conditioned on trust

Language editions differ in the institutions that shape reverting. Some hold edits by new users for review through the FlaggedRevs extension (Tran et al., 2022), some patrol recent changes, the rollback right is granted on different terms, and norms of interaction differ (Hara et al., 2010). These institutions also govern the record. MediaWiki applies the `mw-reverted` tag only once the reverting edit counts as approved: at once if recent-changes patrolling is off or the reverter holds the autopatrol right, and otherwise when someone patrols the edit or, under FlaggedRevs, reviews it. In the words of the manual, "reverts that are not patrolled will not be marked with the reverted tag" (MediaWiki, n.d.; Endnote 2). Whether an act of quality work is documented thus depends on the standing of the person who performed it, which is a question of provenance before it is a question of measurement.

### Reporting practice

To see how the three decisions are reported, I examined 41 empirical studies and official Wikimedia analyses, published from 2007 to 2026, in which a revert measure computed from revision histories is an outcome, an exposure, a label or a conflict indicator, or is itself the object of description (39 on Wikipedia, two on Wikia wikis). The search, the studies listed but not tallied (among them four in which reverting is one coded activity or a control variable, such as Arazy et al., 2019) and the eleven texts that could not be read are in Table S1. A language model (Claude) retrieved texts, extracted passages and proposed codes; I checked the codes of every study against the source, and the released coding table gives the passage behind each code. A choice counts as stated only if the article or its supplement states it for the main analysis. No second human coder took part and no reliability coefficient is claimed, so Table 2 is a survey of what one reader could find, not a systematic review, and its counts are approximate.

**Table 2.** Reporting of revert operationalization in 41 studies, 2007 to 2026. The observation window is tallied for the 21 studies in which the revert is an edit-level outcome, exposure or label; it does not apply in the same form to conflict measures computed over whole article histories.

| Choice | Studies in which it applies | Stated in the article |
|---|---|---|
| Detection rule | 41 | 29 |
| Search radius | 22 (identity rule) | 1 |
| Reverts made by bots | 41 | 9 |
| Reverts made with one-click tools | 41 | 5 |
| Self-reverts | 41 | 16 |
| Observation window | 21 (edit-level measures) | 5 |
| Sensitivity analysis over the reverter population | 41 | 0 |

Twelve studies do not state how reverts were detected, and of the 22 that use an identity rule one reports a search radius (three more cite a library whose default is 15). The treatment of reverts made by bots is stated in nine studies: five treat the type of reverter as a variable or focus on it, two exclude bot reverts (West et al., 2010; Tsvetkova et al., 2016) and two count them explicitly; ten more remove bot accounts from the sample and are silent on reverts that bots perform. Five studies say how one-click tools are treated, and one states the treatment of bots, tools and self-reverts together (Halfaker et al., 2013). Of the 21 studies with an edit-level measure, five state an observation window; four describe the outcome as "eventually reverted". No study varies the reverter population as a sensitivity analysis. Two features of this record shape the audit. The exclusions actually made are of self-reverts, commonly, and of bot reverts, rarely, and no study excludes tool-assisted reverts, so the audit sizes every reverter class and treats tool exclusion as hypothetical. And one study builds a conflict indicator partly on the software's revert tags, for the Hebrew edition (Ariel, 2026); none notes the conditions under which the `mw-reverted` tag is applied.

## Method

### Data and cohort

The data are the `mediawiki_history` dumps of version 2026-09 (Wikimedia Foundation, 2026). Seven editions were processed: English from January 2018 to September 2026 and the complete histories of Italian, Korean, German, Polish, French and Japanese. Reverts to states older than 2018 are therefore not detected in English, which against the dumps' own flag affects 28 of 42,042 sampled first edits from October 2020.

The unit is a registered editor whose first edit in any namespace was made in the article namespace; that edit is the measured edit. Editors whose first edit was elsewhere (6.5 to 13.1 percent of first-time editors) are outside the cohort, as are unregistered and temporary accounts and accounts flagged as bots. The primary cohort is self-created accounts whose first edit dates from 1 January 2019 to 31 March 2026, leaving at least 180 days of follow-up: 3,246,958 editors (Table 3). One edit per editor makes the editor the unit. First edits that create a page can be removed only by deletion; their share is reported (Table S2).

### Attribution rules

Three rules are compared. The *dump rule* is the `revision_is_identity_reverted` flag with the identifier of and delay to the first reverting revision. The source code shows that the flag groups a page's revisions by content hash over its entire history; the first occurrence of a hash is a base, later occurrences are reverts to that base, and a revision is reverted if a later revert has a base that precedes it (Endnote 1). I reimplemented the rule from the hashes on all Korean first edits and on year-stratified samples of 60,000 first edits in each other edition; status agreed with the flag on at least 99.9 percent of edits in every edition. The *radius rule* applies the mwreverts convention of 15 revisions to the same recomputation. The *tag rule* is the `mw-reverted` tag on the measured edit.

### Reverter classes

The first revert of each measured edit is assigned to one class, in this order: *bot* (the dump's bot flags, current or historical); *one-click tool* (the reverting revision carries the `mw-rollback`, `huggle` or `twinkle` change tag); *self* (the reverting account is the author); *unregistered* (no account, including temporary accounts); and *other manual* (any other registered account, including those using the undo function). The tool class is defined by tags, not by a common institution. The rollback right is appointed in some editions, is bundled with the automatically granted `editor` group of FlaggedRevs in German and Polish, and in Japanese belongs to a rollbacker group added by a later configuration change (Endnote 2). Rollback is tagged in all seven editions throughout; Huggle is tagged in English and French and Twinkle only in English, from September 2020 (Table S9). In five editions the class is therefore the exercise of the rollback right, while in English it also contains Twinkle, which any autoconfirmed account can use; tags of other tools are counted in Table S3.

### Quantities

For a window W, p(W) is the share of measured edits reverted within W. Excluding a class in the *strict* sense recodes edits first reverted by that class as not reverted; the change in p equals the class's share of first reverts times p, an identity. The *replace* variant, the object of the registered tests, instead looks for the first later revert by a non-excluded reverter. To learn what such later reverts are, I record for every first revert the next manual revert of the same edit by a registered third party (an account that is neither the author nor the first reverter), under both rules and with the clock started at the first revert.

Tag coverage is the share of reverts found by the radius rule whose measured edit carries no `mw-reverted` tag, for first edits from October 2020, by class of reverter, by whether the reverting account held a user group carrying the autopatrol right at the time, by the account's edit count, and by the edition's patrolling regime (Endnote 2). The other downstream quantities are the share of editors who edit again between day 2 and day 60, by class of first revert within 24 hours, with accounts blocked within 60 days separated, and the rank agreement of editor-level success rates (one minus the reverted share of an editor's first-90-day article edits, for editors with at least ten) with and without tool and bot reverts.

The cohorts are complete populations, so intervals express the sampling of page histories and the sensitivity of an estimate to individual editors and reverting accounts, not inference to other editions or periods. They are Wilson intervals for shares and percentile intervals from 2,000 bootstrap resamples of editors for ratios. Because reverts cluster in reverting accounts, which these intervals ignore, the quantities on which conclusions rest are also given with intervals that resample reverting accounts (Table 4, the tag results, Table S10). Quantities that need page histories use the 60,000-edit samples (all 47,629 Korean first edits with a usable history). Shares for cells with fewer than 50 edits are not reported.

### Registration and its limits

Design, hypotheses and code were registered on Zenodo (https://doi.org/10.5281/zenodo.23720117) after English, Korean, French and German had been analyzed and before the outputs for Japanese, Polish and Italian were opened. It is a hold-out replication with thresholds set from the exploratory editions, not a blind preregistration: the held-out editions had already been processed, a sentence of the registered text that says otherwise is wrong, and that their outputs were unopened is documented only by my own logs (Section S1 of the supplement, which lists all deviations). Four hypotheses were registered, all on the replace variant for bots and tools together. H1: its effect is larger within 24 hours than in the unbounded window (ratio R of unbounded to 24-hour effect below 1). H2: the share of bot- or tool-reverted edits later reverted by a human within 24 hours is below .25. H3, a descriptive criterion without a test: the tag and radius rules agree on at least 95 percent of edits, and more than half of the edits the dump rule marks reverted but the tag does not lie beyond the radius. H4: the odds ratio of retention for reverted versus non-reverted edits varies by a factor of at least 1.5 across nine filter-by-window cells. Decisions use one-sided 95 percent bootstrap bounds with Holm adjustment within edition. All outcomes are reported, in full in Table S7. Every other analysis, including all results on composition, tag coverage and retention by class, was designed after the first results and is exploratory in all seven editions.

### Transparency

Code, aggregates, the coding table of the survey, logs and the deviation log are public (https://github.com/beatsbywoni/wiki-revert-audit; archived release, Jeong, 2026). Editor-level files are not released, a recorded departure from the registration. The study uses public edit histories, reports aggregates only and involved no interaction with editors; it was not submitted for ethics review on that ground. Generative AI (Claude, Anthropic; model versions and dated tasks are in the public AI assistance log) was used for three tasks: drafting analysis code, drafting and editing prose, and, in the survey of reporting practice, retrieving and screening texts, extracting passages and proposing codes, which I checked against the sources. A second model (ChatGPT, OpenAI) assisted that check for two of the tallied studies. Model agents were also used to critique drafts, and several analyses were added in response. No model generated, altered or analyzed the audit's data: every number of the audit is produced by the released deterministic code from unmodified dumps. I specified the design, made the analytic decisions, checked the code against the primary sources cited and against the independent recomputation reported above, and am responsible for every statement. The study received no funding, and I declare no competing interests.

## Results

### What a revert rate is made of

Within 24 hours, 14.0 percent (Japanese) to 37.0 percent (English) of newcomer first edits were reverted (Table 3, Figure 1). Outside English, 9 to 20 percent of first edits create a page and cannot be reverted in this sense (Table S2). The first revert came from a bot in 12.2 percent of cases in English and 4.2 percent in French, and in at most 0.3 percent elsewhere. One-click tools made 24.7 percent (Japanese) to 52.5 percent (Italian) of first reverts. Manual reverts by other registered editors made up 28.9 to 64.3 percent, 49 to 78 percent of them through the undo function; unregistered editors and the newcomers themselves made the rest.

**Table 3.** Cohorts and composition of first reverts within 24 hours (dump rule, first edits of self-created accounts, 2019 to March 2026). Shares are of first reverts; the strict effect of excluding a class, in percentage points, is its share times p. Tool accounts: accounts that made the tool reverts, with the share of the most active. In English the tool class includes Twinkle only from September 2020. Editions marked * were held out for registered tests. Exploratory.

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

Three qualifications apply to the tool share. Outside English and German it is produced by few people: 93 accounts made the tool reverts in Korean and 103 in Japanese, the most active alone 19 and 23 percent, and intervals that resample reverting accounts are correspondingly wide (Table S2). In English the class is not constant over time, since Twinkle is tagged only from September 2020 and Huggle tags are nearly absent in 2021 and 2022; the share is .524 for first edits from 2021. And it is a lower bound where other tools are tagged: reverts carrying only the tags of LiveRC in French, or of four further tools in English, would add 8.5 and 3.9 points (Table S3).

### The tag records a revert only where the reverter is trusted or the revert approved

The tag and radius rules agreed on 98.6 percent of first edits in Japanese, 97.9 in Polish and 95.4 in Italian, meeting the first clause of H3. The second clause was rejected in all three: of the edits that the dump rule marked reverted and the tag did not, 42, 9 and 7 percent lay beyond the radius, against the registered expectation of more than half. The exploratory follow-up locates the gap in the approval condition described above.

For first edits from October 2020, the share of radius-rule reverts whose measured edit carries no tag was 0.3 to 1.0 percent in English, Korean and Japanese, where recent-changes patrolling is not enabled; 2.4 and 3.9 percent in German and Polish, which use FlaggedRevs; and 9.6 percent in Italian and 7.0 percent in French, which patrol recent changes (Figure 4; with reverting accounts resampled, 7.6 to 12.4 and 5.8 to 8.5 percent). The omission is concentrated among reverters without standing. In Italian and French, 79 and 71 percent of reverts by unregistered editors and 71 and 73 percent of newcomers' self-reverts were untagged, against under 1 percent of tool reverts. In German and Polish the figures were 23 and 29 percent for unregistered reverters and 13 percent for self-reverts.

Patrol actions are not in the dumps, but the user groups held by the reverting account at the time of the revert test the mechanism indirectly (Table S6). Among manual reverts by other registered editors in Italian, 1.0 percent were untagged where the account held a group that carries the autopatrol right and 77 percent (752 reverts by 345 accounts; 72 to 82 percent with accounts resampled) where it held none. The corresponding figures without such a group were 13 and 15 percent in German and Polish and at most 0.2 percent in English, Korean and Japanese. French looked like an exception, with 4.5 percent, and resolves into the rule: that edition grants the autopatrolled status automatically at 500 edits and 90 days without recording a group (Endnote 2), and among manual reverters with no recorded group 60 to 70 percent of reverts were untagged below 500 edits, 3.4 percent between 500 and 4,999 and 0.1 percent above. Two things remain unexplained by the rule as documented: a residue among trusted reverters (5.3 percent of tool reverts by group holders in Polish, 4.0 percent of manual reverts by group holders in Japanese), and how many unapproved reverts are patrolled later, since approval can arrive only while the software retains the patrol record. Because a later approved revert by anyone also tags the edit, the class-specific shares are lower bounds on the omission per revert.

[Figure 4 here]

**Figure 4.** Reverts found by the 15-revision radius rule whose reverted edit carries no `mw-reverted` tag, first edits from October 2020, by who made the revert and by the edition's patrolling regime. Bars are 95 percent Wilson intervals. Exploratory.

The consequence for a comparison can be computed directly. For first edits from October 2020, the share reverted under the radius rule is 39.5 percent in English and 35.9 percent in Italian, a difference of 3.6 points; with the tag it is 40.1 and 32.7 percent, a difference of 7.4 points. Of the change of 3.8 points (3.4 to 4.2 with reverting accounts resampled), 3.2 come from Italian, where 3.4 percent of first edits are reverted under the radius rule and untagged and 0.3 percent are tagged without a radius-rule revert, and 0.6 from English, where the two figures are 0.1 and 0.7 percent (Table S6). Nearly all English edits tagged without a radius-rule revert (292 of 301) are not identity-reverted under the dumps' own flag either. Undos whose result matches no earlier revision are a likely source, but the reverting revisions were not examined. The change is stable over time (3.7 points for first edits to 2024, 4.0 from 2025), and the French gap to English grows from 13.7 to 15.8 points. The association of being reverted with retention is unaffected (odds ratios within .02 of each other under the two rules); what moves is any quantity that depends on who reverted. Neither rule is the truth, and the example is a favorable case, a small gap between two large editions, measured on newcomer first edits only.

### Reverts by different classes reach different newcomers

Newcomers whose first edit was not reverted within 24 hours edited again on days 2 to 60 in 17.1 to 26.6 percent of cases (Figure 3). Of those reverted with a one-click tool, 3.5 to 8.6 percent did; of those reverted manually by another registered editor, 10.4 to 14.2 percent; of those who reverted themselves, 11.3 to 19.9 percent. As odds ratios against non-reverted newcomers, tool reverts range from 0.10 to 0.38, manual reverts by others from 0.41 to 0.71 and self-reverts from 0.55 to 0.68 (Table S5). Blocking does not produce the contrast: with accounts blocked within 60 days removed, the odds ratios are 0.09 to 0.38 for tool reverts and 0.40 to 0.70 for manual ones. These are associations between groups of newcomers, not effects of the mode of reverting: tools are aimed at vandalism, and intent, repeat accounts and accompanying warnings are not controlled. The point for measurement is that a single "reverted" category averages over events whose relation to the contributor's later activity differs, by a factor of 1.4 to 4 in odds between manual and tool reverts, in proportions that vary by edition.

[Figure 3 here]

**Figure 3.** Newcomers who edited again on days 2 to 60, by who made the first revert of their first edit within 24 hours. Bars are 95 percent Wilson intervals; the grey line spans the classes within an edition. Exploratory.

Downstream estimates move accordingly when the reverter population changes. The registered H4 compared the odds ratio of retention across nine cells (all reverts, without bots, without bots and tools; 24 hours, 7 days, unbounded). The ratio of the largest to the smallest was 1.84 [1.79, 1.89] in Japanese and 1.78 [1.72, 1.85] in Italian, above the registered 1.5, and 1.43 [1.37, 1.49] in Polish, below it, so H4 is met in two of three held-out editions (its second clause, a lower bound above 1, cannot fail). The nine cells mix the effect of the filter with that of the window. Across the three 24-hour cells alone, which isolate the filter, the ratio is 1.30 to 1.50 (1.93 in Korean) and reaches 1.5 among the held-out editions only in Italian. The movement is compositional: recoding tool-reverted newcomers, the group least likely to return, as not reverted raises the odds ratio. Editor-level rankings shift for the same reason: the rank correlation between editors' success rates with and without bot and tool reverts was .75 to .93.

### Later reverts and the window

If a class of reverts is excluded, does a later revert by someone else take its place? H2 was supported in the three held-out editions: the share of bot- or tool-reverted first edits with a later non-bot, non-tool revert within 24 hours was .145 in Japanese, .111 in Polish and .114 in Italian, with upper bounds below the registered .25. Counting only registered third parties, and the 24 hours from the first revert, a manual revert followed 5.7 to 9.7 percent of bot and tool first reverts under the dump rule and 0.9 to 2.9 percent under the radius rule (Table 4, Figure 2).

**Table 4.** Follow-up manual reverts by a registered third party within 24 hours of the first revert, by who made the first revert, and the window ratio R, under two attribution rules. Manual: first revert by another registered editor without a tool. Denominators are all first reverts by the class. R: replace effect of excluding bots and tools, unbounded window over 24 hours, with 95 percent bootstrap intervals that resample reverting accounts. Follow-up shares are exploratory.

| Edition | Dump rule: after bot or tool | Dump rule: after manual | Radius rule: after bot or tool | Radius rule: after manual | R, dump rule | R, radius rule |
|---|---|---|---|---|---|---|
| English | .077 | .066 | .010 | .006 | .92 [.90, .95] | 1.05 [1.03, 1.07] |
| Italian* | .079 | .082 | .013 | .010 | .84 [.83, .86] | 1.02 [1.02, 1.03] |
| Korean | .069 | .068 | .017 | .010 | .77 [.72, .84] | 1.07 [1.05, 1.11] |
| German | .057 | .041 | .009 | .003 | .92 [.90, .94] | 1.04 [1.02, 1.05] |
| Polish* | .060 | .035 | .013 | .002 | .88 [.85, .91] | 1.07 [1.04, 1.10] |
| French | .090 | .070 | .013 | .005 | .86 [.84, .88] | 1.04 [1.02, 1.06] |
| Japanese* | .097 | .091 | .029 | .013 | .92 [.89, .97] | 1.05 [1.02, 1.10] |

[Figure 2 here]

**Figure 2.** First edits with a later manual revert by a registered third party, by who made the first revert, under the dump rule (top) and the 15-revision radius rule (bottom), within 24 hours of the first revert (left) and unbounded (right). Bars are 95 percent Wilson intervals, which ignore clustering in reverting accounts. Exploratory.

What the data bound is the yield of the replace variant. An analyst who drops bot and tool reverts and looks for the next human revert recovers 6 to 10 percent of the dropped events within a day of the first revert (9 to 15 percent within a day of the edit under the registered definition), and under the dump rule mostly later reverts that reach back past the measured edit or undo unrelated edits; only 1.0 to 12.2 percent of bot- or tool-reverted first edits were reverted again after their content had been reinstated (Table S4).

H1 was supported under the dump rule in all three held-out editions (R of .92, .88 and .84; Table 4), also when reverting accounts are resampled (Table S10). Under the radius rule R is 1.02 to 1.07 in all seven editions, with every interval above 1. The reversal is close to arithmetic: a longer window adds first reverts by bots and tools and adds follow-up; under the radius rule follow-up is rare, so the effect grows, while under the dump rule deep reverts accumulate and the effect shrinks. H1 thus describes the unbounded rule more than it describes reverting, and analysts who take the reverting revision from the dumps to ask who reverted inherit that rule.

## Discussion

### What the indicator contains

For each construct the audit shows what an undifferentiated revert count contains for newcomer first edits; among the edits of established editors, from which conflict measures draw most of their reverts, the shares will differ. Read as a *quality judgment on the edit*, 3 to 11 percent of the judgments are the authors' own. Read as *conflict*, a quarter to a half of first reverts are one-click responses, made with the rollback right or, in English, also with Huggle and Twinkle. Read as *the contributor's experience of rejection*, the count mixes encounters that differ in what follows them, and the edition determines which is typical: a tool in Italian, Korean and English, a manual revert in German, Polish, French and Japanese. Read as *human quality-work effort*, bots make a material share of first reverts only in English and French, while the status of one-click reverts concerns a quarter to a half of first reverts everywhere.

That bots, tools and other editors revert differently, and that tool reverts go with lower retention, was known for English (Halfaker & Riedl, 2012; Geiger & Halfaker, 2013; Halfaker et al., 2013), and that operational choices can reverse a conclusion about reverts was shown for bots (Geiger & Halfaker, 2017). The audit adds measurement: the size of each component in seven editions on one operational definition, and the dependence of timing results on the attribution rule. Neither rule is wrong: the unbounded rule answers whether content was ever removed, the radius rule who removed it.

### A record that follows the hierarchy of trust

The tag result bears on how information systems document the work done in them. The `mw-reverted` tag is the cheapest revert indicator and the only one the platform itself asserts. In the two editions that patrol recent changes it is missing for seven to ten percent of reverts overall and for most of those made by unregistered editors, by registered editors without patrol-exempt status and by the newcomers themselves (71 to 79 percent in Italian); under FlaggedRevs the omission for the same groups is 13 to 29 percent. The record is thus complete for the quality work of trusted editors and sparse for that of everyone else, and the boundary is set by each community's configuration. For studies of information quality work in the tradition of Stvilia et al. (2008), this means that platform-asserted metadata about an act carries the provenance of the actor: who may act without review decides whose acts are recorded.

Tag-based indicators are entering the literature. One surveyed study builds a conflict flag for the Hebrew edition from four revert tags and edit summaries (Ariel, 2026). Hebrew also enables recent-changes patrolling (Endnote 2), but its tag coverage was not measured here; it depends on how completely reverts by non-exempt editors are patrolled as well as on the configuration, and the three tags placed on reverting revisions are not subject to the condition. A comparison of tag-based revert rates across editions with different regimes can read a configuration difference as a difference in reception, as the English and Italian example shows, and the direction of the bias is known: reverts by the least established editors are the ones missing.

### Proposed reporting items

Table 5 separates what any study can state from what requires recomputation, in the manner of documentation standards with a low entry cost (Gebru et al., 2021). The items are a proposal from one audit, untested on other studies, and not a consensus guideline; the items completed for this study are in Table S11.

**Table 5.** Proposed reporting items for revert-based indicators.

| Tier | Item |
|---|---|
| Always (no extra computation) | 1. The construct the revert stands for. |
| | 2. The attribution rule: source field, library and radius, or tag. |
| | 3. The observation window and its justification for the editions studied. |
| | 4. Whether reverts by bots, by one-click tools and by the author are counted. |
| When reverter data are available | 5. The share of reverts made by each reverter class, and how many accounts make the tool reverts. |
| | 6. Outcomes separately by reverter class when the construct is the contributor's experience. |
| When page histories are available | 7. Results under both an unbounded and a radius rule if timing or the identity of the reverter matters. |
| For tag-based indicators | 8. The edition's patrolling regime and autopatrol rules, the period of tag availability, and a coverage check against a hash-based rule. |

### Limitations

The measured edits are first edits of self-created accounts, so the audit says nothing directly about established editors or article-level conflict measures. The mechanism behind the tag omission is inferred from user groups, edit counts and configuration; the public patrol and review logs were not joined, and edits tagged without a hash-based revert were counted but not examined. Reverter classes rest on bot flags and change tags: unflagged bots appear to be few, but tools without a tag are counted as manual, the English tags are incomplete before 2021, and holders of global rights appear without a local group. Edit filters, deletions and rejections of pending edits remove cases before they can be reverted, and partial reverts are missed by all hash-based rules. Resampling reverting accounts widens intervals without changing a registered decision on H1 or H2 (Table S10); H4 was not recomputed in this way, and clustering in pages is not modeled. The registration cannot demonstrate that the held-out outputs were unseen, and the most informative analyses are exploratory and should be replicated on other editions and later dumps; version 2026-09 will not remain hosted, after which reproduction starts from the released aggregates. The survey of reporting practice was read by one person with the assistance of language models, without a second human coder, and describes what articles report, not what their code does.

### Conclusion

A revert is evidence of information quality work, and like other evidence it depends on who produced it and by what procedure it was recorded. A newcomer revert rate is a mixture of acts by bots, tool users, other editors and the newcomers themselves, in edition-specific proportions; the platform's own record of reverts depends on the standing of the person who reverted, enough to change a difference between editions; and what a longer window shows depends on the attribution rule. Stating the construct, the reverter population and the rule costs a sentence each.

## Data availability statement

The data that support the findings are openly available from the Wikimedia Foundation at https://dumps.wikimedia.org/other/mediawiki_history/ (version 2026-09 was used; only recent versions remain hosted). Code, aggregates, the coding table, figure data, logs and the registration (https://doi.org/10.5281/zenodo.23720117; the registered text is also in the repository) are available at https://github.com/beatsbywoni/wiki-revert-audit and archived at Zenodo (https://doi.org/10.5281/zenodo.24054641). Editor-level derived data are not released because they could be re-identified from public edit histories; the code regenerates them from the dumps.

## Endnotes

1. Column order and the identity-revert rule were read from the Wikimedia Analytics Refinery source (`MediawikiEvent.scala`; `DenormalizedRevisionsBuilder.scala`), master branch on 26 October 2026. A revision whose parent is the previous revision with the same hash is not counted as a revert, a filter added in commits of 28 May and 3 June 2026 (the source cites Phabricator task T266374); earlier dump versions may count such revisions.
2. Patrolling configuration was read from the Wikimedia configuration repository operations/mediawiki-config on 28 October and 12 November 2026: `wgUseRCPatrol` is enabled for French and Italian (and for Hebrew); FlaggedRevs is installed on German, Polish and English (on English for a small set of protected pages; the edition is grouped with those without patrolling); Japanese and Korean have neither; French promotes accounts to autopatrolled implicitly at 500 edits and 90 days; the `editor` group of German and Polish carries the rollback right, and the Japanese rollbacker group cites Phabricator task T258339. The `mw-reverted` tag was enabled on all Wikimedia wikis on 15 September 2020 (Phabricator task T164307). Its conditions are in the MediaWiki manual: approval of the reverting edit through autopatrol, patrol or FlaggedRevs review, and no tagging if the reverting edit has itself been reverted or deleted by the time it is approved. The core source, read on 12 November 2026, shows that an undo counts as a revert without an exact match of content (`EditResultBuilder.php`, `RevertedTagUpdate.php`), that later approval relies on a cached edit result kept no longer than `$wgRCMaxAge` (`EditResultCache.php`), and that the depth of tagging (`$wgRevertedTagMaxDepth`) and the search radius for manual reverts (`$wgManualRevertSearchRadius`) are separate settings, both 15 by default. Task T266374 (2020) compares the tag with the dumps' identity-revert field; I found no published measurement of tag coverage by reverter or edition.

## References

Arazy, O., Lifshitz-Assaf, H., & Balila, A. (2019). Neither a bazaar nor a cathedral: The interplay between structure and agency in Wikipedia's role system. Journal of the Association for Information Science and Technology, 70(1), 3–15. https://doi.org/10.1002/asi.24076

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

Mesgari, M., Okoli, C., Mehdi, M., Nielsen, F. Å., & Lanamäki, A. (2015). "The sum of all human knowledge": A systematic review of scholarly research on the content of Wikipedia. Journal of the Association for Information Science and Technology, 66(2), 219–245. https://doi.org/10.1002/asi.23172

Morgan, J. T., & Halfaker, A. (2018). Evaluating the impact of the Wikipedia Teahouse on newcomer socialization and retention. In Proceedings of the 14th International Symposium on Open Collaboration (pp. 1–7). ACM. https://doi.org/10.1145/3233391.3233544

Müller-Birn, C., Dobusch, L., & Herbsleb, J. D. (2013). Work-to-rule: The emergence of algorithmic governance in Wikipedia. In Proceedings of the 6th International Conference on Communities and Technologies (pp. 80–89). ACM. https://doi.org/10.1145/2482991.2482999

Okoli, C., Mehdi, M., Mesgari, M., Nielsen, F. Å., & Lanamäki, A. (2014). Wikipedia in the eyes of its beholders: A systematic review of scholarly research on Wikipedia readers and readership. Journal of the Association for Information Science and Technology, 65(12), 2381–2403. https://doi.org/10.1002/asi.23162

Priedhorsky, R., Chen, J., Lam, S. K., Panciera, K., Terveen, L., & Riedl, J. (2007). Creating, destroying, and restoring value in Wikipedia. In Proceedings of the 2007 International ACM Conference on Supporting Group Work (pp. 259–268). ACM. https://doi.org/10.1145/1316624.1316663

Sen, I., Flöck, F., Weller, K., Weiß, B., & Wagner, C. (2021). A total error framework for digital traces of human behavior on online platforms. Public Opinion Quarterly, 85(S1), 399–422. https://doi.org/10.1093/poq/nfab018

Simonsohn, U., Simmons, J. P., & Nelson, L. D. (2020). Specification curve analysis. Nature Human Behaviour, 4(11), 1208–1214. https://doi.org/10.1038/s41562-020-0912-z

Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W. (2016). Increasing transparency through a multiverse analysis. Perspectives on Psychological Science, 11(5), 702–712. https://doi.org/10.1177/1745691616658637

Stvilia, B., Gasser, L., Twidale, M. B., & Smith, L. C. (2007). A framework for information quality assessment. Journal of the American Society for Information Science and Technology, 58(12), 1720–1733. https://doi.org/10.1002/asi.20652

Stvilia, B., Twidale, M. B., Smith, L. C., & Gasser, L. (2008). Information quality work organization in Wikipedia. Journal of the American Society for Information Science and Technology, 59(6), 983–1001. https://doi.org/10.1002/asi.20813

Tran, C., Champion, K., Hill, B. M., & Greenstadt, R. (2022). The risks, benefits, and consequences of prepublication moderation: Evidence from 17 Wikipedia language editions. Proceedings of the ACM on Human-Computer Interaction, 6(CSCW2), 1–25. https://doi.org/10.1145/3555225

Trokhymovych, M., Aslam, M., Chou, A.-J., Baeza-Yates, R., & Saez-Trumper, D. (2023). Fair multilingual vandalism detection system for Wikipedia. In Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (pp. 4981–4990). ACM. https://doi.org/10.1145/3580305.3599823

Tsvetkova, M., García-Gavilanes, R., & Yasseri, T. (2016). Dynamics of disagreement: Large-scale temporal network analysis reveals negative interactions in online collaboration. Scientific Reports, 6, Article 36333. https://doi.org/10.1038/srep36333

Warncke-Wang, M., Ho, R., Miller, M., & Johnson, I. (2023). Increasing participation in peer production communities with the Newcomer Homepage. Proceedings of the ACM on Human-Computer Interaction, 7(CSCW2), 1–26. https://doi.org/10.1145/3610071

West, A. G., Kannan, S., & Lee, I. (2010). Detecting Wikipedia vandalism via spatio-temporal analysis of revision metadata? In Proceedings of the Third European Workshop on System Security (pp. 22–28). ACM. https://doi.org/10.1145/1752046.1752050

Wikimedia Foundation. (2026). MediaWiki history dumps (Version 2026-09) [Data set]. https://dumps.wikimedia.org/other/mediawiki_history/

Yasseri, T., Sumi, R., Rung, A., Kornai, A., & Kertész, J. (2012). Dynamics of conflicts in Wikipedia. PLoS ONE, 7(6), Article e38869. https://doi.org/10.1371/journal.pone.0038869

Zheng, L., Albano, C. M., Vora, N. M., Mai, F., & Nickerson, J. V. (2019). The roles bots play in Wikipedia. Proceedings of the ACM on Human-Computer Interaction, 3(CSCW), 1–20. https://doi.org/10.1145/3359317
