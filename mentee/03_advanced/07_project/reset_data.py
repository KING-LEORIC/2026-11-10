"""서버를 끈 상태에서만 명시적으로 초기화합니다. 서버 시작 시 호출하지 마세요."""
# 명령행 옵션 처리
# - --confirm-reset 옵션 확인
import argparse
# JSON 데이터 처리
# - 파일 읽기/쓰기
import json
# 파일 경로 객체 사용
# - 운영체제 독립적 경로 처리
from pathlib import Path
# 현재 시각 생성
# - 백업 파일명 생성용
from datetime import datetime
# 파일 복사 기능
# - 기존 데이터 백업
import shutil

"""시드 데이터(knowledge.seed.json)를 기준으로 현재 저장 데이터를 초기 상태로 복원하고, 기존 데이터는 백업 파일로 보관하는 유틸리티 프로그램"""
# 초기화 프로그램 시작 함수
# - 시드 데이터로 복원 수행
# - 반환값 없음
def main() -> None:
    # 명령행 옵션 파서 생성
    # - 초기화 실행 전 확인 절차 제공
    parser = argparse.ArgumentParser(description="현재 폴더의 학습 데이터 초기화")
    # 강제 확인 옵션 등록
    # - 사용자가 명시적으로 승인해야 실행
    parser.add_argument("--confirm-reset", action="store_true", help="기존 작업 데이터 초기화를 명시적으로 승인")
    # 명령행 인수 해석
    args = parser.parse_args()
    # 확인 옵션 누락 시 실행 중단
    if not args.confirm_reset:
        parser.error("서버를 먼저 종료하세요. 초기화가 필요할 때만 --confirm-reset을 붙입니다.")
    # 프로젝트 루트 경로 계산
    # - reset_data.py 위치 기준
    base = Path(__file__).resolve().parent
    # 실제 데이터 파일 경로
    data = base / "data" / "knowledge.json"
    # 초기 시드 데이터 경로
    seed = base / "data" / "knowledge.seed.json"
    # 시드 데이터 로드
    # - 파일 내용을 JSON 객체로 변환
    obj = json.loads(seed.read_text(encoding="utf-8"))
    # 시드 데이터 구조 검증
    # - dict 구조인지 확인
    # - entries 리스트 확인
    # - next_id 정수 확인
    if not isinstance(obj, dict) or not isinstance(obj.get("entries"), list) or not isinstance(obj.get("next_id"), int):
        raise ValueError("초기 데이터 형식이 올바르지 않습니다. 현재 파일은 유지합니다.")
    # 기존 데이터 백업 생성
    if data.exists():
        # 현재 시각 기반 백업 이름 생성
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        # 백업 파일 경로 생성
        backup = data.with_name(f"knowledge.backup_{stamp}.json")
        # 원본 파일 복사
        shutil.copy2(data, backup)
        print("백업:", backup)
    # 초기화용 임시 파일 생성
    # - 저장 중 데이터 손상 방지
    temp = data.with_suffix(".reset.tmp")
    try:
        # 시드 데이터를 임시 파일에 저장
        temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        # 임시 파일을 실제 데이터 파일로 교체
        # - 원자적 교체 방식
        temp.replace(data)
    finally:
        # 남아있는 임시 파일 제거
        temp.unlink(missing_ok=True)
    print("초기화 완료:", data)
    print("일일프로젝트의 재시작 확인 중에는 이 명령을 실행하지 않습니다.")

# 현재 파일을 직접 실행한 경우에만 동작
# - import 시 자동 실행 방지
if __name__ == "__main__":
    # 초기화 함수 실행
    main()

"""
데이터 초기화 도구를 별도로 구현하여 운영 중인 데이터를 보호하면서도 필요 시 초기 상태로 안전하게 복원할 수 있도록 하였다.
또한 백업 생성과 임시 파일 교체 방식을 적용하여 데이터 손실 가능성을 최소화하였다.
"""