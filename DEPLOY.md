# 배포 가이드

## 🚀 Vercel 배포 (권장)

### 방법 1: GitHub 연동 (가장 쉬움)

1. **Vercel 계정 생성**
   - https://vercel.com 접속
   - GitHub 계정으로 로그인

2. **프로젝트 Import**
   - "Add New..." → "Project" 클릭
   - GitHub 리포지토리 선택: `sang-su0916/biz-newsletter`
   - "Import" 클릭

3. **설정**
   - Framework Preset: **Other**
   - Build Command: (비워둠)
   - Output Directory: `public`
   - Install Command: `npm install`

4. **환경 변수 설정** (선택사항)
   - Settings → Environment Variables
   - `NODE_ENV`: `production`

5. **배포**
   - "Deploy" 클릭
   - 배포 완료 후 URL 확인

### 방법 2: Vercel CLI

```bash
# Vercel 로그인
vercel login

# 배포
vercel

# 프로덕션 배포
vercel --prod
```

## 📦 배포 전 체크리스트

- [x] `.gitignore`에 `.env` 추가됨
- [x] API 키가 `.env.example`에서 제거됨
- [x] `vercel.json` 설정 파일 생성됨
- [x] GitHub에 푸시됨

## 🌐 배포 후 확인사항

1. **웹사이트 접속 확인**
2. **뉴스레터 생성 기능 테스트**
3. **파일 다운로드 기능 확인**

## ⚠️ 주의사항

- **Obsidian 폴더 경로**: 로컬 경로(`/Users/isangsu/TMP_MY/knowledge.biz/`)는 배포 환경에서 작동하지 않습니다
- 배포 환경에서는 샘플 데이터를 사용하거나, 파일 업로드 기능을 추가해야 합니다

## 🔧 트러블슈팅

### 배포 실패 시
- `vercel logs`로 로그 확인
- GitHub 리포지토리 설정 확인
- 환경 변수 확인

### 404 에러 발생 시
- `vercel.json` 설정 확인
- 정적 파일 경로 확인

## 📞 문의
- GitHub Issues: https://github.com/sang-su0916/biz-newsletter/issues
