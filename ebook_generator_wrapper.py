#!/usr/bin/env python3
"""
전자책 생성 래퍼 스크립트
웹 서버에서 호출하기 위한 간단한 인터페이스
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# 기존 ebook_generator 모듈의 모든 클래스와 함수를 import
from ebook_generator import (
    KnowledgeBaseReader,
    AIConsultingTeam,
    HTMLGenerator,
    MarkdownGenerator,
    KNOWLEDGE_BASE_PATH,
    GUIDELINE_PATH,
    DESIGN_TEMPLATE_PATH,
    OUTPUT_HTML_PATH,
    OBSIDIAN_VAULT_PATH,
    client
)


def generate_ebook_api(folder_name: str, topic: str, theme: str = 'dark', model: str = 'claude') -> dict:
    """
    API용 전자책 생성 함수

    Args:
        folder_name: 지식 베이스 폴더명
        topic: 전자책 주제
        theme: 디자인 테마 (dark, colorful)
        model: AI 모델 (claude, gemini)

    Returns:
        dict: 생성 결과 정보
    """
    try:
        # 출력 경로 설정
        output_html_path = Path(OUTPUT_HTML_PATH)
        output_html_path.mkdir(parents=True, exist_ok=True)

        obsidian_output_path = Path(OBSIDIAN_VAULT_PATH) / "Auto News letter" / "News Completion"
        obsidian_output_path.mkdir(parents=True, exist_ok=True)

        # 1단계: 지식 베이스 구축
        kb_reader = KnowledgeBaseReader(KNOWLEDGE_BASE_PATH)
        knowledge = kb_reader.aggregate_knowledge(folder_name)

        # 2단계: AI 경영자문팀 - 구조 기획
        ai_team = AIConsultingTeam(client, GUIDELINE_PATH, model_type=model)
        structure = ai_team.generate_structure(topic, knowledge)

        # 3단계: 각 소주제별 콘텐츠 생성
        subtopics_content = []
        experts = ["세무사", "노무사", "회계사", "AI컨설턴트", "세무사"]

        for idx, subtopic in enumerate(structure['subtopics']):
            expert = experts[idx % len(experts)]

            content = ai_team.write_subtopic(
                main_topic=structure['main_topic'],
                subtopic=subtopic,
                knowledge=knowledge,
                expert_role=expert
            )

            subtopics_content.append({
                'title': subtopic['title'],
                'content': content,
                'expert': expert
            })

        # 4단계: HTML 생성
        html_gen = HTMLGenerator(DESIGN_TEMPLATE_PATH, theme=theme)
        html_output = html_gen.generate(
            main_topic=structure['main_topic'],
            subtopics_content=subtopics_content,
            metadata={
                "date": datetime.now().strftime("%Y년 %m월 %d일"),
                "author": "엘비즈 파트너스 이상수"
            }
        )

        # 5단계: 마크다운 생성
        md_gen = MarkdownGenerator()
        md_output = md_gen.generate(
            main_topic=structure['main_topic'],
            subtopics_content=subtopics_content,
            metadata={
                "date": datetime.now().strftime("%Y-%m-%d"),
                "author": "엘비즈 파트너스 이상수"
            }
        )

        # 6단계: 저장
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '_')).strip()
        safe_topic = safe_topic.replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # HTML 저장
        html_filename = f"{safe_topic}_{timestamp}.html"
        html_path = output_html_path / html_filename
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_output)

        # 마크다운 저장
        md_filename = f"{safe_topic}_{timestamp}.md"
        md_path = obsidian_output_path / md_filename
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_output)

        return {
            'success': True,
            'htmlPath': str(html_path),
            'mdPath': str(md_path),
            'filename': html_filename
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def main():
    """CLI 인터페이스"""
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        result = {
            "success": False,
            "error": "Usage: python ebook_generator_wrapper.py <folder_name> <topic> [theme] [model]"
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    folder_name = sys.argv[1]
    topic = sys.argv[2]
    theme = sys.argv[3] if len(sys.argv) >= 4 else 'dark'
    model = sys.argv[4] if len(sys.argv) == 5 else 'claude'

    result = generate_ebook_api(folder_name, topic, theme, model)
    print(json.dumps(result, ensure_ascii=False))

    if not result['success']:
        sys.exit(1)


if __name__ == "__main__":
    main()
