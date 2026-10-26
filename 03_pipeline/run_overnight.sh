#!/usr/bin/env bash
# 밤샘 배치 드라이버 (2026-10-26). 사용자가 맥 터미널에서 실행:
#   cd ~/Desktop/wiki-revert-audit && caffeinate -i bash 03_pipeline/run_overnight.sh 2>&1 | tee -a 04_logs/overnight_$(date +%Y%m%d_%H%M).log
# 위키별로 다운로드(이어받기) → 02 → 07 → 03 → 06 → 04. 한 위키가 실패해도 다음 위키로 넘어간다.
# 단계별 완료 표식(02_derived/<wiki>.<step>.done)이 있으면 그 단계는 건너뛴다(재실행 안전). 다시 하려면 표식을 지운다.
# 디스크 여유가 MIN_FREE_GB 미만이면 그 위키의 다운로드를 건너뛴다.
set -u
cd "$(dirname "$0")/.."
MIN_FREE_GB=${MIN_FREE_GB:-40}
D=02_derived; mkdir -p "$D" 04_output 04_logs

free_gb () { df -g . | awk 'NR==2{print $4}'; }
step () {  # step <wiki> <name> <cmd...>
  local wiki=$1 name=$2; shift 2
  if [[ -f "$D/$wiki.$name.done" ]]; then echo "--- [$wiki] $name: skip (done)"; return 0; fi
  echo "--- [$wiki] $name: start $(date '+%F %T')"
  if "$@"; then touch "$D/$wiki.$name.done"; echo "--- [$wiki] $name: ok $(date '+%F %T')"; return 0
  else echo "!!! [$wiki] $name: FAILED $(date '+%F %T')"; return 1; fi
}
run_wiki () {  # run_wiki <wiki> [download range args...]
  local wiki=$1; shift
  echo "=================== $wiki  $(date "+%F %T")  free $(free_gb)GB"
  if [[ ! -f "$D/$wiki.download.done" && $(free_gb) -lt $MIN_FREE_GB ]]; then echo "!!! [$wiki] 디스크 여유 부족, 건너뜀"; return 1; fi
  step "$wiki" download bash 03_pipeline/00_download_dump.sh "$wiki" "$@" || return 1
  step "$wiki" 02 python3 03_pipeline/02_extract_pass1.py "$wiki" --chunksize 1000000 || return 1
  step "$wiki" 07 python3 03_pipeline/07_diagnostics_v2_v3.py "$wiki" || true
  step "$wiki" 03 python3 03_pipeline/03_build_anchor_table.py "$wiki" || return 1
  step "$wiki" 06 python3 03_pipeline/06_recompute_reverts_d3.py "$wiki" || return 1
  step "$wiki" 04 python3 03_pipeline/04_audit_grid.py "$wiki" --min-year 2019 || return 1
  echo "=================== $wiki done $(date '+%F %T')  free $(free_gb)GB"
}

# 순서: kowiki(새 앵커 정의로 재실행, 10분) → enwiki(2018-01~2026-09 월별, 가장 큼) → frwiki(Salebot) → dewiki → jawiki
run_wiki kowiki
run_wiki enwiki 2018-01 2026-09
run_wiki frwiki
run_wiki dewiki
run_wiki jawiki
echo "ALL DONE $(date '+%F %T')"; ls -la 04_output | head -40; df -h .
