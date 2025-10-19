#!/usr/bin/env python3
"""
CLI 전자책 생성 스크립트
웹 서버에서 호출하기 위한 간단한 인터페이스
"""

import sys
import json
from ebook_generator import generate_ebook


def main():
    if len(sys.argv) != 3:
        print(json.dumps({
            "success": False,
            "error": "Usage: python generate_ebook_cli.py <folder_name> <topic>"
        }))
        sys.exit(1)

    folder_name = sys.argv[1]
    topic = sys.argv[2]

    try:
        result = generate_ebook(folder_name, topic)

        # 성공 응답 (JSON)
        print(json.dumps({
            "success": True,
            "htmlPath": str(result['html_path']),
            "mdPath": str(result['md_path']),
            "filename": result['html_path'].name
        }, ensure_ascii=False))

    except Exception as e:
        # 실패 응답 (JSON)
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
