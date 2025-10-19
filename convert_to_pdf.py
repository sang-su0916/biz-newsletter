#!/usr/bin/env python3
"""
HTML을 PDF로 변환하는 스크립트
weasyprint 사용
"""

import sys
import os
from pathlib import Path


def convert_html_to_pdf(html_path: str, pdf_path: str) -> bool:
    """HTML 파일을 PDF로 변환"""
    try:
        # weasyprint 임포트 (설치 필요: pip install weasyprint)
        try:
            from weasyprint import HTML, CSS
        except ImportError:
            print("Error: weasyprint가 설치되지 않았습니다.", file=sys.stderr)
            print("설치: pip install weasyprint", file=sys.stderr)
            return False

        # HTML 파일 읽기
        if not os.path.exists(html_path):
            print(f"Error: HTML 파일을 찾을 수 없습니다: {html_path}", file=sys.stderr)
            return False

        # PDF 변환
        print(f"Converting: {html_path} -> {pdf_path}", file=sys.stderr)

        # HTML을 PDF로 변환
        html = HTML(filename=html_path)

        # PDF 생성 (최적화 옵션 포함)
        html.write_pdf(
            pdf_path,
            optimize_size=('fonts', 'images')  # PDF 크기 최적화
        )

        print(f"Success: PDF 생성 완료 - {pdf_path}", file=sys.stderr)
        return True

    except Exception as e:
        print(f"Error: PDF 변환 실패 - {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


def main():
    """CLI 인터페이스"""
    if len(sys.argv) != 3:
        print("Usage: python convert_to_pdf.py <input.html> <output.pdf>", file=sys.stderr)
        sys.exit(1)

    html_path = sys.argv[1]
    pdf_path = sys.argv[2]

    # 출력 디렉토리 생성
    output_dir = Path(pdf_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # 변환 실행
    success = convert_html_to_pdf(html_path, pdf_path)

    if success:
        print(f"PDF: {pdf_path}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
