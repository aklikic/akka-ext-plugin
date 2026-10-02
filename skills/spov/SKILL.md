---
name: spov
description: Generate a standardized POC/SPOV Scope of Work document for an Akka engagement. Reads project context (README, existing docs, background info) and produces a scope doc following the team's standard structure. Use when creating or updating a scope of work for a customer engagement.
allowed-tools: Read, Write, Glob, Grep, mcp__claude_ai_Google_Drive__create_file, mcp__claude_ai_Google_Drive__search_files, mcp__claude_ai_Google_Drive__update_file, mcp__claude_ai_Google_Drive__read_file_content
argument-hint: "[customer name and use case, e.g. 'Rossmann warehouse management modernization']"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Load the guide**: Read `skills/spov/scope-of-work-guide.md` from the plugin directory. This defines the required sections, optional sections, conventions, and scaffold.

2. **Gather context**: Look for existing project context in the current working directory:
   - `README.md` — project overview
   - `SCOPE_OF_WORK.md`, `poc-scope.md`, or any `*scope*.md` — existing scope doc to update
   - `docs/` — any background documents
   - `specs/` or `.akka/specs/` — SDD artifacts if they exist
   - Any Mermaid diagrams or architecture docs

3. **Goal discovery**: If the user has not already specified the goals, ask the Goal Discovery questions from the guide. Keep it conversational — don't dump all questions at once. Ask the most important 3-4 based on what you already know from the user input and project context. Always ask:
   - Does the customer want a UI/dashboard? (If yes, the UI must be minimalistic — a thin layer that maps 1:1 to the service's HTTP endpoints. No invented features.)
   - Is the customer evaluating Akka against alternatives? (If yes, include platform comparison notes in each goal)
   - Does the customer have infosec/compliance requirements that affect where the POC runs?

4. **Determine mode**:

   ### Mode A — New scope doc (no existing scope file found)

   Generate a complete scope of work from the scaffold in the guide. Use the user input for customer name, use case, and any details provided. Ask the user to fill gaps where critical context is missing (e.g., customer pain points, target architecture).

   ### Mode B — Update existing scope doc
   Read the existing scope doc. Compare its structure against the guide's required sections. Report what's missing, what's misaligned, and propose updates. Wait for user confirmation before rewriting.

5. **Generate the scope doc**:
   - Follow the guide's required sections in order (1-13)
   - Start in DRAFT stage — set header status to DRAFT
   - Include optional sections only when the user input or project context makes them relevant
   - Use Mermaid diagrams following the color conventions in the guide
   - Use the guide's scaffold as the starting structure
   - Ensure the POC is self-contained: every external dependency (including LLMs) must appear in the Mocked/Stubbed table
   - If the POC uses Agents and performance is a goal, include a mocked-LLM benchmark showing concurrent processing at realistic model latency

6. **Write output**: Save the scope doc to `SCOPE_OF_WORK.md` in the current working directory (or update the existing file).

7. **Offer Google Drive export**: Ask the user if they want to export to Google Drive as a branded document. If yes, use the `gdoc-restyle` pipeline from the presentations repo:

   a. **Convert markdown to blocks + render diagrams**: Run:
      ```
      python3 skills/spov/md_to_blocks.py <SCOPE_OF_WORK.md> <blocks.json> --img-dir <diagrams-dir>
      ```
      This parses the markdown into blocks, extracts Mermaid code blocks, and renders them to PNG via `mmdc`. Outputs `blocks.json` + diagram PNGs.

   b. **Build styled DOCX**: Run:
      ```
      python3 skills/spov/build_spov_docx.py <blocks.json> <out.docx> --title "<Customer — Description>" --meta "Akka · <Month Year>"
      ```
      This produces a DOCX with cover page (brand bar, teal eyebrow, gold title), styled headings, tables with gold-rule headers, embedded Mermaid diagrams, callout boxes, and page footer. Outputs `<out.docx>` and `<out.docx>.b64`.

   c. **Upload or deliver**: Check the size of `<out.docx>.b64`. If under 23,000 characters, upload via MCP `mcp__claude_ai_Google_Drive__create_file` with `base64Content` from the `.b64` file and `contentMimeType: application/vnd.openxmlformats-officedocument.wordprocessingml.document` — Google Drive auto-converts to a Google Doc with formatting preserved. Use the title format `{Customer} — {One-line description}` (e.g., `Paysafe — Consumer Risk Audit Response Agent`).

      If the upload fails (conversion error, connector size limits, or any other error), save the DOCX locally and inform the user of the local file path. The local filename must match the title format: `{Customer} — {One-line description}.docx` (e.g., `Paysafe — Consumer Risk Audit Response Agent.docx`). Do NOT attempt to upload as a raw DOCX with `disableConversionToGoogleType` — an unconverted DOCX in Google Drive is not useful. The user can manually upload the DOCX to Google Drive, which will auto-convert it to a Google Doc with all formatting preserved.

   d. **Report the DOCX path** (and Google Drive URL if uploaded) to the user.

8. **Offer kickoff presentation export**: Ask the user if they want a presentation version for the kickoff meeting. If yes, generate a self-contained HTML slide deck:

   a. **Structure**: 4 slides condensing the scope doc:
      - **Slide 1: Assumptions & Open Questions** — key assumptions as numbered list, open questions in yellow mono. This is the starting point for the kickoff conversation — validate before proceeding.
      - **Slide 2: Proposed Solution** — eyebrow label, title, Mermaid solution overview diagram (from Section 3), key design decision bullets
      - **Slide 3: Goals & Expected Benefits** — goals as card grid (2 columns), each card has: tag (G1, G2...), title, key bullets. Expected benefits table below.
      - **Slide 4: Next Steps & Timeline** — timeline milestones table, next steps (deploy BYOC + connect real systems)

   b. **Design system** (from TylerJewell/presentations):
      - Dark theme: `--black: #000`, `--dark: #07070C`, `--card: #131316`, `--line: #222`
      - Text: `--white: #fff`, `--muted: #9a9a9a`, `--dim: #6c6c6c`
      - Accent: `--yellow: #F5C518`
      - Component colors: `--blue: #1a73e8`, `--purple: #7c4dff`, `--orange: #ff8f00`, `--green: #28C840`, `--red: #E74C3C`
      - Fonts: Instrument Sans (body/headings), JetBrains Mono (labels/eyebrows/tags)
      - Slides: full viewport height, vertically centered, scroll-snap
      - Eyebrow: mono 11px uppercase with yellow dash prefix
      - Cards: `--card` background, `--line` border, 12px radius
      - Phase card active: yellow border; future: muted styling
      - Mermaid: dark theme with matching color variables
      - Slide counter: fixed bottom-right, mono 11px

   c. **Content rules**:
      - Extract directly from the scope doc — do not invent content
      - Goals should show concise bullets (bold key point + muted detail), not full paragraphs
      - Open questions from the scope doc appear as yellow mono text at bottom of relevant goal cards
      - Mermaid diagrams use the same diagram from the scope doc's Proposed Solution section

   d. **Write output**: Save to `presentation.html` in the current working directory.

9. **Report**:
   - Path to generated/updated scope doc
   - Which required sections are complete vs. need customer input
   - Which optional sections were included and why
   - Google Drive URL or local DOCX path if exported
   - Path to presentation.html if generated

## Recommendations

The following are recommendations, not strict rules. After generating the scope doc, present these as a checklist for the user to review and approve before finalizing. The user has final say on all of these.

### Self-Containment (recommend)
- POC should run standalone with a single command. No Docker compose, no external databases, no API keys for the basic demo
- Include a Mocked/Stubbed table — every external dependency should appear, including LLM providers
- Mocks should have configurable latency and failure rate
- If the POC uses Agents, recommend including an LLM mock entry with realistic latency (~200-500ms)
- If performance/throughput is a goal and LLMs are involved, recommend a benchmark using mocked LLMs

### Goals (recommend)
- Goals should emerge from the Goal Discovery conversation and the customer's specific pain points — don't force goals into predefined pillars
- DevEx, OpsEx, and Scalability are common themes (see the guide) but are guidelines, not mandatory sections — include what's relevant, omit what isn't
- Use the Goal Discovery questions to understand what matters — don't guess, ask the user
- Goals should be tied to customer pain points, not generic Akka feature lists

### Expected Benefits (recommend)
- Expected Benefits maps pain points to what **Akka as a platform** delivers — NOT what the use case solves
- The customer already knows the value of their use case; show them what the platform brings
- Do not repeat pain points in the Background section — they belong here

### Structure & Content (recommend)
- Follow the section order and naming from the guide — consistency across scope docs is the goal
- Don't invent customer details, pain points, or technical specifics — ask the user if context is missing
- Background covers Current State only — no Pain Points subsection
- Timeline section uses TBD milestones in DRAFT/PROPOSAL — no duration estimates until scope is agreed
- Next Steps should be simple (deploy BYOC + connect real systems) — don't add sales items
- Never name specific competitors — use "alternative frameworks" or "alternative approaches"
- No CLI commands in customer-facing text — use outcome-oriented language
- Diagrams should use the color conventions from the guide (blue=Akka transactional, purple=Akka AI, orange=external, green=human, teal=UI)
- Number flow lines in architecture diagrams to show sequence
- Success Criteria should be observable and measurable — flag vague criteria like "system performs well" for user review
- If updating an existing doc (Mode B), preserve content that already follows the guide and only restructure/add what's missing

### Human Gate
After generating the scope doc, present a summary of recommendations applied and any deviations from the guide. Wait for user confirmation before considering the doc final. Use absolute paths when reading files.
