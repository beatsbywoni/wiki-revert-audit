"""D3: sha1 로 identity revert 를 직접 재계산하고, 되돌린 쪽을 "교체(replace)" 하는 F1r/F2r 플래그를 만든다.

왜 필요한가
- 덤프의 D1 필드는 '첫' 되돌림만 기록한다. 흔한 전처리(봇 되돌림 제외)를 strict 로 재현하면 Δ(F0−F2) 는
  봇·도구가 첫 되돌림을 차지한 비율과 거의 같아져 창에 거의 의존하지 않는다(합성 데이터 스모크 테스트에서 확인).
- H1(창이 있는 지표만 민감)의 진짜 검정 대상은 replace 변형이다: 봇 되돌림을 무시했을 때 '사람이 나중에 되돌렸는가,
  그리고 그 시점이 창 안인가'. 이는 문서별 revision 흐름에서 sha1 로 다시 계산해야 한다.
- 부수 효과: V1 검증(덤프의 탐지 규칙 재현)을 D1 vs D3 불일치로 정량화한다.

덤프(refinery) 규칙 — analytics-refinery-source DenormalizedRevisionsBuilder.scala 를 2026-10-26 원문 확인(04_logs/WORKLOG.md V1):
  1. 반경·시간 제한 없음. 문서 안에서 (sha1) 별로 전체 역사를 묶어 첫 등장 = base, 이후 같은 sha1 = 그 base 로의 revert.
  2. no-op 필터: 같은 sha1 목록(시각·id 순)에서 parent id 가 직전 같은-sha1 revision 의 id 인 revision 은 revert 목록에서 제거.
  3. revision i 는 "base 가 i 보다 앞에 있는 revert j(j>i) 가 존재" 하면 되돌려진 것이며, 첫 되돌림 = 그런 j 중 (시각, id) 최소.
     단 i 자신이 revert(base k)일 때 같은 base k 로의 revert 는 i 를 되돌린 것으로 치지 않는다(같은 상태를 다시 복원한 것).
     → 조건: sha1_j != sha1_i (i 가 no-op 인 드문 경우는 예외로 refinery 그대로 되돌려진 것으로 처리).
  4. 되돌림까지 시간 = ts_j − ts_i. sha1 이 비어 있는(삭제·숨김) revision 은 revert 계산에서 제외.
mwreverts 규칙(문헌 관행, 기본 radius=15) — python-mwreverts detector.py 원문 확인:
  최근 radius+1 개 revision 의 체크섬만 기억. j 의 체크섬이 그 안의 가장 최근 revision k 와 같으면 (k, j) 사이가 되돌려짐.
  → j 가 i 를 되돌림 ⇔ k = (j 이전 가장 최근 같은-sha1) < i 이고 j − k − 1 ≤ radius.

출력 열(anchors.parquet 에 추가)
  d3_*      refinery 규칙 재현(반경 없음): first_rev_id, sec_to_revert, reverter_is_bot, reverter_is_tool, is_reverted
  d3nb_*, d3nt_*   첫 '비봇' / '비봇·비도구' 되돌림(replace 변형의 기반)
  d3r_*     mwreverts 규칙(--radius, 기본 15): first_rev_id, sec_to_revert, is_reverted (+ d3rnb_, d3rnt_)
  F0d3_W*, F1r_W*, F2r_W*      replace 변형 격자(refinery 규칙)
  F0r15_W*, F1r15_W*, F2r15_W* 반경 15 변형 격자(민감도·정의 축 확장용)
  d1_d3_mismatch, d1_d3_rev_mismatch(되돌린 revision id 까지 비교)

입력  02_derived/<wiki>_ns0_all_revs.parquet (02 의 압축형), <wiki>_anchors.parquet (03 의 d3_sample 플래그로 대상 제한)
사용법: python 03_pipeline/06_recompute_reverts_d3.py kowiki [--radius 15]
enwiki 메모: all_revs 가 너무 크면 02 를 --no-allrevs 로 돌리고, 여기서 앵커 문서(page_id) 집합만 2차 추출하도록 확장.
주의: ns0 historical 기준으로 추출한 revision 만 쓰므로, 문서가 다른 namespace 로 이동한 뒤의 revision 은 빠진다
      (D1≠D3 의 한 원인이 될 수 있음; 불일치 사례의 page_namespace 를 진단에서 확인).
"""
import argparse
import os
import sys
import time
from importlib import import_module

import numpy as np
import pandas as pd
import pyarrow.compute as pc
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(__file__))
schema = import_module("01_schema")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def tag_set(s):
    return set(t.strip() for t in s.split(",") if t.strip()) if isinstance(s, str) and s else set()


def analyze_page(sha, rid, parent, ts, bot, tool, anchor_pos, radius):
    """한 문서의 revision 배열(시각·id 순). anchor_pos: 앵커의 위치 인덱스 배열.
    반환: {anchor_rev_id: dict(...)}"""
    n = len(sha)
    bot = np.asarray(bot, dtype=bool)
    tool = np.asarray(tool, dtype=bool)
    first_occ, prev_id, prev_idx = {}, {}, {}
    base_idx = np.full(n, -1, dtype=np.int64)   # refinery: kept revert j 의 base 위치, 아니면 -1
    noop = np.zeros(n, dtype=bool)
    mw_prev = np.full(n, -1, dtype=np.int64)    # mwreverts: j 이전 가장 최근 같은-sha1 위치
    for i in range(n):
        h = sha[i]
        if h == 0:
            continue
        if h in first_occ:
            mw_prev[i] = prev_idx[h]
            if parent[i] == prev_id[h]:
                noop[i] = True
            else:
                base_idx[i] = first_occ[h]
        else:
            first_occ[h] = i
        prev_id[h] = rid[i]
        prev_idx[h] = i

    idx = np.arange(n)
    rid_set = set(rid.tolist())
    out = {}
    for i in anchor_pos:
        res = {"prev_in_range": bool(parent[i] <= 0 or parent[i] in rid_set)}  # 부분 기간 덤프(enwiki) 대책
        # refinery 규칙
        cand = (idx > i) & (base_idx >= 0) & (base_idx < i)
        if not noop[i]:
            cand &= (sha != sha[i])
        cj = np.flatnonzero(cand)
        # mwreverts 규칙(radius)
        candr = (idx > i) & (mw_prev >= 0) & (mw_prev < i) & ((idx - mw_prev - 1) <= radius)
        cjr = np.flatnonzero(candr)
        for prefix, c in (("d3", cj), ("d3r", cjr)):
            for suffix, mask in (("", np.ones(len(c), bool)), ("nb", ~bot[c]), ("nt", ~bot[c] & ~tool[c])):
                sel = c[mask]
                key = prefix + suffix
                if len(sel):
                    j = sel[0]
                    res[key] = (int(rid[j]), float(ts[j] - ts[i]), bool(bot[j]), bool(tool[j]))
                else:
                    res[key] = None
        out[int(rid[i])] = res
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wiki")
    ap.add_argument("--radius", type=int, default=schema.MWREVERTS_RADIUS, help="mwreverts 변형의 반경(revision 수)")
    ap.add_argument("--all-anchors", action="store_true", help="d3_sample 플래그를 무시하고 모든 앵커(첫 편집)에서 계산")
    a = ap.parse_args()
    t0 = time.time()
    d = os.path.join(ROOT, "02_derived")
    anchors = pd.read_parquet(os.path.join(d, f"{a.wiki}_anchors.parquet"))
    target = anchors["anchor_rank"] == 1 if a.all_anchors else anchors["d3_sample"].fillna(False).astype(bool)
    anchor_pages = anchors.loc[target, "page_id"].dropna().astype("int64").unique()
    anchor_ids = anchors.loc[target, "anchor_rev_id"].dropna().astype("int64").unique()
    print(f"D3 target anchors {len(anchor_ids):,} on {len(anchor_pages):,} pages", flush=True)

    # 02 의 압축형 all_revs(page_id, revision_id, parent, sha(uint64), ts(초), is_bot, is_tool, is_tool_sens)
    tbl = pq.read_table(os.path.join(d, f"{a.wiki}_ns0_all_revs.parquet"),
                        columns=["page_id", "revision_id", "parent", "sha", "ts", "is_bot", "is_tool"],
                        filters=pc.field("page_id").isin(anchor_pages.tolist()))
    ar = tbl.to_pandas()
    del tbl
    print(f"all_revs rows on anchor pages: {len(ar):,}  {time.time()-t0:,.0f}s", flush=True)
    ar["is_anchor"] = ar["revision_id"].isin(anchor_ids)
    ar = ar.sort_values(["page_id", "ts", "revision_id"], kind="mergesort").reset_index(drop=True)

    P = ar["page_id"].to_numpy(); SHA = ar["sha"].to_numpy(); RID = ar["revision_id"].to_numpy()
    PAR = ar["parent"].to_numpy(); TS = ar["ts"].to_numpy().astype(np.int64)
    BOT = ar["is_bot"].to_numpy(); TOOL = ar["is_tool"].to_numpy(); ANC = ar["is_anchor"].to_numpy()
    del ar
    starts = np.flatnonzero(np.r_[True, P[1:] != P[:-1]])
    ends = np.r_[starts[1:], len(P)]
    res = {}
    for b, (s, e) in enumerate(zip(starts, ends)):
        apos = np.flatnonzero(ANC[s:e])
        if len(apos) == 0:
            continue
        res.update(analyze_page(SHA[s:e], RID[s:e], PAR[s:e], TS[s:e], BOT[s:e], TOOL[s:e], apos, a.radius))
        if b % 50000 == 0:
            print(f"  pages {b:,}/{len(starts):,}  anchors done {len(res):,}  {time.time()-t0:,.0f}s", flush=True)

    def pick(rev, key, field):
        r = res.get(int(rev)) if pd.notna(rev) else None
        if r is None or r.get(key) is None:
            return np.nan
        return r[key][field]

    for key in ["d3", "d3nb", "d3nt", "d3r", "d3rnb", "d3rnt"]:
        anchors[f"{key}_first_rev_id"] = anchors["anchor_rev_id"].map(lambda v: pick(v, key, 0))
        anchors[f"{key}_sec_to_revert"] = anchors["anchor_rev_id"].map(lambda v: pick(v, key, 1))
    anchors["d3_is_reverted"] = anchors["d3_first_rev_id"].notna()
    anchors["d3r_is_reverted"] = anchors["d3r_first_rev_id"].notna()
    anchors["d3_reverter_is_bot"] = anchors["anchor_rev_id"].map(lambda v: pick(v, "d3", 2))
    anchors["d3_reverter_is_tool"] = anchors["anchor_rev_id"].map(lambda v: pick(v, "d3", 3))
    found = anchors["anchor_rev_id"].map(lambda v: int(v) in res if pd.notna(v) else False)
    prev_ok = anchors["anchor_rev_id"].map(lambda v: res[int(v)]["prev_in_range"] if (pd.notna(v) and int(v) in res) else False)
    anchors["anchor_found_allrevs"] = found
    anchors["anchor_on_allrevs"] = found & prev_ok   # replace·radius 변형은 직전 revision 이 범위 안인 앵커에서만
    d1 = anchors["is_reverted_d1"].astype(bool)
    anchors["d1_d3_mismatch"] = d1 != anchors["d3_is_reverted"]
    same_rev = anchors["reverting_rev_id"].astype("float").eq(anchors["d3_first_rev_id"].astype("float"))
    anchors["d1_d3_rev_mismatch"] = (d1 | anchors["d3_is_reverted"]) & ~same_rev.fillna(False)

    for wname, wsec in schema.WINDOWS.items():
        def inw(col):
            s_ = anchors[col].astype(float)
            return s_.notna() & ((s_ <= wsec) if wsec is not None else True)
        anchors[f"F0d3_{wname}"] = inw("d3_sec_to_revert")
        anchors[f"F1r_{wname}"] = inw("d3nb_sec_to_revert")
        anchors[f"F2r_{wname}"] = inw("d3nt_sec_to_revert")
        anchors[f"F0r{a.radius}_{wname}"] = inw("d3r_sec_to_revert")
        anchors[f"F1r{a.radius}_{wname}"] = inw("d3rnb_sec_to_revert")
        anchors[f"F2r{a.radius}_{wname}"] = inw("d3rnt_sec_to_revert")

    out = os.path.join(d, f"{a.wiki}_anchors.parquet")
    anchors.to_parquet(out, index=False)
    on = anchors["anchor_on_allrevs"]
    mm = anchors.loc[on, "d1_d3_mismatch"].mean()
    mr = anchors.loc[on, "d1_d3_rev_mismatch"].mean()
    print(f"D3 done {time.time()-t0:,.0f}s. target {len(anchor_ids):,} (all_revs 에서 찾은 앵커 {int(found.sum()):,}, "
          f"직전 revision 범위 안 {int(on.sum()):,}); "
          f"D1≠D3 되돌림 여부 불일치 {mm:.5f}, 되돌린 revision 불일치 {mr:.5f} "
          f"(D1=1,D3=0: {int((d1 & ~anchors['d3_is_reverted'] & on).sum()):,}; "
          f"D1=0,D3=1: {int((~d1 & anchors['d3_is_reverted'] & on).sum()):,}); "
          f"radius-{a.radius} 되돌림 {anchors.loc[on, 'd3r_is_reverted'].mean():.4f} vs 무반경 {anchors.loc[on, 'd3_is_reverted'].mean():.4f} → {out}")


if __name__ == "__main__":
    main()
