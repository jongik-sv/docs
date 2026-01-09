const pptxgen = require('pptxgenjs');
const html2pptx = require('./.claude/skills/ppt-gen/scripts/html2pptx.js');
const fs = require('fs');
const path = require('path');

async function main() {
  const slidesDir = process.argv[2] || 'output/2026-01-09_project-plan/slides';
  const outputFile = process.argv[3] || 'output/2026-01-09_project-plan/스마트물류시스템_수행계획서.pptx';

  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.title = '스마트 물류관리 시스템 구축 수행계획서';
  pptx.author = '(주)테크솔루션';

  const files = fs.readdirSync(slidesDir)
    .filter(f => f.endsWith('.html'))
    .sort();

  console.log(`Processing ${files.length} slides...`);

  for (const file of files) {
    const htmlPath = path.join(slidesDir, file);
    console.log(`  Converting: ${file}`);
    try {
      await html2pptx(htmlPath, pptx);
    } catch (err) {
      console.error(`  Error in ${file}: ${err.message}`);
    }
  }

  await pptx.writeFile(outputFile);
  console.log(`\nPPTX saved: ${outputFile}`);
}

main().catch(console.error);
