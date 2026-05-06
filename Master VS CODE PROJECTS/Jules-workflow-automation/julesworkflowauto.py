import requests
import time
import os

# ==========================================
#  🔐 YOUR SECRETS (you only need to add your API key now)
# ==========================================
JULES_API_KEY = "AQ.Ab8RN6IorRSWhNMkhWjQOjMYiRCDjqmCil3hG-ybzML9Wzc_DA"  # <--- REPLACE THIS
YOUR_SOURCE_ID = "sources/github/RocelioDaSilva/THE-petrolumen"  # <--- Already set!

# ==========================================
#  📋 YOUR SEQUENTIAL PLANS
#  Edit the prompts for each plan below.
# ==========================================
task_plans = [
    {
        "title": "Plan 1: Refactor User model",
        "prompt": "Refactor the User model to include separate methods for full name and address formatting. Ensure all existing tests still pass.",
        "starting_branch": "main"
    },
    {
        "title": "Plan 2: Add email validation",
        "prompt": "Create a new utility function for email validation and add corresponding unit tests.",
        "starting_branch": "main"
    },
    {
        "title": "Plan 3: Update API endpoint",
        "prompt": "Update the PUT /user/settings API endpoint to use the new User model methods created in Plan 1.",
        "starting_branch": "main"
    }
]

# Final repo-wide analysis task
analysis_task = {
    "title": "Final Repo Analysis",
    "prompt": "Perform a thorough review of the entire repository. Check for weaknesses, areas for improvement, potential bugs, and any code that could be refactored for better performance, readability, or security. Create a detailed plan for each finding and implement the suggested improvements."
}

# ==========================================
#  ⚙️ DO NOT EDIT BELOW THIS LINE
# ==========================================
API_BASE_URL = "https://jules.googleapis.com/v1alpha"
HEADERS = {
    "X-Goog-Api-Key": JULES_API_KEY,
    "Content-Type": "application/json"
}

def run_jules_session(task, source_id, starting_branch_override=None):
    title = task["title"]
    prompt = task["prompt"]
    branch = starting_branch_override if starting_branch_override else task["starting_branch"]
    
    print(f"\n🚀 Starting Task: {title}")
    print(f"   Branch base: {branch}")

    payload = {
        "prompt": prompt,
        "title": title,
        "sourceContext": {
            "source": source_id,
            "githubRepoContext": {"startingBranch": branch}
        },
        "automationMode": "AUTO_CREATE_PR",
        "requirePlanApproval": False
    }

    # Create session
    try:
        resp = requests.post(f"{API_BASE_URL}/sessions", headers=HEADERS, json=payload)
        resp.raise_for_status()
        session = resp.json()
        session_name = session["name"]
        print(f"✅ Session created: {session_name}")
    except Exception as e:
        print(f"❌ Failed to create session: {e}")
        return None

    # Wait for completion
    while True:
        time.sleep(30)  # check every 30 seconds
        try:
            check = requests.get(f"{API_BASE_URL}/{session_name}", headers=HEADERS)
            check.raise_for_status()
            session_data = check.json()
            state = session_data.get("state")
            print(f"   Status: {state}")
            if state == "COMPLETED":
                print(f"🏁 Task '{title}' completed!")
                pr_url = session_data.get("output", {}).get("pullRequest", {}).get("url")
                if pr_url:
                    print(f"🔗 Pull Request: {pr_url}")
                return session_data
            elif state == "FAILED":
                error_msg = session_data.get("error", "No error details")
                print(f"❌ Task '{title}' failed: {error_msg}")
                return None
        except Exception as e:
            print(f"   Network error, retrying... ({e})")
            time.sleep(60)

if __name__ == "__main__":
    print("========================================")
    print("JULES AUTOMATIC SEQUENTIAL PIPELINE")
    print("========================================")
    
    if JULES_API_KEY == "PASTE_YOUR_API_KEY_HERE" or "your-username" in YOUR_SOURCE_ID:
        print("⚠️  Please edit the script and replace YOUR_API_KEY and YOUR_SOURCE_ID first!")
        exit(1)

    for i, plan in enumerate(task_plans):
        result = run_jules_session(plan, YOUR_SOURCE_ID)
        if result is None:
            print("\n🛑 Pipeline stopped because a task failed.")
            break
        # After each successful plan, ask user to merge the PR
        print("\n----------------------------------------")
        print("⚠️  ACTION REQUIRED: Please go to GitHub and merge the Pull Request.")
        print("   (Wait until the merge is fully complete before continuing.)")
        input("   Press Enter here AFTER you have merged the PR...")
        print("----------------------------------------\n")
    else:
        # All plans done, run final analysis
        print("\n🔍 All plans completed. Starting final repo-wide analysis...")
        run_jules_session(analysis_task, YOUR_SOURCE_ID, starting_branch_override="main")
        print("\n✅ Pipeline finished. Final analysis results are in the new Pull Request.")