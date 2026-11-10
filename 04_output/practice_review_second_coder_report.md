# Second-coder report (practice review, revert operationalisation)

Date: 2026-11-10. Coder: independent second coder (LLM agent). Blind to the original codes until second_coder_codes.csv was saved (12:15 UTC); the only file opened before that was the code-stripped study list.

## Part 1. Blind double coding

Sample: numpy default_rng(20261110), 14 of 34 sorted ids without replacement:
P02, P04, P06, P10, P14, P15, P16, P17, P19, P20, P22, P26, P30, P31.

Readable: 13 of 14. P02 (Priedhorsky et al., 2007) could not be read (ACM PDF, GroupLens, author sites, CiteSeerX, Wayback all failed or blocked; OpenAlex and Semantic Scholar list it as closed). It was not coded and not replaced.

Versions read: P06 DTIC technical report; P10, P15, P20, P22, P26, P30, P31 arXiv versions; P19 mirror copy (gwern.net); P14 author PDF; P04 OpenSym proceedings PDF; P16, P17 publisher pages. P20 detection details are in Appendix S3 (read in the arXiv version). P26 Supplementary Information not read.

| field | n | agree | raw agreement | Cohen's kappa |
|---|---|---|---|---|
| detection | 13 | 11 | 0.846 | 0.776 |
| bot_reverts | 13 | 13 | 1.000 | 1.000 |
| tool_reverts | 13 | 13 | 1.000 | 1.000 |
| self_reverts | 13 | 13 | 1.000 | 1.000 |
| window | 13 | 11 | 0.846 | 0.612 |
| sensitivity_over_revert_choices | 13 | 11 | 0.846 | 0.594 |

Pooled: 72 of 78 decisions agree (0.923). No field had a single category, so kappa is defined everywhere. With n = 13 the kappas are imprecise; no interval was computed.

Mapping of original values: "excluded (definitional)" to "excluded"; "time-bounded: ..." to "time-bounded"; "revision-bounded: ..." to "revision-bounded"; "yes: ..." to "yes".

### Disagreements (6) and adjudication

1. P14 detection. Original: not stated. Second: identity + summary matching. Second coder's sentence: time-to-revert runs until "the edit is entirely removed from the encyclopedia in a later edit, taking the article back to a previous state", plus "mining edit summaries for standard traces" to attribute reverts to agents. Original note: no checksum or identity statement; summaries used for attribution. View: original is right under a strict rule (method must be named). My code was an inference from the definition.
2. P30 detection. Original: not stated (note: identity-type definition, tool not named). Second: identity hash. Sentence: "A contribution is said to have been reverted if someone restored an article to its state before the contribution in question." View: same boundary as item 1; original is right under the strict rule. Both disagreements come from one unwritten rule, so the codebook should state it: code a detection method only when the method (hash, library, field) is named, not when only an identity-style definition is given.
3. P14 window. Original: unbounded stated (quote: "the proportion of revisions that were eventually reverted"). Second: not stated (no cutoff found). View: weak either way. "Eventually" implies no bound but is not a statement of the follow-up horizon; I lean to "not stated", or keep "unbounded stated" with an "implied" flag.
4. P16 window. Original: time-bounded: 24 hours. Second: not stated. Sentence: motif responses are "restricted to a time window of 24 hours" (motif analysis). The original's own note says the 24 h bounds the reciprocation analysis, not detection. View: second coder is right; the field asks about the window for an edit to count as reverted.
5. P16 sensitivity. Original: yes (window 24-240 h). Second: no. Sentence: "We found that a time window on the order of 24-240 hours produces similar results", which the fetch tool located in the null-model (shuffling) description. View: second coder is closer; this varies an analysis window, not a revert-definition choice. "partial" is the most I would give, and the location of the sentence should be rechecked in the PDF.
6. P06 sensitivity. Original: partial (manual inspection of potential false positives). Second: no. View: validation of the label is not sensitivity over revert choices, so "no"; but I coded P10 and P20 "partial" for comparing two detection methods without rerunning the analysis, and the original agreed. The codebook needs one rule for "partial" (suggest: an alternative revert definition is compared or reported, analysis not rerun) and under that rule P06 is "no".

Net: 2 of 6 favour the original (both the same detection boundary), 3 favour the second coder (P16 x2, P06), 1 open (P14 window).

Borderlines that happened to agree: P04 bot_reverts (all robot edits dropped from the sample, coded not stated by rule); P19 tool_reverts (paper says tool interfaces are invisible on Wikia; coded not stated); P22 self_reverts (excluded from "reverted by someone else").

## Part 2. Construct coding (all 34, not blind)

Primary construct: Q 10, C 9, R 9, E 3, O 3.

| primary | pre-2019 | 2019+ | all |
|---|---|---|---|
| Q quality | 2 | 8 | 10 |
| R rejection/reception | 7 | 2 | 9 |
| E quality-control work | 1 | 2 | 3 |
| C conflict | 8 | 1 | 9 |
| O other | 2 | 1 | 3 |
| all | 20 | 14 | 34 |

Secondary: none 16, E 8, Q 5, R 3, C 2.

Primary construct by whether the original file states handling (anything other than "not stated"):

| primary | bot_reverts stated | not stated | self_reverts stated | not stated |
|---|---|---|---|---|
| Q | 2 | 8 | 2 | 8 |
| R | 2 | 7 | 5 | 4 |
| E | 1 | 2 | 1 | 2 |
| C | 3 | 6 | 7 | 2 |
| O | 1 | 2 | 0 | 3 |
| all | 9 | 25 | 15 | 19 |

Reading: conflict studies mostly state self-revert handling (7 of 9); quality studies mostly do not (8 of 10 for each of bot and self). Cells are small; descriptive only.

Check against the original "role" column (opened only after Part 1): C = all 9 "conflict indicator"; O = all 3 "descriptive"; E = 3 "outcome"; Q = 3 ML label, 6 outcome, 1 descriptive; R = 5 exposure, 3 outcome, 1 descriptive.

Least certain construct codes: P03 (R vs Q), P18 (C; the paper argues against the conflict reading), P25 (R vs E), P26 (O; construct not named), P29 (E; abstract does not name reverts), P34 (E vs Q), P23 (Q from abstract that does not name reverts).

## Limits

- P02 methods text not read (Part 1); its construct code rests on the abstract only.
- Part 2: 17 of 34 coded from the abstract only (P01, P02, P03, P05, P07, P08, P09, P12, P18, P21, P23, P24, P25, P28, P29, P32, P33), most via OpenAlex abstracts that the fetch tool summarised rather than reproduced.
- All quotes come from a fetch tool that summarises pages with a small model. Sentences are recorded as returned and may be shortened or paraphrased; "nothing found" means the tool reported no such statement, not that I read every line. Several papers were read in preprint or report versions, not the version of record. Supplements were not read (P26; P20 only via the arXiv appendix).
- One coder, one pass, small sample (13). Kappa is sensitive to the heavy "not stated" share.

Files: second_coder_list.csv, second_coder_codes.csv, second_coder_agreement.csv, second_coder_disagreements.csv, second_coder_constructs.csv, sc_codes.py, sc_agree.py, sc_constructs.py (same folder).
