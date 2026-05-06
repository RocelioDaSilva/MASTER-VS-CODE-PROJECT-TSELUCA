Uploading prompts to a GitHub Gist

This file explains how to create a Gist containing the generated prompt files using the included `gist_upload.ps1` script.

1) Create a GitHub personal access token (PAT)
- Visit https://github.com/settings/tokens
- Generate a new token with the `gist` scope (no other scopes required)
- Copy the token immediately (you won't see it again)

2) Set the token in your PowerShell session
```powershell
$env:GITHUB_TOKEN = "ghp_your_token_here"
```

3) Run the uploader
```powershell
cd c:\Users\PCGAME\Desktop\story&universes\chain-weapon-story
.
\tools\image_pipeline\gist_upload.ps1
```

4) If successful, the script will print the created Gist URL.

Notes & alternatives
- If you prefer bash/curl, you can perform a similar POST to `https://api.github.com/gists` with the same JSON payload.
- If you want the Gist to be public, edit the `$Public` parameter in `gist_upload.ps1` or run the script with `-Public $true`.
- Keep your PAT secret. Do not commit it to the repository.
