"""V2(봇 판별 한계)·V3(태그 가용 기간) 진단. 02_extract_pass1.py 산출물만 있으면 돈다(03 이전에 실행 가능).

주의(2026-10-26 개정): edits 테이블이 "첫 편집 뒤 91일 안" 편집으로 제한되므로 V2 의 모집단은 신규 편집자의 편집이다.

V2: 되돌려진 편집(등록·비봇 편집자의 ns0 편집 중 D1=1)의 sec_to_revert 분포를 되돌린 쪽 부류별로 비교.
    부류: bot_cur(현재 is_bot_by), bot_hist(historical), 둘 다 아님(nonbot) / 익명(anon). 이름/그룹 근거도 분리.
    비봇인데 매우 빠른(≤5s, ≤30s) 되돌림이 많으면 미등록 봇·반자동 도구 의심 → 상위 50 계정을 02_derived 에 사용자명과 함께
    저장(공개 금지)하고, 04_output 에는 집계만 쓴다.
V3: mw-reverted·mw-undo·mw-rollback·mw-manual-revert·huggle·twinkle 태그가 처음 나타난 월과 연도별 건수.

사용법: python 03_pipeline/07_diagnostics_v2_v3.py kowiki
출력  04_output/<wiki>_v2_bot_speed.md, 04_output/<wiki>_v3_tags.md, 02_derived/<wiki>_v2_fast_nonbot_reverters.csv
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
SPEED_CUTS = [("≤5s", 5), ("≤30s", 30), ("≤60s", 60), ("≤1h", 3600), ("≤24h", 86400), ("≤7d", 604800)]


def tag_set(s):
    return set(t.strip() for t in s.split(",") if t.strip()) if isinstance(s, str) and s else set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wiki")
    ap.add_argument("--fast-sec", type=int, default=5)
    a = ap.parse_args()
    d = os.path.join(ROOT, "02_derived")
    o = os.path.join(ROOT, "04_output")
    os.makedirs(o, exist_ok=True)

    # 되돌려진 편집(등록·비봇 편집자, ns0)만 읽기
    ed = pq.read_table(os.path.join(d, f"{a.wiki}_ns0_edits.parquet"),
                       columns=["event_timestamp", "event_user_id", "revision_first_identity_reverting_revision_id",
                                "revision_seconds_to_identity_revert", "tag_mw_reverted"],
                       filters=pc.field("revision_is_identity_reverted") == True).to_pandas()  # noqa: E712
    need = ed["revision_first_identity_reverting_revision_id"].dropna().astype("int64").unique()
    rv_all_cols = ["revision_id", "event_timestamp", "revision_tags"]
    rv = pq.read_table(os.path.join(d, f"{a.wiki}_reverters.parquet"),
                       filters=pc.field("revision_id").isin(need.tolist())).to_pandas()
    rv = rv.rename(columns={"revision_id": "reverting_rev_id"}).drop_duplicates("reverting_rev_id")
    # V3 용: 되돌린 revision 전체의 태그·시각만(사용자명 불필요)
    rv_tags = pq.read_table(os.path.join(d, f"{a.wiki}_reverters.parquet"), columns=["event_timestamp", "revision_tags"]).to_pandas()
    m = ed.merge(rv[["reverting_rev_id", "event_user_id", "event_user_text", "event_user_is_bot_by",
                     "event_user_is_bot_by_historical", "event_user_is_anonymous", "revision_tags"]]
                 .rename(columns={"event_user_id": "rv_user_id", "event_user_text": "rv_user_text",
                                  "revision_tags": "rv_tags"}),
                 left_on="revision_first_identity_reverting_revision_id", right_on="reverting_rev_id", how="left")
    m["sec"] = m["revision_seconds_to_identity_revert"].astype(float)
    cur = m["event_user_is_bot_by"].fillna("")
    hist = m["event_user_is_bot_by_historical"].fillna("")
    m["joined"] = m["reverting_rev_id"].notna()
    m["cls"] = np.select(
        [~m["joined"], m["event_user_is_anonymous"].fillna(False).astype(bool),
         cur.ne("") & hist.ne(""), cur.ne("") & hist.eq(""), cur.eq("") & hist.ne("")],
        ["join_failed", "anon", "bot_cur&hist", "bot_cur_only", "bot_hist_only"], default="nonbot_registered")
    m["bot_by_name"] = cur.str.contains("name") | hist.str.contains("name")
    m["bot_by_group"] = cur.str.contains("group") | hist.str.contains("group")
    rvt = m["rv_tags"].fillna("").map(tag_set)
    m["rv_tool"] = rvt.map(lambda s: bool(s & schema.TOOL_TAGS_DEFAULT))
    m["rv_undo"] = rvt.map(lambda s: "mw-undo" in s)
    m["rv_rollback"] = rvt.map(lambda s: "mw-rollback" in s)
    m["rv_manual"] = rvt.map(lambda s: "mw-manual-revert" in s)
    m["year"] = m["event_timestamp"].dt.year

    lines = [f"# V2 진단 — {a.wiki}: 되돌린 쪽 부류별 되돌림 속도", "",
             f"되돌려진 편집(등록·비봇 편집자 ns0, D1=1): {len(m):,}건. 되돌린 revision join 실패: {int((~m['joined']).sum()):,}건.", ""]
    g = m.groupby("cls")["sec"]
    q = g.describe(percentiles=[.1, .25, .5, .75, .9]).drop(columns=["mean", "std"])
    q["share"] = g.size() / len(m)
    lines += ["## 부류별 건수·분위수(초)", q.round(2).to_markdown(), ""]
    rows = []
    for c, sub in m.groupby("cls"):
        r = {"cls": c, "n": len(sub)}
        for name, s in SPEED_CUTS:
            r[name] = (sub["sec"] <= s).mean()
        r["tool_tag"] = sub["rv_tool"].mean(); r["undo"] = sub["rv_undo"].mean(); r["rollback"] = sub["rv_rollback"].mean()
        r["manual_tag"] = sub["rv_manual"].mean()
        rows.append(r)
    lines += ["## 부류별 창 안 비율과 태그 비율", pd.DataFrame(rows).round(4).to_markdown(index=False), ""]
    bots = m[m["cls"].str.startswith("bot")]
    lines += ["## 봇 판별 근거(봇 부류 안에서)",
              f"- name 정규식만: {int((bots['bot_by_name'] & ~bots['bot_by_group']).sum()):,}, group 만: "
              f"{int((~bots['bot_by_name'] & bots['bot_by_group']).sum()):,}, 둘 다: {int((bots['bot_by_name'] & bots['bot_by_group']).sum()):,}", ""]

    # 연도별 첫 되돌림 점유율(용량-반응 X축 후보)
    yr = m.groupby("year").agg(n=("sec", "size"),
                               bot_share=("cls", lambda s: s.str.startswith("bot").mean()),
                               anon_share=("cls", lambda s: (s == "anon").mean()),
                               tool_share=("rv_tool", "mean"), undo_share=("rv_undo", "mean"),
                               manual_tag_share=("rv_manual", "mean"),
                               med_sec=("sec", "median"), p_le_24h=("sec", lambda s: (s <= 86400).mean()))
    lines += ["## 연도별 첫 되돌림의 부류 점유율", yr.round(4).to_markdown(), ""]

    # 비봇 고속 되돌림 계정 (사용자명 포함 → 02_derived 에만)
    nb = m[(m["cls"] == "nonbot_registered")]
    fast = nb[nb["sec"] <= a.fast_sec]
    top = (fast.groupby(["rv_user_id", "rv_user_text"]).agg(n_fast=("sec", "size"), med_sec=("sec", "median"),
                                                            tool_share=("rv_tool", "mean"), rollback_share=("rv_rollback", "mean"),
                                                            undo_share=("rv_undo", "mean"))
           .reset_index().sort_values("n_fast", ascending=False))
    tot = nb.groupby("rv_user_id").size().rename("n_total_reverts")
    top = top.merge(tot, on="rv_user_id", how="left")
    top["fast_share"] = top["n_fast"] / top["n_total_reverts"]
    top.head(50).to_csv(os.path.join(d, f"{a.wiki}_v2_fast_nonbot_reverters.csv"), index=False)
    lines += [f"## 비봇 등록 계정의 고속(≤{a.fast_sec}s) 되돌림",
              f"- 비봇 되돌림 {len(nb):,}건 중 ≤{a.fast_sec}s {len(fast):,}건({len(fast)/max(len(nb),1):.2%}); 계정 수 {top.shape[0]:,}",
              f"- 상위 50 계정이 차지하는 고속 되돌림 비율: {top.head(50)['n_fast'].sum()/max(len(fast),1):.1%}",
              f"- 상위 50 목록(사용자명 포함, 비공개): 02_derived/{a.wiki}_v2_fast_nonbot_reverters.csv",
              "- 수동 점검 기준: 이름에 bot 이 없는 봇, 전직 봇, Huggle/롤백 사용자인지 판단해 WORKLOG 에 기록", ""]
    with open(os.path.join(o, f"{a.wiki}_v2_bot_speed.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("\n".join(lines[:12]))

    # V3: 태그 가용 기간
    def tag_first_and_yearly(df, col, label):
        ts = df["event_timestamp"]
        tags = df[col].fillna("").map(tag_set)
        out = []
        for t in schema.TAGS_OF_INTEREST:
            has = tags.map(lambda s: t in s)
            if has.any():
                first = ts[has].min()
                by_year = ts[has].dt.year.value_counts().sort_index()
                out.append(dict(source=label, tag=t, first_month=first.strftime("%Y-%m"), n=int(has.sum()),
                                by_year=", ".join(f"{y}:{n}" for y, n in by_year.items())))
            else:
                out.append(dict(source=label, tag=t, first_month="(없음)", n=0, by_year=""))
        return pd.DataFrame(out)

    ed_tag = ed[["event_timestamp"]].copy(); ed_tag["revision_tags"] = np.where(ed["tag_mw_reverted"], "mw-reverted", "")
    v3 = pd.concat([tag_first_and_yearly(rv_tags, "revision_tags", "reverting revisions(모든 ns·사용자)"),
                    tag_first_and_yearly(ed_tag, "revision_tags", "reverted ns0 edits(등록·비봇, mw-reverted 만)")], ignore_index=True)
    v3_lines = [f"# V3 진단 — {a.wiki}: 태그 첫 출현 월과 연도별 건수", "", v3.to_markdown(index=False), "",
                "분기: 태그 기반 F2(도구 제외)·D2(mw-reverted)는 해당 태그 첫 출현 월 이후만 주 분석."]
    with open(os.path.join(o, f"{a.wiki}_v3_tags.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(v3_lines))
    print("\n".join(v3_lines))


if __name__ == "__main__":
    main()
