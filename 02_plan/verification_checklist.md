# 착수 검증 체크리스트 (파일럿 분석 전에 끝낼 것)

각 항목은 결과를 `04_logs/WORKLOG.md`에 날짜·출처 URL·확인 방법과 함께 기록한다. 외부 작업지시서를 받으면 그 주장도 같은 방식으로 원자료에서 재검증한다.

## V1. 덤프의 identity revert 탐지 반경
- 질문: `revision_is_identity_reverted`는 시간·revision 수 제한 없이 "언젠가 같은 sha1로 돌아갔는가"를 보는가, 아니면 mwreverts처럼 반경(기본 15 revision)이 있는가?
- 확인 방법: (a) wikitech `Analytics/Data_Lake/Edits/MediaWiki_history` 와 DataHub 필드 설명, (b) analytics-refinery 소스(`refinery-source` 의 mediawikihistory revert 관련 Scala 코드) 검색, (c) kowiki에서 sha1 직접 재계산(D3)과 D1 비교: D1=0인데 D3=1인 사례의 분포(되돌림까지 revision 수·시간).
- 결과에 따른 분기: 반경이 있으면 W∞는 D3로 계산하고 D1은 "덤프 정의"로 별도 보고. 반경이 없으면 D1을 주 정의로 쓰고 D3는 검증용.

## V2. 봇 판별의 한계
- `event_user_is_bot_by`는 'name'(사용자명 패턴)·'group'(bot 그룹) 기준. 미등록 봇, 과거 봇 플래그 해제, 반자동 도구를 쓰는 사람은 잡히지 않는다.
- 확인: kowiki에서 되돌린 쪽의 `sec_to_revert` 분포를 봇/비봇으로 나눠 그리기. 비봇인데 수 초 안에 되돌린 계정이 많으면 이름 목록을 뽑아 수동 점검(상위 50개).
- 보완: 되돌림 속도 임계(예: 5초 이내)를 보조 봇 지표로 민감도에 포함.

## V3. 태그의 가용 기간과 위키별 차이
- `mw-undo`, `mw-rollback`, `mw-reverted`, `mw-manual-revert`가 각 위키에서 처음 나타나는 월을 산출. Huggle·Twinkle 태그 존재 여부(kowiki는 없을 수 있음).
- 분기: 태그 기반 F2·D2는 가용 시점 이후만 주 분석.

## V4. 덤프 버전·분할·용량
- `https://dumps.wikimedia.org/other/mediawiki_history/` 최신 버전 디렉터리 확인(최근 2개만 보관). kowiki 파일 크기, enwiki 월별 파일 수와 총량, 중형 위키 후보의 분할 방식.
- 다운로드는 사용자가 터미널에서 실행. 체크섬 파일이 있으면 대조.

## V5. 선행연구 재검색(착수일 기준)
- 검색어: "Wikipedia revert definition sensitivity", "identity revert bots window", "newcomer revert rate measurement", "successor selection audit". Google Scholar·OpenAlex·arXiv·Zenodo(Boté-Vericad 후속 여부).
- Geiger & Halfaker 2017(CSCW) 본문을 읽고 조작화 변경이 결론을 바꾼 지점을 정확히 인용.
- JASIST 최근 3년 Wikipedia·측정 논문 목록(제목·초록) 수집.

## V6. 22번 스크립트 위치 확인
- 맥 `GitHub_AI코딩_마이닝/논문1_작업/` 아래에서 고정 앵커 비교·부트스트랩·시뮬레이션 스크립트 파일명을 찾아 WORKLOG에 기록. 이 저장소에는 참조만 하고 새로 구현.

## V7. 저널 체크
- JASIST 투고 규정(길이, 구조화 초록 여부, 이중익명 여부, 데이터 정책, 생성형 AI 정책), Wiley 계정 이메일 확인.
