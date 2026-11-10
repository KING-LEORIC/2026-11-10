"""서버를 끈 상태에서만 명시적으로 초기화합니다. 서버 시작 시 호출하지 마세요."""
import argparse
import json
from pathlib import Path
from datetime import datetime
import shutil

# 학습 데이터 초기화 진입점
# - 실행 인자 검증
# - seed 데이터를 현재 데이터로 복원
# - 기존 데이터는 백업 생성
# - 안전한 파일 교체 방식 사용
def main() -> None:
    # 명령행 인자 파서 생성
    # - 초기화 승인 여부 확인
    parser = argparse.ArgumentParser(description="현재 폴더의 학습 데이터 초기화")
    parser.add_argument("--confirm-reset", action="store_true", help="기존 작업 데이터 초기화를 명시적으로 승인")
    args = parser.parse_args()
    # 사용자 명시적 승인 확인
    # - 승인 없으면 초기화 중단
    if not args.confirm_reset:
        parser.error("서버를 먼저 종료하세요. 초기화가 필요할 때만 --confirm-reset을 붙입니다.")
    # 프로젝트 기준 경로 계산
    # - reset_data.py 위치 기준
    base = Path(__file__).resolve().parent
    # 현재 사용 데이터 파일
    data = base / "data" / "knowledge.json"
    # 초기 상태(시드) 데이터 파일
    seed = base / "data" / "knowledge.seed.json"
    # 시드 데이터 로드
    # - JSON → dict 변환
    obj = json.loads(seed.read_text(encoding="utf-8"))
    # 시드 데이터 구조 검증
    # - entries 목록 존재 확인
    # - next_id 정수 여부 확인
    if not isinstance(obj, dict) or not isinstance(obj.get("entries"), list) or not isinstance(obj.get("next_id"), int):
        raise ValueError("초기 데이터 형식이 올바르지 않습니다. 현재 파일은 유지합니다.")
    # 기존 데이터 백업 생성
    # - 타임스탬프 포함 파일명 사용
    if data.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup = data.with_name(f"knowledge.backup_{stamp}.json")
        shutil.copy2(data, backup)
        print("백업:", backup)
    # 임시 파일 생성
    # - 완성 후 원본 교체
    temp = data.with_suffix(".reset.tmp")
    try:
        # 초기 데이터를 임시 파일에 저장
        temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        # 현재 데이터 파일 교체
        temp.replace(data)
    finally:
        # 임시 파일 정리
        temp.unlink(missing_ok=True)
    print("초기화 완료:", data)
    print("일일프로젝트의 재시작 확인 중에는 이 명령을 실행하지 않습니다.")

# 스크립트 직접 실행 시 진입
# - main() 호출
if __name__ == "__main__":
    main()
