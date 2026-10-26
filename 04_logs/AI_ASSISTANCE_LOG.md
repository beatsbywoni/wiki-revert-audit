# 생성형 AI 사용 로그 (투고 시 선언용)

| 날짜 | 도구 | 용도 | 산출물 | 검증 방법 |
|---|---|---|---|---|
| 2026-10-26 | Claude (Anthropic) | 주제 선정 검토, 연구 설계 초안, 파이프라인 스크립트 골격, 문서 초안 | 이 패키지 전체 | 합성 자료 스모크 테스트, 덤프 문서 대조 |
| 2026-10-26 | Claude (Anthropic, 맥 Cowork) | V1·V2 검증(refinery·mwreverts 소스 해석), 06 D3 재계산 로직 재작성, 07 진단 스크립트 작성, README·WORKLOG 작성 | 03_pipeline/01·02·03·04·06·07, README, 04_logs/WORKLOG.md | refinery·mwreverts 원문 직접 대조, 손수 만든 11개 사례 단위검사, 합성 자료 스모크 테스트 |
