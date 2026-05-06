# github_utils.py
import requests
import time
import sys
import config  # <-- This line was missing in the original snippet

GITHUB_API_BASE = "https://api.github.com"

def get_github_headers():
    return {
        "Authorization": f"token {config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

def merge_pull_request(pr_number):
    """Merges a pull request using the GitHub API."""
    url = f"{GITHUB_API_BASE}/repos/{config.GITHUB_OWNER}/{config.GITHUB_REPO}/pulls/{pr_number}/merge"
    payload = {"merge_method": "squash"}
    
    print(f"   ⏳ Attempting to merge PR #{pr_number}...")
    response = requests.put(url, headers=get_github_headers(), json=payload)
    
    if response.status_code == 200:
        print(f"   ✅ PR #{pr_number} merged successfully.")
        return response.json()
    else:
        print(f"   ❌ Failed to merge PR #{pr_number}. Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return None

def delete_branch(branch_name):
    """Deletes a branch from the remote repository."""
    url = f"{GITHUB_API_BASE}/repos/{config.GITHUB_OWNER}/{config.GITHUB_REPO}/git/refs/heads/{branch_name}"
    
    print(f"   🗑️  Deleting branch '{branch_name}'...")
    response = requests.delete(url, headers=get_github_headers())
    
    if response.status_code == 204:
        print(f"   ✅ Branch '{branch_name}' deleted.")
    else:
        print(f"   ⚠️ Could not delete branch '{branch_name}'. Status: {response.status_code}")

def get_combined_status(ref_name):
    """Gets the combined commit status for a given ref (e.g., a branch)."""
    url = f"{GITHUB_API_BASE}/repos/{config.GITHUB_OWNER}/{config.GITHUB_REPO}/commits/{ref_name}/status"
    response = requests.get(url, headers=get_github_headers())
    if response.status_code == 200:
        return response.json()
    return None

def wait_for_ci(ref_name, max_wait_seconds=900, poll_interval=15):
    """
    Polls the CI status for a given ref until it's successful or fails.
    Returns True if successful, False otherwise.
    """
    print(f"   ⏳ Waiting for CI checks to pass on '{ref_name}'...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait_seconds:
        status = get_combined_status(ref_name)
        if status is None:
            print("   Could not retrieve status, retrying...")
            time.sleep(poll_interval)
            continue
            
        state = status.get("state")
        print(f"   Current CI status: {state}")
        
        if state == "success":
            print(f"   ✅ CI checks passed!")
            return True
        elif state == "failure":
            print(f"   ❌ CI checks failed! Check details on GitHub.")
            return False
            
        time.sleep(poll_interval)
    
    print(f"   ⏰ CI checks timed out after {max_wait_seconds}s.")
    return False