from pydantic import BaseModel, Field

# 입력 모델은 HTTP Body의 규칙입니다. DB 테이블이나 저장 코드가 아닙니다.
# 지식 생성 요청 모델
# - title : 지식 제목
# - content : 지식 내용
# - category : 지식 분류
# - Field() : 입력 길이 검증 수행
class KnowledgeWrite(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=2000)
    category: str = Field(min_length=1, max_length=30)

# 지식 응답 모델
# - KnowledgeWrite 상속
# - id : 저장된 지식 식별자
# - API 응답 스키마 정의
class Knowledge(KnowledgeWrite):
    id: int
