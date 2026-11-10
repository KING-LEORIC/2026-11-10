"""제공 코드: 파일 접근 보조 함수. 호출자가 같은 LOCK으로 읽기~저장을 묶습니다."""
import json
from pathlib import Path
from threading import Lock

# 프로젝트 기준 경로
# - 현재 파일 위치 기준
BASE = Path(__file__).resolve().parent
# 데이터 파일 경로
# - knowledge.json 사용
DATA = BASE / "data" / "knowledge.json"
# 파일 접근 동기화 객체
# - 동일 프로세스 내 동시 접근 방지
LOCK = Lock()

# JSON 데이터 읽기
# - 파일 내용을 dict로 변환
# - 오류는 호출자에게 전달
def read_data() -> dict:
    # 파일이 없거나 JSON이 손상되면 예외를 알립니다. 빈 목록으로 덮어쓰지 않습니다.
    with DATA.open("r", encoding="utf-8") as f:
        return json.load(f)

# JSON 데이터 저장
# - 임시 파일 작성
# - 원본 교체
# - 저장 중 손상 최소화
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
