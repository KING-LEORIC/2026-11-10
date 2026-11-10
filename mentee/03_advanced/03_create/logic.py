"""데이터 처리 함수. HTTPException을 만들지 않고 dict·None·bool을 반환합니다."""
from storage import LOCK, read_data, write_data

# 지식 목록 조회
# - category : 조회할 카테고리
# - LOCK : 파일 접근 동기화
# - read_data() : 저장 데이터 읽기
# - entries : 전체 지식 목록
# - category가 지정되면 해당 카테고리만 필터링
# - 최종 지식 목록 반환
def list_entries(category: str | None = None) -> list[dict]:
    with LOCK:
        data = read_data()
    entries = data["entries"]
    if category is not None:
        entries = [entry for entry in entries if entry["category"] == category]
    return entries

# 단일 지식 조회
# - knowledge_id : 조회할 지식 ID
# - read_data() : 저장 데이터 읽기
# - data["entries"] : 전체 지식 목록
# - entry["id"] : 저장된 지식의 ID
# - 일치하는 항목 반환
# - 없으면 None 반환
def find_entry(knowledge_id: int) -> dict | None:
    with LOCK:
        data = read_data()
    for entry in data["entries"]:
        if entry["id"] == knowledge_id:
            return entry
    return None

# 새로운 지식 생성
# - fields : 요청 데이터(title, content, category)
# - LOCK : 파일 접근 동기화
# - read_data() : 저장 데이터 읽기
# - next_id : 다음에 사용할 ID
# - entry : 실제 저장할 지식 객체
# - 저장 완료 후 생성 결과 반환
def create(fields: dict) -> dict:
    with LOCK:
        data = read_data()
        # BEGIN H03-01
        # TODO H03-01: fields를 복사한 entry를 만들고 현재 next_id를 id로 지정하세요.
        # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
        # raise NotImplementedError("H03-01를 먼저 완성하세요.")

        # fields 사본 생성 및 ID 부여
        # - dict(fields) : 입력 데이터 복사
        # - data["next_id"] : 다음에 사용할 ID
        # - entry["id"] : 생성할 지식의 ID
        entry = dict(fields)
        entry["id"] = data["next_id"]
        # END H03-01
        # BEGIN H03-02
        # TODO H03-02: entry를 추가하고 다음 ID를 증가시켜 data 전체를 저장하세요.
        # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
        # raise NotImplementedError("H03-02를 먼저 완성하세요.")

        # 신규 지식 저장
        # - append() : 지식 목록에 추가
        # - next_id += 1 : 다음 ID 증가
        # - write_data() : 전체 데이터 저장
        data["entries"].append(entry)
        data["next_id"] += 1
        write_data(data)
        # END H03-02
    return entry
