# 03_pipeline

실행 순서(kowiki 파일럿). 다운로드와 긴 배치는 사용자가 맥 터미널에서 실행한다(Cowork 쪽 셸은 호출당 180초 제한).

```bash
cd ~/Desktop/wiki-revert-audit
python3 -m pip install -r 03_pipeline/requirements.txt
bash   03_pipeline/00_download_dump.sh kowiki                 # 01_raw/kowiki/<ver>.kowiki.all-time.tsv.bz2 (+ _version.txt)
caffeinate -i python3 03_pipeline/02_extract_pass1.py kowiki  # 02_derived/kowiki_{ns0_edits,reverters,ns0_all_revs}.parquet
python3 03_pipeline/07_diagnostics_v2_v3.py kowiki            # 04_output/kowiki_v2_bot_speed.md, kowiki_v3_tags.md (V2·V3)
python3 03_pipeline/03_build_anchor_table.py kowiki           # 02_derived/kowiki_anchors.parquet (strict 격자 플래그)
caffeinate -i python3 03_pipeline/06_recompute_reverts_d3.py kowiki   # D3(refinery 규칙 재현) + replace 변형 + 반경15 변형, D1≠D3 진단
python3 03_pipeline/04_audit_grid.py kowiki --min-year 2019   # 04_output/kowiki_grid.csv, kowiki_gonogo_report.md
python3 03_pipeline/05_simulation_skeleton.py                 # 04_output/simulation_grid.csv
```

스모크 테스트(합성 자료, 1분): `python3 03_pipeline/99_make_synthetic_dump.py` 후 위 02→07→03→06→04를 `synthwiki`로.

| 스크립트 | 역할 | 상태 |
|---|---|---|
| 00_download_dump.sh | 최신 덤프 버전 탐지·다운로드(소형 all-time / 중형 연도 / enwiki 월별) | 작성, 실행 미검증(네트워크) |
| 01_schema.py | 70열 스키마, 창·태그 상수. V1·V2 반영: parent id·historical 봇·사용자명 열 추가 | 문서 대조 완료(2026-10-26) |
| 02_extract_pass1.py | 스트리밍 추출 3종 parquet | 합성 자료로 검증(2026-10-26 개정판) |
| 07_diagnostics_v2_v3.py | V2(되돌린 쪽 부류별 속도, 비봇 고속 계정 상위 50 → 02_derived 비공개)·V3(태그 첫 출현 월) | 합성 자료로 검증 |
| 03_build_anchor_table.py | 앵커·되돌린 쪽 join·strict 플래그·잔존·90일 활동. 봇 = 현재 ∪ historical, F1h(historical만) 민감도 | 합성 자료로 검증 |
| 06_recompute_reverts_d3.py | sha1 재계산. refinery 규칙(반경 없음·no-op 필터·같은 base 제외) 정확 재현 + mwreverts 반경 15 변형, replace 변형, D1≠D3 | 손수 만든 11개 사례 단위검사 통과 + 합성 자료 |
| 04_audit_grid.py | 3×3 격자(strict·replace·radius15), 부트스트랩 CI, success rate 순위, OR, go/no-go 보고 | 합성 자료로 검증 |
| 05_simulation_skeleton.py | 파라미터 격자 시뮬레이션 | 골격 |

덤프 정의 요약(V1, 04_logs/WORKLOG.md 참조): `revision_is_identity_reverted`는 반경·시간 제한 없이 문서 전체 역사에서
"base 가 앞에 있는 같은-sha1 revision 이 뒤에 존재"하면 true. 첫 되돌림 revision 과 초 단위 시차를 기록. 삭제된 revision 도 포함.
mwreverts(문헌 관행)는 반경 15가 기본이라 D1 보다 적게 잡는다 → 06 의 radius15 변형으로 그 차이를 보고한다.

미구현(파일럿 뒤): 혼합모형(statsmodels MixedLM 또는 R lme4), 위키×연도 용량-반응 그림, D2 태그 정의 비교 표, 공개용 난수 ID 변환,
enwiki 용 2차 추출(--no-allrevs 뒤 앵커 문서만).
