---
name: readme
description: Generate or update README.md from SDD artifacts (spec, plan, contracts, diagrams, research). Use when user asks to generate or update the README for an Akka SDK feature.
allowed-tools: Read, Write, mcp__akka_sdd__akka_sdd_list_specs, mcp__akka_sdd__akka_sdd_get_template
argument-hint: "[feature name or number]"
handoffs:
  - label: Review Implementation
    agent: akka:review
    prompt: Review the implementation against the spec
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Call `akka_sdd_list_specs` to find the target feature. Identify FEATURE_DIR and
   which SDD artifacts are available (AVAILABLE_DOCS). Check whether `README.md` exists at the
   repository root.

2. **Load SDD artifacts** (read what exists — skip missing files):
   - `FEATURE_DIR/spec.md` — service description, user stories
   - `FEATURE_DIR/plan.md` — components, tech stack, project structure, design decisions
   - `FEATURE_DIR/data-model.md` — entities and relationships
   - `FEATURE_DIR/contracts/http-api.md` — endpoints, request/response shapes, curl examples
   - `FEATURE_DIR/diagrams.md` — component graph, sequence diagram, state machine
   - `FEATURE_DIR/research.md` — key design decisions and rationale

3. **Detect UI**: Check plan.md and spec.md for any frontend, web UI, or static asset references.
   Set HAS_UI = true if found; false otherwise.

4. **Choose mode** based on whether README.md exists:

   ### Mode A — README does not exist
   Generate a full README from `akka_sdd_get_template` with `template_name="readme"`.
   Populate every section from the loaded SDD artifacts. Go to step 5.

   ### Mode B — README exists
   Perform a change analysis before writing anything:

   a. Read the existing `README.md`.

   b. For each SDD artifact loaded in step 2, identify what is **new or changed** compared
      to what is currently documented in the README. Build a change map:

      | SDD Artifact | Change Type | README Section Affected |
      |--------------|-------------|------------------------|
      | spec.md | new user story / changed description | Overview, Usage |
      | plan.md | new component / changed architecture | Architecture > Components |
      | data-model.md | new entity / changed fields | Architecture > Data Model |
      | contracts/http-api.md | new endpoint / changed contract | Usage > API Reference |
      | diagrams.md | updated diagrams | Architecture > Diagrams |
      | research.md | new decision | Architecture > Design Decisions |

   c. Present the change map to the developer and ask for confirmation:

      > The following README sections need updating based on SDD changes:
      > [list from change map]
      > Proceed with updates? (yes / no / select specific sections)

   d. Wait for confirmation. Update only the confirmed sections. Preserve all content
      in sections not listed in the change map.

5. **Populate / update sections** using these rules:

   ### Overview
   - Extract from spec.md: service name, primary capability, key components used.

   ### Quick Start
   - Use the standard Akka Maven commands (compile, exec:java).
   - Add the first curl example from contracts/http-api.md as the verify step.
   - If HAS_UI: add the UI start command after the service start command.

   ### Usage > API Reference
   - One subsection per endpoint group from contracts/http-api.md.
   - For each operation include: HTTP method + path, one-line description, curl command
     with example request body (if applicable), and example response.
   - If contracts/http-api.md does not exist: note "API contracts not yet generated —
     run `/akka.plan` to produce them."

   ### Usage > UI Usage
   - INCLUDE ONLY if HAS_UI is true. Remove the section entirely otherwise.
   - Extract screen names, paths, and key workflows from spec.md user stories and
     plan.md endpoint descriptions.

   ### Usage > Configuration
   - Extract env vars and `application.conf` keys from plan.md Technical Context.

   ### Architecture > Components
   - Build the component table from plan.md Component Details.
   - One row per class: name, Akka component type, one-line responsibility.

   ### Architecture > Data Model
   - Summarise entities from data-model.md (one bullet per entity).
   - If data-model.md does not exist: omit this subsection.

   ### Architecture > Diagrams
   - If diagrams.md exists: embed all three Mermaid blocks directly.
   - If diagrams.md does not exist: add a note "Run `/akka.diagram` to generate diagrams."

   ### Architecture > Design Decisions
   - Extract key decisions from research.md (decision → rationale, one row per decision).
   - If research.md does not exist: omit this subsection.

   ### Deployment
   - Use standard Akka CLI commands from plan.md service name.

   ### Development > Project Structure
   - Use the source tree from plan.md Project Structure section.

6. **Write output**: Save the updated or newly generated content to `README.md` at the
   repository root.

7. **Report**:
   - Mode used (generated / updated)
   - Sections written or updated
   - Sections skipped and why (missing artifact or no change detected)
   - Any placeholders that still need manual input

## Key Rules

- NEVER overwrite README sections that have no corresponding SDD change (Mode B)
- NEVER invent curl examples — derive all examples strictly from contracts/http-api.md
- NEVER include the UI Usage section if HAS_UI is false
- If a required SDD artifact is missing, note the gap in the report and leave the
  corresponding README section as a placeholder — do not fabricate content
- Use absolute paths when reading files