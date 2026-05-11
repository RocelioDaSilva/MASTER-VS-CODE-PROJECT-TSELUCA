# GitHub Repository Setup Guide

Complete step-by-step instructions for creating and pushing the GEESP-Angola project to GitHub.

## Overview

This guide walks you through:
1. Installing Git
2. Creating a GitHub account (if needed)
3. Creating the repository on GitHub
4. Initializing and pushing your local code
5. Configuring repository settings

---

## Step 1: Install Git

### Windows

1. Download Git for Windows from: https://git-scm.com/download/win
2. Run the installer (Git-2.x.x-64-bit.exe or 32-bit version)
3. Follow the installer steps:
   - Accept license
   - Choose installation directory
   - Accept default options (or customize if you prefer)
   - For editor, select VS Code or your preferred editor
   - For default branch, select `main`
   - Install

4. Verify installation by opening PowerShell and typing:
   ```powershell
   git --version
   ```
   You should see something like: `git version 2.x.x.windows.x`

### macOS

```bash
# Using Homebrew (if installed)
brew install git

# Or using MacPorts
sudo port install git +universal
```

### Linux

```bash
# Ubuntu/Debian
sudo apt-get install git

# Fedora
sudo dnf install git

# Arch
sudo pacman -S git
```

---

## Step 2: Create GitHub Account

1. Visit https://github.com
2. Click "Sign up"
3. Enter email, create password, choose username
4. Complete verification steps
5. Verify email address

**Recommendations**:
- Use a professional username (e.g., `ISPTEC-Energy`)
- Use institutional email if available
- Enable two-factor authentication for security

---

## Step 3: Create Repository on GitHub

1. Sign in to GitHub (https://github.com)
2. Click **+** icon in top-right corner → **New repository**
3. Configure repository:

   | Setting | Value |
   |---------|-------|
   | **Repository name** | `geesp-angola` |
   | **Description** | `Geospatial Analysis and Energy Strategic Planning for Angola` |
   | **Visibility** | Public (or Private if preferred) |
   | **Initialize with** | ❌ DO NOT check "Add a README" |
   | | ❌ DO NOT check "Add .gitignore" |
   | | ❌ DO NOT check "Choose a license" |

4. Click **Create repository**

5. **Important**: You'll see quick setup instructions. Keep this page open - you'll need the URL:
   ```
   https://github.com/YOUR-USERNAME/geesp-angola.git
   ```

---

## Step 4: Configure Git Locally

Open PowerShell (Windows) or Terminal (Mac/Linux) and run:

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (use same as GitHub)
git config --global user.email "your.email@gmail.com"

# Verify configuration
git config --global --list
```

---

## Step 5: Initialize Repository & Push to GitHub

### Option A: Push Existing Local Folder

If you already have code locally (which you do):

```bash
# Navigate to your project
cd "c:\Users\rocel\OneDrive\Desktop\MIT SCIENCE PAPER\Coding parts\geesp-angola"

# Initialize git (one-time)
git init
git config user.name "GEESP-Angola"
git config user.email "geesp@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "feat: Initial commit - GEESP-Angola v1.0.0

- Core MCDA analysis framework with AHP weighting
- Google Earth Engine data extraction module
- LCOE financial calculator for solar technologies
- Streamlit interactive dashboard with 5 pages
- Demonstration maps and analysis tools
- Complete documentation and guides"

# Add remote repository
git remote add origin https://github.com/YOUR-USERNAME/geesp-angola.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Replace `YOUR-USERNAME` with your actual GitHub username**

### Option B: Alternative - Using GitHub CLI

If you have GitHub CLI installed:

```bash
# Install (if not already installed)
# Windows: winget install GitHub.cli
# Mac: brew install gh

# Authenticate
gh auth login

# Create repository from current directory
gh repo create geesp-angola --public --source=. --remote=origin --push
```

---

## Step 6: Verify Push Success

1. Go to https://github.com/YOUR-USERNAME/geesp-angola
2. You should see:
   - All your files and folders
   - Recent commit message
   - File tree showing project structure
   - README.md displayed as default page

---

## Step 7: Configure Repository Settings

### Branch Protection (Recommended)

1. Go to **Settings** → **Branches**
2. Click **Add rule** under "Branch protection rules"
3. Apply to branch: `main`
4. Enable:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date

### Collaboration Settings

1. Go to **Settings** → **Collaborators and teams**
2. Add team members who can contribute
3. Assign appropriate roles (Maintain, Write, Read)

### Topics & Visibility

1. Go to **About** (⚙️ gear icon on main page)
2. Add topics: `renewable-energy` `gis` `mcda` `python` `streamlit`
3. Check "Use as your profile README"

---

## Step 8: Configure GitHub Pages (Optional)

To host project documentation as a website:

1. Go to **Settings** → **Pages**
2. Select source: `main` branch, `/root` folder
3. Choose a theme (jekyll-theme-slate is nice)
4. Save

Your documentation will be available at: https://YOUR-USERNAME.github.io/geesp-angola

---

## Step 9: Add GitHub Actions CI/CD (Optional)

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pip install pytest
      - run: pytest tests/
      - run: black --check scripts/ dashboard/
      - run: flake8 scripts/ dashboard/
```

---

## Future: Releases & Versioning

When you're ready to release:

1. Update version in:
   - `CHANGELOG.md`
   - Any version files
   
2. Create git tag:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

3. On GitHub:
   - Go to **Releases**
   - Click **Create a new release**
   - Select tag `v1.0.0`
   - Add release notes (copy from CHANGELOG.md)
   - Publish release

---

## Common Commands Reference

```bash
# Check status
git status

# Add files
git add .                      # Add all files
git add file.py                # Add specific file

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push                       # Push current branch
git push origin main           # Push to main branch
git push --all                 # Push all branches

# Pull changes
git pull                       # Get latest from GitHub

# Create branches
git checkout -b feature/name    # Create and switch to branch
git checkout main              # Switch to main branch

# View history
git log                        # View commit history
git log --oneline              # Short format

# Undo changes
git restore file.py            # Discard local changes
git revert <commit-hash>       # Undo a commit (keeps history)
```

---

## Troubleshooting

### "Permission denied (publickey)"
You need to set up SSH keys:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@gmail.com"

# Add to GitHub
# 1. Copy output of: cat ~/.ssh/id_ed25519.pub
# 2. Go to GitHub Settings → SSH and GPG keys
# 3. Click New SSH key
# 4. Paste the key

# Test connection
ssh -T git@github.com
```

### "fatal: not a git repository"
You need to initialize git:
```bash
git init
```

### "remote already exists"
If you get an error about origin already existing:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/geesp-angola.git
```

### "Your branch is ahead of origin/main by X commits"
Push your commits:
```bash
git push origin main
```

---

## Next Steps

After pushing to GitHub:

1. ✅ **Share the repository link**
   - Anyone can now access: https://github.com/YOUR-USERNAME/geesp-angola

2. ✅ **Add collaborators**
   - Settings → Collaborators → Add collaborators by username

3. ✅ **Set up GitHub Pages** (optional)
   - Publish documentation as a website

4. ✅ **Create GitHub Projects** (optional)
   - Track issues and features in a Kanban-style board

5. ✅ **Write GitHub Issues & Discussions**
   - Document bugs, features, and ideas

---

## Additional Resources

- **Git Documentation**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com/
- **GitHub Help**: https://help.github.com/
- **Markdown Guide**: https://www.markdownguide.org/

---

## Support

If you get stuck:
1. Check GitHub Help: https://help.github.com/
2. Search existing GitHub issues
3. Ask on Stack Overflow with `git` and `github` tags
4. Contact the repository maintainers

---

**Created**: February 8, 2026
**For**: GEESP-Angola Project
**Repository**: https://github.com/ISPTEC-Energy/geesp-angola
