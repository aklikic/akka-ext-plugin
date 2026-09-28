---
name: spov
description: Generate a standardized POC/SPOV Scope of Work document for an Akka engagement. Reads project context (README, existing docs, background info) and produces a scope doc following the team's standard structure. Use when creating or updating a scope of work for a customer engagement.
allowed-tools: Read, Write, Glob, Grep, mcp__claude_ai_Google_Drive__create_file, mcp__claude_ai_Google_Drive__search_files, mcp__claude_ai_Google_Drive__update_file
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

3. **Goal discovery**: If the user has not already specified the goals, ask the Goal Discovery questions from the guide to determine the right emphasis across DevEx, OpsEx, and Scalability. Keep it conversational — don't dump all questions at once. Ask the most important 3-4 based on what you already know from the user input and project context.

4. **Determine mode**:

   ### Mode A — New scope doc (no existing scope file found)

   Generate a complete scope of work from the scaffold in the guide. Use the user input for customer name, use case, and any details provided. Ask the user to fill gaps where critical context is missing (e.g., customer pain points, target architecture).

   ### Mode B — Update existing scope doc
   Read the existing scope doc. Compare its structure against the guide's required sections. Report what's missing, what's misaligned, and propose updates. Wait for user confirmation before rewriting.

5. **Generate the scope doc**:
   - Follow the guide's required sections in order (1-10)
   - Include optional sections only when the user input or project context makes them relevant
   - Use Mermaid diagrams following the color conventions in the guide
   - Use the guide's scaffold as the starting structure
   - Ensure the POC is self-contained: every external dependency (including LLMs) must appear in the Mocked/Stubbed table
   - If the POC uses Agents and performance is a goal, include a mocked-LLM benchmark showing concurrent processing at realistic model latency

6. **Write output**: Save the scope doc to `SCOPE_OF_WORK.md` in the current working directory (or update the existing file).

7. **Offer Google Drive publish**: Ask the user if they want to publish to Google Drive. If yes:
   - Search Google Drive for an existing file with the same name to avoid duplicates
   - Create or update the file in Google Drive
   - Report the file URL

8. **Report**:
   - Path to generated/updated file
   - Which required sections are complete vs. need customer input
   - Which optional sections were included and why
   - Google Drive URL if published

## Key Rules

### Self-Containment
- The POC MUST run standalone — `mvn compile exec:java` and nothing else. No Docker compose, no external databases, no API keys for the basic demo
- ALWAYS include the Mocked/Stubbed table — every external dependency must appear, including LLM providers
- Every mock MUST have configurable latency and failure rate
- If the POC uses Agents, the Mocked/Stubbed table MUST include an LLM mock entry with realistic latency (~200-500ms)
- If performance/throughput is a goal and LLMs are involved, the scope MUST include a benchmark using mocked LLMs — you cannot benchmark against real LLMs with rate limits

### Goals
- Every scope doc MUST address all three pillars: DevEx, OpsEx, Scalability — the emphasis varies but none should be absent
- Use the Goal Discovery questions to determine weighting — don't guess, ask the user
- Goals must be tied to customer pain points, not generic Akka feature lists

### Structure & Content
- ALWAYS follow the section order and naming from the guide — consistency across all scope docs is the point
- NEVER invent customer details, pain points, or technical specifics — ask the user if context is missing
- NEVER include a Timeline section — this is explicitly excluded from the standard
- Diagrams MUST use the color conventions from the guide (blue=Akka transactional, purple=Akka AI, orange=external, green=human, teal=UI)
- Number flow lines in all architecture diagrams to show sequence
- Success Criteria must be observable and measurable — reject vague criteria like "system performs well"
- The "After the POC" section must be customer-specific — not generic Akka marketing
- If updating an existing doc (Mode B), preserve content that already follows the guide and only restructure/add what's missing
- Use absolute paths when reading files
