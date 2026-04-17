---
name: pitch
description: Generate a self-contained HTML pitch page showcasing the Akka SDD workflow for a specific use case. Reads spec.md, plan.md, and tasks.md to populate a 5-step walkthrough (Specify, Clarify, Plan, Tasks, Implement). Use when user wants to create a visual pitch or demo page for a feature.
allowed-tools: Read, Write, mcp__akka_sdd__akka_sdd_list_specs
argument-hint: "[feature name or number]"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Call `akka_sdd_list_specs` to find the target feature. Identify FEATURE_DIR and
   which SDD artifacts are available. Read the HTML template from `skills/pitch/pitch.template.html`
   in the plugin directory.

2. **Load SDD artifacts** (read what exists — skip missing files):
   - `FEATURE_DIR/spec.md` — service description, user stories, acceptance scenarios
   - `FEATURE_DIR/spec-diagrams.md` — requirement-level Mermaid diagrams
   - `FEATURE_DIR/plan.md` — component design, architecture decisions
   - `FEATURE_DIR/plan-diagrams.md` — technical Mermaid diagrams
   - `FEATURE_DIR/tasks.md` — dependency-ordered task list
   - `FEATURE_DIR/research.md` — key design decisions (optional)

3. **Extract content** for each of the five pitch sections:

   ### Section 1 — Specify (from spec.md + spec-diagrams.md)
   - **Input card**: The original feature description / one-liner from the spec overview
   - **Output card**: One representative user story with 2-3 acceptance scenarios (pick the most
     illustrative one — ideally showing Given/When/Then format)
   - **Diagram tabs**: Include up to 3 diagrams from spec-diagrams.md. Pick the most visually
     compelling ones. Common choices: User Journey, Actor-Goal, Status Lifecycle.
     Use the raw Mermaid code from the source — do NOT modify diagram content or styling.

   ### Section 2 — Clarify (from spec.md)
   - Extract 2-4 clarification Q&A pairs. Look for:
     - Assumptions or decisions noted in the spec
     - Edge cases and how they are handled
     - Non-obvious design choices
   - If the spec does not contain explicit Q&A, synthesize questions from the spec's
     assumptions/decisions sections — phrase them as "Q: [question about ambiguity]" /
     "A: [how the spec resolved it]"

   ### Section 3 — Plan (from plan.md + plan-diagrams.md)
   - **Output card**: Component design excerpt — list 3-5 key components with their Akka type
     (Workflow, Agent, View, Entity, Endpoint) and one-line responsibility
   - **Diagram tabs**: Include up to 2 diagrams from plan-diagrams.md. Common choices:
     Component Graph, Workflow States.
     Use the raw Mermaid code from the source — do NOT modify diagram content or styling.

   ### Section 4 — Tasks (from tasks.md)
   - Extract 5-8 representative tasks spanning different phases. Include:
     - Task ID (e.g., T004)
     - Tags where present (Parallel, US reference)
     - Task description with file path
   - Show a mix: some domain tasks, some application-layer tasks, some test tasks

   ### Section 5 — Implement (from plan.md + spec.md)
   - **Code card**: Generate a representative code snippet for the most interesting component.
     Prefer Agents or Workflows over simple endpoints. Use syntax-highlighted `<span>` elements
     matching the template's CSS classes: `.kw` (keyword/annotation), `.str` (string),
     `.cmt` (comment), `.type` (type name), `.num` (number), `.fn` (function name), `.ok` (success)
   - **Build loop card**: Show a realistic incremental build progression with 3-4 phases,
     each with compile/test results and approval gates

4. **Populate the HTML template**:
   - Replace `PITCH_TITLE` with a short, punchy title derived from the feature name
   - Replace `PITCH_SUBTITLE` with the feature's one-line description
   - Replace `PITCH_BADGE` with "Akka SDD Workflow" (default) or user-provided badge text
   - Fill each section's cards, diagrams, and content blocks
   - Set the `<title>` element to match the pitch title

5. **Write output**: Save the generated HTML to `FEATURE_DIR/pitch.html`

6. **Report**:
   - Path to generated file
   - Which SDD artifacts were used
   - Which sections have full content vs. placeholder content due to missing artifacts
   - Suggest opening the file in a browser to preview

## Key Rules

- The output MUST be a single self-contained HTML file — no external dependencies except
  the Mermaid CDN and Google Fonts (already in the template)
- NEVER modify Mermaid diagram code from the source files — copy it exactly as-is including
  all `style` and `linkStyle` directives
- NEVER invent acceptance scenarios, component names, or task IDs — derive all content
  strictly from the SDD artifacts
- If an SDD artifact is missing, include placeholder content in that section with a note
  like "Run /specify to generate this content" — do NOT leave the section empty
- Code snippets in the Implement section should be realistic but concise (15-30 lines).
  Use the component names and types from plan.md
- Apply syntax highlighting using the template's CSS classes (`kw`, `str`, `cmt`, `type`,
  `num`, `fn`, `ok`) — do NOT use `<code>` blocks or markdown formatting
- Preserve all CSS, JavaScript, and structural HTML from the template exactly — only
  replace content within the designated placeholder areas
- Use absolute paths when reading files