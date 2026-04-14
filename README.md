# akka-ext — Claude Code Plugin

An extension plugin for Akka SDK projects, exposing the `diagrams` and `readme` skills as plugin skills backed by the real SDD workflow.

## Prerequisites

Requires the `akka-sdd` MCP server to be available (provides `akka_sdd_list_specs` and `akka_sdd_get_template`).

## Usage

```bash
# Load locally
claude --plugin-dir /path/to/akka-ext

# Generate diagrams for a feature
/akka-ext:diagrams

# Generate or update README from SDD artifacts
/akka-ext:readme
```

## Skills

### `diagrams`

Generates Mermaid diagrams for an Akka SDK feature. Automatically selects the mode based on available artifacts:

**Requirements mode** (spec.md only, no plan.md):
1. **User Journey Map** — user stories arranged by priority with dependency relationships
2. **Actor–Goal Overview** — actors, their goals, and external systems (use-case level)
3. **Entity Relationship Map** — key entities and conceptual relationships (if defined in spec)
4. **Status Lifecycle** — state progression with triggers (if defined in spec)

**Technical mode** (plan.md exists):
1. **Component Dependencies** — flowchart of all components grouped by layer (Endpoint, Workflow, Agent, View, Entity, Consumer)
2. **Sequence Diagram** — end-to-end flows (happy path, error path, HITL if applicable)
3. **Workflow State Machines** — one per Workflow class (omitted if no Workflow is used)

Saves output to `FEATURE_DIR/diagrams.md`.

### `readme`

Generates or updates `README.md` at the repository root from SDD artifacts:

- **Mode A** (no README): generates from the `readme` template
- **Mode B** (README exists): performs a change analysis against SDD artifacts, presents a change map, and updates only confirmed sections

## Structure

```
skills/
├── diagrams/
│   ├── SKILL.md                    ← mirrors akka.diagram command
│   ├── plan-diagrams.template.md    ← technical diagrams template (plan.md mode)
│   └── spec-diagrams.template.md   ← requirements diagrams template (spec.md mode)
└── readme/
    ├── SKILL.md               ← mirrors akka.readme command
    └── readme.template.md     ← akka README template
```