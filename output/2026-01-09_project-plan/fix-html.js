#!/usr/bin/env node
/**
 * HTML 파일 수정 스크립트
 * - <div> 안의 직접 텍스트를 <p> 태그로 감싸기
 * - CSS에 p 태그 리셋 스타일 추가
 */

const fs = require('fs');
const path = require('path');

const slidesDir = path.join(__dirname, 'slides');

// CSS 리셋 스타일
const pReset = '    p { font: inherit; color: inherit; line-height: inherit; text-align: inherit; }';

// 수정할 파일들
const files = fs.readdirSync(slidesDir).filter(f => f.endsWith('.html'));

files.forEach(file => {
  const filePath = path.join(slidesDir, file);
  let content = fs.readFileSync(filePath, 'utf-8');

  // 1. CSS에 p 리셋 추가 (이미 있으면 스킵)
  if (!content.includes('p { font: inherit')) {
    content = content.replace(
      /(\* \{ margin: 0; padding: 0; box-sizing: border-box; \})/,
      `$1\n${pReset}`
    );
  }

  // 2. <div class="xxx">텍스트</div> 패턴을 <div class="xxx"><p>텍스트</p></div>로 변경
  // 텍스트만 있는 div (중첩된 태그 없음, 단 <br>은 허용)
  content = content.replace(
    /<div class="([^"]+)">([^<]+(?:<br\/?>[^<]*)*)<\/div>/g,
    (match, className, text) => {
      // 이미 <p>로 감싸져 있으면 스킵
      if (text.trim().startsWith('<p>')) return match;
      // 텍스트가 비어있으면 스킵
      if (!text.trim()) return match;
      return `<div class="${className}"><p>${text}</p></div>`;
    }
  );

  fs.writeFileSync(filePath, content);
  console.log(`Fixed: ${file}`);
});

console.log(`\nTotal: ${files.length} files processed`);
