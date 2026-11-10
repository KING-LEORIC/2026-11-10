"""데이터 처리 함수. HTTPException을 만들지 않고 dict·None·bool을 반환합니다."""
from storage import LOCK, read_data, write_data

# 지식 목록 조회
# - category=None : 전체 데이터 조회
# - category 지정 : 해당 카테고리 데이터만 조회
# - LOCK : 파일 접근 동기화
# - read_data() : JSON 데이터 로드
# - 반환값 : 지식 목록(list[dict])
def list_entries(category: str | None = None) -> list[dict]:
    with LOCK:
        data = read_data()
    entries = data["entries"]
    if category is not None:
        entries = [entry for entry in entries if entry["category"] == category]
    return entries

# 지식 단건 조회
# - knowledge_id : 조회할 지식 ID
# - entries 목록을 순회하면서 검색
# - 찾으면 해당 dict 반환
# - 찾지 못하면 None 반환
def find_entry(knowledge_id: int) -> dict | None:
    with LOCK:
        data = read_data()
    for entry in data["entries"]:
        if entry["id"] == knowledge_id:
            return entry
    return None

# 지식 생성
# - fields : title/content/category 입력 데이터
# - next_id : 다음 사용할 ID
# - entries : 저장 목록
# - write_data() : 변경사항 저장
# - 반환값 : 생성된 지식 정보
def create(fields: dict) -> dict:
    with LOCK:
        data = read_data()
        entry = dict(fields)
        entry["id"] = data["next_id"]
        data["entries"].append(entry)
        data["next_id"] += 1
        write_data(data)
    return entry

# 지식 수정
# - knowledge_id : 수정 대상 ID
# - fields : 수정할 데이터
# - 기존 ID는 유지
# - 수정 성공 시 수정 결과 반환
# - 수정 실패 시 None 반환
def update(knowledge_id: int, fields: dict) -> dict | None:
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                updated = dict(fields)
                updated["id"] = knowledge_id
                data["entries"][i] = updated
                write_data(data)
                return updated
    return None

# 지식 삭제
# - knowledge_id : 삭제 대상 ID
# - entries 목록에서 해당 항목 탐색
# - pop(i) : 해당 위치 데이터 제거
# - write_data(data) : 삭제 결과 저장
# - 성공 시 True 반환
# - 실패 시 False 반환
def delete(knowledge_id: int) -> bool:
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                # BEGIN H05-01
                # TODO H05-01: 대상 위치를 제거하고 저장한 뒤 True를 반환하세요. next_id는 변경하지 마세요.
                # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
                # raise NotImplementedError("H05-01를 먼저 완성하세요.")

                data["entries"].pop(i)
                write_data(data)
                return True
                # END H05-01
    return False
