# 생성형 AI 사용 로그 (투고 시 선언용)

| 날짜 | 도구 | 용도 | 산출물 | 검증 방법 |
|---|---|---|---|---|
| 2026-10-26 | Claude (Anthropic) | 주제 선정 검토, 연구 설계 초안, 파이프라인 스크립트 골격, 문서 초안 | 이 패키지 전체 | 합성 자료 스모크 테스트, 덤프 문서 대조 |
| 2026-10-26 | Claude (Anthropic, 맥 Cowork) | V1·V2 검증(refinery·mwreverts 소스 해석), 06 D3 재계산 로직 재작성, 07 진단 스크립트 작성, README·WORKLOG 작성 | 03_pipeline/01·02·03·04·06·07, README, 04_logs/WORKLOG.md | refinery·mwreverts 원문 직접 대조, 손수 만든 11개 사례 단위검사, 합성 자료 스모크 테스트 |
| 2026-10-27~28 | Claude (Anthropic, 맥 Cowork) | 파이프라인 개정(앵커 정의·압축형 테이블·표본 D3·등록 검정 자동화), 밤샘 배치 드라이버, 등록문(영문) 작성, Zenodo 기탁 양식 입력(Publish는 사용자 확인), 확증 결과 요약·비교표, 그림 1~4, 시뮬레이션, MediaWiki 태그 소스 확인, JASIST 규정 확인, 원고 초안 v0.1 | 03_pipeline/*, 02_plan/preregistration.md, 04_output/*, 05_manuscript/draft_v0.1.md | 등록 코드와 실행 코드 git diff 대조, MediaWiki 소스·매뉴얼 원문 확인, 모든 수치는 산출 CSV에서 전사(원고 머리말에 출처 명시) |
