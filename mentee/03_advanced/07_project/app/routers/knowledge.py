"""HTTP 경로·입력·응답. 저장 구현은 repository에 위임합니다."""
# FastAPI 라우터 및 예외 처리 객체 사용
# - APIRouter : URL 그룹 생성
# - HTTPException : HTTP 오류 응답
# - Response : 사용자 정의 응답 반환
from fastapi import APIRouter, HTTPException, Response
# 요청/응답 데이터 검증 모델
# - Knowledge : 응답 스키마
# - KnowledgeWrite : 입력 스키마
from schemas import Knowledge, KnowledgeWrite
# 저장소(Repository) 계층 import
# - 실제 CRUD 작업 담당
from repositories import json_knowledge as repo

"""HTTP 요청을 받아 적절한 Repository 함수를 호출하고, 입력 검증 및 HTTP 응답 처리를 담당하는 Router 계층"""
# Knowledge 관련 API 그룹 생성
# - prefix : 공통 URL
# - tags : Swagger 문서 분류
router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

# 지식 데이터 목록 조회 API
# - category 지정 시 조건 조회
# - 미지정 시 전체 조회
# - 반환 타입 : list[Knowledge]
@router.get("", response_model=list[Knowledge])
def list_knowledge(category: str | None = None):
    # Repository에 조회 위임
    # - category 조건 전달
    return repo.list_entries(category)

# 특정 ID의 지식 데이터 조회 API
# - knowledge_id : URL 경로 변수
# - 성공 시 Knowledge 반환
@router.get("/{knowledge_id}", response_model=Knowledge)
def get_knowledge(knowledge_id: int):
    # Repository에서 데이터 조회
    # - 없으면 None 반환
    entry = repo.find_entry(knowledge_id)
    # 조회 결과가 없는 경우
    # - HTTP 404 반환
    if entry is None:
        raise HTTPException(404, "Knowledge not found")
    return entry

# 신규 지식 데이터 생성 API
# - payload : 요청 Body
# - 201 Created 반환
# - 반환 타입 : Knowledge
@router.post("", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    # Pydantic 모델을 dict로 변환
    # - model_dump() 사용
    return repo.create(payload.model_dump())

# 기존 지식 데이터 수정 API
# - knowledge_id : 수정 대상 ID
# - payload : 수정 내용
# - 반환 타입 : Knowledge
@router.put("/{knowledge_id}", response_model=Knowledge)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite):
    # Repository 수정 수행
    # - 성공 시 수정 데이터 반환
    # - 실패 시 None 반환
    updated = repo.update(knowledge_id, payload.model_dump())
    # 수정 대상이 없는 경우
    # - HTTP 404 반환
    if updated is None:
        raise HTTPException(404, "Knowledge not found")
    return updated

# 지식 데이터 삭제 API
# - knowledge_id : 삭제 대상 ID
# - 성공 시 HTTP 204 반환
@router.delete("/{knowledge_id}", status_code=204)
def delete_knowledge(knowledge_id: int):
    # Repository 삭제 요청
    # - True : 삭제 성공
    # - False : 삭제 실패
    deleted = repo.delete(knowledge_id)
    # 삭제 대상이 없는 경우
    # - HTTP 404 반환
    if not deleted:
        raise HTTPException(404, "Knowledge not found")
    # BEGIN H07-02
    # TODO H07-02: Repository 삭제가 성공한 경우 빈 204 응답을 반환하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    # raise NotImplementedError("H07-02를 먼저 완성하세요.")

    # 본문 없는 성공 응답 반환
    # - HTTP 204 No Content
    # - 삭제 성공을 의미
    return Response(status_code=204)
    # END H07-02

"""
Router 계층은 데이터 저장 방식과 분리되어 HTTP 요청 처리에만 집중하도록 구현하였다.
이를 통해 URL 라우팅, 입력 검증, 예외 처리의 책임을 분리하여 코드의 유지보수성과 확장성을 향상시켰다.
"""