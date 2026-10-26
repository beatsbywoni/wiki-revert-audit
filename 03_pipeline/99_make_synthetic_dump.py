"""스모크 테스트용 합성 덤프 생성 (실제 자료 아님). 파이프라인이 끝까지 도는지 확인하는 용도.

주의: 합성 자료의 D1 플래그는 무작위 생성이고 D3(sha1 재계산)는 문서 흐름에서 계산되므로 둘의 불일치가 크게 나온다.
이는 합성 자료의 성질이며 실제 덤프에서는 V1 검증 항목으로 해석한다.

python 03_pipeline/99_make_synthetic_dump.py          → 01_raw/synthwiki/2026-09.synthwiki.all-time.tsv.bz2
python 03_pipeline/02_extract_pass1.py synthwiki && python 03_pipeline/03_build_anchor_table.py synthwiki \
  && python 03_pipeline/04_audit_grid.py synthwiki --min-year 2019 --boot 200
"""
import bz2
import os
import sys
from importlib import import_module

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
schema = import_module("01_schema")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(n_users=3000, seed=1):
    rng = np.random.default_rng(seed)
    rows = []
    rev_id = 1
    t0 = pd.Timestamp("2019-01-01", tz="UTC")
    for u in range(1, n_users + 1):
        n_edits = int(rng.integers(1, 30))
        start = t0 + pd.Timedelta(seconds=int(rng.integers(0, 6 * 365 * 86400)))
        created_self = rng.random() < 0.8
        for k in range(n_edits):
            ts = start + pd.Timedelta(seconds=int(k * rng.integers(60, 20 * 86400)))
            reverted = rng.random() < 0.25
            rows.append(dict(user=u, ts=ts, rev=rev_id, reverted=reverted, self=created_self, ns=0 if rng.random() < 0.9 else 1))
            rev_id += 1
    df = pd.DataFrame(rows)
    # 되돌린 쪽 revision 생성: 봇 50%(5초), 도구 20%(10분), 사람 30%(2일 중앙값)
    reverters = []
    rev_map = {}
    for i, r in df[df.reverted].iterrows():
        kind = rng.choice(["bot", "tool", "human"], p=[0.5, 0.2, 0.3])
        delay = {"bot": rng.exponential(5), "tool": rng.exponential(600), "human": rng.lognormal(np.log(2 * 86400), 1.0)}[kind]
        rid = rev_id
        rev_id += 1
        rev_map[r.rev] = (rid, int(delay), kind)
        # 되돌림 = 같은 문서의 직전 revision(rev-500) 내용(sha1)으로 복원. 첫 revision 이면 복원 대상이 없어 D3 는 미탐지(의도된 불일치 사례).
        prev_sha = f"sha{int(r.rev) - 500}" if int(r.rev) > 500 else f"sha_new{rid}"
        reverters.append(dict(rev=rid, ts=r.ts + pd.Timedelta(seconds=int(delay)), kind=kind, page=int(r.rev) % 500 + 1,
                              sha=prev_sha, user=900000 + (1 if kind == "bot" else int(rng.integers(2, 50)))))
    out_rows = []

    def base_row():
        return {c: "" for c in schema.COLUMNS}

    first_ts = df.groupby("user")["ts"].transform("min")
    df["first_ts"] = first_ts
    df["revcount"] = df.groupby("user").cumcount() + 1
    for r in df.itertuples():
        b = base_row()
        b.update(wiki_db="synthwiki", event_entity="revision", event_type="create",
                 event_timestamp=r.ts.strftime("%Y-%m-%d %H:%M:%S.0"), event_user_id=str(r.user),
                 event_user_is_bot_by="", event_user_is_created_by_self=str(r.self).lower(),
                 event_user_is_anonymous="false", event_user_is_temporary="false",
                 event_user_first_edit_timestamp=r.first_ts.strftime("%Y-%m-%d %H:%M:%S.0"),
                 event_user_revision_count=str(r.revcount), page_id=str(int(r.rev) % 500 + 1),
                 page_namespace_historical=str(r.ns), revision_id=str(r.rev),
                 revision_text_sha1=f"sha{r.rev}", revision_is_identity_reverted=str(bool(r.reverted)).lower(),
                 revision_is_identity_revert="false",
                 revision_tags="mw-reverted" if r.reverted else "")
        if r.reverted:
            rid, delay, kind = rev_map[r.rev]
            b.update(revision_first_identity_reverting_revision_id=str(rid), revision_seconds_to_identity_revert=str(delay))
        out_rows.append(b)
    for rv in reverters:
        b = base_row()
        tags = {"bot": "", "tool": "mw-rollback,huggle", "human": "mw-undo"}[rv["kind"]]
        b.update(wiki_db="synthwiki", event_entity="revision", event_type="create",
                 event_timestamp=rv["ts"].strftime("%Y-%m-%d %H:%M:%S.0"), event_user_id=str(rv["user"]),
                 event_user_is_bot_by="name,group" if rv["kind"] == "bot" else "", event_user_is_anonymous="false",
                 event_user_is_temporary="false", event_user_text=f"user{rv['user']}",
                 page_namespace_historical="0", page_id=str(rv["page"]), revision_id=str(rv["rev"]),
                 revision_text_sha1=rv["sha"], revision_is_identity_reverted="false",
                 revision_is_identity_revert="true", revision_tags=tags)
        out_rows.append(b)
    out = pd.DataFrame(out_rows, columns=schema.COLUMNS)
    d = os.path.join(ROOT, "01_raw", "synthwiki")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, "2026-09.synthwiki.all-time.tsv.bz2")
    with bz2.open(path, "wt", encoding="utf-8") as fh:
        out.to_csv(fh, sep="\t", header=False, index=False)
    print(f"synthetic dump: {len(out):,} rows → {path}")


if __name__ == "__main__":
    main()
