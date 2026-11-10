# JSON 데이터 확인용
# - 저장 파일 내용을 읽어 검증
import json
# pytest 기능 사용
# - parametrize를 이용한 반복 테스트
import pytest

"""HTTP 입력·응답과 저장 결과를 실제 임시 파일로 확인합니다."""
"""API의 CRUD 기능, 입력 검증, 예외 처리, OpenAPI 문서 생성 및 데이터 보존 여부를 실제 HTTP 요청을 통해 검증하는 통합 테스트"""
# Health Check API 검증
# - 서버 상태 확인
# - 정상 응답(JSON) 반환 여부 검사
def test_health(isolated_client):
    # fixture에서 client 획득
    client, _ = isolated_client
    # 상태 확인 요청
    r = client.get("/health")
    # HTTP 200 확인
    assert r.status_code == 200
    # 응답 내용 확인
    assert r.json() == {"status": "ok"}

# 목록 조회 및 카테고리 필터 검증
# - 전체 조회
# - 조건 조회
# - 빈 결과 조회
# - 조회 시 파일 변경 없음 확인
def test_list_and_filter(isolated_client):
    # 테스트 클라이언트 및 임시 저장소 획득
    client, path = isolated_client
    # 조회 전 파일 상태 저장
    before = path.read_bytes()
    # 전체 목록 조회
    r = client.get("/api/knowledge")
    # 조회 성공 확인
    assert r.status_code == 200
    # 기본 데이터 ID 확인
    assert [entry["id"] for entry in r.json()] == [1, 2, 3]
    # 내부 관리 정보 노출 금지 확인
    assert "next_id" not in r.text
    # category=api 조건 조회
    filtered = client.get("/api/knowledge", params={"category": "api"})
    # api 카테고리 결과 확인
    assert [entry["id"] for entry in filtered.json()] == [2, 3]
    # 존재하지 않는 카테고리 조회
    empty = client.get("/api/knowledge", params={"category": "unknown"})
    # BEGIN H07-04
    # TODO H07-04: 없는 category를 조회한 목록이 200과 빈 배열인지 검사하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    # raise NotImplementedError("H07-04를 먼저 완성하세요.")

    # 조회 자체는 정상 처리
    # - 조건에 맞는 데이터만 없는 상태
    assert empty.status_code == 200
    # 결과 없음 확인
    # - 빈 배열 반환
    assert empty.json() == []
    # END H07-04
    # 조회는 저장 데이터 변경 금지
    assert path.read_bytes() == before

# 단건 조회 및 예외 처리 검증
# - 정상 조회
# - 없는 ID
# - 잘못된 ID 타입
def test_detail_and_errors(isolated_client):
    # 테스트 클라이언트 및 임시 저장소 획득
    client, path = isolated_client
    # 조회 전 파일 상태 저장
    before = path.read_bytes()
    # ID 2 조회
    r = client.get("/api/knowledge/2")
    # 조회 성공
    assert r.status_code == 200
    # 제목 확인
    assert r.json()["title"] == "서버 실행"
    # 없는 ID 조회
    assert client.get("/api/knowledge/9999").status_code == 404
    # 숫자가 아닌 ID 조회
    assert client.get("/api/knowledge/foo").status_code == 422
    # 조회는 파일 변경 금지
    assert path.read_bytes() == before

# 생성(Create) 기능 검증
# - 데이터 생성
# - 재조회
# - 파일 저장 확인
# - next_id 증가 확인
def test_create_and_read_back(isolated_client):
    # 테스트 클라이언트 및 임시 저장소 획득
    client, path = isolated_client
    # 생성 요청 데이터
    payload = {"title": "새 안내", "content": "로컬 폴더를 확인합니다.", "category": "guide"}
    # 생성 요청
    r = client.post("/api/knowledge", json=payload)
    # 생성 성공
    assert r.status_code == 201
    # 생성 결과 저장
    entry = r.json()
    # 생성 데이터 확인
    assert entry == dict(payload, id=4)
    # 재조회 확인
    assert client.get(f"/api/knowledge/{entry['id']}").json() == entry
    # 실제 저장 파일 확인
    saved = json.loads(path.read_text(encoding="utf-8"))
    # 데이터 개수 증가
    assert len(saved["entries"]) == 4
    # next_id 증가 확인
    assert saved["next_id"] == 5
    # 마지막 데이터 확인
    assert saved["entries"][-1] == entry

# 잘못된 입력 데이터 목록
# - 필수값 누락
# - 빈 문자열
# - 길이 제한 초과
@pytest.mark.parametrize("payload", [
    {"content": "본문", "category": "guide"},
    {"title": "제목", "category": "guide"},
    {"title": "제목", "content": "본문"},
    {"title": "", "content": "본문", "category": "guide"},
    {"title": "제목", "content": "", "category": "guide"},
    {"title": "제목", "content": "본문", "category": ""},
    {"title": "가" * 81, "content": "본문", "category": "guide"},
    {"title": "제목", "content": "가" * 2001, "category": "guide"},
    {"title": "제목", "content": "본문", "category": "가" * 31},
])

# 잘못된 입력 처리 검증
# - HTTP 422
# - 파일 변경 없음
def test_invalid_post_preserves_file(isolated_client, payload):
    # 테스트 클라이언트 및 임시 저장소 획득
    client, path = isolated_client
    # 요청 전 상태 저장
    before = path.read_bytes()
    # 생성 요청
    r = client.post("/api/knowledge", json=payload)
    # BEGIN H07-03
    # TODO H07-03: 잘못된 입력이 422이며 저장 파일을 바꾸지 않는지 검사하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    # raise NotImplementedError("H07-03를 먼저 완성하세요.")

    # 입력 검증 실패 확인
    # - Pydantic Validation Error
    assert r.status_code == 422
    # 저장 파일 변경 금지 확인
    assert path.read_bytes() == before
    # END H07-03

# JSON 문법 오류 검증
# - 잘못된 JSON 요청
# - HTTP 422
# - 파일 변경 없음
def test_json_syntax_error(isolated_client):
    # 테스트 클라이언트 및 임시 저장소 획득
    client, path = isolated_client
    before = path.read_bytes()
    r = client.post("/api/knowledge", content='{"title":', headers={"Content-Type": "application/json"})
    # JSON 파싱 실패
    assert r.status_code == 422
    # 파일 변경 없음
    assert path.read_bytes() == before

# 수정(Update) 기능 검증
# - 동일 ID 유지 확인
# - 데이터 개수 유지 확인
# - 다른 데이터 영향 없음 확인
# - 저장 파일 반영 확인
def test_update_preserves_id_count_and_other_entries(isolated_client):
    # 테스트 클라이언트 및 임시 저장소 획득
    client, path = isolated_client
    # 수정 전 데이터 저장
    # - 이후 변경 여부 비교
    before = json.loads(path.read_text(encoding="utf-8"))
    # 수정 요청 데이터
    payload = {"title": "서버 실행", "content": "새 안내 내용입니다.", "category": "api"}
    # 동일 요청을 두 번 수행
    # - 멱등성(idempotent) 확인
    for _ in range(2):
        # 수정 요청
        r = client.put("/api/knowledge/2", json=payload)
        # 수정 성공 확인
        assert r.status_code == 200
        # ID 유지 확인
        assert r.json() == dict(payload, id=2)
    # 수정 후 저장 데이터 로드
    saved = json.loads(path.read_text(encoding="utf-8"))
    # next_id 변경 금지
    # - 수정은 새 데이터 생성이 아님
    assert saved["next_id"] == before["next_id"]
    # 데이터 개수 유지 확인
    assert len(saved["entries"]) == len(before["entries"])
    # 첫 번째 데이터 불변 확인
    assert saved["entries"][0] == before["entries"][0]
    # 세 번째 데이터 불변 확인
    assert saved["entries"][2] == before["entries"][2]
    # 실제 수정 내용 확인
    assert client.get("/api/knowledge/2").json()["content"] == payload["content"]

# 수정 실패 상황 검증
# - 없는 ID 수정
# - 잘못된 요청 데이터
# - 파일 변경 없음 확인
def test_update_404_and_422_preserve_file(isolated_client):
    # 테스트 클라이언트 및 임시 파일 획득
    client, path = isolated_client
    # 요청 전 파일 상태 저장
    before = path.read_bytes()
    # 정상 형식 데이터
    valid = {"title": "제목", "content": "본문", "category": "guide"}
    # 존재하지 않는 ID 수정
    # - 404 Not Found
    assert client.put("/api/knowledge/9999", json=valid).status_code == 404
    # 잘못된 입력 데이터
    # - 필수 필드 누락
    # - 422 Validation Error
    assert client.put("/api/knowledge/2", json={"content": "본문만"}).status_code == 422
    # 실패 요청은 파일 변경 금지
    assert path.read_bytes() == before

# 삭제(Delete) 기능 검증
# - 204 응답 확인
# - 응답 본문 없음 확인
# - 실제 삭제 확인
# - next_id 유지 확인
def test_delete_empty_body_and_other_entries(isolated_client):
    # 테스트 클라이언트 및 임시 파일 획득
    client, path = isolated_client
    # 삭제 전 데이터 저장
    before = json.loads(path.read_text(encoding="utf-8"))
    # ID 2 삭제
    r = client.delete("/api/knowledge/2")
    # 삭제 성공
    assert r.status_code == 204
    # No Content 응답 확인
    assert r.content == b""
    # 삭제 후 상세 조회 불가
    assert client.get("/api/knowledge/2").status_code == 404
    # 저장 파일 확인
    saved = json.loads(path.read_text(encoding="utf-8"))
    # 삭제된 데이터 제외 확인
    assert saved["entries"] == [entry for entry in before["entries"] if entry["id"] != 2]
    # next_id 유지 확인
    assert saved["next_id"] == before["next_id"]

# 삭제 실패 검증
# - 존재하지 않는 ID
# - 잘못된 ID 형식
# - 파일 변경 없음 확인
def test_delete_errors_preserve_file(isolated_client):
    # 테스트 클라이언트 및 임시 파일 획득
    client, path = isolated_client
    # 요청 전 상태 저장
    before = path.read_bytes()
    # 없는 ID 삭제
    # - 404
    assert client.delete("/api/knowledge/9999").status_code == 404
    # 숫자가 아닌 ID
    # - 422
    assert client.delete("/api/knowledge/foo").status_code == 422
    # 실패 시 파일 변경 금지
    assert path.read_bytes() == before

# 마지막 ID 삭제 후 생성 검증
# - next_id 재사용 금지
# - 증가된 ID 사용 확인
def test_create_after_last_id_deleted(isolated_client):
    # 테스트 클라이언트 및 임시 파일 획득
    client, path = isolated_client
    # 마지막 엔트리 삭제
    assert client.delete("/api/knowledge/3").status_code == 204
    # 신규 데이터 생성
    r = client.post("/api/knowledge", json={"title":"새 지식", "content":"새 내용", "category":"guide"})
    # 생성 성공
    assert r.status_code == 201
    # next_id 기반 신규 ID 확인
    assert r.json()["id"] == 4
    # next_id 증가 확인
    assert json.loads(path.read_text(encoding="utf-8"))["next_id"] == 5

# OpenAPI 문서 및 응답 형식 검증
# - Swagger 문서 생성 확인
# - 응답 필드 확인
# - Docs 페이지 확인
def test_openapi_and_response_fields(isolated_client):
    # 테스트 클라이언트 획득
    client, _ = isolated_client
    # OpenAPI 스키마 조회
    doc = client.get("/openapi.json").json()
    # 목록 API 문서 확인
    assert {"get", "post"} <= set(doc["paths"]["/api/knowledge"])
    # 단건 API 문서 확인
    assert {"get", "put", "delete"} <= set(doc["paths"]["/api/knowledge/{knowledge_id}"])
    # 응답 스키마 검증용 조회
    r = client.get("/api/knowledge/1")
    # 조회 성공
    assert r.status_code == 200
    # 응답 필드 확인
    assert set(r.json()) == {"id", "title", "content", "category"}
    # Swagger UI 접근 확인
    assert client.get("/docs").status_code == 200


"""
본 테스트 코드는 생성·조회·수정·삭제 기능뿐만 아니라 입력 검증 실패 상황과 예외 처리까지 확인함으로써 API가 요구사항에 맞게 동작함을 검증하였다.
또한 실패 요청 시 저장 데이터가 변경되지 않음을 검사하여 데이터 무결성을 보장할 수 있음을 확인하였다.
"""