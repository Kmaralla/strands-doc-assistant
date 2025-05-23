# Strands Documentation Assistant

A lightweight agent built using Amazon Strands and Amazon Bedrock that searches, reads, and makes recommendations based on documentation.

## Overview

This project demonstrates how to build an AI agent using Amazon Strands (an open-source agent building toolkit) that can:

1. Search through documentation
2. Read and understand documentation content
3. Make recommendations based on the documentation

## Project Structure

```
strands-doc-assistant/
├── app.py              # Core agent functionality
├── bedrock_integration.py  # Amazon Bedrock integration
├── docs/               # Documentation directory
├── docs_processor.py   # Documentation indexing and processing
├── main.py             # Main entry point
├── mcp_integration.py  # MCP tools integration
├── requirements.txt    # Project dependencies
├── LICENSE             # MIT License
└── README.md           # This file
```

## Prerequisites

- Python 3.9+
- AWS account with access to Amazon Bedrock
- AWS credentials configured
- Minimal dependencies:
  - strands-agent
  - boto3

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/strands-doc-assistant.git
   cd strands-doc-assistant
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure AWS credentials:
   ```
   aws configure
   ```

## Usage

1. Add documentation to the `docs/` directory

2. Run the application:
   ```
   python main.py
   ```

3. Additional options:
   ```
   python main.py --docs-path /path/to/docs --model-id anthropic.claude-3-sonnet-20240229-v1:0 --index
   ```

   - `--docs-path`: Path to documentation directory
   - `--model-id`: Bedrock model ID to use
   - `--mcp-server`: URL of MCP server (optional)
   - `--index`: Index documentation before starting
   - `--region`: AWS region for Bedrock
   - `--profile`: AWS profile name

## Features

- **Documentation Search**: Find relevant information in documentation
- **Content Understanding**: Read and comprehend documentation content
- **Contextual Recommendations**: Get recommendations based on documentation
- **MCP Integration**: Extend capabilities with Model Context Protocol tools

## Extending the Project

### Adding New Tools

To add new tools to the agent, create a new class that inherits from `strands.tools.Tool` and register it with the agent's tool registry.

### Using Different Models

You can use different Bedrock models by specifying the `--model-id` parameter when running the application.

### Adding Documentation

Simply add your documentation files (Markdown, HTML, or plain text) to the `docs/` directory, and the agent will be able to search and read them.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
