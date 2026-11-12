# Which reverts count? Reverter populations, attribution rules and observation windows behind a Wikipedia indicator of information quality work

Hongwon Jeong

Center for Creative Convergence Education, Hanyang University ERICA, 55 Hanyangdaehak-ro, Sangnok-gu, Ansan, Gyeonggi-do 15588, Republic of Korea. Telephone +82-31-400-5786. Email: beatsbywoni@hanyang.ac.kr. ORCID 0009-0003-7908-7478

## Abstract

Whether an edit was reverted is a standard trace of information quality work in Wikipedia, read as quality judgment, as conflict, as the rejection a contributor experiences and as human effort. What the trace records depends on three seldom-reported choices: who counts as a reverter, how a later revision is attributed to an earlier edit, and how long edits are observed. This study measures what a revert count contains, on the first edits of 3.2 million newcomers in seven language editions. One-click tools make 25 to 52 percent of first reverts, and newcomers reverted with tools return less often than those reverted by hand. The platform's own revert tag captures this work selectively. In the Italian edition, which patrols recent changes, the tag is absent from 77 percent of manual reverts by registered editors without a recorded patrol-exempt group, against 1 percent with one. Separately, using the tag instead of a hash-based rule changes the gap between English and Italian revert rates from 3.6 to 7.4 points. These analyses are exploratory; registered tests concern a secondary question. The study contributes a specification of what a revert count contains, an account of the tag as approval-conditioned documentation, and reporting items.

**Keywords:** information quality; trace data; measurement validity; documentation; invisible work; Wikipedia; reverts

## Introduction

When Stvilia et al. (2007) proposed a framework for information quality assessment in this journal, two of the measures they derived for Wikipedia articles were built from reverts. The number of reverts entered the measure of authority and reputation, and the median time to revert defined volatility. The article does not say how a revert was identified or whose reverts were counted. Nearly two decades later the revert is a standard trace of what Stvilia et al. (2008) called information quality work in Wikipedia, and in the 41 studies surveyed below the choices on which a revert count depends are seldom reported (Table 2).

Because edits leave a trace in the public revision history, "was this edit reverted" serves as a general-purpose indicator. It is read as a judgment on the quality of an edit and as a label for training quality-prediction models (Trokhymovych et al., 2023), as a measure of conflict (Kittur et al., 2007; Yasseri et al., 2012), as the rejection a newcomer experiences (Halfaker et al., 2011, 2013), as an outcome in onboarding experiments (Warncke-Wang et al., 2023) and as evidence about how humans and automated agents share quality work (Geiger & Halfaker, 2013; Zheng et al., 2019). These uses presuppose different constructs, and information science has long held that what an indicator of quality means depends on the activity and context in which it is used (Stvilia et al., 2007; Mai, 2013). A judgment on an edit, a dispute, an experience of rejection and a quantity of human effort are not carried by the same reverts.

A revert is a relation between an edit and a later revision, so the analyst has to decide which later revisions count. The first decision is the reverter population. Wikipedia's quality work is done by bots, by trusted editors using one-click tools such as rollback, Huggle and Twinkle, by other registered and unregistered editors who use the undo function or edit by hand, and by authors who take back their own edits (Geiger & Ribes, 2010; Halfaker & Riedl, 2012; de Laat, 2015). The second is the attribution rule that links a later revision to the edit it undoes, on which the Wikimedia history dumps, the mwreverts library (Halfaker, n.d.) and the software's own revert tag differ. The third is the observation window. Research on digital trace data has shown that such preprocessing decisions can drive results (Howison et al., 2011; Hill & Shaw, 2014; Geiger & Halfaker, 2017; Sen et al., 2021), and measurement theory asks that an operationalization be justified against the construct it claims (Jacobs & Wallach, 2021). For reverts, the accuracy of detection has been examined (Ekstrand & Riedl, 2009; Flöck et al., 2012), Geiger and Halfaker (2017) showed for reverts between bots that the operationalization changes the conclusion, and that reverters are of different kinds is established for the English edition (Halfaker & Riedl, 2012; Halfaker et al., 2013). What the trace contains under each decision, across language editions and attribution rules, has not been measured.

This study asks three questions about the reverts of newcomer first edits. What share of first reverts does each class of reverter make in each edition? How completely does the software's own record of reverts, the `mw-reverted` tag, cover them, and on what does its coverage depend? And do newcomers reverted by different classes differ in later activity? A fourth, whether the effect of excluding a class of reverters depends on the window and the attribution rule, was the subject of registered tests and is reported briefly. The questions are answered with a fixed-edit audit of 3.2 million newcomer first edits in seven language editions, in the spirit of a multiverse analysis (Steegen et al., 2016; Simonsohn et al., 2020). A survey of reporting practice in 41 studies motivates the audit; it is not offered as a systematic review.

The contribution is a specification of what a revert count contains under each choice. For information science its central result concerns documentation. The tag is a record that the system itself produces about quality work, and for the reverts of newcomer first edits its coverage varies with the standing of the worker, in the pattern the documented rule predicts: where an edition patrols recent changes, a revert is tagged at once if the reverter is exempt from patrol and otherwise only if someone approves it. The condition is documented in the software manual; its extent has not, to my knowledge, been measured (Endnote 1). The other results are the share of each class of reverter in each edition and the later activity of the newcomers each class reverts.

## Background

### One trace, four readings

If quality is relative to activity and context (Stvilia et al., 2007; Mai, 2013), a trace produced by quality work is not itself a quality score. Stvilia et al. (2008) describe information quality work in Wikipedia as a division of labor among agents in different roles. A revert is the trace of one act in that work, the removal of a contribution, and the constructs for which it is used read that act from four positions (Table 1): its object (was the edit acceptable), the relation between the parties (are they in dispute), its recipient (what the contributor experienced) and its performer (who did the work). The typology is my reading of how the trace is used, and the reverter population each construct calls for is an argument, not a finding.

As a *quality judgment on the edit*, every revert that removes the edit counts, whoever made it, though a self-revert is a different judgment from a rejection by others. As *conflict* between editors or over an article (Kittur et al., 2007; Yasseri et al., 2012), reverts by bots or of vandalism should not be read as disputes without contextual validation, and mutual or repeated reverts are stronger but not conclusive evidence. As *the contributor's experience of rejection*, in research on newcomer socialization and retention (Choi et al., 2010; Halfaker et al., 2013; Morgan & Halfaker, 2018), self-reverts should not count and the mode of rejection matters. As *human quality-work effort*, in studies of how communities and algorithms share governance (Müller-Birn et al., 2013; Zheng et al., 2019), bot reverts are a separate category and the status of one-click tools has to be decided, because a tool revert is a human judgment delivered with machine assistance (Halfaker & Riedl, 2012).

**Table 1.** Four constructs a revert is used to indicate, the position from which each reads the act, and the choice of reverter population each requires an analyst to justify (the author's reading). Each construct also needs observations beyond that choice (reciprocity and repetition for conflict, time for effort).

| Construct | Position | Example | Reverter population to justify |
|---|---|---|---|
| Quality judgment on the edit | Object | Trokhymovych et al. (2023) | All reverters; self-reverts reported separately |
| Conflict | Relation | Yasseri et al. (2012) | For disputes between people: human reverters other than the author; vandalism reverts set apart |
| Contributor's experience of rejection | Recipient | Halfaker et al. (2013) | Others only; mode (bot, tool, manual) distinguished |
| Human quality-work effort | Performer | Geiger and Halfaker (2013) | Humans; bots separate; tools decided explicitly |

### Detecting and attributing reverts

The identity revert, an edit that returns a page to a byte-identical earlier state, is the standard operationalization (Kittur et al., 2007). Two implementations dominate. The mwreverts library searches a window of 15 revisions by default, a value its source attributes to Priedhorsky et al. (2007). The `mediawiki_history` dataset (Wikimedia Foundation, 2026) instead marks a revision as reverted if any later revision of the page restores a state that preceded it, with no radius and no time limit, so that an edit removed once can be "reverted" again years later by any revision that returns the page to a still earlier state. A third source is the `mw-reverted` change tag, enabled on all Wikimedia wikis on 15 September 2020 (Endnote 1), which the software applies to edits undone by an undo, a rollback or a manual revert, to a depth of 15 revisions. An unmodified undo of an edit that is no longer the latest revision is recorded as a revert although its result matches no earlier revision, so the tag and the hash-based rules are not nested.

### Approval-conditioned documentation

Quality work in peer production is partly invisible work: what a system records about work decides which work can later be seen, counted and credited (Suchman, 1995; Star & Strauss, 1999). Revert traces are such records. They are documents the platform produces as a by-product of coordination (Buckland, 1997; Geiger & Ribes, 2011), under rules that differ across language editions: some hold edits by new users for review through the FlaggedRevs extension (Tran et al., 2022), some patrol recent changes, and the rollback right is granted on different terms (Hara et al., 2010).

MediaWiki applies the `mw-reverted` tag only once the reverting edit counts as approved (MediaWiki, n.d.; Endnote 1). Where recent-changes patrolling is off, every revert is approved at once. Where it is on, a revert is approved at once if the reverter holds the autopatrol right and otherwise when someone patrols it; in the words of the manual, "reverts that are not patrolled will not be marked with the reverted tag". Under FlaggedRevs a revert is approved at once if the page is not under review, if the reverter holds the autoreview right or if it is a self-revert, and otherwise when a reviewer accepts it. The design has a reason: it keeps an unreviewed and possibly abusive revert from marking a good edit as reverted. Its consequence is that the tag documents reverts that meet the software's approval condition, which is a technical condition and not a community judgment on the particular revert. Standing, meaning a formal status that exempts an editor's edits from review whether appointed or earned automatically by tenure, then bears on whether an act of quality work is captured by the tag without anyone's further action. The revision history and the other change tags record the act in either case.

### Reporting practice

To see how the three decisions are reported, I examined 40 empirical studies and one official Wikimedia analysis, published from 2007 to 2026, in which a revert measure computed from revision histories is an outcome, an exposure, a label or a conflict indicator, or is itself the object of description (39 on Wikipedia, two on Wikia wikis). The search, the studies listed but not tallied (among them four in which reverting is one coded activity or a control variable, such as Arazy et al., 2019) and the eleven texts that could not be read are in Table S1. A language model (Claude) retrieved and screened texts, extracted passages and proposed eligibility and codes; I confirmed the list of included studies and checked the codes of every one against the source (the released coding table gives the passage behind each code). Candidates the model excluded were not re-read, the inclusion criterion was narrowed after a first tally, and the search was not logged in full. A choice counts as stated only if the article or its supplement states it for the main analysis, and as recoverable if it is fixed by a cited procedure, a library default, the data source, released code or the design of the measure. No second human coder took part and no reliability coefficient is claimed, so Table 2 describes what one reader found in these 41 studies; it is not a systematic review, and its counts are approximate.

**Table 2.** Reporting of revert operationalization in 41 studies, 2007 to 2026. The search radius is tallied for studies that detect identity reverts by hash or by definition. The observation window is tallied for the 20 studies in which the revert is an edit-level outcome, exposure or label; it does not apply in the same form to measures computed over whole article histories.

| Choice | Studies in which it applies | Stated in the article | Not stated but recoverable |
|---|---|---|---|
| Detection rule | 41 | 29 | 3 |
| Search radius | 22 | 1 | 4 |
| Reverts made by bots | 41 | 9 | 0 |
| Reverts made with one-click tools | 41 | 5 | 0 |
| Self-reverts | 41 | 16 | 5 |
| Observation window | 20 | 5 | 6 |
| Reverter population varied as a sensitivity analysis | 41 | 0 | |

Twelve studies do not state how reverts were detected, and of the 22 that use an identity rule one reports a search radius (three more cite a library whose default is 15, and one compares all pairs of revisions). The treatment of reverts made by bots is stated in nine studies: five treat the type of reverter as a variable or focus on it, two exclude bot reverts (West et al., 2010; Tsvetkova et al., 2016) and two count them explicitly; ten more remove bot accounts or bot-authored edits from the sample, which concerns who wrote the observed edits and leaves open who reverted them (Table S1). Five studies say how one-click tools are treated, and one states the treatment of bots, tools and self-reverts together (Halfaker et al., 2013). Of the 20 studies with an edit-level measure, five state an observation window; four describe the outcome as "eventually reverted" and two take it from the dumps' unbounded field. Eight studies vary some other revert choice; I found none that varies the reverter population. The exclusions actually made are of self-reverts, commonly, and of bot reverts, rarely; no study excludes tool-assisted reverts, so the audit sizes every reverter class and treats tool exclusion as hypothetical. One study builds a conflict indicator partly on the software's revert tags (Ariel, 2026); none notes the conditions under which the `mw-reverted` tag is applied.

## Method

### Data and cohort

The data are the `mediawiki_history` dumps of version 2026-09 (Wikimedia Foundation, 2026). Seven editions were processed: English from January 2018 to September 2026 and the complete histories of Italian, Korean, German, Polish, French and Japanese. Reverts to states older than 2018 are therefore not detected in English; a comparison with the dumps' own flag, which is computed on complete histories, shows that this affects 28 of 42,042 sampled first edits from October 2020.

The unit is a registered editor whose first edit in any namespace was made in the article namespace; that edit is the measured edit. Editors whose first edit was elsewhere (6.5 to 13.1 percent of first-time editors) are outside the cohort, as are unregistered and temporary accounts and accounts flagged as bots. The primary cohort is self-created accounts whose first edit dates from 1 January 2019 to 31 March 2026, leaving at least 180 days of follow-up: 3,246,958 editors (Table 3). First edits that create a page can be removed only by deletion; their share is reported (Table S2).

### Attribution rules

Three rules are compared. The *dump rule* is the `revision_is_identity_reverted` flag with the identifier of and delay to the first reverting revision. The source code shows that the flag groups a page's revisions by content hash over its entire history; the first occurrence of a hash is a base, later occurrences are reverts to that base, and a revision is reverted if a later revert has a base that precedes it (Endnote 2). I reimplemented the rule from the hashes on all Korean first edits and on samples of 60,000 first edits in each other edition, stratified by year with proportional allocation, so that unweighted sample shares estimate cohort shares (Table S12). Status agreed with the flag on at least 99.89 percent of edits in every edition; among edits reverted under both, the first reverting revision agreed in at least 99.98 percent, and no case crossed the 24-hour boundary. The *radius rule* applies the mwreverts convention of 15 revisions to the same recomputation; on synthetic page histories it returned the same first reverting revision as the mwreverts library for all 60,297 revisions checked (Table S12). The *tag rule* is the `mw-reverted` tag on the measured edit.

### Reverter classes

The first revert of each measured edit is assigned to one class, in this order: *bot* (the dump's bot flags, current or historical); *one-click tool* (the reverting revision carries the `mw-rollback`, `huggle` or `twinkle` change tag); *self* (the reverting account is the author); *unregistered* (no account, including temporary accounts); and *other manual* (any other registered account, including those using the undo function). The tool class is defined by tags, not by a common institution. The rollback right is appointed in some editions, is bundled with the automatically granted `editor` group of FlaggedRevs in German and Polish, and in Japanese belongs to a rollbacker group added by a later configuration change (Endnote 1). Rollback is tagged in all seven editions throughout; Huggle is tagged in English and French and Twinkle only in English, from September 2020 (Table S9). In five editions the class is therefore the exercise of the rollback right, while in English it also contains Twinkle, which any autoconfirmed account can use; tags of other tools are counted in Table S3.

### Quantities

For a window W, p(W) is the share of measured edits reverted within W. Excluding a class in the *strict* sense recodes edits first reverted by that class as not reverted; the change in p equals the class's share of first reverts times p, an identity. The *replace* variant, used in the registered H1 and, against the strict variant, in H2, instead looks for the first later revert by a non-excluded reverter.

Tag omission is the share of reverts found by the radius rule whose measured edit carries no `mw-reverted` tag, for first edits from 1 October 2020 to 31 March 2026 (below, from October 2020), by class of reverter, by the user groups recorded for the reverting account at the time, by the account's edit count, and by the edition's patrolling regime. Whether a group carries the autopatrol or autoreview right is taken from each edition's configuration as read in November 2026 (Endnote 1), so the grouping is a proxy for the rights held at the time of the revert. The other downstream quantity is the share of editors who edit again between day 2 and day 60, by class of first revert within 24 hours, with accounts blocked within 60 days separated.

The cohorts are complete populations, so intervals express the sampling of page histories and the sensitivity of an estimate to individual editors and reverting accounts, not inference to other editions or periods. They are Wilson intervals for shares and percentile intervals from 2,000 bootstrap resamples of editors for ratios. Because reverts cluster in reverting accounts, which these intervals ignore, the quantities on which conclusions rest are also given with intervals that resample reverting accounts (the tag results; Tables S6 and S10). Quantities that need page histories use the 60,000-edit samples (all 47,629 Korean first edits with a usable history). Shares for cells with fewer than 50 edits are not reported.

### Registration and its limits

Design, hypotheses and code were registered on Zenodo (https://doi.org/10.5281/zenodo.23720117) after English, Korean, French and German had been analyzed and before the outputs for Japanese, Polish and Italian were opened. It is a hold-out replication with thresholds set from the exploratory editions, not a blind preregistration: the held-out editions had already been processed, a sentence of the registered text that says otherwise is wrong, and that their outputs were unopened is documented only by my own logs (Section S1 of the supplement, which lists all deviations). Four hypotheses were registered for the exclusion of bots and tools together: that the effect of the replace variant is larger within 24 hours than in the unbounded window (H1); that fewer than a quarter of bot- or tool-reverted edits are later reverted by a human within 24 hours, from the replace against the strict variant (H2); that the tag and radius rules agree on at least 95 percent of edits and that most edits the dump rule marks reverted but the tag does not lie beyond the radius (H3, a descriptive criterion on detection rules); and that the odds ratio of retention varies by a factor of at least 1.5 across nine strict cells of filter by window (H4). The estimand, data, criterion and resampling of each are tabulated in Section S1. All outcomes are reported, in full in Table S7. Every other analysis, including all results on composition, tag omission and retention by class, was designed after the first results and is exploratory in all seven editions.

### Transparency

Code, aggregates, the coding table of the survey, logs and the deviation log are public (https://github.com/beatsbywoni/wiki-revert-audit; archived release, Jeong, 2026). Editor-level files are not released, a recorded departure from the registration. The study uses public edit histories, reports aggregates only and involved no interaction with editors; it was not submitted for ethics review on that ground. Generative AI (Claude, Anthropic; sessions configured for the model claude-fable-5-2, with dated tasks in the public AI assistance log) was used for three tasks: drafting analysis code, drafting and editing prose, and, in the survey of reporting practice, retrieving and screening texts, extracting passages and proposing eligibility and codes as described above. A second model (ChatGPT, OpenAI) assisted my check of four studies, two of them tallied. Model agents were also used to critique drafts, and several analyses were added in response. No model generated or altered the audit's data, and none analyzed them on its own: every number of the audit is produced by released deterministic code from unmodified dumps, long-running jobs were executed by me, and model sessions also ran the released scripts on derived files. I specified the design, made the analytic decisions, checked the code against the primary sources cited and against the independent recomputation reported above, and am responsible for every statement. The study received no funding, and I declare no competing interests.

## Results

### What a revert rate is made of

Within 24 hours, 14.0 percent (Japanese) to 37.0 percent (English) of newcomer first edits were reverted (Table 3, Figure 1). Outside English, 9 to 20 percent of first edits create a page and cannot be reverted in this sense (Table S2). The first revert came from a bot in 12.2 percent of cases in English (almost all from a single bot) and 4.2 percent in French, and in at most 0.3 percent elsewhere. One-click tools made 24.7 percent (Japanese) to 52.5 percent (Italian) of first reverts. Manual reverts by other registered editors made up 28.9 to 64.3 percent, 49 to 78 percent of them through the undo function; unregistered editors and the newcomers themselves made the rest.

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

Three qualifications apply. Outside English and German it is produced by few people (93 accounts in Korean and 103 in Japanese, the most active alone 19 and 23 percent; Table S2). In English the class is not constant over time, since Twinkle is tagged only from September 2020 and Huggle tags are nearly absent in 2021 and 2022; the share is .524 for first edits from 2021. And it is a lower bound where other tools are tagged: reverts carrying only the tags of LiveRC in French, or of four further tools in English, would add 8.5 and 3.9 points (Table S3).

### Tag omission varies with the standing of the reverter

For first edits from October 2020, the share of radius-rule reverts whose measured edit carries no tag was 0.3 to 1.0 percent in English, Korean and Japanese, where recent-changes patrolling is not enabled; 2.4 and 3.9 percent in German and Polish, which use FlaggedRevs; and 9.6 percent in Italian and 7.0 percent in French, which patrol recent changes (Figure 2; with reverting accounts resampled, 7.7 to 12.3 and 5.8 to 8.4 percent). The omission is concentrated among reverters without patrol-exempt status. In Italian and French, 79 and 71 percent of reverts by unregistered editors and 71 and 73 percent of newcomers' self-reverts were untagged, against under 1 percent of tool reverts. In German and Polish the figures were 24 and 29 percent for unregistered reverters and 13 percent for self-reverts.

Patrol and review actions were not observed. What is observed is an association between tag omission and the user groups recorded for the reverting account at the time of the revert (Table S6), in the pattern the documented approval rule predicts. Among manual reverts by other registered editors in Italian, 1.0 percent were untagged where the account held a group that carries the autopatrol right in that edition and 77 percent where it held none (752 reverts by 345 accounts; 72 to 82 percent with accounts resampled). In German and Polish, 20 and 22 percent were untagged without a group that carries the autoreview right, and in English, Korean and Japanese at most 0.2 percent without any group. French looked like an exception, with 3.7 percent, and is consistent with the same rule: that edition grants the autopatrolled status automatically at 500 edits and 90 days without recording a group (Endnote 1), and among manual reverters with no recorded group 60 to 70 percent of reverts were untagged below 500 edits, 3.4 percent between 500 and 4,999 and 0.1 percent above (account age was not available, so the edit count is a proxy for that status).

Three things are not explained by the rule as documented: a residue among reverters with standing (5.3 percent of tool reverts by group holders in Polish, 4.0 percent of manual reverts by group holders in Japanese); the untagged self-reverts under FlaggedRevs, which the manual lists as approved at once; and how many unapproved reverts are approved later, which the current software allows only where recent-changes patrolling is enabled and only while the patrol record is retained (Endnote 1). Because a later approved revert by anyone also tags the edit, the class-specific shares are lower bounds on the omission per revert. The registered H3 fits this picture: the tag and radius rules agreed on 98.6 percent of first edits in Japanese, 97.9 in Polish and 95.4 in Italian, meeting its first clause, while the second was rejected in all three (42, 9 and 7 percent of dump-only reverts lay beyond the radius, against an expected majority), in Japanese only because the registered window began before the tag existed (75 percent from October 2020; Table S10).

[Figure 2 here]

**Figure 2.** Reverts found by the 15-revision radius rule whose reverted edit carries no `mw-reverted` tag, first edits from October 2020, by who made the revert and by the edition's regime (left: neither recent-changes patrolling nor FlaggedRevs on ordinary pages). Bars are 95 percent Wilson intervals, which ignore clustering in reverting accounts (Table S6). Exploratory.

The consequence for a comparison can be computed directly. For first edits from October 2020, the share reverted under the radius rule is 39.5 percent in English and 35.9 percent in Italian, a difference of 3.6 points; with the tag it is 40.1 and 32.7 percent, a difference of 7.4 points. Of the change of 3.8 points (3.4 to 4.2 with reverting accounts resampled), about 3.2 come from Italian, where 3.44 percent of first edits are reverted under the radius rule and untagged and 0.26 percent are tagged without a radius-rule revert, and about 0.6 from English, where the two figures are 0.11 and 0.72 percent (Table S6). Nearly all English edits tagged without a radius-rule revert (292 of 301) are not identity-reverted under the dumps' own flag either. Undos of edits that were no longer the latest revision are a likely source, but the reverting revisions were not examined. The change is stable over time (3.7 points for first edits to 2024, 4.0 from 2025), and the French gap to English grows from 13.7 to 15.8 points. Neither rule is the truth, and the example, chosen because the gap is small enough for the change to show, concerns newcomer first edits only.

### Reverts by different classes reach different newcomers

Newcomers whose first edit was not reverted within 24 hours edited again on days 2 to 60 in 17.1 to 26.6 percent of cases (Figure 3). Of those reverted with a one-click tool, 3.5 to 8.6 percent did; of those reverted manually by another registered editor, 10.4 to 14.2 percent; of those who reverted themselves, 11.3 to 19.9 percent. As odds ratios against non-reverted newcomers, tool reverts range from 0.10 to 0.38, manual reverts by others from 0.41 to 0.71 and self-reverts from 0.55 to 0.68 (Table S5). Blocking does not produce the contrast: with accounts blocked within 60 days removed, the odds ratios are 0.09 to 0.38 for tool reverts and 0.40 to 0.70 for manual ones. Nor does the mix of the reference group: on the page-history samples, removing first edits that create a page, which cannot be reverted, leaves them at 0.09 to 0.37 and 0.40 to 0.67 (Table S5). These are associations between groups of newcomers, not effects of the mode of reverting: tools are aimed at vandalism, and intent, repeat accounts and accompanying warnings are not controlled. The point for measurement is that a single "reverted" category averages over events whose relation to the contributor's later activity differs, in proportions that vary by edition; across the seven complete cohorts the odds ratio for manual reverts is 1.4 to 4 times that for tool reverts, a descriptive range without an interval of its own.

[Figure 3 here]

**Figure 3.** Newcomers who edited again on days 2 to 60, by who made the first revert of their first edit within 24 hours. Bars are 95 percent Wilson intervals, which ignore clustering in reverting accounts; the grey line spans the classes within an edition. Exploratory.

### Registered tests on excluding bots and tools

The registered H1 and H2 concerned an analyst who drops bot and tool reverts and looks for the next human revert, a filter that none of the surveyed studies uses (Tables S4, S7 and S10). H2 was supported in the three held-out editions: .145, .111 and .114 of bot- or tool-reverted first edits in Japanese, Polish and Italian had a later non-bot, non-tool revert within 24 hours, below the registered .25. A manual revert by a registered third party followed 6 to 10 percent of bot and tool first reverts within a day under the dump rule and 1 to 3 percent under the radius rule. H1 was supported under the dump rule (ratios of the unbounded to the 24-hour effect of .92, .88 and .84), but under the radius rule the ratio is 1.02 to 1.07 in all seven editions, with every account-resampled interval above 1. The reversal is largely arithmetic: under the unbounded rule later reverts that reach back past the measured edit accumulate with time, so H1 describes that rule more than it describes reverting, and analysts who take the reverting revision from the dumps to ask who reverted inherit it. H4, on the strict variant, was met in two of three held-out editions (ratios of the largest to the smallest odds ratio of retention of 1.84 and 1.78 in Japanese and Italian and 1.43 in Polish, against a registered 1.5), but its nine cells mix the filter with the window; across the three 24-hour cells alone the ratio is 1.30 to 1.50 and reaches 1.5 by point estimate only in Italian.

## Discussion

### What the indicator contains

For each construct the audit shows what an undifferentiated revert count contains for newcomer first edits; among the edits of established editors, from which conflict measures draw most of their reverts, the shares will differ. Read as a *quality judgment on the edit*, 3 to 11 percent of the judgments are the authors' own. Read as *conflict*, a quarter to a half of first reverts are one-click responses, made with the rollback right or, in English, also with Huggle and Twinkle. Read as *the contributor's experience of rejection*, the count mixes encounters that differ in what follows them, and by point estimate the commonest differs by edition: a tool in Italian, Korean and English, a manual revert in German, Polish, French and Japanese. Read as *human quality-work effort*, bots make a material share of first reverts only in English and French, while the status of one-click reverts concerns a quarter to a half of first reverts everywhere.

That reverters differ in kind and that tool reverts go with lower retention was known for English (Halfaker & Riedl, 2012; Geiger & Halfaker, 2013; Halfaker et al., 2013), and that operational choices can reverse a conclusion about reverts was shown for bots (Geiger & Halfaker, 2017). The audit adds the size of each component in seven editions on one operational definition. Neither attribution rule is wrong: the unbounded rule answers whether an identical earlier state was ever restored, the radius rule which nearby revision restored it.

### The tag as approval-conditioned documentation

The tag result bears on how information systems document the work done in them. The `mw-reverted` tag is the cheapest revert indicator and the only one the platform itself asserts. For the reverts of newcomer first edits in the two editions studied that patrol recent changes, it is missing for seven to ten percent of reverts and for most of those made by unregistered editors, by registered editors without patrol-exempt status and by the newcomers themselves (71 to 79 percent in Italian); in the two FlaggedRevs editions the omission for the same groups is 13 to 29 percent. In those editions an indicator built on the tag is nearly complete for the quality work of editors with standing and sparse for that of everyone else, and each community's configuration sets the boundary. In the terms of Star and Strauss (1999), such an indicator makes the quality work of some participants visible and leaves that of others out of view, although the revision history still holds it, and it does so by a rule that is reasonable in itself.

What the omission means depends on the construct (Table 1). As a quality judgment the tag may suit some purposes, since it records reverts that met the approval condition, but an analyst must know that this is what it records. As conflict it misses reverts exchanged among the least established editors. As the contributor's experience it misses rejections that happened to the newcomer whether or not anyone approved them. As human effort it undercounts the work of participants without status. Tag-based indicators are entering the literature: one surveyed study builds a conflict flag from revert tags and edit summaries for the Hebrew edition (Ariel, 2026), which also enables recent-changes patrolling (Endnote 1); its tag coverage was not measured here, and the tags placed on reverting revisions are not subject to the condition. A comparison of tag-based revert rates across editions with different regimes can read a configuration difference as a difference in reception, as the English and Italian example shows.

### Proposed reporting items

Table 4 separates what any study can state from what requires recomputation, in the manner of documentation standards with a low entry cost (Gebru et al., 2021). The items are a proposal from one audit, untested on other studies, and not a consensus guideline; the items completed for this study are in Table S11.

**Table 4.** Proposed reporting items for revert-based indicators.

| Tier | Item |
|---|---|
| Always (no extra computation) | 1. The construct the revert stands for (Table 1), from which items 3, 4 and 6 follow. |
| | 2. The attribution rule: source field, library and radius, or tag. |
| | 3. The observation window and its justification for the editions studied. |
| | 4. Whether reverts by bots, by one-click tools and by the author are counted. |
| When reverter data are available | 5. The share of reverts made by each reverter class, and how many accounts make the tool reverts. |
| | 6. Outcomes separately by reverter class when the construct is the contributor's experience. |
| When page histories are available | 7. Results under both an unbounded and a radius rule if timing or the identity of the reverter matters. |
| For tag-based indicators | 8. The edition's patrolling regime and autopatrol rules, the period of tag availability, and a coverage check against a hash-based rule. |

### Limitations

The measured edits are first edits of self-created accounts, so the audit says nothing directly about established editors or article-level conflict measures, and the tag results rest on two editions with recent-changes patrolling and two with FlaggedRevs. The account of the tag omission rests on an association with recorded user groups and edit counts under the configuration of 2026; the public patrol and review logs were not joined, and edits tagged without a hash-based revert were counted but not examined. Reverter classes rest on bot flags and change tags: tools without a tag are counted as manual, the English tags are incomplete before 2021, and holders of global rights appear without a local group. Edit filters and deletions remove cases before they can be reverted, and partial reverts escape all hash-based rules. Resampling reverting accounts widens intervals without changing a registered decision on H1 or H2, and was also applied to the tag results and to the odds ratio of retention after tool reverts (Tables S6 and S10); H4 and the direct contrast between manual and tool reverts were not recomputed in this way, and clustering in pages is not modeled. The registration cannot demonstrate that the held-out outputs were unseen, and the most informative analyses are exploratory and should be replicated on other editions and later dumps. The survey of reporting practice was read by one person with the assistance of language models, without a second human coder, and describes what articles report, not what their code does.

### Conclusion

A revert is evidence of information quality work, and like other evidence it depends on who produced it and by what procedure it was recorded. A newcomer revert rate is a mixture of acts by bots, tool users, other editors and the newcomers themselves, in edition-specific proportions; where edits are patrolled, whether the platform's revert tag captures the revert of a newcomer edit varies with the standing of the person who reverted, and replacing a hash-based rule by the tag changes a difference between editions; and what a longer window shows depends on the attribution rule. Stating the construct, the reverter population and the rule costs a sentence each.

## Data availability statement

The data that support the findings are openly available from the Wikimedia Foundation at https://dumps.wikimedia.org/other/mediawiki_history/ (version 2026-09 was used; only recent versions remain hosted). Code, aggregates, the coding table, figure data, logs and the registration (https://doi.org/10.5281/zenodo.23720117; the registered text is also in the repository) are available at https://github.com/beatsbywoni/wiki-revert-audit and archived at Zenodo (https://doi.org/10.5281/zenodo.24054641). Editor-level derived data are not released because they could be re-identified from public edit histories; the code regenerates them from the dumps.

## Endnotes

1. Patrolling configuration was read from the Wikimedia configuration repository operations/mediawiki-config on 28 October and 12 November 2026: `wgUseRCPatrol` is enabled for French and Italian (and for Hebrew); FlaggedRevs is installed on German, Polish and English (on English for a small set of protected pages; the edition is grouped with those without patrolling); Japanese and Korean have neither; French promotes accounts to autopatrolled implicitly at 500 edits and 90 days; the `editor` group of German and Polish carries the rollback right, and the Japanese rollbacker group cites Phabricator task T258339. The `mw-reverted` tag was enabled on all Wikimedia wikis on 15 September 2020 (Phabricator task T164307). Its conditions are in the MediaWiki manual: approval of the reverting edit through autopatrol or patrol, or under FlaggedRevs through a page not under review, the autoreview right, a self-revert or later review; no tagging if the reverting edit has itself been reverted or deleted by the time it is approved; and, since MediaWiki 1.36, no undo mark on an undo modified before saving. The core source, read on 12 November 2026, shows that an undo counts as a revert without an exact match of content (`EditResultBuilder.php`, `RevertedTagUpdate.php`), that the edit result needed for later approval is cached only where `$wgUseRCPatrol` is enabled and no longer than `$wgRCMaxAge` (`DerivedPageDataUpdater.php`, `EditResultCache.php`; when this came into force was not established), and that the depth of tagging (`$wgRevertedTagMaxDepth`) and the search radius for manual reverts (`$wgManualRevertSearchRadius`) are separate settings, both 15 by default. I found no published measurement of tag coverage by reverter or edition.
2. Column order and the identity-revert rule were read from the Wikimedia Analytics Refinery source (`MediawikiEvent.scala`; `DenormalizedRevisionsBuilder.scala`), master branch on 26 October 2026. A revision whose parent is the previous revision with the same hash is not counted as a revert, a filter added in commits of 28 May and 3 June 2026 (the source cites Phabricator task T266374); earlier dump versions may count such revisions.

## References

Arazy, O., Lifshitz-Assaf, H., & Balila, A. (2019). Neither a bazaar nor a cathedral: The interplay between structure and agency in Wikipedia's role system. Journal of the Association for Information Science and Technology, 70(1), 3–15. https://doi.org/10.1002/asi.24076

Ariel, Y. (2026). Crisis documentation on Hebrew Wikipedia: Revision dynamics and epistemic stabilization in wartime articles. Journal of Documentation. Advance online publication. https://doi.org/10.1108/JD-04-2026-0232

Buckland, M. K. (1997). What is a "document"? Journal of the American Society for Information Science, 48(9), 804–809. https://doi.org/10.1002/(SICI)1097-4571(199709)48:9<804::AID-ASI5>3.0.CO;2-V

Choi, B., Alexander, K., Kraut, R. E., & Levine, J. M. (2010). Socialization tactics in Wikipedia and their effects. In Proceedings of the 2010 ACM Conference on Computer Supported Cooperative Work (pp. 107–116). ACM. https://doi.org/10.1145/1718918.1718940

de Laat, P. B. (2015). The use of software tools and autonomous bots against vandalism: Eroding Wikipedia's moral order? Ethics and Information Technology, 17(3), 175–188. https://doi.org/10.1007/s10676-015-9366-9

Ekstrand, M. D., & Riedl, J. T. (2009). rv you're dumb: Identifying discarded work in wiki article history. In Proceedings of the 5th International Symposium on Wikis and Open Collaboration (pp. 1–10). ACM. https://doi.org/10.1145/1641309.1641317

Flöck, F., Vrandečić, D., & Simperl, E. (2012). Revisiting reverts: Accurate revert detection in Wikipedia. In Proceedings of the 23rd ACM Conference on Hypertext and Social Media (pp. 3–12). ACM. https://doi.org/10.1145/2309996.2310000

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé, H., III, & Crawford, K. (2021). Datasheets for datasets. Communications of the ACM, 64(12), 86–92. https://doi.org/10.1145/3458723

Geiger, R. S., & Halfaker, A. (2013). When the levee breaks: Without bots, what happens to Wikipedia's quality control processes? In Proceedings of the 9th International Symposium on Open Collaboration (pp. 1–6). ACM. https://doi.org/10.1145/2491055.2491061

Geiger, R. S., & Halfaker, A. (2017). Operationalizing conflict and cooperation between automated software agents in Wikipedia: A replication and expansion of "Even good bots fight". Proceedings of the ACM on Human-Computer Interaction, 1(CSCW), 1–33. https://doi.org/10.1145/3134684

Geiger, R. S., & Ribes, D. (2010). The work of sustaining order in Wikipedia: The banning of a vandal. In Proceedings of the 2010 ACM Conference on Computer Supported Cooperative Work (pp. 117–126). ACM. https://doi.org/10.1145/1718918.1718941

Geiger, R. S., & Ribes, D. (2011). Trace ethnography: Following coordination through documentary practices. In Proceedings of the 44th Hawaii International Conference on System Sciences (pp. 1–10). IEEE. https://doi.org/10.1109/HICSS.2011.455

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

Star, S. L., & Strauss, A. (1999). Layers of silence, arenas of voice: The ecology of visible and invisible work. Computer Supported Cooperative Work, 8(1–2), 9–30. https://doi.org/10.1023/A:1008651105359

Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W. (2016). Increasing transparency through a multiverse analysis. Perspectives on Psychological Science, 11(5), 702–712. https://doi.org/10.1177/1745691616658637

Suchman, L. (1995). Making work visible. Communications of the ACM, 38(9), 56–64. https://doi.org/10.1145/223248.223263

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

