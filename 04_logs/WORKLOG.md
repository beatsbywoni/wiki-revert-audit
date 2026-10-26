# 작업 로그

형식: 날짜 · 작업 · 확인한 사실(출처 URL) · 결정 · 다음 할 일

## 2026-10-26 (갤럭시북 Cowork, 패키지 생성)
- 투고 현황 261022(26편)·로드맵 폴더(2027~2031)·09-24 추천 메모 검토 → 28번 주제를 위키백과 되돌림 감사로 결정.
- 선점 점검: Boté-Vericad 2026-10-17 Zenodo(코호트 구성 감사), Formisano 외 2026 HSSC(content-hash 한계 명시). 되돌림 정의 감사는 미발견.
- mediawiki_history 덤프 스키마 70열 확인(wikitech). identity revert 탐지 반경은 문서에 미기재 → V1.
- 합성 자료 스모크 테스트: 02→03→06→04 통과. strict 변형의 Δ가 창에 둔감함을 발견 → H1은 replace 변형으로 검정(설계 §5 갱신).
- 공개·사전등록: OSF 대신 GitHub + Zenodo(사용자 결정).

## (맥 Cowork 시작 후 이어서 기록)

## 2026-10-26 (맥 Cowork 1회차, 착수 검증)

### 환경
- 맥 Cowork 셸은 맥 자체가 아니라 맥 위의 Linux VM(aarch64, 4코어, RAM 3GB, Python 3.10; pandas·pyarrow 설치함). 호출당 180초 제한, 백그라운드 프로세스는 호출 종료 시 함께 종료됨 → kowiki 전체 패스(02·06)는 사용자 터미널에서 실행. `gh`·`caffeinate`는 VM에 없음.
- dumps.wikimedia.org 는 Cowork 쪽(클라우드·VM)에서 403 → 덤프 버전·용량 확인(V4)과 다운로드는 사용자 터미널에서.
- git 미초기화 상태(00_START_HERE §1-2 미실행).

### V1. 덤프의 identity revert 탐지 반경 — 결론: **반경·시간 제한 없음(전체 역사)**
- 확인 방법 (a): wikitech 덤프 문서(https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Edits/Mediawiki_history_dumps)와 MediaWiki_history 문서는 필드 설명("whether this revision was reverted by another future revision")만 있고 탐지 규칙·반경 언급 없음.
- 확인 방법 (b): analytics-refinery-source 원문 확인(https://github.com/wikimedia/analytics-refinery-source/blob/master/refinery-job/src/main/scala/org/wikimedia/analytics/refinery/job/mediawikihistory/denormalized/DenormalizedRevisionsBuilder.scala, 2026-10-26 master).
  - `prepareRevertsLists`: (wiki, page_id, sha1) 로 groupByKey → 시각·id 순 정렬 → "First revision with a given sha1 is the base, others are reverts to the base". 반경·시간 상수 없음(유일한 관련 주석: "We assume there will not be so many reverting events per page for this sort to fail").
  - no-op 필터: parent id 가 직전 같은-sha1 revision 의 id 인 revision 은 되돌림 목록에서 제거(T266374).
  - `updateRevisionAndReverts`: revision i 는 "base 가 i 앞에 있는 revert j > i 가 대기 중"이면 되돌려진 것(첫 되돌림 = 시각·id 최소 j). i 자신이 revert 일 때 같은 base 로의 revert 는 i 를 되돌린 것으로 치지 않음(wider revert 검사). 시차 = ts_j − ts_i(상한 없음).
  - 필터: page_id > 0, sha1 정의됨(삭제·숨김 텍스트 제외). 보관(archive)·현존 revision 모두 포함.
- 참고: mwreverts(https://github.com/mediawiki-utilities/python-mwreverts) `defaults.RADIUS = 15`, Detector 는 최근 radius+1 개 체크섬만 기억 → 문헌 관행(Research:Revert 페이지도 radius 15, 48h 창을 "common practice"로 기술)과 덤프 정의가 다름. 덤프 D1 은 문헌의 identity revert 보다 **넓은** 정의(몇 년 뒤 수백 revision 을 한 번에 되돌린 것도 포함).
- 분기 결정(체크리스트 V1): 반경이 없으므로 **D1 을 주 정의로 쓰고 D3 는 검증용** — 단, 사전등록에 "덤프 정의 = 무반경"을 명시하고, **mwreverts 반경 15 변형(D3r15)을 정의 축에 추가**하는 것을 제안(사용자 확정 필요). 06 스크립트가 refinery 규칙을 그대로 재현(손수 만든 11개 사례 단위검사 통과)하고 반경 15 변형을 함께 산출하도록 개정.
- (c) kowiki 실제 자료의 D1 vs D3 비교는 다운로드 후 실행(06 출력 `d1_d3_mismatch`, `d1_d3_rev_mismatch`).

### V2. 봇 판별의 한계 — 문서·소스 부분
- 소스(UserEventBuilder.scala): `botUsernamePattern = (?i)^.*bot([^a-z].*$|$)` (사용자명에 'bot' 이 오고 그 뒤가 비문자이거나 끝) → 'name'; 그룹에 'bot' 포함 → 'group'. 이름 규칙의 거짓양성 예: Talbot·Cabot·Abbot 같은 사람 이름(끝이 bot)은 봇으로 분류됨. 거짓음성: 이름에 bot 이 없고 그룹 플래그도 없는 봇(미등록 봇), 반자동 도구 사용자.
- 덤프에 두 열: `event_user_is_bot_by`(현재 사용자명·현재 그룹), `event_user_is_bot_by_historical`(사건 시점 사용자명·그룹). 패키지 초안은 현재 열만 썼음 → 02 에서 historical 열과 사용자명을 함께 추출하고, 03 에서 되돌린 쪽 봇 = 현재 ∪ historical(기본), historical 단독(F1h) 민감도로 변경. 앵커 편집자도 historical 봇은 기본 제외(건수 출력).
- 자료 점검(속도 분포·비봇 고속 계정 상위 50)은 07_diagnostics_v2_v3.py 로 다운로드 후 실행. 상위 50 목록은 사용자명이 들어가므로 02_derived(비공개)에만 저장.

### V3. 태그 가용 기간 — 07 스크립트로 산출 예정(mw-reverted·mw-undo·mw-rollback·mw-manual-revert·huggle·twinkle·mw-replace 첫 출현 월).

### V4. 덤프 버전·용량 — 사용자 터미널에서 확인(2026-10-26 21:00)
- 최신 버전 **2026-09**(파일 생성일 2026-10-05). `https://dumps.wikimedia.org/other/mediawiki_history/2026-09/kowiki/`
- **kowiki 는 all-time 단일 파일이 아니라 연도별 분할**(2002~2026, 25개 파일, 합계 약 3.25GB; 최대 2020년 225MB). 패키지 초안의 "소형=all-time" 가정 오류 → 00_download_dump.sh 를 디렉터리 목록 기반 자동 판단으로 개정, research_design §3 수정 필요. 2002~2009 파일은 작아서(총 ~430MB) 전체를 받아도 부담 없음(앵커 코호트 산출에 편집자 '첫 편집' 판정이 필요하므로 전체 기간 필요).
- 체크섬 파일 없음(디렉터리에 tsv.bz2 만). 우절단: 덤프 마지막 월 2026-09 → min-followup 180일이면 앵커는 2026-03 까지.
- 문서상 분할 규칙(참고): 문서상: 월 1회, 최근 2개 버전만 보관, 파일당 ~2GB 상한, enwiki·wikidata·commons 월별, 중형 약 45개 위키 연도별(dewiki·frwiki·jawiki·ruwiki 등), 나머지 all-time 단일 파일. 체크섬 파일 언급 없음.

### V4 추가(21:30). 덤프 TSV 는 **78열**(문서의 70열 아님)
- 02 가 "Number of passed names did not match" 로 실패 → 2002 파일 전수 확인: 모든 행 78열. refinery `MediawikiEvent.scala` 의 `toTSVLine` 필드 순서(78개)로 스키마 확정(01_schema.COLUMNS, 실제 행과 1:1 대조).
- 문서 대비 추가 열: event_log_id(2), event_user_central_id(8), event_user_is_temporary/permanent/cross_wiki(21~23), user_central_id(43), user_is_temporary/permanent(56~57). wikitech 덤프 문서의 70열 표는 구버전.
- 설계 영향: **임시 계정(temporary account, IP 마스킹)** 열이 있으므로 "등록 계정" = 익명 아님 & 임시 아님으로 02 수정(reverters·all_revs 의 is_anonymous 도 익명∪임시). prereg 의 포함 기준 문구에 반영 필요.
- 02 를 kowiki 2002~2006 실제 파일로 검증: 791,961행 8초(VM), ns0 등록·비봇 편집 234,094, 되돌림 revision 11,225, ns0 전체 462,805; D1 되돌림 비율 2.96%, 중앙값 9,093초; 봇 표기 값 `name,group` 515 / `group` 154 / `name` 15; historical 봇 플래그 편집자의 편집 3,066건(현재 비봇). parquet 고정 스키마 적용(빈 열 null 타입 드리프트 수정).
- 처리량 추정: kowiki 전체 약 3.25GB bz2 ≈ 5~6천만 행 → VM 기준 10분 내외, 맥은 더 빠를 것. 03·06 은 전체 테이블을 메모리에 올리므로 맥 터미널에서 실행.
- 테스트 산출물 02_derived/kowiki_test_* 는 삭제해도 됨.

### 파이프라인 변경(03_pipeline/README.md 갱신)
- 01_schema: `revision_parent_id`, `event_user_is_bot_by_historical`, `event_user_text` 추출 열 추가, `MWREVERTS_RADIUS=15`, `TAGS_OF_INTEREST`.
- 02: 위 열을 edits/reverters/all_revs 에 보존.
- 03: 봇 합집합, F1h 민감도, `reverter_join_failed` 진단, historical 봇 편집자 제외.
- 06: refinery 규칙 정확 재현(no-op 필터·같은 base 제외) + mwreverts 반경 변형(d3r_*) + replace 변형(F1r/F2r) + 반경15 격자(F0r15/F1r15/F2r15). sha1 은 64비트 해시로 축약(충돌 확률 무시 가능, 논문 각주 대상).
- 04: radius15 변형 격자 추가.
- 07 신설: V2·V3 진단.
- 합성 자료 스모크 테스트 02→07→03→06→04 통과(2026-10-26).

### 설계에 대한 제안(사용자 확정 필요)
1. 정의 축을 D1(덤프, 무반경) / D3r15(mwreverts 관행) / D2(mw-reverted 태그)로 두고, D3(무반경 재계산)는 D1 검증용으로만 보고.
2. 사전등록 "중단·분기 규칙"의 V1 조항을 "덤프 정의는 무반경임을 확인했으므로 W∞ 주 정의 = D1" 로 확정.
3. 봇 판별 기본값 = 현재 ∪ historical, 민감도 = historical 단독 + 되돌림 속도 임계(≤5s) 보조 지표.

### 다음 할 일
- 사용자: 터미널에서 V4 확인·kowiki 다운로드(명령은 대화에 제시) → 02 → 07 실행 후 결과 공유.
- Cowork: 07 결과로 V2·V3 WORKLOG 기록 → 03·06·04 → go/no-go 보고서.

## 2026-10-26 (맥 Cowork 2회차, kowiki 파일럿 완료 22:40)
- 사용자 터미널: 02(50,946,764행, 454초) → 07 → 03(앵커 557,879; 첫 편집 190,045) → 06(앵커 문서 162,465, ns0 revision 15,557,231행, 40초) → 04. 전 단계 정상.
- **V1 (c) 완료**: kowiki 전수 재계산 D3 vs 덤프 D1 불일치 0.017%(94/555,712, 전부 D1=1·D3=0, D1=0·D3=1은 0건) → refinery 규칙(무반경·no-op 필터·같은 base 제외) 재현 확인. 반경 15 변형은 W∞ 되돌림을 27.9%→25.7%로 낮춤.
- **V2 완료**: 봇 되돌림 1.4%(느림, 중앙값 31일), 익명 25%, 등록 비봇 73%. 이름 정규식만으로는 group 전용 봇 3,328건(봇 중 28%) 누락 → 합집합 유지. 비봇 ≤5초 되돌림 0.67%, 상위 50 계정이 81%, 봇 이름 0, 상위 8개는 undo 100%·고속 26~45%(반자동 스크립트 의심). 계정명 목록은 02_derived(비공개)에만.
- **V3 완료**: mw-rollback 2017-12, mw-undo 2018-01, mw-manual-revert 2020-07, mw-replace 2017-12, mw-reverted는 되돌림 시점 2020-07 이후(이전 앵커도 소급 태그). huggle·twinkle 없음.
- **go/no-go: GO(H1 수정)**. 상세 `04_output/gonogo_report.md`. 핵심: F2r Δ 9.86/9.43/7.69pp(24h/7d/∞), Spearman .764, 하위 10% 이동 55%, OR 0.31~0.92(연도별로 부호 반전), D2≈D3r15(98.8%), D1 vs D2 96.7%.
- 결정 대기(사용자): 보고서 §7의 7개 제안(H1 재서술, 정의 축 3개, 도구 태그 위키별, 확대 위키 enwiki+frwiki+dewiki/jawiki, 음성 대조 정의, 2023~24 급증 탐색, 등록 시점 명시).
- 다음 할 일: 사용자 확정 → research_design·prereg·codebook 갱신 → git init·첫 커밋(사용자) → 확대 위키 V3·V2 진단 → prereg 확정·Zenodo.
