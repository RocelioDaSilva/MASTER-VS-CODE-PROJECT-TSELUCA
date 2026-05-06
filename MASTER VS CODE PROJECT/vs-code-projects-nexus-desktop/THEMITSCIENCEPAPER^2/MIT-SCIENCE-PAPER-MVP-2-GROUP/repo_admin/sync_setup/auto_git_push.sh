#!/usr/bin/env bash
# WARNING: This auto-commit script is intentionally minimal and may create noisy commits.
# Use only if you understand the implications (merge conflicts, many small commits).

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT" || exit 1

# Only run on a branch with a remote configured
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ -z "$BRANCH" ]; then
  echo "Not on a branch; aborting."
  exit 1
fi

# Stage all changes that are not ignored
git add -A

# If there is something to commit, create a timestamped commit and push
if ! git diff --cached --quiet; then
  git commit -m "auto-sync: auto commit $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  git push origin "$BRANCH"
else
  echo "No staged changes."
fi
