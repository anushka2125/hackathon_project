import requests
from typing import List, Dict


def get_pr_diff_by_file(pr_url: str, extensions: List[str] = [".py", ".js", ".java", ".cpp", ".cs"]) -> Dict[str, str]:
    """
    Fetch the git diff for the specified GitHub pull request URL and separate it by file.

    Args:
        pr_url (str): GitHub pull request URL.
        extensions (List[str]): List of file extensions to include.

    Returns:
        Dict[str, str]: Dictionary where keys are filenames and values are the git diff for each file.
    """
    # Parse the GitHub URL to extract the repository and PR number
    parts = pr_url.rstrip('/').split('/')
    if len(parts) < 5 or parts[-2] != 'pull':
        raise ValueError("Invalid GitHub PR URL format")
    
    repo_owner = parts[-4]
    repo_name = parts[-3]
    pr_number = parts[-1]

    # Prepare the API URL to fetch the PR diff
    api_url = f"https://github.com/{repo_owner}/{repo_name}/pull/{pr_number}.diff"

    # Make the request to GitHub API
    response = requests.get(api_url)
    print(f"response git diff = {response.text}")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch PR diff from GitHub: {response.status_code}, {response.text}")

    diff_content = response.text
    file_diffs = {}

    # Split the diff content by the file headers (lines starting with "diff --git")
    file_diff_blocks = diff_content.split("diff --git")
    
    for block in file_diff_blocks:
        # Skip empty blocks
        if not block.strip():
            continue
        
        # Look for the file name in the diff block (it should start with 'a/filename' or 'b/filename')
        lines = block.strip().splitlines()
        
        # Extract file name from the header line, it will be something like "a/path/to/file.py"
        file_header = next((line for line in lines if line.startswith('a/') or line.startswith('b/')), None)
        
        if file_header:
            # Extract file name from the header
            file_name = file_header.split()[0][2:]  # Remove 'a/' or 'b/' prefix

            # Check if the file has the correct extension
            if any(file_name.endswith(ext) for ext in extensions):
                # Join the diff content for the current file
                file_diff = "\n".join(lines[1:])  # Skip the first line (diff --git ...)

                file_diffs[file_name] = file_diff

    return file_diffs
