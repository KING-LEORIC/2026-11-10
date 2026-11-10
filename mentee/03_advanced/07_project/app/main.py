"""HTTP와 저장 책임을 구분하는 지식 관리 API입니다."""
# FastAPI 애플리케이션 객체 사용
# - 웹 서버 생성
# - API 경로 등록
from fastapi import FastAPI
# Knowledge 관련 라우터 import
# - CRUD API 제공
from routers import knowledge

"""FastAPI 기반의 지식(Knowledge) 데이터를 JSON 파일에 저장·조회·수정·삭제(CRUD)하는 REST API 구현"""
"""main.py는 FastAPI 애플리케이션을 생성하고 Router를 등록하여 API 서버를 실행하는 진입점"""
# FastAPI 애플리케이션 생성
# - title : Swagger 문서 제목
app = FastAPI(title="Knowledge API")
# Knowledge Router 등록
# - /api/knowledge 이하 경로 활성화
app.include_router(knowledge.router)

# 서버 상태 확인 API
# - GET /health
# - 서버 동작 여부 확인용
@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    # 정상 상태 응답 반환
    # - 단순 헬스 체크
    # - DB 및 파일 상태 전체 점검은 아님
    return {"status": "ok"}

# 직접 실행 시 개발 서버 구동
# - main:app 애플리케이션 실행
# - 127.0.0.1:18080 포트 사용
# - reload=True : 파일 변경 시 자동 재시작
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=18080, reload=True)

"""
FastAPI 애플리케이션과 Router를 연결하여 API 서버의 시작점을 구성하였으며, Health Check API를 통해 서버 동작 상태를 확인할 수 있도록 구현하였다.
"""

"""
본 프로젝트는 FastAPI 기반 REST API와 JSON 파일 저장소를 이용하여 지식 데이터를
생성(Create), 조회(Read), 수정(Update), 삭제(Delete)할 수 있는 지식 관리 시스템을 구현하는 것을 목적으로 한다.

결론 : 본 프로젝트에서는 FastAPI를 이용하여 지식 데이터 관리 API를 구현하고, Repository 계층과 Router 계층을 분리하여 역할과 책임을 명확히 하였다.
또한 Pydantic을 통해 입력 데이터를 검증하고, Lock 및 임시 파일 교체 방식을 적용하여 파일 기반 저장 환경에서도 데이터 무결성과 안정성을 확보하였다.
이를 통해 간단한 JSON 저장소를 활용한 CRUD 기반 지식 관리 시스템을 성공적으로 구축할 수 있었다.
"""