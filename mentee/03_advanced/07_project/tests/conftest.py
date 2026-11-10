"""제공 fixture: 각 테스트마다 새로운 임시 저장소를 사용합니다."""
# JSON 데이터 생성/읽기
# - 테스트용 seed 데이터 저장
import json
# pytest fixture 기능 사용
# - 테스트 준비 및 정리 자동화
import pytest
# FastAPI 테스트 클라이언트
# - HTTP 요청 시뮬레이션
from fastapi.testclient import TestClient

import sys
from pathlib import Path
# 07_project 폴더 경로 추가
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))
# app 폴더 경로도 추가 (main.py 내부의 routers 등을 인식하기 위함)
sys.path.append(str(root_dir / 'app'))
# # 현재 파일(conftest.py)의 부모(tests)의 부모(07_project) 경로를 시스템 경로에 추가
# sys.path.append(str(Path(__file__).parent.parent))
# 실제 애플리케이션 객체
# - 테스트 대상 서버
from app.main import app
# 저장소 모듈
# - DATA 경로 교체용
from app.repositories import json_knowledge as store

"""테스트마다 독립적인 임시 JSON 저장소를 생성하여 실제 운영 데이터를 변경하지 않고 API를 검증하기 위한 공통 Fixture 제공"""
# 테스트 시작 시 사용할 초기 데이터
# - next_id : 다음 생성 ID
# - entries : 기본 지식 데이터
SEED = {'next_id': 4, 'entries': [{'id': 1, 'title': '가상환경', 'category': 'setup', 'content': '프로젝트별 패키지를 분리한다.'}, {'id': 2, 'title': '서버 실행', 'category': 'api', 'content': 'uvicorn으로 개발 서버를 켠다.'}, {'id': 3, 'title': '입력 오류', 'category': 'api', 'content': '422이면 입력값을 확인한다.'}]}

# 각 테스트마다 독립적인 임시 저장소 제공
# - tmp_path : pytest 임시 디렉터리
# - monkeypatch : 전역 변수 교체
# - 반환 : (client, test_file)
@pytest.fixture
def isolated_client(tmp_path, monkeypatch):
    # 실제 data/knowledge.json을 읽거나 바꾸지 않습니다. 독립적인 고정 입력을 만듭니다.
    # 테스트 전용 JSON 파일 생성
    # - 실제 운영 데이터 사용 금지
    test_file = tmp_path / "knowledge.json"
    # seed 데이터 기록
    # - 모든 테스트 동일한 시작 상태 보장
    test_file.write_text(json.dumps(SEED, ensure_ascii=False), encoding="utf-8")
    # 실제 DATA 경로를 임시 파일로 교체
    # - 운영 파일 보호
    monkeypatch.setattr(store, "DATA", test_file)
    # 테스트 클라이언트 생성
    with TestClient(app) as client:
        # 테스트 함수에 전달
        yield client, test_file


"""
Fixture를 활용하여 모든 테스트가 동일한 초기 상태에서 시작하도록 구성하였으며,
monkeypatch를 이용해 실제 저장소 대신 임시 파일을 사용함으로써 테스트의 독립성과 안정성을 확보하였다.
"""