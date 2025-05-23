#!/usr/bin/env python3
"""
Main entry point for the Strands Documentation Assistant.
This script initializes and runs the agent.
"""

import os
import argparse
from typing import Optional

from strands.agent import Agent
from strands.language_model import BedrockLanguageModel
from strands.tools import ToolRegistry

from app import DocumentSearchTool, DocumentReaderTool, create_agent
from mcp_integration import register_mcp_tools
from docs_processor import DocumentationProcessor


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Strands Documentation Assistant")
    parser.add_argument(
        "--docs-path", 
        type=str, 
        default="./docs",
        help="Path to the documentation directory"
    )
    parser.add_argument(
        "--model-id", 
        type=str, 
        default="anthropic.claude-3-sonnet-20240229-v1:0",
        help="Bedrock model ID to use"
    )
    parser.add_argument(
        "--mcp-server", 
        type=str, 
        default=None,
        help="URL of the MCP server (if any)"
    )
    parser.add_argument(
        "--index", 
        action="store_true",
        help="Index documentation before starting"
    )
    parser.add_argument(
        "--region", 
        type=str, 
        default="us-east-1",
        help="AWS region for Bedrock"
    )
    parser.add_argument(
        "--profile", 
        type=str, 
        default=None,
        help="AWS profile name"
    )
    return parser.parse_args()


def main():
    """Main entry point for the application."""
    args = parse_args()
    
    # Create docs directory if it doesn't exist
    if not os.path.exists(args.docs_path):
        os.makedirs(args.docs_path)
        print(f"Created documentation directory: {args.docs_path}")
    
    # Index documentation if requested
    if args.index:
        print("Indexing documentation...")
        processor = DocumentationProcessor(args.docs_path)
        processor.index_documentation()
        processor.save_index()
        print("Documentation indexed.")
    
    # Create the agent
    print(f"Initializing agent with model {args.model_id}...")
    agent = create_agent(model_id=args.model_id)
    
    # Register MCP tools if a server URL is provided
    if args.mcp_server:
        print(f"Registering MCP tools from server: {args.mcp_server}")
        register_mcp_tools(agent.tools, args.mcp_server)
    
    print("\nDocumentation Assistant initialized. Type 'exit' to quit.")
    print("Ask me anything about the documentation!")
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        # Process the user's request
        response = agent.process_message(user_input)
        
        # Display the response
        print(f"\nAssistant: {response.message}")


if __name__ == "__main__":
    main()
