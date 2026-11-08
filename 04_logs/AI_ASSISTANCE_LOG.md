# 생성형 AI 사용 로그 (투고 시 선언용)

| 날짜 | 도구 | 용도 | 산출물 | 검증 방법 |
|---|---|---|---|---|
| 2026-10-26 | Claude (Anthropic) | 주제 선정 검토, 연구 설계 초안, 파이프라인 스크립트 골격, 문서 초안 | 이 패키지 전체 | 합성 자료 스모크 테스트, 덤프 문서 대조 |
| 2026-10-26 | Claude (Anthropic, 맥 Cowork) | V1·V2 검증(refinery·mwreverts 소스 해석), 06 D3 재계산 로직 재작성, 07 진단 스크립트 작성, README·WORKLOG 작성 | 03_pipeline/01·02·03·04·06·07, README, 04_logs/WORKLOG.md | refinery·mwreverts 원문 직접 대조, 손수 만든 11개 사례 단위검사, 합성 자료 스모크 테스트 |
| 2026-10-27~28 | Claude (Anthropic, 맥 Cowork) | 파이프라인 개정(앵커 정의·압축형 테이블·표본 D3·등록 검정 자동화), 밤샘 배치 드라이버, 등록문(영문) 작성, Zenodo 기탁 양식 입력(Publish는 사용자 확인), 확증 결과 요약·비교표, 그림 1~4, 시뮬레이션, MediaWiki 태그 소스 확인, JASIST 규정 확인, 원고 초안 v0.1 | 03_pipeline/*, 02_plan/preregistration.md, 04_output/*, 05_manuscript/draft_v0.1.md | 등록 코드와 실행 코드 git diff 대조, MediaWiki 소스·매뉴얼 원문 확인, 모든 수치는 산출 CSV에서 전사(원고 머리말에 출처 명시) |
| 2026-11-08 | Claude (Anthropic, 맥 Cowork) | 내부 심사 보고서(편집자·심사자 관점), 강건성 스크립트 09·10 작성·실행(창 확장, 정의·코호트 변형, Holm, 클러스터 SE 로지스틱, 급증 점검, 태그 가용성 표), 그림 5 | 05_manuscript/review_internal_v0.1.md, 03_pipeline/09_robustness.py, 10_robustness_summary.py, 04_output/robust_*.csv, robustness_summary.md, fig5_monthly_surge.* | 09 의 수치를 등록 격자(04) 와 대조해 일치 확인; 로지스틱 구현은 IRLS 수렴·SE 공식 검토 |
| 2026-11-08 | Claude (Anthropic, 맥 Cowork) | 참고문헌 API 대조·교정, 관행 예시 문헌 원문 확인, 원고 v0.2 작성(내부 심사 조치 반영), 그림 3 재구성·투고용 그림 파일, 보충자료 생성 스크립트, 편차 로그, 커버레터 초안, Word/PDF 빌드 스크립트 | 05_manuscript/draft_v0.2.md, manuscript_v0.2.docx, supplement_v0.2.*, cover_letter_v0.2.*, figures/, 03_pipeline/11_*, 12_*, build_docx.py, 04_logs/DEVIATION_LOG.md | 참고문헌은 Crossref·OpenAlex·DataCite 레코드와 대조(2건 저자 오류 발견·교정); 원고 수치는 04_output CSV 에서 전사 후 단어 수·엠대시·we 자동 점검 |
