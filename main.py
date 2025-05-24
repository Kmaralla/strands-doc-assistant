#!/usr/bin/env python3
"""
Main entry point for the Strands Documentation Assistant.
This script initializes and runs the agent.
"""

import os
import argparse
import logging
from typing import Optional

from strands.agent.agent import Agent
from strands.models.bedrock import BedrockModel
from strands.tools.registry import ToolRegistry

from app import DocumentSearchTool, DocumentReaderTool, create_agent
from mcp_integration import register_mcp_tools
from docs_processor import DocumentationProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_messages(messages):
    """Validate messages to ensure no empty content blocks are sent to Bedrock."""
    if not messages:
        return messages
        
    for i, msg in enumerate(messages):
        if "content" in msg and isinstance(msg["content"], list):
            for j, content in enumerate(msg["content"]):
                if "text" in content and (content["text"] is None or content["text"] == ""):
                    # Replace empty text with placeholder
                    messages[i]["content"][j]["text"] = "[No content]"
    return messages


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
        default="anthropic.claude-3-5-sonnet-20240620-v1:0",
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
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Test configuration without initializing Bedrock"
    )
    return parser.parse_args()


def main():
    """Main entry point for the application."""
    args = parse_args()
    
    # Log the parsed arguments
    logger.info(f"Parsed arguments: docs_path='{args.docs_path}', model_id='{args.model_id}', index={args.index}, dry_run={args.dry_run}")
    
    # Create docs directory if it doesn't exist
    if not os.path.exists(args.docs_path):
        os.makedirs(args.docs_path)
        logger.info(f"Created documentation directory: {args.docs_path}")
        print(f"Created documentation directory: {args.docs_path}")
    else:
        logger.info(f"Using existing documentation directory: {args.docs_path}")
    
    # Index documentation if requested
    if args.index:
        print("Indexing documentation...")
        logger.info(f"Starting documentation indexing from: {args.docs_path}")
        processor = DocumentationProcessor(args.docs_path)
        processor.index_documentation()
        processor.save_index()
        print("Documentation indexed.")
        logger.info("Documentation indexing completed.")
    
    # If dry-run, just test the configuration and exit
    if args.dry_run:
        print("=== DRY RUN MODE ===")
        print(f"Testing configuration with docs_path: {args.docs_path}")
        
        # Test DocumentSearchTool creation
        from app import DocumentSearchTool
        tool = DocumentSearchTool(docs_path=args.docs_path)
        print(f"✓ DocumentSearchTool initialized with path: {tool.docs_path}")
        
        # Check if path exists and list files
        if os.path.exists(args.docs_path):
            files = []
            for root, _, filenames in os.walk(args.docs_path):
                for filename in filenames:
                    if filename.endswith(('.md', '.txt', '.html')):
                        files.append(os.path.join(root, filename))
            print(f"✓ Found {len(files)} documentation files:")
            for file in files:
                print(f"  - {file}")
        else:
            print(f"⚠ Documentation path does not exist: {args.docs_path}")
        
        print("=== Dry run completed successfully ===")
        return
    
    # Create the agent
    print(f"Initializing agent with model {args.model_id}...")
    logger.info(f"Creating agent with model_id='{args.model_id}' and docs_path='{args.docs_path}'")
    agent = create_agent(model_id=args.model_id, docs_path=args.docs_path)
    
    # Register MCP tools if a server URL is provided
    if args.mcp_server:
        print(f"Registering MCP tools from server: {args.mcp_server}")
        logger.info(f"Registering MCP tools from server: {args.mcp_server}")
        register_mcp_tools(agent.tools, args.mcp_server)
    
    print("\nDocumentation Assistant initialized. Type 'exit' to quit.")
    print("Ask me anything about the documentation!")
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            logger.info("Application terminated by user")
            break
        
        try:
            # Process the user's request with message validation
            logger.debug(f"Processing user input: {user_input}")
            response = agent(user_input, messages_validator=validate_messages)
            
            # Display the response
            print(f"\nAssistant: {response.message}")
        except Exception as e:
            logger.error(f"Error processing user input: {str(e)}", exc_info=True)
            print(f"\nError: {str(e)}")
            print("Creating a new agent instance to continue...")
            agent = create_agent(model_id=args.model_id, docs_path=args.docs_path)
            if args.mcp_server:
                register_mcp_tools(agent.tools, args.mcp_server)


if __name__ == "__main__":
    main()
