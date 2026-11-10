"""HTTP와 저장 책임을 구분하는 지식 관리 API입니다."""
from fastapi import FastAPI, HTTPException, Response
import logic as repo
from schemas import Knowledge, KnowledgeWrite

# FastAPI 애플리케이션 생성
# - title : Swagger/OpenAPI 문서 제목
app = FastAPI(title="Knowledge API")
"""JSON 파일을 저장소로 사용하는 CRUD 기반 지식(Knowledge) 관리 REST API를 FastAPI로 구현"""
# 서버 상태 확인 API
# - 서버 실행 여부 확인
# - {"status":"ok"} 반환
@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    return {"status": "ok"}

# 지식 목록 조회 API
# - category 미지정 : 전체 조회
# - category 지정 : 카테고리 필터 조회
# - repo.list_entries() 호출
@app.get("/api/knowledge")
def list_knowledge(category: str | None = None):
    return repo.list_entries(category)

# 지식 단건 조회 API
# - knowledge_id : 조회 대상 ID
# - 존재하지 않으면 HTTP 404 반환
@app.get("/api/knowledge/{knowledge_id}")
def get_knowledge(knowledge_id: int):
    entry = repo.find_entry(knowledge_id)
    if entry is None:
        raise HTTPException(404, "Knowledge not found")
    return entry

# 지식 생성 API
# - payload : 요청 Body
# - KnowledgeWrite 모델로 검증
# - 생성 성공 시 201 반환
@app.post("/api/knowledge", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    return repo.create(payload.model_dump())

# 지식 수정 API
# - knowledge_id : 수정 대상 ID
# - payload : 수정 데이터
# - 수정 실패 시 404 반환
@app.put("/api/knowledge/{knowledge_id}", response_model=Knowledge)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite):
    updated = repo.update(knowledge_id, payload.model_dump())
    if updated is None:
        raise HTTPException(404, "Knowledge not found")
    return updated

# 지식 삭제 API
# - knowledge_id : 삭제 대상 ID
# - 삭제 실패 시 404 반환
# - 삭제 성공 시 204 No Content 반환
@app.delete("/api/knowledge/{knowledge_id}", status_code=204)
def delete_knowledge(knowledge_id: int):
    deleted = repo.delete(knowledge_id)
    if not deleted:
        raise HTTPException(404, "Knowledge not found")
    # BEGIN H05-02
    # TODO H05-02: 삭제 성공 시 본문 없는 204를 반환하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    # raise NotImplementedError("H05-02를 먼저 완성하세요.")
    return Response(status_code=204)
    # END H05-02

# 직접 실행 시 개발 서버 구동
# - main:app 애플리케이션 실행
# - 127.0.0.1:18080 포트 사용
# - reload=True : 파일 변경 시 자동 재시작
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=18080, reload=True)

"""
본 프로젝트에서는 FastAPI 기반의 Knowledge API를 구현하여 지식 데이터의 생성(Create), 조회(Read), 수정(Update), 삭제(Delete) 기능을 제공하였다.
HTTP 계층과 데이터 처리 계층을 분리하여 유지보수성을 높였으며, Pydantic을 이용한 입력 검증과 HTTP 상태 코드를 적용하여 RESTful API 원칙을 준수하였다.
또한 파일 저장 시 Lock과 임시 파일 교체 방식을 사용하여 데이터 무결성을 확보하였다. 이를 통해 간단한 파일 기반 데이터 관리 시스템을 안정적으로 구현할 수 있음을 확인하였다.
"""