# [Service Name]

> [One sentence: what the service does and the problem it solves.]

---

## Overview

[2–3 sentences expanding the tagline. Mention the primary user-facing capability,
the key Akka components used (e.g., Workflow, Agent, View), and any notable
integration points (e.g., external APIs, message broker).]

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Java | 21+ |
| Maven | 3.9+ |
| Akka CLI | latest |
| Docker | 24+ (for local runtime) |

Install the Akka CLI: [Install Akka CLI](https://doc.akka.io/reference/cli/index.html)

---

## Quick Start

```bash
# 1. Build
mvn compile

# 2. Run locally
mvn compile exec:java

# 3. Verify
curl http://localhost:9000/[health-or-first-endpoint]
```

---

## Usage

### API Reference

<!--
  One subsection per endpoint group. For each operation include:
  - HTTP method + path
  - Short description
  - Request body (if any) as a JSON block
  - curl example
  - Example response
  SKIP this section entirely if the service exposes no HTTP endpoints.
-->

#### [Resource / Operation Group]

**[Verb] `[METHOD] /path`**

[One-line description of what this operation does.]

```bash
curl -X [METHOD] http://localhost:9000/[path] \
  -H "Content-Type: application/json" \
  -d '{
    "[field]": "[value]"
  }'
```

Response:

```json
{
  "[field]": "[value]"
}
```

---

<!--
  Repeat the block above for each endpoint group.
-->

### UI Usage

<!--
  INCLUDE ONLY if the service has a web or desktop UI.
  Remove this section entirely if there is no UI.
-->

#### Starting the UI

```bash
# [Command to start the UI, e.g. npm run dev or open index.html]
```

Open [http://localhost:[port]](http://localhost:[port]) in your browser.

#### Key Screens

| Screen | Path | Description |
|--------|------|-------------|
| [Screen name] | `/[path]` | [What the user does here] |

#### Walkthrough

1. **[Step 1]** — [What the user does and what happens]
2. **[Step 2]** — [What the user does and what happens]
3. **[Step 3]** — [What the user does and what happens]

---

### Configuration

| Key | Default | Description |
|-----|---------|-------------|
| `[akka.javasdk.*]` | `[default]` | [What it controls] |
| `[ENV_VAR]` | `[default]` | [What it controls] |

---

## Architecture

### Components

| Component | Type | Responsibility |
|-----------|------|----------------|
| `[ClassName]` | Workflow / Agent / View / Endpoint / Consumer / Entity | [What it does] |

### Data Model

<!--
  Summarise key entities from data-model.md.
  One bullet per entity: name → fields → lifecycle.
-->

- **[Entity]** — [key fields] — [state transitions or lifecycle notes]

### Diagrams

<!--
  Embed or link to diagrams.md.
  If diagrams.md exists, copy the three mermaid blocks here
  (Component Dependencies, Sequence Diagram, Workflow State Machine).
  If diagrams.md does not exist, link to the plan instead.
-->

See [`specs/[###-feature]/diagrams.md`](specs/[###-feature]/diagrams.md) for:
- Component dependency graph
- End-to-end sequence diagram
- Workflow state machine *(if applicable)*

### Design Decisions

<!--
  Summarise the key architectural choices from research.md.
  Format: Decision → Rationale (one line each).
-->

| Decision | Rationale |
|----------|-----------|
| [e.g., Workflow step for delivery] | [e.g., synchronous confirmation required] |
| [e.g., Event Sourced Entity for X] | [e.g., audit trail needed] |

---

## Deployment

### Build & Push Image

```bash
mvn clean install -DskipTests
```

### Deploy to Akka Cloud

```bash
akka service deploy [service-name] [service-name]:[tag] --push
```

Monitor the service:

```bash
akka service list
akka service logs [service-name]
```

See [Deploy and manage services](https://doc.akka.io/operations/services/deploy-service.html)
for environment variables, scaling, and secrets.

---

## Development

### Running Tests

```bash
# Unit + integration tests
mvn test

# Single test class
mvn test -Dtest=[TestClassName]
```

### Project Structure

```text
src/
├── main/java/[package]/
│   ├── application/      # Workflows, Agents, Consumers
│   ├── domain/           # Entities, value objects, domain logic
│   ├── api/              # HTTP Endpoints, request/response types
│   └── view/             # Views and query models
└── test/java/[package]/
    ├── unit/             # Domain logic tests
    └── integration/      # TestKitSupport-based component tests
```