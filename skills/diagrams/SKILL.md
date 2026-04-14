---
name: diagrams
description: Generate Mermaid diagrams for an Akka SDK feature. Works with spec.md (requirement-level visualizations) or plan.md (technical component diagrams). Use when user asks to generate or update diagrams for an Akka SDK feature.
allowed-tools: Read, Write, mcp__akka_sdd__akka_sdd_list_specs, mcp__akka_sdd__akka_sdd_get_template
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Call `akka_sdd_list_specs` to find the target feature. Identify FEATURE_DIR. Check which artifacts exist: `plan.md`, `spec.md`, or both.

2. **Select mode(s)** — spec and plan diagrams are independent artifacts; generate whichever apply:
   - If `spec.md` exists → run **Requirements mode** (non-technical requirement visualizations). Call `akka_sdd_get_template` with `template_name="spec-diagrams"`. If that template is not found, read `skills/diagrams/spec-diagrams.template.md` from the plugin directory instead.
   - If `plan.md` exists → run **Technical mode** (component diagrams from the plan). Call `akka_sdd_get_template` with `template_name="diagrams"`.
   - If both exist → run **both modes**, producing two separate files.
   - If neither exists → report what is missing and stop.

---

### Requirements Mode (spec.md)

3. **Load context**: Read `FEATURE_DIR/spec.md` to extract:
   - All user stories with their priorities, titles, and dependency relationships
   - Actors and their goals (who interacts with the system and what they do)
   - Key entities and their relationships (if defined)
   - Status lifecycle or state progression (if defined)
   - Edge cases and assumptions

4. **Generate requirement diagrams** using the spec-diagrams template conventions:
   - **Diagram 1 — User Journey Map**: flowchart of all user stories arranged by priority, showing dependency relationships between stories. Color by priority tier.
   - **Diagram 2 — Actor–Goal Overview**: flowchart showing actors, the system, and external systems. Connect actors to their goals derived from user stories. This is a use-case-level view.
   - **Diagram 3 — Entity Relationship Map**: ONLY if the spec defines Key Entities; omit entirely otherwise. Show entities and their conceptual relationships (no database details).
   - **Diagram 4 — Status Lifecycle**: ONLY if the spec describes a status lifecycle or state progression; omit entirely otherwise. Show statuses and transitions with triggers.

5. **Write output**: Save diagrams to `FEATURE_DIR/spec-diagrams.md` using the spec-diagrams template structure.

6. **Report**: Output path to generated `spec-diagrams.md` and list which diagrams were generated.

---

### Technical Mode (plan.md)

3. **Load context**: Read `FEATURE_DIR/plan.md` and `FEATURE_DIR/spec.md` to extract:
   - All components (Workflows, Agents, Views, Endpoints, Consumers, Entities)
   - Their dependencies and call relationships
   - Workflow states and transitions (if a Workflow is present)
   - External systems and actors
   - Topic names (if `@Produce.ToTopic` / `@Consume.FromTopic` is used)

4. **Generate diagrams** using the diagrams template conventions (color, external nodes, topic nodes, sequence numbers):
   - **Diagram 1 — Component Dependencies**: flowchart of all components grouped by layer
   - **Diagram 2 — Sequence Diagram**: end-to-end flows (happy path + error path at minimum; add HITL path if applicable)
   - **Diagram 3 — Workflow State Machines**: ONLY if the feature uses Akka Workflows; omit entirely otherwise.
     Produce **one numbered subsection per Workflow class** (3.1, 3.2, …), each with its own Mermaid flowchart.
     Title each subsection with the workflow class name (e.g., `### 3.1 OrderWorkflow`).

5. **Write output**: Save diagrams to `FEATURE_DIR/plan-diagrams.md` using the diagrams template structure.

6. **Report**: Output path to generated `plan-diagrams.md` and list which diagrams were generated.

---

## Key Rules

### General
- Use absolute paths
- NEVER invent categories to justify using a color — use only colors present in the actual feature

### Requirements Mode
- Diagrams MUST be non-technical — no implementation details, no class names, no API paths
- Use language from the spec (user story titles, entity names, status names) — do not rename or translate
- Diagram 3 (entity relationships) MUST be omitted entirely if no Key Entities section exists in the spec
- Diagram 4 (status lifecycle) MUST be omitted entirely if the spec does not describe a status lifecycle
- If `spec.md` does not yet have enough detail to generate accurate diagrams, report what is missing and stop

### Technical Mode
- NEVER use `-.>>` in sequence diagrams (invalid Mermaid syntax) — use `-->>` for dotted arrows
- NEVER collapse a topic into an arrow label — always represent it as an explicit cylinder node
- Diagram 3 (state machines) MUST be omitted entirely if no Akka Workflow is used
- There MUST be exactly one state machine subsection per Workflow class — never merge multiple workflows into one diagram
- If `plan.md` does not yet have enough component detail to generate accurate diagrams, report what is missing and stop