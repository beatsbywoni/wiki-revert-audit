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

## 2026-10-26 (맥 Cowork 3회차, 23:20 밤샘 배치 시작)
- 사용자 확정: gonogo_report §7 제안 7개 전부 채택. git init·첫 커밋 9f5b190(로컬). GitHub push·Zenodo는 추후.
- 앵커 정의 확정: 편집자의 첫 편집(`event_timestamp == event_user_first_edit_timestamp`)이 ns0인 경우. 부분 기간 덤프(enwiki 2018-01~2026-09)에서도 성립. kowiki 테스트 추출에서 첫 편집이 ns0인 편집자 91%.
- 파이프라인 개정(enwiki 규모 대응): 02 압축형 3테이블(edits = 첫 편집 뒤 91일, all_revs = sha1 64비트 해시·bool), 03 되돌린 쪽 pyarrow 필터 읽기·D3 표본 6만(연도 층화)·`d3_sample`, 06 표본·`anchor_on_allrevs`(직전 revision 범위 안), 04 변형별 격자(strict / strict_d3sample / replace / radius15), 07 신규 편집자 모집단 주의. 합성 자료와 kowiki 2002~2009 실자료로 체인 검증.
- 밤샘 드라이버 `03_pipeline/run_overnight.sh`: kowiki(재실행) → enwiki(2018-01~2026-09, 105파일) → frwiki → dewiki → jawiki. 단계별 `.done` 표식, 디스크 40GB 미만 시 건너뜀. 로그 04_logs/overnight_*.log.
- 설계 문서 갱신: research_design v0.2, prereg_draft v0.2(H1 재서술 = 창 간 차이 Δ(24h)−Δ(∞) 등가 검정, H3 = D2≈D3r15, 음성 대조 = 점유율 <1% 셀, 정의 축 D1/D3r15/D2), codebook v0.2.
- 다음 할 일(아침): 로그 확인 → 위키별 04_output 검토 → 위키 간 비교표(용량-반응: 봇·도구 점유율 vs Δ) → prereg 확정·커밋 해시 고정·Zenodo 기탁(사용자 승인) → 확증 분석 스크립트(혼합모형·용량-반응 그림·OR 범위).

## 2026-10-27 07:50 (밤샘 배치 중간 점검)
- 완료: kowiki(23:22~23:31, 새 앵커 정의 n=47,633, 결과는 구 정의와 거의 동일), enwiki(23:31~06:23; 다운로드 105파일 55GB 4h08m, 02 2h, 04 41m; 앵커 2,189,284, D3 표본 59,680). 진행 중: frwiki 다운로드(17GB, 2022 파일). 디스크 여유 59GB.
- enwiki 핵심: p(24h) 37.0%, 봇 점유 12%(중앙값 8초), 도구 점유 56%; Δ 봇 제외 strict 4.5 / replace 3.0→2.3pp, Δ 봇·도구 제외 strict 21.1 / replace 18.8→17.4pp; Spearman .749, 하위 10% 이동 55%; OR 0.43~0.77. 비교표 04_output/cross_wiki_summary.md.
- 설계 쟁점(사용자 결정 필요): enwiki 결과를 등록 전에 보았으므로 확증 위키를 frwiki·dewiki·jawiki로 둘지, 전체를 서술적 감사로 할지.

## 2026-10-27 14:20 (배치 점검)
- 사용자가 07:50경 배치 중단, 10:47 재시작(이어받기 정상). frwiki 완료(다운로드 21GB, 02 46분; 앵커 346,938, D3 표본 59,985, D1≠D3 0건). dewiki 다운로드 중(13GB, 속도 1.8MB/s로 저하). 디스크 여유 40GB → jawiki는 40GB 기준에 걸려 건너뛸 가능성.
- frwiki 핵심: p(24h) 24.3%, 봇 점유 4.2%(Salebot, 중앙값 3초), 도구 점유 25.5%; Δ 봇 제외 strict 1.0 / replace 0.63→0.49pp; Δ 봇·도구 제외 strict 7.2 / replace 6.36→6.17→5.45pp; Spearman .926, 하위 10% 이동 25%; OR 0.47~0.72.
- 위키 간 용량-반응 확인(도구 점유율 .26/.52/.56 → Δ 6.4/9.8/18.8pp). H1 '+1pp' 절대 기준은 frwiki 미달(0.9pp) → 등록 전 기준 형식 결정 필요(방향성 vs 상대 비율). 비교표 04_output/cross_wiki_summary.md 갱신.

## 2026-10-27 20:00 (밤샘 배치 종료 점검)
- 배치 종료 16:48. dewiki 완료(다운로드 25GB 3h46m, 02 55분; 앵커 236,903, D3 표본 59,995, D1≠D3 1건). jawiki는 디스크 여유 27GB로 건너뜀(ALL DONE). 디스크 여유 30GB, 원자료 01_raw 합계 약 104GB(enwiki 55, dewiki 25, frwiki 21, kowiki 3).
- dewiki 핵심: p(24h) 25.6%, 봇 점유 0.1%(반달 대응 봇 없음, 봇 축 음성 대조), 도구 점유 41%(롤백만); Δ 봇·도구 제외 strict 10.5 / replace 9.59→9.48→8.79pp; Spearman .895, 하위 10% 이동 31%; OR 0.52~0.84.
- 4개 위키 비교표 갱신(04_output/cross_wiki_summary.md). 상대 Δ(Δ/p)가 도구 점유율과 단조(.56/.52/.41/.26 → .51/.45/.38/.26).
- 결정 대기: (1) H1 기준 형식(방향성 CI vs 비율 < 0.95), (2) 확증 위키(미열람: jawiki·plwiki·itwiki 후보; enwiki 원자료 삭제 후 실행), (3) 원자료 보관 범위.

## 2026-10-27 20:30 (사용자 결정 반영)
- 원자료 삭제(사용자 요청): 01_raw/enwiki·frwiki·dewiki 덤프 삭제(약 101GB), 다운로드 로그·버전·인덱스는 01_raw/_meta/<wiki>/ 보존, kowiki 원자료(3.2GB) 유지. 디스크 여유 32 → 105GB. 파생 parquet(02_derived 22GB)과 결과는 유지.
- H1 확정(사용자: 타깃 저널 고려해 추천안 채택): replace 변형 Δ(W24h) − Δ(W∞) > 0 단측 부트스트랩 검정 + 효과 크기 R = Δ(W∞)/Δ(W24h)(R ≥ 0.75 = "대부분 잔존"). prereg_draft·research_design 갱신, 04_audit_grid.py에 h1_window_test 추가(<wiki>_h1_window.csv). kowiki: D = 2.21pp [단측 95% 하한 2.05], R = 0.775 [0.759, 0.792].
- 확증 위키(등록 전 미열람): jawiki·plwiki·itwiki로 prereg에 기재. 드라이버가 인자로 위키 목록을 받도록 개정.
- 다음: 맥에서 4개 탐색 위키 04 재실행(H1 수치 산출) → 확증 위키 배치 → prereg 확정·커밋·Zenodo.

## 2026-10-28 13:40~13:55 (사전등록 완료)
- 확증 배치(jawiki·plwiki·itwiki) 2026-10-27 20:57~2026-10-28 00:05 완료, 오류 없음. 결과 파일은 등록 전 미열람(터미널 로그도 상태 줄만 grep).
- 등록 커밋: 내용 커밋 7fcff3d0f2ec27c7d768f80c21f73c5914558f1a("preregistration v1.0 (content commit)"), 해시 기입 커밋 98226ea. 스냅샷 `git archive HEAD` → _release/wiki-revert-audit_preregistration_7fcff3d0f2ec.zip(821KB, 확증 결과 0개 포함 확인). 등록문 PDF(pandoc+wkhtmltopdf, 3쪽).
- Zenodo 기탁(Claude in Chrome, 사용자 확인 후 Publish): 기록 23720117, DOI 10.5281/zenodo.23720117, concept DOI 10.5281/zenodo.23720116. 유형 Publication/Other(Preregistration 유형 없음), 메타데이터 공개·파일 제한, CC BY 4.0, 키워드 preregistration/Wikipedia reverts/measurement audit. 심사용 공유 링크는 사용자가 직접 생성(자동화 권한 차단).
- 익명 심사 대응: 원고에는 DOI 대신 "deposited on Zenodo, DOI withheld for anonymous review, share link available to the editor" 문구, 게재 후 파일 공개 전환(6번 CER 관행).
- 다음: DOI 기입 커밋 → 확증 결과 열람(jawiki·plwiki·itwiki gonogo_report의 H1~H4 판정) → cross_wiki_summary 7개 위키 갱신 → DEVIATION_LOG 운영 시작.

## 2026-10-28 14:00 (확증 결과 열람, DOI 커밋 278b832 이후)
- 편차 점검: 등록 스냅샷(7fcff3d)의 03_pipeline 과 실행 코드 동일(git diff 없음, 04에 confirmatory_tests 포함). 편차 없음.
- 확증 판정: H1 3/3 지지(D 0.24/0.77/2.49pp, R .92/.88/.84), H2 3/3 지지(S .145/.111/.114), H3 0/3(둘째 조항 기각: 미태그 사례의 반경 밖 비율 .42/.09/.07), H4 2/3(plwiki 1.43 미달), 음성 대조 3/3(8/8 셀). 상세 04_output/cross_wiki_summary.md, 표 cross_wiki_table.csv.
- 등록 후 탐색 #1(H3 기제): 미태그-반경 안 사례에서 익명·수동 되돌림 비중 높음(itwiki 익명 .20 vs 태그 사례 .01). 가설: mw-reverted 는 되돌린 편집의 patrol 승인 뒤 붙는 지연 갱신이라 비자동승인 되돌림은 누락. MediaWiki 소스 확인 필요(원고에서 '검증 완료' 전까지 가설로만 서술).
- 결과 서술 방침: 기각된 H3·plwiki H4 는 그대로 보고(16번 AMPPS 서술 방식). H3 기각은 '태그 정의는 되돌린 사람의 신뢰 등급에 의존한다'는 추가 발견으로 전환.
- 다음: (1) MediaWiki RevertedTagUpdate 소스 확인, (2) 혼합모형·용량-반응 그림·시뮬레이션(05) 실행, (3) 원고 초안(서론·방법·결과) 착수, (4) 심사용 Zenodo 공유 링크(사용자 생성), (5) GitHub push(사용자 승인).

## 2026-10-28 14:20 (등록 후 탐색 #1 확인: mw-reverted 태그의 승인 게이트)
- 출처: MediaWiki Manual:Reverts (https://www.mediawiki.org/wiki/Manual:Reverts): 태그는 revertedTagUpdate 잡으로 적용되며 조건은 (a) undo·rollback·manual revert 로 인식, (b) 되돌려진 편집 수 ≤ $wgRevertedTagMaxDepth(기본 15), (c) 되돌린 편집이 삭제·재되돌림 아님, (d) **자동 승인**: $wgUseRCPatrol 이면 autopatrol 권한자만 즉시, 나머지는 patrol 될 때 재예약, "Reverts that are not patrolled will not be marked with the reverted tag". FlaggedRevs 위키는 autoreview 기준. 소스: includes/Storage/RevertedTagUpdateManager.php(approveRevertedTagForRevision, patrol/autopatrol 시 호출), RevertedTagUpdate.php(shouldExecute), MainConfigSchema.php(ManualRevertSearchRadius=15, RevertedTagMaxDepth=15).
- Wikimedia 설정(operations/mediawiki-config InitialiseSettings.php, dblists/flaggedrevs.dblist): wgUseRCPatrol=true 인 위키 중 본 연구 대상은 frwiki·itwiki; FlaggedRevs 는 dewiki·enwiki·plwiki; kowiki·jawiki 는 둘 다 아님.
- 자료 대조(04_output/h3_tag_coverage.csv, 앵커 2020-08+, 반경 15 안 identity revert 중 태그 누락률): kowiki .024, enwiki .028, jawiki .042, dewiki .046, plwiki .058, frwiki .088, itwiki .120. patrol 위키 2개가 최상위, FlaggedRevs 위키가 중간. 누락 사례의 99% 이상이 되돌린 편집에 undo/rollback/manual-revert 태그를 가짐(탐지는 됨). 익명 되돌림 비중 itwiki .20, frwiki .17.
- 해석(원고용): D2(태그) 정의는 '되돌린 사람의 승인 상태'에 의존하는 정의다. 정의 축의 세 번째 정의가 위키 설정에 따라 2~12% 과소집계됨을 보고하고, H3 둘째 조항(반경이 주원인)은 kowiki 특수성이었음을 기술.

## 2026-10-28 14:45 (그림·시뮬레이션)
- 08_figures.py 신설, 04_output/fig1~fig4(png·pdf)와 fig_data_*.csv: fig1 창별 Δ strict/replace(7위키), fig2 용량-반응(위키 7 + 위키×연도 셀 56, 셀 Spearman ρ = 0.981; 점들이 '상대 Δ = 점유율' 선 바로 아래 = 대체율 S 만큼 낮음), fig3 9셀 OR, fig4 태그 누락률(patrol/FlaggedRevs 색).
- 05 시뮬레이션 실행(n=20,000, reps 20, 격자 p_revert×bot_share×bot_speed×human_delay×follow_prob): R = Δ(∞)/Δ(24h)는 사람 재되돌림 확률(follow) 0.1~0.2, 지연 중앙값 1일~1주에서 .81~.95 → 관측 R(.78~.92)·S(.09~.15)와 부합. follow 0이면 R=1(창 효과 없음), follow 0.5·지연 1주면 R=.51. 04_output/simulation_grid.csv, simulation_window_ratio.csv.
- 해석: 창 효과의 크기는 '봇·도구가 먼저 되돌린 편집을 사람이 다시 되돌리는 확률과 그 지연'으로 결정된다. 관측된 S≈0.1이 작으므로 R이 1에 가깝다.

## 2026-10-28 15:10 (V7·V5 저널 확인)
- JASIST 규정 확인(journal_plan.md에 상세): 7,000단어, 초록 200단어, APA, 미주, single-blind, ScholarOne, 커버레터 필수(정보과학 연결 + 생성형 AI 선언), DAS 필수. Research Exchange 가 아니라 ScholarOne(A 문서 수정 필요).
- single-blind 이므로 Zenodo 파일 제한의 익명성 근거는 사라짐 → 파일을 공개로 전환해도 됨(사용자 결정). 원고에는 DOI 직접 인용.
- JASIST 내 연결 문헌 11편 목록화(OpenAlex, 2008~2026). 서론은 'information quality 측정'과 '봇·인간 협업' 담론에 연결.

## 2026-10-28 15:40 (원고 초안 v0.1)
- 05_manuscript/draft_v0.1.md: 초록 200단어, 본문 약 4,800단어(표 1 포함; 한도 7,000), 엠대시 0, we 0. 서론·배경(JASIST 연결: Stvilia 2008, Arazy 2013, Illari & Floridi 2013, Lewoniewski 2017, Wang & Li 2019, JASIST 2020·2026)·방법·결과(H1~H4, 음성 대조, 태그 게이트)·논의(체크리스트 6항목)·한계·DAS·참고문헌.
- [TBD] 11곳: 확증 위키의 첫 편집 ns0 비율, kowiki 연도별 OR 부호 반전 표 인용, 시뮬레이션 표 인용, 강건성 문단(K=5·전체 계정·historical 봇·undo 도구·5초·창 경계·구 앵커 정의·leave-one-out 미집계), GitHub URL·릴리스 DOI, 미주 2개. [verify] 11곳: 참고문헌 DOI·저자·쪽수.
- 다음: 강건성 집계 스크립트(09_robustness.py) → v0.2; 참고문헌 DOI 대조; 커버레터 초안; docx 변환(JASIST Word 1파일 + Figure1~4 개별).

## 2026-11-08 13:30 (내부 심사 보고서 + 강건성 분석 09/10)
- 05_manuscript/review_internal_v0.1.md: JASIST 편집자·심사자 관점 평가(E1~E6, R1~R12, W1~W7, M1~M5, G1~G3) 와 v0.2 조치 목록.
- 03_pipeline/09_robustness.py (위키별) + 10_robustness_summary.py (7개 위키 집계, 그림 5). VM 에 statsmodels 가 없어 로지스틱은 numpy IRLS + 편집자 클러스터 샌드위치(CR1) 로 직접 구현. 등록 격자와 수치 일치 확인(kowiki replace Δ(24h) 9.830 = 04 산출).
- S1 창 확장: R(12h)·R(48h) 모두 0.98~1.01 → 24h 경계는 민감하지 않음. R(∞) .78~.92 (등록 결과와 동일). S(W) 는 창이 길수록 커짐(24h .09~.15 → ∞ .20~.39).
- S2 정의 변형(strict Δ 24h): 5초 봇 지표 추가 효과 ≤0.05pp(미신고 봇 우려 무시 가능). undo 를 도구로 포함하면 Δ 가 1.5~2.6배(enwiki 21.1→32.3pp, frwiki 7.2→18.9pp) → "도구" 경계 정의가 가장 큰 지렛대. 익명 되돌림자 추가 제외는 +0.3~2.1pp. historical-only 봇 = current∪historical (차이 0).
- S3 코호트: 전체 등록 계정·2021+·보조 앵커(2~5번째 편집) 모두 상대 Δ 순위 불변(enwiki > itwiki > kowiki > dewiki > plwiki > frwiki > jawiki).
- S4 정규근사 p: H1·H2 7/7 p<.001(Holm 후에도). H4 plwiki 1.43(p=.91), frwiki 1.51(p=.33) → 등록 결과(2/3) 와 일치.
- S5 로지스틱(F2r×W∞ 상호작용) 모두 양(+0.07~+0.31, 클러스터 SE ≤0.008) → H1 의 모형 기반 확인.
- S6 kowiki 앵커 정의(첫 편집 vs 첫 ns0 편집): Δ 차이 ≤0.08pp. 02_derived/kowiki_anchors_firstns0.parquet 별도 보관.
- 급증 점검(robust_kowiki_surge.csv, fig5): kowiki 2023-06~2024-12 에 월별 앵커 수 최대 1.9배, 24h 되돌림률 .15→.30~.47, 도구 점유율 .8. 급증 제외 시 R = .865(전체 .775, 급증 구간 .692) → kowiki 의 낮은 R 은 급증 구간이 끌어내린 것. 원고 결과·한계에 기술.
- 태그 가용성(tag_availability_by_wiki.csv): enwiki twinkle 태그는 2020-09 부터, huggle 태그는 2021~2022 에 거의 없음(1,631·2,409건) → enwiki 2019~2020-08 셀의 도구 점유율 과소 측정. 2021+ 코호트에서 enwiki 상대 Δ .57→.65. 원고 한계에 명시.
- 다음: 참고문헌 DOI 대조(#12) → v0.2 원고·커버레터·보충자료·그림(#13).

## 2026-11-08 15:10 (참고문헌 대조, 원고 v0.2, 투고 패키지)
- 참고문헌 Crossref/OpenAlex/DataCite API 로 전수 대조. 오류 2건 교정: asi.22783 은 Illari & Floridi 가 아니라 Mai, J.-E. (2013), 64(4), 675–688; asi.23901 은 Lewoniewski 가 아니라 Jemielniak & Wilamowski (2017), 68(10), 2460–2470. 연도·권호 확정: Wang & Li 71(1) 2020(본문 인용 없어 제거), Rozas & Huckle 72(2) 2021, Gao·Qiu·Zhang·Zhao 2026 advance online, Geiger & Halfaker 2017 1(CSCW) 49, Formisano 13, Art. 1459, Boté-Vericad DataCite 확인.
- 관행 예시 문헌(W1) 추가·원문 확인: Warncke-Wang et al. 2023 (PACM HCI 7 CSCW2 280; 48h 창 "reverted within 48 hours", 봇 언급 없음), Formisano 2026(content-hash, 제외 없음), Halfaker 2013·TeBlunthuis 2018(reverted + tool-reverted 두 변수), Wikimedia Research:Metrics/revert_rate(제외 규정 없음). mwreverts 소프트웨어 인용 추가.
- 05_manuscript/draft_v0.2.md: 본문 약 6,300단어(표·캡션 포함, 한도 7,000), 초록 200단어, 엠대시 0, we 0. 서론을 정보품질 지표의 구성타당도로 열고(E1), 방법론 혁신 문장(E2), 항등식 선행(R1), 기호표(표 2, G1), 180일 창(R2), 등록 시점 증빙(E5), AI 선언 상세(E4), H3 기각 선행·기제는 등록 후 탐색 라벨(R8), 강건성 절(09/10 결과, kowiki 급증, enwiki Twinkle), leave-one-wiki-out ρ .976~.987, 모더레이션 함의(G2), 한계 보강. [TBD] 잔여: GitHub URL·릴리스 DOI(투고 시).
- 그림: 11_figures_submission.py → 05_manuscript/figures/Figure1~4.png(300dpi)+pdf, FigureS1(구 그림 3, 9셀), FigureS2(월별 급증). 그림 3 재구성(위키별 OR 범위 막대). 확인: jawiki·kowiki 는 최소 셀이 F1·24h(F0 와 .002 이내) → 본문·캡션에 명시.
- 보충자료: 12_supplement.py → supplement_v0.2.md/docx/pdf(표 S1~S8, 그림 S1~S2). 편차 로그 #1~#3 기록(혼합모형→위키별 클러스터 SE 로지스틱, 등록 외 강건성 항목, H3 기제 탐색).
- 커버레터 cover_letter_v0.2.md/docx(정보과학 연결, 방법론 혁신, 등록, AI 선언, 데이터·코드, 선호 심사자 자리). build_docx.py(pandoc+python-docx: Times 12pt 1.5, 표 폭 자동, 제목 검정) 로 manuscript_v0.2.docx/pdf(20쪽) 생성.
- 투고 전 사용자 결정 필요: GitHub push·Zenodo 코드 릴리스(DAS 기입), Zenodo 등록 파일 공개 전환, 선호 심사자 명단, 소속·ORCID.
