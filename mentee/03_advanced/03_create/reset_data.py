"""서버를 끈 상태에서만 명시적으로 초기화합니다. 서버 시작 시 호출하지 마세요."""
import argparse
import json
from pathlib import Path
from datetime import datetime
import shutil

# 데이터 초기화 수행
# - argparse : 명령행 옵션 처리
# - seed 데이터 복원
# - 기존 데이터 백업
# - 임시 파일 생성 후 교체
# - 초기화 결과 출력
def main() -> None:
    # 명령행 옵션 설정
    # - --confirm-reset : 초기화 승인 옵션
    parser = argparse.ArgumentParser(description="현재 폴더의 학습 데이터 초기화")
    parser.add_argument("--confirm-reset", action="store_true", help="기존 작업 데이터 초기화를 명시적으로 승인")
    args = parser.parse_args()
    # 초기화 승인 여부 확인
    # - 옵션 없으면 실행 중단
    if not args.confirm_reset:
        parser.error("서버를 먼저 종료하세요. 초기화가 필요할 때만 --confirm-reset을 붙입니다.")
    # 파일 경로 설정
    # - data : 실제 저장 파일
    # - seed : 초기 데이터 파일
    base = Path(__file__).resolve().parent
    data = base / "data" / "knowledge.json"
    seed = base / "data" / "knowledge.seed.json"
    # 초기 데이터 읽기
    # - seed 파일 로드
    # - JSON → dict 변환
    obj = json.loads(seed.read_text(encoding="utf-8"))
    # 데이터 형식 검증
    # - dict 여부 확인
    # - entries 목록 확인
    # - next_id 정수 확인
    if not isinstance(obj, dict) or not isinstance(obj.get("entries"), list) or not isinstance(obj.get("next_id"), int):
        raise ValueError("초기 데이터 형식이 올바르지 않습니다. 현재 파일은 유지합니다.")
    # 기존 데이터 백업
    # - timestamp 기반 백업 파일 생성
    if data.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup = data.with_name(f"knowledge.backup_{stamp}.json")
        shutil.copy2(data, backup)
        print("백업:", backup)
    temp = data.with_suffix(".reset.tmp")
    try:
        # 초기 데이터 저장
        # - obj : 복원 데이터
        # - temp : 임시 파일
        # - replace() : 원본 교체
        temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(data)
    finally:
        temp.unlink(missing_ok=True)
    print("초기화 완료:", data)
    print("일일프로젝트의 재시작 확인 중에는 이 명령을 실행하지 않습니다.")


if __name__ == "__main__":
    main()
