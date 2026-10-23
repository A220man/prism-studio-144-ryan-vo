from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Lesson, Section, Example, Template, UserProgress, DifficultyLevel
from app.core.database import get_session


class LessonService:
    @staticmethod
    async def list_lessons(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 20,
        category: Optional[str] = None,
        difficulty: Optional[DifficultyLevel] = None,
        search: Optional[str] = None,
    ) -> tuple[list[Lesson], int]:
        query = select(Lesson)
        count_query = select(func.count(Lesson.id))

        if category:
            query = query.where(Lesson.category == category)
            count_query = count_query.where(Lesson.category == category)

        if difficulty:
            query = query.where(Lesson.difficulty == difficulty)
            count_query = count_query.where(Lesson.difficulty == difficulty)

        if search:
            search_term = f"%{search.lower()}%"
            query = query.where(
                (Lesson.title.ilike(search_term)) |
                (Lesson.description.ilike(search_term)) |
                (Lesson.category.ilike(search_term))
            )
            count_query = count_query.where(
                (Lesson.title.ilike(search_term)) |
                (Lesson.description.ilike(search_term)) |
                (Lesson.category.ilike(search_term))
            )

        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(Lesson.category, Lesson.difficulty, Lesson.title)
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await db.execute(query)
        lessons = result.scalars().all()

        return list(lessons), total

    @staticmethod
    async def get_lesson(db: AsyncSession, lesson_id: str) -> Optional[Lesson]:
        result = await db.execute(
            select(Lesson)
            .where(Lesson.id == lesson_id)
            .options(
                selectinload(Lesson.sections)
                .selectinload(Section.examples),
                selectinload(Lesson.sections)
                .selectinload(Section.templates),
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def search_lessons(db: AsyncSession, q: str, limit: int = 10) -> list[Lesson]:
        search_term = f"%{q.lower()}%"
        result = await db.execute(
            select(Lesson)
            .where(
                (Lesson.title.ilike(search_term)) |
                (Lesson.description.ilike(search_term)) |
                (Lesson.category.ilike(search_term))
            )
            .limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def seed_lessons(db: AsyncSession) -> None:
        existing = await db.execute(select(func.count(Lesson.id)))
        if existing.scalar() > 0:
            return

        lessons_data = [
            {
                "id": "cli-basics",
                "title": "CLI Basics",
                "description": "Learn the fundamental Claude Code commands and navigation.",
                "category": "Fundamentals",
                "difficulty": DifficultyLevel.BEGINNER,
                "estimated_minutes": 15,
                "sections": [
                    {
                        "id": "cli-intro",
                        "title": "Introduction to Claude Code CLI",
                        "content": "Claude Code is a command-line interface that brings Anthropic's Claude directly into your terminal. It understands your codebase and can help with coding tasks, debugging, and more.\n\nKey concepts:\n- **Commands** start with `/` (e.g., `/help`, `/init`, `/skill`)\n- **Natural language** works for most tasks\n- **Context** is automatically gathered from your project",
                        "order": 0,
                        "examples": [
                            {
                                "id": "ex-cli-help",
                                "title": "Getting Help",
                                "code": "/help\n# Shows all available commands\n\n/help skills\n# Shows help for skills command",
                                "language": "bash",
                                "order": 0,
                            },
                            {
                                "id": "ex-cli-init",
                                "title": "Initializing a Project",
                                "code": "cd my-project\n/claude init\n# Creates .claude/ directory with default config",
                                "language": "bash",
                                "order": 1,
                            },
                        ],
                        "templates": [
                            {
                                "id": "tmpl-claude-json",
                                "title": "Basic .claude.json",
                                "content": '{\n  "model": "sonnet",\n  "permissions": {\n    "allow": ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Task"]\n  }\n}',
                                "filename": ".claude.json",
                                "order": 0,
                            },
                        ],
                    },
                    {
                        "id": "cli-navigation",
                        "title": "Navigation and File Operations",
                        "content": "Claude Code provides powerful file operations through natural language and built-in tools.\n\nCommon operations:\n- **Read files**: \"Read the main.py file\"\n- **Write files**: \"Create a new config.yaml with...\"\n- **Edit files**: \"Change the port to 8080 in config.yaml\"\n- **Search**: \"Find all notes in the codebase\"\n- **Glob**: \"List all Python files in src/\"",
                        "order": 1,
                        "examples": [
                            {
                                "id": "ex-cli-read",
                                "title": "Reading Files",
                                "code": "> Read the README.md file\n\n# Output shows file contents with line numbers",
                                "language": "text",
                                "order": 0,
                            },
                            {
                                "id": "ex-cli-grep",
                                "title": "Searching Code",
                                "code": "> Find all functions named 'handle_*' in src/\n\n# Uses grep tool internally",
                                "language": "text",
                                "order": 1,
                            },
                        ],
                        "templates": [],
                    },
                ],
            },
            {
                "id": "skills-fundamentals",
                "title": "Skills Fundamentals",
                "description": "Create reusable skills to extend Claude Code with custom commands.",
                "category": "Skills",
                "difficulty": DifficultyLevel.BEGINNER,
                "estimated_minutes": 20,
                "sections": [
                    {
                        "id": "skills-concept",
                        "title": "What Are Skills?",
                        "content": "Skills are reusable command definitions that live in `.claude/skills/`. They let you create custom `/` commands with predefined behavior, tools, and examples.\n\nSkill structure:\n- **Frontmatter**: name, description, model, tools, allowed-tools\n- **Body**: Instructions for Claude on how to execute the skill\n- **Examples**: Usage examples shown in `/help`\n\nSkill precedence (highest to lowest):\n1. **Enterprise** (organization-wide)\n2. **Personal** (`~/.claude/skills/`)\n3. **Project** (`.claude/skills/`)\n\nPlugin skills use `plugin-name:skill` namespace and don't conflict.",
                        "order": 0,
                        "examples": [
                            {
                                "id": "ex-skill-structure",
                                "title": "Skill File Structure",
                                "code": "---\nname: my-skill\ndescription: Does something useful\nmodel: sonnet\ntools: bash,read,write,edit\nallowed-tools: bash,read\n---\n\n# Skill instructions go here\n\n## Examples\n\n/my-skill do something",
                                "language": "yaml",
                                "order": 0,
                            },
                        ],
                        "templates": [
                            {
                                "id": "tmpl-skill-basic",
                                "title": "Basic Skill Template",
                                "content": "---\nname: {{name}}\ndescription: {{description}}\nmodel: {{model}}\ntools: {{tools}}\nallowed-tools: {{allowed_tools}}\n---\n\n# {{name}} Skill\n\n## Purpose\n{{description}}\n\n## Instructions\n1. First, understand the request\n2. Then, execute the necessary steps\n3. Finally, summarize what was done\n\n## Examples\n\n/{{name}} {{example}}",
                                "filename": ".claude/skills/{{name}}.yaml",
                                "order": 0,
                            },
                        ],
                    },
                    {
                        "id": "skills-precedence",
                        "title": "Skill Precedence and Overrides",
                        "content": "When skills share the same name across levels, the precedence order is:\n\n**Enterprise > Personal > Project**\n\nThis means a personal skill in `~/.claude/skills/` will override a project skill in `.claude/skills/` of the same name.\n\nThe `skillOverrides` setting (object keyed by skill name) controls **visibility**, not precedence:\n\n```json\n{\n  \"skillOverrides\": {\n    \"legacy-context\": \"name-only\",\n    \"deploy\": \"off\"\n  }\n}\n```\n\n| Value | Listed to Claude | In `/` menu |\n|-------|------------------|-------------|\n| `\"on\"` | Name and description | Yes |\n| `\"name-only\"` | Name only | Yes |\n| `\"user-invocable-only\"` | Hidden | Yes |\n| `\"off\"` | Hidden | Hidden |\n\nPlugin skills are managed via `/plugin` and are unaffected by `skillOverrides`.",
                        "order": 1,
                        "examples": [
                            {
                                "id": "ex-skill-overrides",
                                "title": "skillOverrides Configuration",
                                "code": "{\n  \"skillOverrides\": {\n    \"old-skill\": \"off\",\n    \"experimental-feature\": \"name-only\",\n    \"internal-tool\": \"user-invocable-only\"\n  }\n}",
                                "language": "json",
                                "order": 0,
                            },
                        ],
                        "templates": [],
                    },
                ],
            },
            {
                "id": "subagents-guide",
                "title": "Subagents Guide",
                "description": "Build specialized subagents for code review, testing, documentation, and more.",
                "category": "Agents",
                "difficulty": DifficultyLevel.INTERMEDIATE,
                "estimated_minutes": 25,
                "sections": [
                    {
                        "id": "subagents-concept",
                        "title": "Understanding Subagents",
                        "content": "Subagents are specialized AI agents that Claude Code can delegate tasks to. Each subagent has:\n- **Name**: Unique identifier\n- **Description**: When to use this agent\n- **Model**: sonnet, opus, or haiku\n- **Tools**: Subset of available tools\n- **System Prompt**: Specialized instructions\n\nSubagents are defined in `.claude/agents/` as Markdown files with YAML frontmatter.\n\nWhen you invoke a subagent, it runs in a separate context with only the tools you specify, making it ideal for focused tasks like code review, test generation, or documentation.",
                        "order": 0,
                        "examples": [
                            {
                                "id": "ex-subagent-structure",
                                "title": "Subagent File Structure",
                                "code": "---\nname: code-reviewer\ndescription: Reviews code for quality and security\nmodel: sonnet\ntools: read,glob,grep\n---\n\n# Code Reviewer Agent\n\nYou are an expert code reviewer. Focus on:\n1. Security vulnerabilities\n2. Code quality and maintainability\n3. Performance implications\n4. Test coverage\n\nProvide specific, actionable feedback.",
                                "language": "yaml",
                                "order": 0,
                            },
                        ],
                        "templates": [
                            {
                                "id": "tmpl-subagent-basic",
                                "title": "Subagent Template",
                                "content": "---\nname: {{name}}\ndescription: {{description}}\nmodel: {{model}}\ntools: {{tools}}\n---\n\n# {{name}} Agent\n\n{{system_prompt}}\n\n## Guidelines\n- Be specific and actionable\n- Reference actual code when possible\n- Prioritize the most important issues",
                                "filename": ".claude/agents/{{name}}.md",
                                "order": 0,
                            },
                        ],
                    },
                    {
                        "id": "subagents-patterns",
                        "title": "Common Subagent Patterns",
                        "content": "Effective subagent patterns:\n\n**Code Reviewer**: Reviews PRs for security, quality, style\n**Test Generator**: Creates unit/integration tests for new code\n**Documenter**: Writes and updates documentation\n**Refactorer**: Safely restructures code\n**Debugger**: Helps diagnose and fix bugs\n\nEach pattern uses a focused tool set and targeted system prompt.",
                        "order": 1,
                        "examples": [
                            {
                                "id": "ex-subagent-reviewer",
                                "title": "Code Reviewer System Prompt",
                                "code": "You are a senior code reviewer. Analyze the provided code for:\n\n1. **Security**: SQL injection, XSS, path traversal, auth bypass\n2. **Correctness**: Logic errors, edge cases, null handling\n3. **Maintainability**: Coupling, complexity, naming, DRY\n4. **Performance**: N+1 queries, memory leaks, algorithmic complexity\n\nOutput format:\n- **Critical**: Must fix before merge\n- **Major**: Should fix before merge\n- **Minor**: Nice to have\n- **Praise**: Good patterns to continue",
                                "language": "text",
                                "order": 0,
                            },
                        ],
                        "templates": [],
                    },
                ],
            },
            {
                "id": "mcp-servers",
                "title": "MCP Servers",
                "description": "Connect external tools and data sources via Model Context Protocol.",
                "category": "Integrations",
                "difficulty": DifficultyLevel.INTERMEDIATE,
                "estimated_minutes": 20,
                "sections": [
                    {
                        "id": "mcp-concept",
                        "title": "What Is MCP?",
                        "content": "Model Context Protocol (MCP) is an open standard for connecting AI assistants to external tools and data sources. Claude Code can act as an MCP client, connecting to servers that provide:\n\n- **Resources**: Read-only data (files, database rows, API responses)\n- **Tools**: Actions the AI can invoke (search, write, compute)\n- **Prompts**: Reusable prompt templates\n\nMCP servers run as separate processes (stdio) or remote services (SSE).",
                        "order": 0,
                        "examples": [
                            {
                                "id": "ex-mcp-config",
                                "title": "Basic MCP Configuration",
                                "code": "{\n  \"mcpServers\": {\n    \"filesystem\": {\n      \"command\": \"npx\",\n      \"args\": [\"-y\", \"@modelcontextprotocol/server-filesystem\", \"/path/to/allowed/dir\"]\n    },\n    \"github\": {\n      \"command\": \"npx\",\n      \"args\": [\"-y\", \"@modelcontextprotocol/server-github\"]\n      \"env\": {\n        \"GITHUB_TOKEN\": \"${GITHUB_TOKEN}\"\n      }\n    }\n  }\n}",
                                "language": "json",
                                "order": 0,
                            },
                        ],
                        "templates": [
                            {
                                "id": "tmpl-mcp-basic",
                                "title": "MCP Server Template",
                                "content": "{\n  \"mcpServers\": {\n    \"{{name}}\": {\n      \"command\": \"{{command}}\",\n      \"args\": {{args}},\n      \"env\": {{env}},\n      \"transport\": \"{{transport}}\"\n    }\n  }\n}",
                                "filename": ".mcp.json",
                                "order": 0,
                            },
                        ],
                    },
                    {
                        "id": "mcp-common",
                        "title": "Common MCP Servers",
                        "content": "Popular MCP servers for Claude Code:\n\n| Server | Purpose | Transport |\n|--------|---------|-----------|\n| filesystem | Local file access | stdio |\n| github | GitHub API access | stdio |\n| postgres | Database queries | stdio |\n| sqlite | SQLite queries | stdio |\n| brave-search | Web search | stdio |\n| fetch | HTTP fetching | stdio |\n| memory | Persistent memory | stdio |\n\nFor remote servers, use SSE transport with proper authentication.",
                        "order": 1,
                        "examples": [],
                        "templates": [],
                    },
                ],
            },
            {
                "id": "hooks-advanced",
                "title": "Hooks and Advanced Patterns",
                "description": "Automate workflows with hooks and learn advanced Claude Code patterns.",
                "category": "Advanced",
                "difficulty": DifficultyLevel.ADVANCED,
                "estimated_minutes": 30,
                "sections": [
                    {
                        "id": "hooks-concept",
                        "title": "Understanding Hooks",
                        "content": "Hooks are scripts that run at specific points in the Claude Code lifecycle. They enable automation, validation, and integration.\n\nHook types:\n- **PreToolUse**: Before a tool executes\n- **PostToolUse**: After a tool executes\n- **Notification**: When Claude sends a notification\n- **Stop**: When the conversation ends\n\nHooks are configured in `.claude/settings.json` or `.claude.json`.",
                        "order": 0,
                        "examples": [
                            {
                                "id": "ex-hook-config",
                                "title": "Hook Configuration",
                                "code": "{\n  \"hooks\": {\n    \"PreToolUse\": [\n      {\n        \"matcher\": \"Write|Edit|MultiEdit\",\n        \"hooks\": [\n          {\n            \"type\": \"command\",\n            \"command\": \"python .claude/hooks/validate.py\"\n          }\n        ]\n      }\n    ],\n    \"PostToolUse\": [\n      {\n        \"matcher\": \"Bash\",\n        \"hooks\": [\n          {\n            \"type\": \"command\",\n            \"command\": \"python .claude/hooks/log.py\"\n          }\n        ]\n      }\n    ]\n  }\n}",
                                "language": "json",
                                "order": 0,
                            },
                        ],
                        "templates": [
                            {
                                "id": "tmpl-hook-basic",
                                "title": "Basic Hook Script",
                                "content": "#!/usr/bin/env python3\n\"\"\"Hook script template.\"\"\"\nimport sys\nimport json\n\ndef main():\n    data = json.load(sys.stdin)\n    tool_name = data.get('tool_name')\n    tool_input = data.get('tool_input', {})\n    \n    # Add your validation/logic here\n    \n    # Return success\n    print(json.dumps({\"continue\": True}))\n\nif __name__ == '__main__':\n    main()",
                                "filename": ".claude/hooks/validate.py",
                                "order": 0,
                            },
                        ],
                    },
                    {
                        "id": "advanced-patterns",
                        "title": "Advanced Patterns",
                        "content": "Power user patterns for Claude Code:\n\n**Worktrees**: Use `git worktree` for parallel feature development\n**Checkpoints**: Save/restore conversation state\n**Custom Slash Commands**: Combine skills with shell scripts\n**Multi-Agent Workflows**: Chain subagents for complex tasks\n**Context Optimization**: Use `/compact` and selective file inclusion\n\nThese patterns enable professional-grade AI-assisted development workflows.",
                        "order": 1,
                        "examples": [
                            {
                                "id": "ex-worktree",
                                "title": "Worktree Workflow",
                                "code": "# Create worktree for feature\ngit worktree add ../feature-branch feature-branch\n\n# Work in parallel\ncd ../feature-branch\nclaude-code\n\n# Merge back\ngit worktree remove ../feature-branch",
                                "language": "bash",
                                "order": 0,
                            },
                        ],
                        "templates": [],
                    },
                ],
            },
        ]

        for lesson_data in lessons_data:
            sections_data = lesson_data.pop("sections")
            lesson = Lesson(**lesson_data)
            db.add(lesson)
            await db.flush()

            for section_data in sections_data:
                examples_data = section_data.pop("examples", [])
                templates_data = section_data.pop("templates", [])
                section = Section(**section_data, lesson_id=lesson.id)
                db.add(section)
                await db.flush()

                for ex_data in examples_data:
                    example = Example(**ex_data, section_id=section.id)
                    db.add(example)

                for tmpl_data in templates_data:
                    template = Template(**tmpl_data, section_id=section.id)
                    db.add(template)

        await db.commit()