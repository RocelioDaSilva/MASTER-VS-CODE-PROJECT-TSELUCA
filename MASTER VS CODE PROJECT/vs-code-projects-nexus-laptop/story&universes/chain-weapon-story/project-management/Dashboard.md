# Vault Dashboard

This dashboard includes quick Dataview queries for chapters and open tasks. Install the `Dataview` plugin to use these.

## Draft chapters
```dataview
table file.link as "Note", status, word_goal
from "Chapters"
where status = "draft"
sort file.name asc
```

## Open tasks (from Chapters)
```dataview
task from "Chapters"
where !completed
```

## Notes
- Enable `Dataview` in Community Plugins.
- If queries return nothing, confirm frontmatter keys (e.g., `status`, `word_goal`).
