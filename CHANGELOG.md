# Changelog

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
- Comprehensive test suite: 30 backend tests, 5 frontend tests

### Security
- No credentials or secrets committed
- .env.example provided with blank values
- Keycloak realm import with demo user for development