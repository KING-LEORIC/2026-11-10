from pydantic import BaseModel, Field

# 입력 모델은 HTTP Body의 규칙입니다. DB 테이블이나 저장 코드가 아닙니다.
# 지식 생성/수정 요청 모델
# - title : 지식 제목
# - content : 지식 내용
# - category : 분류명
# - HTTP Body 검증용 모델
class KnowledgeWrite(BaseModel):
    # 지식 제목
    # - 최소 1자
    # - 최대 80자
    title: str = Field(min_length=1, max_length=80)
    # 지식 내용
    # - 최소 1자
    # - 최대 2000자
    content: str = Field(min_length=1, max_length=2000)
    # 지식 카테고리
    # - 최소 1자
    # - 최대 30자
    category: str = Field(min_length=1, max_length=30)

# 응답 모델
# - KnowledgeWrite 필드 상속
# - id 필드 추가
class Knowledge(KnowledgeWrite):
    # 지식 고유 ID
    id: int
