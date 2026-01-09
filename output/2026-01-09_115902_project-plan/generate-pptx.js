const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');

const html2pptx = require('../../.claude/skills/ppt-gen/scripts/html2pptx.js');

async function main() {
  const slidesDir = path.join(__dirname, 'slides');
  const outputFile = path.join(__dirname, '스마트물류관리시스템_수행계획서_v6.pptx');

  // Get all HTML files sorted by name
  const files = fs.readdirSync(slidesDir)
    .filter(f => f.endsWith('.html'))
    .sort();

  console.log(`Found ${files.length} slides`);

  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Claude Code';
  pptx.title = '스마트 물류관리 시스템 구축 수행계획서';
  pptx.subject = '프로젝트 수행계획서';

  for (const file of files) {
    const htmlPath = path.join(slidesDir, file);
    console.log(`Processing: ${file}`);
    try {
      await html2pptx(htmlPath, pptx);
    } catch (err) {
      console.error(`Error processing ${file}:`, err.message);
    }
  }

  await pptx.writeFile(outputFile);
  console.log(`Created: ${outputFile}`);
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
