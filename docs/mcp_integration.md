# MCP Integration with Strands

Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to LLMs. This guide explains how to integrate MCP with Strands agents.

## What is MCP?

MCP enables communication between the system and locally running MCP servers that provide additional tools and resources to extend your agent's capabilities. MCP servers can provide:

- Access to local files and resources
- Integration with external APIs
- Custom tools and functions
- Additional context for the agent

## Setting Up MCP with Strands

### 1. Install MCP Server

First, you need to have an MCP server running. You can use an existing MCP server or create your own.

```bash
# Example installation of a basic MCP server
pip install mcp-server
```

### 2. Create MCP Tool Integration

Create a tool that can communicate with the MCP server:

```python
from strands.tools import Tool
import requests

class MCPTool(Tool):
    def __init__(self, mcp_server_url="http://localhost:8080"):
        self.mcp_server_url = mcp_server_url
        super().__init__(
            name="mcp_tool",
            description="Interact with MCP servers to extend agent capabilities",
            parameters={
                "type": "object",
                "properties": {
                    "tool_name": {
                        "type": "string",
                        "description": "Name of the MCP tool to call"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Parameters to pass to the MCP tool"
                    }
                },
                "required": ["tool_name", "parameters"]
            }
        )
    
    def _execute(self, tool_name, parameters):
        try:
            request_data = {
                "tool": tool_name,
                "parameters": parameters
            }
            
            response = requests.post(
                f"{self.mcp_server_url}/invoke",
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"MCP request failed with status code {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {"error": f"MCP tool execution failed: {str(e)}"}
```

### 3. Register the MCP Tool with Your Agent

```python
from strands.agent import Agent
from strands.language_model import BedrockLanguageModel
from strands.tools import ToolRegistry

# Initialize the language model
llm = BedrockLanguageModel(model_id="anthropic.claude-3-sonnet-20240229-v1:0")

# Create tool registry and register MCP tool
tool_registry = ToolRegistry()
tool_registry.register(MCPTool("http://localhost:8080"))

# Create the agent
agent = Agent(
    llm=llm,
    tools=tool_registry,
    system_prompt="""
    You are an assistant that can use MCP tools to extend your capabilities.
    When a user asks for something that requires external resources, use the mcp_tool.
    """
)
```

## Using MCP Tools in Your Agent

Once your agent is set up with MCP integration, it can use MCP tools to perform various tasks:

```python
# Example of using an MCP tool
response = agent.process_message("Can you search for information about AWS services?")

# The agent might use the MCP tool like this:
# mcp_tool(tool_name="search", parameters={"query": "AWS services"})
```

## Available MCP Tools

The available MCP tools depend on the MCP server you're using. You can discover available tools by querying the MCP server:

```python
import requests

def discover_mcp_tools(mcp_server_url="http://localhost:8080"):
    try:
        response = requests.get(f"{mcp_server_url}/tools")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to discover MCP tools: {response.status_code}"}
    except Exception as e:
        return {"error": f"Error discovering MCP tools: {str(e)}"}
```

## Best Practices

1. **Error Handling**: Always handle errors from MCP tools gracefully
2. **Timeouts**: Set appropriate timeouts for MCP requests
3. **Security**: Be cautious about what tools you allow your agent to use
4. **Documentation**: Document the available MCP tools for users of your agent
5. **Fallbacks**: Provide fallback behavior when MCP tools are unavailable
