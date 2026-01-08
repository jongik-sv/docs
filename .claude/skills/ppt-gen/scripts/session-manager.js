/**
 * Session Manager for PPT Generation Pipeline (v5.2)
 *
 * 슬라이드별 플랫 구조 PPT 생성 파이프라인 세션 관리:
 * 1단계(Setup) → 2단계(Outline) → 3단계(Matching) → 4단계(Content) → 5단계(PPTX)
 *
 * 데이터 구조:
 * - setup: 전역 설정 (1단계)
 * - slides[]: 슬라이드별 플랫 데이터 (2~5단계 누적)
 *
 * 생성 방식:
 * - HTML 기반: html_file, assets, text_content
 * - OOXML 기반: ooxml_bindings (문서양식 편집)
 * - SVG: 정적 그래픽으로만 사용 (바인딩 불가)
 *
 * USAGE:
 *   const SessionManager = require('./session-manager');
 *
 *   // 새 세션 생성
 *   const session = await SessionManager.create('스마트 물류 제안서');
 *
 *   // 1단계: 전역 설정
 *   await session.completeSetup({ presentation: {...}, theme: {...} });
 *
 *   // 2~5단계: 슬라이드별 데이터 누적
 *   await session.updateSlide(0, { title: '표지', purpose: 'cover' });
 *   await session.updateSlide(0, { template_id: 'cover-centered1' });
 *   await session.updateSlide(0, { html_file: 'slide-001.html' });
 *   await session.updateSlide(0, { generated: true });
 *
 *   // 세션 재개
 *   const session = await SessionManager.resume('2026-01-09_143025_a7b2c3d4');
 */

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

const DEFAULT_OUTPUT_DIR = path.join(process.cwd(), 'output');

const STATUS = {
  IN_PROGRESS: 'in_progress',
  PAUSED: 'paused',
  COMPLETED: 'completed',
  FAILED: 'failed'
};

const STAGE_FILES = {
  1: 'stage-1.json',
  2: 'stage-2.json',
  3: 'stage-3.json',
  4: 'stage-4.json',
  5: 'stage-5.json'
};

function generateSessionId() {
  const now = new Date();
  const date = now.toISOString().split('T')[0];
  const time = now.toTimeString().split(' ')[0].replace(/:/g, '');
  const hash = crypto.randomBytes(4).toString('hex');
  return `${date}_${time}_${hash}`;
}

/**
 * Session 클래스 - 슬라이드별 플랫 구조
 */
class Session {
  constructor(id, sessionDir, state = {}) {
    this.id = id;
    this.sessionDir = sessionDir;
    this.state = state;
  }

  async save(stageNum) {
    this.state.session.updated_at = new Date().toISOString();
    const stageFile = path.join(this.sessionDir, STAGE_FILES[stageNum]);
    await fs.writeFile(stageFile, JSON.stringify(this.state, null, 2), 'utf-8');
  }

  // === 1단계: Setup (전역 설정) ===
  async completeSetup(data) {
    this.state.setup = {
      ...data,
      completed_at: new Date().toISOString()
    };
    this.state.current_stage = 1;
    this.state.slides = [];
    await this.save(1);
    return this.state.setup;
  }

  // === 2~5단계: 슬라이드 데이터 누적 (플랫 병합) ===
  async updateSlide(index, data) {
    await this._loadLatestState();

    // 슬라이드 찾기 또는 생성
    let slide = this.state.slides.find(s => s.index === index);
    if (!slide) {
      slide = { index };
      this.state.slides.push(slide);
      this.state.slides.sort((a, b) => a.index - b.index);
    }

    // 플랫하게 데이터 병합
    Object.assign(slide, data);

    // 현재 단계 추론
    const stage = this._inferStage(slide);
    this.state.current_stage = Math.max(this.state.current_stage || 1, stage);

    await this.save(stage);
    return slide;
  }

  // 슬라이드 데이터에서 현재 단계 추론
  _inferStage(slide) {
    if (slide.generated) return 5;
    if (slide.html_file || slide.ooxml_bindings) return 4;
    if (slide.template_id) return 3;
    if (slide.title || slide.purpose) return 2;
    return 1;
  }

  // === 5단계: 최종 생성 완료 ===
  async completeGeneration(outputData) {
    await this._loadLatestState();

    this.state.output = {
      ...outputData,
      completed_at: new Date().toISOString()
    };
    this.state.session.status = STATUS.COMPLETED;
    this.state.current_stage = 5;

    await this.save(5);
    return this.state.output;
  }

  // === 유틸리티 ===
  async _loadLatestState() {
    for (let i = 5; i >= 1; i--) {
      const stageFile = path.join(this.sessionDir, STAGE_FILES[i]);
      try {
        const content = await fs.readFile(stageFile, 'utf-8');
        this.state = JSON.parse(content);
        return;
      } catch (err) {
        if (err.code !== 'ENOENT') throw err;
      }
    }
  }

  async readLatestState() {
    await this._loadLatestState();
    return this.state;
  }

  getSlide(index) {
    return this.state.slides?.find(s => s.index === index);
  }

  getSlidesDir() {
    return path.join(this.sessionDir, 'slides');
  }

  getAssetsDir() {
    return path.join(this.sessionDir, 'assets');
  }

  getOutputPath() {
    return path.join(this.sessionDir, 'output.pptx');
  }

  getThumbnailsDir() {
    return path.join(this.sessionDir, 'thumbnails');
  }

  getSummary() {
    return {
      id: this.id,
      title: this.state.session?.title,
      status: this.state.session?.status,
      current_stage: this.state.current_stage,
      slide_count: this.state.slides?.length || 0,
      created_at: this.state.session?.created_at,
      updated_at: this.state.session?.updated_at,
      path: this.sessionDir
    };
  }
}

/**
 * SessionManager 클래스
 */
class SessionManager {
  constructor(outputDir = DEFAULT_OUTPUT_DIR) {
    this.outputDir = outputDir;
  }

  async create(title = 'Untitled Presentation') {
    const sessionId = generateSessionId();
    const sessionDir = path.join(this.outputDir, sessionId);

    await fs.mkdir(sessionDir, { recursive: true });
    await fs.mkdir(path.join(sessionDir, 'slides'), { recursive: true });
    await fs.mkdir(path.join(sessionDir, 'assets'), { recursive: true });
    await fs.mkdir(path.join(sessionDir, 'assets', 'icons'), { recursive: true });
    await fs.mkdir(path.join(sessionDir, 'assets', 'images'), { recursive: true });
    await fs.mkdir(path.join(sessionDir, 'thumbnails'), { recursive: true });

    const state = {
      session: {
        id: sessionId,
        title: title,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        status: STATUS.IN_PROGRESS
      },
      current_stage: 0,
      setup: null,
      slides: [],
      output: null
    };

    return new Session(sessionId, sessionDir, state);
  }

  async resume(sessionId) {
    const sessionDir = path.join(this.outputDir, sessionId);
    const session = new Session(sessionId, sessionDir, {});
    await session._loadLatestState();

    if (!session.state.session) {
      throw new Error(`Session not found: ${sessionId}`);
    }

    return session;
  }

  async listSessions() {
    try {
      const dirs = await fs.readdir(this.outputDir);
      const sessions = [];

      for (const dir of dirs) {
        const sessionDir = path.join(this.outputDir, dir);
        const session = new Session(dir, sessionDir, {});

        try {
          await session._loadLatestState();
          if (session.state.session) {
            sessions.push(session.getSummary());
          }
        } catch (err) {
          // Skip invalid sessions
        }
      }

      sessions.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      return sessions;
    } catch (err) {
      if (err.code === 'ENOENT') return [];
      throw err;
    }
  }

  async getInProgressSessions() {
    const sessions = await this.listSessions();
    return sessions.filter(s => s.status === STATUS.IN_PROGRESS || s.status === STATUS.PAUSED);
  }

  async deleteSession(sessionId) {
    const sessionDir = path.join(this.outputDir, sessionId);
    await fs.rm(sessionDir, { recursive: true, force: true });
  }
}

const defaultManager = new SessionManager();

module.exports = {
  SessionManager,
  Session,
  STATUS,
  STAGE_FILES,
  generateSessionId,
  create: (title) => defaultManager.create(title),
  resume: (sessionId) => defaultManager.resume(sessionId),
  listSessions: () => defaultManager.listSessions(),
  getInProgressSessions: () => defaultManager.getInProgressSessions(),
  deleteSession: (sessionId) => defaultManager.deleteSession(sessionId)
};
