"""HTTP와 저장 책임을 구분하는 지식 관리 API입니다."""
from fastapi import FastAPI, HTTPException, Response

# FastAPI 애플리케이션 생성
# - title="Knowledge API" : OpenAPI 문서에 표시될 서비스 이름
# - app : API 엔드포인트를 등록하는 FastAPI 객체
app = FastAPI(title="Knowledge API")
"""FastAPI 기반의 지식 관리 서비스가 정상적으로 요청을 처리할 수 있는지 확인하기 위한 Health Check API를 제공하는 코드"""

# 서비스 상태 확인(Health Check) API
# - 경로 : GET /health
# - 반환 타입 : dict[str, str]
# - 서버 프로세스가 정상적으로 요청을 처리할 수 있는지 확인
# - 파일·DB·AI 모델의 세부 상태는 검사하지 않음
@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    # BEGIN H01-01
    # TODO H01-01: status=ok인 dict를 반환하는 health를 완성하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    # raise NotImplementedError("H01-01를 먼저 완성하세요.")

    # 상태 확인 결과 반환
    # - "status" : 상태 정보 키
    # - "ok" : 정상 응답을 의미하는 상태 값
    # - 반환값(dict) : JSON 형태로 자동 변환되어 응답
    return {"status" : "ok"}
    # END H01-01

    """
    /health 엔드포인트를 구현하여 서버의 기본 동작 여부를 확인할 수 있도록 하였으며,
    요청 시 {"status":"ok"}를 반환함으로써 애플리케이션이 정상적으로 실행 중임을 검증하였다.
    해당 API는 서비스 가용성 확인을 위한 최소한의 상태 점검 기능을 수행한다.
    """
