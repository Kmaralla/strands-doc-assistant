#!/usr/bin/env python3
"""
Amazon Bedrock integration for the Strands Documentation Assistant.
This module provides utilities for working with Amazon Bedrock.
"""

import boto3
import json
from typing import Dict, Any, List, Optional


class BedrockClient:
    """Client for interacting with Amazon Bedrock."""
    
    def __init__(self, region_name: str = "us-east-1", profile_name: Optional[str] = None):
        """
        Initialize the Bedrock client.
        
        Args:
            region_name: AWS region name
            profile_name: AWS profile name (optional)
        """
        session_kwargs = {}
        if profile_name:
            session_kwargs["profile_name"] = profile_name
            
        session = boto3.Session(region_name=region_name, **session_kwargs)
        self.bedrock_runtime = session.client(
            service_name="bedrock-runtime",
            region_name=region_name
        )
    
    def invoke_model(
        self, 
        model_id: str, 
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """
        Invoke a Bedrock model with the given prompt.
        
        Args:
            model_id: The Bedrock model ID
            prompt: The prompt to send to the model
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling
            top_p: Top-p sampling parameter
            
        Returns:
            The model's response text
        """
        # Handle different model providers
        if "anthropic" in model_id.lower():
            return self._invoke_anthropic(model_id, prompt, max_tokens, temperature, top_p)
        elif "amazon" in model_id.lower():
            return self._invoke_amazon(model_id, prompt, max_tokens, temperature, top_p)
        else:
            raise ValueError(f"Unsupported model provider in model_id: {model_id}")
    
    def _invoke_anthropic(
        self, 
        model_id: str, 
        prompt: str,
        max_tokens: int,
        temperature: float,
        top_p: float
    ) -> str:
        """Invoke an Anthropic model."""
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature,
            "top_p": top_p
        }
        
        response = self.bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response.get("body").read())
        return response_body.get("content")[0].get("text")
    
    def _invoke_amazon(
        self, 
        model_id: str, 
        prompt: str,
        max_tokens: int,
        temperature: float,
        top_p: float
    ) -> str:
        """Invoke an Amazon model."""
        request_body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": max_tokens,
                "temperature": temperature,
                "topP": top_p
            }
        }
        
        response = self.bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response.get("body").read())
        return response_body.get("results")[0].get("outputText")


def list_available_models(region_name: str = "us-east-1", profile_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List available Bedrock models.
    
    Args:
        region_name: AWS region name
        profile_name: AWS profile name (optional)
        
    Returns:
        List of available models
    """
    session_kwargs = {}
    if profile_name:
        session_kwargs["profile_name"] = profile_name
        
    session = boto3.Session(region_name=region_name, **session_kwargs)
    bedrock = session.client(service_name="bedrock", region_name=region_name)
    
    response = bedrock.list_foundation_models()
    return response.get("modelSummaries", [])
