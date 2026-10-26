# 사전등록 초안 v0.1 (GitHub 커밋 고정 + Zenodo 기탁용)

> 절차: 이 문서를 확정 → 커밋 → `git rev-parse HEAD` 해시를 본문에 기입 → 저장소 스냅샷(zip)을 Zenodo에 "Preregistration" 유형으로 기탁 → DOI와 날짜를 타이틀페이지·Transparency 절에 기재. 확정 이후 변경은 전부 `04_logs/DEVIATION_LOG.md`에 번호를 붙여 기록(24번 관행 #14~#38).
> 등록 시점: 파일럿(kowiki) 결과는 본 적이 있으므로 "파일럿 공개 후 등록"임을 명시하고, 확증 분석은 **파일럿에 쓰지 않은 위키(enwiki + 중형)**에서만 수행한다(24번의 파일럿 공개 방식).

## 제목
Which reverts count? Successor filtering and observation windows in Wikipedia revert-based metrics

## 연구 유형
공개 2차 자료의 측정 감사. 확증 가설 H1~H4와 탐색 분석을 구분.

## 자료
- mediawiki_history 덤프 버전 [YYYY-MM] (등록 시 확정). 확증 위키: enwiki, [dewiki/jawiki/plwiki 중 2~3개]. 파일럿(비확증): kowiki.
- 기간: 2010-01-01 ~ [덤프 마지막 완전 월 − 6개월].
- 포함: 등록 계정, `event_user_is_bot_by` 비어 있음, 본문 namespace 0 첫 편집이 기간 안에 있음.
- 제외: 익명 편집, 봇, 첫 편집이 삭제된 문서인 경우(민감도로 포함 버전 보고).

## 가설과 검정
- H1. 짝지은 차이 |Δp| = |p(F0,W) − p(F2_strict,W)|는 W24h > W7d > W∞ 순이고, W∞에서 Δp의 95% CI가 ±1pp 안(등가). 검정: 편집자 군집 부트스트랩 2,000회.
- H2. 위키×연도 셀에서 |Δp(W24h)|와 봇·도구 되돌림 점유율의 Spearman ρ > 0 (단측, α=.05), 셀 수 가중 선형 기울기 보고.
- H3. D1(identity)과 D2(mw-reverted 태그) 불일치율은 W24h 상당 지표(D1 24h vs D2)보다 W∞(D1 inf vs D2)에서 낮다. 태그 가용 기간만.
- H4. 되돌림→잔존 OR의 정의 간 범위(9셀 최대−최소)가 F0·W∞ 셀 OR의 95% CI 폭보다 크다.
- 음성 대조: 봇·도구 점유율 < 1%인 셀에서 Δp의 95% CI가 ±1pp 안.
- 다중성: H1~H4는 사전 지정 4개 검정, Holm 보정 보고.

## 사전 지정 분석 선택
- 앵커: 첫 편집(주). K=5(강건성).
- 창 경계: 86,400초 / 604,800초 / 무한. 강건성: 43,200 / 172,800 / 2,592,000.
- 도구 태그 목록: mw-rollback, huggle, twinkle. mw-undo는 도구로 치지 않음(강건성에서 포함).
- 잔존: 앵커 +2일 ~ +60일 편집 ≥1.
- success rate 적격: 첫 90일 편집 ≥10.
- 공개 셀 최소 n: 50.

## 중단·분기 규칙
- V1에서 덤프 정의에 반경이 확인되면 W∞의 주 정의를 D3(sha1 재계산)로 바꾼다(등록 전 확정).
- enwiki 처리 시간이 7일을 넘으면 2016~2025 월별 파일 중 홀수 월만으로 축소(사전 지정).

## 공개
코드·집계·시뮬레이션·편차 로그를 GitHub 저장소와 Zenodo DOI로 공개. 편집자 수준 파생 자료는 난수 ID.

## 등록 메타
- 커밋 해시: [확정 시 기입]
- Zenodo DOI: [기탁 후 기입]
- 등록일: [ ]
