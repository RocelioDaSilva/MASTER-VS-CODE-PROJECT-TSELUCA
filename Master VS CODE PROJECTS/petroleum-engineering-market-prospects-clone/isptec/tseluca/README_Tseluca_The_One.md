Transform this workspace into GitHub repo `Tseluca_The_One`

Usage (PowerShell):

```powershell
cd "c:\Users\rocel\OneDrive\Desktop\petroleum-engineering-market-prospects\isptec\tseluca"
# Create the remote repo and push (requires PAT with repo scope)
./create_and_push_Tseluca_The_One.ps1 -Token '<YOUR_PERSONAL_ACCESS_TOKEN>' -RepoName 'Tseluca_The_One' -Visibility 'public'

# If you prefer to keep an existing 'origin' remote, add -NoRenameOrigin
# Or authenticate locally with `gh auth login` and use `gh repo create` instead.
```

Notes:
- The script will rename an existing `origin` remote to `upstream` by default.
- A local git repo and an initial commit were created for you.
- A bundle `Tseluca_The_One.bundle` was generated as a backup.
