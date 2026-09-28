# POC / SPOV Scope of Work — Guide & Template

This guide defines the standard structure for Akka POC and SPOV (Scope of Proof of Value) documents.

## Purpose

A scope of work document aligns the Akka team and the customer on what will be built, what it proves, and what comes next. It is the single artifact that the customer reviews before we start building.

## Audience

- **Primary**: Customer stakeholders (technical leads, architects, decision-makers)
- **Secondary**: Akka team members building the POC

## Tone

Professional but direct. Lead with value, not technology. Use tables over prose for structured information. Every section should earn its place — if it doesn't help the customer decide or the team build, cut it.

---

## Required Sections

### 1. Header

| Field | Description |
|-------|-------------|
| **Title** | `{Customer} x Akka — {One-line description}` |
| **Date** | Month Year |
| **Version** | `1.0 — Draft for Discussion` (update as it evolves) |
| **Prepared for** | Customer name, key contacts |
| **Prepared by** | Akka / Lightbend |

### 2. Executive Summary

3-5 sentences. What we're building, why it matters to this customer, and what the expected outcome is. A busy executive should be able to read only this and understand the proposal.

Do NOT list Akka features here. Focus on the customer's problem and the outcome.

### 3. Background

Set the context: what the customer does, what system or process this targets, and why now. Include:

- **Current state** — what exists today (technology, process, pain points)
- **Pain points** — specific problems this POC addresses

Use a Mermaid diagram if the current state or pain points benefit from visualization (e.g., a flow showing where latency comes from, or a diagram of a monolithic architecture's bottlenecks).

If the current state is assumed (pre-sales, no deep discovery yet), say so explicitly: *"Assumed based on initial conversations — to be validated."*

### 4. Goals

What the POC proves. Number each goal and explain why it matters to this customer specifically. Typically 2-4 goals.

Good goals are:
- Tied to a customer pain point from the Background section
- Demonstrable in a live walkthrough
- Measurable (even if qualitatively)

Common goal categories (pick what fits, don't force all):
- **Functional** — prove the domain model works (e.g., "demonstrate durable replenishment workflow")
- **DevEx** — show how fast you can build with Akka
- **OpsEx** — show what you get out of the box (observability, durability, auditability)
- **Performance** — prove latency/throughput targets
- **Architecture** — prove a pattern (event sourcing, CQRS, multi-region)

### 5. Scope

Three subsections:

#### What's Included

List the Akka components that will be built, in a table:

| Component | Type | Purpose |
|-----------|------|---------|
| `WarehouseProductEntity` | Event Sourced Entity | Inventory per product per warehouse |
| `ReplenishmentWorkflow` | Workflow | Durable multi-step store replenishment |
| ... | ... | ... |

#### What's NOT in Scope

Bullet list of things the customer might expect but that are explicitly excluded. Be specific — "production deployment" is better than "out of scope items".

#### What's Mocked / Stubbed

Table mapping real systems to their mock implementations:

| Real System | Mock Implementation |
|-------------|---------------------|
| Risk Engine | In-memory dataset of sample rules |
| Salesforce | Sample customer records |
| ... | ... |

State clearly: *"The POC runs standalone with no external dependencies. All mocks are replaced by configuration change, not code change, when connecting to real systems."*

### 6. Architecture

At minimum, include:

1. **High-level system diagram** — shows the Akka service, external systems, and human actors with numbered flow lines
2. **Core business flow** — sequence diagram or state diagram showing the main happy path

Optional (include when they add value):
- Akka components breakdown diagram
- Data flow / event sourcing diagram
- Benchmark architecture diagram

#### Diagram conventions

- Use Mermaid for all diagrams
- Color Akka components distinctly from external systems:
  - **Blue** (`#1a73e8`) — Akka transactional components (Entity, Workflow, View, Endpoint)
  - **Purple** (`#7c4dff`) — Akka AI components (Agent)
  - **Orange** (`#ff8f00`) — External systems (mocked or real)
  - **Green** (`#2e7d32`) — Human actors
  - **Teal** (`#00897b`) — Web UI
- Number flow lines to show sequence
- Include a legend below each diagram

### 7. Deliverables

Numbered table of what ships:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | Working Akka service | Complete implementation with all components and mocked data |
| 2 | Unit tests | Entity and workflow unit tests |
| 3 | Integration tests | End-to-end lifecycle tests |
| 4 | README with curl examples | Step-by-step guide to run locally |
| ... | ... | ... |

### 8. Success Criteria

Table with three columns — tie each criterion back to a goal:

| Goal | Success Criterion | How Measured |
|------|-------------------|--------------|
| Prove workflow resilience | Workflow survives simulated crash mid-process | Kill and restart during workflow |
| Prove latency target | VALIDATION + ENGINE < 250ms p95 | Per-step metrics via OpenTelemetry |
| ... | ... | ... |

Criteria must be **observable** — something you can demonstrate in a live session or measure in a test run. Avoid vague criteria like "system performs well."

### 9. After the POC

What this engagement enables. Typically 3-5 bullet points covering:

- What gets connected to real systems
- What gets deployed to production
- What additional use cases become possible
- How this positions Akka for broader adoption within the customer

This section is strategic — it shows the customer that the POC is a starting point, not an end.

### 10. Assumptions & Open Questions

Two parts:

**Assumptions** — what we assumed to be true while writing this scope. Numbered list. The customer should validate or correct these.

**Open Questions** — specific questions for the customer that would affect scope or design. Numbered list.

End this section with: *"Please validate the assumptions above or suggest changes."*

---

## Optional Sections

Include these when they add value for the specific engagement:

| Section | When to Include |
|---------|-----------------|
| **Non-Functional Requirements** | Performance/scale/availability are key selling points (latency targets, TPS, availability SLAs) |
| **Multi-Region / HA Strategy** | Enterprise modernization where HA is a requirement |
| **DevEx / OpsEx Comparison** | Replacing a legacy system — show legacy vs Akka side-by-side |
| **Throughput Benchmark** | Performance is a primary proof point |
| **Phased Delivery** | POC has distinct internal phases (e.g., Phase 1: static workflow, Phase 2: caching, Phase 3: AI agent) |

---

## Scaffold

```markdown
# {Customer} x Akka — {One-line description}

## Scope of Work

**Date:** {Month Year}
**Version:** 1.0 — Draft for Discussion
**Prepared for:** {Customer} — {Contact names}
**Prepared by:** Akka / Lightbend

---

## 1. Executive Summary

{3-5 sentences: what we're building, why it matters, expected outcome}

## 2. Background

### Current State

{What exists today — technology, process, scale}

### Pain Points

{Specific problems this POC addresses}

## 3. Goals

### Goal 1: {Name}

{What it proves and why it matters to this customer}

### Goal 2: {Name}

{What it proves and why it matters to this customer}

## 4. Scope

### What's Included

| Component | Type | Purpose |
|-----------|------|---------|
| | | |

### What's NOT in Scope

- {Item}

### What's Mocked / Stubbed

| Real System | Mock Implementation |
|-------------|---------------------|
| | |

The POC runs standalone with no external dependencies. All mocks are replaced by configuration change, not code change, when connecting to real systems.

## 5. Architecture

### High-Level System Diagram

{Mermaid diagram with numbered flow lines}

**Legend:**
- **Blue** — Akka transactional components
- **Purple** — Akka AI components (Agent)
- **Orange** — External systems (mocked)
- **Green** — Human actors

### Core Business Flow

{Mermaid sequence or state diagram}

## 6. Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | Working Akka service | Complete implementation with all components and mocked data |
| 2 | Unit tests | Entity and workflow unit tests |
| 3 | Integration tests | End-to-end lifecycle tests |
| 4 | README with curl examples | Step-by-step guide to run locally |

## 7. Success Criteria

| Goal | Success Criterion | How Measured |
|------|-------------------|--------------|
| | | |

## 8. After the POC

1. **Connect real systems** — replace mocks with actual service APIs
2. **Deploy to Akka cloud** — managed infrastructure with built-in observability
3. **Expand use cases** — {customer-specific expansion path}

## 9. Assumptions & Open Questions

### Assumptions

1. {Assumption}

### Open Questions

1. {Question}

Please validate the assumptions above or suggest changes.
```
