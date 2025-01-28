import requests
import json
import os
from typing import Optional, Dict, Any, List
from pathlib import Path
from get_file_wise_git_diff import get_pr_diff_by_file
from code_analyzer import analyze_code
from display_analysis import display_analysis

def main():
    """Main function to run the code analysis on files in the directory."""
    # Get API key from environment variable or input
    api_key ="xxx"
    
    # Get list of code files
    print("\nScanning for code files...")
    code_files = get_pr_diff_by_file("https://github.com/anushka2125/test_code_analyzer/pull/3")
    
    if not code_files:
        print("No code files found in the current directory!")
        return
    
    print("\nFound the following code files:")

    for file_name, diff in code_files.items():
        print(f"File: {file_name}")
        print(f"Git Diff:\n{diff}")
        print("\n" + "="*40 + "\n") 

    # Let user select files to analyze
    while True:
        selection = input("\nEnter file numbers to analyze (comma-separated) or 'all' for all files: ").strip().lower()
        
        if selection == 'all':
            print(code_files)
            files_to_analyze = code_files
            break
    
    # Analyze each selected file
    for file_name, diff in files_to_analyze.items():
        print(f"\nAnalyzing...")
        code = files_to_analyze[file_name]
        if code:
            response = analyze_code(api_key, code, str(file_name))
            if response:
                display_analysis(str(file_name), response)
            else:
                print(f"Analysis failed for {file_name}")

if __name__ == "__main__":
    main()