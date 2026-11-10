"""HTTP와 저장 책임을 구분하는 지식 관리 API입니다."""
from fastapi import FastAPI, HTTPException, Response
import logic as repo
from schemas import Knowledge, KnowledgeWrite

# FastAPI 애플리케이션 생성
# - title : Swagger 문서 제목
# - app : API 서버 객체
app = FastAPI(title="Knowledge API")
"""FastAPI와 JSON 파일 저장소를 이용하여 지식 정보를 조회하고 등록할 수 있는 RESTful Knowledge API 구현"""
# 서버 동작 상태 확인
# - GET /health
# - 파일 저장소 상태 확인 아님
# - 서버 응답 가능 여부만 반환 //{"status":"ok"} 반환
@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    return {"status": "ok"}

# 지식 목록 조회 API
# - GET /api/knowledge
# - category 쿼리 파라미터 사용 가능
# - repo.list_entries() 호출
# - 없으면 전체 조회
# - 있으면 해당 카테고리만 조회
@app.get("/api/knowledge")
def list_knowledge(category: str | None = None):
    return repo.list_entries(category)

# 단일 지식 조회 API
# - GET /api/knowledge/{knowledge_id}
# - knowledge_id : 조회할 ID
# - repo.find_entry() 호출
# - 데이터가 없으면 404 예외 발생
# - 존재 시 해당 데이터 반환
@app.get("/api/knowledge/{knowledge_id}")
def get_knowledge(knowledge_id: int):
    entry = repo.find_entry(knowledge_id)
    if entry is None:
        raise HTTPException(404, "Knowledge not found")
    return entry

# 지식 생성 API
# - POST /api/knowledge
# - payload : 요청 Body
# - model_dump() : Pydantic 객체를 dict 변환
# - repo.create() : 저장 처리
# - 생성된 지식 반환
# - HTTP 201 반환
@app.post("/api/knowledge", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    return repo.create(payload.model_dump())

# 직접 실행 시 개발 서버 구동
# - main:app 애플리케이션 실행
# - 127.0.0.1:18080 포트 사용
# - reload=True : 파일 변경 시 자동 재시작
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=18080, reload=True)

"""
본 프로젝트에서는 FastAPI 기반의 Knowledge API를 구현하여 지식 데이터의 조회(Read)와 생성(Create) 기능을 제공하였다.
Pydantic을 활용한 입력 검증, 파일 기반 영속 저장, Lock을 이용한 동시성 제어를 적용하여 데이터 무결성을 보장하였다.
또한 API 계층과 데이터 처리 계층을 분리하여 유지보수성과 확장성을 향상시켰으며, 이를 통해 REST API 설계와 계층 분리 구조의 중요성을 확인할 수 있었다.
"""