/**
 * YAML 템플릿에서 SVG를 추출하여 PNG로 렌더링
 */

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const templates = [
  {
    yaml: 'templates/contents/templates/cycle/cycle-4arrow1.yaml',
    thumb: 'templates/contents/thumbnails/cycle/cycle-4arrow1.png',
    output: 'comparison-cycle-4arrow1.png'
  },
  {
    yaml: 'templates/contents/templates/matrix/venn-4segment1.yaml',
    thumb: 'templates/contents/thumbnails/matrix/venn-4segment1.png',
    output: 'comparison-venn-4segment1.png'
  },
  {
    yaml: 'templates/contents/templates/flow/flow-circular-apple1.yaml',
    thumb: 'templates/contents/thumbnails/flow/flow-circular-apple1.png',
    output: 'comparison-flow-circular-apple1.png'
  },
  {
    yaml: 'templates/contents/templates/comparison/infographic-race1.yaml',
    thumb: 'templates/contents/thumbnails/comparison/infographic-race1.png',
    output: 'comparison-infographic-race1.png'
  }
];

// Extract svg_inline from YAML file (simple extraction)
function extractSvgInline(yamlContent) {
  // Find the start of svg_inline
  const startMarker = 'svg_inline: |';
  const startIdx = yamlContent.indexOf(startMarker);
  if (startIdx === -1) {
    console.log('    - svg_inline marker not found');
    return null;
  }

  // Find the end - look for next top-level key (shapes:, thumbnail:, etc.)
  const afterStart = yamlContent.substring(startIdx + startMarker.length);

  // Find where the SVG ends (next non-indented line that starts a new key)
  const lines = afterStart.split('\n');
  let svgLines = [];
  let foundEnd = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    // Check if this is a top-level YAML key (not indented, ends with :)
    if (i > 0 && line.match(/^[a-z_]+:/i) && !line.startsWith(' ')) {
      foundEnd = true;
      break;
    }
    svgLines.push(line);
  }

  // Remove leading empty lines and get SVG content
  const svg = svgLines
    .map(l => l.replace(/^  /, '')) // Remove 2-space indentation
    .join('\n')
    .trim();

  if (!svg.includes('<svg')) {
    console.log('    - No <svg> tag found in extracted content');
    return null;
  }

  return svg;
}

// Extract canvas dimensions
function extractCanvas(yamlContent) {
  const widthMatch = yamlContent.match(/reference_width:\s*(\d+)/);
  const heightMatch = yamlContent.match(/reference_height:\s*(\d+)/);
  return {
    width: widthMatch ? parseInt(widthMatch[1]) : 960,
    height: heightMatch ? parseInt(heightMatch[1]) : 540
  };
}

async function renderAndCompare() {
  const browser = await chromium.launch();
  const results = [];

  for (const t of templates) {
    console.log(`\nProcessing: ${t.yaml}`);

    try {
      const content = fs.readFileSync(t.yaml, 'utf8');
      const svgInline = extractSvgInline(content);

      if (!svgInline) {
        console.log(`  - No svg_inline found, skipping`);
        results.push({ template: t.yaml, status: 'no_svg' });
        continue;
      }

      const canvas = extractCanvas(content);
      console.log(`  - Canvas: ${canvas.width}x${canvas.height}`);
      console.log(`  - SVG length: ${svgInline.length} chars`);

      const html = `<!DOCTYPE html>
<html>
<head>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: ${canvas.width}px;
      height: ${canvas.height}px;
      background: #fff;
    }
    svg { display: block; }
  </style>
</head>
<body>
  ${svgInline}
</body>
</html>`;

      const page = await browser.newPage();
      await page.setContent(html);
      await page.setViewportSize({
        width: canvas.width,
        height: canvas.height
      });

      await page.screenshot({ path: t.output, fullPage: true });
      console.log(`  - Rendered: ${t.output}`);

      // Check if thumbnail exists
      if (fs.existsSync(t.thumb)) {
        console.log(`  - Thumbnail exists: ${t.thumb}`);
        results.push({ template: t.yaml, rendered: t.output, thumb: t.thumb, status: 'success' });
      } else {
        console.log(`  - Thumbnail NOT FOUND: ${t.thumb}`);
        results.push({ template: t.yaml, rendered: t.output, status: 'no_thumb' });
      }

      await page.close();

    } catch (err) {
      console.error(`  - Error: ${err.message}`);
      results.push({ template: t.yaml, status: 'error', error: err.message });
    }
  }

  await browser.close();

  console.log('\n=== Summary ===');
  for (const r of results) {
    const icon = r.status === 'success' ? '✓' : r.status === 'no_thumb' ? '?' : '✗';
    console.log(`${icon} ${path.basename(r.template)}`);
    if (r.rendered) console.log(`    Rendered: ${r.rendered}`);
  }

  console.log('\nRendered files are in the current directory.');
  console.log('Compare them with the thumbnails manually.');
}

renderAndCompare().catch(console.error);
