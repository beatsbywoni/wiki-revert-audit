#!/usr/bin/env bash
# mediawiki_history 덤프 다운로드 (사용자가 맥 터미널에서 직접 실행; Cowork은 명령만 만든다)
# 분할 방식(all-time / 연도별 / 월별)은 서버 디렉터리 목록에서 자동 판단한다(2026-10-26 V4: kowiki 는 연도별 2002~2026).
# 사용법:
#   bash 03_pipeline/00_download_dump.sh kowiki                  # 그 위키의 모든 파일
#   bash 03_pipeline/00_download_dump.sh kowiki 2019 2026        # 연도(또는 YYYY-MM) 범위만: 토큰이 사전순으로 [from, to] 안인 파일
#   bash 03_pipeline/00_download_dump.sh enwiki 2016-01 2025-12  # enwiki 월별 범위
# 최신 버전 디렉터리를 자동 탐지한다(최근 2개만 보관되므로 버전을 WORKLOG에 기록할 것). 이어받기(-C -) 지원.
set -euo pipefail
WIKI="${1:?wiki code required}"
FROM="${2:-}"; TO="${3:-}"
BASE="https://dumps.wikimedia.org/other/mediawiki_history"
OUT="$(cd "$(dirname "$0")/.." && pwd)/01_raw/${WIKI}"
mkdir -p "$OUT"

VER="$(curl -fsSL "$BASE/" | grep -oE '20[0-9]{2}-[0-9]{2}/' | tr -d '/' | sort -u | tail -n 1)"
echo "latest version: $VER" | tee -a "$OUT/_download.log"
echo "$VER" > "$OUT/_version.txt"

INDEX="$(curl -fsSL "$BASE/$VER/$WIKI/")"
echo "$INDEX" > "$OUT/_index_${VER}.html"
FILES="$(echo "$INDEX" | grep -oE "${VER}\.${WIKI}\.[0-9a-z-]+\.tsv\.bz2" | sort -u)"
[[ -z "$FILES" ]] && { echo "파일 목록을 찾지 못함: $BASE/$VER/$WIKI/"; exit 1; }

n=0
for f in $FILES; do
  tok="${f#${VER}.${WIKI}.}"; tok="${tok%.tsv.bz2}"          # all-time | YYYY | YYYY-MM
  if [[ -n "$FROM" && "$tok" != "all-time" ]]; then
    [[ "$tok" < "$FROM" ]] && continue
    [[ -n "$TO" && "$tok" > "$TO" ]] && continue
  fi
  echo "GET $BASE/$VER/$WIKI/$f" | tee -a "$OUT/_download.log"
  curl -fL --retry 5 --retry-delay 10 -C - -o "$OUT/$f" "$BASE/$VER/$WIKI/$f"
  n=$((n+1))
done
echo "downloaded/verified $n files" | tee -a "$OUT/_download.log"
ls -lh "$OUT" | tee -a "$OUT/_download.log"
echo "done. 기록: $OUT/_download.log, 버전: $OUT/_version.txt"
