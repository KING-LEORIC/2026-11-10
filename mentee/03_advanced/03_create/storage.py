"""제공 코드: 파일 접근 보조 함수. 호출자가 같은 LOCK으로 읽기~저장을 묶습니다."""
import json
from pathlib import Path
from threading import Lock

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "knowledge.json"
LOCK = Lock()

# JSON 데이터 읽기
# - DATA : knowledge.json 파일 경로
# - open() : 파일 열기
# - json.load() : JSON → dict 변환
# - dict 형태 데이터 반환
def read_data() -> dict:
    # 파일이 없거나 JSON이 손상되면 예외를 알립니다. 빈 목록으로 덮어쓰지 않습니다.
    with DATA.open("r", encoding="utf-8") as f:
        return json.load(f)

# JSON 데이터 저장
# - data : 저장할 전체 데이터
# - temp : 임시 파일 경로
# - json.dump() : dict → JSON 저장
# - replace() : 원본 파일 교체
# - finally : 임시 파일 정리
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
