"""2차: 앵커 테이블 구축 (코드북 §앵커 테이블).

앵커 정의(2026-10-26 확정): **편집자의 첫 편집**(event_timestamp == event_user_first_edit_timestamp)이고 그 편집이 본문(ns 0)인 것.
  첫 편집이 다른 namespace 였던 편집자는 앵커가 없다(비율을 출력). 이 정의는 덤프 한 행만으로 판정되므로 enwiki 처럼
  부분 기간(월별 파일)만 받아도 된다. kowiki 전 기간 자료에서는 구 정의(첫 ns0 편집, --anchor first-ns0)와 비교 가능.
  보조 앵커 K=5: 첫 편집 뒤 91일 안 ns0 편집의 2~5번째.

봇 판별(V2): 되돌린 쪽 reverter_is_bot = 현재 ∪ historical(기본), _cur/_hist 분리 보존. 앵커 편집자의 historical 봇은 기본 제외.
D3 표본: enwiki 규모에서는 replace 변형(06)을 표본 앵커에서만 계산. --d3-sample N (기본 60,000; 2019+ self-created 첫 편집 앵커 중
  연도 층화 무작위, 전체가 N 이하이면 전수). 플래그 열 d3_sample.

입력  02_derived/<wiki>_ns0_edits.parquet, <wiki>_reverters.parquet
출력  02_derived/<wiki>_anchors.parquet
사용법: python 03_pipeline/03_build_anchor_table.py kowiki [--anchor first-edit|first-ns0] [--d3-sample 60000]
"""
import argparse
import os
import sys
from importlib import import_module

import numpy as np
import pandas as pd
pd.set_option("future.no_silent_downcasting", True)
import pyarrow.compute as pc
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(__file__))
schema = import_module("01_schema")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def tag_set(s):
    return set(t.strip() for t in s.split(",") if t.strip()) if isinstance(s, str) and s else set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wiki")
    ap.add_argument("--k", type=int, default=5, help="보조 앵커: 첫 K 편집")
    ap.add_argument("--min-followup-days", type=int, default=180, help="덤프 끝까지 최소 추적 기간이 확보된 앵커만(우절단 통제)")
    ap.add_argument("--anchor", choices=["first-edit", "first-ns0"], default="first-edit")
    ap.add_argument("--keep-hist-bot", action="store_true")
    ap.add_argument("--d3-sample", type=int, default=60000)
    ap.add_argument("--d3-min-year", type=int, default=2019)
    ap.add_argument("--seed", type=int, default=20261026)
    a = ap.parse_args()
    d = os.path.join(ROOT, "02_derived")
    edits = pd.read_parquet(os.path.join(d, f"{a.wiki}_ns0_edits.parquet"))
    edits = edits.dropna(subset=["event_user_id", "event_timestamp"])
    n_users_all = edits["event_user_id"].nunique()
    hist_bot_users = set(edits.loc[edits["user_bot_hist"], "event_user_id"].unique())
    if not a.keep_hist_bot and hist_bot_users:
        edits = edits[~edits["event_user_id"].isin(hist_bot_users)]
    edits = edits.sort_values(["event_user_id", "event_timestamp", "revision_id"])
    edits["rank"] = edits.groupby("event_user_id").cumcount() + 1
    dump_end = edits["event_timestamp"].max()

    if a.anchor == "first-edit":
        is_first = edits["event_timestamp"] == edits["event_user_first_edit_timestamp"]
        first_users = set(edits.loc[is_first & (edits["rank"] == 1), "event_user_id"])
        edits = edits[edits["event_user_id"].isin(first_users)]  # 첫 편집이 ns0 인 편집자만
        share_first_ns0 = len(first_users) / max(n_users_all, 1)
    else:
        share_first_ns0 = np.nan
    anchors = edits[edits["rank"] <= a.k].copy()
    anchors = anchors.rename(columns={
        "event_user_id": "user_id", "event_timestamp": "anchor_ts", "revision_id": "anchor_rev_id",
        "revision_is_identity_reverted": "is_reverted_d1",
        "revision_first_identity_reverting_revision_id": "reverting_rev_id",
        "revision_seconds_to_identity_revert": "sec_to_revert", "tag_mw_reverted": "is_reverted_d2",
        "event_user_is_created_by_self": "created_by_self", "rank": "anchor_rank",
        "user_bot_hist": "anchor_user_bot_hist", "event_user_first_edit_timestamp": "first_edit_ts",
    })
    anchors = anchors[(dump_end - anchors["anchor_ts"]).dt.days >= a.min_followup_days]

    # 되돌린 쪽 속성 join: 필요한 revision 만 pyarrow 필터로 읽는다(enwiki 용량 대책)
    need = pd.concat([anchors["reverting_rev_id"], edits["revision_first_identity_reverting_revision_id"]]).dropna().astype("int64").unique()
    rv = pq.read_table(os.path.join(d, f"{a.wiki}_reverters.parquet"),
                       columns=["revision_id", "event_user_id", "event_user_is_bot_by", "event_user_is_bot_by_historical",
                                "event_user_is_anonymous", "revision_tags", "event_timestamp"],
                       filters=pc.field("revision_id").isin(need.tolist())).to_pandas()
    rv = rv.rename(columns={
        "revision_id": "reverting_rev_id", "event_user_id": "reverter_user_id",
        "event_user_is_bot_by": "reverter_bot_by", "event_user_is_bot_by_historical": "reverter_bot_by_hist",
        "revision_tags": "tags_reverter", "event_timestamp": "reverter_ts", "event_user_is_anonymous": "reverter_is_anon",
    }).drop_duplicates("reverting_rev_id")
    rv["reverter_is_bot_cur"] = rv["reverter_bot_by"].fillna("").ne("")
    rv["reverter_is_bot_hist"] = rv["reverter_bot_by_hist"].fillna("").ne("")
    rv["reverter_is_bot"] = rv["reverter_is_bot_cur"] | rv["reverter_is_bot_hist"]
    tr = rv["tags_reverter"].fillna("").map(tag_set)
    rv["reverter_is_tool"] = tr.map(lambda s: bool(s & schema.TOOL_TAGS_DEFAULT))
    rv["reverter_is_tool_sens"] = tr.map(lambda s: bool(s & schema.TOOL_TAGS_SENSITIVITY))
    rv["reverter_is_manual"] = tr.map(lambda s: "mw-manual-revert" in s)
    rv["reverter_is_undo"] = tr.map(lambda s: "mw-undo" in s)
    rvcols = ["reverting_rev_id", "reverter_user_id", "reverter_is_anon", "reverter_ts", "reverter_is_bot_cur",
              "reverter_is_bot_hist", "reverter_is_bot", "reverter_is_tool", "reverter_is_tool_sens",
              "reverter_is_manual", "reverter_is_undo"]
    anchors = anchors.merge(rv[rvcols], on="reverting_rev_id", how="left")
    for c in ["reverter_is_bot_cur", "reverter_is_bot_hist", "reverter_is_bot", "reverter_is_tool",
              "reverter_is_tool_sens", "reverter_is_manual", "reverter_is_undo"]:
        anchors[c] = anchors[c].fillna(False).astype(bool)
    anchors["reverter_join_failed"] = anchors["is_reverted_d1"] & anchors["reverter_ts"].isna()

    # 격자 플래그 (strict 변형; replace 변형은 06)
    sec = anchors["sec_to_revert"].astype("float")
    for wname, wsec in schema.WINDOWS.items():
        in_w = anchors["is_reverted_d1"] & ((sec <= wsec) if wsec is not None else True)
        anchors[f"F0_{wname}"] = in_w
        anchors[f"F1_{wname}"] = in_w & ~anchors["reverter_is_bot"]
        anchors[f"F1h_{wname}"] = in_w & ~anchors["reverter_is_bot_hist"]
        anchors[f"F2_{wname}"] = in_w & ~anchors["reverter_is_bot"] & ~anchors["reverter_is_tool"]
        anchors[f"F2s_{wname}"] = in_w & ~anchors["reverter_is_bot"] & ~anchors["reverter_is_tool_sens"]

    # 편집자 활동: 잔존(+2d~+60d), 첫 90일 편집 수와 되돌림 수(F0/F2, W24h/Winf)
    first = anchors[anchors["anchor_rank"] == 1][["user_id", "anchor_ts"]].rename(columns={"anchor_ts": "t0"})
    e = edits[["event_user_id", "event_timestamp", "revision_is_identity_reverted",
               "revision_first_identity_reverting_revision_id", "revision_seconds_to_identity_revert"]]
    e = e.merge(first, left_on="event_user_id", right_on="user_id", how="inner")
    dt = (e["event_timestamp"] - e["t0"]).dt.total_seconds() / 86400.0
    e["in_2_60"] = (dt >= 2) & (dt <= 60)
    e["in_90"] = (dt >= 0) & (dt <= 90)
    e = e.merge(rv[["reverting_rev_id", "reverter_is_bot", "reverter_is_tool"]],
                left_on="revision_first_identity_reverting_revision_id", right_on="reverting_rev_id", how="left")
    e_bot = e["reverter_is_bot"].fillna(False).astype(bool)
    e_tool = e["reverter_is_tool"].fillna(False).astype(bool)
    s90 = e["revision_seconds_to_identity_revert"].astype("float")
    e["rv_F0_W24h"] = e["in_90"] & e["revision_is_identity_reverted"] & (s90 <= 86400)
    e["rv_F2_W24h"] = e["rv_F0_W24h"] & ~e_bot & ~e_tool
    e["rv_F0_Winf"] = e["in_90"] & e["revision_is_identity_reverted"]
    e["rv_F2_Winf"] = e["rv_F0_Winf"] & ~e_bot & ~e_tool
    act = e.groupby("user_id").agg(
        n_edits_2_60d=("in_2_60", "sum"), n_edits_90d=("in_90", "sum"),
        n_rv_F0_W24h=("rv_F0_W24h", "sum"), n_rv_F2_W24h=("rv_F2_W24h", "sum"),
        n_rv_F0_Winf=("rv_F0_Winf", "sum"), n_rv_F2_Winf=("rv_F2_Winf", "sum"),
    ).reset_index()
    anchors = anchors.merge(act, on="user_id", how="left")
    anchors["retained_2_60"] = anchors["n_edits_2_60d"].fillna(0) > 0
    anchors["anchor_year"] = anchors["anchor_ts"].dt.year

    # D3(replace) 표본: 2019+ self-created 첫 편집 앵커, 연도 층화
    pool = anchors[(anchors["anchor_rank"] == 1) & (anchors["anchor_year"] >= a.d3_min_year) & anchors["created_by_self"].fillna(False)]
    if len(pool) == 0:
        pool = anchors[anchors["anchor_rank"] == 1]
    if len(pool) <= a.d3_sample:
        sample_users = set(pool["user_id"])
    else:
        rng = np.random.default_rng(a.seed)
        frac = a.d3_sample / len(pool)
        sample_users = set(pool.groupby("anchor_year", group_keys=False)
                           .apply(lambda g: g.sample(n=max(1, int(round(len(g) * frac))), random_state=int(rng.integers(1 << 31))))["user_id"])
    anchors["d3_sample"] = anchors["user_id"].isin(sample_users) & (anchors["anchor_rank"] == 1)

    out = os.path.join(d, f"{a.wiki}_anchors.parquet")
    anchors.to_parquet(out, index=False)
    n1 = (anchors["anchor_rank"] == 1).sum()
    print(f"anchors: {len(anchors):,} rows, first-edit anchors {n1:,} (anchor={a.anchor}; 첫 편집이 ns0 인 편집자 비율 "
          f"{share_first_ns0:.3f}); historical-bot editors {'kept' if a.keep_hist_bot else 'dropped'} {len(hist_bot_users):,}; "
          f"reverter join failed {int(anchors['reverter_join_failed'].sum()):,} / reverted {int(anchors['is_reverted_d1'].sum()):,}; "
          f"d3_sample {int(anchors['d3_sample'].sum()):,} → {out}")


if __name__ == "__main__":
    main()
