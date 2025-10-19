#!/usr/bin/env node
import { generateEbook } from './src/generator.js';

console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         📚 비즈니스 전자책 자동 생성 시스템 📚              ║
║         (테스트 실행 모드)                                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
`);

async function test() {
  const testData = {
    folderName: '10. Biz',
    topic: '중소기업 절세 전략 가이드',
    author: 'J-Business Team'
  };

  console.log('📋 테스트 데이터:');
  console.log(`   폴더: ${testData.folderName}`);
  console.log(`   주제: ${testData.topic}`);
  console.log(`   저자: ${testData.author}\n`);

  try {
    const result = await generateEbook(testData);

    console.log('\n✅ 테스트 성공!');
    console.log('\n📊 생성 결과:');
    console.log(`   - HTML 파일: ${result.htmlPath}`);
    console.log(`   - MD 파일: ${result.mdPath}`);
    console.log(`   - 총 글자수: ${result.wordCount.toLocaleString()}자`);
    console.log(`   - 섹션 수: ${result.sections}개`);

  } catch (error) {
    console.error('\n❌ 테스트 실패:', error.message);
    throw error;
  }
}

test();
