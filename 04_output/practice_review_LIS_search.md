# Practice review extension: library and information science and neighbouring venues

Search and coding date: 2026-11-10. Companion file: `practice_review_LIS.csv` (same columns and vocabularies as `practice_review.csv`; ids L01 to L08).

**How to read this.** Every quote below is the sentence as returned by the fetch tool, which passes each page through a small summarising model. Quotes were not checked against the PDFs by eye, and the tool sometimes shortens sentences. Treat each quote as a pointer to verify before it is cited in the manuscript.

## 1. Search log

**Tool and endpoint.** OpenAlex works API, called through WebFetch (direct HTTP from the shell was blocked by the session proxy). URL template for the six protocol queries:

`https://api.openalex.org/works?search=<QUERY>&filter=primary_location.source.id:<ID>%7C<ID>%7C<ID>%7C<ID>&select=doi,title,publication_year&per-page=50` (per-page=100 and `&page=2` where hits exceeded one page).

**Deviations from the suggested protocol, and why.**

- Journals were queried in seven groups of two to four source ids, not one journal per call. The fetch proxy silently dropped the whole `filter` when the URL exceeded roughly 210 characters (the call then returned about 8,300 unfiltered hits), so short URLs were needed; every logged call returned a plausible filtered count.
- No date filter was put in the URL for the same length reason. All listed hits had publication years 2005 to 2026 except one 2003 First Monday item in the title sweep, which was screened out.
- Per-journal counts were derived from DOI prefixes for queries 1 to 4. For queries 5 and 6 (and group G of query 3) the listing was title-filtered at fetch time to save space, so only group totals are recorded.
- OpenAlex `search=` matched title, abstract and, for some records, indexed full text. It stems terms, so "wikipedia reverted" returned the same DOI set as "wikipedia revert" in all seven groups.
- Crossref was not used for searching (not needed as a fallback). APA references of included studies were verified in OpenAlex only.
- Supplementary sweep, added because the six queries missed known Wikipedia papers in these journals: `filter=title.search:wikipedia,primary_location.source.id:<group>` with per-page=100.

**Source ids** (from `https://api.openalex.org/sources?search=<name>` and a group-by on Wikipedia articles): see group rows. OpenAlex has no separate source for Aslib Proceedings; its DOIs (10.1108/000125...) appear under the Aslib Journal of Information Management id.

| Group | Journals (OpenAlex source id) |
|---|---|
| A | JASIST (S4210197613), JASIST "American Society" (S80113298), JASIS (S4210220780), Journal of Documentation (S10082577) |
| B | Journal of Information Science (S68913162), Information Processing & Management (S174847851), Online Information Review (S931548824), Aslib Journal of Information Management incl. Aslib Proceedings (S4210189668) |
| C | Library & Information Science Research (S186163925), Information Research (S163673364), Scientometrics (S148561398), Journal of Informetrics (S205292342) |
| D | Quantitative Science Studies (S4210195326), First Monday (S102129144), New Media & Society (S88603889), Information Communication & Society (S70010600) |
| E | Journal of Computer-Mediated Communication (S30594836), Social Science Computer Review (S127118166), Internet Research (S63576417), Telematics and Informatics (S25720340) |
| F | Computers in Human Behavior (S204030396), Royal Society Open Science (S2737558550), EPJ Data Science (S2504380752), Journal of the Royal Society Interface (S129150467) |
| G | PLoS ONE (S202381698), Physical Review E (S35412551) |

**Hits per query and group** (records returned; not deduplicated across queries).

| Query | A | B | C | D | E | F | G | Total |
|---|---|---|---|---|---|---|---|---|
| "wikipedia revert" | 6 | 4 | 2 | 16 | 2 | 6 | 25 | 61 |
| "wikipedia reverted" | 6 | 4 | 2 | 16 | 2 | 6 | 25 | 61 |
| "wikipedia edit war" | 26 | 9 | 5 | 29 | 8 | 17 | 84 | 178 |
| "wikipedia vandalism" | 11 | 3 | 1 | 17 | 1 | 7 | 24 | 64 |
| "wikipedia conflict editors" | 35 | 10 | 21 | 53 | 21 | 19 | 141 | 300 |
| "wikipedia bots" | 24 | 24 | 12 | 43 | 15 | 29 | 100 | 247 |
| Title sweep `title.search:wikipedia` | 48 | 52 | 11 | 77 | 9 | 17 | 44 | 258 |

Total records from the six protocol queries: 911. Title sweep: 258.

**Per-journal breakdown where recorded.**

| Query | Group | Hits | Per journal |
|---|---|---|---|
| "wikipedia revert" | A | 6 | JASIST (Assoc.) 4, JASIST (Am. Soc.) 1, JASIS 0, JDoc 1 |
| "wikipedia revert" | B | 4 | JIS 0, IPM 2, OIR 1, Aslib 1 |
| "wikipedia revert" | C | 2 | LISR 0, InfRes 0, Scientometrics 1, JoI 1 |
| "wikipedia revert" | D | 16 | QSS 2, First Monday 5, NMS 6, ICS 3 |
| "wikipedia revert" | E | 2 | JCMC 0, SSCR 2, IntR 0, T&I 0 |
| "wikipedia revert" | F | 6 | CHB 0, RSOS 0, EPJ DS 6, JRSI 0 |
| "wikipedia revert" | G | 25 | PLoS ONE 24, PRE 1 |
| "wikipedia reverted" | A | 6 | identical DOI set to "wikipedia revert" (OpenAlex stems the term) |
| "wikipedia reverted" | B | 4 | identical DOI set to "wikipedia revert" (OpenAlex stems the term) |
| "wikipedia reverted" | C | 2 | identical DOI set to "wikipedia revert" (OpenAlex stems the term) |
| "wikipedia reverted" | D | 16 | identical DOI set to "wikipedia revert" (OpenAlex stems the term) |
| "wikipedia reverted" | E | 2 | identical DOI set to "wikipedia revert" (OpenAlex stems the term) |
| "wikipedia reverted" | F | 6 | identical DOI set to "wikipedia revert" (OpenAlex stems the term) |
| "wikipedia reverted" | G | 25 | identical DOI set to "wikipedia revert" (OpenAlex stems the term) |
| "wikipedia edit war" | A | 26 | JASIST family 17, JDoc 9 |
| "wikipedia edit war" | B | 9 | JIS 1, IPM 6, OIR 2, Aslib 0 |
| "wikipedia edit war" | C | 5 | LISR 0, InfRes 2, Scientometrics 2, JoI 1 |
| "wikipedia edit war" | D | 29 | QSS 3, First Monday 6, NMS 13, ICS 7 |
| "wikipedia edit war" | E | 8 | JCMC 6, SSCR 2, IntR 0, T&I 0 |
| "wikipedia edit war" | F | 17 | CHB 1, RSOS 6, EPJ DS 8, JRSI 2 |
| "wikipedia edit war" | G | 84 | not split (title-filtered listing) |
| "wikipedia vandalism" | A | 11 | JASIST family 10, JDoc 1 |
| "wikipedia vandalism" | B | 3 | JIS 1, IPM 1, OIR 1, Aslib 0 |
| "wikipedia vandalism" | C | 1 | LISR 0, InfRes 0, Scientometrics 1, JoI 0 |
| "wikipedia vandalism" | D | 17 | QSS 2, First Monday 6, NMS 6, ICS 3 |
| "wikipedia vandalism" | E | 1 | JCMC 0, SSCR 0, IntR 0, T&I 1 |
| "wikipedia vandalism" | F | 7 | CHB 3, RSOS 2, EPJ DS 2, JRSI 0 |
| "wikipedia vandalism" | G | 24 | PLoS ONE 24, PRE 0 |
| "wikipedia conflict editors" | A | 35 | not split (title-filtered listing) |
| "wikipedia conflict editors" | B | 10 | not split (title-filtered listing) |
| "wikipedia conflict editors" | C | 21 | not split (title-filtered listing) |
| "wikipedia conflict editors" | D | 53 | not split (title-filtered listing) |
| "wikipedia conflict editors" | E | 21 | not split (title-filtered listing) |
| "wikipedia conflict editors" | F | 19 | not split (title-filtered listing) |
| "wikipedia conflict editors" | G | 141 | not split (title-filtered listing) |
| "wikipedia bots" | A | 24 | not split (title-filtered listing) |
| "wikipedia bots" | B | 24 | not split (title-filtered listing) |
| "wikipedia bots" | C | 12 | not split (title-filtered listing) |
| "wikipedia bots" | D | 43 | not split (title-filtered listing) |
| "wikipedia bots" | E | 15 | not split (title-filtered listing) |
| "wikipedia bots" | F | 29 | not split (title-filtered listing) |
| "wikipedia bots" | G | 100 | not split (title-filtered listing) |

**Screening per query.** All returned titles were screened. For listings of up to about 30 records I read every title; for the larger listings (queries 5 and 6 in all groups, query 3 in group G, and the title sweep) the fetch model was asked to return only titles about Wikipedia or wiki editing, editors, revisions, conflict, controversy, quality, vandalism, governance or bots, and I screened that subset. That pre-filter is a model judgement and can miss titles. Page 2 was fetched for query 3 group G (34 records), query 5 group D (3 records) and query 5 group G (41 records); query 6 group G returned exactly 100 on one page.

Included studies by retrieving query: L03 (Purdy) by "revert" and "vandalism" in group D; L04 (Iñiguez) by "revert", "edit war", "vandalism" and "conflict editors" in group F; L05 (Rudas) by all six queries in group G; L06 (Lerner & Lomi) by "revert" in group G. L01 (Stvilia 2007, JASIST) was NOT retrieved by any query or by the title sweep (no "Wikipedia" in its title); it came from the named-candidate check. L02, L07 and L08 are outside the journal list and also came from the named-candidate check.

## 2. PRISMA-style counts

- Records identified by the six protocol queries: 911 (61, 61, 178, 64, 300, 247), with heavy duplication across queries.
- Records identified by the supplementary title sweep: 258.
- Named candidates supplied with the task and checked or attempted: listed in sections 4 and 5.
- Titles screened: all 1169 records (see screening note above).
- Distinct works kept after title screening as possibly using a revert measure, plus named candidates assessed: 79.
- Duplicates of the existing 34-study review: 6.
- Full or near-full methods text read, no revert-based measure: 9 (plus 2 borderline removal-outcome studies excluded).
- Abstract read, revert measure not stated, full text not reachable: 14.
- Not assessed beyond the title (paywalled or fetch refused): 40.
- Included and coded: 8 (7 in tallies; L02 kept out of tallies as the same data as L01). By venue type: 1 LIS journal (JASIST), 1 First Monday, 1 EPJ Data Science, 2 PLoS ONE, 3 outside the journal list (ICIQ, Journal of Statistical Physics, WikiSym).
- All other screened records were excluded at title level as not being empirical studies of wiki edit histories (reviews, reader or citation studies, surveys and interviews, Wikipedia as a text corpus, other platforms, unrelated topics).

**Exclusion reasons used:** X2 methods text read, no revert-based measure; X2b borderline, outcome is removal or flagging of a planted claim and is not coded as a revert; X3 only the abstract could be read and it does not state a revert measure; X4 not assessed beyond the title; D already in the 34.

## 3. Coded table

| id | short_cite | venue | editions | role | detection | radius_or_rule | bot_reverts | bot_edits_excluded_from_sample | tool_reverts | self_reverts | window | sensitivity_over_revert_choices | evidence_level | in_tallies |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L01 | Stvilia et al., 2007 | Journal of the American Society for Information Science and Technology | en only | exposure | not stated | none stated | not stated | not stated | not stated | not stated | not stated | no | A | yes |
| L02 | Stvilia et al., 2005 | ICIQ 2005 (International Conference on Information Quality) | en only | exposure | not stated | none stated | not stated | not stated | not stated | not stated | not stated | no | A | no |
| L03 | Purdy, 2020 | First Monday | en only | descriptive | diff-based | none stated | not stated | not stated | not stated | not stated | not stated | no | A | yes |
| L04 | Iñiguez et al., 2014 | EPJ Data Science | multilingual | conflict indicator | identity hash | none stated | not stated | not stated | not stated | not stated | not stated | no | A | yes |
| L05 | Rudas et al., 2017 | PLoS ONE | multilingual | conflict indicator | not stated | none stated | not stated | yes | not stated | not stated | not stated | no | A | yes |
| L06 | Lerner & Lomi, 2018 | PLoS ONE | en only | exposure | not stated | none stated | not stated | not stated | not stated | not stated | not stated | no | A | yes |
| L07 | Yasseri & Kertész, 2013 | Journal of Statistical Physics | multilingual | conflict indicator | identity hash | none stated | excluded | not stated | not stated | not stated | not stated | partial | A | yes |
| L08 | Sepehri Rad & Barbosa, 2012 | WikiSym '12 | not stated | conflict indicator | not stated | none stated | not stated | not stated | not stated | not stated | not stated | no | A | yes |

`window_justification` is "none" for all eight. "not stated" means the fetch tool was asked for that item on the methods text and reported it absent.

## 4. Per-study evidence

### L01 Stvilia et al., 2007 (Journal of the American Society for Information Science and Technology)

- Evidence: Table 5, row 8: "Number of reverts 12 0 8 Authority Edit history" / Table 5, row 10: "Article median revert time (in minutes) 9 0 17 Volatility Edit history" / Table 6, metric 1 (Authority/Reputation): "0.3 * number of reverts" / Table 6, metric 7 (Volatility): "Median revert time 9 0" [as returned by the fetch tool from the author preprint]
- URL read: https://myweb.fsu.edu/bstvilia/papers/stvilia_IQFramework_p.pdf
- Notes: LIS venue. Revert count and median revert time are two inputs of the information-quality metrics (Authority/Reputation; Volatility) used to separate Featured from Random articles; coded exposure (quality-model indicator; the scheme has no closer role). The tool reported that the paper does not say how reverts were identified and contains no sentence on bots; self-reverts, tools and window were not found in the same read. Read from the author preprint, not the Wiley version of record (Wiley refused the fetch). Sample: 236 Featured and 828 Random articles, English Wikipedia 2005 dumps.
- Reference: Stvilia, B., Gasser, L., Twidale, M. B., & Smith, L. C. (2007). A framework for information quality assessment. Journal of the American Society for Information Science and Technology, 58(12), 1720-1733. https://doi.org/10.1002/asi.20652 [OpenAlex verified: authors, title, year, volume, issue, pages]

### L02 Stvilia et al., 2005 (ICIQ 2005 (International Conference on Information Quality))

- Evidence: "7. Volatility = Median Revert Time" / "Authority/Reputation = 0.2 * Num. Unique. Editors + 0.2 * Total Num. Edits + 0.1 * Connectivity + 0.3 * Num. of Reverts" (formula continues) / "the types of the edits, such as reverts (returning the article to an earlier state/version), minor edits, copyediting, etc." [as returned by the fetch tool]
- URL read: http://mitiq.mit.edu/ICIQ/Documents/IQ%20Conference%202005/Papers/AssessingIQofaCommunity-basedEncy.pdf
- Notes: NOT an LIS journal (conference paper by an LIS group); kept out of tallies because it reports the same Wikipedia sample and the same seven metrics as L01. The tool reported: no method for detecting reverts is stated; bots are described ("the community employed around 50 Bots") but not linked to reverts. Sample: 236 Featured articles and 834 Random articles from the 2005/03/09 English dump. The PDF itself shows no venue or year; venue/year taken from the hosting ICIQ 2005 directory.
- Reference: Stvilia, B., Twidale, M. B., Smith, L. C., & Gasser, L. (2005). Assessing information quality of a community-based encyclopedia. In Proceedings of the 2005 International Conference on Information Quality (ICIQ 2005). MIT. [NOT VERIFIED in Crossref/OpenAlex: no DOI; page range not verified; authors and title verified against the PDF]

### L03 Purdy, 2020 (First Monday)

- Evidence: Tool report of the full text: manual coding of every version using the "diff" feature; category "Removing vandalism"; vandalism = "Sabotaging pages (e.g., by including profanity or sexual references)"; 144 reverts of 1,141 changes (12.6%) in 2012-2014; vandalism reverted "often in the next change to the article". Abstract: "vandalizing and reverting vandalism"; "vandalism and its removal were not found" (2002-2004).
- URL read: https://firstmonday.org/ojs/index.php/fm/article/view/10857/9718
- Notes: LIS-neighbouring venue. Hand-coded revision activities in three English Wikipedia articles (archive, design, writing), 2012-2014 vs 2002-2004; "reverting vandalism" is one coded activity and a headline descriptive result. Detection is human reading of diffs, not an algorithm; coded diff-based as the nearest vocabulary term. Tool reported no mention of bots, tools or self-reverts. Counts are the tool paraphrase, not a verbatim table.
- Reference: Purdy, J. P. (2020). A decade of writing on Wikipedia: A comparative study of three articles. First Monday, 25(9). https://doi.org/10.5210/fm.v25i9.10857 [OpenAlex verified: author, title, year, DOI; volume/issue from the journal page]

### L04 Iñiguez et al., 2014 (EPJ Data Science)

- Evidence: "a revert is detected when two versions in the history line are exactly the same." / "13 different languages, from the start of each language WP up to March 2010." [as returned by the fetch tool]
- URL read: https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-014-0007-z
- Notes: Venue on the requested list (physics/data science neighbour). Revert-based controversy measure M (mutual reverts, MD5 hashes) ranks articles and tracks edit wars; used to compare an agent-based model with empirical data. Tool reported bots, self-reverts, window and robustness over the revert definition all absent; only external validation cited.
- Reference: Iñiguez, G., Török, J., Yasseri, T., Kaski, K., & Kertész, J. (2014). Modeling social dynamics in a collaborative environment. EPJ Data Science, 3(1), Article 7. https://doi.org/10.1140/epjds/s13688-014-0007-z [OpenAlex verified: authors, title, year, volume, issue; article number 7 inferred from the DOI, NOT verified]

### L05 Rudas et al., 2017 (PLoS ONE)

- Evidence: "edits that undo a previous edit." / "the ratio of reverts to all the edits in each language editions." / "we explicitly excluded Wikibots" [as returned by the fetch tool from the arXiv version]
- URL read: https://arxiv.org/pdf/1607.08127
- Notes: Venue on the requested list. Share of reverts among all edits per language edition (13 editions) used as a proxy for time to consensus and compared with the talk/edit ratio. No detection algorithm given. The bot sentence does not say whether it removes bot edits, bot reverts or both; coded as bot edits excluded from the sample and bot reverts not stated. Read from arXiv 1607.08127, not the PLoS ONE version of record (PLoS rate-limited the fetch tool).
- Reference: Rudas, C., Surányi, O., Yasseri, T., & Török, J. (2017). Understanding and coping with extremism in an online collaborative environment: A data-driven modeling. PLoS ONE, 12(3), e0173561. https://doi.org/10.1371/journal.pone.0173561 [OpenAlex verified: authors, title, year, volume, issue, e-number]

### L06 Lerner & Lomi, 2018 (PLoS ONE)

- Evidence: "the logarithm of the number of reverts in its edit history." / "the English-language version of Wikipedia from October 20, 2016" [as returned by the fetch tool]
- URL read: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0190674
- Notes: Venue on the requested list. Revert count enters only as a CONTROL covariate in the featured-article models, so this is the weakest inclusion; coded exposure because the scheme has no control role. Tool reported no sentence defining revert detection, bots, tools, self-reverts or window; the only robustness check varies the quality definition.
- Reference: Lerner, J., & Lomi, A. (2018). Knowledge categorization affects popularity and quality of Wikipedia articles. PLoS ONE, 13(1), e0190674. https://doi.org/10.1371/journal.pone.0190674 [OpenAlex verified: authors, title, year, volume, issue, e-number]

### L07 Yasseri & Kertész, 2013 (Journal of Statistical Physics)

- Evidence: "detect when two versions in the history line are exactly the same" / "we first assign a MD5 hash code [93] to each revision of the article" / "we excluded reverter-reverted editor pairs consisting at least of one IP address or bot" / "we also excluded repeated reverts where the reverter-reverted pair was the same" [as returned by the fetch tool from the arXiv version]
- URL read: https://arxiv.org/pdf/1208.5130
- Notes: NOT an LIS venue (from the named-candidate check). Controversy measure M from mutual reverts. Bot and IP reverter-reverted pairs are dropped in the revert-pattern analysis "to avoid the effects of vandalism". A one-day window appears only in the leader-follower definition ("A reverts C and (within one day) B reverts C"), not in revert detection. Partial sensitivity = comparison of M with alternative controversy measures (same basis as P10). Read from arXiv 1208.5130, whose header has no journal reference.
- Reference: Yasseri, T., & Kertész, J. (2013). Value production in a collaborative environment: Sociophysical studies of Wikipedia. Journal of Statistical Physics, 151(3-4), 414-439. https://doi.org/10.1007/s10955-013-0728-6 [OpenAlex verified: authors, year, volume, issue, pages; OpenAlex gives the title without the subtitle, which is taken from the arXiv PDF]

### L08 Sepehri Rad & Barbosa, 2012 (WikiSym '12)

- Evidence: "where two editors have reverted each other's edits at least once." / "reverts are also common in combating vandalism in non-controversial articles" / "to filter out less active editors such as vandals" [as returned by the fetch tool]
- URL read: https://opensym.cs.fau.de/ws2012/p18wikisym2012.pdf
- Notes: NOT an LIS venue (from the named-candidate check). Mutual Reverts is one of five controversy scores compared on 240 controversial and 240 non-controversial articles; reverts also form disagreement edges in the bipolarity method. The paper defines mutual reverts but not how a single revert is detected. Dataset language is not stated explicitly (English Wikipedia is discussed). The comparison is across controversy methods, not across revert definitions, hence sensitivity = no.
- Reference: Sepehri Rad, H., & Barbosa, D. (2012). Identifying controversial articles in Wikipedia: A comparative study. In Proceedings of the Eighth Annual International Symposium on Wikis and Open Collaboration (WikiSym '12) (pp. 1-10). ACM. https://doi.org/10.1145/2462932.2462942 [OpenAlex verified: authors, year, pages 1-10, DOI; OpenAlex title lacks the subtitle, taken from the PDF; article number not verified]

### Candidates assessed and not included

**Duplicate of existing review** (6)

| DOI or locator | Study | Finding |
|---|---|---|
| 10.1371/journal.pone.0038869 | Yasseri et al. 2012, Dynamics of conflicts in Wikipedia (PLoS ONE) | already P11 |
| 10.1371/journal.pone.0171774 | Tsvetkova et al. 2017, Even good bots fight (PLoS ONE) | already P17 |
| 10.1371/journal.pone.0075818 | DeDeo 2013, Collective phenomena and non-finite state computation (PLoS ONE) | already P20 |
| 10.1109/passat/socialcom.2011.47 | Sumi et al. 2011, Edit wars in Wikipedia (named candidate) | already P10 |
| Global Wikipedia chapter | Yasseri et al. 2014 (named candidate) | already P15 |
| Scientific Reports 2021 | Ruprechter et al. 2021 (named candidate) | already P26 |

**Read, no revert measure** (9)

| DOI or locator | Study | Finding |
|---|---|---|
| 10.1002/asi.20813 | Stvilia et al. 2008, Information quality work organization in Wikipedia (JASIST) | author preprint read (first 100,000 of 112,613 characters): reverts are an edit type and a coded action only; no revert counts or revert times reported |
| 10.2753/MIS0742-1222270403 (JMIS 27(4)) | Arazy, Nov, Patterson & Yeo 2011, Information quality in Wikipedia (named candidate) | full text read (core.ac.uk): "Task conflict was measured by an analysis of articles' discussion pages"; three assessors, seven-point scale; reverts never mentioned. DOI not verified |
| 10.5210/fm.v12i4.1763 | Wilkinson & Huberman 2007, Assessing the value of cooperation in Wikipedia (First Monday) | arXiv cs/0702140 read: measures are edit counts and distinct editors; "revert times" appears only as prior work; "Robot edits were identified using the list of registered Wikipedia robots" and removed |
| 10.5210/fm.v16i12.3613 | Kimmons 2011, Understanding collaboration in Wikipedia (First Monday) | full text read: measures are revisions per article and "collaborative rigor"; no revert measure |
| 10.1371/journal.pone.0155305 | Kim et al. 2016, Understanding editing behaviors in multilingual Wikipedia (PLoS ONE) | arXiv 1508.07266 read: no reverts; bot edits discarded |
| 10.1371/journal.pone.0281725 | Anand et al. 2023, A game-theoretic analysis of Wikipedia's peer production (PLoS ONE) | publisher HTML read up to character 100,000 of 160,899 (cut in Section 5): revert only in background on turf wars; no revert variable seen |
| 10.1038/s41562-019-0541-6 | Shi, Teplitskiy, Duede & Evans 2019, The wisdom of polarized crowds (named candidate) | arXiv 1712.06414 read: no revert measure; only "powerful moderators may step in and revert edits, lock pages and execute bans". DOI not verified |
| 10.3390/computers8030060 | Lewoniewski, Węcel & Abramowicz 2019, Multilingual ranking of Wikipedia articles (Computers; named candidate) | publisher HTML read (first 100,000 of 182,114 characters): five quality features (length, references, reference density, images, sections); "revert" does not appear |
| 10.1145/2702123.2702436 | Borra et al. 2015, Societal controversies in Wikipedia articles (CHI; named candidate) | arXiv 1904.08721 read: controversy score counts sentences with substantive edits containing a deletion; reverts used only to filter vandalism ("whether the comment of a revert contains the word 'vandal'", known anti-vandalism bots, IP edit reverted within 60 seconds). Borderline exclusion. DOI not verified |

**Borderline, excluded** (2)

| DOI or locator | Study | Finding |
|---|---|---|
| 10.5210/fm.v13i9.2115 | Magnus 2008, Early response to false claims in Wikipedia (First Monday) | borderline, excluded: outcome is "whether it was removed or flagged as needing citation in the 48 hours after I inserted it" (as quoted in the 2023 follow-up); the word revert is not used and flagging counts as correction. 2008 galley itself returned a server error twice |
| 10.5210/fm.v28i9.12912 | Magnus 2023, Early response to false claims in Wikipedia, 15 years later (First Monday) | full text read; borderline, excluded for the same reason: "corrected within 48 hours", 12/33 corrected; no justification of the 48 hours; no bots or tools mentioned |

**Abstract only, not verifiable** (14)

| DOI or locator | Study | Finding |
|---|---|---|
| 10.1002/asi.22869 | Arazy, Yeo & Nov 2013, Stay on the Wikipedia task (JASIST) | abstract only (RePEc): "including analysis of Wikipedia system logs, manual content analysis of articles' discussion pages"; conflict operationalisation not stated in the abstract; Wiley full text not reachable |
| 10.1002/asi.70123 | Gao, Qiu, Zhang & Zhao 2026, From divergence to convergence (JASIST) | abstract only (OpenAlex): 337,830 edit and talk records from 200 articles; no mention of reverts; Wiley PDF refused |
| 10.1002/asi.23653 | Robert & Romero 2016, The influence of diversity and experience on the effects of crowd size (JASIST) | abstract only: 4,317 WikiProject Film articles; no reverts in abstract (OpenAlex full-text search matched "revert"); Wiley and Deep Blue refused |
| 10.1002/asi.23901 | Jemielniak & Wilamowski 2017, Cultural diversity of quality of information on Wikipedias (JASIST) | abstract only: images, references, links, word/character counts, Good/Featured status; no reverts |
| 10.1002/asi.70014 | Quality teamwork on Wikipedia 2025 (JASIST) | abstract only: communication networks and article quality; no reverts |
| 10.1108/jd-04-2022-0090 | Morris-O'Connor, Strotmann & Zhao 2022/2023, The colonization of Wikipedia (JDoc) | abstract only (Emerald page): "the authors identify edit-warring camps across many conflict zones of the English language WP"; how camps or edit wars are detected is not in the abstract; no open copy found |
| 10.1108/jd-04-2026-0232 | Crisis documentation on Hebrew Wikipedia 2026 (JDoc) | abstract only: structural indicators include "conflict"; "signaling did not predict lower next-day conflict"; operationalisation not stated |
| 10.1016/j.ipm.2017.08.005 | Jang, Foley, Dori-Hacohen & Allan 2017, Computing controversy (IPM) | abstract only; no revert statement. A related preprint by Jang, Dori-Hacohen & Allan (Modeling controversy within populations) uses the Sumi et al. M score as a baseline but is a different paper |
| 10.1108/oir-06-2017-0199 | Luyt 2018, Wikipedia's gaps in coverage: Cambodian Wikiproject (OIR) | abstract only: qualitative content analysis of project and talk pages |
| 10.1177/0894439317703579 | Göbel & Munzert 2017, Political advertising on the Wikipedia marketplace of information (SSCR) | abstract only: edit histories of MP biographies; no revert statement |
| 10.1177/14614448251336418 | Decoding revision mechanisms in Wikipedia 2025 (NMS) | abstract only: 140,593 revisions, survival analysis; "revert" not in abstract |
| 10.1080/1369118x.2021.1994633 | Wikipedia: a self-organizing bureaucracy 2021 (ICS) | abstract only: interviews and archival research |
| 10.1145/1341531.1341556 | Vuong et al. 2008, On ranking controversies in Wikipedia (WSDM; named candidate) | abstract only (SMU repository): "the Basic model only considers the amount of disputes within an article"; dispute definition not in abstract; PDF fetch failed. DOI not verified |
| 10.1145/1985347.1985352 | Liu & Ram 2011, Who does what (ACM TMIS; named candidate) | abstract only: contributor roles from provenance; reverts not mentioned |

**Not assessed beyond title** (40)

| DOI or locator | Study | Finding |
|---|---|---|
| 10.1002/asi.24210 | Assessing the quality of information on Wikipedia: a deep-learning approach 2019 (JASIST) | not assessed beyond title (paywalled) |
| 10.1002/asi.20755 | Improving Wikipedia's accuracy: Is edit age a solution? 2007/2008 (JASIST) | not assessed beyond title |
| 10.1002/asi.24076 | Neither a bazaar nor a cathedral 2018 (JASIST) | not assessed beyond title |
| 10.1002/asi.24393 | Loosen control without losing control 2020 (JASIST) | not assessed beyond title |
| 10.1177/0165551519877646 | Deep learning-based quality assessment model 2019 (JIS) | not assessed beyond title |
| 10.1177/0165551519888607 | Indicator of quality for environmental articles 2019 (JIS) | not assessed beyond title |
| 10.1177/01655515251362587 | Evolution of Wikipedia articles through triggering networks 2025 (JIS) | not assessed beyond title |
| 10.1016/j.ipm.2018.08.003 | Quality flaw prediction in Spanish Wikipedia 2018 (IPM) | not assessed beyond title |
| 10.1016/j.ipm.2020.102225 | How Wikipedia disease information evolve over time 2020 (IPM) | not assessed beyond title |
| 10.1108/oir-02-2023-0084 | Polarization and reliability of news sources in Wikipedia 2024 (OIR) | not assessed beyond title |
| 10.1108/oir-03-2011-0182 | Network analysis of user generated content quality in Wikipedia 2013 (OIR) | not assessed beyond title |
| 10.1108/oir-01-2016-0003 | Improving information quality of Wikipedia articles with cooperative principle 2017 (OIR) | not assessed beyond title |
| 10.1108/oir-10-2023-0515 | Mass collaboration or curatorship? 2025 (OIR) | not assessed beyond title |
| 10.1016/j.lisr.2009.07.005 | Stvilia, Al-Faraj & Yi 2009, Issues of cross-contextual information quality evaluation: Arabic, English, Korean Wikipedias (LISR) | not assessed beyond title; same group as L01, so the L01 revert metrics may recur. Priority for a manual check |
| 10.5210/fm.v27i11.12754 | Editors, sources and the 'go back' button 2022 (First Monday) | not assessed beyond title |
| 10.5210/fm.v13i10.2217 | Collaboration in context: article evolution among subject disciplines 2008 (First Monday) | not assessed beyond title |
| 10.5210/fm.v14i5.2365 | Comparing featured article groups and revision patterns 2009 (First Monday) | not assessed beyond title |
| 10.5210/fm.v24i5.9530 | Breaking news on Wikipedia 2019 (First Monday) | not assessed beyond title |
| 10.5210/fm.v23i12.9184 | WikiScanner scandals and anonymity on the Japanese Wikipedia 2018 (First Monday) | not assessed beyond title |
| 10.1177/1461444810365297 | Niederer & van Dijck 2010, Wisdom of the crowd or technicity of content? (NMS) | not assessed beyond title (matched revert, vandalism and bots queries) |
| 10.1177/14614448251336436 | Templates and sovereignty 2025 (NMS) | not assessed beyond title |
| 10.1177/14614448241248139 | Countering underproduction of peer produced goods 2024 (NMS) | not assessed beyond title |
| 10.1177/14614448251406231 | The block log: 20 years of content moderation on Wikipedia 2025 (NMS) | not assessed beyond title |
| 10.1177/1461444819838227 | Controversies around global warming on Portuguese Wikipedia 2019 (NMS) | not assessed beyond title |
| 10.1080/1369118x.2021.1924224 | Predicting conflict-prone disputes using the structure of turn-taking 2021 (ICS) | not assessed beyond title |
| 10.1080/1369118x.2017.1293709 | A river by any other name: Ganga/Ganges 2017 (ICS) | not assessed beyond title |
| 10.1093/jcmc/zmad002 | Communication networks do not predict success in attempts at peer production 2023 (JCMC) | not assessed beyond title |
| 10.1111/j.1083-6101.2006.00316.x | Cultural differences in collaborative authoring of Wikipedia 2006 (JCMC) | not assessed beyond title |
| 10.1177/0894439315591136 | Models for understanding collective intelligence on Wikipedia 2015 (SSCR) | not assessed beyond title |
| 10.1016/j.chb.2015.03.078 | Interacting with bots online: users' reactions to automated programs in Wikipedia 2015 (CHB) | not assessed beyond title |
| 10.1098/rsos.240514 | Causal evidence for social group sizes from Wikipedia editing data 2024 (RSOS) | not assessed beyond title; publisher refused the fetch |
| 10.1103/physreve.91.012824 | Wikipedia editing dynamics 2015 (PRE) | not assessed beyond title |
| 10.1371/journal.pone.0134454 | Wilson & Likens 2015, Content volatility of scientific topics in Wikipedia (PLoS ONE) | not assessed: PLoS rate-limited six attempts. Matched revert, edit war and vandalism queries. Priority for a manual check |
| 10.1371/journal.pone.0060584 | Neff et al. 2013, Jointly they edit (PLoS ONE) | not assessed beyond title |
| 10.1371/journal.pone.0111958 | Halatchliyski & Cress 2014, How structure shapes dynamics (PLoS ONE) | not assessed beyond title |
| 10.1371/journal.pone.0291097 | Network traits driving knowledge evolution in open collaboration systems 2023 (PLoS ONE) | not assessed beyond title |
| 10.1371/journal.pone.0020902 | Content disputes in Wikipedia reflect geopolitical instability 2011 (PLoS ONE) | not assessed beyond title |
| 10.1371/journal.pone.0030091 | Circadian patterns of Wikipedia editorial activity 2012 (PLoS ONE) | not assessed beyond title |
| 10.1371/journal.pone.0178985 | A productive clash of perspectives? 2017 (PLoS ONE) | not assessed beyond title |
| 10.1145/1641309.1641333 | Wöhner & Peters 2009, Assessing the quality of Wikipedia articles with lifecycle based metrics (WikiSym; named candidate) | PDF fetch failed (guessed URL); not assessed. DOI not verified |

## 5. What could not be verified

- **Paywalled publishers.** Wiley (JASIST), Emerald (JDoc, OIR, Aslib), Sage (JIS, NMS, SSCR), Elsevier (IPM, LISR, CHB, T&I), Taylor & Francis (ICS), Oxford (JCMC) and the Royal Society refused or returned no full text. Every candidate from those journals therefore sits in X3 or X4 unless an author copy was found. This is the main limit on the LIS result: the low LIS count reflects what could be read, not a demonstrated absence.
- **PLoS ONE.** The site rate-limited the fetch tool on most attempts; two articles were read from the publisher (Lerner & Lomi; Anand et al., truncated) and two from arXiv. Wilson & Likens 2015 failed six times.
- **Arazy, Yeo & Nov 2013 (JASIST).** Only the abstract was read. The conflict operationalisation is inferred from the abstract wording and from the companion JMIS 2011 paper by the same team, which was read in full.
- **Gao et al. 2026 (JASIST, 10.1002/asi.70123).** Abstract only; it does not mention reverts. Whether reverts are measured in the full text is unknown. OpenAlex matched this article on the "revert", "vandalism", "edit war", "conflict editors" and "bots" queries, which suggests the indexed full text contains those words.
- **Named candidates not checked at all:** Arazy & Nov 2010 JASIST (Determinants of Wikipedia quality): the DOI I tried (10.1002/asi.21283) resolves to a different article; the paper was not located in the OpenAlex title sweep output; Keegan, Gergle & Contractor (breaking news articles); Ortega, Gonzalez-Barahona & Robles 2008 HICSS; other Ortega et al.; Soto WikiXRay work; Kuznetsov 2006; Thornton & McDonald (tagging/templates); Ren & Yan 2017; Jiang & Vetter; Zhang, Ren et al. on Chinese Wikipedia; Ferschke et al.; Lewoniewski et al. 2017 (the 2019 Computers paper was read; no Lewoniewski paper appeared in the JASIST listing); Kittur/Suh/Halfaker-type studies already in the 34 were not re-read.
- **Quotes.** All quotes are tool-returned and unverified by eye (see the note at the top). Three reads were truncated at 100,000 characters (Stvilia 2008; Anand 2023; Lewoniewski 2019).
- **References.** L02 has no DOI and its page range is unverified. The article number for L04 and the subtitles for L07 and L08 are not in OpenAlex. DOIs marked "not verified" in the tables above were typed from memory and should not be cited without checking.
- **Screening.** The large listings were pre-filtered by the fetch model on titles, and per-journal splits were not recorded for queries 5 and 6. Deduplicated record counts across queries were not computed.
