#!/usr/bin/env node
import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { generateEbook } from './generator.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// 미들웨어
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// 생성된 파일 제공 (JavaScript 출력 경로)
app.use('/downloads', express.static(path.join(process.cwd(), 'Auto News letter', 'News Completion')));

// 헬스체크
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: '비즈니스 전자책 생성기가 정상 작동 중입니다' });
});

// 전자책 생성 API (JavaScript 버전)
app.post('/api/generate', async (req, res) => {
  try {
    const { folderName, topic } = req.body;

    // 입력값 검증
    if (!folderName || !topic) {
      return res.status(400).json({
        success: false,
        error: '폴더명과 주제를 모두 입력해주세요'
      });
    }

    console.log(`\n📚 전자책 생성 요청:`);
    console.log(`   폴더: ${folderName}`);
    console.log(`   주제: ${topic}\n`);

    // JavaScript 전자책 생성 함수 호출
    const result = await generateEbook({
      folderName,
      topic,
      author: 'J-Business'
    });

    // 파일명 추출
    const filename = path.basename(result.htmlPath);

    res.json({
      success: true,
      message: '전자책이 성공적으로 생성되었습니다',
      downloadUrl: `/downloads/${filename}`,
      filename: filename,
      paths: {
        html: result.htmlPath,
        md: result.mdPath
      },
      stats: {
        wordCount: result.wordCount,
        sections: result.sections
      }
    });

  } catch (error) {
    console.error('❌ 전자책 생성 오류:', error);
    res.status(500).json({
      success: false,
      error: error.message || '전자책 생성 중 오류가 발생했습니다'
    });
  }
});

// 404 핸들러
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'API 엔드포인트를 찾을 수 없습니다'
  });
});

// 서버 시작
app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║       🌐 비즈니스 전자책 생성기 웹 서버 시작됨 🌐          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

🚀 서버 주소: http://localhost:${PORT}
📁 정적 파일: public/
📥 다운로드: output/generated_ebooks/

✅ 브라우저에서 http://localhost:${PORT} 을 열어보세요!
`);
});

// 에러 핸들러
process.on('uncaughtException', (error) => {
  console.error('💥 Uncaught Exception:', error);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('💥 Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});
