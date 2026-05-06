#!/usr/bin/env bash
# Create GitHub issues from a local HIGH_PRIORITY_ACTIONS.md file using `gh` CLI.
# Requires: GitHub CLI authenticated (`gh auth login`) and repository initialized.

REPO="$(git rev-parse --show-toplevel 2>/dev/null | xargs basename)"
if [ -z "$REPO" ]; then
  echo "Cannot determine repository root. Run from inside a git repo." >&2
  exit 1
fi

FILE="docs/HIGH_PRIORITY_ACTIONS.md"
if [ ! -f "$FILE" ]; then
  echo "$FILE not found" >&2
  exit 1
fi

# Parse the file for numbered items
awk '/^[0-9]+\. /{print substr($0, index($0,$2))}' "$FILE" | nl -w1 -s": " | while IFS= read -r line; do
  # Each line looks like: 1: IRB / Ethical approvals
  num=$(echo "$line" | cut -d: -f1)
  title=$(echo "$line" | cut -d: -f2- | sed 's/^ *//')
  body="Auto-created issue from docs/HIGH_PRIORITY_ACTIONS.md (item #$num)\n\nSee file: $FILE"
  echo "Creating issue: $title"
  gh issue create --title "$title" --body "$body" || echo "Failed to create issue for: $title"
done
