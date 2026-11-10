"""8교시 심화: 임시 파일만 변경합니다. 실제 서버 재시작 검증은 별도로 하세요."""
# JSON 데이터 읽기
# - 저장 파일 상태 확인
# - 생성/수정/삭제 검증
import json

"""생성(Create), 수정(Update), 입력 검증(Validation), 삭제(Delete)를 하나의 시나리오로 연결하여 실제 사용 흐름에서 API가 정상 동작하는지 종합적으로 검증하는 통합 테스트"""
# CRUD 전체 흐름 검증
# - 생성(Create)
# - 수정(Update)
# - 입력 검증(Validation)
# - 삭제(Delete)
# - 기존 데이터 보존 확인
def test_daily_project_abc(isolated_client):
    # 테스트 클라이언트와 임시 저장 파일 획득
    client, path = isolated_client
    # 초기 데이터 저장
    # - 이후 변경 여부 비교
    initial = json.loads(path.read_text(encoding="utf-8"))
    # 초기 데이터 개수 저장
    n = len(initial["entries"])
    # 생성할 테스트 데이터 목록
    # - A : 파일 보관
    # - B : 질문 방법
    # - C : 삭제 확인용
    payloads = [
        {"title": "파일 보관", "content": "개인 폴더에 보관합니다.", "category": "learning"},
        {"title": "질문 방법", "content": "질문을 메모합니다.", "category": "help"},
        {"title": "임시 공지", "content": "이 항목은 삭제 확인용입니다.", "category": "help"},
    ]
    # 생성 결과 저장 리스트
    created = []
    # 데이터 생성 반복
    for payload in payloads:
        # 생성 요청
        response = client.post("/api/knowledge", json=payload)
        # 생성 성공 확인
        assert response.status_code == 201
        # 생성 결과 저장
        created.append(response.json())
    # 생성된 데이터 분리
    # - a : 첫 번째 생성 데이터
    # - b : 두 번째 생성 데이터
    # - c : 세 번째 생성 데이터
    a, b, c = created
    # 모든 ID가 서로 다른지 확인
    assert len({a["id"], b["id"], c["id"]}) == 3
    # 전체 데이터 개수 증가 확인
    assert len(client.get("/api/knowledge").json()) == n + 3
    # B 데이터 수정 요청 생성
    # - 제목 유지
    # - 카테고리 유지
    # - 내용만 수정
    changed = {"title": b["title"], "content": "오류 메시지와 함께 질문합니다.", "category": b["category"]}
    # 수정 요청
    r = client.put(f"/api/knowledge/{b['id']}", json=changed)
    # BEGIN H08-01
    # TODO H08-01: B 수정의 200과 같은 ID의 재조회 본문을 검사하세요. expected는 changed와 B의 기존 ID입니다.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    # raise NotImplementedError("H08-01를 먼저 완성하세요.")

    # 수정 성공 확인
    # - HTTP 200 OK
    assert r.status_code == 200
    # 수정 데이터 재조회 확인
    # - 기존 ID 유지
    # - 내용 변경 반영
    assert client.get(f"/api/knowledge/{b['id']}").json() == dict(changed, id=b["id"])
    # END H08-01
    # 잘못된 요청 전 파일 상태 저장
    before_invalid = path.read_bytes()
    # 검증 실패용 데이터
    # - content가 빈 문자열
    bad = {"title": "빈 본문", "content": "", "category": "help"}
    # 생성 요청
    r = client.post("/api/knowledge", json=bad)
    # BEGIN H08-02
    # TODO H08-02: 빈 본문 입력의 422와 파일 불변을 검사하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    # raise NotImplementedError("H08-02를 먼저 완성하세요.")

    # 입력 검증 실패 확인
    # - HTTP 422 Validation Error
    assert r.status_code == 422
    # 실패 요청은 저장 파일 변경 금지
    assert path.read_bytes() == before_invalid
    # END H08-02
    # C 데이터 삭제 요청
    r = client.delete(f"/api/knowledge/{c['id']}")
    # BEGIN H08-03
    # TODO H08-03: C 삭제의 204·빈 본문과 삭제 후 상세 GET의 404를 모두 확인하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    # raise NotImplementedError("H08-03를 먼저 완성하세요.")

    # 삭제 성공 확인
    # - HTTP 204 No Content
    assert r.status_code == 204
    # 응답 본문 없음 확인
    assert r.content == b""
    # 삭제 후 조회 불가 확인
    # - HTTP 404 Not Found
    assert client.get(f"/api/knowledge/{c['id']}").status_code == 404
    # END H08-03
    # 최종 저장 데이터 확인
    final = json.loads(path.read_text(encoding="utf-8"))
    # 생성 3건 + 삭제 1건
    # - 결과적으로 2건 증가
    assert len(final["entries"]) == n + 2
    # A 데이터 유지 확인
    assert client.get(f"/api/knowledge/{a['id']}").json() == a
    # 기존 데이터가 모두 보존되는지 확인
    # - 수정하지 않은 데이터는 그대로 유지
    for old in initial["entries"]:
        assert client.get(f"/api/knowledge/{old['id']}").json() == old


"""
본 테스트는 여러 CRUD 작업을 연속 수행하면서 데이터 생성, 수정, 삭제 및 입력 검증 과정이 올바르게 동작하는지 검증하였다.
또한 오류 발생 시 저장 데이터가 유지되고, 정상 작업 후에는 기대한 결과만 반영됨을 확인하여 시스템의 신뢰성과 데이터 무결성을 검증할 수 있었다.
"""