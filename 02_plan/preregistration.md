# Preregistration: Which reverts count? Successor filtering and observation windows in Wikipedia revert-based metrics

Author: Hongwon Jeong (Center for Creative Convergence Education, Hanyang University ERICA). ORCID 0009-0003-7908-7478.
Version: 1.0, registered 2026-10-28. Content commit (this text): 7fcff3d0f2ec27c7d768f80c21f73c5914558f1a. Zenodo DOI: 10.5281/zenodo.23720117 (concept DOI 10.5281/zenodo.23720116; deposited 2026-10-28, metadata public, files restricted during peer review). Confirmatory wikis (jawiki, plwiki, itwiki) were processed by the pipeline before this registration but none of their output files has been opened; they remain untracked and are excluded from the deposited snapshot.

## 1. Study type and registration status

This is a measurement audit of public secondary data (Wikimedia `mediawiki_history` dumps). It asks how much revert-based metrics for newcomer edits move when the set of revisions that count as a revert (the successor filter) and the observation window are varied while the newcomer edits themselves (the anchors) are held fixed. The design transfers the fixed-anchor successor-selection audit of a companion manuscript (Author, under review) to Wikipedia reverts.

Registration status is disclosed in full. Before this document was finalized, the full pipeline was run on four wikis (kowiki, enwiki, frwiki, dewiki), and their results were examined. Those four wikis are therefore exploratory; their results will be reported as such, with all numbers that informed the hypotheses below. Confirmatory tests are run only on wikis whose data had not been downloaded or examined before the registered commit: jawiki, plwiki and itwiki. The confirmatory pipeline runs are launched before registration, but their output files are not opened until the registered commit and the Zenodo deposit exist. Any change after registration is numbered and recorded in `04_logs/DEVIATION_LOG.md`.

## 2. Data

- Source: `mediawiki_history` dumps, version 2026-09 (78 tab-separated columns; column order taken from the refinery source `MediawikiEvent.toTSVLine`). Exploratory: kowiki (yearly files, full history), enwiki (monthly files 2018-01 to 2026-09), frwiki and dewiki (yearly files, full history). Confirmatory: jawiki, plwiki, itwiki (yearly files, full history).
- Period: anchors dated 2019-01-01 to 2026-03-31 (last dump month minus 180 days, so that every anchor has at least 180 days of follow-up). Tag-based definitions (D2) use anchors from 2020-08-01 onward because the `mw-reverted` tag is applied at revert time from 2020-07.
- Unit and anchor: the editor's first edit, when that edit is in the main namespace (namespace 0). Editors whose first edit is in another namespace are excluded and their share reported. Registered accounts only (anonymous IP edits and temporary accounts excluded). Editors flagged as bots by current or historical username pattern or bot group are excluded. The primary cohort is self-created accounts; all registered accounts are a sensitivity analysis.
- Secondary anchors (robustness): the editor's second to fifth main-namespace edits within 91 days of the first edit (K = 5).

## 3. Design grid (fixed anchors, varied successors)

Three successor filters by three observation windows, each in two variants:

- F0: all identity reverts count. F1: reverts by bots do not count. F2: reverts by bots and by semi-automated tools (revisions tagged `mw-rollback`, `huggle`, `twinkle`, whichever tags exist in that wiki) do not count.
- W24h (86,400 s), W7d (604,800 s), W-inf (any time before the dump date).
- Strict variant: if the first revert was by a bot or tool, the anchor counts as not reverted (reproduces the common preprocessing practice). Replace variant: the anchor counts as reverted at the time of the first revert by a non-excluded actor, recomputed from the page's revision history by SHA-1 identity.

Definition axis: D1, the dump's `revision_is_identity_reverted` (verified in the refinery source to have no radius and no time limit: a revision is reverted if any later revision of the same page restores a state that existed before it); D3r15, SHA-1 identity reverts recomputed with the mwreverts convention of a 15-revision radius; D2, the `mw-reverted` tag. Unbounded SHA-1 recomputation (D3) is used only to verify D1 (exploratory mismatch: 94 of 555,712 kowiki anchors, 0 of 59,985 frwiki anchors, 1 of 59,995 dewiki anchors).

Bot identification: `event_user_is_bot_by` (current) or `event_user_is_bot_by_historical` (at event time) non-empty. Sensitivity: historical only; revert latency of 5 s or less as an auxiliary bot indicator. `mw-undo` is not treated as a tool (sensitivity: included).

Outcome measures: (1) cohort revert proportion p(F, W, D) with Wilson 95% intervals; (2) editor success rate, 1 minus the reverted share of the editor's first-90-day edits, for editors with at least 10 such edits; (3) the odds ratio of retention (at least one edit between day 2 and day 60 after the anchor) given a reverted anchor.

Paired differences Δ(W) = p(F0, W) − p(F, W) are computed on the same anchor set; confidence intervals use 2,000 editor-cluster bootstrap resamples (one anchor per editor). Replace-variant quantities are computed on a year-stratified random sample of 60,000 first-edit anchors per wiki (all anchors when fewer), seed 20261026.

## 4. Confirmatory hypotheses (tested separately in each confirmatory wiki, Holm-adjusted across H1 to H4 within wiki)

- H1 (window). In the replace variant, the filter effect is larger in the short window than in the unbounded window: Δ(W24h) − Δ(W-inf) > 0 for F2r, one-sided 95% bootstrap lower bound above 0. The effect size R = Δ(W-inf) / Δ(W24h) is reported with its 95% interval; R of 0.75 or more is interpreted as "most of the filter effect survives the unbounded window" (exploratory R: kowiki 0.78, enwiki 0.92, frwiki 0.86, dewiki 0.92).
- H2 (substitution). In the strict variant, Δ equals the revert proportion times the bot-and-tool share of first reverts by construction, so dose-response with that share is reported descriptively, not tested. The registered test concerns the substitution rate S = 1 − Δ(F2r, W24h) / Δ(F2 strict, W24h), the share of anchors first reverted by a bot or tool that a non-excluded actor also reverted within 24 hours. Hypothesis: S < 0.25 in each confirmatory wiki, one-sided 95% bootstrap upper bound below 0.25 (exploratory S: 0.12, 0.11, 0.12, 0.09).
- H3 (definitions). Agreement between D2 (tag) and D3r15 (15-revision radius) on reverted status at W-inf is at least 0.95, and among anchors that D1 marks reverted but D2 does not, more than half are reverted beyond the 15-revision radius (anchors from 2020-08-01; exploratory kowiki: agreement 0.988, 76% beyond radius).
- H4 (downstream estimate). The retention odds ratio varies across the nine strict cells by a factor of at least 1.5: OR_max / OR_min ≥ 1.5 with a 95% bootstrap lower bound above 1.0 (exploratory ratios: 3.0, 1.8, 1.5, 1.6).
- Negative control (bot axis). In wiki-by-year cells where bots account for less than 1% of first reverts, the bot-only filter must not move the metric: the 95% interval of Δ(F0 − F1r, W24h) lies within ±0.5 percentage points. Cells from years before tool tags existed are not used as negative controls, because the absence of a tag is not the absence of a tool.

Sample sizes are fixed by the data (exploratory first-edit anchors: kowiki 47,633; enwiki 2,189,284; frwiki 346,938; dewiki 236,903). No optional stopping.

## 5. Pre-specified analyses and robustness

- Window boundaries: 86,400 / 604,800 / unbounded; robustness 43,200 / 172,800 / 2,592,000 s.
- Mixed model (exploratory, descriptive): reverted ~ filter × window + (1 | wiki/year) + (1 | editor).
- Robustness: K = 5 anchors; all registered accounts; historical-only bot flag; `mw-undo` as a tool; 5-second latency as a bot indicator; leave-one-wiki-out; by year; for kowiki, the former anchor definition (first main-namespace edit) against the registered one.
- Independent recomputation: D3 against D1 on each confirmatory wiki's 60,000-anchor sample; mismatch rates reported.
- Simulation: a parameter grid over bot speed, bot-and-tool share, human revert delay and baseline revert probability, used to locate the observed grids.
- Reporting threshold: cell-level aggregates are released only for cells with at least 50 anchors.

## 6. Stopping and branching rules

- If a confirmatory wiki has no tool tags in the period (checked from tag first-appearance months before opening any result), F2 reduces to F1 for that wiki and this is reported; H1, H2 and H4 are then evaluated with F1r in place of F2r.
- If the D3 sample in a confirmatory wiki yields fewer than 5,000 anchors with the previous revision inside the downloaded range, the replace variant for that wiki is reported as descriptive only.

## 7. Transparency and availability

Code, cell-level aggregates, simulation outputs and the deviation log are released in the GitHub repository and archived on Zenodo. Editor-level derived data are released with random identifiers only; usernames of reverting accounts are never released. The study uses public edit histories and was not submitted for ethics review. Generative AI (Claude, Anthropic) was used for code drafting, analysis scripts, document drafting and language editing; every claim derived with its help was checked against the primary sources (dump documentation, refinery source code, the data themselves), and the assistance log is part of the repository.
