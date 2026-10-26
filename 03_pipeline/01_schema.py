"""mediawiki_history 덤프 TSV 스키마 (78열, 헤더 없음).

출처(확정): analytics-refinery-source MediawikiEvent.scala `toTSVLine` 의 필드 순서(2026-10-26 master 확인) + 실제 2026-09 kowiki
파일에서 78열 관찰(04_logs/WORKLOG.md V4). wikitech 문서의 70열 표는 구버전이라 쓰지 않는다. 문서 대비 추가된 열:
event_log_id, event_user_central_id, event_user_is_temporary/permanent/cross_wiki, user_central_id, user_is_temporary/permanent.
열 순서가 바뀌면 전부 틀어지므로 새 덤프 버전마다 열 수(78)를 다시 확인할 것.
배열형 열은 쉼표 구분 문자열, 빈 문자열은 null.

V1·V2 검증(2026-10-26, 04_logs/WORKLOG.md)에 따른 변경:
- revision_parent_id 추가: refinery 의 identity revert 계산은 "parent 가 직전 같은-sha1 revision 인 no-op revision" 을
  되돌림 목록에서 제거한다. D3 재계산(06)이 D1 과 같아지려면 parent id 가 필요.
- event_user_is_bot_by_historical 추가: 덤프의 is_bot_by 는 '현재' 사용자명·그룹 기준, _historical 은 사건 시점 기준.
  되돌린 쪽의 봇 판별은 둘의 합집합을 기본으로 쓰고 historical 단독을 민감도로 둔다.
- event_user_text 추가: V2 수동 점검(비봇인데 수 초 안에 되돌린 계정 상위 목록)용. 02_derived 에만 남기고 공개하지 않는다.
"""

COLUMNS = [
    "wiki_db", "event_log_id", "event_entity", "event_type", "event_timestamp", "event_comment",
    "event_user_id", "event_user_central_id", "event_user_text_historical", "event_user_text",
    "event_user_blocks_historical", "event_user_blocks",
    "event_user_groups_historical", "event_user_groups",
    "event_user_is_bot_by_historical", "event_user_is_bot_by",
    "event_user_is_created_by_self", "event_user_is_created_by_system",
    "event_user_is_created_by_peer", "event_user_is_anonymous",
    "event_user_is_temporary", "event_user_is_permanent", "event_user_is_cross_wiki",
    "event_user_registration_timestamp", "event_user_creation_timestamp",
    "event_user_first_edit_timestamp", "event_user_revision_count",
    "event_user_seconds_since_previous_revision",
    "page_id", "page_title_historical", "page_title",
    "page_namespace_historical", "page_namespace_is_content_historical",
    "page_namespace", "page_namespace_is_content", "page_is_redirect",
    "page_is_deleted", "page_creation_timestamp", "page_first_edit_timestamp",
    "page_revision_count", "page_seconds_since_previous_revision",
    "user_id", "user_central_id", "user_text_historical", "user_text",
    "user_blocks_historical", "user_blocks", "user_groups_historical",
    "user_groups", "user_is_bot_by_historical", "user_is_bot_by",
    "user_is_created_by_self", "user_is_created_by_system",
    "user_is_created_by_peer", "user_is_anonymous",
    "user_is_temporary", "user_is_permanent",
    "user_registration_timestamp", "user_creation_timestamp",
    "user_first_edit_timestamp",
    "revision_id", "revision_parent_id", "revision_minor_edit",
    "revision_deleted_parts", "revision_deleted_parts_are_suppressed",
    "revision_text_bytes", "revision_text_bytes_diff", "revision_text_sha1",
    "revision_content_model", "revision_content_format",
    "revision_is_deleted_by_page_deletion",
    "revision_deleted_by_page_deletion_timestamp",
    "revision_is_identity_reverted",
    "revision_first_identity_reverting_revision_id",
    "revision_seconds_to_identity_revert", "revision_is_identity_revert",
    "revision_is_from_before_page_creation", "revision_tags",
]
assert len(COLUMNS) == 78, len(COLUMNS)

# 1차 패스(앵커·편집자 활동)에서 읽는 열만 고름 → 메모리·속도 절약
USECOLS_REVISIONS = [
    "wiki_db", "event_entity", "event_type", "event_timestamp",
    "event_user_id", "event_user_text",
    "event_user_is_bot_by_historical", "event_user_is_bot_by",
    "event_user_is_created_by_self",
    "event_user_is_anonymous", "event_user_is_temporary", "event_user_creation_timestamp",
    "event_user_first_edit_timestamp", "event_user_revision_count",
    "page_id", "page_namespace_historical",
    "revision_id", "revision_parent_id", "revision_text_sha1",
    "revision_is_identity_reverted", "revision_first_identity_reverting_revision_id",
    "revision_seconds_to_identity_revert", "revision_is_identity_revert",
    "revision_tags",
]

# 창(초). inf 는 None 으로 표기
WINDOWS = {"W24h": 86400, "W7d": 604800, "Winf": None}

# 도구 태그: 기본 집합(사전등록 대상). mw-undo 는 수동 되돌림이라 기본 제외, 민감도에서만 포함.
TOOL_TAGS_DEFAULT = {"mw-rollback", "huggle", "twinkle"}
TOOL_TAGS_SENSITIVITY = TOOL_TAGS_DEFAULT | {"mw-undo"}
REVERTED_TAG = "mw-reverted"

# V3 진단 대상 태그(가용 시점·빈도 산출)
TAGS_OF_INTEREST = ["mw-reverted", "mw-undo", "mw-rollback", "mw-manual-revert", "huggle", "twinkle", "mw-replace"]

# 앵커·활동 창(일): 편집자의 첫 편집 뒤 이 기간 안의 편집만 edits 테이블에 남긴다(잔존 +2~60일, 활동 90일 계산에 충분)
NEWCOMER_WINDOW_DAYS = 91

# mwreverts 기본 탐지 반경(문헌 관행). 덤프(refinery)는 반경 없음 — V1 검증 결과.
MWREVERTS_RADIUS = 15
