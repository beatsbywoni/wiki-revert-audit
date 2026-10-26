# 코드북 v0.1 — 파생 변수 정의

원자료 열 이름은 mediawiki_history 덤프 70열(`03_pipeline/01_schema.py`의 `COLUMNS`)을 그대로 쓴다.

## 앵커 테이블 `02_derived/<wiki>_anchors.parquet` (행 = 앵커 revision)
| 변수 | 정의 |
|---|---|
| wiki_db | 위키 코드 |
| user_id | 편집자 ID(공개 산출물에서는 `user_hash`로 대체) |
| created_by_self | `event_user_is_created_by_self` |
| anchor_rev_id | 본문(ns 0) 첫 revision의 `revision_id` |
| anchor_ts | 그 revision의 `event_timestamp` |
| anchor_rank | 1 = 첫 편집, 2..5 = K=5 보조 앵커 |
| page_id | 편집된 문서 |
| rev_sha1 | `revision_text_sha1`(D3 재계산용) |
| is_reverted_d1 | `revision_is_identity_reverted` |
| reverting_rev_id | `revision_first_identity_reverting_revision_id` |
| sec_to_revert | `revision_seconds_to_identity_revert` |
| tags_anchor | `revision_tags`(mw-reverted 포함 여부 → D2) |
| n_edits_2_60d | 앵커 +2일 ~ +60일 사이 본 편집자 편집 수(잔존) |
| n_edits_90d | 앵커 +90일 안 편집 수(success rate 적격 기준 ≥10) |
| n_reverted_90d_F*_W* | 90일 안 편집 중 되돌려진 수(격자별) |

## 되돌린 쪽 테이블 `02_derived/<wiki>_reverters.parquet` (행 = reverting revision)
| 변수 | 정의 |
|---|---|
| reverting_rev_id | revision_id |
| reverter_user_id | `event_user_id` |
| reverter_is_bot | `event_user_is_bot_by`가 비어 있지 않음(name 또는 group) |
| reverter_bot_by | 'name' / 'group' / '' |
| tags_reverter | `revision_tags` |
| reverter_is_tool | tags에 `mw-rollback`, `huggle`, `twinkle`, `mw-undo`(주의: undo는 사람 수동 되돌림이므로 **기본값은 도구로 치지 않음**; 민감도에서만 포함) 중 하나 포함 |
| reverter_is_manual | tags에 `mw-manual-revert` 포함 |

## 격자 플래그 (앵커 테이블에 붙임)
- 창 W ∈ {24h: 86400초, 7d: 604800초, inf}. `reverted_W = is_reverted_d1 & (sec_to_revert <= W)`.
- 필터 F:
  - F0: `reverted_W`
  - F1_strict: `reverted_W & ~reverter_is_bot`
  - F2_strict: `reverted_W & ~reverter_is_bot & ~reverter_is_tool`
  - F1_replace, F2_replace: D3 재계산에서 첫 비봇(비도구) 되돌림의 시점으로 창 판정(파일럿 이후 구현).
- 정의 D2: `'mw-reverted' in tags_anchor` (창 정보는 없으므로 W∞에만 해당; 창별은 D1·D3로).

## 셀 지표 `04_output/<wiki>_grid.csv`
| 열 | 정의 |
|---|---|
| wiki, year, F, W, D | 셀 식별 |
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
