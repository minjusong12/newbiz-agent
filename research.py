import streamlit as st
import openai
import ssl
import os
import httpx

# ✅ Streamlit Cloud용: Secrets에서 API 키 가져오기
api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=api_key)

# 인증서 무시 (일부 환경 대응)
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['CURL_CA_BUNDLE'] = ''

def run_deep_research(topic: str) -> dict:
    """
    GPT 기반 심층 리서치 수행
    입력: 주제 (예: '일본 장례 플랫폼 시장')
    출력: 정성적/정량적 분석을 담은 구조화된 딕셔너리
    """
    system_prompt = """
    당신은 신사업 전략 컨설턴트입니다. 사용자가 제공한 주제에 대해 신사업 제안서를 작성할 수 있도록
    정성적·정량적 관점에서 심층 리서치를 수행하세요.

    다음 두 범주로 정보를 정리해주세요:

    1. 📘 정성적 인사이트 (Qualitative Insight)
    - 산업 구조 및 밸류체인
    - 최근 3~5년간 시장 트렌드 및 변화 요인
    - 해당 시장의 대표 기업 3개 중심의 전략, BM, 고객, 기술 분석
    - 소비자 인식과 문화적 특수성
    - 제도/법률/정책 이슈
    - 경쟁 강도 및 진입장벽 요인
    - 향후 변화 가능성 (기술, 사회 등)

    2. 📊 정량적 데이터 (Quantitative Insight)
    - 연간 시장 규모 (건수 / 금액)
    - 대표 기업별 시장 점유율 (가능 시)
    - 평균 단가 / 건당 원가 / 마진율
    - 연평균 성장률(CAGR)
    - 고정비/단가 기반 BEP 계산 요소
    - 점유율 기반 보수/기본/낙관 수익 시나리오

    모든 데이터를 가능한 수치로 표현하고, 추정 데이터라도 근거 기반으로 제시하세요.
    구조화된 JSON으로 요약 정리해주세요.
    """

    user_prompt = f"주제: {topic}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5
    )

    output = response.choices[0].message.content
    return {"raw_text": output}
