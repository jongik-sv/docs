const pptxgen = require('pptxgenjs');
const html2pptx = require('/home/jji/project/docs/.claude/skills/pptx/scripts/html2pptx');
const path = require('path');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = '테크솔루션_김철수';
    pptx.title = '스마트 물류관리 시스템 구축 프로젝트 수행계획서';
    pptx.subject = '착수보고회';

    const slidesDir = '/home/jji/project/docs/workspace/slides';

    for (let i = 1; i <= 18; i++) {
        const slideNum = i.toString().padStart(2, '0');
        const htmlFile = path.join(slidesDir, `slide${slideNum}.html`);
        console.log(`Processing slide ${i}...`);
        await html2pptx(htmlFile, pptx);
    }

    const outputPath = '/home/jji/project/docs/스마트물류관리시스템_착수보고.pptx';
    await pptx.writeFile({ fileName: outputPath });
    console.log(`Presentation saved to: ${outputPath}`);
}

createPresentation().catch(err => {
    console.error('Error:', err);
    process.exit(1);
});
