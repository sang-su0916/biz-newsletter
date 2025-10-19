import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// MCP 도구 모킹 (실제 환경에서는 MCP 서버 연결)
const mockMCP = {
  async readObsidianFolder(folderPath) {
    console.log(`📖 MCP: Obsidian 폴더 읽기 - ${folderPath}`);

    try {
      // 실제 폴더 읽기
      const files = await fs.readdir(folderPath);
      const mdFiles = files.filter(f => f.endsWith('.md'));

      let content = '';
      for (const file of mdFiles.slice(0, 10)) { // 최대 10개 파일만 읽기
        const filePath = path.join(folderPath, file);
        const fileContent = await fs.readFile(filePath, 'utf-8');
        content += `\n\n${fileContent}`;
      }

      return {
        files: mdFiles,
        content: content || '지식 베이스 샘플 내용...'
      };
    } catch (error) {
      console.error(`폴더 읽기 오류: ${error.message}`);
      return {
        files: [],
        content: '지식 베이스 샘플 내용...'
      };
    }
  },

  async analyzeContent(content, topic) {
    console.log(`🤖 MCP: AI 분석 중 - 주제: ${topic}`);
    // 실제로는 Sequential MCP 등 사용
    return {
      subtopics: [
        { title: '세무 기초 이해하기', description: '개인사업자를 위한 세무 기본 개념과 절세 전략' },
        { title: '노무 관리 실전', description: '인사노무 관리와 4대보험 완벽 가이드' },
        { title: '회계 실무 마스터', description: '재무제표 작성과 손익 분석 방법' },
        { title: 'AI 도구 활용', description: '업무 자동화를 위한 AI 도구 활용법' },
        { title: '종합 전략 수립', description: '세무·노무·회계 통합 전략과 실행 계획' }
      ]
    };
  },

  async generateContent(subtopic, knowledgeBase) {
    console.log(`✍️  MCP: 콘텐츠 생성 중 - ${subtopic.title}`);

    // 마크다운을 HTML로 변환
    const htmlContent = this.convertMarkdownToHTML(knowledgeBase.content || '');

    return {
      content: `
<h3>${subtopic.title}</h3>
<p>이 섹션에서는 ${subtopic.description}에 대해 자세히 다룹니다.</p>

${htmlContent}

<div class="tax-info">
    <div class="tax-info-title">세금정보</div>
    <p>최신 세법 및 절세 전략에 대한 정보입니다. (출처: 국세청, 2025년 10월 기준)</p>
</div>

<div class="j-tip">
    <div class="j-tip-title">실무 팁</div>
    <p>실무에서 바로 활용할 수 있는 구체적인 방법을 소개합니다.</p>
</div>

<div class="checklist">
    <h4>실행 체크리스트</h4>
    <ul>
        <li>첫 번째 실행 항목</li>
        <li>두 번째 실행 항목</li>
        <li>세 번째 실행 항목</li>
    </ul>
</div>
`,
      wordCount: 3500
    };
  },

  convertMarkdownToHTML(markdown) {
    // 마크다운을 HTML로 변환
    let html = markdown
      // YAML frontmatter 제거
      .replace(/^---[\s\S]*?---\n/m, '')
      // 코드 블록 제거 (html, javascript 등)
      .replace(/```[\s\S]*?```/g, '')
      .replace(/`[^`]+`/g, '')
      // ** (볼드) 변환
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      // * (이탤릭) 변환
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      // ### (H3) 변환
      .replace(/^### (.*?)$/gm, '<h4>$1</h4>')
      // ## (H2) 변환
      .replace(/^## (.*?)$/gm, '<h3>$1</h3>')
      // # (H1) 변환
      .replace(/^# (.*?)$/gm, '<h2>$1</h2>')
      // 리스트 변환
      .replace(/^- (.*?)$/gm, '<li>$1</li>')
      // 리스트를 ul로 감싸기
      .replace(/(<li>.*?<\/li>\n?)+/g, '<ul>$&</ul>')
      // 불필요한 공백 제거
      .replace(/\n\s*\n/g, '\n')
      // 줄바꿈을 p 태그로
      .replace(/([^\n>])\n(?!<)/g, '$1</p><p>')
      // 빈 태그 제거
      .replace(/<p>\s*<\/p>/g, '')
      .replace(/<ul>\s*<\/ul>/g, '');

    return `<p>${html}</p>`;
  },

  async generateDiagram(sectionIndex, subtopic) {
    console.log(`📊 MCP: 다이어그램 생성 중 - ${subtopic.title}`);
    return `
<div class="diagram-container">
    <div class="diagram-title">${subtopic.title} 프로세스</div>
    <svg width="100%" height="200" viewBox="0 0 600 200">
        <rect x="50" y="75" width="120" height="50" rx="8" fill="#1E40AF" stroke="none"/>
        <text x="110" y="105" text-anchor="middle" fill="white" font-size="14">단계 1</text>

        <path d="M180 100 L220 100" stroke="#1E40AF" stroke-width="2" marker-end="url(#arrowhead)"/>

        <rect x="230" y="75" width="120" height="50" rx="8" fill="#1E40AF" stroke="none"/>
        <text x="290" y="105" text-anchor="middle" fill="white" font-size="14">단계 2</text>

        <path d="M360 100 L400 100" stroke="#1E40AF" stroke-width="2" marker-end="url(#arrowhead)"/>

        <rect x="410" y="75" width="120" height="50" rx="8" fill="#1E40AF" stroke="none"/>
        <text x="470" y="105" text-anchor="middle" fill="white" font-size="14">단계 3</text>

        <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#1E40AF"/>
            </marker>
        </defs>
    </svg>
</div>
`;
  }
};

export async function generateEbook({ folderName, topic, author }) {
  const startTime = Date.now();

  try {
    // 1단계: 지식 베이스 구축
    console.log('📚 1단계: Obsidian 볼트에서 지식 베이스 구축 중...');
    const obsidianPath = `/Users/isangsu/TMP_MY/knowledge.biz/${folderName}`;
    const knowledgeBase = await mockMCP.readObsidianFolder(obsidianPath);
    console.log('   ✓ 지식 베이스 구축 완료\n');

    // 2단계: AI 분석 및 소주제 생성
    console.log('🤖 2단계: AI 경영자문팀 분석 중...');
    const analysis = await mockMCP.analyzeContent(knowledgeBase.content, topic);
    console.log(`   ✓ ${analysis.subtopics.length}개의 소주제 생성 완료\n`);

    // 3단계: 콘텐츠 생성
    console.log('✍️  3단계: 전자책 콘텐츠 생성 중...');
    let totalWordCount = 0;
    const sections = [];

    for (let i = 0; i < analysis.subtopics.length; i++) {
      const subtopic = analysis.subtopics[i];
      console.log(`   [${i + 1}/${analysis.subtopics.length}] ${subtopic.title} 생성 중...`);

      const content = await mockMCP.generateContent(subtopic, knowledgeBase);
      const diagram = await mockMCP.generateDiagram(i + 1, subtopic);

      sections.push({
        id: `section${i + 1}`,
        number: i + 1,
        title: subtopic.title,
        intro: subtopic.description,
        content: content.content + diagram
      });

      totalWordCount += content.wordCount;
    }
    console.log(`   ✓ 전체 콘텐츠 생성 완료 (약 ${totalWordCount.toLocaleString()}자)\n`);

    // 4단계: HTML 파일 생성
    console.log('📄 4단계: HTML 전자책 생성 중...');
    const htmlContent = await generateHTMLEbook(topic, author, sections);
    const outputDir = path.join(process.cwd(), 'Auto News letter', 'News Completion');
    await fs.mkdir(outputDir, { recursive: true });

    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `${topic.replace(/[^가-힣a-zA-Z0-9]/g, '_')}_${timestamp}.html`;
    const outputPath = path.join(outputDir, filename);

    await fs.writeFile(outputPath, htmlContent, 'utf-8');
    console.log(`   ✓ HTML 파일 생성: ${outputPath}\n`);

    // 5단계: Markdown 파일 생성
    console.log('📝 5단계: Markdown 파일 생성 중...');
    const mdContent = generateMarkdownEbook(topic, sections);
    const mdPath = path.join(outputDir, `${topic.replace(/[^가-힣a-zA-Z0-9]/g, '_')}_${timestamp}.md`);
    await fs.writeFile(mdPath, mdContent, 'utf-8');
    console.log(`   ✓ Markdown 파일 생성: ${mdPath}\n`);

    const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(1);
    console.log(`⏱️  총 소요 시간: ${elapsedTime}초`);

    return {
      htmlPath: outputPath,
      mdPath,
      wordCount: totalWordCount,
      sections: sections.length
    };

  } catch (error) {
    console.error('❌ 전자책 생성 중 오류 발생:', error);
    throw error;
  }
}

async function generateHTMLEbook(topic, author, sections) {
  const templatePath = path.join(process.cwd(), 'templates', 'newsletter_template.html');
  let template = await fs.readFile(templatePath, 'utf-8');

  const currentDate = new Date().toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  // 목차 생성
  const tocItems = sections.map(section => `
                <a href="#${section.id}" class="toc-item fade-in">
                    <h3>${section.number}. ${section.title}</h3>
                    <p>${section.intro}</p>
                </a>
  `).join('\n');

  // 본문 섹션 생성
  const contentSections = sections.map(section => `
    <section id="${section.id}" class="content-section fade-in">
        <div class="section-header">
            <div class="container">
                <h2>${section.number}. ${section.title}</h2>
                <p class="section-intro">${section.intro}</p>
            </div>
        </div>
        <div class="section-content">
            <div class="container">
                ${section.content}
            </div>
        </div>
    </section>
  `).join('\n');

  // 요약 섹션 생성
  const summaryContent = `
    <p>이 전자책은 ${sections.length}개의 핵심 주제로 구성되어 있으며,
    세무·노무·회계 분야의 실전 지식을 제공합니다.</p>
  `;

  const keyPrinciples = `
    <div class="principle-card">
        <h3>법규 준수</h3>
        <p>모든 정보는 국가 주무부처 공식 자료를 기반으로 작성되었습니다.</p>
    </div>
    <div class="principle-card">
        <h3>증빙 관리</h3>
        <p>세무·회계 처리 시 적격증빙 구비가 필수입니다.</p>
    </div>
    <div class="principle-card">
        <h3>전문가 상담</h3>
        <p>개별 상황에 맞는 의사결정은 전문가와 상담하세요.</p>
    </div>
  `;

  // 템플릿 치환 (저자 정보는 템플릿에 고정됨)
  template = template
    .replace(/\{\{TITLE\}\}/g, topic)
    .replace(/\{\{DATE\}\}/g, currentDate)
    .replace(/\{\{TOC_ITEMS\}\}/g, tocItems)
    .replace(/\{\{CONTENT_SECTIONS\}\}/g, contentSections)
    .replace(/\{\{SUMMARY_CONTENT\}\}/g, summaryContent)
    .replace(/\{\{KEY_PRINCIPLES\}\}/g, keyPrinciples);

  return template;
}

function generateMarkdownEbook(topic, sections) {
  let markdown = `# ${topic}\n\n`;
  markdown += `> 개인사업자와 중소기업을 위한 세무/노무/회계 실전 가이드\n\n`;
  markdown += `---\n\n`;
  markdown += `## 목차\n\n`;

  sections.forEach(section => {
    markdown += `${section.number}. [${section.title}](#${section.id})\n`;
  });

  markdown += `\n---\n\n`;

  sections.forEach(section => {
    markdown += `## ${section.number}. ${section.title}\n\n`;
    markdown += `> ${section.intro}\n\n`;

    // HTML 태그 제거 및 간단한 마크다운 변환
    const cleanContent = section.content
      .replace(/<div class="term-box">[\s\S]*?<\/div>/g, (match) => {
        return '\n> 📖 **용어풀이**: (내용은 HTML 버전 참조)\n\n';
      })
      .replace(/<div class="tax-info">[\s\S]*?<\/div>/g, '\n> 💰 **세금정보**: (내용은 HTML 버전 참조)\n\n')
      .replace(/<div class="j-tip">[\s\S]*?<\/div>/g, '\n> 💡 **실무 팁**: (내용은 HTML 버전 참조)\n\n')
      .replace(/<div class="checklist">[\s\S]*?<\/div>/g, '\n**체크리스트:**\n- [ ] 항목 확인\n\n')
      .replace(/<div class="diagram-container">[\s\S]*?<\/div>/g, '\n![다이어그램](diagram.svg)\n\n')
      .replace(/<[^>]+>/g, '')
      .replace(/\n\s*\n\s*\n/g, '\n\n');

    markdown += cleanContent;
    markdown += `\n---\n\n`;
  });

  markdown += `## 면책조항\n\n`;
  markdown += `본 전자책의 내용은 일반적인 정보 제공을 목적으로 하며, `;
  markdown += `개별 상황에 따라 전문가의 상담이 필요할 수 있습니다.\n\n`;

  return markdown;
}
