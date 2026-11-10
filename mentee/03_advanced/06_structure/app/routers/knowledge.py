"""HTTP 경로·입력·응답. 저장 구현은 repository에 위임합니다."""
from fastapi import APIRouter, HTTPException, Response
from app.schemas import Knowledge, KnowledgeWrite
from app.repositories import json_knowledge as repo

# Knowledge API Router 생성
# - prefix : 모든 경로 앞에 /api/knowledge 부여
# - tags : Swagger 문서 그룹명
router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

# 지식 목록 조회 API
# - GET /api/knowledge
# - category 쿼리 파라미터 지원
# - Repository에서 목록 반환
@router.get("", response_model=list[Knowledge])
def list_knowledge(category: str | None = None):
    return repo.list_entries(category)

# 단일 지식 조회 API
# - GET /api/knowledge/{id}
# - ID 존재 시 데이터 반환
# - 없으면 404 예외 발생
@router.get("/{knowledge_id}", response_model=Knowledge)
def get_knowledge(knowledge_id: int):
    entry = repo.find_entry(knowledge_id)
    if entry is None:
        raise HTTPException(404, "Knowledge not found")
    return entry

# 지식 생성 API
# - POST /api/knowledge
# - 검증된 Body를 Repository에 전달
# - 생성 결과 반환
@router.post("", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    # BEGIN H06-03
    # TODO H06-03: 검증된 payload를 dict로 바꾸어 repo.create에 전달하고 결과를 반환하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    # raise NotImplementedError("H06-03를 먼저 완성하세요.")

    # Pydantic 객체를 dict로 변환
    # - payload.model_dump()
    # - Repository create()에 전달
    # - 생성된 데이터 반환
    return repo.create(payload.model_dump())
    # END H06-03

# 지식 수정 API
# - PUT /api/knowledge/{id}
# - 존재 시 수정 결과 반환
# - 없으면 404 예외 발생
@router.put("/{knowledge_id}", response_model=Knowledge)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite):
    updated = repo.update(knowledge_id, payload.model_dump())
    if updated is None:
        raise HTTPException(404, "Knowledge not found")
    return updated

# 지식 삭제 API
# - DELETE /api/knowledge/{id}
# - 삭제 성공 시 204 반환
# - 없으면 404 예외 발생
@router.delete("/{knowledge_id}", status_code=204)
def delete_knowledge(knowledge_id: int):
    deleted = repo.delete(knowledge_id)
    if not deleted:
        raise HTTPException(404, "Knowledge not found")
    return Response(status_code=204)

