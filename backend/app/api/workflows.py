from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from app.services.workflow_service import WorkflowService

router = APIRouter(tags=["workflows"])


class WorkflowInfo(BaseModel):
    id: str
    title: str
    description: str


@router.get("", response_model=Dict[str, list[WorkflowInfo]])
async def list_workflows():
    return {
        "workflows": [
            WorkflowInfo(
                id="skill-wizard",
                title="Skill Creation Wizard",
                description="Generate a complete .claude/skills/ YAML file with proper frontmatter, tools, and examples.",
            ),
            WorkflowInfo(
                id="subagent-builder",
                title="Subagent Builder",
                description="Create a specialized subagent with model selection, tools, and system prompt template.",
            ),
            WorkflowInfo(
                id="mcp-configurator",
                title="MCP Server Configurator",
                description="Configure Model Context Protocol servers with transport, auth, and capability settings.",
            ),
        ]
    }


class SkillWizardRequest(BaseModel):
    name: str
    description: str
    model: str = "sonnet"
    tools: str = "bash,read,write,edit,glob,grep,task"
    allowed_tools: str = ""
    example: str = "do something"


class SubagentBuilderRequest(BaseModel):
    name: str
    description: str
    model: str = "sonnet"
    tools: str = "bash,read,write,edit,glob,grep,task"
    system_prompt: str


class MCPConfiguratorRequest(BaseModel):
    name: str
    command: str = "npx"
    args: str = ""
    env: str = "{}"
    transport: str = "stdio"


@router.post("/skill-wizard")
async def skill_wizard(request: SkillWizardRequest):
    try:
        template = WorkflowService.generate_skill(request.model_dump())
        return {"template": template}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate skill: {str(e)}")


@router.post("/subagent-builder")
async def subagent_builder(request: SubagentBuilderRequest):
    try:
        template = WorkflowService.generate_subagent(request.model_dump())
        return {"template": template}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate subagent: {str(e)}")


@router.post("/mcp-configurator")
async def mcp_configurator(request: MCPConfiguratorRequest):
    try:
        template = WorkflowService.generate_mcp_config(request.model_dump())
        return {"template": template}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate MCP config: {str(e)}")