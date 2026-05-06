#!/usr/bin/env python3
"""Apply safe, manuscript-wide chapter improvements.

Improvements applied to every markdown file under manuscript/Chapters:
1. Frontmatter normalization:
   - Ensure `status` exists (default: Draft)
   - Ensure `updated` exists and is set to today's date
   - Replace placeholder `title: "TBD"` with inferred chapter title
2. Text hygiene:
   - Remove trailing whitespace
   - Collapse 3+ consecutive blank lines to 2
   - Ensure newline at end of file
"""

from __future__ import annotations

import datetime
import pathlib
import re


ROOT = pathlib.Path("manuscript/Chapters")
TODAY = datetime.date.today().isoformat()
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def infer_title_from_content_or_name(path: pathlib.Path, body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def normalize_frontmatter(path: pathlib.Path, text: str) -> str:
    match = FM_RE.match(text)
    if not match:
        return text

    fm_block = match.group(1)
    body = text[match.end() :]
    lines = fm_block.splitlines()

    parsed: list[tuple[str, str]] = []
    for raw in lines:
        if ":" in raw:
            k, v = raw.split(":", 1)
            parsed.append((k.strip(), v.strip()))

    keys_lower = {k.lower() for k, _ in parsed}

    if "status" not in keys_lower:
        parsed.append(("status", "Draft"))

    if "updated" in keys_lower:
        parsed = [
            (k, TODAY) if k.lower() == "updated" else (k, v)
            for k, v in parsed
        ]
    else:
        parsed.append(("updated", TODAY))

    title_inferred = infer_title_from_content_or_name(path, body)
    new_parsed: list[tuple[str, str]] = []
    for k, v in parsed:
        if k.lower() == "title" and v.strip('"').strip().lower() == "tbd":
            new_parsed.append((k, f'"{title_inferred}"'))
        else:
            new_parsed.append((k, v))

    new_fm = "\n".join(f"{k}: {v}" for k, v in new_parsed)
    return f"---\n{new_fm}\n---\n{body}"


def normalize_body_whitespace(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    if not text.endswith("\n"):
        text += "\n"
    return text


def main() -> None:
    changed = 0
    total = 0

    for path in sorted(ROOT.glob("*.md")):
        total += 1
        original = path.read_text(encoding="utf-8")
        updated = normalize_frontmatter(path, original)
        updated = normalize_body_whitespace(updated)

        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1

    print(f"Processed {total} chapter markdown files.")
    print(f"Updated {changed} files.")


if __name__ == "__main__":
    main()
