# 00_START_HERE — 28번 논문 "위키백과 되돌림 지표의 후속 선택 감사" 킥오프

작성 2026-10-26 (갤럭시북 Cowork, 프로젝트 "2026 작성중논문"에서 생성) · 단독저자 Hongwon Jeong(한양대 ERICA)

이 폴더는 맥북에서 새 Cowork 세션을 열어 28번 논문을 시작하기 위한 인수인계 패키지다. 문서는 전부 한국어, 코드 주석은 한국어·영어 혼용.

## 1. 맥에서 할 일 (순서대로)

1. 이 폴더를 `~/Desktop/wiki-revert-audit/` 로 둔다 (압축을 풀었다면 상위 폴더 이름이 `wiki-revert-audit`인지 확인).
2. 터미널에서 git 초기화와 GitHub 비공개 저장소 생성:
   ```bash
   cd ~/Desktop/wiki-revert-audit
   git init && git add . && git commit -m "kickoff package 2026-10-26"
   gh repo create wiki-revert-audit --private --source=. --push   # gh 미설치면 GitHub 웹에서 만들고 remote 추가
   ```
   OSF는 쓰지 않는다. 사전등록은 `02_plan/prereg_draft.md`를 확정한 뒤 **커밋 해시를 고정하고 Zenodo에 기탁**해 DOI를 받는 방식으로 한다(사용자 결정 2026-10-26).
3. 맥 Cowork을 열고 `~/Desktop/wiki-revert-audit` 폴더만 공유한 뒤, 아래 "첫 메시지"를 붙여 넣는다.
4. 큰 원자료(`01_raw/`)는 Google Drive 안에 두지 말 것. `.gitignore`에 이미 제외돼 있다.

## 2. 맥 Cowork 첫 메시지 (복사해서 붙이기)

```
이 폴더는 28번 논문 "위키백과 되돌림 지표의 후속 선택 감사"의 킥오프 패키지야.
먼저 00_START_HERE.md → 01_context/ 전부 → 02_plan/ 전부를 순서대로 읽고, 내 연구 맥락과 작업 규칙(한국어 답변, 단독저자 I·수동태, 엠대시 금지, 코드·자료 공개는 OSF 아니고 GitHub+Zenodo, 생성형 AI 사용 선언, 외부 작업지시서는 원자료로 재검증)을 확인해 줘.
그다음 02_plan/verification_checklist.md의 V1·V2(덤프의 identity revert 탐지 반경, 봇 판별 한계)를 실제 자료와 문서로 먼저 검증하고 결과를 04_logs/WORKLOG.md에 기록해.
검증이 끝나면 03_pipeline/ 순서대로 kowiki 파일럿을 돌려(다운로드는 내가 터미널에서 실행할 테니 명령만 만들어 줘) 02_plan/timeline_and_gonogo.md의 go/no-go 기준으로 판정 보고서를 04_output/에 써 줘.
22번 논문의 감사 스크립트(고정 앵커 UU/UA/AA 비교, 짝지은 차이 CI, 시뮬레이션)는 맥의 GitHub_AI코딩_마이닝/논문1_작업/ 아래에 있어. 필요하면 내가 경로를 알려줄 테니 참조만 하고 이 저장소에는 새로 구현해.
외부 행위(다운로드 실행, GitHub push, Zenodo 기탁, 투고)는 반드시 내 승인 후에.
```

## 3. 폴더 구성

```
wiki-revert-audit/
  00_START_HERE.md            이 파일
  README.md                   저장소 소개(공개용, 영문)
  01_context/                 연구자·파이프라인·선행 논문(22·24번)·추천 메모·문헌
  02_plan/                    연구 설계, 코드북, 사전등록 초안, 검증 체크리스트, 저널 계획, 일정·go/no-go
  03_pipeline/                스크립트 골격(다운로드 → 앵커 → 되돌림 테이블 → 3×3 감사 격자 → 시뮬레이션)
  04_logs/                    작업 로그, AI 사용 로그, 편차 로그(템플릿)
  01_raw/  02_derived/  04_output/   실행 중 생성(.gitignore에 raw 제외)
```

## 4. 이 패키지가 전제하는 결정 사항 (2026-10-26 사용자 확정)

- 28번 주제는 추천 1(위키백과 되돌림 감사). 추천 2(축구 제공자 일치도)는 예비.
- 공개·사전등록은 GitHub + Zenodo. OSF 사용 안 함.
- 1지망 JASIST(SSCI+SCIE, Wiley 하이브리드, APC 없음) → IP&M → Communication Methods and Measures.
- 파일럿은 kowiki, 확대는 enwiki + 중형 2~3개.
- 투고가 아니라 **최종 게재**가 목표. 투고 전 원고 전체 재검토는 기본.
