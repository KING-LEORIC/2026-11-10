"""제공 코드: 파일 접근 보조 함수. 호출자가 같은 LOCK으로 읽기~저장을 묶습니다."""
# JSON 파일 읽기/쓰기 기능 사용
# - json.load() : JSON → dict 변환
# - json.dump() : dict → JSON 저장
import json
# 파일 경로 조작 객체 사용
# - 운영체제와 무관한 경로 처리 지원
from pathlib import Path
# 스레드 동기화를 위한 Lock 사용
# - 파일 동시 접근 충돌 방지
from threading import Lock

"""JSON 파일을 데이터 저장소로 사용하여 지식 데이터의 조회, 생성, 수정, 삭제(CRUD) 기능을 담당하는 Repository 계층"""
# 프로젝트 루트 디렉터리 계산
# - __file__ : 현재 파이썬 파일 위치
# - resolve() : 절대 경로 반환
# - parents[2] : 상위 2단계 폴더 선택
BASE = Path(__file__).resolve().parents[2]
# 실제 지식 데이터 저장 파일 경로
# - BASE : 프로젝트 루트
# - knowledge.json : 데이터 저장 파일
DATA = BASE / "data" / "knowledge.json"
# 파일 읽기/쓰기 동기화를 위한 Lock 객체
# - 같은 프로세스 내 스레드 충돌 방지
LOCK = Lock()

# JSON 파일 데이터를 읽어 dict로 반환
# - 파일이 존재해야 함
# - JSON 형식 오류 시 예외 발생
# - 반환 타입 : dict
def read_data() -> dict:
    # 파일이 없거나 JSON이 손상되면 예외를 알립니다. 빈 목록으로 덮어쓰지 않습니다.
    with DATA.open("r", encoding="utf-8") as f:
        return json.load(f)

# 전달받은 dict 데이터를 JSON 파일에 저장
# - data : 저장할 JSON 객체
# - 반환값 없음(None)
def write_data(data: dict) -> None:
    # 원본부터 비우지 않고 같은 폴더의 임시 파일을 완성한 다음 교체합니다.
    # 단일 프로세스의 같은 LOCK 아래에서만 호출합니다. DB 트랜잭션은 아닙니다.
    # 임시 저장 파일 경로 생성
    # - knowledge.tmp 생성
    temp = DATA.with_suffix(".tmp")
    try:
        # 임시 파일에 JSON 기록
        # - ensure_ascii=False : 한글 유지
        # - indent=2 : 보기 좋은 들여쓰기
        with temp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # 임시 파일을 원본 파일로 교체
        # - 저장 중 손상 방지
        temp.replace(DATA)
    finally:
        # 남아있을 수 있는 임시 파일 삭제
        # - missing_ok=True : 없어도 예외 없음
        temp.unlink(missing_ok=True)

# 전체 데이터 또는 카테고리별 데이터 조회
# - category : 조회할 카테고리
# - None이면 전체 반환
# - 반환 타입 : list[dict]
def list_entries(category: str | None = None) -> list[dict]:
    # 데이터 읽기 중 동시 접근 방지
    with LOCK:
        data = read_data()
    # 엔트리 목록 추출
    # - entries : 전체 지식 데이터 목록
    entries = data["entries"]
    # 카테고리 조건 조회
    # - category 값이 있는 경우만 수행
    if category is not None:
        entries = [entry for entry in entries if entry["category"] == category]
    return entries

# ID로 특정 데이터 조회
# - knowledge_id : 찾을 ID
# - 찾으면 dict 반환
# - 없으면 None 반환
def find_entry(knowledge_id: int) -> dict | None:
    # 파일 읽기 중 동시 접근 방지
    with LOCK:
        data = read_data()
    # 모든 엔트리 순회
    # - entry : 개별 지식 데이터
    for entry in data["entries"]:
        # 요청 ID와 저장된 ID 비교
        # - 일치 시 해당 데이터 반환
        if entry["id"] == knowledge_id:
            return entry
    return None

# 신규 지식 데이터 생성
# - fields : 입력 데이터
# - 반환 타입 : dict
# - 생성된 데이터 반환
def create(fields: dict) -> dict:
    # 파일 읽기/쓰기 동기화
    with LOCK:
        data = read_data()
        # 입력 데이터 복사
        # - 원본 수정 방지
        entry = dict(fields)
        # 새 ID 부여
        # - next_id 사용
        entry["id"] = data["next_id"]
        # 엔트리 목록에 추가
        # - 신규 데이터 저장
        data["entries"].append(entry)
        # 다음 ID 증가
        # - 중복 ID 방지
        data["next_id"] += 1
        # BEGIN H07-01
        # TODO H07-01: 생성 데이터와 next_id를 파일에 저장하는 연결을 완성하세요.
        # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
        # raise NotImplementedError("H07-01를 먼저 완성하세요.")

        # 변경된 entries 와 next_id 저장
        # - write_data() : JSON 파일 반영
        write_data(data)
        # END H07-01
    return entry

# 기존 지식 데이터 수정
# - knowledge_id : 수정 대상 ID
# - fields : 수정 데이터
# - 성공 시 dict 반환
# - 실패 시 None 반환
def update(knowledge_id: int, fields: dict) -> dict | None:
    # 파일 읽기/쓰기 동기화
    with LOCK:
        data = read_data()
        # 인덱스와 데이터를 함께 순회
        # - i : 위치 인덱스
        # - entry : 현재 데이터
        for i, entry in enumerate(data["entries"]):
            # 수정 대상 검색
            if entry["id"] == knowledge_id:
                # 수정 데이터 복사
                # - fields 원본 보호
                updated = dict(fields)
                # 기존 ID 유지
                # - URL 경로의 ID 사용
                updated["id"] = knowledge_id
                # 기존 데이터 교체
                # - i 위치 갱신
                data["entries"][i] = updated
                # 수정 결과 저장
                # - JSON 파일 반영
                write_data(data)
                return updated
    return None

# 특정 지식 데이터 삭제
# - knowledge_id : 삭제 대상 ID
# - 성공 시 True
# - 실패 시 False
def delete(knowledge_id: int) -> bool:
    # 파일 읽기/쓰기 동기화
    with LOCK:
        data = read_data()
        # 인덱스와 데이터를 함께 순회
        # - 삭제를 위해 위치 필요
        for i, entry in enumerate(data["entries"]):
            # 삭제 대상 확인
            if entry["id"] == knowledge_id:
                # 목록에서 데이터 제거
                # - pop(i) : 해당 위치 삭제
                data["entries"].pop(i)
                # 삭제 결과 저장
                # - JSON 파일 반영
                write_data(data)
                return True
    return False

"""
본 파일은 JSON 기반 저장소를 이용하여 지식 데이터를 관리하도록 구현하였다.
또한 Lock을 사용한 동기화와 임시 파일 교체 방식을 적용하여 동시 접근 상황과 저장 중 데이터 손상 가능성을 최소화하였다.
"""