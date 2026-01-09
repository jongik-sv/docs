/**
 * HTML Templates for PPT Content Design
 *
 * 콘텐츠 템플릿별 HTML 렌더러
 * - 각 콘텐츠 템플릿(grid, timeline, chart 등)을 HTML로 렌더링
 * - 테마 색상 토큰을 CSS 변수로 변환
 * - html2pptx.js와 함께 사용
 *
 * Usage:
 *   const { renderTemplate } = require('./html-templates');
 *   const html = renderTemplate('deepgreen-grid-3col1', data, theme);
 */

// 기본 테마 색상 (동국시스템즈)
const DEFAULT_THEME = {
  primary: '#002452',
  secondary: '#C51F2A',
  accent: '#A1BFB4',
  dark: '#153325',
  dark_text: '#262626',
  light: '#FFFFFF',
  gray: '#B6B6B6',
  surface: '#F8F9FA',
  background: '#FFFFFF'
};

// Deep Green 테마
const DEEPGREEN_THEME = {
  primary: '#22523B',
  secondary: '#153325',
  accent: '#A1BFB4',
  dark: '#153325',
  dark_text: '#183C2B',
  light: '#FFFFFF',
  gray: '#B6B6B6',
  surface: '#F5F7F6',
  background: '#FFFFFF'
};

/**
 * 테마 색상을 CSS 변수로 변환
 */
function generateThemeCSS(theme) {
  const colors = { ...DEFAULT_THEME, ...theme };
  return `
    :root {
      --primary: ${colors.primary};
      --secondary: ${colors.secondary};
      --accent: ${colors.accent};
      --dark: ${colors.dark};
      --dark-text: ${colors.dark_text};
      --light: ${colors.light};
      --gray: ${colors.gray};
      --surface: ${colors.surface};
      --background: ${colors.background};
    }
  `;
}

/**
 * 기본 슬라이드 스타일
 */
const BASE_STYLES = `
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', Arial, sans-serif;
    width: 1084px;
    height: 750px;
    overflow: hidden;
    background: var(--background);
  }
  .slide {
    width: 1084px;
    height: 750px;
    padding: 35px 40px;
    position: relative;
  }
  h1.main-title {
    font-size: 19px;
    color: var(--primary);
    font-weight: 600;
    margin-bottom: 8px;
  }
  p.action-title {
    font-size: 17px;
    color: var(--dark-text);
    font-weight: 500;
    margin-bottom: 25px;
    line-height: 1.5;
  }
  p.footer {
    position: absolute;
    bottom: 15px;
    right: 30px;
    font-size: 8px;
    color: var(--gray);
  }
`;

/**
 * 3열 그리드 템플릿 (deepgreen-grid-3col1)
 */
function renderGrid3Col(data, theme) {
  const { title, subtitle, cards = [] } = data;
  const colors = { ...DEEPGREEN_THEME, ...theme };

  const cardHTML = cards.slice(0, 6).map((card, i) => {
    const isTopRow = i < 3;
    const bgColor = isTopRow ? colors.primary : colors.secondary;

    return `
      <div class="card" style="background: ${bgColor}; position: relative;">
        <div class="card-decoration" style="
          position: absolute;
          top: 0;
          left: 0;
          width: 0;
          height: 0;
          border-style: solid;
          border-width: 80px 80px 0 0;
          border-color: rgba(255,255,255,0.08) transparent transparent transparent;
        "></div>
        <div class="number-badge" style="
          position: absolute;
          top: -12px;
          left: -8px;
          width: 36px;
          height: 36px;
          background: ${colors.accent};
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 700;
          font-size: 14px;
          color: ${colors.dark};
          box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        "><p style="margin:0;">${card.number || i + 1}</p></div>
        <div class="card-content" style="padding: 20px 15px 15px 15px;">
          <h3 class="card-title" style="
            font-size: 14px;
            font-weight: 600;
            color: ${colors.light};
            margin-bottom: 8px;
          ">${card.title || ''}</h3>
          <p class="card-desc" style="
            font-size: 11px;
            color: rgba(255,255,255,0.85);
            line-height: 1.6;
          ">${(card.description || '').replace(/\n/g, '<br>')}</p>
        </div>
      </div>
    `;
  }).join('');

  return `<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  ${generateThemeCSS(colors)}
  ${BASE_STYLES}
  .grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-top: 30px;
  }
  .card {
    border-radius: 12px;
    min-height: 160px;
    overflow: hidden;
  }
</style>
</head><body>
<div class="slide">
  <h1 class="main-title">${title || ''}</h1>
  <p class="action-title">${subtitle || ''}</p>
  <div class="grid-container">
    ${cardHTML}
  </div>
</div>
</body></html>`;
}

/**
 * 아이콘 그리드 템플릿 (deepgreen-grid-icon1)
 */
function renderGridIcon(data, theme) {
  const { title, subtitle, items = [] } = data;
  const colors = { ...DEEPGREEN_THEME, ...theme };

  const itemHTML = items.slice(0, 4).map((item, i) => `
    <div class="icon-card" style="
      background: ${colors.surface};
      border-radius: 12px;
      padding: 25px 20px;
      text-align: center;
    ">
      <div class="icon-box" style="
        width: 60px;
        height: 60px;
        background: ${colors.primary};
        border-radius: 12px;
        margin: 0 auto 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        color: ${colors.light};
      "><p style="margin:0;">${item.icon || '📦'}</p></div>
      <h3 class="icon-title" style="
        font-size: 15px;
        color: ${colors.dark_text};
        font-weight: 600;
        margin-bottom: 8px;
      ">${item.title || ''}</h3>
      <p class="icon-desc" style="
        font-size: 12px;
        color: ${colors.gray};
        line-height: 1.5;
      ">${(item.description || '').replace(/\n/g, '<br>')}</p>
    </div>
  `).join('');

  return `<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  ${generateThemeCSS(colors)}
  ${BASE_STYLES}
  .icon-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-top: 30px;
  }
</style>
</head><body>
<div class="slide">
  <h1 class="main-title">${title || ''}</h1>
  <p class="action-title">${subtitle || ''}</p>
  <div class="icon-grid">
    ${itemHTML}
  </div>
</div>
</body></html>`;
}

/**
 * 타임라인 템플릿 (deepgreen-timeline1)
 */
function renderTimeline(data, theme) {
  const { title, subtitle, steps = [] } = data;
  const colors = { ...DEEPGREEN_THEME, ...theme };

  const stepHTML = steps.slice(0, 5).map((step, i) => `
    <div class="step" style="
      text-align: center;
      width: 160px;
      position: relative;
      z-index: 1;
    ">
      <div class="step-number" style="
        width: 60px;
        height: 60px;
        background: ${colors.primary};
        border-radius: 50%;
        color: ${colors.light};
        font-size: 24px;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      "><p style="margin:0;">${step.number || i + 1}</p></div>
      <h3 class="step-title" style="
        font-size: 14px;
        color: ${colors.dark_text};
        font-weight: 600;
        margin-bottom: 6px;
      ">${step.title || ''}</h3>
      <p class="step-desc" style="
        font-size: 11px;
        color: ${colors.gray};
        line-height: 1.4;
      ">${step.description || ''}</p>
    </div>
  `).join('');

  return `<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  ${generateThemeCSS(colors)}
  ${BASE_STYLES}
  .timeline {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-top: 50px;
    position: relative;
    padding: 0 30px;
  }
  .timeline::before {
    content: '';
    position: absolute;
    top: 30px;
    left: 80px;
    right: 80px;
    height: 3px;
    background: linear-gradient(90deg, ${colors.primary} 0%, ${colors.accent} 100%);
  }
</style>
</head><body>
<div class="slide">
  <h1 class="main-title">${title || ''}</h1>
  <p class="action-title">${subtitle || ''}</p>
  <div class="timeline">
    ${stepHTML}
  </div>
</div>
</body></html>`;
}

/**
 * 통계 카드 템플릿 (deepgreen-feature-cards1)
 */
function renderStats(data, theme) {
  const { title, subtitle, stats = [] } = data;
  const colors = { ...DEEPGREEN_THEME, ...theme };

  const statColors = [colors.primary, colors.secondary, colors.gray];

  const statHTML = stats.slice(0, 3).map((stat, i) => `
    <div class="stat-card" style="
      width: 280px;
      background: ${colors.surface};
      border-radius: 16px;
      padding: 35px 25px;
      text-align: center;
    ">
      <div class="stat-value" style="
        font-size: 52px;
        font-weight: 700;
        color: ${statColors[i] || colors.primary};
        margin-bottom: 8px;
        display: flex; justify-content: center;
      "><p style="margin:0;">${stat.value || '0'}</p></div>
      <h3 class="stat-label" style="
        font-size: 16px;
        font-weight: 600;
        color: ${statColors[i] || colors.primary};
        margin-bottom: 8px;
      ">${stat.label || ''}</h3>
      <p class="stat-desc" style="
        font-size: 12px;
        color: ${colors.gray};
      ">${stat.description || ''}</p>
    </div>
  `).join('');

  return `<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  ${generateThemeCSS(colors)}
  ${BASE_STYLES}
  .stats-grid {
    display: flex;
    gap: 30px;
    margin-top: 40px;
    justify-content: center;
  }
</style>
</head><body>
<div class="slide">
  <h1 class="main-title">${title || ''}</h1>
  <p class="action-title">${subtitle || ''}</p>
  <div class="stats-grid">
    ${statHTML}
  </div>
</div>
</body></html>`;
}

/**
 * 불릿 리스트 템플릿 (텍스트 중심)
 */
function renderBulletList(data, theme) {
  const { title, subtitle, items = [] } = data;
  const colors = { ...DEFAULT_THEME, ...theme };

  const itemHTML = items.map(item => `
    <li style="margin-bottom: 12px;">${item}</li>
  `).join('');

  return `<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  ${generateThemeCSS(colors)}
  ${BASE_STYLES}
  .bullet-list {
    font-size: 16px;
    color: ${colors.dark_text};
    line-height: 2.0;
    list-style: none;
    padding-left: 25px;
  }
  .bullet-list li::before {
    content: "▐";
    color: ${colors.primary};
    margin-right: 15px;
    font-size: 12px;
  }
</style>
</head><body>
<div class="slide">
  <h1 class="main-title">${title || ''}</h1>
  <p class="action-title">${subtitle || ''}</p>
  <ul class="bullet-list">
    ${itemHTML}
  </ul>
</div>
</body></html>`;
}

/**
 * Q&A / 클로징 슬라이드
 */
function renderClosing(data, theme) {
  const { title = 'Q&A', subtitle = '', description = '' } = data;
  const colors = { ...DEFAULT_THEME, ...theme };

  return `<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  ${generateThemeCSS(colors)}
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Malgun Gothic', Arial, sans-serif;
    width: 1084px;
    height: 750px;
    overflow: hidden;
  }
  .closing-slide {
    width: 1084px;
    height: 750px;
    background: ${colors.primary};
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  .closing-title {
    color: ${colors.light};
    font-size: 56px;
    font-weight: 700;
    margin-bottom: 25px;
  }
  .closing-subtitle {
    color: ${colors.accent};
    font-size: 20px;
    margin-bottom: 10px;
  }
  .closing-desc {
    color: rgba(255,255,255,0.7);
    font-size: 16px;
  }
</style>
</head><body>
<div class="closing-slide">
  <h1 class="closing-title">${title}</h1>
  <p class="closing-subtitle">${subtitle}</p>
  <p class="closing-desc">${description}</p>
</div>
</body></html>`;
}

/**
 * 막대 차트 템플릿 (deepgreen-chart-bar1)
 */
function renderBarChart(data, theme) {
  const { title, subtitle, chart_data = {} } = data;
  const colors = { ...DEFAULT_THEME, ...theme };

  const categories = chart_data.categories || [];
  const series = chart_data.series || [];

  // 최대값 계산
  let maxVal = 0;
  series.forEach(s => {
    (s.values || []).forEach(v => {
      if (v > maxVal) maxVal = v;
    });
  });
  if (maxVal === 0) maxVal = 1;

  // 시리즈 색상
  const seriesColors = [colors.primary, colors.secondary, colors.accent];

  // 막대 생성
  let barsHTML = '';
  const barWidth = 100 / categories.length;

  categories.forEach((cat, catIdx) => {
    const groupLeft = catIdx * barWidth + barWidth * 0.1;
    const groupWidth = barWidth * 0.8;

    series.forEach((ser, serIdx) => {
      const values = ser.values || [];
      const value = values[catIdx] || 0;
      const heightPct = (value / maxVal) * 100;
      const barColor = seriesColors[serIdx % seriesColors.length];
      const seriesBarWidth = groupWidth / series.length;
      const barLeft = groupLeft + serIdx * seriesBarWidth;

      barsHTML += `
        <div class="bar" style="
          position: absolute;
          left: ${barLeft}%;
          bottom: 50px;
          width: ${seriesBarWidth * 0.8}%;
          height: ${heightPct * 0.8}%;
          background: ${barColor};
          border-radius: 4px 4px 0 0;
          display: flex;
          flex-direction: column;
          align-items: center;
        ">
          <div class="bar-value" style="
            position: absolute;
            top: -25px;
            font-size: 12px;
            font-weight: 600;
            color: ${colors.dark_text};
            display: flex; justify-content: center;
          "><p style="margin:0;">${value}</p></div>
        </div>
      `;
    });

    // 카테고리 레이블
    barsHTML += `
      <div class="cat-label" style="
        position: absolute;
        left: ${groupLeft}%;
        bottom: 15px;
        width: ${groupWidth}%;
        text-align: center;
        font-size: 12px;
        color: ${colors.gray};
      "><p style="margin:0;">${cat}</p></div>
    `;
  });

  // 범례
  let legendHTML = '';
  series.forEach((ser, idx) => {
    const color = seriesColors[idx % seriesColors.length];
    legendHTML += `
      <div style="display: flex; align-items: center; margin-right: 20px;">
        <div style="width: 16px; height: 16px; background: ${color}; border-radius: 3px; margin-right: 6px;"></div>
        <span style="font-size: 12px; color: ${colors.dark_text};">${ser.name || `시리즈 ${idx + 1}`}</span>
      </div>
    `;
  });

  return `<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  ${generateThemeCSS(colors)}
  ${BASE_STYLES}
  .chart-container {
    position: relative;
    width: 100%;
    height: 450px;
    margin-top: 20px;
    background: ${colors.surface};
    border-radius: 12px;
    padding: 20px;
  }
  .chart-area {
    position: relative;
    height: 350px;
    border-bottom: 2px solid ${colors.gray};
    border-left: 2px solid ${colors.gray};
    margin-left: 40px;
  }
  .legend {
    display: flex;
    justify-content: center;
    margin-top: 15px;
  }
</style>
</head><body>
<div class="slide">
  <h1 class="main-title">${title || ''}</h1>
  <p class="action-title">${subtitle || ''}</p>
  <div class="chart-container">
    <div class="chart-area">
      ${barsHTML}
    </div>
    <div class="legend">
      ${legendHTML}
    </div>
  </div>
</div>
</body></html>`;
}

/**
 * 프로세스/플로우 템플릿
 */
function renderProcess(data, theme) {
  const { title, subtitle, steps = [] } = data;
  const colors = { ...DEEPGREEN_THEME, ...theme };

  const stepsHTML = steps.slice(0, 5).map((step, i) => {
    const isLast = i === steps.length - 1;
    return `
      <div class="process-step" style="
        display: flex;
        align-items: center;
        flex: 1;
      ">
        <div class="step-box" style="
          background: ${i % 2 === 0 ? colors.primary : colors.secondary};
          border-radius: 12px;
          padding: 20px 25px;
          text-align: center;
          min-width: 140px;
        ">
          <div style="
            font-size: 28px;
            font-weight: 700;
            color: ${colors.light};
            margin-bottom: 8px;
          "><p style="margin:0;">${step.number || i + 1}</p></div>
          <h3 style="
            font-size: 14px;
            font-weight: 600;
            color: ${colors.light};
            margin-bottom: 5px;
          ">${step.title || ''}</h3>
          <p style="
            font-size: 11px;
            color: rgba(255,255,255,0.8);
          ">${step.description || ''}</p>
        </div>
        ${!isLast ? `
          <div class="arrow" style="
            width: 40px;
            height: 2px;
            background: ${colors.accent};
            position: relative;
            margin: 0 5px;
          ">
            <div style="
              position: absolute;
              right: -8px;
              top: -6px;
              width: 0;
              height: 0;
              border-left: 10px solid ${colors.accent};
              border-top: 7px solid transparent;
              border-bottom: 7px solid transparent;
            "></div>
          </div>
        ` : ''}
      </div>
    `;
  }).join('');

  return `<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  ${generateThemeCSS(colors)}
  ${BASE_STYLES}
  .process-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 50px;
    padding: 0 20px;
  }
</style>
</head><body>
<div class="slide">
  <h1 class="main-title">${title || ''}</h1>
  <p class="action-title">${subtitle || ''}</p>
  <div class="process-container">
    ${stepsHTML}
  </div>
</div>
</body></html>`;
}

/**
 * 템플릿 렌더러 매핑
 */
const TEMPLATE_RENDERERS = {
  'deepgreen-grid-3col1': renderGrid3Col,
  'deepgreen-grid-icon1': renderGridIcon,
  'deepgreen-grid-text1': renderGrid3Col,
  'deepgreen-timeline1': renderTimeline,
  'deepgreen-feature-cards1': renderStats,
  'deepgreen-stats1': renderStats,
  'deepgreen-closing1': renderClosing,
  'deepgreen-chart-bar1': renderBarChart,
  'deepgreen-process1': renderProcess,
  'deepgreen-bullets1': renderBulletList,
  // 별칭
  'grid-3col': renderGrid3Col,
  'grid-icon': renderGridIcon,
  'timeline': renderTimeline,
  'stats': renderStats,
  'bullets': renderBulletList,
  'closing': renderClosing,
  'chart-bar': renderBarChart,
  'process': renderProcess,
};

/**
 * 메인 렌더 함수
 *
 * @param {string} templateId - 콘텐츠 템플릿 ID
 * @param {Object} data - 바인딩할 데이터
 * @param {Object} theme - 테마 색상 (옵션)
 * @returns {string} 렌더링된 HTML
 */
function renderTemplate(templateId, data, theme = {}) {
  const renderer = TEMPLATE_RENDERERS[templateId];

  if (!renderer) {
    console.warn(`Unknown template: ${templateId}, falling back to bullet list`);
    return renderBulletList(data, theme);
  }

  return renderer(data, theme);
}

/**
 * 지원되는 템플릿 목록 반환
 */
function getSupportedTemplates() {
  return Object.keys(TEMPLATE_RENDERERS);
}

module.exports = {
  renderTemplate,
  getSupportedTemplates,
  // 개별 렌더러 내보내기
  renderGrid3Col,
  renderGridIcon,
  renderTimeline,
  renderStats,
  renderBulletList,
  renderClosing,
  renderBarChart,
  renderProcess,
  // 테마
  DEFAULT_THEME,
  DEEPGREEN_THEME,
  generateThemeCSS,
  BASE_STYLES,
};
