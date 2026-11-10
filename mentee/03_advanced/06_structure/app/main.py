"""HTTP와 저장 책임을 구분하는 지식 관리 API입니다."""
from fastapi import FastAPI
from app.routers import knowledge

# FastAPI 애플리케이션 생성
# - title : Swagger 문서 제목
app = FastAPI(title="Knowledge API")
"""FastAPI 기반의 지식(Knowledge) 관리 REST API에서 JSON 파일을 저장소처럼 사용하여 CRUD(Create, Read, Update, Delete) 기능을 제공하는 프로그램"""
# BEGIN H06-01
# TODO H06-01: knowledge 모듈의 router를 app에 포함하세요. 추가 prefix를 붙이지 마세요.
# 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
# pass  # 앱은 시작되지만 아직 지식 Router는 연결되지 않았습니다.

# Knowledge Router 등록
# - knowledge.router의 모든 API 활성화
app.include_router(knowledge.router)
# END H06-01

# 서버 상태 확인 API
# - GET /health
# - 서비스 동작 여부 간단 확인
@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    return {"status": "ok"}

# 직접 실행 시 개발 서버 구동
# - main:app 애플리케이션 실행
# - 127.0.0.1:18080 포트 사용
# - reload=True : 파일 변경 시 자동 재시작
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=18080, reload=True)

"""
본 프로그램은 FastAPI와 JSON 파일 저장 방식을 이용하여 지식 데이터를 생성, 조회, 수정, 삭제할 수 있는 REST API를 구현하였다.
Router는 HTTP 요청과 응답을 담당하고 Repository는 데이터 저장 및 조회를 담당하도록 계층을 분리하였으며,
Lock과 임시 파일 교체 방식을 통해 데이터 무결성을 고려한 파일 저장 구조를 적용하였다.
이를 통해 API 계층과 데이터 저장 계층의 역할을 명확하게 분리하는 구조를 학습할 수 있었다.

핵심 설계 요약
- Router : HTTP 요청/응답 처리 담당
- Schema(Pydantic) : 입력 데이터 검증 담당
- Repository : JSON 파일 CRUD 담당
- Lock : 동시 접근 방지
- Temp File + replace() : 저장 중 파일 손상 위험 감소
- FastAPI Response Model : 응답 형식 자동 검증
- HTTPException : 404 오류 처리

즉, 이 프로젝트의 가장 중요한 특징은 "API 계층(Router)과 데이터 저장 계층(Repository)을 분리하여 역할을 명확히 나눈 CRUD REST API 구현" 이라는 점이다.
"""