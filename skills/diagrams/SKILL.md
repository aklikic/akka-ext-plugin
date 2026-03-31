---
name: diagrams
description: Generate Mermaid diagrams (component dependencies, sequence, workflow state machine) for a feature plan. Use when user asks to generate or update diagrams for an Akka SDK feature.
allowed-tools: Read, Write, mcp__akka_sdd__akka_sdd_list_specs, mcp__akka_sdd__akka_sdd_get_template
argument-hint: "[feature name or number]"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Call `akka_sdd_list_specs` to find the target feature. Identify FEATURE_DIR and confirm `plan.md` exists. Call `akka_sdd_get_template` with `template_name="diagrams"` to load the diagram template.

2. **Load context**: Read `FEATURE_DIR/plan.md` and `FEATURE_DIR/spec.md` to extract:
   - All components (Workflows, Agents, Views, Endpoints, Consumers, Entities)
   - Their dependencies and call relationships
   - Workflow states and transitions (if a Workflow is present)
   - External systems and actors
   - Topic names (if `@Produce.ToTopic` / `@Consume.FromTopic` is used)

3. **Generate diagrams** using the template conventions (color, external nodes, topic nodes, sequence numbers):
   - **Diagram 1 — Component Dependencies**: flowchart of all components grouped by layer
   - **Diagram 2 — Sequence Diagram**: end-to-end flows (happy path + error path at minimum; add HITL path if applicable)
   - **Diagram 3 — Workflow State Machines**: ONLY if the feature uses Akka Workflows; omit entirely otherwise.
     Produce **one numbered subsection per Workflow class** (3.1, 3.2, …), each with its own Mermaid flowchart.
     Title each subsection with the workflow class name (e.g., `### 3.1 OrderWorkflow`).

4. **Write output**: Save diagrams to `FEATURE_DIR/diagrams.md` using the diagrams template structure.

5. **Report**: Output path to generated `diagrams.md` and list which diagrams were generated.

## Key Rules

- Use absolute paths
- NEVER invent flow categories to justify using a color — use only colors present in the actual feature flows
- NEVER use `-.>>` in sequence diagrams (invalid Mermaid syntax) — use `-->>` for dotted arrows
- NEVER collapse a topic into an arrow label — always represent it as an explicit cylinder node
- Diagram 3 (state machines) MUST be omitted entirely if no Akka Workflow is used
- There MUST be exactly one state machine subsection per Workflow class — never merge multiple workflows into one diagram
- If `plan.md` does not yet have enough component detail to generate accurate diagrams, report what is missing and stop