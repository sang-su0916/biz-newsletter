#!/usr/bin/env node
import inquirer from 'inquirer';
import { generateEbook } from './generator.js';

console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         📚 비즈니스 전자책 자동 생성 시스템 📚              ║
║                                                           ║
║   Obsidian 볼트 기반 AI 전자책 생성기                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
`);

async function main() {
  try {
    const answers = await inquirer.prompt([
      {
        type: 'input',
        name: 'folderName',
        message: '옵시디언 폴더명을 입력하세요:',
        default: '10. Biz',
        validate: (input) => input.trim() !== '' || '폴더명을 입력해주세요.'
      },
      {
        type: 'input',
        name: 'topic',
        message: '전자책 주제(제목)를 입력하세요:',
        validate: (input) => input.trim() !== '' || '주제를 입력해주세요.'
      },
      {
        type: 'input',
        name: 'author',
        message: '저자명을 입력하세요:',
        default: 'J-Business Team'
      },
      {
        type: 'confirm',
        name: 'confirm',
        message: '전자책 생성을 시작하시겠습니까?',
        default: true
      }
    ]);

    if (!answers.confirm) {
      console.log('\n✖ 전자책 생성이 취소되었습니다.');
      return;
    }

    console.log('\n🚀 전자책 생성을 시작합니다...\n');
    console.log(`📁 대상 폴더: ${answers.folderName}`);
    console.log(`📖 주제: ${answers.topic}`);
    console.log(`✍️  저자: ${answers.author}\n`);

    await generateEbook(answers);

    console.log('\n✅ 전자책 생성이 완료되었습니다!');
    console.log(`\n📂 생성된 파일 위치:`);
    console.log(`   - HTML: Auto News letter/News Completion/`);
    console.log(`   - Markdown: Obsidian Vault (지정한 경로)\n`);

  } catch (error) {
    console.error('\n❌ 오류 발생:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

main();
