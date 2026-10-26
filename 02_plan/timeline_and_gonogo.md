# 일정과 go/no-go

## 단계
| 주차 | 작업 | 산출물 |
|---|---|---|
| 0 (착수 1~2일) | V1~V7 검증, 덤프 버전 확인, kowiki 다운로드(사용자 터미널) | WORKLOG 항목, 덤프 메타 기록 |
| 1 (3일) | kowiki 파일럿: 앵커·되돌린 쪽 테이블 → 3×3 격자 → V1 D3 재계산 비교 | `04_output/kowiki_grid.csv`, `04_output/gonogo_report.md` |
| 1 말 | **go/no-go 판정**(아래 기준) | 사용자 결정 |
| 2 | 설계 확정, prereg_draft 확정·커밋·Zenodo 기탁; enwiki·중형 위키 다운로드 시작(며칠) | DOI, 다운로드 로그 |
| 3~4 | 확증 분석(격자, 혼합모형, 용량-반응, OR), 시뮬레이션 | 표·그림 초안 |
| 5 | 독립 재계산(D3 전 위키), 원고 초안(서론·방법·결과), 참고문헌 DOI 대조 | draft v0.x |
| 6 | 전면 검토 2회(내부 → 외부 작업지시서, 각 주장 원자료 재검증) → 투고 패키지 | JASIST 제출 세트 |

## go/no-go 기준 (kowiki 파일럿, 2019-01 이후 앵커)
GO 조건(둘 다 충족):
1. 민감도 존재: W24h 또는 W7d에서 F0 vs F2_strict 짝지은 차이 ≥ 5pp, 또는 success rate 순위 Spearman ρ < .95, 또는 상위 10% 집합의 ≥ 15% 이동.
2. 창 대비: W∞에서 같은 차이의 95% CI가 ±2pp 안(창이 있는 지표만 민감하다는 패턴). 만약 W∞에서도 크게 움직이면 그것도 GO지만 H1 서술을 바꾼다("최종 상태도 정의 의존").

NO-GO 신호:
- 모든 셀 차이 < 2pp이고 ρ > .98: 정의에 둔감. 이 경우 "둔감하다"는 짧은 보고(Communication Methods and Measures Brief 또는 PLOS ONE)로 격하하거나, 추천 2(축구 제공자 일치도)로 전환.
- V1에서 덤프 정의 결함이 커서 D3 재계산이 전 위키에 필요하고 enwiki 처리가 2주 이상이면: 중형 위키 3개로 범위 축소 후 진행(NO-GO 아님, 범위 조정).

## 선점 모니터링
- 2주마다 Zenodo·arXiv·Google Scholar에서 Boté-Vericad 후속과 "revert definition" 신규 문헌 검색. 발견 시 포지셔닝 수정.
