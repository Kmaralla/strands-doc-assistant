#!/usr/bin/env python3
"""
Documentation processor for the Strands Documentation Assistant.
This module provides utilities for processing and indexing documentation.
"""

import os
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path


class DocumentationProcessor:
    """Processor for documentation files."""
    
    def __init__(self, docs_path: str = "./docs"):
        """
        Initialize the documentation processor.
        
        Args:
            docs_path: Path to the documentation directory
        """
        self.docs_path = docs_path
        self.index = {}
        
    def index_documentation(self) -> Dict[str, Any]:
        """
        Index all documentation files.
        
        Returns:
            Dictionary containing the index
        """
        self.index = {
            "files": [],
            "keywords": {}
        }
        
        # Ensure the docs directory exists
        if not os.path.exists(self.docs_path):
            os.makedirs(self.docs_path)
            
        # Walk through the docs directory
        for root, _, files in os.walk(self.docs_path):
            for file in files:
                if file.endswith(('.md', '.txt', '.html')):
                    file_path = os.path.join(root, file)
                    try:
                        # Process the file
                        file_info, keywords = self._process_file(file_path)
                        
                        # Add to the index
                        self.index["files"].append(file_info)
                        
                        # Update keywords
                        for keyword in keywords:
                            if keyword not in self.index["keywords"]:
                                self.index["keywords"][keyword] = []
                            self.index["keywords"][keyword].append(file_info["id"])
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")
        
        return self.index
    
    def _process_file(self, file_path: str) -> Tuple[Dict[str, Any], List[str]]:
        """
        Process a single documentation file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Tuple of (file_info, keywords)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract title
        title = os.path.basename(file_path)
        if file_path.endswith('.md'):
            # Try to extract title from markdown
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                title = title_match.group(1)
        
        # Generate a simple ID
        file_id = os.path.relpath(file_path, self.docs_path).replace('/', '_').replace('\\', '_')
        
        # Extract keywords (simple implementation)
        words = re.findall(r'\b\w+\b', content.lower())
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Ignore short words
                word_freq[word] = word_freq.get(word, 0) + 1
                
        # Get top keywords
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        keywords = [k for k, _ in keywords]
        
        # Create file info
        file_info = {
            "id": file_id,
            "path": file_path,
            "title": title,
            "size": len(content),
            "modified": os.path.getmtime(file_path)
        }
        
        return file_info, keywords
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search the documentation.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results
        """
        if not self.index:
            self.index_documentation()
            
        results = []
        query_terms = query.lower().split()
        
        # Check each file
        for file_info in self.index["files"]:
            score = 0
            file_path = file_info["path"]
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    
                # Score based on term frequency
                for term in query_terms:
                    score += content.count(term)
                    
                # If any term appears, add to results
                if score > 0:
                    results.append({
                        "file": file_path,
                        "title": file_info["title"],
                        "score": score,
                        "preview": content[:200] + "..." if len(content) > 200 else content
                    })
            except Exception as e:
                print(f"Error searching file {file_path}: {e}")
                
        # Sort by relevance score and limit results
        results = sorted(results, key=lambda x: x["score"], reverse=True)[:max_results]
        return results
    
    def save_index(self, index_path: str = "docs_index.json") -> None:
        """
        Save the index to a file.
        
        Args:
            index_path: Path to save the index
        """
        if not self.index:
            self.index_documentation()
            
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2)
    
    def load_index(self, index_path: str = "docs_index.json") -> Dict[str, Any]:
        """
        Load the index from a file.
        
        Args:
            index_path: Path to the index file
            
        Returns:
            The loaded index
        """
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
        else:
            self.index_documentation()
            
        return self.index
