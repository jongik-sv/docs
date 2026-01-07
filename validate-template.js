/**
 * YAML 템플릿에서 SVG를 추출하여 PNG로 렌더링하는 검증 스크립트
 * Usage: node validate-template.js <yaml-file> <output-png>
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const { chromium } = require('playwright');

async function validateTemplate(yamlFile, outputPng) {
  const content = fs.readFileSync(yamlFile, 'utf8');
  const template = yaml.load(content);

  // SVG inline이 있는 경우 직접 사용
  let svgContent = '';

  if (template.svg_inline) {
    svgContent = template.svg_inline;
  } else if (template.svg && template.svg.arrows) {
    // SVG 구조에서 SVG 생성
    const canvas = template.canvas || { reference_width: 960, reference_height: 540 };
    svgContent = generateSvgFromTemplate(template, canvas);
  } else {
    // shapes에서 SVG 타입 찾기
    const svgShape = (template.shapes || []).find(s => s.type === 'svg' && s.svg);
    if (svgShape && svgShape.svg.inline) {
      svgContent = svgShape.svg.inline;
    }
  }

  if (!svgContent) {
    console.error('No SVG content found in template');
    process.exit(1);
  }

  // HTML 래퍼 생성
  const canvas = template.canvas || { reference_width: 960, reference_height: 540 };
  const bgColor = template.background?.color || '#FFFFFF';

  const html = `<!DOCTYPE html>
<html>
<head>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: ${canvas.reference_width}px;
      height: ${canvas.reference_height}px;
      background: ${bgColor};
      font-family: Arial, sans-serif;
    }
    .container { width: 100%; height: 100%; position: relative; }
  </style>
</head>
<body>
  <div class="container">
    ${svgContent}
  </div>
</body>
</html>`;

  // Playwright로 렌더링
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.setContent(html);
  await page.setViewportSize({
    width: canvas.reference_width,
    height: canvas.reference_height
  });

  await page.screenshot({ path: outputPng, fullPage: true });
  await browser.close();

  console.log(`Screenshot saved to: ${outputPng}`);
}

function generateSvgFromTemplate(template, canvas) {
  // 기본 SVG 구조 생성
  const width = canvas.reference_width;
  const height = canvas.reference_height;

  let svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}">`;

  // defs 추가
  if (template.svg?.defs) {
    svg += template.svg.defs;
  }

  // 배경
  const bg = template.background?.color || '#F8F9FA';
  svg += `<rect width="${width}" height="${height}" fill="${bg}"/>`;

  // 헤더 바
  if (template.header?.style?.fill) {
    const headerGeo = template.header.geometry || { x: '0%', y: '0%', cx: '100%', cy: '11%' };
    const hx = parsePercent(headerGeo.x, width);
    const hy = parsePercent(headerGeo.y, height);
    const hcx = parsePercent(headerGeo.cx, width);
    const hcy = parsePercent(headerGeo.cy, height);

    if (template.header.style.fill.type === 'gradient') {
      const colors = template.header.style.fill.gradient?.colors || ['#7B68EE', '#9370DB'];
      svg += `<defs><linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">`;
      svg += `<stop offset="0%" stop-color="${colors[0]}"/>`;
      svg += `<stop offset="100%" stop-color="${colors[1]}"/>`;
      svg += `</linearGradient></defs>`;
      svg += `<rect x="${hx}" y="${hy}" width="${hcx}" height="${hcy}" fill="url(#headerGrad)"/>`;
    }
  }

  // 화살표 추가
  if (template.svg?.arrows) {
    svg += '<g filter="url(#arrowShadow)">';
    for (const arrow of template.svg.arrows) {
      const stroke = arrow.stroke || '#7B7FD4';
      const strokeWidth = arrow.stroke_width || 14;
      svg += `<path d="${arrow.path}" stroke="${stroke}" stroke-width="${strokeWidth}" fill="none" stroke-linecap="round"/>`;

      // 라벨 추가
      if (arrow.label) {
        const lp = arrow.label.position;
        const rotate = arrow.label.rotate ? `transform="rotate(${arrow.label.rotate}, ${lp.x}, ${lp.y})"` : '';
        svg += `<text x="${lp.x}" y="${lp.y}" text-anchor="middle" font-family="Arial" font-size="${arrow.label.font_size || 15}" font-weight="${arrow.label.font_weight || 'bold'}" fill="${arrow.label.fill || '#6B5CE7'}" ${rotate}>${arrow.label.text}</text>`;
      }
    }
    svg += '</g>';
  }

  // 중앙 요소
  if (template.svg?.center_element) {
    const ce = template.svg.center_element;
    const pos = ce.position;

    if (ce.lines) {
      for (const line of ce.lines) {
        svg += `<text x="${pos.x}" y="${pos.y + (line.y || 0)}" text-anchor="middle" font-family="Arial" font-size="${line.font_size}" font-weight="${line.font_weight || 'normal'}" fill="${ce.color || '#333'}">${line.content}</text>`;
      }
    }
  }

  svg += '</svg>';
  return svg;
}

function parsePercent(val, total) {
  if (typeof val === 'string' && val.endsWith('%')) {
    return (parseFloat(val) / 100) * total;
  }
  return parseFloat(val);
}

// CLI 실행
const args = process.argv.slice(2);
if (args.length < 2) {
  console.log('Usage: node validate-template.js <yaml-file> <output-png>');
  process.exit(1);
}

validateTemplate(args[0], args[1]).catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
