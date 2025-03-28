def generate_slide_outline(topic: str, report_text: str) -> list:
    """
    보고서 텍스트를 기반으로 슬라이드 제목, 요약, 시각자료 제안을 구조화
    """
    slide_structure = [
        ("사업 개요", ['사업 제안', 'GPT 기반', '개요']),
        ("산업 및 시장 분석", ['산업 구조', '시장 규모', '트렌드']),
        ("경쟁사 벤치마킹", ['대표 기업', '전략', '벤치마킹']),
        ("고객 및 수요 분석", ['소비자', '고객', '문화']),
        ("수익 모델 및 BEP 분석", ['단가', '마진', '수익', '시장 규모']),
        ("전략 제안 및 실행 방안", ['전략', '실행', '기회']),
        ("결론 및 기대효과", ['기대효과', '요약', '종합']),
    ]

    slides = []

    for title, keywords in slide_structure:
        summary = extract_slide_content(report_text, keywords)
        slides.append({
            "title": title,
            "summary": summary,
            "visual_suggestion": suggest_visual(title)
        })

    return slides


def extract_slide_content(text: str, keywords: list) -> str:
    """
    텍스트에서 키워드가 포함된 문장들을 추출하여 요약문을 구성
    """
    lines = text.split('\n')
    summary_lines = []
    for line in lines:
        if any(k in line for k in keywords):
            summary_lines.append(f"- {line.strip()}")
    return '\n'.join(summary_lines[:5])  # 각 슬라이드당 최대 5줄


def suggest_visual(title: str) -> str:
    """
    슬라이드 제목에 따라 추천 시각자료 형태 제안
    """
    suggestions = {
        "산업 및 시장 분석": "시장 크기 막대 그래프 / 트렌드 타임라인",
        "경쟁사 벤치마킹": "경쟁사 비교 테이블 / SWOT 차트",
        "수익 모델 및 BEP 분석": "BEP 손익분기 그래프 / 마진구조 도넛차트",
        "전략 제안 및 실행 방안": "전략 로드맵 / 액션 플랜 도표",
        "결론 및 기대효과": "성과 기대 효과 아이콘 요약",
    }
    return suggestions.get(title, "텍스트 요약 중심 슬라이드")


# =====================
# ✅ 실행 예시
# =====================
if __name__ == "__main__":
    from generate_report import generate_business_report
    from research import run_deep_research

    topic = "일본 온라인 장례 플랫폼 시장"
    result = run_deep_research(topic)
    report_text = generate_business_report(topic, result["raw_text"])

    slide_outline = generate_slide_outline(topic, report_text)

    for slide in slide_outline:
        print(f"\n📄 슬라이드: {slide['title']}")
        print(slide["summary"])
        print(f"📊 추천 시각자료: {slide['visual_suggestion']}")
