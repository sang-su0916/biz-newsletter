# 사용 가이드

## 빠른 시작

### 1. 환경 설정

```bash
# API 키 설정 (반드시 필요!)
export ANTHROPIC_API_KEY="your_api_key_here"

# 또는 .env 파일 생성
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 실행

```bash
python ebook_generator.py
```

## 입력 예시

프로그램 실행 후 다음 정보를 순서대로 입력합니다:

```
지식베이스 폴더명을 입력하세요: 테스트_세무자료
주제(H1)를 입력하세요: 개인사업자를 위한 세금 절세 가이드
옵시디언 저장 경로를 입력하세요 (기본값: /Users/isangsu/Documents/Obsidian/Obsi/Vault.01):
```

**참고**:
- 옵시디언 저장 경로는 엔터만 치면 기본값이 사용됩니다
- 지식베이스 폴더는 `/Users/isangsu/TMP_MY/knowledge.biz/` 하위에 있어야 합니다

## 테스트용 샘플 데이터

샘플 지식베이스가 이미 생성되어 있습니다:
- **폴더**: `/Users/isangsu/TMP_MY/knowledge.biz/테스트_세무자료/`
- **파일**:
  - `종합소득세_가이드.md`
  - `부가가치세_안내.md`
  - `4대보험_가입안내.md`

테스트 시 **"테스트_세무자료"**를 폴더명으로 입력하세요.

## 예상 실행 시간

- **구조 기획**: 약 30초
- **콘텐츠 작성** (5개 소주제): 약 2-3분
- **HTML/마크다운 생성**: 약 10초
- **총 소요시간**: 약 3-5분

## 출력 확인

생성 완료 후 다음 위치에서 파일을 확인할 수 있습니다:

1. **HTML 전자책**
   - 경로: `output/generated_ebooks/`
   - 파일명: `[주제]_[타임스탬프].html`
   - 브라우저에서 열어서 확인

2. **옵시디언 마크다운**
   - 경로: 입력한 옵시디언 경로
   - 파일명: `[주제]_[타임스탬프].md`
   - 옵시디언에서 열어서 확인

## 트러블슈팅

### API 키 오류
```
Error: The api_key client option must be set
```
**해결**: ANTHROPIC_API_KEY 환경 변수를 설정하세요
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

### 폴더를 찾을 수 없음
```
FileNotFoundError: 폴더를 찾을 수 없습니다
```
**해결**: 지식베이스 폴더 경로를 확인하세요
```bash
ls -la /Users/isangsu/TMP_MY/knowledge.biz/
```

### 파일 저장 오류
```
PermissionError: [Errno 13] Permission denied
```
**해결**: 출력 디렉토리에 대한 쓰기 권한을 확인하세요
```bash
chmod 755 output/generated_ebooks
```

## 고급 사용법

### 다른 지식베이스 폴더 추가

```bash
# 새 폴더 생성
mkdir -p "/Users/isangsu/TMP_MY/knowledge.biz/내_비즈니스_자료"

# 파일 추가 (마크다운 또는 텍스트)
touch "/Users/isangsu/TMP_MY/knowledge.biz/내_비즈니스_자료/자료1.md"
```

### 가이드라인 커스터마이징

`전자책_Auto-Agent_지침_비즈니스버전.md` 파일을 수정하여 AI 팀의 작동 방식을 변경할 수 있습니다.

### HTML 디자인 수정

`templates/newsletter_template.html` 파일을 수정하여 전자책의 디자인을 변경할 수 있습니다.

## 주의사항

1. **팩트체크**: AI가 생성한 내용은 반드시 공식 출처에서 재확인하세요
2. **API 비용**: Claude API 사용에 따른 비용이 발생할 수 있습니다
3. **생성 시간**: 네트워크 상태에 따라 소요 시간이 달라질 수 있습니다
4. **파일 덮어쓰기**: 동일한 주제와 타임스탬프로 파일이 생성되면 덮어쓰여질 수 있습니다

## 문의

프로그램 사용 중 문제가 발생하면 다음을 확인하세요:
1. Python 버전 (3.8 이상 권장)
2. API 키 설정
3. 지식베이스 폴더 경로
4. 네트워크 연결 상태
