#!/usr/bin/env python3
"""
Simplified Documentation Assistant using Amazon Bedrock directly.
This version doesn't rely on the Strands library.
"""

import os
import json
import boto3
import argparse
from typing import Dict, List, Any, Optional


class DocumentationAssistant:
    """A documentation assistant that uses Amazon Bedrock for natural language understanding."""
    
    def __init__(
        self, 
        docs_path: str = "./docs",
        model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
        region_name: str = "us-east-1",
        profile_name: Optional[str] = None
    ):
        """
        Initialize the documentation assistant.
        
        Args:
            docs_path: Path to the documentation directory
            model_id: Bedrock model ID to use
            region_name: AWS region name
            profile_name: AWS profile name (optional)
        """
        self.docs_path = docs_path
        self.model_id = model_id
        
        # Initialize Bedrock client
        session_kwargs = {}
        if profile_name:
            session_kwargs["profile_name"] = profile_name
            
        session = boto3.Session(region_name=region_name, **session_kwargs)
        self.bedrock_runtime = session.client(
            service_name="bedrock-runtime",
            region_name=region_name
        )
        
        # Ensure docs directory exists
        if not os.path.exists(docs_path):
            os.makedirs(docs_path)
    
    def search_docs(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search through documentation.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results
        """
        results = []
        
        # Simple file-based search implementation
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
    
    def read_doc(self, file_path: str) -> Dict[str, Any]:
        """
        Read a documentation file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return {
                    "file": file_path,
                    "content": content
                }
        except Exception as e:
            return {"error": f"Failed to read file {file_path}: {str(e)}"}
    
    def invoke_bedrock(
        self, 
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """
        Invoke a Bedrock model.
        
        Args:
            prompt: The prompt to send to the model
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling
            top_p: Top-p sampling parameter
            
        Returns:
            The model's response text
        """
        # Handle different model providers
        if "anthropic" in self.model_id.lower():
            return self._invoke_anthropic(prompt, max_tokens, temperature, top_p)
        elif "amazon" in self.model_id.lower():
            return self._invoke_amazon(prompt, max_tokens, temperature, top_p)
        else:
            raise ValueError(f"Unsupported model provider in model_id: {self.model_id}")
    
    def _invoke_anthropic(
        self, 
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
            modelId=self.model_id,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response.get("body").read())
        return response_body.get("content")[0].get("text")
    
    def _invoke_amazon(
        self, 
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
            modelId=self.model_id,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response.get("body").read())
        return response_body.get("results")[0].get("outputText")
    
    def process_query(self, query: str) -> str:
        """
        Process a user query.
        
        Args:
            query: User query
            
        Returns:
            Response to the user
        """
        # First, search for relevant documentation
        search_results = self.search_docs(query)
        
        if not search_results:
            return "I couldn't find any relevant documentation for your query."
        
        # Read the content of the top results
        doc_contents = []
        for result in search_results[:3]:  # Limit to top 3 results
            file_path = result["file"]
            doc_data = self.read_doc(file_path)
            if "error" not in doc_data:
                doc_contents.append({
                    "file": file_path,
                    "content": doc_data["content"]
                })
        
        if not doc_contents:
            return "I found some documentation but couldn't read the content."
        
        # Construct a prompt for the model
        prompt = f"""
        I need you to answer a question based on the documentation provided below.
        
        Question: {query}
        
        Documentation:
        """
        
        for i, doc in enumerate(doc_contents):
            prompt += f"\n--- Document {i+1}: {doc['file']} ---\n{doc['content']}\n"
        
        prompt += """
        Based on the documentation above, please provide a concise and accurate answer to the question.
        If the documentation doesn't contain the answer, please state that clearly.
        Include references to the specific documents you used in your answer.
        """
        
        # Invoke the model
        try:
            response = self.invoke_bedrock(prompt)
            return response
        except Exception as e:
            return f"I encountered an error while processing your query: {str(e)}"


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Documentation Assistant")
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
    
    # Create the assistant
    assistant = DocumentationAssistant(
        docs_path=args.docs_path,
        model_id=args.model_id,
        region_name=args.region,
        profile_name=args.profile
    )
    
    print("\nDocumentation Assistant initialized. Type 'exit' to quit.")
    print("Ask me anything about the documentation!")
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        # Process the user's request
        response = assistant.process_query(user_input)
        
        # Display the response
        print(f"\nAssistant: {response}")


if __name__ == "__main__":
    main()
