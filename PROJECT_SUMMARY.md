# 비즈니스 전자책 생성기 - 프로젝트 작업 요약

## 📅 작업 일자
2025년 1월 (세션 연속)

## 🎯 주요 작업 내역

### 1. Colorful 테마 가독성 개선 (완료 ✅)

**문제점:**
- 텍스트가 전혀 보이지 않는 문제 (어두운 배경 + 흰색 텍스트)
- 중첩된 박스 디자인이 너무 어수선함
- 전문적이지 않고 복잡한 구조

**해결 방법:**
- 배경색을 어두운 그라디언트에서 밝은 단색으로 변경
- 텍스트 색상을 흰색에서 진한 회색(#111827)으로 변경
- 모든 특수 박스를 플랫 디자인 + 왼쪽 테두리로 단순화
- 중첩 구조 제거하고 깔끔한 레이아웃 적용

**수정된 파일:**
- `/templates/colorful_template.html`

**주요 CSS 변경사항:**
```css
/* 배경색 변경 */
--bg-white: #FFFFFF;  /* 기존: gradient */
--text-white: #111827;  /* 기존: #FFFFFF */

/* 특수 박스 디자인 단순화 */
.tax-info {
    background: #F0FDF4;
    border-left: 4px solid #10B981;
    border-radius: 8px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.term-box {
    background: #FAF5FF;
    border-left: 4px solid #8B5CF6;
}

.j-tip {
    background: #FFFBEB;
    border-left: 4px solid #F59E0B;
}

.ai-tool {
    background: #ECFEFF;
    border-left: 4px solid #06B6D4;
}
```

---

### 2. Light 테마 삭제 (완료 ✅)

**문제점:**
- Light 테마에서 계속 에러 발생
- 사용자가 삭제 요청

**해결 방법:**
- `public/index.html`에서 Light 테마 옵션 제거
- 드롭다운에서 선택지 삭제

**수정된 파일:**
- `/public/index.html`

**변경 코드:**
```html
<!-- 기존 -->
<option value="light">Clean Light - 깔끔한 라이트 테마</option>

<!-- 삭제됨 -->
```

---

### 3. 중복 텍스트 문제 해결 (완료 ✅)

**문제점:**
- 박스 제목이 두 번 표시됨 (예: "용어풀이" 아래 또 "용어풀이")
- CSS `::before` 요소가 전체 텍스트를 중복 생성

**해결 방법:**
- CSS `::before` 요소를 이모지만 표시하도록 수정
- HTML 제목 요소가 텍스트를 한 번만 표시하도록 변경

**수정된 파일:**
- `/templates/colorful_template.html`

**변경 코드:**
```css
/* 기존 - 전체 텍스트 표시 */
.tax-info-title::before {
    content: '💰 절세 정보';
}

/* 수정 - 이모지만 표시 */
.tax-info-title::before {
    content: '💰';
}

/* 동일하게 모든 박스에 적용 */
.term-box-title::before { content: '📖'; }
.j-tip-title::before { content: '💡'; }
.ai-tool-title::before { content: '🤖'; }
```

---

### 4. Gemini API 통합 (완료 ✅)

**목적:**
- Claude API가 비싸므로 테스트용으로 Gemini API 사용 가능하게 함
- 사용자가 모델을 선택적으로 사용할 수 있도록 UI 제공

**구현 세부사항:**

#### 4.1. Python 라이브러리 설치
```bash
pip install google-generativeai
```

#### 4.2. 환경 변수 설정
**파일:** `.env`
```bash
# Claude API 키 (고품질, 비용 높음)
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Gemini API 키 (빠르고 저렴함, 테스트용)
GEMINI_API_KEY=AIzaSyCj9En-fRZ5eetQ9R33zAbhlcudkZjcpzc
```

#### 4.3. 프론트엔드 UI 추가
**파일:** `/public/index.html`

```html
<!-- AI 모델 선택 드롭다운 추가 -->
<div class="form-group">
    <label for="model">AI 모델 선택</label>
    <select id="model" name="model">
        <option value="claude">Claude 3.5 Sonnet - 고품질 (비용 높음)</option>
        <option value="gemini" selected>Gemini 2.0 Flash - 빠르고 저렴함 (테스트용 권장)</option>
    </select>
    <p class="hint">테스트용으로는 Gemini를, 최종 결과물은 Claude를 권장합니다</p>
</div>

<!-- JavaScript에서 model 파라미터 추가 -->
<script>
const formData = {
    folderName: document.getElementById('folderName').value,
    topic: document.getElementById('topic').value,
    theme: document.getElementById('theme').value,
    model: document.getElementById('model').value  // 추가
};
</script>
```

#### 4.4. Node.js 서버 수정
**파일:** `/src/server.js`

```javascript
app.post('/api/generate', async (req, res) => {
  try {
    const { folderName, topic, theme, model } = req.body;  // model 추가

    const selectedModel = model || 'claude';  // 기본값: claude

    console.log(`   모델: ${selectedModel}\n`);

    // Python 스크립트 실행 시 model 파라미터 전달
    const { stdout, stderr } = await execAsync(
      `"${pythonBin}" "${pythonScript}" "${folderName}" "${topic}" "${selectedTheme}" "${selectedModel}"`,
      // ...
    );
  }
});
```

#### 4.5. Python Wrapper 수정
**파일:** `/ebook_generator_wrapper.py`

```python
def generate_ebook_api(folder_name: str, topic: str, theme: str = 'dark',
                       model: str = 'claude') -> dict:
    """
    Args:
        model: AI 모델 (claude, gemini)  # 추가
    """
    # AI 팀 초기화 시 model_type 전달
    ai_team = AIConsultingTeam(client, GUIDELINE_PATH, model_type=model)
    # ...

def main():
    """CLI 인터페이스"""
    folder_name = sys.argv[1]
    topic = sys.argv[2]
    theme = sys.argv[3] if len(sys.argv) >= 4 else 'dark'
    model = sys.argv[4] if len(sys.argv) == 5 else 'claude'  # 추가

    result = generate_ebook_api(folder_name, topic, theme, model)
```

#### 4.6. 핵심 Python 모듈 수정
**파일:** `/ebook_generator.py`

```python
import google.generativeai as genai

# Gemini API 초기화
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class AIConsultingTeam:
    def __init__(self, client, guideline_path: str, model_type: str = 'claude'):
        self.client = client
        self.model_type = model_type  # 'claude' 또는 'gemini'
        self.guideline = self._load_guideline(guideline_path)

        # Gemini 모델 초기화
        if model_type == 'gemini':
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def generate_structure(self, topic: str, knowledge: str) -> Dict[str, any]:
        # 시스템 프롬프트와 사용자 메시지 준비
        # ...

        # 모델별 API 호출
        if self.model_type == 'gemini':
            full_prompt = f"{system_prompt}\n\n{user_message}"
            response = self.gemini_model.generate_content(full_prompt)
            content = response.text
        else:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            content = response.content[0].text

        # JSON 파싱 및 반환
        # ...

    def write_subtopic(self, main_topic: str, subtopic: Dict[str, str],
                      knowledge: str, expert_role: str) -> str:
        # 시스템 프롬프트와 사용자 메시지 준비
        # ...

        # 모델별 API 호출
        if self.model_type == 'gemini':
            full_prompt = f"{system_prompt}\n\n{user_message}"
            response = self.gemini_model.generate_content(full_prompt)
            return response.text
        else:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=3000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            return response.content[0].text
```

---

## 🔧 시스템 아키텍처

### 요청 흐름
```
사용자 (브라우저)
    ↓ POST /api/generate
Node.js Express Server (src/server.js)
    ↓ execAsync
Python Wrapper (ebook_generator_wrapper.py)
    ↓
Python Core Module (ebook_generator.py)
    ↓ API 호출
Claude API 또는 Gemini API
    ↓ 응답
HTML + Markdown 파일 생성
```

### 파일 구조
```
J-project/
├── .env                           # API 키 설정
├── src/
│   └── server.js                  # Express 웹 서버
├── public/
│   └── index.html                 # 사용자 UI
├── templates/
│   ├── dark_template.html         # 다크 테마
│   └── colorful_template.html     # 컬러풀 테마 (수정됨)
├── ebook_generator.py             # 핵심 생성 로직 (Gemini 통합)
├── ebook_generator_wrapper.py     # CLI 래퍼 (모델 파라미터 추가)
└── output/
    └── generated_ebooks/          # HTML 출력 폴더
```

---

## ⚠️ 알려진 이슈 및 해결 방법

### Claude API Rate Limit (Error 429)

**문제:**
```
Error code: 429 - rate_limit_error:
This request would exceed your organization's maximum usage increase rate
for input tokens per minute
```

**원인:**
- 짧은 시간 내 여러 번 Claude API 호출
- 분당 입력 토큰 한도 초과

**해결 방법:**
1. **즉시 해결:** 5-10분 대기 후 재시도
2. **테스트용:** Gemini 모델 사용 (기본 선택됨)
3. **최종 결과물:** Claude 모델 사용

**권장 사용 패턴:**
- 테스트 및 실험: Gemini 2.0 Flash (빠르고 저렴)
- 최종 결과물: Claude 3.5 Sonnet (고품질)

---

## 📊 API 비용 비교

| 모델 | 품질 | 속도 | 비용 | 권장 용도 |
|------|------|------|------|-----------|
| Claude 3.5 Sonnet | ⭐⭐⭐⭐⭐ | 중간 | 💰💰💰 | 최종 결과물 |
| Gemini 2.0 Flash | ⭐⭐⭐⭐ | 빠름 | 💰 | 테스트/실험 |

---

## 🎨 테마 비교

### Professional Dark (다크 테마)
- 전문가용 다크 테마
- 진한 배경색 + 밝은 텍스트
- 프레젠테이션에 적합

### Colorful Modern (컬러풀 테마) - 수정됨 ✅
- 생동감 있는 컬러풀 테마
- 밝은 배경색 + 진한 텍스트
- 가독성 개선됨
- 심플하고 고급스러운 디자인
- 특수 박스별 색상 구분:
  - 💰 절세 정보: 연한 녹색 (#F0FDF4)
  - 📖 용어 풀이: 연한 보라색 (#FAF5FF)
  - 💡 J-TIP: 연한 노란색 (#FFFBEB)
  - 🤖 AI 도구: 연한 청록색 (#ECFEFF)

---

## 🚀 사용 방법

### 1. 서버 실행
```bash
cd /Users/isangsu/TMP_MY/J-project
npm start
```

### 2. 브라우저 접속
```
http://localhost:3000
```

### 3. 전자책 생성
1. 옵시디언 폴더명 입력 (예: `10. Biz`)
2. 전자책 주제 입력
3. 디자인 테마 선택
4. AI 모델 선택
   - 테스트: Gemini 2.0 Flash (기본)
   - 최종: Claude 3.5 Sonnet
5. "🚀 전자책 생성하기" 클릭
6. 2-3분 대기
7. HTML 또는 Markdown 다운로드

### 4. 출력 파일 위치
- **HTML**: `/Users/isangsu/TMP_MY/J-project/output/generated_ebooks/`
- **Markdown**: `/Users/isangsu/Documents/Obsidian/Obsi/Vault.01/Auto News letter/News Completion/`

---

## 💡 개발 팁

### API 키 관리
- `.env` 파일에 안전하게 저장
- Git에 커밋하지 않도록 `.gitignore` 설정 확인

### 테마 커스터마이징
- `/templates/` 폴더의 HTML 파일 수정
- CSS 변수를 활용하여 색상 일괄 변경 가능

### 디버깅
- 서버 로그 확인: 터미널 출력 모니터링
- Python 에러: `venv/bin/python3 ebook_generator_wrapper.py` 직접 실행

---

## 📝 변경 이력

### 2025-01-XX (현재 세션)
- ✅ Colorful 테마 가독성 개선
- ✅ Light 테마 삭제
- ✅ 중복 텍스트 문제 해결
- ✅ Gemini API 통합 완료
- ✅ AI 모델 선택 UI 추가

### 이전 세션
- 마크다운 to HTML 변환
- 멀티 포맷 다운로드 (HTML + MD)
- JSON 파싱 개선
- 애플리케이션 이름 변경

---

## 🎯 향후 개선 사항 (선택사항)

1. 추가 테마 개발
2. 사용자 커스텀 색상 선택 기능
3. PDF 내보내기 기능
4. 진행 상황 실시간 표시
5. 생성된 전자책 미리보기 기능

---

## 📞 지원

문제 발생 시:
1. 서버 로그 확인
2. API 키 설정 확인 (`.env`)
3. Python 가상환경 활성화 확인
4. Rate limit 에러 → 5-10분 대기 또는 Gemini 사용

---

**문서 작성일:** 2025년 1월
**프로젝트 경로:** `/Users/isangsu/TMP_MY/J-project/`
