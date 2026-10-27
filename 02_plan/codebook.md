# 코드북 v0.2 — 파생 변수 정의 (2026-10-26 파일럿 반영)

원자료 열 이름은 mediawiki_history 덤프 78열(`03_pipeline/01_schema.py`의 `COLUMNS`, refinery `toTSVLine` 순서)을 그대로 쓴다. 02 단계 테이블은 압축형이다: edits = 첫 편집 뒤 91일 안 편집, all_revs = (page_id, revision_id, parent, sha 64비트 해시, ts 초, is_bot, is_tool, is_tool_sens).

## 앵커 테이블 `02_derived/<wiki>_anchors.parquet` (행 = 앵커 revision)
| 변수 | 정의 |
|---|---|
| wiki_db | 위키 코드 |
| user_id | 편집자 ID(공개 산출물에서는 `user_hash`로 대체) |
| created_by_self | `event_user_is_created_by_self` |
| anchor_rev_id | 편집자의 첫 편집(`event_timestamp == event_user_first_edit_timestamp`)이 ns 0인 경우 그 `revision_id` |
| anchor_ts | 그 revision의 `event_timestamp` |
| anchor_rank | 1 = 첫 편집, 2..5 = 첫 편집 뒤 91일 안 ns0 편집의 2~5번째(K=5) |
| first_edit_ts | `event_user_first_edit_timestamp` |
| anchor_user_bot_hist | 편집자의 historical 봇 플래그(기본 제외) |
| d3_sample | replace·반경15 변형 계산 대상 표본 플래그 |
| anchor_on_allrevs | D3 계산 완료이고 직전 revision이 덤프 범위 안인 앵커(변형 간 비교는 이 집합에서) |
| page_id | 편집된 문서 |
| is_reverted_d1 | `revision_is_identity_reverted` |
| reverting_rev_id | `revision_first_identity_reverting_revision_id` |
| sec_to_revert | `revision_seconds_to_identity_revert` |
| is_reverted_d2 | `revision_tags`에 mw-reverted 포함(D2; 앵커 2020-08 이후만 유효) |
| n_edits_2_60d | 앵커 +2일 ~ +60일 사이 본 편집자 편집 수(잔존) |
| n_edits_90d | 앵커 +90일 안 편집 수(success rate 적격 기준 ≥10) |
| n_reverted_90d_F*_W* | 90일 안 편집 중 되돌려진 수(격자별) |

## 되돌린 쪽 테이블 `02_derived/<wiki>_reverters.parquet` (행 = reverting revision)
| 변수 | 정의 |
|---|---|
| reverting_rev_id | revision_id |
| reverter_user_id | `event_user_id` |
| reverter_is_bot | `event_user_is_bot_by`(현재) 또는 `_historical`이 비어 있지 않음(name 또는 group). `_cur`/`_hist` 분리 열 보존 |
| reverter_is_anon | 익명 또는 임시 계정 |
| tags_reverter | `revision_tags` |
| reverter_is_tool | tags에 `mw-rollback`, `huggle`, `twinkle`, `mw-undo`(주의: undo는 사람 수동 되돌림이므로 **기본값은 도구로 치지 않음**; 민감도에서만 포함) 중 하나 포함 |
| reverter_is_manual | tags에 `mw-manual-revert` 포함 |

## 격자 플래그 (앵커 테이블에 붙임)
- 창 W ∈ {24h: 86400초, 7d: 604800초, inf}. `reverted_W = is_reverted_d1 & (sec_to_revert <= W)`.
- 필터 F:
  - F0: `reverted_W`
  - F1_strict: `reverted_W & ~reverter_is_bot`
  - F2_strict: `reverted_W & ~reverter_is_bot & ~reverter_is_tool`
  - F1h_W: historical 봇만 제외(민감도). F2s_W: 도구에 mw-undo 포함(민감도).
  - F0d3/F1r/F2r (replace 변형): sha1 재계산(refinery 규칙 재현)에서 첫 / 첫 비봇 / 첫 비봇·비도구 되돌림의 시점으로 창 판정.
  - F0r15/F1r15/F2r15: 같은 것을 mwreverts 반경 15로.
- 정의 D2: `is_reverted_d2` (창 정보는 없으므로 W∞에만 해당; 창별은 D1·D3로). 파일럿에서 D2 ≈ D3r15(98.8%).
- D3 진단 열: d3_is_reverted, d3_first_rev_id, d3_sec_to_revert, d3r_*(반경 15), d1_d3_mismatch, d1_d3_rev_mismatch.

## 셀 지표 `04_output/<wiki>_grid.csv`
| 열 | 정의 |
|---|---|
| label, variant(strict / strict_d3sample / replace / radius15), F, W | 셀 식별(연도별 파일은 label=연도) |
| n_anchor | 앵커 수 |
| p_reverted | 되돌림 비율 |
| ci_lo, ci_hi | Wilson 95% |
| delta_vs_F0 | 같은 W의 F0 대비 짝지은 차이(pp) |
| delta_ci_lo, delta_ci_hi | 편집자 군집 부트스트랩 2,000회 |
| rho_success_vs_F0 | success rate 순위 Spearman(F0 대비) |
| or_retention | 되돌림→잔존 odds ratio, 95% CI |
| bot_share | 그 셀에서 첫 되돌림 중 봇 비율(용량-반응 X축) |
| tool_share | 도구 비율 |

## 공개 산출물 규칙
- `user_id`는 SHA-256(salt + id)으로 `user_hash` 대체. salt는 비공개.
- 셀 단위 집계는 n_anchor ≥ 50인 셀만 공개.
