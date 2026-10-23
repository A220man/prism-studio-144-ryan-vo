from typing import Dict, Any
from string import Template


class WorkflowService:
    """Deterministic workflow generators - no LLM required."""

    @staticmethod
    def generate_skill(data: Dict[str, Any]) -> str:
        name = data.get("name", "my-skill")
        description = data.get("description", "A custom skill")
        model = data.get("model", "sonnet")
        tools = data.get("tools", "bash,read,write,edit,glob,grep,task")
        allowed_tools = data.get("allowed_tools", "")
        example = data.get("example", "do something")

        tools_list = [t.strip() for t in tools.split(",") if t.strip()]
        allowed_list = [t.strip() for t in allowed_tools.split(",") if t.strip()] if allowed_tools else tools_list

        template = Template("""---
name: ${name}
description: ${description}
model: ${model}
tools: ${tools}
allowed-tools: ${allowed_tools}
---

# ${name} Skill

## Purpose
${description}

## Instructions
1. First, understand the request
2. Then, execute the necessary steps
3. Finally, summarize what was done

## Examples

/${name} ${example}
""")
        return template.substitute(
            name=name,
            description=description,
            model=model,
            tools=",".join(tools_list),
            allowed_tools=",".join(allowed_list),
            example=example,
        )

    @staticmethod
    def generate_subagent(data: Dict[str, Any]) -> str:
        name = data.get("name", "custom-agent")
        description = data.get("description", "A specialized agent")
        model = data.get("model", "sonnet")
        tools = data.get("tools", "read,glob,grep")
        system_prompt = data.get("system_prompt", "You are a specialized agent.")

        tools_list = [t.strip() for t in tools.split(",") if t.strip()]

        template = Template("""---
name: ${name}
description: ${description}
model: ${model}
tools: ${tools}
---

# ${name} Agent

${system_prompt}

## Guidelines
- Be specific and actionable
- Reference actual code when possible
- Prioritize the most important issues
""")
        return template.substitute(
            name=name,
            description=description,
            model=model,
            tools=",".join(tools_list),
            system_prompt=system_prompt,
        )

    @staticmethod
    def generate_mcp_config(data: Dict[str, Any]) -> str:
        name = data.get("name", "custom-server")
        command = data.get("command", "npx")
        args_str = data.get("args", "")
        env_str = data.get("env", "{}")
        transport = data.get("transport", "stdio")

        args_list = [a.strip() for a in args_str.split() if a.strip()]

        try:
            import json
            env_dict = json.loads(env_str) if env_str else {}
        except json.JSONDecodeError:
            env_dict = {}

        import json as json_module
        config = {
            "mcpServers": {
                name: {
                    "command": command,
                    "args": args_list,
                }
            }
        }

        if env_dict:
            config["mcpServers"][name]["env"] = env_dict
        if transport != "stdio":
            config["mcpServers"][name]["transport"] = transport

        return json_module.dumps(config, indent=2)