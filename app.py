#!/usr/bin/env python3
"""
Main application file for the Strands Documentation Assistant.
This agent searches, reads, and makes recommendations based on documentation.
"""

import os
import json
from typing import Dict, List, Any, Optional

from strands.agent import Agent
from strands.language_model import BedrockLanguageModel
from strands.tools import Tool, ToolRegistry

# Define tools for documentation handling
class DocumentSearchTool(Tool):
    """Tool for searching through documentation."""
    
    def __init__(self, docs_path: str = "./docs"):
        """Initialize with path to documentation files."""
        self.docs_path = docs_path
        super().__init__(
            name="document_search",
            description="Search through documentation for specific terms or topics",
            parameters={
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
        )
    
    def _execute(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Execute the search through documentation.
        
        This is a simple implementation. In a real application, you might use
        a vector database or other search mechanism.
        """
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
                            print(f"Error reading file {file_path}: {e}")
                            
            # Sort by relevance score and limit results
            results = sorted(results, key=lambda x: x["score"], reverse=True)[:max_results]
            return results
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]


class DocumentReaderTool(Tool):
    """Tool for reading documentation content."""
    
    def __init__(self):
        """Initialize the document reader tool."""
        super().__init__(
            name="document_read",
            description="Read the content of a specific documentation file",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the documentation file to read"
                    }
                },
                "required": ["file_path"]
            }
        )
    
    def _execute(self, file_path: str) -> Dict[str, Any]:
        """Read the content of the specified file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return {
                    "file": file_path,
                    "content": content
                }
        except Exception as e:
            return {"error": f"Failed to read file {file_path}: {str(e)}"}


def create_agent(model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> Agent:
    """
    Create and configure the Strands agent with necessary tools.
    
    Args:
        model_id: The Bedrock model ID to use
        
    Returns:
        Configured Strands agent
    """
    # Initialize the language model
    llm = BedrockLanguageModel(model_id=model_id)
    
    # Create tool registry and register tools
    tool_registry = ToolRegistry()
    tool_registry.register(DocumentSearchTool())
    tool_registry.register(DocumentReaderTool())
    
    # Create the agent
    agent = Agent(
        llm=llm,
        tools=tool_registry,
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
