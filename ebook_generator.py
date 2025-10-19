#!/usr/bin/env python3
"""
전자책 자동 생성 시스템 (비즈니스 전문가 버전)
AI 경영자문팀을 활용한 맞춤형 전자책 생성
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import anthropic
import google.generativeai as genai
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 설정
KNOWLEDGE_BASE_PATH = "/Users/isangsu/TMP_MY/knowledge.biz"
GUIDELINE_PATH = "/Users/isangsu/TMP_MY/J-project/전자책_Auto-Agent_지침_비즈니스버전.md"
DESIGN_TEMPLATE_PATH = "/Users/isangsu/TMP_MY/J-project/templates/newsletter_template.html"
OUTPUT_HTML_PATH = "/Users/isangsu/TMP_MY/J-project/output/generated_ebooks"
OBSIDIAN_VAULT_PATH = "/Users/isangsu/Documents/Obsidian/Obsi/Vault.01"

# Claude API 초기화
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Gemini API 초기화
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


class KnowledgeBaseReader:
    """지식 베이스 읽기 및 집계"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def read_folder(self, folder_name: str) -> Dict[str, str]:
        """특정 폴더의 모든 파일 읽기"""
        folder_path = self.base_path / folder_name

        if not folder_path.exists():
            raise FileNotFoundError(f"폴더를 찾을 수 없습니다: {folder_path}")

        files_content = {}

        # 지원하는 파일 형식
        supported_extensions = ['.md', '.txt']

        for file_path in folder_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in supported_extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        relative_path = file_path.relative_to(folder_path)
                        files_content[str(relative_path)] = content
                except Exception as e:
                    print(f"파일 읽기 오류 ({file_path}): {e}")

        return files_content

    def aggregate_knowledge(self, folder_name: str) -> str:
        """지식베이스 집계 및 요약"""
        files_content = self.read_folder(folder_name)

        if not files_content:
            return "지식베이스가 비어있습니다."

        # 파일 내용 집계
        aggregated = f"## 지식베이스: {folder_name}\n\n"
        aggregated += f"총 파일 수: {len(files_content)}개\n\n"

        for filename, content in files_content.items():
            aggregated += f"### 파일: {filename}\n\n"
            aggregated += content + "\n\n"
            aggregated += "---\n\n"

        return aggregated


class AIConsultingTeam:
    """AI 경영자문팀 워크플로우"""

    def __init__(self, client, guideline_path: str, model_type: str = 'claude'):
        self.client = client
        self.model_type = model_type  # 'claude' or 'gemini'
        self.guideline = self._load_guideline(guideline_path)

        # Gemini 모델 초기화
        if model_type == 'gemini':
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def _load_guideline(self, path: str) -> str:
        """가이드라인 로드"""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def generate_structure(self, topic: str, knowledge: str) -> Dict[str, any]:
        """
        5가지 소주제 구조 생성
        PM이 전체 구조를 기획
        """
        system_prompt = f"""당신은 전문 프로젝트 매니저입니다.

{self.guideline}

위 가이드라인을 따라, 주어진 주제와 지식베이스를 바탕으로 5가지 소주제(H2)를 구성하세요.

중요:
1. 팩트체크: 모든 정보는 국세청, 고용노동부 등 공신력 있는 출처에서 검증
2. 전문용어 풀이: 일반인이 이해할 수 있도록 쉽게 설명
3. 전체 흐름이 자연스럽게 연결되도록 구성
4. 각 소주제는 독립적이면서도 주제(H1)와 연결

응답 형식 (JSON):
{{
    "main_topic": "주제 제목",
    "subtopics": [
        {{
            "title": "소주제 1",
            "description": "소주제 설명",
            "target_length": 2000
        }},
        ...
    ],
    "overall_structure": "전체 구조 설명"
}}
"""

        user_message = f"""## 주제(H1)
{topic}

## 지식베이스
{knowledge[:8000]}  # API 제한 고려하여 일부만 전달

위 지식베이스를 바탕으로 '{topic}'에 대한 5가지 소주제를 구성해주세요."""

        # 모델에 따라 API 호출
        if self.model_type == 'gemini':
            # Gemini API 호출
            full_prompt = f"{system_prompt}\n\n{user_message}"
            response = self.gemini_model.generate_content(full_prompt)
            content = response.text
        else:
            # Claude API 호출
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            content = response.content[0].text

        # JSON 추출 (코드 블록 및 추가 텍스트 제거)
        if "```json" in content:
            # ```json 블록에서 JSON만 추출
            json_start = content.find("```json") + 7
            json_end = content.find("```", json_start)
            content = content[json_start:json_end].strip()
        elif "```" in content:
            # 일반 코드 블록에서 추출
            json_start = content.find("```") + 3
            json_end = content.find("```", json_start)
            content = content[json_start:json_end].strip()
        else:
            # 코드 블록이 없으면 전체 응답 사용
            content = content.strip()

        # JSON 객체만 추출 (추가 텍스트 제거)
        # 텍스트 중간에 있는 { 부터 } 까지 추출
        json_start_pos = content.find('{')
        if json_start_pos != -1:
            # { 위치부터 중괄호 카운팅 시작
            brace_count = 0
            json_end = 0
            for i, char in enumerate(content[json_start_pos:], start=json_start_pos):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break

            if json_end > json_start_pos:
                content = content[json_start_pos:json_end]

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            import sys
            print(f"[ERROR] JSON 파싱 실패: {e}", file=sys.stderr)
            print(f"[ERROR] 파싱 시도한 내용 (처음 500자): {content[:500]}", file=sys.stderr)
            print(f"[ERROR] 파싱 시도한 내용 (끝 500자): {content[-500:]}", file=sys.stderr)
            raise

    def write_subtopic(self,
                      main_topic: str,
                      subtopic: Dict[str, str],
                      knowledge: str,
                      expert_role: str) -> str:
        """
        각 소주제별로 전문가가 글 작성
        expert_role: "세무사", "노무사", "회계사", "AI컨설턴트"
        """
        role_prompts = {
            "세무사": "세무/회계 전문가로서, 국세청과 기획재정부 공식 자료를 기반으로",
            "노무사": "노무 전문가로서, 고용노동부와 근로기준법을 기반으로",
            "회계사": "회계 전문가로서, 금융감독원과 한국회계기준원 공식 자료를 기반으로",
            "AI컨설턴트": "AI 활용 전문가로서, 최신 AI 기술과 도구를 기반으로"
        }

        system_prompt = f"""당신은 {expert_role}입니다.

{self.guideline}

위 가이드라인을 엄격히 따라 글을 작성하세요.

필수 준수 사항:
1. 팩트체크: {role_prompts.get(expert_role, "")} 검증된 정보만 사용
2. 전문용어 풀이: 모든 전문 용어는 3단계 구조로 설명
   - 전문 용어 제시
   - 쉬운 풀이 (초등학생도 이해 가능)
   - 실제 사례 (구체적 숫자와 상황)
3. 글 길이: 약 2000자 (한국어 기준)
4. 구조: H3 제목으로 시작, 본문, 필요시 콘텐츠 박스 활용
5. 출처 표기: 중요 정보는 "(출처: XX부, YYYY년 MM월 기준)" 형식으로 표기

콘텐츠 박스 활용:
- [세금정보💰]: 세금 관련 핵심 정보
- [용어풀이📖]: 전문 용어 설명
- [꿀팁💡]: 실용적인 팁
- [체크리스트✓]: 확인사항 목록
- [AI도구🤖]: AI 활용 방법
"""

        user_message = f"""## 메인 주제
{main_topic}

## 소주제
{subtopic['title']}

## 소주제 설명
{subtopic['description']}

## 참고할 지식베이스
{knowledge[:6000]}

위 내용을 바탕으로 약 2000자 분량의 글을 작성해주세요.
반드시 가이드라인의 팩트체크와 용어 풀이 규칙을 준수하세요."""

        # 모델에 따라 API 호출
        if self.model_type == 'gemini':
            # Gemini API 호출
            full_prompt = f"{system_prompt}\n\n{user_message}"
            response = self.gemini_model.generate_content(full_prompt)
            return response.text
        else:
            # Claude API 호출
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=3000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            return response.content[0].text


class HTMLGenerator:
    """HTML 생성 엔진"""

    def __init__(self, template_path: str, theme: str = 'dark'):
        self.theme = theme
        self.template = self._load_template(template_path, theme)

    def _load_template(self, base_path: str, theme: str) -> str:
        """테마에 따라 템플릿 로드"""
        from pathlib import Path

        # 템플릿 디렉토리 경로
        template_dir = Path(base_path).parent

        # 테마별 템플릿 파일명
        theme_templates = {
            'dark': 'dark_template.html',
            'light': 'light_template.html',
            'colorful': 'colorful_template.html'
        }

        # 테마 파일 경로
        template_file = theme_templates.get(theme, 'dark_template.html')
        template_path = template_dir / template_file

        # 파일이 없으면 기본 dark 템플릿 사용
        if not template_path.exists():
            template_path = template_dir / 'dark_template.html'
            if not template_path.exists():
                # dark_template.html도 없으면 newsletter_template.html 사용
                template_path = template_dir / 'newsletter_template.html'

        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()

    def generate(self,
                main_topic: str,
                subtopics_content: List[Dict[str, str]],
                metadata: Dict[str, str]) -> str:
        """
        HTML 생성
        새로운 비즈니스 전문가 템플릿 활용
        """
        html = self.template

        # 메타데이터 교체
        html = html.replace("{{TITLE}}", main_topic)
        html = html.replace("{{DATE}}", metadata.get("date", datetime.now().strftime("%Y년 %m월 %d일")))
        html = html.replace("{{AUTHOR}}", metadata.get("author", "AI 경영자문팀"))

        # 목차 아이템 생성
        toc_items_html = ""
        for idx, item in enumerate(subtopics_content, 1):
            toc_items_html += f'''
                <a href="#section{idx}" class="toc-item fade-in">
                    <h3>{idx}. {item['title']}</h3>
                    <p>{item.get('description', '이 섹션에서는 관련 내용을 깊이 있게 다룹니다.')}</p>
                </a>
            '''
        html = html.replace("{{TOC_ITEMS}}", toc_items_html)

        # 본문 섹션들 생성
        sections_html = ""
        for idx, item in enumerate(subtopics_content, 1):
            section_content = self._convert_markdown_to_html(item['content'])
            sections_html += f'''
    <section id="section{idx}" class="content-section fade-in">
        <div class="section-header">
            <div class="container">
                <h2>{idx}. {item['title']}</h2>
                <p class="section-intro">{item.get('description', '이 섹션의 핵심 내용을 다룹니다.')}</p>
            </div>
        </div>
        <div class="section-content">
            <div class="container">
                {section_content}
            </div>
        </div>
    </section>
            '''
        html = html.replace("{{CONTENT_SECTIONS}}", sections_html)

        # 요약 내용 생성
        summary_html = "<p>이 전자책에서 다룬 핵심 내용을 요약합니다:</p><ul>"
        for idx, item in enumerate(subtopics_content, 1):
            summary_html += f"<li><strong>{item['title']}</strong>: 주요 포인트를 정리합니다.</li>"
        summary_html += "</ul>"
        html = html.replace("{{SUMMARY_CONTENT}}", summary_html)

        # 핵심 원칙 생성
        principles_html = f'''
            <div class="principle-card">
                <h3>법규 준수</h3>
                <p>모든 세무/노무/회계 처리는 현행 법규를 철저히 준수해야 합니다.</p>
            </div>
            <div class="principle-card">
                <h3>증빙 관리</h3>
                <p>세금계산서, 현금영수증 등 모든 증빙을 체계적으로 관리하세요.</p>
            </div>
            <div class="principle-card">
                <h3>전문가 상담</h3>
                <p>복잡한 사안은 반드시 세무사, 노무사 등 전문가와 상담하세요.</p>
            </div>
        '''
        html = html.replace("{{KEY_PRINCIPLES}}", principles_html)

        return html

    def _convert_markdown_to_html(self, markdown: str) -> str:
        """마크다운을 HTML로 변환 (개선된 버전)"""
        import re
        html = markdown

        # 코드 블록 제거 (```로 감싸진 부분을 특수 박스로 변환)
        def convert_code_block(match):
            content = match.group(1).strip()
            # 리스트 형식이면 ul로 변환
            if '\n-' in content or '\n*' in content:
                lines = content.split('\n')
                list_html = '<ul class="box-list">'
                for line in lines:
                    line = line.strip()
                    if line.startswith('-') or line.startswith('*'):
                        list_html += f'<li>{line[1:].strip()}</li>'
                    elif line and not line.startswith('(출처'):
                        list_html += f'<li>{line}</li>'
                list_html += '</ul>'
                # 출처 정보 추가
                for line in lines:
                    if line.strip().startswith('(출처'):
                        list_html += f'<p class="source">{line.strip()}</p>'
                return list_html
            else:
                # 일반 텍스트
                return f'<div class="info-content">{content}</div>'

        html = re.sub(r'```(.*?)```', convert_code_block, html, flags=re.DOTALL)

        # 특수 박스 변환 (``` 없이 마커만 있는 경우)
        # [세금정보💰] 다음 내용을 박스로 변환
        def convert_special_box(match):
            box_type = match.group(1)

            box_classes = {
                '세금정보💰': 'tax-info',
                '용어풀이📖': 'term-box',
                '실무팁💡': 'j-tip',
                'AI도구🤖': 'ai-tool',
                '체크리스트✓': 'checklist'
            }

            box_titles = {
                '세금정보💰': '💰 세금정보',
                '용어풀이📖': '📖 용어풀이',
                '실무팁💡': '💡 실무 팁',
                'AI도구🤖': '🤖 AI 활용 도구',
                '체크리스트✓': '✓ 실행 체크리스트'
            }

            css_class = box_classes.get(box_type, 'info-box')
            title = box_titles.get(box_type, box_type)

            return f'<div class="{css_class}"><div class="{css_class}-title">{title}</div>'

        html = re.sub(r'\[([^\]]+)\]', convert_special_box, html)

        # H4 제목 변환 (####)
        html = re.sub(r'^####\s*(.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

        # H3 제목 변환 (###)
        html = re.sub(r'^###\s*(.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

        # H2 제목 변환 (##)
        html = re.sub(r'^##\s*(.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)

        # 단락 변환
        lines = html.split('\n')
        processed_lines = []
        in_box = False
        in_list = False

        for line in lines:
            line_stripped = line.strip()

            # 박스 시작/종료 감지
            if '<div class=' in line_stripped:
                in_box = True
                processed_lines.append(line)
            elif '</div>' in line_stripped:
                in_box = False
                processed_lines.append(line)
            # 리스트 감지
            elif '<ul' in line_stripped:
                in_list = True
                processed_lines.append(line)
            elif '</ul>' in line_stripped:
                in_list = False
                processed_lines.append(line)
            # 이미 HTML 태그가 있는 경우
            elif line_stripped.startswith('<'):
                processed_lines.append(line)
            # 빈 줄
            elif not line_stripped:
                processed_lines.append('')
            # 일반 텍스트 → <p> 태그로 변환 (박스 밖에서만)
            elif not in_box and not in_list:
                # 출처 정보는 특별 스타일
                if line_stripped.startswith('(출처'):
                    processed_lines.append(f'<p class="source">{line_stripped}</p>')
                else:
                    processed_lines.append(f'<p>{line_stripped}</p>')
            else:
                # 박스 안의 내용
                if line_stripped.startswith('-'):
                    processed_lines.append(f'<p class="box-item">{line_stripped[1:].strip()}</p>')
                else:
                    processed_lines.append(f'<p>{line_stripped}</p>')

        html = '\n'.join(processed_lines)

        # 연속된 빈 <p></p> 제거
        html = re.sub(r'<p>\s*</p>', '', html)

        return html


class MarkdownGenerator:
    """옵시디언 마크다운 생성"""

    def generate(self,
                main_topic: str,
                subtopics_content: List[Dict[str, str]],
                metadata: Dict[str, str]) -> str:
        """마크다운 생성"""
        md = "---\n"
        md += f"title: {main_topic}\n"
        md += f"created: {metadata.get('date', datetime.now().strftime('%Y-%m-%d'))}\n"
        md += f"updated: {datetime.now().strftime('%Y-%m-%d')}\n"
        md += f"author: {metadata.get('author', 'AI 경영자문팀')}\n"
        md += "tags:\n"
        md += "  - 전자책\n"
        md += "  - 비즈니스\n"
        md += "  - AI생성\n"
        md += "---\n\n"

        md += f"# {main_topic}\n\n"

        for item in subtopics_content:
            md += f"## {item['title']}\n\n"
            md += item['content']
            md += "\n\n"

        return md


def main():
    """메인 실행 함수"""
    print("="*60)
    print("전자책 자동 생성 시스템 (비즈니스 전문가 버전)")
    print("="*60)
    print()

    # 사용자 입력
    folder_name = input("지식베이스 폴더명을 입력하세요: ").strip()
    topic = input("주제(H1)를 입력하세요: ").strip()
    obsidian_output_path = input(f"옵시디언 저장 경로를 입력하세요 (기본값: {OBSIDIAN_VAULT_PATH}): ").strip()

    # 옵시디언 경로 설정
    if not obsidian_output_path:
        obsidian_output_path = OBSIDIAN_VAULT_PATH

    print()
    print("생성 시작...")
    print()

    try:
        # 1. 지식베이스 읽기
        print("📚 1단계: 지식베이스 읽기...")
        kb_reader = KnowledgeBaseReader(KNOWLEDGE_BASE_PATH)
        knowledge = kb_reader.aggregate_knowledge(folder_name)
        print(f"   ✓ {len(kb_reader.read_folder(folder_name))}개 파일 읽기 완료")
        print()

        # 2. AI 팀 구조 생성
        print("🤖 2단계: AI 경영자문팀 - 구조 기획...")
        ai_team = AIConsultingTeam(client, GUIDELINE_PATH)
        structure = ai_team.generate_structure(topic, knowledge)
        print(f"   ✓ 5가지 소주제 구성 완료")
        print()

        # 3. 각 소주제별 콘텐츠 생성
        print("✍️  3단계: 전문가별 콘텐츠 작성...")
        subtopics_content = []

        # 전문가 배정 (라운드 로빈)
        experts = ["세무사", "노무사", "회계사", "AI컨설턴트", "세무사"]

        for idx, subtopic in enumerate(structure['subtopics']):
            expert = experts[idx % len(experts)]
            print(f"   - {subtopic['title']} (담당: {expert})")

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

        print("   ✓ 전체 콘텐츠 작성 완료")
        print()

        # 4. HTML 생성
        print("🎨 4단계: HTML 생성...")
        html_gen = HTMLGenerator(DESIGN_TEMPLATE_PATH)
        html_output = html_gen.generate(
            main_topic=structure['main_topic'],
            subtopics_content=subtopics_content,
            metadata={
                "date": datetime.now().strftime("%Y년 %m월 %d일"),
                "author": "AI 경영자문팀"
            }
        )
        print("   ✓ HTML 생성 완료")
        print()

        # 5. 마크다운 생성
        print("📝 5단계: 옵시디언 마크다운 생성...")
        md_gen = MarkdownGenerator()
        md_output = md_gen.generate(
            main_topic=structure['main_topic'],
            subtopics_content=subtopics_content,
            metadata={
                "date": datetime.now().strftime("%Y-%m-%d"),
                "author": "AI 경영자문팀"
            }
        )
        print("   ✓ 마크다운 생성 완료")
        print()

        # 6. 저장
        print("💾 6단계: 파일 저장...")

        # 파일명 생성
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '_')).strip()
        safe_topic = safe_topic.replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # HTML 저장
        html_filename = f"{safe_topic}_{timestamp}.html"
        html_path = Path(OUTPUT_HTML_PATH) / html_filename
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        print(f"   ✓ HTML 저장: {html_path}")

        # 마크다운 저장
        md_filename = f"{safe_topic}_{timestamp}.md"
        md_path = Path(obsidian_output_path) / md_filename
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_output)
        print(f"   ✓ 마크다운 저장: {md_path}")
        print()

        # 완료
        print("="*60)
        print("✅ 전자책 생성 완료!")
        print("="*60)
        print()
        print(f"📄 HTML: {html_path}")
        print(f"📝 마크다운: {md_path}")
        print()

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
