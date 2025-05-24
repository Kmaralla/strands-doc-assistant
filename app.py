#!/usr/bin/env python3
"""
Main application file for the Strands Documentation Assistant.
This agent searches, reads, and makes recommendations based on documentation.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional

from strands.agent.agent import Agent
from strands.models.bedrock import BedrockModel
from strands.tools.registry import ToolRegistry
from strands.tools.tools import PythonAgentTool as Tool

# Configure logging for this module
logger = logging.getLogger(__name__)

# Define tools for documentation handling
class ConversationResetTool(Tool):
    """Tool for resetting the conversation history."""
    
    def __init__(self):
        """Initialize the conversation reset tool."""
        super().__init__(
            tool_name="reset_conversation",
            tool_spec={
                "name": "reset_conversation",
                "description": "Reset the conversation history to start fresh",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            callback=self._execute
        )
    
    def _execute(self, tool_use, **kwargs) -> Dict[str, Any]:
        """Reset the conversation."""
        # The actual reset will be handled by the agent
        return {
            "toolUseId": tool_use.get("toolUseId", "unknown"),
            "status": "success",
            "content": [{"text": "Conversation history has been reset."}]
        }


class DocumentSearchTool(Tool):
    """Tool for searching through documentation."""
    
    def __init__(self, docs_path: str = "./docs"):
        """Initialize with path to documentation files."""
        self.docs_path = docs_path
        logger.info(f"DocumentSearchTool initialized with docs_path: '{docs_path}'")
        super().__init__(
            tool_name="document_search",
            tool_spec={
                "name": "document_search",
                "description": "Search through documentation for specific terms or topics",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of results to return",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            callback=self._execute
        )
    
    def _execute(self, tool_use, max_results: int = 5, **kwargs) -> Dict[str, Any]:
        """
        Execute the search through documentation.
        
        This is a simple implementation. In a real application, you might use
        a vector database or other search mechanism.
        """
        # Extract query from tool_use
        query = tool_use.get("input", {}).get("query", "")
        if not query:
            logger.warning("No search query provided in tool_use")
            return {
                "toolUseId": tool_use.get("toolUseId", "unknown"),
                "status": "error",
                "content": [{"text": "No search query provided"}]
            }
            
        logger.info(f"Searching for query '{query}' in docs_path: '{self.docs_path}'")
        results = []
        
        # Simple file-based search implementation
        try:
            for root, _, files in os.walk(self.docs_path):
                for file in files:
                    if file.endswith(('.md', '.txt', '.html')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if query.lower() in content.lower():
                                    # Calculate a simple relevance score based on term frequency
                                    score = content.lower().count(query.lower())
                                    results.append({
                                        "file": file_path,
                                        "score": score,
                                        "preview": content[:200] + "..." if len(content) > 200 else content
                                    })
                        except Exception as e:
                            logger.warning(f"Error reading file {file_path}: {e}")
                            print(f"Error reading file {file_path}: {e}")
            
            # Check results after processing all files
            if not results:
                logger.info(f"No matching documents found for query '{query}'")
                return {
                    "toolUseId": tool_use.get("toolUseId", "unknown"),
                    "status": "success",
                    "content": [{"text": "No matching documents found for your query."}]
                }
                        
            # Sort by relevance score and limit results
            results = sorted(results, key=lambda x: x["score"], reverse=True)[:max_results]
            logger.info(f"Found {len(results)} matching documents for query '{query}'")
            return {
                "toolUseId": tool_use.get("toolUseId", "unknown"),
                "status": "success",
                "content": [{"text": json.dumps(results, indent=2) if results else "No results found."}]
            }
        except Exception as e:
            logger.error(f"Search failed for query '{query}': {str(e)}", exc_info=True)
            return {
                "toolUseId": tool_use.get("toolUseId", "unknown"),
                "status": "error",
                "content": [{"text": f"Search failed: {str(e)}"}]
            }


class DocumentReaderTool(Tool):
    """Tool for reading documentation content."""
    
    def __init__(self):
        """Initialize the document reader tool."""
        super().__init__(
            tool_name="document_read",
            tool_spec={
                "name": "document_read",
                "description": "Read the content of a specific documentation file",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the documentation file to read"
                            }
                        },
                        "required": ["file_path"]
                    }
                }
            },
            callback=self._execute
        )
    
    def _execute(self, tool_use, **kwargs) -> Dict[str, Any]:
        """Read the content of the specified file."""
        # Extract file_path from tool_use
        file_path = tool_use.get("input", {}).get("file_path", "")
        if not file_path:
            return {
                "toolUseId": tool_use.get("toolUseId", "unknown"),
                "status": "error",
                "content": [{"text": "No file path provided"}]
            }
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return {
                    "toolUseId": tool_use.get("toolUseId", "unknown"),
                    "status": "success",
                    "content": [{"text": f"File: {file_path}\n\n{content}"}]
                }
        except Exception as e:
            return {
                "toolUseId": tool_use.get("toolUseId", "unknown"),
                "status": "error",
                "content": [{"text": f"Failed to read file {file_path}: {str(e)}"}]
            }


def create_agent(model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0", docs_path: str = "./docs") -> Agent:
    """
    Create and configure the Strands agent with necessary tools.
    
    Args:
        model_id: The Bedrock model ID to use
        docs_path: The path to the documentation files
        
    Returns:
        Configured Strands agent
    """
    logger.info(f"Creating agent with model_id='{model_id}' and docs_path='{docs_path}'")
    
    # Initialize the language model with region
    llm = BedrockModel(model_id=model_id, region_name="us-east-1")
    
    # Create tool registry and register tools
    tool_registry = ToolRegistry()
    tool_registry.register_tool(ConversationResetTool())
    tool_registry.register_tool(DocumentSearchTool(docs_path))
    tool_registry.register_tool(DocumentReaderTool())
    
    # Get the list of registered tools
    registered_tools = list(tool_registry.registry.values())
    logger.info(f"Registered {len(registered_tools)} tools with the agent")
    
    # Create the agent
    agent = Agent(
        model=llm,
        tools=registered_tools,
        system_prompt="""
        You are a Documentation Assistant built with Amazon Strands and Amazon Bedrock.
        Your purpose is to help users find information in documentation, understand concepts,
        and get recommendations based on their needs.
        
        When helping users:
        1. Use the document_search tool to find relevant documentation
        2. Use the document_read tool to retrieve the full content of relevant files
        3. Provide concise, accurate answers based on the documentation
        4. If the documentation doesn't contain the answer, clearly state that
        5. Recommend related topics that might be helpful
        
        Always cite your sources by mentioning which documentation files you referenced.
        """
    )
    
    return agent


def main():
    """Main entry point for the application."""
    # Create the agent
    agent = create_agent()
    
    print("Documentation Assistant initialized. Type 'exit' to quit.")
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
