# Which reverts count? Reverter populations, attribution rules and observation windows behind a Wikipedia indicator of information quality work

Hongwon Jeong

Center for Creative Convergence Education, Hanyang University ERICA, Ansan, Republic of Korea. ORCID 0009-0003-7908-7478. Email: beatsbywoni@hanyang.ac.kr

## Abstract

[ABSTRACT: to be rewritten after the seven-edition rerun; 200 words maximum]

**Keywords:** information quality; trace data; measurement validity; Wikipedia; reverts; bots; operationalization

## Introduction

When Stvilia et al. (2007) proposed a framework for information quality assessment in this journal, two of the measures they derived for Wikipedia articles were built from reverts. The number of reverts entered the measure of authority and reputation, and the median time to revert defined volatility. The article does not say how a revert was identified or whose reverts were counted. Nothing in 2007 required it to. Two decades later the revert is the most widely used trace of what Stvilia et al. (2008) called information quality work in Wikipedia, and the omission has become the norm: of 41 studies reviewed below, none reports the four choices on which a revert count depends.

Because every revert is recorded, "was this edit reverted" serves as a general-purpose indicator. It is read as a judgment on the quality of an edit and as a label for training quality-prediction models (Sarabadani et al., 2017; Trokhymovych et al., 2023), as a measure of conflict (Kittur et al., 2007; Yasseri et al., 2012), as the rejection a newcomer experiences (Halfaker et al., 2011, 2013), as an outcome in onboarding experiments (Warncke-Wang et al., 2023) and as evidence about how humans and automated agents share quality work (Geiger & Halfaker, 2013; Zheng et al., 2019). These uses presuppose different constructs, and information science has long held that an indicator of quality has no meaning apart from the activity and context in which it is used (Stvilia et al., 2007; Mai, 2013). A judgment on an edit, a dispute, an experience of rejection and a quantity of human effort are not carried by the same reverts.

A revert is a relation between an edit and a later revision, so the analyst has to decide which later revisions count. The first decision is the reverter population. Wikipedia's quality work is done by bots, by trusted editors using one-click tools such as rollback, Huggle and Twinkle, by other registered and unregistered editors who use the undo function or edit by hand, and by authors who take back their own edits (Geiger & Ribes, 2010; Halfaker & Riedl, 2012; de Laat, 2015). The second is the attribution rule that links a later revision to the edit it undoes: the Wikimedia history dumps search a page's entire history, the mwreverts library (Halfaker, n.d.) searches the last 15 revisions, and since 2020 the MediaWiki software tags reverted revisions itself. The third is the observation window. Research on the validity of digital trace data has shown that decisions of this kind, taken in preprocessing and often undocumented, can drive results (Howison et al., 2011; Hill & Shaw, 2014; Geiger & Halfaker, 2017; Sen et al., 2021), and measurement theory asks that an operationalization be justified against the construct it claims (Jacobs & Wallach, 2021). For reverts, the accuracy of detection has been examined (Ekstrand & Riedl, 2009; Flöck et al., 2012; Kiesel et al., 2017). That reverters are of different kinds is also established: Halfaker and Riedl (2012) described the division of reverting among bots, tool users and others in the English edition, and Halfaker et al. (2013) modeled tool and bot reverts as distinct exposures for newcomers. What has not been measured is how far the indicator, and conclusions drawn from it, move with the three decisions, in more than one language edition and under more than one attribution rule.

This study asks three questions. How are the decisions handled and reported in published work? Holding the measured edits fixed, how far do the newcomer revert rate, editor rankings and the association between being reverted and staying move when the decisions change? And are reverts made by different classes of reverter the same kind of event, in what follows them and in whom they affect? The first is answered with a structured review of practice, the others with a fixed-edit audit of 3.2 million newcomer first edits in seven language editions, in the spirit of a multiverse or specification-curve analysis (Steegen et al., 2016; Simonsohn et al., 2020). Four editions were explored, hypotheses were then registered, and three editions were opened afterwards.

The contribution is a specification of what this indicator of quality work indicates. Two findings are new and empirical: the software's own revert tag records a revert only when the reverting edit is trusted or patrolled, so that its coverage depends on who reverted and on the edition's patrolling regime; and the apparent effect of the observation window reverses between the two attribution rules in common use. Two are measured compositions with consequences for interpretation: the shares of reverts made by each class of reverter in each edition, and the differing later activity of the newcomers each class reverts. The paper ends with a reporting checklist tied to the construct an analyst intends to measure.

## Conceptual background

### One trace, four constructs

Stvilia et al. (2007) define information quality relative to activities and their contexts, and Mai (2013) argues that quality cannot be read off an information object without reference to the conversation in which it is used. Applied to reverts, the trace is produced by quality work but is not itself a quality score.

The constructs for which the revert is used were coded for every study in the review reported in the next section (Table 1). Four account for 36 of 41 studies. As a *quality judgment on the edit*, every revert that removes the edit counts, whoever made it, though a self-revert is a different judgment from a rejection by others. As *conflict* between editors or over an article (Kittur et al., 2007; Yasseri et al., 2012), reverts by bots and reverts of vandalism are not disputes, and mutual or repeated reverts matter more than single ones. As *the contributor's experience of rejection*, in research on newcomer socialization and retention (Choi et al., 2010; Halfaker et al., 2013; Morgan & Halfaker, 2018), self-reverts should not count and the mode of rejection matters, since a rollback within seconds and a hand-written correction are different encounters. As *human quality-work effort*, in studies of how communities and algorithms share governance (Müller-Birn et al., 2013; Zheng et al., 2019), bot reverts are a separate category and the status of one-click tools has to be decided, because a tool revert is a human judgment delivered with machine assistance (Halfaker & Riedl, 2012).

**Table 1.** Constructs a revert is used to indicate in 41 reviewed studies, the reverter population each implies, and how many studies using the construct leave the relevant choices unstated. Five studies use the revert for other purposes.

| Construct | Studies | Reverter population implied | No statement on bot, tool or self-reverts | No observation window stated |
|---|---|---|---|---|
| Quality judgment on the edit | 11 | All reverters; self-reverts reported separately | 7 | 6 |
| Conflict | 13 | Human reverters other than the author; vandalism reverts set apart | 4 | 13 |
| Contributor's experience of rejection | 9 | Others only; mode (bot, tool, manual) distinguished | 3 | 5 |
| Human quality-work effort | 3 | Humans; bots separate; tools decided explicitly | 1 | 2 |

### Detecting and attributing reverts

The identity revert, an edit that returns a page to a byte-identical earlier state, is the standard operationalization (Kittur et al., 2007); Ekstrand and Riedl (2009), Flöck et al. (2012) and Kiesel et al. (2017) examined its accuracy and proposed alternatives. Two implementations dominate. The mwreverts library searches a window of 15 revisions, a convention that goes back to Priedhorsky et al. (2007), who limited the distance between a damaged revision and its repair to 15 revisions on the stated assumption that essentially all damage is repaired within that span. The `mediawiki_history` dataset (Wikimedia Foundation, 2026) instead marks a revision as reverted if any later revision of the page restores a state that preceded it, with no radius and no time limit. A third source is the `mw-reverted` change tag, enabled on all Wikimedia wikis on 15 September 2020 (Endnote 2), which the software applies when it recognizes the reverting edit as an undo, a rollback or a manual revert within 15 revisions.

The rules differ in what they attribute. Under the unbounded rule, an edit removed by one revert can be "reverted" again years later by any revision that returns the page to a still earlier state; under the radius rule this is rare. The difference is immaterial for asking whether an edit was ever undone and decisive for asking who undid it and when.

### Automation and edition differences

Geiger and Halfaker (2013) used an outage of the anti-vandalism bot ClueBot NG in the English edition as a natural experiment and found that edits made during the outage were eventually reverted, but more slowly. Their design compares periods with and without the bot. It does not follow that, in data where the bot is present, discarding its reverts after the fact shows what humans would have done. Language editions also differ in institutions that shape reverting. Some hold edits by new and unregistered users for review through FlaggedRevs (Tran et al., 2022), some patrol recent changes, the rollback right is granted on different terms, and communities differ in norms of interaction (Hara et al., 2010). An indicator compared across editions inherits these differences.

## How reverts are operationalized in published work

### Procedure

I reviewed empirical studies and official Wikimedia analyses from 2005 to 2026 in which a revert-based measure is an outcome, an exposure, a label, a conflict indicator or a key descriptive quantity. The search had two stages. The first followed the citation networks of the methodological works cited above and keyword searches of OpenAlex, and yielded 34 studies whose methods text could be read. Because that stage favored computing venues, the second searched OpenAlex for information science and neighboring journals (six queries, 911 records, and a title search with 258) and assessed 79 candidates; seven were added, and 40 could not be assessed because the full text was not accessible, which is a limit on coverage. Three further studies are listed but not tallied: two whose full text could not be read and an earlier conference report of the Stvilia et al. sample. The set is a structured sample of 41 studies (26 published before 2019, 15 since; 23 on the English edition only), not a census.

Each study was coded for detection rule, treatment of reverts made by bots, by one-click tools and by the author, observation window, sensitivity analysis over these choices, and the construct the revert stands for. A choice was coded as stated only if a sentence in the article or its supplement establishes it; that sentence is quoted in the released table (Table S1). First-pass coding was produced by a language model from the full texts. All codes were then checked against the quoted sentences, which changed codes in 7 of the first 34 studies. As a reliability check, a separate model instance without access to the first codes coded a random 13 studies: the two passes agreed on 72 of 78 judgments, completely on the three reverter choices (κ = 1.00) and less on detection rule (κ = .78), window (κ = .61) and sensitivity analysis (κ = .59); the six disagreements were resolved against the source text. Agreement between two model passes is weaker evidence than agreement between two trained human coders, and the tallies should be read with that in mind.

### Findings

**Table 2.** Reporting of revert operationalization in 41 studies, 2005 to 2026.

| Choice | Stated | Not stated |
|---|---|---|
| Detection rule | 27 (identity hash 16; hash plus edit summaries 3; dump field 3; rollback or undo actions only 2; diff-based 2; edit summaries only 1) | 14 |
| Search radius, in the 19 studies using a hash rule | 1 (3 more use a library default without reporting it) | 15 |
| Reverts made by bots | 10 (modeled separately 5; excluded 3; counted 2) | 31 |
| Reverts made with one-click tools | 4 (modeled separately 2; counted 2) | 37 |
| Self-reverts | 15 (excluded 14; counted 1) | 26 |
| Observation window | 11 (time-bounded 4; revision-bounded 3; unbounded 4) | 30 |
| Sensitivity analysis over any revert choice | 9 (full 2; partial 7) | 32 |
| Sensitivity analysis over the reverter population | 0 | 41 |

Fourteen studies do not state how reverts were detected, and of the 19 that use a hash rule one reports the search radius (Table 2). Thirty-one do not say whether reverts made by bots are counted. Where bots are mentioned it is usually as authors: eleven studies remove bot-authored edits from the sample, and nine of these are silent on reverts that bots perform. Three studies exclude bot reverts from the measure (West et al., 2010; Yasseri & Kertész, 2013; Tsvetkova et al., 2016), five treat the type of reverter as a variable or focus on it, and thirty-seven say nothing about one-click tools. Self-reverts are the most often addressed and, when addressed, almost always excluded. Thirty studies state no observation window; of the four with a time bound, three use 48 hours. Nineteen studies state nothing about bot, tool or self-reverts, no study reports detection rule, reverter treatment, window and radius together, and none varies the reverter population as a sensitivity analysis. The one study from this journal in the sample, Stvilia et al. (2007), is typical of the record and not an exception to it.

Read against the constructs (Table 1), the gaps fall where they matter. All 13 studies that use reverts as conflict leave the window unstated, and nine of them do not say whether bot reverts are counted. Eight of the nine studies of contributors' experience say nothing about one-click tools, the mode of rejection that the audit below finds most strongly associated with not returning. Two of the three studies of human effort do not say whether bot reverts are included.

Three features of this record shape the audit. First, the exclusions actually made in the literature are of self-reverts, commonly, and of bot reverts, rarely. No study excludes tool-assisted reverts, although Halfaker et al. (2013) and Geiger and Halfaker (2013) model them separately. The audit therefore sizes every reverter class, treats self-revert and bot exclusion as practices, and treats tool exclusion as a hypothetical filter that shows what the indicator contains. Second, where a time window is stated it is now usually 48 hours, in two cases with reference to a single study of the English edition. Third, no study notes the conditions under which the `mw-reverted` tag is applied.

## Method

### Data and cohort

The data are the `mediawiki_history` dumps of version 2026-09 (Wikimedia Foundation, 2026). Each row is a revision, page or user event; the column order (78 fields) was taken from the source code of the Wikimedia Analytics Refinery because the published documentation described an older schema (Endnote 1). Seven editions were processed: English from January 2018 to September 2026 (643 million revision rows; reverts to states older than 2018 are therefore not detected in English) and the complete histories of Italian, Korean, German, Polish, French and Japanese.

The unit is a registered editor whose first edit in any namespace was made in the article namespace; that edit is the measured edit. Editors whose first edit was elsewhere (6.5 to 13.1 percent of first-time editors) are outside the cohort, as are unregistered and temporary accounts and accounts flagged as bots. The primary cohort is self-created accounts whose first edit dates from 1 January 2019 to 31 March 2026, leaving at least 180 days of follow-up: 3,246,958 editors (Table 3). First edits are the population for which revert indicators are most often computed in research on newcomers, and one edit per editor makes the editor the unit of inference. First edits that create a page cannot be identity-reverted, since removal is by deletion; their share is reported by edition and rates are also given for edits to existing pages (Table S2).

### Attribution rules

Three rules are compared. The *dump rule* is the `revision_is_identity_reverted` flag with the identifier of and delay to the first reverting revision. Reading the refinery source established that the flag groups a page's revisions by content hash over its entire history; the first occurrence of a hash is a base, later occurrences are reverts to that base, and a revision is reverted if a later revert has a base that precedes it. A revision whose parent is the previous revision with the same hash is not counted as a revert, a filter added to the source in mid-2026 (Endnote 1). I reimplemented the rule from the hashes and compared it with the flag on all Korean first edits and on year-stratified samples of 60,000 first edits in each other edition: status agreed on all but 0 or 1 edits in the five other editions with complete histories, on 99.98 percent in Korean and 99.9 percent in English. The *radius rule* applies the mwreverts convention of 15 revisions to the same recomputation. The *tag rule* is the `mw-reverted` tag on the measured edit.

### Reverter classes

The first revert of each measured edit is assigned to one class, in this order: *bot* (the dump's bot flags, current or historical); *one-click tool* (the reverting revision carries the `mw-rollback`, `huggle` or `twinkle` change tag); *self* (the reverting account is the author); *unregistered* (edits made without an account, including temporary accounts where an edition has introduced them); and *other manual* (any other registered account, including those using the undo function). Tool identification rests on tags whose availability differs: rollback is tagged in all seven editions throughout the period; Huggle is tagged in English and French, and in the English data almost no revisions carry the tag in 2021 and 2022; Twinkle is tagged only in English and only from September 2020, and it works through the undo interface. Tags of other tools were searched for and their counts are given in Table S3. In five editions the tool class is therefore the exercise of the rollback right, and English estimates are given for first edits from 2021 as well as for the whole period. Because a few accounts can make a large part of an edition's tool reverts, class shares are reported with the number of reverting accounts, the share of the most active one, and intervals from a bootstrap that resamples reverting accounts.

### Quantities

For a window W, p(W) is the share of measured edits reverted within W. Excluding a class in the *strict* sense recodes edits first reverted by that class as not reverted; the change in p equals the class's share of first reverts times p. This is an identity, reported as a description of what the indicator contains. The *replace* variant, the object of the registered tests, instead looks for the first later revert by a non-excluded reverter. To learn what such later reverts are, I record for every first revert the next manual revert of the same measured edit by a third party (neither the author nor the account that made the first revert), by class of the first reverter and under both attribution rules, with the clock started at the measured edit and, alternatively, at the first revert. Follow-up after manual first reverts is the comparison for follow-up after bot and tool reverts. The comparison is descriptive: pages where tools are used are busier, so rates are also given within terciles of page activity in the 30 days after the first revert.

Downstream quantities are the share of editors who edit again between day 2 and day 60, by class of first revert within 24 hours, with accounts blocked within 60 days separated; the rank agreement of editor-level success rates (one minus the reverted share of an editor's article edits in the first 90 days, for editors with at least ten) with and without tool and bot reverts; and tag coverage, the share of reverts found by the radius rule whose measured edit carries no `mw-reverted` tag, for first edits from October 2020, by class of reverter, by whether the reverting account held a user group that carries the autopatrol right at the time of the revert, and by the edition's patrolling regime read from the Wikimedia configuration (Endnote 2). User groups and block events were not kept in the first pass and were extracted afterwards by streaming the same dump version. Intervals are Wilson intervals for shares and percentile intervals from 2,000 bootstrap resamples of editors for ratios. Quantities that need page histories use the 60,000-edit samples (all 47,629 Korean first edits with a usable history). Cells with fewer than 50 edits are not reported, as registered.

### Registration and its limits

Design, hypotheses and code were registered on Zenodo (https://doi.org/10.5281/zenodo.23720117) after English, Korean, French and German had been analyzed and before the outputs for Japanese, Polish and Italian were opened. The registration is a hold-out replication with thresholds set from the exploratory editions, not a blind preregistration; the held-out editions had already been processed by the batch driver, and that their outputs were unopened is documented only by my own logs (Supplement, Section S1, which also lists all deviations). Four hypotheses were registered. H1: the replace effect of excluding bots and tools is larger within 24 hours than in the unbounded window (ratio R of unbounded to 24-hour effect below 1). H2: the share of bot- or tool-reverted edits later reverted by a human within 24 hours is below .25. H3, a descriptive criterion: the tag and radius rules agree on at least 95 percent of edits, and more than half of the edits the dump rule marks reverted but the tag does not lie beyond the radius. H4: the odds ratio of retention for reverted versus non-reverted edits varies by a factor of at least 1.5 across nine filter-by-window cells. Decisions use one-sided 95 percent bootstrap bounds with Holm adjustment over H1, H2 and H4 within edition. All four outcomes are reported. Every other analysis, including those by reverter class, under the radius rule and of tag coverage, was designed after the first results and is exploratory in all seven editions; tables and figures carrying exploratory results are labeled.

### Transparency

Code, cell-level aggregates, the review table, figure data, logs and the deviation log are public (https://github.com/beatsbywoni/wiki-revert-audit; archived release, Jeong, 2026). Editor-level files are not released, a departure from the registration that is recorded in the deviation log, and usernames of reverting accounts were used only to identify self-reverts and are not retained in outputs. The study uses public edit histories, reports aggregates only and involved no interaction with editors; it was not submitted for ethics review on that ground. Generative AI (Claude, Anthropic; model versions and dated tasks are in the public AI assistance log) was used for three tasks: drafting analysis code, drafting and editing prose, and first-pass and reliability coding of the literature review as described above. It was not used to generate, alter or impute data; every reported number is produced by the released deterministic code from unmodified dumps. I specified the design, made the analytic decisions, checked the code against the primary sources cited and against the independent recomputation reported above, and am responsible for every statement. The study received no funding, and I declare no competing interests.

## Results

### What a revert rate is made of

Within 24 hours, 14.0 percent (Japanese) to 37.0 percent (English) of newcomer first edits were reverted (Table 3, Figure 1). The first revert came from a bot in 12.2 percent of cases in English and 4.2 percent in French, where anti-vandalism bots operate, and in at most 0.3 percent elsewhere. One-click tools made 24.7 percent (Japanese) to 52.5 percent (Italian) of first reverts. The newcomers themselves made 2.7 to 11.4 percent and unregistered editors 1.2 to 9.6 percent; the remainder, 28.9 to 64.3 percent, were manual reverts by other registered editors, 48 to 71 percent of them through the undo function.

**Table 3.** Cohorts and composition of first reverts within 24 hours (dump rule, all first edits of self-created accounts, 2019 to March 2026). Shares are of first reverts; the strict effect of excluding a class, in percentage points, is its share times p. Editions marked * were held out for registered tests.

| Edition | First edits | p(24 h) | Bot | One-click tool | Other manual | Unregistered | Self |
|---|---|---|---|---|---|---|---|
| English | 2,189,284 | .370 | .122 | .448 | .364 | .023 | .044 |
| Italian* | 135,400 | .342 | .000 | .525 | .407 | .024 | .044 |
| Korean | 47,633 | .216 | .003 | .516 | .289 | .096 | .096 |
| German | 236,903 | .256 | .001 | .410 | .545 | .017 | .027 |
| Polish* | 67,755 | .222 | .001 | .315 | .616 | .030 | .038 |
| French | 346,938 | .243 | .042 | .255 | .643 | .012 | .047 |
| Japanese* | 223,045 | .140 | .001 | .247 | .558 | .080 | .114 |

[Figure 1 here]

**Figure 1.** Newcomer first edits reverted within 24 hours, by who made the first revert, as a percentage of all first edits. Segment widths are the strict effects of excluding each class. Asterisks mark editions held out for registered tests.

The practices found in the literature therefore have small and edition-specific effects. Excluding bot reverts lowers the 24-hour rate by 4.5 points in English, 1.0 in French and less than 0.1 elsewhere. Excluding self-reverts lowers it by 0.7 (German) to 2.1 points (Korean). The hypothetical exclusion of one-click tools would lower it by 3.4 (Japanese) to 17.9 points (Italian), and counting undo as a tool would add 5.7 to 11.7 points more (Table S3). In English the tool share rises from .448 to .524 for first edits from 2021, when Twinkle reverts are tagged; the whole-period figure understates it. These are compositional facts, not effects: they say that between a quarter and a half of what a newcomer revert rate counts is the use of one-click tools, almost none of it outside English and French is bot activity, and a non-trivial part is newcomers correcting themselves.

### Later reverts do not replace excluded ones

If a class of reverts is excluded, does a later revert by someone else take its place? Under the dump rule, a later manual revert of the same first edit followed 8.9 to 14.5 percent of bot or tool first reverts within 24 hours and 19.8 to 38.5 percent in the unbounded window (Table 4). The registered H2, that this share is below .25 within 24 hours, was supported in the three held-out editions (Japanese .145, one-sided 95 percent upper bound .157; Polish .111, .119; Italian .114, .119).

The placebo shows what this quantity is. After a *manual* first revert by another editor, a further manual revert followed 9.1 to 23.9 percent of cases within 24 hours and 18.7 to 41.9 percent in the unbounded window. Follow-up was more frequent after manual than after automated first reverts in English, Italian, Korean, French and Japanese, about equal in German and less frequent in Polish (Figure 2); nowhere is it concentrated after automation. The follow-up revert is not a human response to automation. Its composition says the same. Of all first edits first reverted by a bot or tool, only 1.2 to 4.4 percent (12.7 percent in Korean) were reverted again after their content had been reinstated; the other follow-up events were reverts that reached further back or that undid unrelated later edits, which the dump rule attributes to every earlier revision they span. Under the radius rule follow-up is rare whoever reverted first: 1.7 to 6.3 percent within 24 hours and 2.7 to 7.4 percent unbounded after bots and tools, 0.8 to 5.1 and 1.1 to 6.4 percent after manual reverts.

**Table 4.** Follow-up manual reverts and the window ratio R under two attribution rules. Follow-up: share of first edits first reverted by the class shown that were later reverted manually by another editor, unbounded window. R: replace effect of excluding bots and tools in the unbounded window divided by the effect within 24 hours, with 95 percent bootstrap intervals.

| Edition | Follow-up after bot or tool, dump rule | Follow-up after manual, dump rule | Follow-up after bot or tool, radius rule | Follow-up after manual, radius rule | R, dump rule | R, radius rule |
|---|---|---|---|---|---|---|
| English | .217 | .282 | .027 | .027 | .92 [.92, .93] | 1.05 [1.04, 1.05] |
| Italian* | .279 | .318 | .044 | .036 | .84 [.83, .85] | 1.02 [1.02, 1.03] |
| Korean | .385 | .419 | .074 | .064 | .78 [.76, .79] | 1.07 [1.07, 1.09] |
| German | .198 | .187 | .033 | .011 | .92 [.91, .93] | 1.04 [1.03, 1.04] |
| Polish* | .280 | .217 | .060 | .017 | .88 [.86, .89] | 1.07 [1.06, 1.08] |
| French | .279 | .293 | .034 | .022 | .86 [.84, .87] | 1.04 [1.03, 1.05] |
| Japanese* | .258 | .320 | .070 | .040 | .92 [.90, .94] | 1.05 [1.04, 1.06] |

[Figure 2 here]

**Figure 2.** First edits with a later manual revert by another editor, by who made the first revert, under the dump rule (top) and the 15-revision radius rule (bottom), within 24 hours (left) and unbounded (right). Bars are 95 percent Wilson intervals. Note the different horizontal scales.

### The window effect depends on the attribution rule

The registered H1 predicted that the replace effect of excluding bots and tools shrinks as the window lengthens. Under the dump rule it did, in all three held-out editions: the difference between the 24-hour and unbounded effects was 0.24 points in Japanese (one-sided 95 percent lower bound 0.19), 0.77 in Polish (0.68) and 2.49 in Italian (2.36), and R was .92, .88 and .84 (Table 4). Under the radius rule the direction reverses in all seven editions: R ranges from 1.02 to 1.07, with every interval above 1. With a fixed 180-day window in place of the unbounded one the pattern is the same (Table S4). H1 is thus supported as registered and not robust to the attribution rule; because R is an algebraic function of the follow-up shares at the two windows, H1 and H2 are one finding, not two. What can be said without qualification is that the size of a class's contribution does not fade with a longer window under either rule, and that whether it appears to shrink or grow is a property of the rule.

### Reverts by different classes are different events

Newcomers whose first edit was not reverted within 24 hours edited again on days 2 to 60 in 17.1 to 26.6 percent of cases (Figure 3). Of those reverted with a one-click tool, 3.5 to 8.6 percent did; of those reverted manually by another registered editor, 10.4 to 14.2 percent; of those who reverted themselves, 11.3 to 19.9 percent. Expressed as odds ratios against non-reverted newcomers, tool reverts range from 0.10 to 0.38, manual reverts by others from 0.41 to 0.71 and self-reverts from 0.55 to 0.68 (Table S5). These are associations: tools are aimed at vandalism, and the edits they remove differ from those corrected by hand. The point for measurement is that a single "reverted" category averages over events whose relation to the contributor's future differs by a factor of 1.4 to 4 in odds.

[Figure 3 here]

**Figure 3.** Newcomers who edited again on days 2 to 60, by who made the first revert of their first edit within 24 hours. Bars are 95 percent Wilson intervals; the grey line spans the classes within an edition.

This is what moves downstream estimates when the reverter population changes. The registered H4 compared nine cells (all reverts, without bots, without bots and tools; 24 hours, 7 days, unbounded). The ratio of the largest to the smallest odds ratio was 1.84 [1.79, 1.89] in Japanese and 1.78 [1.72, 1.85] in Italian, above the registered 1.5, and 1.43 [1.37, 1.49] in Polish, below it; the exploratory values were 1.51 to 1.79, and 3.01 in Korean. The movement is compositional: recoding tool-reverted newcomers, the group least likely to return, as not reverted raises the odds ratio mechanically, and the longer windows in these cells overlap the outcome period, so only the 24-hour cells have a clean temporal order. Editor-level rankings shift for the same reason. Among editors with at least ten article edits in 90 days (5,781 in Polish to 204,717 in English), the rank correlation between success rates with and without bot and tool reverts was .75 to .94, and 25 to 56 percent of the lowest decile changed membership.

### The tag rule depends on who reverted

The tag and radius rules agreed on 98.6 percent of first edits in Japanese, 97.9 in Polish and 95.4 in Italian, meeting the first clause of H3. The second clause was rejected in all three: of the edits that the dump rule marked reverted and the tag did not, 42, 9 and 7 percent lay beyond the radius, against the registered expectation of more than half, which had been derived from Korean.

The exploratory follow-up locates the gap. The MediaWiki manual states that the tag is applied by a deferred job once the reverting edit is approved: immediately if the reverter has the autopatrol right, and otherwise when another user patrols the edit, so that "reverts that are not patrolled will not be marked with the reverted tag"; the job also skips reverts deeper than 15 revisions and reverting edits that are themselves reverted or deleted (MediaWiki, n.d.). Tag coverage follows this rule closely (Figure 4). For first edits from October 2020, the share of radius-rule reverts whose measured edit carries no tag was 0.3 to 1.0 percent in English, Korean and Japanese, which do not patrol edits; 2.4 and 3.9 percent in German and Polish, which use FlaggedRevs; and 9.6 and 7.0 percent in Italian and French, which patrol recent changes. By reverter the contrast is starker. In Italian and French, 79 and 72 percent of reverts by unregistered editors and 71 and 73 percent of newcomers' self-reverts were untagged, against 11 and 3 percent of manual reverts by other registered editors and under 1 percent of tool reverts. In German and Polish the figures for unregistered reverters were 24 and 29 percent, and in the three editions without patrolling at most 0.2 percent. Patrol status itself is not in the dumps, and seven editions cannot separate the regime from other differences between communities; but the mechanism is documented in the software and the pattern by reverter class is what it predicts.

[Figure 4 here]

**Figure 4.** Reverts found by the 15-revision radius rule whose reverted edit carries no `mw-reverted` tag, first edits from October 2020, by who made the revert and by the edition's patrolling regime. Bars are 95 percent Wilson intervals. Exploratory.

## Discussion

### What the indicator indicates

Returning to the three constructs: as a *quality judgement on the edit*, the revert flag performs as intended only in its most inclusive form, and even then 3 to 11 percent of the judgements are the authors' own. As *the contributor's experience of rejection*, it mixes encounters that differ both in kind and in what follows them: a newcomer reverted with a one-click tool and a newcomer corrected by hand are 1.4 to 4 times apart in their odds of returning, and the edition determines which encounter is typical, a tool in Italian, Korean and English, a manual revert in Polish, French and Japanese. As *human quality-work effort*, the flag needs the least adjustment where it is most often adjusted: bots account for a material share of first reverts only in English and French, while the unsettled question, whether a rollback is human work, concerns a quarter to a half of all reverts everywhere. The review found that published studies seldom say which of these they mean, and Table 1 is offered as a way to say it.

Two results concern what cannot be recovered by analysis. Excluding a class of reverts after the fact does not produce the indicator that would have been observed without that class: later reverts by others follow at similar rates whoever acted first, and most of them are not about the same content. The window, on which practice has converged, matters less than the rule by which reverts are attributed, and the apparent fading of a filter's effect over time is produced by the unbounded rule's attribution of deep reverts to every revision they span. Neither rule is wrong. The unbounded rule answers whether content was ever removed, the radius rule answers who removed it; analysts using the history dumps for the second question inherit the first rule unless they recompute.

### Implications

For studies of quality work and of human-bot collaboration in knowledge communities (Stvilia et al., 2008; Gao et al., 2026), the practical consequence is to report the composition of reverts by reverter class alongside any rate, and to choose exclusions from the construct, not from convention. For comparative work, the indicator is not edition-neutral: tool shares reflect how each community grants the rollback right and which tools are tagged, FlaggedRevs changes what an unreviewed edit and its revert mean (Tran et al., 2022), and a 48-hour window validated on English is applied elsewhere without test.

The tag result is the most immediately usable. The `mw-reverted` tag is the cheapest revert indicator, since it needs no recomputation, and in editions that patrol edits it systematically omits reverts by unregistered and newly registered people. A comparison of tag-based revert rates between, say, French and English will read a configuration difference as a difference in reception, and a model trained on the tag will learn that reverts by unpatrolled editors did not happen.

Beyond Wikipedia the argument can only be stated as a conjecture. Indicators built from later events, such as removals and flags on platforms that combine automated and human moderation (Jhaver et al., 2019; Gorwa et al., 2020), have the same structure, and the same questions about who acted and by which rule an action is tied to a contribution apply to them. Whether excluded automated actions are followed by human ones there is an empirical matter that this study does not address.

### A tiered reporting checklist

The review suggests that a short list with a low entry cost is more likely to be used than an ideal one, in the manner of earlier calls for reporting standards in this field (Geiger & Halfaker, 2017; Geiger et al., 2020). Table 5 separates what any study can state from what requires recomputation.

**Table 5.** Reporting checklist for revert-based indicators.

| Tier | Item |
|---|---|
| Always (no extra computation) | 1. The construct the revert stands for (Table 1). |
| | 2. The attribution rule: source field, library and radius, or tag. |
| | 3. The observation window and its justification for the editions studied. |
| | 4. Whether reverts by bots, by one-click tools and by the author are counted. |
| When reverter data are available | 5. The share of reverts made by each reverter class, since excluding a class changes the rate by that share. |
| | 6. Outcomes separately by reverter class when the construct is the contributor's experience. |
| When page histories are available | 7. Results under both an unbounded and a radius rule if timing or the identity of the reverter matters. |
| For tag-based indicators | 8. The edition's patrolling regime and the period of tag availability; a coverage check against a hash-based rule. |

### Limitations

The measured edits are first edits of self-created accounts, so the audit says nothing directly about established editors or article-level conflict measures, where shares will differ. Reverter classes rest on bot flags and change tags: unflagged bots are few (reverts within 5 seconds by non-bot accounts are 0.1 to 0.7 percent), but tools without a tag are counted as manual, the tool class means rollback in five editions and more in English, and the English tags are incomplete before 2021. Edit filters, which stop some edits before they are saved (Vaseva & Müller-Birn, 2020), remove cases from the data altogether. An identity revert is not a human judgement that an edit was bad (Flöck et al., 2012), and partial reverts are missed by all hash-based rules; in the other direction, 0.6 to 4.2 percent of tagged first edits had no identity revert within the radius. The follow-up classification identifies reinstatement by exact content only. The registration fixed thresholds chosen from exploratory data and cannot demonstrate that the held-out outputs were unseen; the most informative analyses here are exploratory and should be replicated on other editions and on later dumps. The retention comparison is descriptive, and blocked accounts, which cannot return, are not separated. A coincidence of high newcomer inflow and tool reverting in Korean from mid-2023 to 2024 is documented in the supplement (Figure S2) without an explanation. Finally, the review of practice is a structured sample, not an exhaustive census, and its coding of unstated choices depends on reading methods sections that may describe procedures elsewhere.

### Conclusion

A revert is evidence of information quality work, and like other evidence it depends on who produced it and by what procedure it was recorded. The audit shows that a newcomer revert rate is a mixture of acts by bots, tool users, other editors and the newcomers themselves, in proportions that differ across language editions; that the contributors affected by each class differ in what they do next; that removing a class is not made good by later reverts; that the apparent effect of the observation window is a property of the attribution rule; and that the software's own record omits most reverts by unpatrolled editors where patrolling is used. Stating the construct, the reverter population and the rule costs a sentence each, and it is what makes revert-based findings comparable.

## Data availability statement

The data that support the findings are openly available from the Wikimedia Foundation at https://dumps.wikimedia.org/other/mediawiki_history/ (version 2026-09). Code, aggregates, the review table, figure data, logs and the registration (https://doi.org/10.5281/zenodo.23720117) are available at https://github.com/beatsbywoni/wiki-revert-audit and archived at Zenodo (https://doi.org/10.5281/zenodo.24054641). Editor-level derived data are not released because they could be re-identified from public edit histories; the code regenerates them from the dumps.

## Endnotes

1. Column order and the identity-revert rule were read from the Wikimedia Analytics Refinery source (`MediawikiEvent.scala`, method `toTSVLine`; `DenormalizedRevisionsBuilder.scala`), repository wikimedia/analytics-refinery-source, master branch on 26 October 2026. The filter that excludes a revision whose parent is the previous revision with the same hash was added in commits of 28 May and 3 June 2026 (Phabricator task T266374); earlier dump versions may count such revisions as reverts. Content hashes were reduced to 64 bits for the recomputation.
2. Patrolling configuration was read from the Wikimedia configuration repository operations/mediawiki-config on 28 October 2026 and rechecked on 10 November 2026: `wgUseRCPatrol` is enabled for the French and Italian editions; FlaggedRevs is installed on German, Polish and English (on English it applies to a small set of protected pages, and the edition is grouped here with those that do not patrol edits); Japanese and Korean have neither. The tag was enabled on all Wikimedia wikis on 15 September 2020; its conditions are documented in the MediaWiki manual and implemented in the core class `RevertedTagUpdateManager` (default `$wgRevertedTagMaxDepth` 15).

## References

Arazy, O., & Kopak, R. (2011). On the measurability of information quality. Journal of the American Society for Information Science and Technology, 62(1), 89–99. https://doi.org/10.1002/asi.21447

Arazy, O., Yeo, L., & Nov, O. (2013). Stay on the Wikipedia task: When task-related disagreements slip into personal and procedural conflicts. Journal of the American Society for Information Science and Technology, 64(8), 1634–1648. https://doi.org/10.1002/asi.22869

Choi, B., Alexander, K., Kraut, R. E., & Levine, J. M. (2010). Socialization tactics in Wikipedia and their effects. In Proceedings of the 2010 ACM Conference on Computer Supported Cooperative Work (pp. 107–116). ACM. https://doi.org/10.1145/1718918.1718940

Ekstrand, M. D., & Riedl, J. T. (2009). rv you're dumb: Identifying discarded work in wiki article history. In Proceedings of the 5th International Symposium on Wikis and Open Collaboration (pp. 1–10). ACM. https://doi.org/10.1145/1641309.1641317

Flöck, F., Vrandečić, D., & Simperl, E. (2012). Revisiting reverts: Accurate revert detection in Wikipedia. In Proceedings of the 23rd ACM Conference on Hypertext and Social Media (pp. 3–12). ACM. https://doi.org/10.1145/2309996.2310000

Gao, S., Qiu, J., Zhang, F., & Zhao, J. (2026). From divergence to convergence: How human–bot collaboration influences the evolution of collective knowledge in online knowledge communities. Journal of the Association for Information Science and Technology. Advance online publication. https://doi.org/10.1002/asi.70123

Geiger, R. S., & Halfaker, A. (2013). When the levee breaks: Without bots, what happens to Wikipedia's quality control processes? In Proceedings of the 9th International Symposium on Open Collaboration (pp. 1–6). ACM. https://doi.org/10.1145/2491055.2491061

Geiger, R. S., & Halfaker, A. (2017). Operationalizing conflict and cooperation between automated software agents in Wikipedia: A replication and expansion of "Even good bots fight". Proceedings of the ACM on Human-Computer Interaction, 1(CSCW), 1–33. https://doi.org/10.1145/3134684

Geiger, R. S., & Ribes, D. (2010). The work of sustaining order in Wikipedia: The banning of a vandal. In Proceedings of the 2010 ACM Conference on Computer Supported Cooperative Work (pp. 117–126). ACM. https://doi.org/10.1145/1718918.1718941

Geiger, R. S., Yu, K., Yang, Y., Dai, M., Qiu, J., Tang, R., & Huang, J. (2020). Garbage in, garbage out? Do machine learning application papers in social computing report where human-labeled training data comes from? In Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency (pp. 325–336). ACM. https://doi.org/10.1145/3351095.3372862

Gorwa, R., Binns, R., & Katzenbach, C. (2020). Algorithmic content moderation: Technical and political challenges in the automation of platform governance. Big Data & Society, 7(1), Article 2053951719897945. https://doi.org/10.1177/2053951719897945

Halfaker, A., Geiger, R. S., Morgan, J. T., & Riedl, J. (2013). The rise and decline of an open collaboration system: How Wikipedia's reaction to popularity is causing its decline. American Behavioral Scientist, 57(5), 664–688. https://doi.org/10.1177/0002764212469365

Halfaker, A., Kittur, A., & Riedl, J. (2011). Don't bite the newbies: How reverts affect the quantity and quality of Wikipedia work. In Proceedings of the 7th International Symposium on Wikis and Open Collaboration (pp. 163–172). ACM. https://doi.org/10.1145/2038558.2038585

Halfaker, A., & Riedl, J. (2012). Bots and cyborgs: Wikipedia's immune system. Computer, 45(3), 79–82. https://doi.org/10.1109/MC.2012.82

Hara, N., Shachaf, P., & Hew, K. F. (2010). Cross-cultural analysis of the Wikipedia community. Journal of the American Society for Information Science and Technology, 61(10), 2097–2108. https://doi.org/10.1002/asi.21373

Hill, B. M., & Shaw, A. (2014). Consider the redirect: A missing dimension of Wikipedia research. In Proceedings of the International Symposium on Open Collaboration (pp. 1–4). ACM. https://doi.org/10.1145/2641580.2641616

Howison, J., Wiggins, A., & Crowston, K. (2011). Validity issues in the use of social network analysis with digital trace data. Journal of the Association for Information Systems, 12(12), 767–797. https://doi.org/10.17705/1jais.00282

Jeong, H. (2026). wiki-revert-audit: Code, aggregates and logs for "Which reverts count?" [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.24054641

Jhaver, S., Birman, I., Gilbert, E., & Bruckman, A. (2019). Human-machine collaboration for content regulation: The case of Reddit Automoderator. ACM Transactions on Computer-Human Interaction, 26(5), 1–35. https://doi.org/10.1145/3338243

Kiesel, J., Potthast, M., Hagen, M., & Stein, B. (2017). Spatio-temporal analysis of reverted Wikipedia edits. Proceedings of the International AAAI Conference on Web and Social Media, 11(1), 122–131. https://doi.org/10.1609/icwsm.v11i1.14900

Kittur, A., Suh, B., Pendleton, B. A., & Chi, E. H. (2007). He says, she says: Conflict and coordination in Wikipedia. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (pp. 453–462). ACM. https://doi.org/10.1145/1240624.1240698

Mai, J.-E. (2013). The quality and qualities of information. Journal of the American Society for Information Science and Technology, 64(4), 675–688. https://doi.org/10.1002/asi.22783

MediaWiki. (n.d.). Manual:Reverts. Retrieved November 10, 2026, from https://www.mediawiki.org/wiki/Manual:Reverts

Mesgari, M., Okoli, C., Mehdi, M., Nielsen, F. Å., & Lanamäki, A. (2015). "The sum of all human knowledge": A systematic review of scholarly research on the content of Wikipedia. Journal of the Association for Information Science and Technology, 66(2), 219–245. https://doi.org/10.1002/asi.23172

Morgan, J. T., & Halfaker, A. (2018). Evaluating the impact of the Wikipedia Teahouse on newcomer socialization and retention. In Proceedings of the 14th International Symposium on Open Collaboration (pp. 1–7). ACM. https://doi.org/10.1145/3233391.3233544

Müller-Birn, C., Dobusch, L., & Herbsleb, J. D. (2013). Work-to-rule: The emergence of algorithmic governance in Wikipedia. In Proceedings of the 6th International Conference on Communities and Technologies (pp. 80–89). ACM. https://doi.org/10.1145/2482991.2482999

Priedhorsky, R., Chen, J., Lam, S. K., Panciera, K., Terveen, L., & Riedl, J. (2007). Creating, destroying, and restoring value in Wikipedia. In Proceedings of the 2007 International ACM Conference on Supporting Group Work (pp. 259–268). ACM. https://doi.org/10.1145/1316624.1316663

Sen, I., Flöck, F., Weller, K., Weiß, B., & Wagner, C. (2021). A total error framework for digital traces of human behavior on online platforms. Public Opinion Quarterly, 85(S1), 399–422. https://doi.org/10.1093/poq/nfab018

Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W. (2016). Increasing transparency through a multiverse analysis. Perspectives on Psychological Science, 11(5), 702–712. https://doi.org/10.1177/1745691616658637

Stvilia, B., Gasser, L., Twidale, M. B., & Smith, L. C. (2007). A framework for information quality assessment. Journal of the American Society for Information Science and Technology, 58(12), 1720–1733. https://doi.org/10.1002/asi.20652

Stvilia, B., Twidale, M. B., Smith, L. C., & Gasser, L. (2008). Information quality work organization in Wikipedia. Journal of the American Society for Information Science and Technology, 59(6), 983–1001. https://doi.org/10.1002/asi.20813

TeBlunthuis, N., Hill, B. M., & Halfaker, A. (2021). Effects of algorithmic flagging on fairness: Quasi-experimental evidence from Wikipedia. Proceedings of the ACM on Human-Computer Interaction, 5(CSCW1), 1–27. https://doi.org/10.1145/3449130

TeBlunthuis, N., Shaw, A., & Hill, B. M. (2018). Revisiting "The rise and decline" in a population of peer production projects. In Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems (pp. 1–7). ACM. https://doi.org/10.1145/3173574.3173929

Tran, C., Champion, K., Hill, B. M., & Greenstadt, R. (2022). The risks, benefits, and consequences of prepublication moderation: Evidence from 17 Wikipedia language editions. Proceedings of the ACM on Human-Computer Interaction, 6(CSCW2), 1–25. https://doi.org/10.1145/3555225

Trokhymovych, M., Aslam, M., Chou, A.-J., Baeza-Yates, R., & Saez-Trumper, D. (2023). Fair multilingual vandalism detection system for Wikipedia. In Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (pp. 4981–4990). ACM. https://doi.org/10.1145/3580305.3599823

Tsvetkova, M., García-Gavilanes, R., & Yasseri, T. (2016). Dynamics of disagreement: Large-scale temporal network analysis reveals negative interactions in online collaboration. Scientific Reports, 6, Article 36333. https://doi.org/10.1038/srep36333

Vaseva, L., & Müller-Birn, C. (2020). You shall not publish: Edit filters on English Wikipedia. In Proceedings of the 16th International Symposium on Open Collaboration (pp. 1–10). ACM. https://doi.org/10.1145/3412569.3412580

Warncke-Wang, M., Ho, R., Miller, M., & Johnson, I. (2023). Increasing participation in peer production communities with the Newcomer Homepage. Proceedings of the ACM on Human-Computer Interaction, 7(CSCW2), 1–26. https://doi.org/10.1145/3610071

West, A. G., Kannan, S., & Lee, I. (2010). Detecting Wikipedia vandalism via spatio-temporal analysis of revision metadata? In Proceedings of the Third European Workshop on System Security (pp. 22–28). ACM. https://doi.org/10.1145/1752046.1752050

Wikimedia Foundation. (2026). MediaWiki history dumps (Version 2026-09) [Data set]. https://dumps.wikimedia.org/other/mediawiki_history/

Yasseri, T., Sumi, R., Rung, A., Kornai, A., & Kertész, J. (2012). Dynamics of conflicts in Wikipedia. PLoS ONE, 7(6), Article e38869. https://doi.org/10.1371/journal.pone.0038869

Zheng, L., Albano, C. M., Vora, N. M., Mai, F., & Nickerson, J. V. (2019). The roles bots play in Wikipedia. Proceedings of the ACM on Human-Computer Interaction, 3(CSCW), 1–20. https://doi.org/10.1145/3359317

