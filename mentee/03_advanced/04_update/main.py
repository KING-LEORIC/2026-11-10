"""HTTP와 저장 책임을 구분하는 지식 관리 API입니다."""
from fastapi import FastAPI, HTTPException, Response
import logic as repo
from schemas import Knowledge, KnowledgeWrite

# FastAPI 애플리케이션 생성
# - API 라우터 등록 대상
# - 제목 설정
app = FastAPI(title="Knowledge API")

# 서버 상태 확인
# - 서비스 응답 여부 확인
# - 단순 health check
@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    return {"status": "ok"}

# 지식 목록 조회
# - category가 없으면 전체 조회
# - category가 있으면 필터 조회
@app.get("/api/knowledge")
def list_knowledge(category: str | None = None):
    return repo.list_entries(category)

# 단건 조회
# - knowledge_id로 조회
# - 없으면 404 반환
@app.get("/api/knowledge/{knowledge_id}")
def get_knowledge(knowledge_id: int):
    entry = repo.find_entry(knowledge_id)
    if entry is None:
        raise HTTPException(404, "Knowledge not found")
    return entry

# 지식 생성
# - 요청 Body 검증
# - 저장 후 생성 데이터 반환
@app.post("/api/knowledge", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    return repo.create(payload.model_dump())

# 지식 수정
# - knowledge_id 대상 수정
# - 존재하지 않으면 404 반환
# - 수정 결과 반환
@app.put("/api/knowledge/{knowledge_id}", response_model=Knowledge)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite):
    updated = repo.update(knowledge_id, payload.model_dump())
    # BEGIN H04-03
    # TODO H04-03: 데이터 함수가 None을 반환하면 Router에서 404를 보내세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    # raise NotImplementedError("H04-03를 먼저 완성하세요.")

    # 수정 대상 존재 여부 확인
    # - None이면 데이터 없음
    # - Router 계층에서 404 응답
    if updated is None:
        raise HTTPException(404, "Knowledge not found")
    # END H04-03
    return updated

# 직접 실행 시 개발 서버 구동
# - main:app 애플리케이션 실행
# - 127.0.0.1:18080 포트 사용
# - reload=True : 파일 변경 시 자동 재시작
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=18080, reload=True)