"""Validation of first-revert attribution and description of the page-history samples (round 9; exploratory).

(1) rev_sample_flow.csv: by edition and year of the first edit, the eligible cohort (first edits of self-created accounts from 2019),
    the number sampled (proportional allocation within year, seed 20261026 in 03_build_anchor_table.py) and the number usable
    (preceding revision inside the loaded page history).
(2) rev_attribution_validation.csv: on the usable samples, the dumps' own fields (revision_is_identity_reverted, the first reverting
    revision and the delay to it) against the independent recomputation from content hashes: status confusion matrix, and among edits
    reverted under both, agreement on the first reverting revision, on the delay, on the side of the 24-hour boundary and on the
    class of the first reverter.
(3) rev_radius_fixture.csv: the radius rule as implemented in 06_recompute_reverts_d3.py against python-mwreverts (Detector, radius 15)
    on synthetic page histories that include repeated hashes, consecutive identical hashes, restorations and reverts at the
    15-revision boundary. Skipped with a message if mwreverts is not installed.
"""
import os, sys, importlib.util, warnings
import numpy as np, pandas as pd
warnings.simplefilter("ignore", FutureWarning)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "02_derived"); OUT = os.path.join(ROOT, "04_output")
WIKIS = ["enwiki", "itwiki", "kowiki", "dewiki", "plwiki", "frwiki", "jawiki"]


def b(s): return s.fillna(False).astype(bool).to_numpy()


def cls(bot, tool, user, anon, author):
    bot = b(bot); tool = b(tool) & ~bot; selfr = (user == author).to_numpy() & ~bot & ~tool; anon = b(anon) & ~bot & ~tool & ~selfr
    return np.where(bot, "bot", np.where(tool, "tool", np.where(selfr, "self", np.where(anon, "unregistered", "other manual"))))


def main():
    flow, val = [], []
    for w in WIKIS:
        A = pd.read_parquet(os.path.join(D, f"{w}_anchors.parquet"), columns=["user_id", "anchor_rank", "anchor_year", "created_by_self", "d3_sample"])
        A = A[(A.anchor_rank == 1) & (A.anchor_year >= 2019) & b(A.created_by_self)]
        S = pd.read_parquet(os.path.join(D, f"{w}_decomp.parquet"), columns=["user_id", "anchor_year", "created_by_self", "anchor_on_allrevs", "is_reverted_d1", "reverting_rev_id",
                            "sec_to_revert", "reverter_user_id", "reverter_is_anon", "reverter_is_bot", "reverter_is_tool", "d3_first_rev", "d3_first_sec", "d3_first_user",
                            "d3_first_anon", "d3_first_bot", "d3_first_tool"])
        S = S[b(S.created_by_self) & (S.anchor_year >= 2019)]
        for y, g in A.groupby("anchor_year"):
            flow.append(dict(wiki=w, year=int(y), eligible=len(g), sampled=int(b(g.d3_sample).sum()), usable=int((S.anchor_year == y).sum())))
        f = b(S.is_reverted_d1); r = S.d3_first_sec.notna().to_numpy(); both = f & r
        T = S[both]
        same_rev = (T.reverting_rev_id.astype("int64") == T.d3_first_rev.astype("int64")).to_numpy()
        same_delay = (np.abs(T.sec_to_revert.to_numpy() - T.d3_first_sec.to_numpy()) < 1)
        same_24h = ((T.sec_to_revert.to_numpy() <= 86400) == (T.d3_first_sec.to_numpy() <= 86400))
        c1 = cls(T.reverter_is_bot, T.reverter_is_tool, T.reverter_user_id, T.reverter_is_anon, T.user_id)
        c2 = cls(T.d3_first_bot, T.d3_first_tool, T.d3_first_user, T.d3_first_anon, T.user_id)
        val.append(dict(wiki=w, n=len(S), both_reverted=int(both.sum()), flag_only=int((f & ~r).sum()), recomputed_only=int((~f & r).sum()), neither=int((~f & ~r).sum()),
                        status_agreement=float((f == r).mean()), agreement_among_flag_positive=float(r[f].mean()),
                        same_first_reverting_revision=float(same_rev.mean()), different_first_reverting_revision=int((~same_rev).sum()),
                        same_delay=float(same_delay.mean()), crosses_24h_boundary=int((~same_24h).sum()),
                        same_reverter_class=float((c1 == c2).mean()), different_reverter_class=int((c1 != c2).sum())))
        print("done", w, flush=True)
    pd.DataFrame(flow).to_csv(os.path.join(OUT, "rev_sample_flow.csv"), index=False)
    pd.DataFrame(val).to_csv(os.path.join(OUT, "rev_attribution_validation.csv"), index=False)

    try:
        import mwreverts
    except Exception:
        print("mwreverts not installed; fixture comparison skipped"); return
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    spec = importlib.util.spec_from_file_location("d3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "06_recompute_reverts_d3.py"))
    d3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(d3)
    rng = np.random.default_rng(20261112); rows = []
    kinds = {"random, few states": lambda n: rng.integers(1, 6, n), "random, many states": lambda n: rng.integers(1, 40, n),
             "edit war (two states alternating with noise)": lambda n: np.where(rng.random(n) < .8, 1 + (np.arange(n) % 2), rng.integers(3, 30, n)),
             "consecutive identical hashes": lambda n: np.repeat(rng.integers(1, 12, n), 2)[:n],
             "restoration at the 15-revision boundary": None}
    for kind, gen in kinds.items():
        pages = checked = mism = reverted = 0
        for _ in range(400):
            if gen is None:
                gap = int(rng.integers(13, 19)); sha = np.concatenate([[1], 100 + np.arange(gap), [1], rng.integers(200, 230, 5)])
            else:
                sha = gen(int(rng.integers(5, 60)))
            n = len(sha); rid = np.arange(1, n + 1); parent = np.concatenate([[0], rid[:-1]]); ts = np.arange(n, dtype=float) * 60
            z = np.zeros(n, bool)
            mine = d3.analyze_page(sha.astype(np.uint64), rid, parent, ts, z, z, np.arange(n), 15)
            det = mwreverts.Detector(radius=15); first = {}
            for i in range(n):
                rv = det.process(int(sha[i]), int(rid[i]))
                if rv is not None:
                    for x in rv.reverteds:
                        first.setdefault(int(x), int(rv.reverting))
            for i in range(n):
                m = mine[int(rid[i])]["d3r"]; m = None if m is None else m[0]
                checked += 1; reverted += first.get(int(rid[i])) is not None; mism += (m != first.get(int(rid[i])))
            pages += 1
        rows.append(dict(fixture=kind, pages=pages, revisions_checked=checked, reverted_under_mwreverts=reverted, mismatches=mism))
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "rev_radius_fixture.csv"), index=False)
    print(pd.DataFrame(rows).to_string())


if __name__ == "__main__":
    main()
