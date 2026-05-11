# orchestrator.py
import requests
import json
import time
import sys
import config
import github_utils

def run_jules_task(task):
    print(f"\n🚀 --- Starting Task: '{task['title']}' ---")
    
    create_url = f"{config.API_BASE_URL}/sessions"
    payload = {
        "prompt": task["prompt"],
        "title": task["title"],
        "sourceContext": {
            "source": config.JULES_SOURCE_FULL_NAME,
            "githubRepoContext": {"startingBranch": config.BASE_BRANCH}
        },
        "automationMode": "AUTO_CREATE_PR",
        "requirePlanApproval": False
    }
    
    try:
        response = requests.post(create_url, headers=config.HEADERS, json=payload)
        response.raise_for_status()
        session = response.json()
        print(f"   Session created: {session['name']}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to create session for '{task['title']}'. Error: {e}")
        return None

    session_name = session["name"]
    get_url = f"{config.API_BASE_URL}/{session_name}"
    poll_interval = 30

    while True:
        time.sleep(poll_interval)
        try:
            response = requests.get(get_url, headers=config.HEADERS)
            response.raise_for_status()
            updated_session = response.json()
            state = updated_session.get("state")
            print(f"   Status for '{task['title']}': {state}")
            
            if state == "COMPLETED":
                print(f"   ✅ Task completed successfully!")
                output = updated_session.get("output", {})
                pr_link = output.get("pullRequest", {}).get("url")
                if pr_link:
                    print(f"   📎 PR Created: {pr_link}")
                return updated_session
            elif state == "FAILED":
                print(f"   ❌ Task failed.")
                error = updated_session.get("error", {})
                print(f"   Error details: {error}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️ Error polling session: {e}. Retrying...")
            time.sleep(poll_interval * 2)

def run_full_pipeline():
    print("🏁 Starting automated Jules pipeline!")
    
    for i, task in enumerate(config.SEQUENTIAL_TASKS, 1):
        print(f"\n--- Plan {i}/{len(config.SEQUENTIAL_TASKS)} ---")
        
        completed_session = run_jules_task(task)
        if not completed_session:
            print("Pipeline halted due to task failure.")
            sys.exit(1)
            
        output = completed_session.get("output", {})
        pr_info = output.get("pullRequest", {})
        pr_number = pr_info.get("number")
        head_branch = pr_info.get("head", {}).get("ref")
        
        if not pr_number or not head_branch:
            print("❌ Pipeline halted. Could not find PR details from Jules session.")
            sys.exit(1)
            
        if not github_utils.wait_for_ci(head_branch):
            print(f"❌ Pipeline halted. CI failed for PR #{pr_number}.")
            sys.exit(1)
            
        merge_result = github_utils.merge_pull_request(pr_number)
        if not merge_result:
            print(f"❌ Pipeline halted. Could not merge PR #{pr_number}.")
            sys.exit(1)
            
        github_utils.delete_branch(head_branch)
        print(f"   🎉 Task '{task['title']}' fully integrated into main.")

    print("\n" + "="*50)
    print("🚀 All sequential plans completed. Starting final repo analysis...")
    print("="*50)
    run_jules_task(config.FINAL_ANALYSIS_TASK)
    
    print("\n🏁 Pipeline complete. Final analysis PR is ready for your review.")

if __name__ == "__main__":
    run_full_pipeline()