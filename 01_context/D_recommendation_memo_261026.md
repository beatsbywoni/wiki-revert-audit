# D. 다음 논문(28번) 추천 메모 (2026-10-26, 프로젝트 문서 사본)

> 원본: 프로젝트 "2026 작성중논문" 문서 `claude/next_paper_recommendations_261026.md`. 아래 go/no-go 항목의 "OSF 사전등록"은 사용자 결정(2026-10-26)으로 **GitHub 커밋 고정 + Zenodo 기탁**으로 바뀌었다.

전제: 투고 현황 261022 기준 26편(게재 2: 4번 Sage Open·20번 SoftwareX / 철회 1: 2번 / 심사·접수 중 23편). 27번은 np-behavior 프로젝트 3(배낭문제). SCIE 또는 SSCI, APC 없음 우선, 단독저자, 공개데이터. 09-24 메모의 추천 1("Disclosure Is Not Use")은 24번으로 실현(EMSE 심사 중).

## 포트폴리오 진단
- 저널 풀 혼잡: BRM(26) · AMPPS(16) · PB&R(17) · PLOS ONE(11) · ToG(9) · EC(25) · EMSE(24) · JSEP(22) · TOCE(8·21) · PSE(13) · IJPAS(10). 27번(배낭문제)도 인지·심리방법론 풀로 들어갈 예정이라 그 풀은 더 넣지 않는 것이 안전.
- 데스크 통과율이 낮았던 풀: 교육공학(C&E·BJET·EAIT·JCAL), CALL(ReCALL·LLT·CALL), Journal of Sports Sciences(10·16번 데스크 리젹 2회), IJED(통과 이력 없음).
- 아직 한 번도 안 쓴 풀: 정보학(JASIST·IP&M·JOI·Scientometrics), 축구 과학지 중 Science and Medicine in Football, 생태·보전(Biological Conservation).

## 추천 1 (1순위, 채택): 위키백과 되돌림 지표의 후속 선택 감사
- 가제: "Which reverts count? Successor filtering and observation windows in Wikipedia revert-based metrics"
- 설계: 22번 고정 앵커 감사 틀 이식. 같은 편집자·같은 첫 편집(앵커)을 고정하고 되돌림으로 인정하는 후속 집합만 바꿈(전체 / 봇 제외 / 봇+도구(Huggle·Twinkle·rollback 태그) 제외) × 관찰 창(24h / 7d / 최종). identity revert(mediawiki_history의 revision_is_identity_reverted) vs 되돌림 태그(mw-reverted; 되돌린 쪽은 mw-undo·mw-rollback·mw-manual-revert) 두 정의 교차.
- 결과변수: 신규 편집자 되돌림 비율(Halfaker 2013), 편집자 수준 success rate, 되돌림과 잔존(retention)의 연관 크기.
- 가설: 창이 있는 지표만 민감(Geiger & Halfaker 2013 봇 중단 사례: 속도는 느려졌지만 최종 비율은 동일).
- 데이터: mediawiki_history 월간 TSV 덤프(kowiki 파일럿 → enwiki + 중규모 2~3개).
- 2026-10 선점 점검: Boté-Vericad(Univ. Barcelona), Zenodo 2026-10-17 "Constructing newcomer cohorts from Wikimedia logs"(계정 생성 유형·삭제 기여·관찰 창·행동 임계값 4개 결정, pl·cs·hu·da 위키, Quarry; 첫 편집 되돌림 → 1회 편집 후 이탈 odds 1.20). 코호트 구성 감사이며 되돌림 정의(후속 선택) 감사는 아님 → 인접 선행으로 인용·차별화, 그러나 공간이 열리고 있어 착수를 서둘러야 함. HSSC 2026(Formisano 외, 2024 미국 선거 되돌림)은 content-hash 정의를 한계로 명시 → 수요 근거. Wikimedia Research:Metrics/revert rate 페이지도 복수 탐지 방법 존재를 인정.
- 저널 체인: JASIST(SSCI+SCIE, Wiley 하이브리드, APC 없음) → IP&M(SCIE+SSCI) → Communication Methods and Measures(SSCI).
- go/no-go(약 3일): kowiki 최신 월 덤프로 3×3 격자 신규 편집자 되돌림 비율 산출. 격자 간 차이가 5pp 이상이거나 순위가 바뀌면 사전등록(GitHub 커밋 고정 + Zenodo) 후 확대.

## 추천 2 (2순위, 예비): 축구 이벤트 데이터 제공자 간 일치도 감사
- 가제: "Same match, different record: provider concordance of public football event data and its downstream consequences"
- 데이터: StatsBomb open data와 Wyscout 공개 데이터셋(Pappalardo 외 2019, figshare 4415000)의 중복 경기. 예상 중복: 2018 월드컵 64경기 + 2017/18 라리가 바르셀로나 38경기(착수 시 매치 ID 대조로 확정).
- 결과변수: 팀-경기 이벤트 수(슛·패스·키패스), 슛 좌표·xG 입력 특성, 점유 시퀀스 길이; 하류 검정으로 10번의 score-state 설계 등 공개된 발견이 제공자에 따라 바뀌는지.
- 선행: Liu 외 2013(Opta 운영자 간 신뢰도), PLOS ONE 2024(이벤트 탐지 신뢰도)은 운영자·주석 수준. 공개 데이터 제공자 간 같은 경기 일치도 감사는 2026-10-26 검색에서 미발견(착수 전 재확인).
- 저널 체인: Science and Medicine in Football(SCIE, T&F, APC 없음) → PLOS ONE → Journal of Sports Analytics. Journal of Sports Sciences는 10·16번 데스크 리젹 이력으로 제외. IJPAS는 10번 R1 심사 중이라 제외.

## 보류
- AI 디지털교과서 국회 회의록(272건 정제 v5 보유): SSCI 경로만 있음(LMT·JEP·APER), 한국 단일 사례의 스코프 리젹 위험(23번 체인 5회 리젹 참고), KCI 담론 분석 1편(ART003269051, 회의록 사용 여부 미확인)·국회입법조사처 2024 보고서 존재.
- 2030 리더보드 트랙: 1지망 풀(BRM·PB&R·PLOS ONE)이 26·17·11번으로 점유. 결정 후 착수.
- 2029 P2(철회 탐지): Fletcher & Stevenson 2025(RIPR) 등 선행 다수, RIPR은 APC. P4(statcheck): Nuijten 2016이 결과당 비율(9.7%/gross 1.6%)을 이미 보고하고 타당성 연구가 높은 정확도를 보고해 기여가 얇을 위험.
- 2028 커뮤니티 트랙: 총량 감소 포화, SE 덤프 라이선스 논쟁.
- 10번에서 분리한 esports 역할 층화 원고: ToG·EC 풀 점유로 대기.

## 출처
- Boté-Vericad 2026 Zenodo: https://zenodo.org/records/23435553
- Formisano 외 2026 HSSC: https://www.nature.com/articles/s41599-026-06810-2
- Wikimedia revert rate 정의: https://meta.wikimedia.org/wiki/Research:Metrics/revert_rate
- mediawiki_history 덤프 문서: https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Edits/Mediawiki_history_dumps
- Wyscout 공개 데이터셋: https://figshare.com/collections/Soccer_match_event_dataset/4415000/2
- PLOS ONE 2024 이벤트 탐지 신뢰도: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0298107
- Fletcher & Stevenson 2025 RIPR: https://researchintegrityjournal.biomedcentral.com/articles/10.1186/s41073-025-00168-w
