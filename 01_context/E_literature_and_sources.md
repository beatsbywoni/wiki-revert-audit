# E. 선행 문헌과 자료 출처 (2026-10-26 기준, 서지 상태 표기)

표기: **[확인]** = 2026-10-26 웹에서 존재·내용 확인 / **[기억]** = 널리 알려진 문헌이나 이번에 서지를 다시 확인하지 않음(투고 전 DOI 대조 필수) / **[미확인]** = 존재 자체를 확인해야 함.

## 1. 되돌림 측정의 정의와 도구
- Wikimedia Research:Metrics/revert rate. identity revert(체크섬 일치)를 가장 흔한 탐지법으로 소개하고 다른 정의가 있다고 명시. 노이즈·시차(lag) 주의 기재. **[확인]** https://meta.wikimedia.org/wiki/Research:Metrics/revert_rate
- Wikimedia Research:Revert (되돌림 정의 모음 페이지; identity revert, 되돌림 태그 등). **[기억]** 맥 Cowork에서 열어 확인.
- `mwreverts`(Halfaker, Python). identity revert 탐지 라이브러리. 기본 탐지 반경(radius)이 15 revision인 것으로 기억함 → **V1 검증 항목**. **[기억]**
- mediawiki_history 덤프 문서(필드·분할·갱신 주기). 70개 열, 월 1회, 소형 위키는 all-time 단일 파일, 중형은 연도별, enwiki·wikidata·commons는 월별. 최근 2개 버전만 보관. **[확인]** https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Edits/Mediawiki_history_dumps
- Kittur, Suh, Pendleton & Chi (2007). He says, she says: Conflict and coordination in Wikipedia. CHI. (되돌림을 갈등 지표로 사용한 고전) **[기억]**
- Flöck & Acosta (2014). WikiWho: Precise and efficient attribution of authorship of revisioned content. WWW. (텍스트 생존 기반 대안 측정) **[기억]**

## 2. 되돌림과 신규 편집자(지표의 사용처)
- Halfaker, Geiger, Morgan & Riedl (2013). The rise and decline of an open collaboration system: How Wikipedia's reaction to popularity is causing its decline. American Behavioral Scientist, 57(5), 664–688. (신규 편집자 되돌림 비율 상승 → 잔존 하락; 28번 결과변수의 원천) **[기억]**
- Halfaker, Kittur & Riedl (2011). Don't bite the newbies: How reverts affect the quantity and quality of Wikipedia work. WikiSym. **[기억]**
- Geiger & Halfaker (2013). When the levee breaks: Without bots, what happens to Wikipedia's quality control processes? WikiSym. (ClueBot NG 중단 기간: 되돌림 속도는 느려졌지만 최종 비율은 유지 → **H1의 직접 근거**) **[기억]** 2013-08 Wikimedia Research Newsletter 요약 https://diff.wikimedia.org/2013/08/31/research-newsletter-august-2013/ 에서 간접 확인(09-24 메모).
- Geiger & Halfaker (2017). Operationalizing conflict and cooperation between automated software agents in Wikipedia: A replication and expansion of "Even Good Bots Fight". PACM HCI (CSCW). (봇 간 되돌림의 **조작화 감사**; 정의 변경이 결론을 바꾼 선례 → 서론의 핵심 포지셔닝 자료) **[기억]**
- Tsvetkova, García-Gavilanes, Floridi & Yasseri (2017). Even good bots fight. PLOS ONE. **[기억]**
- TeBlunthuis, Shaw & Hill (2018). Revisiting "The rise and decline" in a population of peer production projects. CHI. (지표 재현) **[기억]**

## 3. 2026년 인접 연구(선점·수요 근거)
- Boté-Vericad, J.-J. (2026-10-17). Constructing newcomer cohorts from Wikimedia logs: account creation type, deleted contributions, observation windows, and the behavioural threshold (version 2). Zenodo. 코호트 구성 4개 결정, pl·cs·hu·da 위키, Quarry 36회 실행, 첫 편집 되돌림 → 1회 편집 후 이탈 odds 1.20, 삭제 1.15. 저널 게재 아님. **[확인]** https://zenodo.org/records/23435553 (v1: 10.5281/zenodo.23140935, 데이터 23434679, 소프트웨어 23435588)
- Formisano, G., Hine, E., Juneja, P., Laitila, J., Novelli, C., Chiu, E., Dejanikus, E., Levin, M., Schroder, T., West, A., & Floridi, L. (2026). Editorial governance under pressure: Wikipedia's revert dynamics during the 2024 US election. Humanities and Social Sciences Communications, 13, 1459. content-hash 정의만 사용, 정의 민감도 미검정, 한계로 명시. **[확인]** https://doi.org/10.1057/s41599-026-06810-2
- Wikimedia Growth 팀 실험 보고(Add-a-link enwiki A/B 등)는 "되돌림(48시간 이내)" 같은 창이 있는 지표를 쓴다 → 정책 관련성. **[기억]** 맥에서 https://analytics.wikimedia.org/published/reports/growth/ 확인.

## 4. 측정 감사 방법론(본인 계보)
- 22번(JSEP 심사 중) Auditing successor selection in software repository mining. (Author, under review)
- 24번(EMSE) Disclosure Is Not Use. (Author, under review)
- 16번(AMPPS) Event-based split halves... (Author, under review) 등록 실패 자진 보고 서술.

## 5. 저널 정보(투고 전 재확인)
- JASIST: Wiley, SSCI+SCIE, 하이브리드(구독형 무료). Research Exchange 제출. 생성형 AI 공개 정책 있음(2028 트랙 검증 메모). 최근호에 Wikipedia·측정 논문이 있는지 **맥에서 목차 확인 필요** [미확인].
- Information Processing & Management: Elsevier, SCIE+SSCI, 하이브리드. 구독 경로 무료.
- Communication Methods and Measures: T&F, SSCI Q1(5.8, 09-24 메모). T&F 계정은 nightsea05@naver.com.

## 6. 자료 URL
- mediawiki_history 덤프 루트: https://dumps.wikimedia.org/other/mediawiki_history/ (디렉터리 `YYYY-MM/<wiki>/`)
- 보조(검증용): stub-meta-history XML 덤프(sha1 포함) https://dumps.wikimedia.org/kowiki/ ; Quarry https://quarry.wmcloud.org (라이브 복제 DB SQL, 소규모 교차검증)
