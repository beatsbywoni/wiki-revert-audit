# Review of practice: how studies operationalise "reverted" (2005 to 2026), consolidated and re-verified

Compiled 2026-11-10 from practice_review_A (2005 to 2018) and practice_review_B (2019 to 2026). Machine-readable version: practice_review_final.csv (same folder).

## 1. Read this first (caveats)

- **All text was read through a fetch tool that summarises pages.** Direct download is blocked in this environment. The tool caps quotes at about 125 characters, so long sentences were requested as consecutive fragments and rejoined here. Quotes are "as returned by the tool", not checked against a PDF by eye. Check each one against the PDF before printing it verbatim.
- **Evidence levels.** A = the sentence(s) establishing the bot / tool / self-revert / window coding (or their absence, for all-not-stated rows) were re-fetched in this pass and match. B = earlier coder's extract only. C = metadata or abstract only. A does NOT mean every field was re-read: the `sensitivity` column and the "partial" judgements come mostly from the earlier coders.
- **"not stated" is an absence claim from a targeted extraction**, weaker than a manual full read. Supplements were not read (TeBlunthuis 2021, Champion & Hill 2023, Ruprechter 2021).
- **Versions read other than the version of record:** arXiv or author preprints for P10, P11, P13, P15 to P18, P20, P22, P23, P25, P26, P28, P30 to P33; technical report for P06; dissertation chapter for P12; Wayback snapshot for P27; NSF PAR copy for P29.
- **Coding conventions applied uniformly in this pass** (they change a few of the earlier codes):
  1. `bot_reverts` is about reverts PERFORMED by bots. Dropping bot-authored edits from the sample is recorded only in `bot_edits_excluded_from_sample`.
  2. `self_reverts` = "excluded" when the text states a rule; "excluded (definitional)" when self-reverts are ruled out only by wording such as "by another editor" or "a second user".
  3. `window` = "unbounded stated" when the outcome is worded as "eventually reverted"; "not stated" otherwise.
  4. `detection` = "identity hash" only when a checksum, hash, text-identity comparison or mwreverts is named. An identity-style verbal definition without a method is "not stated".
  5. A window that applies only to a sub-analysis (3RR in P22, BRD in P13) is not coded as the study's window. P16's 24 hours bounds the interaction analysis, not detection.
- Rows C01 and C02 meet the inclusion rule but could not be read; they are listed, not coded, and not in the tallies.

## 2. Inclusion set

n = 34 coded studies (20 published 2005 to 2018, 14 published 2019 to 2026): 33 peer-reviewed, 1 official Wikimedia report, 0 preprints. Two further eligible items are uncoded (C01 peer-reviewed, C02 non-peer-reviewed Zenodo report).

### Excluded

| Earlier id | Item | Reason |
|---|---|---|
| A-S20 | Narayan et al. (2017), The Wikipedia Adventure | Peripheral: reverts enter only as a decision to keep reverted edits in edit counts; quality is measured by persistent words. |
| B-S02 | Sarkar et al. (2019), StRE | Peripheral: reverts used only to validate a persistence-based label; no operational definition. |
| B-S07 | Asthana et al. (2021) | Data cleaning only, confirmed on re-read: "We used the mwreverts library to label edits that were reverted and exclude them from the labeling step." and "We used a revert window of 15 edits and a maximum revert time of 2 days to identify edit diffs that were reverted [12]." No bot or self-revert sentence. Worth citing in prose as the one recent paper that reports both radius and time cut-off, but it is not a revert-measure study. |
| B-S16 | Ruprechter et al. (2025), page protection | Peripheral, confirmed on re-read: identity-revert counts (1 hour, 24 hours, 1 week before the request) are one matching covariate; the outcome is ORES quality. Borderline: reinstate as "conflict indicator" if covariate use is to count. |
| B-S17 | Song et al. (2026), arXiv | Data preparation only ("reverted revisions using MediaWiki's revert tags"); no revert outcome; preprint. |
| B-S18 | Phabricator T363616 (2024) | Internal task ticket, no report. |
| B-S19 | Phabricator T385103 (2025) | Internal task ticket, no report. |
| B-N02 | Gao et al. (2026), JASIST | Abstract mentions no revert measure; full text not readable. |
| A-S22 | Kiesel et al. (2017) | Eligible, unreadable: kept as C01, outside the tallies. |
| B-N03 | Boté-Vericad (2026) | Eligible, unreadable: kept as C02, outside the tallies. |

## 3. Harmonised table

| id | cite | venue | status | editions | role | detection | radius | bot reverts | bot edits excluded | tool reverts | self-reverts | window | window justif. | sensitivity | ev. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P01 | Kittur et al., 2007 | CHI 2007 | peer-reviewed | en only | conflict indicator | identity + summary matching | none stated | not stated | not stated | not stated | excluded | not stated | none | partial | A |
| P02 | Priedhorsky et al., 2007 | GROUP '07 | peer-reviewed | en only | descriptive | identity + summary matching | 15 revisions | counted explicitly | no | counted explicitly | not stated | revision-bounded: 15 revisions | other | partial | B |
| P03 | Halfaker et al., 2009 | WikiSym '09 | peer-reviewed | en only | outcome | identity hash | none stated | not stated | yes | not stated | excluded | unbounded stated | none | yes: vandalism reverts removed | A |
| P04 | Suh et al., 2009 | WikiSym '09 | peer-reviewed | en only | descriptive | summary matching only | none stated | not stated | yes | not stated | not stated | not stated | none | no | A |
| P05 | Ekstrand & Riedl, 2009 | WikiSym '09 | peer-reviewed | en only | descriptive | identity hash | none stated | not stated | not stated | not stated | not stated | not stated | none | no | A |
| P06 | West et al., 2010 | EUROSEC '10 | peer-reviewed | en only | ML label | rollback or undo actions only | none stated | excluded | not stated | counted explicitly | not stated | not stated | none | partial | A |
| P07 | Halfaker et al., 2011a | WikiSym '11 | peer-reviewed | en only | exposure | not stated | none stated | not stated | not stated | not stated | excluded | not stated | none | no | A |
| P08 | Halfaker et al., 2011b | WikiSym '11 | peer-reviewed | en only | exposure | rollback or undo actions only | none stated | not stated | not stated | not stated | not stated | not stated | none | no | A |
| P09 | Lam et al., 2011 | WikiSym '11 | peer-reviewed | en only | outcome | identity + summary matching | none stated | not stated | not stated | not stated | not stated | time-bounded: 7 days | other | no | A |
| P10 | Sumi et al., 2011 | IEEE PASSAT/SocialCom 2011 | peer-reviewed | multilingual | conflict indicator | identity hash | none stated | not stated | not stated | not stated | excluded | not stated | none | partial | A |
| P11 | Yasseri et al., 2012 | PLoS ONE | peer-reviewed | en only | conflict indicator | identity hash | none stated | not stated | not stated | not stated | excluded | not stated | none | no | A |
| P12 | Flöck et al., 2012 | HT '12 | peer-reviewed | en only | descriptive | diff-based | 20 revisions (also 50, 100) | not stated | not stated | not stated | not stated | revision-bounded: 20 revisions | none | yes: scan range 20/50/100; diff vs identity | A |
| P13 | Halfaker et al., 2013 | American Behavioral Scientist | peer-reviewed | en only | exposure | identity hash | none stated | modelled separately or focal | not stated | modelled separately | excluded (definitional) | not stated | none | no | A |
| P14 | Geiger & Halfaker, 2013 | WikiSym '13 | peer-reviewed | en only | outcome | not stated | none stated | modelled separately or focal | not stated | modelled separately | not stated | unbounded stated | none | no | A |
| P15 | Yasseri et al., 2014 | Global Wikipedia (edited book) | peer-reviewed (edited book chapter; review status not verified) | multilingual | conflict indicator | identity hash | none stated | not stated | not stated | not stated | not stated | not stated | none | no | A |
| P16 | Tsvetkova et al., 2016 | Scientific Reports | peer-reviewed | multilingual | conflict indicator | identity hash | none stated | excluded | yes | not stated | excluded | time-bounded: 24 hours | other | yes: window 24-240 h | A |
| P17 | Tsvetkova et al., 2017 | PLoS ONE | peer-reviewed | multilingual | conflict indicator | identity hash | none stated | modelled separately or focal | not stated | not stated | excluded | not stated | none | no | A |
| P18 | Geiger & Halfaker, 2017 | PACM HCI (CSCW) | peer-reviewed | multilingual | conflict indicator | identity hash | mwreverts default (not reported) | modelled separately or focal | not stated | not stated | not stated | not stated | none | partial | A |
| P19 | TeBlunthuis et al., 2018 | CHI 2018 | peer-reviewed | Wikia | exposure | not stated | none stated | modelled separately or focal | not stated | not stated | not stated | not stated | none | no | A |
| P20 | DeDeo, 2013 | PLoS ONE | peer-reviewed | en only | conflict indicator | identity hash | none stated | not stated | not stated | not stated | excluded | not stated | none | partial | A |
| P21 | Zhang et al., 2019 | ICWSM 2019 | peer-reviewed | en only | exposure | not stated | none stated | not stated | yes | not stated | excluded (definitional) | unbounded stated | none | no | A |
| P22 | Tran et al., 2020 | IEEE S&P 2020 | peer-reviewed | en only | outcome | identity hash | mwreverts default (not reported) | not stated | not stated | not stated | excluded | not stated | none | no | A |
| P23 | Hill & Shaw, 2021 | Communication Research | peer-reviewed | Wikia | outcome | identity hash | mwreverts default (not reported) | not stated | not stated | not stated | not stated | not stated | none | no | A |
| P24 | Chhabra et al., 2020 | OpenSym 2020 | peer-reviewed | en only | conflict indicator | identity hash | none stated | not stated | not stated | not stated | counted explicitly | not stated | none | no | A |
| P25 | TeBlunthuis et al., 2021 | PACM HCI (CSCW) | peer-reviewed | multilingual | outcome | identity hash | none stated | not stated | yes | not stated | excluded | time-bounded: 48 hours | cites Geiger & Halfaker 2013 | no | A |
| P26 | Ruprechter et al., 2021 | Scientific Reports | peer-reviewed | multilingual | descriptive | dump precomputed field | none stated | counted explicitly | yes | not stated | not stated | not stated | none | no | A |
| P27 | Wikimedia Foundation, 2021 | Meta-Wiki report | official report | single non-English edition (pt) | outcome | not stated | none stated | not stated | yes | not stated | not stated | time-bounded: 48 hours | none | no | A |
| P28 | Tran et al., 2022 | PACM HCI (CSCW) | peer-reviewed | multilingual | outcome | not stated | none stated | not stated | not stated | not stated | not stated | unbounded stated | none | no | A |
| P29 | Wang & Zhu, 2022 | FAccT '22 | peer-reviewed | multilingual | outcome | not stated | none stated | not stated | yes | not stated | excluded (definitional) | not stated | none | no | A |
| P30 | Champion & Hill, 2023 | PACM HCI (CSCW) | peer-reviewed | en only | outcome | not stated | 10 contributions forward | not stated | yes | not stated | not stated | revision-bounded: 10 contributions | none | no | A |
| P31 | Warncke-Wang et al., 2023 | PACM HCI (CSCW) | peer-reviewed | multilingual | outcome | not stated | none stated | not stated | not stated | not stated | not stated | time-bounded: 48 hours | cites Geiger & Halfaker 2013 | no | A |
| P32 | Trokhymovych et al., 2023 | KDD '23 | peer-reviewed | multilingual | ML label | dump precomputed field | none stated | not stated | yes | not stated | not stated | not stated | none | no | A |
| P33 | Franzmeyer et al., 2024 | Findings of ACL 2024 | peer-reviewed | en only | ML label | not stated | none stated | not stated | not stated | not stated | excluded (definitional) | not stated | none | no | A |
| P34 | Formisano et al., 2026 | Humanities and Social Sciences Communications | peer-reviewed | en only | outcome | dump precomputed field | none stated | not stated | not stated | not stated | not stated | not stated | none | no | A |
| C01 | Kiesel et al., 2017 | ICWSM 2017 | peer-reviewed | multilingual | ML label | not verified | not verified | not verified | not verified | not verified | not verified | not verified | not verified | not verified | C |
| C02 | Boté-Vericad, 2026 | Zenodo report | preprint | multilingual | exposure | not verified | not verified | not verified | not verified | not verified | not verified | not verified | not verified | not verified | C |
### Evidence per row

| id | cite | quote (as returned by the fetch tool) | url | notes |
|---|---|---|---|---|
| P01 | Kittur et al., 2007 | Self-reverts are disregarded. | https://www.gwern.net/doc/wikipedia/2007-kittur.pdf | Partial sensitivity = MD5 vs comment-detected revert counts (earlier coder; not re-read). No bot or tool sentence found on re-read. |
| P02 | Priedhorsky et al., 2007 | Both D-Loose and D-Strict limit the distance between the first damaged revision and the repairing revert to 15 revisions. [earlier coder extract] | https://www.academia.edu/4906724/Creating_destroying_and_restoring_value_in_wikipedia (earlier coder; all re-fetch attempts failed) | NOT re-verified: academia.edu, grouplens, UMN, gwern and Wayback copies all refused. Bots/tools counted via D-Loose criterion (b) "use of revert-helper tools or autonomous anti-vandalism bot activity" (earlier extract). Self-reverts recoded from "retained (Other class)" to not stated: no explicit rule in the extract. Window justification is the authors own assumption ("essentially all damage is repaired within 15 revisions"). Bots dropped only in the separate persistent-word-view analysis. |
| P03 | Halfaker et al., 2009 | A bot's actions are not directly controlled by a user, so we exclude them from our analysis. / Self-reverts, where an editor reverts himself, were not counted as reverts. | https://opensym.cs.fau.de/ws2009/Proceedings/p115-halfaker.pdf | Bot sentence is a footnote to the SAMPLE description ("revisions attributed to registered editors (with bots removed)"), so it is bot-authored edits, not bot reverts. Window: outcome is "whether a revision was eventually reverted". Sensitivity item from earlier coder, not re-read. |
| P04 | Suh et al., 2009 | In the results presented in this paper, vandalism and bot edits are generally excluded in the analyses. | https://opensym.cs.fau.de/ws2009/Proceedings/p108-suh.pdf | Bots defined as "edits made by a user whose user id is registered as a bot": author side. Nothing on reverts performed by bots. |
| P05 | Ekstrand & Riedl, 2009 | we detect reverts by computing the MD5 checksum of the UTF-8 encoding of each revision's text | https://opensym.cs.fau.de/ws2009/Proceedings/p104-ekstrand.pdf | All-not-stated row, re-read: no bot, self-revert or window rule. |
| P06 | West et al., 2010 | We disregard rollbacks initiated by bots, to maintain a human-validated set. / Editing assistants like Huggle/Twinkle leave comments of a varied form, which are also parsed. | https://apps.dtic.mil/sti/tr/pdf/ADA514680.pdf | Read in technical-report version (UPenn MS-CIS-10-05), not the ACM version. Both sentences are in footnote 1. Partial = manual inspection of potential false positives (earlier coder). |
| P07 | Halfaker et al., 2011a | The reverted subsample comprises 200,000 revisions that were reverted by another editor (no self-reverts) | https://opensym.cs.fau.de/ws2011/_media/proceedings%253Ap163-halfaker.pdf | Two targeted re-reads: no detection method stated (no identity/MD5/checksum; only D LOOSE from Priedhorsky for vandalism) and the word bot does not occur in the body. Reverter TYPE is modelled: "Reverted edits are split by whether the reverting editor was registered or anonymous." |
| P08 | Halfaker et al., 2011b | NICE modified the interface that an editor saw when he used Wikipedia's "undo" interface to performed a revert. [sic] | https://opensym.cs.fau.de/ws2011/_media/proceedings%253Ap101-halfaker.pdf | Short paper. Reverts made through undo define the sample; outcomes are the reverted editor's activity and share of later edits reverted, one month before vs after. No revert look-ahead window. |
| P09 | Lam et al., 2011 | To limit the effect of right truncation, we also only considered reverts that occurred within one week of an edit | https://opensym.cs.fau.de/ws2011/_media/proceedings%253Ap1-lam.pdf | Detection by citation: "We used the method described in Priedhorsky et al. in [21] to detect reverts". Window justified by right truncation and own data (over 95% of reverts within a week, paraphrased by the tool). Vandalism-repair reverts excluded. |
| P10 | Sumi et al., 2011 | If the text of revision j coincides with the text of revision i-1, we considered this a revert ... (self-reverts are excluded) | https://arxiv.org/pdf/1107.3689 | Read from arXiv. Text identity, hash not named; comment-detected counts appear only in a comparison table, so recoded from identity + comment to identity. Languages: en, cs, hu, fa, es. |
| P11 | Yasseri et al., 2012 | To detect reverts we calculated the MD5 hash for each revision ... d refers to the reverted editor (self-reverts are excluded). | https://arxiv.org/pdf/1202.3643 | Read from arXiv. Main analysis on the January 2010 English dump; measure "checked" on six languages. |
| P12 | Flöck et al., 2012 | The maximum scan-range i is in our example set to 20 previous revisions (we discuss the size of i in Section 5.1.4). | https://publikationen.bibliothek.kit.edu/1000058165/3879557 (chars 190000-290000) | Read via Section 5.1 of the 2016 KIT dissertation, which adapts the HT 12 paper; the ACM PDF itself was not read. Edition not stated explicitly (en inferred). Method-evaluation study. |
| P13 | Halfaker et al., 2013 | tool reverted: (Boolean) Was the editor reverted by an algorithmic tool in their first session? | https://webcf.waybackmachine.org/web/20161129032037/https://www-users.cs.umn.edu/~halfak/publications/The_Rise_and_Decline/halfaker13rise-preprint.pdf | Author preprint. Detection by citation: "We use the approach described in Halfaker et al. (2009) to identify identity reverts". Bots and semi-automated tools are pooled in ONE covariate; tools identified from edit comments (Geiger et al. 2012); the Methods do not list which tools/bots. Self: "completely removed by another editor". 14 days appears only in the BRD sub-analysis. |
| P14 | Geiger & Halfaker, 2013 | However, the proportion of revisions that were eventually reverted was not significantly different | https://stuartgeiger.com/wikisym13-cluebot.pdf | Two re-reads: no checksum/identity statement; edit-summary traces are used to attribute reverts to agents (bots: ClueBot NG, XLinkBot; assisted: Huggle, STiki; manual incl. rollback/undo/Twinkle). The paper does NOT report a share of reverts within 24 or 48 hours; it reports median time-to-revert 744 s (bot up) vs 1286 s (bot down). |
| P15 | Yasseri et al., 2014 | To detect reverts, we first assign a MD5 hash code (Rivest RL, 1992) to each revision of the article | https://arxiv.org/pdf/1305.5566 | Read from arXiv:1305.5566. All-not-stated row, re-read: no self-revert, bot or window rule in this text. Text gives both 10 and 12 language editions. |
| P16 | Tsvetkova et al., 2016 | The revert networks were then pruned by removing self-reverts and by removing anonymous users, vandals, and bots | https://arxiv.org/pdf/1602.01652 | Read from arXiv. Bots removed as nodes, so both bot reverters and bot-authored reverted edits drop out. 24 h bounds the interaction (reciprocation) analysis, not detection. "We found that a time window on the order of 24-240 hours produces similar results." 13 editions. |
| P17 | Tsvetkova et al., 2017 | The multi-layer network was pruned by removing self-reverts, as well as reverts between a bot and its owner. | https://arxiv.org/pdf/1609.04285 | Read from arXiv. Bot-bot, bot-human, human-human layers; the layer sentence was paraphrased by the tool, the pruning sentence is verbatim. 13 editions. |
| P18 | Geiger & Halfaker, 2017 | we filtered the dataset for reverting and reverted usernames that match [the bot list] / identify identity reverts by SHA1 hashing [fragments] | https://arxiv.org/pdf/1810.07273 | Read from arXiv (both halves). mwreverts v0.1.4 appears in the reference list; no radius, no self-revert sentence. Only bot-bot reverts kept. A 180-day time-to-revert filter exists for candidate bot fights; its direction was returned inconsistently by the tool, so it is not coded. 7 editions. |
| P19 | TeBlunthuis et al., 2018 | These interfaces are either very rare or invisible on Wikia, so our measure of tool reverted only includes rejection by bots. | https://www.gwern.net/doc/wikipedia/2018-teblunthuis.pdf | Follows Halfaker et al. (2013); own detection not stated. Tool reverts are not excluded from "reverted", they simply cannot be identified. 740 Wikia wikis. |
| P20 | DeDeo, 2013 | We do not include self-reverts, or edits that do not alter any aspect of the page | https://arxiv.org/pdf/1212.0018 | Read from arXiv (appendix S3). SHA1 identity. Partial = compares checksum and keyword detection (earlier coder). |
| P21 | Zhang et al., 2019 | we use the fraction of their edits during that week being reverted eventually. / reverts-revisions that undo other editors' contributions | https://cdn.aaai.org/ojs/3253/3253-28-6302-1-10-20190531.pdf | Edition never named (en implied). Footnote "We exclude bots using:" + bot list is attached to the definition of the editor crowd, i.e. bot editors, not bot reverts. Reverts are negative feedback (mediator) on newcomer retention. |
| P22 | Tran et al., 2020 | We used a Python library called mwreverts to detect whether or not a revision was subsequently reverted by someone else | https://arxiv.org/pdf/1904.04324 | Read from arXiv. Self-reverts are out of the main outcome by the wording "by someone else", and explicitly out of the 3RR analysis ("We excluded self-revert actions because reverting one's own edit is allowed."). 24 h / 48 h apply only to the 3RR sub-analysis. Author order in the IEEE record differs from arXiv. |
| P23 | Hill & Shaw, 2021 | We detect reverts using the python-mwreverts software library published by Aaron Halfaker at the Wikimedia Foundation. | https://arxiv.org/pdf/2111.10688 | Read from arXiv preprint. Sentence is footnote 7. 136 Wikia wikis. Published online 2020, issue 2021. |
| P24 | Chhabra et al., 2020 | We collected all the reverts taking place in the articles using MD5 checksum [27, 32] on the revisions' content. | https://opensym.org/wp-content/uploads/2020/08/os20-paper-a8-chhabra.pdf | Edition never named (en implied by footnote URLs). Self-reverts are reported, not removed ("There were 16.56% cases of reverting to their own content"). ClueBot appears as "a user named ClueBot" in an edit war: bot reverts are in the data but no rule is stated. |
| P25 | TeBlunthuis et al., 2021 | We therefore only treat a revision as reverted if it was undone, but not by a self-revert. / We exclude revisions by bots since we care about how algorithmic flagging and social signals are used by human moderators. | https://arxiv.org/pdf/2006.03121 | Read from arXiv. Bot exclusion is of bot-authored revisions; the paper notes "we are aware of bots that automatically revert edits" but states no rule for bot reverts. 48 h: "most damage to Wikipedia will be undone within that amount of time [28]" = Geiger & Halfaker 2013. 23 editions. |
| P26 | Ruprechter et al., 2021 | We calculate the daily revert rate by dividing the number of identity reverts (by humans or bots) by the number of non-bot edits on this given day. | https://arxiv.org/pdf/2102.10090v2 | Read from arXiv v2. MediaWiki history dumps with "precomputed standard metrics, such as revert information". Authors call it "a cursory analysis of the revert rate". 12 editions. |
| P27 | Wikimedia Foundation, 2021 | Number of reverts is defined as the number of reverted edits within 48 hours of editing. | https://webcf.waybackmachine.org/web/20210924071129/https://meta.wikimedia.org/wiki/IP_Editing:_Privacy_Enhancement_and_Abuse_Mitigation/Impact_report_for_Login_Required_Experiment_on_Portuguese_Wikipedia | Wayback snapshot of 2021-09-24; live page not reachable. Bots removed only from the "net non-reverted edits" metric ("...and not a revert edit, and not an edit by bots"). No publication date on the page. |
| P28 | Tran et al., 2022 | Following previous research [73, 74], revert rate is measured as the proportion of contributions that are eventually reverted. | https://arxiv.org/pdf/2202.05548 | Read from arXiv. Identity-type definition only ("any contribution that returns a page to a previous state"); computed with "custom software scripts" from stub-meta-history dumps; no bot sentence. 17 editions. |
| P29 | Wang & Zhu, 2022 | A revision is considered as being reverted if and only if a second user's revision restores the page to its state before the first revision. | https://par.nsf.gov/servlets/purl/10374248 | NSF PAR copy. Identity-type definition, detection tool not named. "we remove revisions by robots from our dataset" = bot-authored revisions. 17 of 23 editions analysed. |
| P30 | Champion & Hill, 2023 | We looked 10 contributions forward to see if a contribution was reverted. / Given that our interest is in human behavior, we attempt to omit revisions made by bots. | https://arxiv.org/pdf/2308.06403 | Read from arXiv; supplement not read. Identity-type definition ("someone restored an article to its state before the contribution in question"); tool not named. |
| P31 | Warncke-Wang et al., 2023 | This 48-hour window is chosen based on Geiger and Halfaker's 2013 paper [23] [fragment] / reverted, meaning they were undone, within 48 hours of the edit being made | https://arxiv.org/pdf/2308.09642 | Read from arXiv. Authors are Wikimedia Foundation staff; peer-reviewed venue. Detection and data source not stated. 27 wikis. |
| P32 | Trokhymovych et al., 2023 | We are removing bots edits from our dataset because we are interested in human-made changes. | https://arxiv.org/pdf/2306.01650 | Read from arXiv. Label source is the mediawiki history dataset; the field revision_is_identity_reverted is visible only in a data sample figure, never named in the text. Extra filter: "remove all reverting revisions that are further reverted by the next revision." 47 languages. |
| P33 | Franzmeyer et al., 2024 | We retrieve the previous month's edits to all articles from the Wikipedia API, as well as whether an edit was later reverted by another user. | https://arxiv.org/pdf/2406.03428 | Read from arXiv. API endpoint or tag not named. Edition never named (en implied by footnote URLs). Rejected = reverted AND paragraph unchanged after the reversion. |
| P34 | Formisano et al., 2026 | Specifically, we used the 'revision_is_identity_reverted' flag available in the Wikipedia history dump files | https://www.nature.com/articles/s41599-026-06810-2 | Publisher HTML read in two passes (note 13 gives the flag). "edits are only marked as reverted in these files if the two edits share the same content-hash". Edition not named explicitly (US politicians; en implied). Observed reversion is measured for 18 manually coded misinformation edits (9 reverted, under 3 minutes to over 3 years); the bulk of the paper uses the predicted revert-risk score. Bots mentioned only as background. |
| C01 | Kiesel et al., 2017 | identify vandalism and damaging edits via ex post facto evidence by mining Wikipedia's revert graph [abstract fragment] | https://aitopics.org/doc/conferences:D758B70C | Eligible, but full text unreadable (AAAI OJS blocked, no author copy found). Abstract only. Not in tallies. |
| C02 | Boté-Vericad, 2026 | Contributions to pages that were later deleted move to archive [record description fragment] | https://zenodo.org/records/23435553 | Eligible (reverted first edit as exposure for one-edit abandonment; pl, cs, hu, da), but the only file (Constructing newcomer cohorts from Wikimedia logs_version2.pdf, 407.8 kB) came back as binary. Record metadata only. Not in tallies. |
## 4. Tallies (n = 34 coded studies; C01, C02 excluded)

Headline numbers:

- Reverts performed by bots are addressed in 9 of 34 (26%): excluded 2 (P06, P16), counted explicitly 2 (P02, P26), modelled separately or focal 5 (P13, P14, P17, P18, P19). Pre-2019: 8 of 20. 2019+: 1 of 14.
- Tool-assisted reverts are addressed in 4 of 34, all pre-2019 (P02, P06 counted; P13, P14 modelled). 2019+: 0 of 14.
- Self-reverts: excluded by an explicit rule in 10, excluded only by wording in 4, reported but kept in 1, not stated in 19.
- 8 studies drop bot-authored edits from the sample and say nothing about reverts performed by bots (P03, P04, P21, P25, P27, P29, P30, P32); 6 of these are 2019+.
- Observation window: time-bounded 5 (7 days P09; 24 hours P16; 48 hours P25, P27, P31), revision-bounded 3 (P02, P12, P30), "eventually" 4, not stated 22.
- The two studies that justify 48 hours by citation both cite Geiger & Halfaker (2013). On re-read that paper reports median time-to-revert (744 s with ClueBot NG up, 1286 s down) and states no share of reverts within 24 or 48 hours.
- Detection method not stated in 10 of 34 (3 of 20 pre-2019; 7 of 14 2019+). A revision radius or look-ahead count is given in 3; three more name mwreverts without reporting the radius.
- Exactly 1 study reports all four of detection rule, bot reverts, self-reverts and window (P16, Tsvetkova et al. 2016). 13 report none of bot, tool or self-revert handling.
- No study re-runs its result with bot or tool reverts in versus out. Five model reverter type as a variable or stratum (P07 registered vs anonymous reverter; P13, P14, P19 tool/bot covariate or class; P17 bot and human layers).
- Sensitivity over any revert choice: yes 3 (P03 vandalism reverts removed; P12 scan range and method; P16 window 24 to 240 h), partial 6, no 25. All "yes" and "partial" are pre-2019.

## 5. Full tallies by column

n = 34 (pre-2019: 20; 2019+: 14)


**peer_review_status**

| category | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| peer-reviewed | 33 | 20 | 13 | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P28, P29, P30, P31, P32, P33, P34 |
| official report | 1 | 0 | 1 | P27 |

**editions**

| category | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| en only | 20 | 14 | 6 | P01, P02, P03, P04, P05, P06, P07, P08, P09, P11, P12, P13, P14, P20, P21, P22, P24, P30, P33, P34 |
| multilingual | 11 | 5 | 6 | P10, P15, P16, P17, P18, P25, P26, P28, P29, P31, P32 |
| Wikia | 2 | 1 | 1 | P19, P23 |
| single non-English edition | 1 | 0 | 1 | P27 |

**role**

| category | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| outcome | 12 | 3 | 9 | P03, P09, P14, P22, P23, P25, P27, P28, P29, P30, P31, P34 |
| conflict indicator | 9 | 8 | 1 | P01, P10, P11, P15, P16, P17, P18, P20, P24 |
| descriptive | 5 | 4 | 1 | P02, P04, P05, P12, P26 |
| exposure | 5 | 4 | 1 | P07, P08, P13, P19, P21 |
| ML label | 3 | 1 | 2 | P06, P32, P33 |

**detection**

| category | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| identity hash | 14 | 10 | 4 | P03, P05, P10, P11, P13, P15, P16, P17, P18, P20, P22, P23, P24, P25 |
| not stated | 10 | 3 | 7 | P07, P14, P19, P21, P27, P28, P29, P30, P31, P33 |
| identity + summary matching | 3 | 3 | 0 | P01, P02, P09 |
| dump precomputed field | 3 | 0 | 3 | P26, P32, P34 |
| rollback or undo actions only | 2 | 2 | 0 | P06, P08 |
| summary matching only | 1 | 1 | 0 | P04 |
| diff-based | 1 | 1 | 0 | P12 |

**radius_or_rule**

| category | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| none stated | 28 | 17 | 11 | P01, P03, P04, P05, P06, P07, P08, P09, P10, P11, P13, P14, P15, P16, P17, P19, P20, P21, P24, P25, P26, P27, P28, P29, P31, P32, P33, P34 |
| explicit value | 3 | 2 | 1 | P02, P12, P30 |
| library default, value not reported | 3 | 1 | 2 | P18, P22, P23 |

**bot_reverts**

| category | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| not stated | 25 | 12 | 13 | P01, P03, P04, P05, P07, P08, P09, P10, P11, P12, P15, P20, P21, P22, P23, P24, P25, P27, P28, P29, P30, P31, P32, P33, P34 |
| modelled separately or focal | 5 | 5 | 0 | P13, P14, P17, P18, P19 |
| counted explicitly | 2 | 1 | 1 | P02, P26 |
| excluded | 2 | 2 | 0 | P06, P16 |

**bot_edits_excluded_from_sample**

| category | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| not stated | 23 | 16 | 7 | P01, P05, P06, P07, P08, P09, P10, P11, P12, P13, P14, P15, P17, P18, P19, P20, P22, P23, P24, P28, P31, P33, P34 |
| yes | 10 | 3 | 7 | P03, P04, P16, P21, P25, P26, P27, P29, P30, P32 |
| no | 1 | 1 | 0 | P02 |

**tool_reverts**

| category | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| not stated | 30 | 16 | 14 | P01, P03, P04, P05, P07, P08, P09, P10, P11, P12, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29, P30, P31, P32, P33, P34 |
| counted explicitly | 2 | 2 | 0 | P02, P06 |
| modelled separately | 2 | 2 | 0 | P13, P14 |

**self_reverts**

| category | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| not stated | 19 | 11 | 8 | P02, P04, P05, P06, P08, P09, P12, P14, P15, P18, P19, P23, P26, P27, P28, P30, P31, P32, P34 |
| excluded | 10 | 8 | 2 | P01, P03, P07, P10, P11, P16, P17, P20, P22, P25 |
| excluded (definitional) | 4 | 1 | 3 | P13, P21, P29, P33 |
| counted explicitly | 1 | 0 | 1 | P24 |

**window**

| category | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| not stated | 22 | 14 | 8 | P01, P04, P05, P06, P07, P08, P10, P11, P13, P15, P17, P18, P19, P20, P22, P23, P24, P26, P29, P32, P33, P34 |
| time-bounded | 5 | 2 | 3 | P09, P16, P25, P27, P31 |
| unbounded stated | 4 | 2 | 2 | P03, P14, P21, P28 |
| revision-bounded | 3 | 2 | 1 | P02, P12, P30 |

**window_justification**

| category | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| none | 29 | 17 | 12 | P01, P03, P04, P05, P06, P07, P08, P10, P11, P12, P13, P14, P15, P17, P18, P19, P20, P21, P22, P23, P24, P26, P27, P28, P29, P30, P32, P33, P34 |
| other | 3 | 3 | 0 | P02, P09, P16 |
| cites Geiger & Halfaker 2013 | 2 | 0 | 2 | P25, P31 |

**sensitivity_over_revert_choices**

| category | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| no | 25 | 11 | 14 | P04, P05, P07, P08, P09, P11, P13, P14, P15, P17, P19, P21, P22, P23, P24, P25, P26, P27, P28, P29, P30, P31, P32, P33, P34 |
| partial | 6 | 6 | 0 | P01, P02, P06, P10, P18, P20 |
| yes | 3 | 3 | 0 | P03, P12, P16 |

**evidence_level**

| category | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| A | 33 | 19 | 14 | P01, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29, P30, P31, P32, P33, P34 |
| B | 1 | 1 | 0 | P02 |

**Composite counts**

| item | all | pre-2019 | 2019+ | ids |
|---|---|---|---|---|
| reports all four: detection rule, bot reverts, self-reverts, window | 1 | 1 | 0 | P16 |
| reports detection, bot reverts and self-reverts (window aside) | 3 | 3 | 0 | P13, P16, P17 |
| reports none of bot reverts / tool reverts / self-reverts | 13 | 6 | 7 | P04, P05, P08, P09, P12, P15, P23, P27, P28, P30, P31, P32, P34 |
| reports none of bot reverts / tool reverts | 25 | 12 | 13 | P01, P03, P04, P05, P07, P08, P09, P10, P11, P12, P15, P20, P21, P22, P23, P24, P25, P27, P28, P29, P30, P31, P32, P33, P34 |
| bot-authored edits dropped from sample while bot reverts not stated | 8 | 2 | 6 | P03, P04, P21, P25, P27, P29, P30, P32 |
| any time-bounded window | 5 | 2 | 3 | P09, P16, P25, P27, P31 |
| 48-hour window | 3 | 0 | 3 | P25, P27, P31 |
| sensitivity analysis over reverter population (bots/tools in vs out) | 0 | 0 | 0 |  |
| reverter type modelled as a separate variable or stratum (not a sensitivity analysis) | 5 | 5 | 0 | P07, P13, P14, P17, P19 |
## 6. Corrections to the earlier coding

1. **Halfaker et al. 2009 (A-S03 → P03).** Was counted under "bot reverts excluded/dropped". The sentence is a footnote to the sample description ("revisions attributed to registered editors (with bots removed)"). Recoded: bot_reverts not stated; bot_edits_excluded_from_sample yes.
2. **Suh et al. 2009 (A-S04 → P04).** Was "bot reverts excluded (bot edits, hence bot reverts, dropped)". Bots are defined as "edits made by a user whose user id is registered as a bot", i.e. the author side. Recoded as in 1.
3. **Halfaker et al. 2009 window.** Was "not stated". The outcome is "whether a revision was eventually reverted". Recoded: unbounded stated.
4. **Geiger & Halfaker 2013 window (A-S14 → P14).** Was "not stated". Recoded: unbounded stated ("eventually reverted"), same convention as Zhang 2019 and Tran 2022.
5. **Halfaker et al. 2013 self-reverts (A-S13 → P13).** Was "not stated". Definition reads "completely removed by another editor". Recoded: excluded (definitional).
6. **Zhang et al. 2019 self-reverts (B-S01 → P21).** Was "not stated". Definition reads "revisions that undo other editors' contributions". Recoded: excluded (definitional). Role recoded from "mediator" to exposure.
7. **Tran et al. 2020 self-reverts (B-S03 → P22).** Was "excluded in the 3RR analysis only". The main measure is "subsequently reverted by someone else", so self-reverts are out of the main outcome too. Recoded: excluded. The 24 h / 48 h values stay out of the window column (3RR only).
8. **Priedhorsky et al. 2007 self-reverts (A-S02 → P02).** Was "retained (Other class)". No explicit rule in the extract and the paper could not be re-read. Recoded: not stated. Row stays at evidence B.
9. **Sumi et al. 2011 detection (A-S10 → P10).** Was grouped with "identity plus comment matching". The measure uses text identity; comments appear only in a comparison table. Recoded: identity hash (text identity).
10. **TeBlunthuis et al. 2018 tool reverts (A-S19 → P19).** Was "not observable". Recoded to the vocabulary: not stated, with the note that tool interfaces are "very rare or invisible on Wikia".
11. **Wang & Zhu 2022 and Franzmeyer et al. 2024 self-reverts.** "Implicitly excluded" mapped to excluded (definitional).
12. **Detection in Tran 2022, Wang & Zhu 2022, Champion & Hill 2023, Zhang 2019.** "Conceptual/identity definition" mapped to not stated (no method named).
13. **Formisano et al. 2026 (B-N01 → P34).** Was unread. Now read from the publisher page: detection is the `revision_is_identity_reverted` flag of the history dumps (note 13). Added as a coded row.
14. **Asthana et al. 2021 and Ruprechter et al. 2025.** Were "core" rows in part B. Both are peripheral on re-read and are excluded (section 2).
15. **Bibliographic fixes.** NICE DOI 10.1145/2038558.2038575 confirmed, pages 101 to 104. DeDeo DOI confirmed. Wang & Zhu pages 824 to 838 confirmed. Tran et al. 2020 author order confirmed as Tran, Champion, Forte, Hill, Greenstadt (differs from arXiv). Franzmeyer pages 12702 to 12716 added. Hill & Shaw: 136 wikis.

Checks that confirmed the earlier coding: West 2010 (bot rollbacks disregarded, Huggle/Twinkle parsed), Tsvetkova 2016 (network pruned of self-reverts, anonymous users, vandals, bots; 24 to 240 h), Tsvetkova 2017, Kittur 2007, Lam 2011 (one week), TeBlunthuis 2018 and 2021, Ruprechter 2021 ("by humans or bots"), Warncke-Wang 2023 (48 h, cites Geiger & Halfaker), Trokhymovych 2023, Champion & Hill 2023, Tran 2022, Flöck 2012, Yasseri 2012, DeDeo 2013, Geiger & Halfaker 2017, WMF 2021 report.

Two expectations that the text does not support:

- **Halfaker et al. 2011, "Don't bite the newbies".** The paper states no revert detection method, and the word "bot" does not occur in the body. It handles self-reverts (excluded) and splits results by registered vs anonymous reverter. It should not be cited for bot handling.
- **Geiger & Halfaker 2013.** No identity or checksum statement, and no "share reverted within 48 hours" figure.

## 7. Not verified

- P02 Priedhorsky et al. 2007: every copy refused the fetch. Coding and quotes are the earlier coder's. End page 268 unverified.
- C01 Kiesel et al. 2017 and C02 Boté-Vericad 2026: full text unreadable.
- PACM HCI article numbers (49, 56, 333, 299, 280), CHI 2018 paper number 355, and WikiSym/OpenSym article numbers: absent from Crossref and OpenAlex; DBLP refused the fetch.
- P15 Yasseri et al. 2014: publisher, pages and peer-review status of the book chapter.
- P27: publication date (year taken from the archive snapshot).
- P18: the direction of the 180-day time-to-revert filter.
- P33: spelling of "evaluations" in the registered title.

## 8. APA 7 references (verification status in brackets; remove brackets before use)

- P01. Kittur, A., Suh, B., Pendleton, B. A., & Chi, E. H. (2007). He says, she says: Conflict and coordination in Wikipedia. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI '07) (pp. 453-462). ACM. https://doi.org/10.1145/1240624.1240698 [Crossref verified]
- P02. Priedhorsky, R., Chen, J., Lam, S. K., Panciera, K., Terveen, L., & Riedl, J. (2007). Creating, destroying, and restoring value in Wikipedia. In Proceedings of the 2007 International ACM Conference on Supporting Group Work (GROUP '07) (pp. 259-268). ACM. https://doi.org/10.1145/1316624.1316663 [Crossref: authors, title, start page 259 verified; END PAGE 268 NOT VERIFIED]
- P03. Halfaker, A., Kittur, A., Kraut, R., & Riedl, J. (2009). A jury of your peers: Quality, experience and ownership in Wikipedia. In Proceedings of the 5th International Symposium on Wikis and Open Collaboration (WikiSym '09) (pp. 1-10). ACM. https://doi.org/10.1145/1641309.1641332 [Crossref verified; article number not in Crossref]
- P04. Suh, B., Convertino, G., Chi, E. H., & Pirolli, P. (2009). The singularity is not near: Slowing growth of Wikipedia. In Proceedings of the 5th International Symposium on Wikis and Open Collaboration (WikiSym '09) (pp. 1-10). ACM. https://doi.org/10.1145/1641309.1641322 [Crossref verified; article number not in Crossref]
- P05. Ekstrand, M. D., & Riedl, J. T. (2009). rv you're dumb: Identifying discarded work in wiki article history. In Proceedings of the 5th International Symposium on Wikis and Open Collaboration (WikiSym '09) (pp. 1-10). ACM. https://doi.org/10.1145/1641309.1641317 [Crossref verified; article number not in Crossref]
- P06. West, A. G., Kannan, S., & Lee, I. (2010). Detecting Wikipedia vandalism via spatio-temporal analysis of revision metadata? In Proceedings of the Third European Workshop on System Security (EUROSEC '10) (pp. 22-28). ACM. https://doi.org/10.1145/1752046.1752050 [Crossref verified]
- P07. Halfaker, A., Kittur, A., & Riedl, J. (2011). Don't bite the newbies: How reverts affect the quantity and quality of Wikipedia work. In Proceedings of the 7th International Symposium on Wikis and Open Collaboration (WikiSym '11) (pp. 163-172). ACM. https://doi.org/10.1145/2038558.2038585 [Crossref verified]
- P08. Halfaker, A., Song, B., Stuart, D. A., Kittur, A., & Riedl, J. (2011). NICE: Social translucence through UI intervention. In Proceedings of the 7th International Symposium on Wikis and Open Collaboration (WikiSym '11) (pp. 101-104). ACM. https://doi.org/10.1145/2038558.2038575 [Crossref verified; DOI now confirmed]
- P09. Lam, S. K., Uduwage, A., Dong, Z., Sen, S., Musicant, D. R., Terveen, L., & Riedl, J. (2011). WP:Clubhouse? An exploration of Wikipedia's gender imbalance. In Proceedings of the 7th International Symposium on Wikis and Open Collaboration (WikiSym '11) (pp. 1-10). ACM. https://doi.org/10.1145/2038558.2038560 [OpenAlex verified: authors, pp. 1-10; SUBTITLE not in metadata]
- P10. Sumi, R., Yasseri, T., Rung, A., Kornai, A., & Kertesz, J. (2011). Edit wars in Wikipedia. In 2011 IEEE Third International Conference on Privacy, Security, Risk and Trust and 2011 IEEE Third International Conference on Social Computing (pp. 724-727). IEEE. https://doi.org/10.1109/PASSAT/SocialCom.2011.47 [OpenAlex verified: authors, pp. 724-727; diacritics: Kertész]
- P11. Yasseri, T., Sumi, R., Rung, A., Kornai, A., & Kertesz, J. (2012). Dynamics of conflicts in Wikipedia. PLoS ONE, 7(6), Article e38869. https://doi.org/10.1371/journal.pone.0038869 [verified in verification_report.md; diacritics: Kertész]
- P12. Flock, F., Vrandecic, D., & Simperl, E. (2012). Revisiting reverts: Accurate revert detection in Wikipedia. In Proceedings of the 23rd ACM Conference on Hypertext and Social Media (HT '12) (pp. 3-12). ACM. https://doi.org/10.1145/2309996.2310000 [verified in verification_report.md; diacritics: Flöck, Vrandečić]
- P13. Halfaker, A., Geiger, R. S., Morgan, J. T., & Riedl, J. (2013). The rise and decline of an open collaboration system: How Wikipedia's reaction to popularity is causing its decline. American Behavioral Scientist, 57(5), 664-688. https://doi.org/10.1177/0002764212469365 [OpenAlex verified; online 2012-12-28]
- P14. Geiger, R. S., & Halfaker, A. (2013). When the levee breaks: Without bots, what happens to Wikipedia's quality control processes? In Proceedings of the 9th International Symposium on Open Collaboration (WikiSym '13) (pp. 1-6). ACM. https://doi.org/10.1145/2491055.2491061 [OpenAlex verified: authors, pp. 1-6; article number NOT VERIFIED]
- P15. Yasseri, T., Spoerri, A., Graham, M., & Kertesz, J. (2014). The most controversial topics in Wikipedia: A multilingual and geographical analysis. In P. Fichman & N. Hara (Eds.), Global Wikipedia: International and cross-cultural issues in online collaboration. Rowman & Littlefield. [NOT VERIFIED: publisher, page range, no DOI found; arXiv:1305.5566]
- P16. Tsvetkova, M., Garcia-Gavilanes, R., & Yasseri, T. (2016). Dynamics of disagreement: Large-scale temporal network analysis reveals negative interactions in online collaboration. Scientific Reports, 6, Article 36333. https://doi.org/10.1038/srep36333 [OpenAlex verified; diacritics: García-Gavilanes]
- P17. Tsvetkova, M., Garcia-Gavilanes, R., Floridi, L., & Yasseri, T. (2017). Even good bots fight: The case of Wikipedia. PLoS ONE, 12(2), Article e0171774. https://doi.org/10.1371/journal.pone.0171774 [OpenAlex verified; diacritics: García-Gavilanes]
- P18. Geiger, R. S., & Halfaker, A. (2017). Operationalizing conflict and cooperation between automated software agents in Wikipedia: A replication and expansion of "Even good bots fight". Proceedings of the ACM on Human-Computer Interaction, 1(CSCW), Article 49, 1-33. https://doi.org/10.1145/3134684 [Crossref verified: volume, issue, pp. 1-33; ARTICLE NUMBER 49 NOT VERIFIED, absent from Crossref]
- P19. TeBlunthuis, N., Shaw, A., & Hill, B. M. (2018). Revisiting "The rise and decline" in a population of peer production projects. In Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems (CHI '18) (Paper 355, pp. 1-7). ACM. https://doi.org/10.1145/3173574.3173929 [OpenAlex verified: authors, pp. 1-7; PAPER NUMBER 355 NOT VERIFIED]
- P20. DeDeo, S. (2013). Collective phenomena and non-finite state computation in a human social system. PLoS ONE, 8(10), Article e75818. https://doi.org/10.1371/journal.pone.0075818 [OpenAlex verified; DOI now confirmed]
- P21. Zhang, A. F., Wang, R., Blohm, E., Budak, C., Robert, L. P., Jr., & Romero, D. M. (2019). Participation of new editors after times of shock on Wikipedia. Proceedings of the International AAAI Conference on Web and Social Media, 13(1), 560-571. https://doi.org/10.1609/icwsm.v13i01.3253 [OpenAlex verified: authors, volume 13, pp. 560-571; issue number from DOI only]
- P22. Tran, C., Champion, K., Forte, A., Hill, B. M., & Greenstadt, R. (2020). Are anonymity-seekers just like everybody else? An analysis of contributions to Wikipedia from Tor. In 2020 IEEE Symposium on Security and Privacy (SP) (pp. 186-202). IEEE. https://doi.org/10.1109/SP40000.2020.00053 [OpenAlex verified: author order, pp. 186-202]
- P23. Hill, B. M., & Shaw, A. (2021). The hidden costs of requiring accounts: Quasi-experimental evidence from peer production. Communication Research, 48(6), 771-795. https://doi.org/10.1177/0093650220910345 [OpenAlex verified; online first 2020-05-26]
- P24. Chhabra, A., Kaur, R., & Iyengar, S. R. S. (2020). Dynamics of edit war sequences in Wikipedia. In Proceedings of the 16th International Symposium on Open Collaboration (OpenSym 2020) (pp. 1-10). ACM. https://doi.org/10.1145/3412569.3412585 [OpenAlex verified: authors, pp. 1-10; article number NOT VERIFIED]
- P25. TeBlunthuis, N., Hill, B. M., & Halfaker, A. (2021). Effects of algorithmic flagging on fairness: Quasi-experimental evidence from Wikipedia. Proceedings of the ACM on Human-Computer Interaction, 5(CSCW1), Article 56, 1-27. https://doi.org/10.1145/3449130 [OpenAlex verified: volume, issue, pp. 1-27; ARTICLE NUMBER 56 NOT VERIFIED]
- P26. Ruprechter, T., Horta Ribeiro, M., Santos, T., Lemmerich, F., Strohmaier, M., West, R., & Helic, D. (2021). Volunteer contributions to Wikipedia increased during COVID-19 mobility restrictions. Scientific Reports, 11, Article 21505. https://doi.org/10.1038/s41598-021-00789-3 [OpenAlex verified]
- P27. Wikimedia Foundation Anti-Harassment Tools Team. (2021). IP editing: Privacy enhancement and abuse mitigation/Impact report for login required experiment on Portuguese Wikipedia. Meta-Wiki. https://meta.wikimedia.org/wiki/IP_Editing:_Privacy_Enhancement_and_Abuse_Mitigation/Impact_report_for_Login_Required_Experiment_on_Portuguese_Wikipedia [YEAR from 2021-09-24 archive snapshot; no publication date on page; group author as stated on page]
- P28. Tran, C., Champion, K., Hill, B. M., & Greenstadt, R. (2022). The risks, benefits, and consequences of prepublication moderation: Evidence from 17 Wikipedia language editions. Proceedings of the ACM on Human-Computer Interaction, 6(CSCW2), Article 333, 1-25. https://doi.org/10.1145/3555225 [OpenAlex verified: volume, issue, pp. 1-25; ARTICLE NUMBER 333 NOT VERIFIED]
- P29. Wang, L., & Zhu, H. (2022). How are ML-based online content moderation systems actually used? Studying community size, local activity, and disparate treatment. In 2022 ACM Conference on Fairness, Accountability, and Transparency (FAccT '22) (pp. 824-838). ACM. https://doi.org/10.1145/3531146.3533147 [OpenAlex verified; page range now confirmed]
- P30. Champion, K., & Hill, B. M. (2023). Taboo and collaborative knowledge production: Evidence from Wikipedia. Proceedings of the ACM on Human-Computer Interaction, 7(CSCW2), Article 299, 1-25. https://doi.org/10.1145/3610090 [OpenAlex verified: volume, issue, pp. 1-25; ARTICLE NUMBER 299 NOT VERIFIED]
- P31. Warncke-Wang, M., Ho, R., Miller, M., & Johnson, I. (2023). Increasing participation in peer production communities with the Newcomer Homepage. Proceedings of the ACM on Human-Computer Interaction, 7(CSCW2), Article 280, 1-26. https://doi.org/10.1145/3610071 [OpenAlex verified: volume, issue, pp. 1-26; ARTICLE NUMBER 280 NOT VERIFIED]
- P32. Trokhymovych, M., Aslam, M., Chou, A.-J., Baeza-Yates, R., & Saez-Trumper, D. (2023). Fair multilingual vandalism detection system for Wikipedia. In Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD '23) (pp. 4981-4990). ACM. https://doi.org/10.1145/3580305.3599823 [verified in verification_report.md; ordinal 29th from memory]
- P33. Franzmeyer, T., Shtedritski, A., Albanie, S., Torr, P., Henriques, J. F., & Foerster, J. N. (2024). HelloFresh: LLM evaluations on streams of real-world human editorial actions across X Community Notes and Wikipedia edits. In Findings of the Association for Computational Linguistics: ACL 2024 (pp. 12702-12716). Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.findings-acl.754 [OpenAlex verified: authors, pp. 12702-12716; OpenAlex spells the title 'Evalutions', check the published spelling]
- P34. Formisano, G., Hine, E., Juneja, P., Laitila, J., Novelli, C., Chiu, E., Dejanikus, E., Levin, M., Schroder, T., West, A., & Floridi, L. (2026). Editorial governance under pressure: Wikipedia's revert dynamics during the 2024 US election. Humanities and Social Sciences Communications, 13, Article 1459. https://doi.org/10.1057/s41599-026-06810-2 [publisher page verified: 11 authors, volume 13, Article 1459, published 2026-05-13]
- C01. Kiesel, J., Potthast, M., Hagen, M., & Stein, B. (2017). Spatio-temporal analysis of reverted Wikipedia edits. Proceedings of the International AAAI Conference on Web and Social Media, 11(1), 122-131. https://doi.org/10.1609/icwsm.v11i1.14900 [verified in verification_report.md]
- C02. Bote-Vericad, J.-J. (2026). Constructing newcomer cohorts from Wikimedia logs: Account creation type, deleted contributions, observation windows, and the behavioural threshold (version 2) [Report]. Zenodo. https://doi.org/10.5281/zenodo.23435553 [Zenodo record verified: author, date 2026-10-17, type Report; diacritics: Boté-Vericad]
