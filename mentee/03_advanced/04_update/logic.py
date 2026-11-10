"""데이터 처리 함수. HTTPException을 만들지 않고 dict·None·bool을 반환합니다."""
from storage import LOCK, read_data, write_data

# 지식 목록 조회
# - category가 None이면 전체 목록 반환
# - category가 지정되면 해당 카테고리만 필터링
# - read_data()로 저장 데이터 조회
# - entries 목록 반환
def list_entries(category: str | None = None) -> list[dict]:
    with LOCK:
        data = read_data()
    entries = data["entries"]
    if category is not None:
        entries = [entry for entry in entries if entry["category"] == category]
    return entries

# ID로 지식 조회
# - knowledge_id와 일치하는 항목 검색
# - 존재하면 해당 dict 반환
# - 없으면 None 반환
def find_entry(knowledge_id: int) -> dict | None:
    with LOCK:
        data = read_data()
    for entry in data["entries"]:
        if entry["id"] == knowledge_id:
            return entry
    return None

# 신규 지식 생성
# - fields 복사
# - next_id를 ID로 부여
# - entries에 추가
# - next_id 증가 후 저장
# - 생성된 항목 반환
def create(fields: dict) -> dict:
    with LOCK:
        data = read_data()
        entry = dict(fields)
        entry["id"] = data["next_id"]
        data["entries"].append(entry)
        data["next_id"] += 1
        write_data(data)
    return entry

# 기존 지식 수정
# - knowledge_id로 항목 검색
# - 입력값 복사본 생성
# - 기존 ID 유지
# - 찾은 위치를 수정 데이터로 교체
# - 저장 후 수정 결과 반환
# - 항목이 없으면 None 반환
def update(knowledge_id: int, fields: dict) -> dict | None:
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                # BEGIN H04-01
                # TODO H04-01: fields의 복사본 updated를 만들고 기존 요청 ID를 유지하세요.
                # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
                # raise NotImplementedError("H04-01를 먼저 완성하세요.")

                # fields 복사본 생성
                # - 요청 데이터 원본 보존
                # - 수정용 객체 생성
                # - 기존 ID 유지
                updated = dict(fields)
                updated["id"] = knowledge_id
                # END H04-01
                # BEGIN H04-02
                # TODO H04-02: 찾은 위치 i를 교체하고 저장하세요. 다른 항목과 next_id는 그대로 두세요.
                # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
                # raise NotImplementedError("H04-02를 먼저 완성하세요.")

                # 기존 위치 교체 및 저장
                # - i 위치만 수정
                # - 다른 entries 유지
                # - next_id 유지
                data["entries"][i] = updated
                write_data(data)
                # END H04-02
                return updated
    return None
