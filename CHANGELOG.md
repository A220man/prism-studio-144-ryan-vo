# Changelog

## 1.4.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.3.0 — work-in-progress checkpoint

### Fixed
- Fixed frontend Callback component to call checkAuth() after OAuth redirect, ensuring user state is updated immediately after login
- All 30 backend tests pass
- All 6 frontend tests pass

Partial code published for continued development. Known issues: STATUS.md.

## 1.2.0 — work-in-progress checkpoint

### Added - OIDC Authentication with Keycloak (PKCE flow)
- Backend: Proper PKCE S256 code challenge generation and verification
- Backend: Authorization code exchange with Keycloak token endpoint
- Backend: Secure httpOnly cookie storage for access/refresh tokens
- Backend: Token validation from both Authorization header and cookies
- Frontend: AuthContext for authentication state management
- Frontend: Login/logout UI in header with user info and role badges
- Frontend: Callback route for OAuth flow completion
- Frontend: API client configured with credentials: 'include' for cookie auth
- Loading state during initial auth check

### Fixed
- Updated auth tests to match new PKCE flow implementation
- All 30 backend tests pass
- All 6 frontend tests pass

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

### Fixed
- Removed duplicate `httpx` dependency in `backend/requirements.txt`
- Added `asyncpg` dependency for PostgreSQL support in Docker deployment
- Added `postgres` optional dependency group in `pyproject.toml`

### Verified
- All 30 backend tests pass
- All 6 frontend tests pass
- Frontend TypeScript type check passes
- Frontend production build succeeds

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-10-23

### Added
- Initial project skeleton with FastAPI backend and React/TypeScript/Vite frontend
- Docker Compose configuration with PostgreSQL, Keycloak, backend, and frontend
- Health check endpoint at `/api/health`
- Lesson API with list, detail, search, and pagination
- Three interactive workflow generators:
  - Skill Creation Wizard (generates `.claude/skills/*.yaml`)
  - Subagent Builder (generates `.claude/agents/*.md`)
  - MCP Server Configurator (generates `.mcp.json`)
- Copy-to-clipboard functionality for templates and examples
- Responsive dark-theme UI with professional styling
- CI/CD workflow with backend tests, frontend build/test, and Docker builds
- Portfolio metadata and documentation structure
- JWT-based authentication with role-based access control (viewer, operator, admin)
- Multi-provider LLM adapter framework (OpenAI-compatible, Anthropic, Gemini, Ollama)
- SQLAlchemy models with Lesson, Section, Example, Template, UserProgress
- Comprehensive test suite: 30 backend tests, 6 frontend tests
- Lesson list with category/difficulty filters and pagination (server-side)

### Security
- No credentials or secrets committed
- .env.example provided with blank values
- Keycloak realm import with demo user for development