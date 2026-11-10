"""제공 코드: 파일 접근 보조 함수. 호출자가 같은 LOCK으로 읽기~저장을 묶습니다."""
import json
from pathlib import Path
from threading import Lock

# 프로젝트 루트 디렉터리 계산
# - __file__ : 현재 파일 경로
# - resolve() : 절대 경로 변환
# - parents[2] : 상위 2단계 디렉터리(프로젝트 루트)
BASE = Path(__file__).resolve().parents[2]
# 지식 데이터 JSON 파일 경로
# - BASE : 프로젝트 루트
# - knowledge.json : 실제 저장 파일
DATA = BASE / "data" / "knowledge.json"
# 스레드 동기화를 위한 전역 Lock 객체
# - 읽기/쓰기 중 동시 접근 방지
LOCK = Lock()

# JSON 파일 읽기
# - knowledge.json 파일 열기
# - json.load() : JSON 문자열 → dict 변환
# - 반환값 : 전체 데이터(dict)
def read_data() -> dict:
    # 파일이 없거나 JSON이 손상되면 예외를 알립니다. 빈 목록으로 덮어쓰지 않습니다.
    with DATA.open("r", encoding="utf-8") as f:
        return json.load(f)

# JSON 파일 저장
# - temp 파일에 먼저 저장
# - 저장 성공 시 원본 파일 교체
# - 예외 발생 시 임시 파일 삭제
def write_data(data: dict) -> None:
    # 원본부터 비우지 않고 같은 폴더의 임시 파일을 완성한 다음 교체합니다.
    # 단일 프로세스의 같은 LOCK 아래에서만 호출합니다. DB 트랜잭션은 아닙니다.
    temp = DATA.with_suffix(".tmp")
    try:
        with temp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        temp.replace(DATA)
    finally:
        temp.unlink(missing_ok=True)

# 지식 목록 조회
# - 전체 entries 목록 조회
# - category가 주어지면 해당 카테고리만 필터링
# - 반환값 : 지식 항목 리스트
def list_entries(category: str | None = None) -> list[dict]:
    with LOCK:
        data = read_data()
    entries = data["entries"]
    if category is not None:
        entries = [entry for entry in entries if entry["category"] == category]
    # BEGIN H06-02
    # TODO H06-02: Repository의 목록 조회 결과를 반환하세요. HTTP Response를 만들지 마세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    # raise NotImplementedError("H06-02를 먼저 완성하세요.")

    # 조회된 지식 목록 반환
    # - entries : 전체 또는 필터링된 결과 목록
    return entries
    # END H06-02

# ID로 지식 조회
# - entries를 순회하며 ID 비교
# - 찾으면 해당 dict 반환
# - 없으면 None 반환
def find_entry(knowledge_id: int) -> dict | None:
    with LOCK:
        data = read_data()
    for entry in data["entries"]:
        if entry["id"] == knowledge_id:
            return entry
    return None

# 지식 생성
# - next_id를 새로운 ID로 사용
# - entries에 추가
# - next_id 증가
# - 저장 후 생성 객체 반환
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
# - ID 일치 항목 탐색
# - 전달된 fields 기반으로 새 객체 생성
# - 기존 항목 교체
# - 성공 시 수정 결과 반환
# - 없으면 None 반환
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
# - ID 일치 항목 탐색
# - 목록에서 제거
# - 저장 수행
# - 성공 여부(bool) 반환
def delete(knowledge_id: int) -> bool:
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                data["entries"].pop(i)
                write_data(data)
                return True
    return False
