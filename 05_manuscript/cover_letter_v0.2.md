[Date]

Editor-in-Chief
Journal of the Association for Information Science and Technology

Dear Editor,

I am pleased to submit the manuscript "Which reverts count? Successor filtering and observation windows in Wikipedia revert-based metrics" for consideration as a Research Article in JASIST. The manuscript has not been published and is not under consideration elsewhere. I am its sole author.

The paper addresses a question at the core of information science's long-standing concern with the measurement of information quality: how far does an indicator of quality work depend on decisions about what it admits? Whether a Wikipedia edit was reverted is among the most widely used such indicators, in JASIST and beyond, serving as a proxy for quality control work (Stvilia et al., 2008), for conflict (Arazy et al., 2013), for the balance of control and openness in peer production (Rozas & Huckle, 2021) and, most recently, for human-bot collaboration in knowledge communities (Gao et al., 2026). The paper shows that the indicator inherits two decisions that are rarely examined, which later revisions are allowed to count as a revert and how long an edit is observed, and that the first decision moves cohort revert rates by 3 to 21 percentage points, reorders editor quality rankings, and changes downstream retention estimates by a factor of up to 3, in a way that is predictable from the local share of automated reverting. It also documents, from the MediaWiki source code and seven language editions, that the software's own revert tag depends on the reverting editor's patrol status, so that tag-based revert rates confound community differences with configuration differences. The paper closes with a six-item reporting checklist and argues that the same mechanics apply to any content-moderation indicator built from later events on platforms that mix automated and human moderation.

Methodologically, the study holds the measured edits fixed and varies only the successor set, across three filters, three windows and three revert definitions, in seven editions and 56 edition-year cells. This fixed-anchor audit requires a revert definition computed over complete page histories, which the Wikimedia history dumps provide and radius-limited libraries cannot, and the comparison across seven editions has not been reported before. The design, hypotheses, thresholds and analysis code were registered on Zenodo (https://doi.org/10.5281/zenodo.23720117) after four exploratory editions had been analyzed and before three confirmatory editions were opened; the sequence is documented by commit and batch-log timestamps in the public repository, and a deviation log records every change made after registration.

Declaration on generative AI. Generative AI (Claude, Anthropic) was used under my direction to draft analysis code, project documents and prose. All computations were performed by the released deterministic code on the unmodified public dumps; the AI did not analyze or modify data, and every numerical result in the manuscript was transcribed from the code's output files. Every claim about the dump format and the MediaWiki software was verified against the primary sources, which are cited. An assistance log is part of the public repository. I reviewed every part of the manuscript and take full responsibility for its content. The declaration is repeated in the manuscript's Transparency section.

Data and code. The data are public Wikimedia dumps. The code, aggregates, robustness tables, figure data and logs are released on GitHub and archived on Zenodo; the URLs are given in the Data Availability Statement. Derived editor-level files are not released because they could be re-identified from public edit histories; the code regenerates them.

The manuscript body is about 6,400 words including tables and figure captions, with a 200-word abstract, four figures and two tables; a Supplementary Material file contains eight tables and two figures. I have no conflicts of interest to declare.

Suggested reviewers (no collaboration or conflict with any of them) are researchers working on Wikipedia quality control and measurement validity in peer production, for example [names and affiliations to be confirmed by the author before submission].

Thank you for considering the manuscript.

Sincerely,

[Name]
[Affiliation]
[ORCID]
[Email]
