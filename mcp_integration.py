#!/usr/bin/env python3
"""
MCP (Model Context Protocol) integration for the Strands Documentation Assistant.
This module adds MCP tool support to the agent.
"""

from typing import Dict, Any, List, Optional
import json
import requests

from strands.tools import Tool


class MCPTool(Tool):
    """Tool for integrating with MCP servers."""
    
    def __init__(self, mcp_server_url: str = "http://localhost:8080"):
        """
        Initialize the MCP tool.
        
        Args:
            mcp_server_url: URL of the MCP server
        """
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
    
    def _execute(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a call to an MCP tool.
        
        Args:
            tool_name: Name of the MCP tool to call
            parameters: Parameters to pass to the tool
            
        Returns:
            Response from the MCP tool
        """
        try:
            # Construct the MCP request
            request_data = {
                "tool": tool_name,
                "parameters": parameters
            }
            
            # Make the request to the MCP server
            response = requests.post(
                f"{self.mcp_server_url}/invoke",
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"MCP request failed with status code {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {"error": f"MCP tool execution failed: {str(e)}"}


class MCPToolDiscovery(Tool):
    """Tool for discovering available MCP tools."""
    
    def __init__(self, mcp_server_url: str = "http://localhost:8080"):
        """
        Initialize the MCP tool discovery.
        
        Args:
            mcp_server_url: URL of the MCP server
        """
        self.mcp_server_url = mcp_server_url
        super().__init__(
            name="mcp_discover",
            description="Discover available MCP tools on connected servers",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    
    def _execute(self) -> Dict[str, Any]:
        """
        Discover available MCP tools.
        
        Returns:
            List of available MCP tools
        """
        try:
            # Make the request to the MCP server
            response = requests.get(
                f"{self.mcp_server_url}/tools",
                headers={"Content-Type": "application/json"}
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                return {"tools": response.json()}
            else:
                return {
                    "error": f"MCP discovery failed with status code {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {"error": f"MCP tool discovery failed: {str(e)}"}


# Example of how to register MCP tools with the agent
def register_mcp_tools(tool_registry, mcp_server_url: str = "http://localhost:8080"):
    """
    Register MCP tools with the agent's tool registry.
    
    Args:
        tool_registry: The agent's tool registry
        mcp_server_url: URL of the MCP server
    """
    tool_registry.register(MCPTool(mcp_server_url))
    tool_registry.register(MCPToolDiscovery(mcp_server_url))
