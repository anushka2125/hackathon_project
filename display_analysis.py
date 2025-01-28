from typing import Optional, Dict, Any, List

def display_analysis(filename: str, response: Dict[Any, Any]) -> None:
    """
    Display the code analysis results in a readable format.
    
    Args:
        filename (str): Name of the file analyzed
        response (Dict): The API response containing the analysis
    """
    if response and 'choices' in response:
        analysis = response['choices'][0]['message']['content']
        print(f"\nCode Analysis Results for {filename}:")
        print("=" * 80)
        print(analysis)
        print("=" * 80)
    else:
        print(f"No analysis results available for {filename}.")