# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

project-skeleton

## Roadmap

### project-skeleton — Project Skeleton with FastAPI + React + Docker + CI

Status: done

Acceptance:
- FastAPI app runs at /api/health
- React + TypeScript + Vite frontend builds and serves
- Docker Compose starts backend, frontend, Keycloak, PostgreSQL
- CI workflow runs backend tests, frontend build/test, Docker builds
- portfolio.json, README, LICENSE, CHANGELOG, .gitignore, .env.example present

Implementation: `backend/app/main.py`, `backend/app/core/config.py`, `backend/app/core/database.py`, `backend/app/core/security.py`, `backend/app/api/health.py`, `backend/app/api/lessons.py`, `backend/app/api/workflows.py`, `backend/app/api/auth.py`, `backend/app/models/models.py`, `backend/app/services/lesson_service.py`, `backend/app/services/workflow_service.py`, `backend/app/services/llm_service.py`, `backend/tests/test_health.py`, `backend/tests/test_lessons.py`, `backend/tests/test_workflows.py`, `backend/tests/test_auth.py`, `backend/tests/test_llm.py`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/index.css`, `frontend/src/components/Layout.tsx`, `frontend/src/components/LessonList.tsx`, `frontend/src/components/LessonDetail.tsx`, `frontend/src/components/Workflows.tsx`, `frontend/src/api/client.ts`, `frontend/vite.config.ts`, `frontend/package.json`, `frontend/Dockerfile`, `frontend/nginx.conf`, `backend/Dockerfile`, `backend/requirements.txt`, `compose.yaml`, `keycloak/realm.json`, `.env.example`, `portfolio.json`, `README.md`, `LICENSE`, `CHANGELOG.md`, `pyproject.toml`, `.gitignore`, `.github/workflows/ci.yml`

Tests: `backend/tests/test_health.py`, `backend/tests/test_lessons.py`, `backend/tests/test_workflows.py`, `backend/tests/test_auth.py`, `backend/tests/test_llm.py`, `frontend/src/components/LessonList.test.tsx`

### auth-oidc — OIDC Authentication with Keycloak (PKCE flow)

Status: planned

Acceptance:
- Login redirects to Keycloak
- Callback exchanges code for tokens with PKCE
- Access token validated on protected endpoints
- Roles: viewer, operator, admin enforced
- Logout clears session

### lesson-engine — Claude Code Lesson Engine (Core Domain)

Status: planned

Acceptance:
- Lessons stored in SQLite with sections, examples, templates
- API: list lessons, get lesson detail, search lessons
- Deterministic lesson progression tracking
- Copy-paste template extraction works offline

### workflow-templates — Interactive Workflow Templates (3+ workflows)

Status: planned

Acceptance:
- Workflow 1: Skill Creation Wizard → generates .claude/skills/ file
- Workflow 2: Subagent Builder → generates agent definition
- Workflow 3: MCP Server Configurator → generates MCP config
- Templates use deterministic algorithms, no LLM required

### llm-explanations — Opt-in LLM Explanations (Advisory, Grounded)

Status: planned

Acceptance:
- LLM_API_KEY optional, providers: OpenAI-compatible, Anthropic, Gemini, Ollama
- Explanations labeled advisory, grounded in lesson content
- Clear provider errors, no fabricated responses
- Works without any LLM key

### frontend-dashboard — React Dashboard with Lesson Viewer & Workflow UI

Status: planned

Acceptance:
- Lesson list with search/filter
- Lesson detail with formatted content, copy-paste buttons
- Workflow wizard forms with live preview
- Loading/error/empty states throughout
- Responsive professional UI

### docs-packaging — Documentation, Packaging, Portfolio Metadata

Status: planned

Acceptance:
- README with install/run/test, Mermaid diagram, API ref, AI/ML evaluation
- portfolio.json with schema_version, workflows, auth, llm_providers
- CHANGELOG.md actual changes
- docs/ API/architecture/deployment docs
- Source budget 50-150KB, 8+ backend modules, 5+ frontend modules

