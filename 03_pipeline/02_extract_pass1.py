"""1차 패스: 덤프 TSV(bz2)를 스트리밍으로 읽어 세 개의 parquet을 만든다(enwiki 규모를 감당하도록 압축형).

  02_derived/<wiki>_ns0_edits.parquet   등록(익명·임시계정 제외)·비봇(현재 기준) 편집자의 본문(ns 0) revision 생성 이벤트 중
                                        **편집자의 첫 편집 뒤 NEWCOMER_WINDOW_DAYS(91일) 안**의 것만. 앵커(첫 편집)와 잔존·90일 활동 계산에 충분.
                                        historical 봇 플래그·mw-reverted 태그 여부는 bool 로 보존.
  02_derived/<wiki>_reverters.parquet   되돌림을 수행한 revision(revision_is_identity_revert == true)의 속성
                                        (봇·익명·모든 namespace 포함; 사용자명 포함 → 공개 금지)
  02_derived/<wiki>_ns0_all_revs.parquet 본문(ns 0) 모든 revision(봇·익명 포함)의 압축형: page_id, revision_id, parent, sha1 64비트 해시,
                                        ts(초), is_bot(현재∪historical), is_tool(롤백·Huggle·Twinkle), is_tool_sens(+undo)
                                        → 06 이 sha1 로 되돌림을 직접 재계산(D3, replace 변형). --no-allrevs 로 생략 가능.

사용법:
  python 03_pipeline/02_extract_pass1.py kowiki
  python 03_pipeline/02_extract_pass1.py enwiki --chunksize 1000000

메모: 처리량은 맥에서 약 11만 행/초(kowiki 5,100만 행 454초). 긴 실행은 사용자가 터미널에서 `caffeinate -i` 로 실행.
"""
import argparse
import csv
import glob
import os
import sys
import time

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(__file__))
from importlib import import_module
schema = import_module("01_schema")  # 파일명이 숫자로 시작해 import_module 사용

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EDITS_SCHEMA = pa.schema([
    ("event_timestamp", pa.timestamp("ns", tz="UTC")),
    ("event_user_id", pa.int64()),
    ("user_bot_hist", pa.bool_()),
    ("event_user_is_created_by_self", pa.bool_()),
    ("event_user_first_edit_timestamp", pa.timestamp("ns", tz="UTC")),
    ("event_user_revision_count", pa.int64()),
    ("page_id", pa.int64()),
    ("revision_id", pa.int64()),
    ("revision_is_identity_reverted", pa.bool_()),
    ("revision_first_identity_reverting_revision_id", pa.int64()),
    ("revision_seconds_to_identity_revert", pa.int64()),
    ("tag_mw_reverted", pa.bool_()),
])
REVERTERS_SCHEMA = pa.schema([
    ("event_timestamp", pa.timestamp("ns", tz="UTC")),
    ("event_user_id", pa.int64()),
    ("event_user_text", pa.string()),
    ("event_user_is_bot_by", pa.string()),
    ("event_user_is_bot_by_historical", pa.string()),
    ("event_user_is_anonymous", pa.bool_()),
    ("revision_id", pa.int64()),
    ("revision_tags", pa.string()),
])
ALLREVS_SCHEMA = pa.schema([
    ("page_id", pa.int64()),
    ("revision_id", pa.int64()),
    ("parent", pa.int64()),
    ("sha", pa.uint64()),
    ("ts", pa.int64()),
    ("is_bot", pa.bool_()),
    ("is_tool", pa.bool_()),
    ("is_tool_sens", pa.bool_()),
])


def to_bool(s: pd.Series) -> pd.Series:
    return s.str.lower().eq("true")


def to_int(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce").astype("Int64")


def tags_have(s: pd.Series, tags: set) -> pd.Series:
    """쉼표 구분 태그 문자열에 tags 중 하나라도 포함되는지(벡터화)."""
    out = pd.Series(False, index=s.index)
    for t in tags:
        out |= s.str.contains(rf"(?:^|,)\s*{t}\s*(?:,|$)", regex=True, na=False)
    return out


def process_chunk(df: pd.DataFrame, keep_allrevs=True):
    df = df[(df["event_entity"] == "revision") & (df["event_type"] == "create")]
    if df.empty:
        return None, None, None
    ts = pd.to_datetime(df["event_timestamp"], errors="coerce", utc=True)
    anon_or_temp = to_bool(df["event_user_is_anonymous"]) | to_bool(df["event_user_is_temporary"])
    bot_cur = df["event_user_is_bot_by"].ne("")
    bot_hist = df["event_user_is_bot_by_historical"].ne("")

    # (A) 되돌린 쪽: 모든 사용자·namespace
    rev_mask = to_bool(df["revision_is_identity_revert"])
    r = df.loc[rev_mask]
    reverters = pd.DataFrame({
        "event_timestamp": ts[rev_mask], "event_user_id": to_int(r["event_user_id"]),
        "event_user_text": r["event_user_text"], "event_user_is_bot_by": r["event_user_is_bot_by"],
        "event_user_is_bot_by_historical": r["event_user_is_bot_by_historical"],
        "event_user_is_anonymous": anon_or_temp[rev_mask], "revision_id": to_int(r["revision_id"]),
        "revision_tags": r["revision_tags"],
    })

    # (B) 등록·비봇(현재) 편집자의 ns0 편집, 첫 편집 뒤 91일 안
    ns0 = df["page_namespace_historical"] == "0"
    first_ts = pd.to_datetime(df["event_user_first_edit_timestamp"], errors="coerce", utc=True)
    within = (ts - first_ts) <= pd.Timedelta(days=schema.NEWCOMER_WINDOW_DAYS)
    sel = ns0 & ~anon_or_temp & ~bot_cur & within.fillna(False)
    e = df.loc[sel]
    edits = pd.DataFrame({
        "event_timestamp": ts[sel], "event_user_id": to_int(e["event_user_id"]),
        "user_bot_hist": bot_hist[sel], "event_user_is_created_by_self": to_bool(e["event_user_is_created_by_self"]),
        "event_user_first_edit_timestamp": first_ts[sel], "event_user_revision_count": to_int(e["event_user_revision_count"]),
        "page_id": to_int(e["page_id"]), "revision_id": to_int(e["revision_id"]),
        "revision_is_identity_reverted": to_bool(e["revision_is_identity_reverted"]),
        "revision_first_identity_reverting_revision_id": to_int(e["revision_first_identity_reverting_revision_id"]),
        "revision_seconds_to_identity_revert": to_int(e["revision_seconds_to_identity_revert"]),
        "tag_mw_reverted": tags_have(e["revision_tags"], {schema.REVERTED_TAG}),
    })

    allrevs = None
    if keep_allrevs:
        a = df.loc[ns0]
        sha_str = a["revision_text_sha1"].to_numpy()
        sha = pd.util.hash_array(sha_str.astype(object)).astype(np.uint64)
        sha[sha_str == ""] = 0
        allrevs = pd.DataFrame({
            "page_id": to_int(a["page_id"]), "revision_id": to_int(a["revision_id"]),
            "parent": to_int(a["revision_parent_id"]).fillna(-1),
            "sha": sha, "ts": (ts[ns0].astype("int64") // 10**9),
            "is_bot": (bot_cur | bot_hist)[ns0],
            "is_tool": tags_have(a["revision_tags"], schema.TOOL_TAGS_DEFAULT),
            "is_tool_sens": tags_have(a["revision_tags"], schema.TOOL_TAGS_SENSITIVITY),
        })
    return edits, reverters, allrevs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wiki")
    ap.add_argument("--files", nargs="*", help="기본값: 01_raw/<wiki>/*.tsv.bz2")
    ap.add_argument("--chunksize", type=int, default=500_000)
    ap.add_argument("--limit-chunks", type=int, default=None, help="디버그용: 처음 N 청크만")
    ap.add_argument("--no-allrevs", action="store_true", help="ns0 전체 revision 테이블 생략")
    a = ap.parse_args()

    files = a.files or sorted(glob.glob(os.path.join(ROOT, "01_raw", a.wiki, "*.tsv.bz2")))
    if not files:
        sys.exit("덤프 파일이 없습니다. 00_download_dump.sh 먼저 실행")
    out_dir = os.path.join(ROOT, "02_derived")
    os.makedirs(out_dir, exist_ok=True)
    w_edits = pq.ParquetWriter(os.path.join(out_dir, f"{a.wiki}_ns0_edits.parquet"), EDITS_SCHEMA)
    w_rev = pq.ParquetWriter(os.path.join(out_dir, f"{a.wiki}_reverters.parquet"), REVERTERS_SCHEMA)
    w_all = None if a.no_allrevs else pq.ParquetWriter(os.path.join(out_dir, f"{a.wiki}_ns0_all_revs.parquet"), ALLREVS_SCHEMA)
    n_rows = n_edits = n_rev = n_all = 0
    t0 = time.time()
    for f in files:
        print(f"[{a.wiki}] reading {os.path.basename(f)}  ({time.time()-t0:,.0f}s)", flush=True)
        reader = pd.read_csv(
            f, sep="\t", header=None, names=schema.COLUMNS, usecols=schema.USECOLS_REVISIONS,
            dtype=str, na_filter=False, quoting=csv.QUOTE_NONE, compression="bz2",
            chunksize=a.chunksize, encoding="utf-8", on_bad_lines="warn",
        )
        for i, chunk in enumerate(reader):
            if a.limit_chunks and i >= a.limit_chunks:
                break
            n_rows += len(chunk)
            edits, reverters, allrevs = process_chunk(chunk, keep_allrevs=w_all is not None)
            if edits is None:
                continue
            w_edits.write_table(pa.Table.from_pandas(edits, schema=EDITS_SCHEMA, preserve_index=False))
            w_rev.write_table(pa.Table.from_pandas(reverters, schema=REVERTERS_SCHEMA, preserve_index=False))
            n_edits += len(edits); n_rev += len(reverters)
            if w_all is not None:
                w_all.write_table(pa.Table.from_pandas(allrevs, schema=ALLREVS_SCHEMA, preserve_index=False))
                n_all += len(allrevs)
            if i % 20 == 0:
                print(f"  chunk {i}  rows so far {n_rows:,}  {time.time()-t0:,.0f}s", flush=True)
    for w in (w_edits, w_rev, w_all):
        if w is not None:
            w.close()
    print(f"done. rows read {n_rows:,} in {time.time()-t0:,.0f}s; edits {n_edits:,}, reverters {n_rev:,}, all_revs {n_all:,} → {out_dir}")


if __name__ == "__main__":
    main()
