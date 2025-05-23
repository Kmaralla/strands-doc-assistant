# Getting Started with Strands

Strands is an open-source toolkit for building AI agents. This guide will help you get started with Strands and build your first agent.

## Installation

To install Strands, use pip:

```bash
pip install strands-agent
```

## Basic Usage

Here's a simple example of creating a Strands agent:

```python
from strands.agent import Agent
from strands.language_model import BedrockLanguageModel

# Initialize the language model
llm = BedrockLanguageModel(model_id="anthropic.claude-3-sonnet-20240229-v1:0")

# Create the agent
agent = Agent(
    llm=llm,
    system_prompt="You are a helpful assistant."
)

# Process a message
response = agent.process_message("Hello, how can you help me?")
print(response.message)
```

## Adding Tools

Strands agents can use tools to interact with external systems. Here's how to add a tool:

```python
from strands.tools import Tool, ToolRegistry

# Define a simple tool
class CalculatorTool(Tool):
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Perform basic arithmetic operations",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The arithmetic expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        )
    
    def _execute(self, expression: str):
        try:
            return {"result": eval(expression)}
        except Exception as e:
            return {"error": str(e)}

# Create a tool registry
tool_registry = ToolRegistry()
tool_registry.register(CalculatorTool())

# Create an agent with tools
agent = Agent(
    llm=llm,
    tools=tool_registry,
    system_prompt="You are a helpful assistant that can perform calculations."
)
```

## Using Amazon Bedrock

Strands integrates seamlessly with Amazon Bedrock. Make sure you have the necessary AWS permissions and credentials configured.

```python
from strands.language_model import BedrockLanguageModel

# Initialize the Bedrock language model
llm = BedrockLanguageModel(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    region_name="us-east-1",
    profile_name="default"  # Optional
)
```

## Next Steps

- Explore more complex tools and integrations
- Learn about conversation memory and state management
- Build multi-step workflows with Strands
- Integrate with MCP (Model Context Protocol) for extended capabilities
