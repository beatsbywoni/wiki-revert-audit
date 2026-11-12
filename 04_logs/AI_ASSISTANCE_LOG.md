# 생성형 AI 사용 로그 (투고 시 선언용)

| 날짜 | 도구 | 용도 | 산출물 | 검증 방법 |
|---|---|---|---|---|
| 2026-10-26 | Claude (Anthropic) | 주제 선정 검토, 연구 설계 초안, 파이프라인 스크립트 골격, 문서 초안 | 이 패키지 전체 | 합성 자료 스모크 테스트, 덤프 문서 대조 |
| 2026-10-26 | Claude (Anthropic, 맥 Cowork) | V1·V2 검증(refinery·mwreverts 소스 해석), 06 D3 재계산 로직 재작성, 07 진단 스크립트 작성, README·WORKLOG 작성 | 03_pipeline/01·02·03·04·06·07, README, 04_logs/WORKLOG.md | refinery·mwreverts 원문 직접 대조, 손수 만든 11개 사례 단위검사, 합성 자료 스모크 테스트 |
| 2026-10-27~28 | Claude (Anthropic, 맥 Cowork) | 파이프라인 개정(앵커 정의·압축형 테이블·표본 D3·등록 검정 자동화), 밤샘 배치 드라이버, 등록문(영문) 작성, Zenodo 기탁 양식 입력(Publish는 사용자 확인), 확증 결과 요약·비교표, 그림 1~4, 시뮬레이션, MediaWiki 태그 소스 확인, JASIST 규정 확인, 원고 초안 v0.1 | 03_pipeline/*, 02_plan/preregistration.md, 04_output/*, 05_manuscript/draft_v0.1.md | 등록 코드와 실행 코드 git diff 대조, MediaWiki 소스·매뉴얼 원문 확인, 모든 수치는 산출 CSV에서 전사(원고 머리말에 출처 명시) |
| 2026-11-08 | Claude (Anthropic, 맥 Cowork) | 내부 심사 보고서(편집자·심사자 관점), 강건성 스크립트 09·10 작성·실행(창 확장, 정의·코호트 변형, Holm, 클러스터 SE 로지스틱, 급증 점검, 태그 가용성 표), 그림 5 | 05_manuscript/review_internal_v0.1.md, 03_pipeline/09_robustness.py, 10_robustness_summary.py, 04_output/robust_*.csv, robustness_summary.md, fig5_monthly_surge.* | 09 의 수치를 등록 격자(04) 와 대조해 일치 확인; 로지스틱 구현은 IRLS 수렴·SE 공식 검토 |
| 2026-11-08 | Claude (Anthropic, 맥 Cowork) | 참고문헌 API 대조·교정, 관행 예시 문헌 원문 확인, 원고 v0.2 작성(내부 심사 조치 반영), 그림 3 재구성·투고용 그림 파일, 보충자료 생성 스크립트, 편차 로그, 커버레터 초안, Word/PDF 빌드 스크립트 | 05_manuscript/draft_v0.2.md, manuscript_v0.2.docx, supplement_v0.2.*, cover_letter_v0.2.*, figures/, 03_pipeline/11_*, 12_*, build_docx.py, 04_logs/DEVIATION_LOG.md | 참고문헌은 Crossref·OpenAlex·DataCite 레코드와 대조(2건 저자 오류 발견·교정); 원고 수치는 04_output CSV 에서 전사 후 단어 수·엠대시·we 자동 점검 |
| 2026-11-10 | Claude (Anthropic, 클라우드 세션 + 맥 연결) | 심사 시뮬레이션(에디터·리뷰어 에이전트), 재분석 스크립트 14·15 작성, 그림 16·보충 17, 선행연구 관행 리뷰의 1차 코딩과 재검증(에이전트), 문헌·저널·기술 사실 검증, 원고 v0.3·커버레터·편차 로그 초안 | 03_pipeline/14~17, 04_output/rev_*.csv, practice_review.csv, 05_manuscript/draft_v0.3.md 등 | 재분석 수치는 등록 격자와 대조(kowiki Δ·R 일치); 리뷰 코딩은 독립 재검증 후 정정 12건 반영, 축어 인용 미사용; 원고 수치는 CSV 에서 전사 후 범위 재확인 |

## 2026-11-10 to 2026-11-12 (Claude Fable 5.2, model id claude-fable-5-2)
- Code drafted with AI assistance: 14_successor_decomposition.py (v2), 15_revision_tables.py (v2), 16_figures_revision.py, 17_supplement_v04.py, 18_stream_extract.py, 19_tag_checks.py. All run by the author on unmodified dumps; outputs in 04_output/.
- Literature review: first-pass coding of 41 studies by the model from full texts; all codes checked against quoted sentences (7 of the first 34 studies corrected); blind second pass by a separate model instance on 13 studies (72 of 78 judgments agree). Search of LIS and neighbouring journals via OpenAlex by a model agent (record in 04_output/practice_review_LIS_search.md).
- Prose: manuscript v0.4, supplement text, cover letter drafted and edited with AI assistance.
- Internal pre-submission checks: three rounds in which model agents acted as an editor and three reviewers of the draft; their reports led to corrections recorded in WORKLOG.md and DEVIATION_LOG.md. No data were generated, altered or imputed by the model.

## 2026-11-12 (review of practice, author check)
- ChatGPT (OpenAI; version reported by the author as 6.1 Astra) assisted the author's check of the review coding for the four studies added on 12 November 2026 (Morris-O'Connor et al. 2023; Ariel 2026; Arazy et al. 2019; Gao et al. 2026). Its points were compared with the source passages before any code was changed.
- Claude (claude-fable-5-2): full-text reading of candidate studies through institutional access, re-verification of the author's check against sources, manuscript v0.7 to v0.9, internal pre-submission checks (rounds 4 and 5).

## 2026-11-12 (round 6, manuscript v0.10)
- Claude (claude-fable-5-2): internal pre-submission check (round 6); script `23_tag_radius_crosstab.py`; derivation of the "recoverable" entries of the conservative tally from the notes of the author's check (to be confirmed by the author); manuscript, supplement and cover letter v0.10. Retrieval and term-count screening of candidate texts in the review of practice were run through Claude's web tools and a scripted browser session; this is now stated in the manuscript.

## 2026-11-12 (round 7, manuscript v0.11)
- Claude (claude-fable-5-2): internal pre-submission check (round 7); reading of the JASIST author guidelines and of recent JASIST abstracts through the author's browser session; script `24_tag_cluster.py`; restructuring and shortening of the manuscript (v0.11), supplement and cover letter.

## 2026-11-12 (round 8, manuscript v0.12)
- Claude (claude-fable-5-2): internal pre-submission check (round 8); verification of reviewer points against the MediaWiki manual, core source and Wikimedia configuration; scripts `24_tag_cluster.py` (per-edition groups) and `25_retention_existing_pages.py`; manuscript, supplement and cover letter v0.12.
