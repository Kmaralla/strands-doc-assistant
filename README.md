# Strands Documentation Assistant

A lightweight AI agent built using Amazon Strands and Amazon Bedrock that searches, reads, and makes recommendations based on documentation.

## Recent Updates

✅ **Fixed `--docs-path` Parameter Issue**: The application now correctly uses the `--docs-path` parameter instead of always defaulting to `./docs`. Added comprehensive logging to track documentation path usage.

## Overview

This project demonstrates how to build an AI agent using Amazon Strands (an open-source agent building toolkit) that can:

1. Search through documentation files
2. Read and understand documentation content  
3. Make recommendations based on the documentation
4. Support custom documentation directories

## Features

- **Custom Documentation Paths**: Use `--docs-path` to specify any documentation directory
- **Documentation Search**: Find relevant information in documentation files (.md, .txt, .html)
- **Content Understanding**: Read and comprehend documentation content
- **Contextual Recommendations**: Get recommendations based on documentation
- **MCP Integration**: Extend capabilities with Model Context Protocol tools
- **Comprehensive Logging**: Track system behavior with detailed logging
- **Dry Run Mode**: Test configuration without AWS credentials

## Prerequisites

- Python 3.9+
- AWS account with access to Amazon Bedrock
- AWS credentials configured
- Virtual environment (recommended)

## Installation

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd strands-doc-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv strands-env
source strands-env/bin/activate  # On Windows: strands-env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure AWS Credentials

```bash
aws configure
```

Or set environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

## Quick Start

### Validate Setup

First, validate your installation:

```bash
python test_setup.py
```

This will check:
- Python version compatibility
- Required dependencies
- CLI argument parsing
- Dry-run functionality
- AWS configuration (optional)

### Test Without AWS (Dry Run)

Test the application configuration without requiring AWS credentials:

```bash
# Test with default docs directory
python main.py --dry-run

# Test with custom docs directory
mkdir -p /tmp/my-docs
echo "# Test Doc" > /tmp/my-docs/test.md
python main.py --docs-path /tmp/my-docs --dry-run
```

### Run with AWS

```bash
# Use default docs directory
python main.py

# Use custom docs directory
python main.py --docs-path /path/to/your/docs

# Index documentation first (recommended for large doc sets)
python main.py --docs-path /path/to/your/docs --index
```

## Usage Examples

### Basic Usage

```bash
python main.py --docs-path ./my-documentation
```

### With Documentation Indexing

```bash
python main.py --docs-path ./my-documentation --index
```

### Using Different Bedrock Models

```bash
python main.py --docs-path ./docs --model-id anthropic.claude-3-haiku-20240307-v1:0
```

### With MCP Server Integration

```bash
python main.py --docs-path ./docs --mcp-server http://localhost:8080
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--docs-path` | Path to documentation directory | `./docs` |
| `--model-id` | Bedrock model ID to use | `anthropic.claude-3-5-sonnet-20240620-v1:0` |
| `--mcp-server` | URL of MCP server (optional) | None |
| `--index` | Index documentation before starting | False |
| `--region` | AWS region for Bedrock | `us-east-1` |
| `--profile` | AWS profile name | None |
| `--dry-run` | Test configuration without AWS | False |

## Testing the docs-path Fix

To verify the recent fix works correctly:

1. **Create test documentation:**
   ```bash
   mkdir -p /tmp/test-docs
   echo "# Test Documentation\nThis is a test file about Python." > /tmp/test-docs/python.md
   echo "# AWS Guide\nThis covers AWS services." > /tmp/test-docs/aws.md
   ```

2. **Test with dry-run:**
   ```bash
   python main.py --docs-path /tmp/test-docs --dry-run
   ```

3. **Verify output shows:**
   - Correct path being used
   - Files being found
   - Logging messages indicating the right directory

## Project Structure

```
strands-doc-assistant/
├── main.py                 # Main entry point with CLI parsing
├── app.py                  # Core agent and tools implementation
├── docs_processor.py       # Documentation indexing
├── mcp_integration.py      # MCP protocol integration
├── bedrock_integration.py  # AWS Bedrock utilities
├── simplified_app.py       # Standalone Bedrock implementation
├── docs/                   # Default documentation directory
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
└── README.md              # This file
```

## Troubleshooting

### Common Issues

1. **"No module named 'strands'" Error**
   ```bash
   pip install strands-agent
   ```

2. **AWS Credentials Not Found**
   ```bash
   aws configure
   # Or use environment variables
   ```

3. **Documentation Not Found**
   ```bash
   # Verify path exists and contains .md, .txt, or .html files
   ls -la /path/to/your/docs
   
   # Use dry-run to test
   python main.py --docs-path /path/to/your/docs --dry-run
   ```

4. **Permission Errors**
   ```bash
   # Ensure directory is readable
   chmod -R 755 /path/to/your/docs
   ```

### Debug Mode

Enable detailed logging:
```bash
python main.py --docs-path ./docs --dry-run
# Check logs for detailed path resolution
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Test your changes with dry-run mode
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Amazon Strands](https://github.com/awslabs/amazon-strands) toolkit
- Uses [Amazon Bedrock](https://aws.amazon.com/bedrock/) for AI capabilities
- Supports [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for extensibility
