#!/usr/bin/env bash
# Script to initialize a git repo and push to GitHub once git/gh are available.
# Run locally on your machine where git and (optionally) gh CLI are installed.

set -e

# initialize
if [ ! -d .git ]; then
  git init
  git add .
  git commit -m "Initial commit: GEESP-Angola project"
fi

echo "Local repo initialized. To create a GitHub repo and push, run:" \
     "\n  gh repo create <owner>/<repo> --public --source=. --remote=origin --push\n" \
     "Or manually create a repo and run:\n  git remote add origin <url>\n  git branch -M main\n  git push -u origin main\n"
