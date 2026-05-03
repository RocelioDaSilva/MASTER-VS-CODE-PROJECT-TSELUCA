# Prompt Templates for Copilot Pro Models

This file contains ready-to-use prompt templates for common research writing tasks, mapped to the best model for each phase.

---

## GPT-4.1 — Workhorse (drafting & brainstorming)

- Purpose: Fast, reliable drafting and brainstorming.
- System cue: You are an academic writing assistant. Produce clear, structured, and cite-ready prose.
- User template: Produce a [section: outline|introduction|methods|results|discussion] on [topic]. Deliver: (1) 3 key points, (2) one concise paragraph (150–250 words), (3) 2 suggested citations (author, year) with one-sentence rationale.
- Example: Produce an Introduction about distributed solar LCOE variability — 3 key points, 180-word paragraph, 2 suggested citations with reasons.
- Tips: Ask for "3 variants" to explore tone/length; use iteratively for drafts.

---

## Claude Sonnet 4 / 4.5 — Deep analysis & restructuring

- Purpose: Condense, restructure, and improve argument logic.
- System cue: Act as a senior editor: improve logic, clarity, and concision while preserving original claims.
- User template: Edit the text below for clarity and academic tone; shorten by ~30%; restructure for logical flow. Mark any unsupported claims needing citations. Text: [paste text].
- Example: Edit this 600-word Theory section, return edited version + list of flagged claims.
- Tips: Request a two-column diff (original → edited) and a short changelog.

---

## Claude Opus 4 / 4.5 / 4.6 — Final polishing & critique

- Purpose: Sophisticated rewrite and reviewer-style critique.
- System cue: Act as a meticulous peer reviewer and copy editor for top journals.
- User template: Perform a final edit: (1) edited text, (2) 5 reviewer-style summary points, (3) 3 suggested counterarguments to address. Text: [paste]. Constraints: tone=academic, length=as original ±10%.
- Example: Finalize Abstract + Methods; return edited text, 5 reviewer comments, and counterarguments.
- Tips: Use at near-submission stage; ask for "track changes" style output.

---

## GPT-5 Series (e.g., GPT-5.2-Codex) — Complex problem solving & code

- Purpose: Advanced reasoning, long-context code handling, reproducible analysis.
- System cue: You are an expert researcher and computational scientist; validate code and explain outputs concisely.
- User template: Given [code/text/files], perform [task: unify methods|check equations|refactor code], provide corrected code, tests, and a step-by-step rationale. Attach files or paste snippets.
- Example: Refactor Python analysis snippet for reproducibility; include unit-test suggestions and a short explanation.
- Tips: Provide the smallest runnable snippet and desired behavior; request unit tests to validate changes.

---

## Gemini 2.5 Pro / 2.0 Flash — Multimodal summarization & visuals

- Purpose: Interpret figures/images and summarize visual data for captions/insights.
- System cue: Summarize visual/data artifacts and produce concise manuscript-ready takeaways.
- User template: Analyze this figure/data: [attach image or data]. Provide: (1) one-sentence caption, (2) 3 bullet takeaways, (3) any axis/legend clarifications.
- Example: Figure: scatterplot capacity vs LCOE — produce caption and 3 insights.
- Tips: Attach high-quality images; specify whether you want trend, outlier, or stat-test focus.

---

## GPT-5.4 — Massive-context manuscript work

- Purpose: Whole-manuscript synthesis and cross-file consistency checks.
- System cue: You can access the full manuscript and supplementary notes; synthesize and align structure, references, and claims.
- User template: Review full manuscript/files: [list or paste]. Produce: (a) unified 150-word abstract, (b) checklist of inconsistent claims vs citations, (c) suggested reorganization of sections.
- Example: Given 8 sections + 20 notes, produce abstract and 10-item inconsistency report.
- Tips: Provide a manifest/TOC; use when you need single-pass consistency across many files.

---

## Auto (Model Selection) — Convenience mode

- Purpose: Let system pick best model for general tasks.
- System cue: Automatically select the model best-suited for the request prioritizing quality then speed.
- User template: Auto: [task]. Constraints: {speed: high|medium|low, max_tokens: N, preserve_style: yes/no}.
- Example: Auto: edit 400-word Methods for clarity; prefer speed=medium, preserve_style=yes.
- Tips: Use for convenience; saves premium requests when not required.

---

## General Prompt Structure (reusable across models)

- Purpose: Keep prompts predictable and actionable.
- Structure: (1) Role/system cue. (2) Task with explicit deliverables. (3) Context (paste/attach). (4) Constraints (length, tone, citations). (5) Acceptance criteria / examples.
- Template: Role: [one line]. Task: [what to produce]. Context: [text/files]. Constraints: [length, style, citations]. Output: [exact deliverables].
- Tips: Always ask for variants and acceptance criteria to reduce iteration.

---

If you'd like a shorter one-line prompt per model or a different file location, tell me and I will revise.
