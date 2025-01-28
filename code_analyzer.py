import requests
import json
import os
from typing import Optional, Dict, Any, List
from pathlib import Path
from get_file_wise_git_diff import get_pr_diff_by_file

def analyze_code(api_key: str, code: str, filename: str, model: str = "llama3-8b-8192") -> Optional[Dict[Any, Any]]:
    """
    Analyze code using Groq API for style, syntax, and best practices.
    
    Args:
        api_key (str): Your Groq API key
        code (str): The code to analyze
        filename (str): Name of the file being analyzed
        model (str): The model to use for analysis
        
    Returns:
        Optional[Dict]: The API response as a dictionary, or None if the request fails
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    prompt = f"""Please analyze the following code from file '{filename}' according to these criteria:

1. Syntax and Basic Structure:
   - Check for syntax errors
   - Verify proper spacing around operators
   - Check line length (should be ≤79 characters for Python)
   - Verify correct placement of braces/parentheses/brackets
   
2. Documentation and Whitespace:
   - Check docstring and comment formatting
   - Verify appropriate empty line usage
   - Check for trailing whitespace
   
3. Indentation and Code Blocks:
   - Verify consistent indentation (spaces vs tabs)
   - Check proper indentation of code blocks
   - Analyze nested structure indentation
   - Look for mixed indentation issues
   
4. Symbols and Completeness:
   - Check for missing symbols (parentheses, brackets, commas, colons)
   - Identify unclosed strings or comments
   - Verify proper function definitions
   
5. Logic and References:
   - Check variable assignments and references
   - Verify correct operator usage
   - Analyze language-specific syntax requirements

Here is the code to analyze:

{code}

Provide us with line numbers of what you think needs to be changed based on the above conditions."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response content: {e.response.text}")
        return None
    
    except json.JSONDecodeError as e:
        print(f"Error decoding response: {e}")
        return None

# def display_analysis(filename: str, response: Dict[Any, Any]) -> None:
#     """
#     Display the code analysis results in a readable format.
    
#     Args:
#         filename (str): Name of the file analyzed
#         response (Dict): The API response containing the analysis
#     """
#     if response and 'choices' in response:
#         analysis = response['choices'][0]['message']['content']
#         print(f"\nCode Analysis Results for {filename}:")
#         print("=" * 80)
#         print(analysis)
#         print("=" * 80)
#     else:
#         print(f"No analysis results available for {filename}.")
