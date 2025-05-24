#!/usr/bin/env python3
"""
MCP (Model Context Protocol) integration for the Strands Documentation Assistant.
This module adds MCP tool support to the agent.
"""

from typing import Dict, Any, List, Optional
import json
import requests

from strands.tools.tools import PythonAgentTool as Tool


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
            tool_name="mcp_tool",
            tool_spec={
                "name": "mcp_tool",
                "description": "Interact with MCP servers to extend agent capabilities",
                "inputSchema": {
                    "json": {
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
                }
            },
            callback=self._execute
        )
    
    def _execute(self, tool_use, **kwargs) -> Dict[str, Any]:
        """
        Execute a call to an MCP tool.
        
        Args:
            tool_use: The tool use request
            **kwargs: Additional keyword arguments
            
        Returns:
            Response from the MCP tool
        """
        try:
            # Extract parameters from tool_use
            tool_name = tool_use.get("input", {}).get("tool_name", "")
            parameters = tool_use.get("input", {}).get("parameters", {})
            
            if not tool_name:
                return {
                    "toolUseId": tool_use.get("toolUseId", "unknown"),
                    "status": "error",
                    "content": [{"text": "No tool name provided"}]
                }
            
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
                return {
                    "toolUseId": tool_use.get("toolUseId", "unknown"),
                    "status": "success",
                    "content": [{"text": json.dumps(response.json(), indent=2)}]
                }
            else:
                return {
                    "toolUseId": tool_use.get("toolUseId", "unknown"),
                    "status": "error",
                    "content": [{"text": f"MCP request failed with status code {response.status_code}: {response.text}"}]
                }
        except Exception as e:
            return {
                "toolUseId": tool_use.get("toolUseId", "unknown"),
                "status": "error",
                "content": [{"text": f"MCP tool execution failed: {str(e)}"}]
            }


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
            tool_name="mcp_discover",
            tool_spec={
                "name": "mcp_discover",
                "description": "Discover available MCP tools on connected servers",
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
        """
        Discover available MCP tools.
        
        Args:
            tool_use: The tool use request
            **kwargs: Additional keyword arguments
            
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
                return {
                    "toolUseId": tool_use.get("toolUseId", "unknown"),
                    "status": "success",
                    "content": [{"text": json.dumps(response.json(), indent=2)}]
                }
            else:
                return {
                    "toolUseId": tool_use.get("toolUseId", "unknown"),
                    "status": "error",
                    "content": [{"text": f"MCP discovery failed with status code {response.status_code}: {response.text}"}]
                }
        except Exception as e:
            return {
                "toolUseId": tool_use.get("toolUseId", "unknown"),
                "status": "error",
                "content": [{"text": f"MCP tool discovery failed: {str(e)}"}]
            }


# Example of how to register MCP tools with the agent
def register_mcp_tools(tool_registry, mcp_server_url: str = "http://localhost:8080"):
    """
    Register MCP tools with the agent's tool registry.
    
    Args:
        tool_registry: The agent's tool registry
        mcp_server_url: URL of the MCP server
    """
    tool_registry.register_tool(MCPTool(mcp_server_url))
    tool_registry.register_tool(MCPToolDiscovery(mcp_server_url))
