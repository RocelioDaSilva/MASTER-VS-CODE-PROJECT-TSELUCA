---
title: Markdown Utilities & Formatting Examples
date: April 9, 2026
purpose: Store markdown formatting guides and utility files
---

# Markdown Directory

This folder stores markdown formatting utilities, style guides, and example formatting for consistent documentation across the project.

## Purpose

- **Markdown templates** (consistent formatting templates)
- **Formatting examples** (how to format specific content types)
- **Style guides** (markdown conventions for this project)
- **Utility scripts** (markdown processing utilities if needed)
- **Checklists** (markdown checklist templates)

## Content Organization

```
markdown/
├── FORMATTING-GUIDE.md              [Markdown style conventions]
├── CHARACTER-PROFILE-TEMPLATE.md    [Character profile formatting]
├── SCENE-TEMPLATE.md                [Scene formatting template]
├── CHAPTER-TEMPLATE.md              [Chapter formatting template]
└── [Other utility files]            [Additional templates as needed]
```

## Markdown Conventions in This Project

**Headings:**
- Use `#` for document titles
- Use `##` for major sections
- Use `###` for subsections
- Use `####` for details

**Lists:**
- Use `-` for unordered lists
- Use `1.` for ordered lists
- Use `- [ ]` for task lists

**Emphasis:**
- Use `**text**` for bold
- Use `*text*` for italics
- Use `~~text~~` for strikethrough (rarely)

**Code:**
- Use backticks for inline code: `code`
- Use triple backticks for code blocks

**Links:**
- Use `[Display Text](relative/path.md)` for internal links
- Use `[Display Text](https://example.com)` for external links
- Use `→` symbol for "see also" navigation

**Frontmatter:**
- Use YAML frontmatter at top of files (in our project)
- Include: title, date, purpose, status fields

## Templates Available

Templates are available for:
- Character profiles
- Scene descriptions
- Chapter organization
- Documentation pages
- Analysis documents
- Planning documents

## How to Use

1. Copy appropriate template
2. Fill in your content
3. Follow formatting conventions above
4. Save with appropriate naming convention
5. Cross-reference from relevant hubs

## Style Examples

**Link formatting:**
```
→ [Character Master Index](../characters/CHARACTER-MASTER-INDEX.md)
→ [Story Hub](../story/INDEX.md)
```

**Code block example:**
```markdown
---
title: Document Title
date: YYYY-MM-DD
purpose: Why this document exists
---
```

**List example:**
```markdown
- Item 1
- Item 2
  - Nested item
  - Another nested
- Item 3
```

## Related Documentation

→ [CONTRIBUTING.md](../CONTRIBUTING.md) — File standards & workflow  
→ [README.md](../README.md) — Project hub  
→ [Templates/](../Templates/) — Story templates (Chapter, Scene, Character)
