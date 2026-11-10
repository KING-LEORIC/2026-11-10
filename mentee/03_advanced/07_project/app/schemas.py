# Pydantic 데이터 검증 모델 사용
# - BaseModel : 스키마 정의
# - Field : 필드 제약조건 지정
from pydantic import BaseModel, Field

"""API 요청과 응답 데이터의 형식을 정의하고 입력값을 검증하는 Pydantic 스키마 제공"""
# 입력 모델은 HTTP Body의 규칙입니다. DB 테이블이나 저장 코드가 아닙니다.
# 지식 생성/수정 요청 데이터 모델
# - 클라이언트 입력 검증 담당
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

# 응답용 데이터 모델
# - KnowledgeWrite 상속
# - 고유 ID 추가
class Knowledge(KnowledgeWrite):
    # 지식 식별자
    # - Repository에서 자동 생성
    id: int

"""
Pydantic 스키마를 활용하여 입력 데이터의 유효성을 자동 검증하고, API 요청과 응답 형식을 일관성 있게 유지하도록 구현하였다.
"""