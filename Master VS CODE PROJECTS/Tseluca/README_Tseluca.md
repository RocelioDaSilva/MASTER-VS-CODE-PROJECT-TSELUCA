create_and_push_to_github.ps1

Usage (PowerShell):

```powershell
cd "c:\Users\rocel\OneDrive\Desktop\petroleum-engineering-market-prospects\isptec\tseluca\petrolumenisback"
./create_and_push_to_github.ps1 -Token '<YOUR_PERSONAL_ACCESS_TOKEN>' -RepoName 'Tseluca' -Visibility 'public'
```

Notes:
- The script requires a GitHub Personal Access Token (`repo` scope).
- By default the script renames an existing `origin` remote to `upstream`; pass `-NoRenameOrigin` to skip renaming.
- Alternatively you can authenticate locally with `gh auth login` and run `gh repo create` instead.
