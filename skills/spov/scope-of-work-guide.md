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

## Core Principles

### Self-Contained POC

Every POC must run standalone on a developer laptop with zero external dependencies. This is non-negotiable — it ensures the demo works reliably in any environment, removes setup friction, and lets the customer focus on what Akka does rather than debugging connectivity.

What this means in practice:
- **All external systems are mocked** — databases, APIs, message brokers, third-party services. Mocks return realistic data with configurable latency and failure rates.
- **All AI/LLM dependencies are mockable** — if the POC uses Agents, provide a mock model mode that returns fixed responses with realistic latency (~200-500ms). This is critical for performance testing — you cannot benchmark throughput against a real LLM with rate limits and variable latency.
- **Single command to run** — `mvn compile exec:java` starts everything. No Docker compose, no external databases, no API keys required for the basic demo flow.
- **Mocks are replaceable by configuration** — swapping a mock for a real service is a URL change in config, not a code change. This makes the "After the POC" path credible.

### Performance Testing with Gatling Enterprise

When scalability/throughput is a goal, the POC includes performance testing using **Gatling Enterprise**:

- **Gatling simulations** are a separate Maven module (e.g., `performance-tests/`) — not part of the Akka service itself
- **Two simulation types**:
  - **Smoke test** — small number of requests to verify the deployed service works end-to-end
  - **Load test** — sustained TPS at target throughput, measuring latency percentiles and error rates
- **Test against deployed service** — the Akka service and its stub dependencies are deployed to the **Akka Platform**. Gatling runs against the deployed service URL, not localhost. This proves real infrastructure behavior, not just local performance.
- **Stub services deploy alongside** — mock/stub external dependencies are packaged as a separate Akka service and deployed to the platform. This gives realistic network latency between the main service and its dependencies.
- **Configurable parameters** — simulations accept system properties for `BASE_URL`, `RATE_PER_SEC`, `DURATION`, `RAMP_UP`, and any domain-specific parameters (e.g., `ACCOUNT_POOL_SIZE` for cache hit ratio tuning)
- **Gatling Enterprise packaging** — simulations are packaged as a fat JAR (`mvn gatling:enterprisePackage`) for upload to Gatling Enterprise, enabling distributed load generation and rich reporting

When performance testing is in scope, the **Deliverables** table should include:
- Gatling smoke test simulation
- Gatling load test simulation
- Stub services deployable to Akka Platform
- Performance test results at target TPS

### Three Pillars: DevEx, OpsEx, Scalability

Every POC should demonstrate value across three dimensions. The balance varies per customer, but all three should be present:

1. **Developer Experience (DevEx)** — how fast and pleasant it is to build with Akka
2. **Operational Experience (OpsEx)** — what you get out of the box when running on Akka
3. **Scalability** — how the architecture handles growing load without redesign

---

## Goal Discovery

Before writing the scope doc, use these questions to identify what matters most to this customer. The answers determine which goals to emphasize and which optional sections to include.

### DevEx Questions
- Is the customer evaluating Akka against other frameworks (LangChain, Spring, etc.)?
- Does the customer care about developer onboarding time?
- Is AI/agent development part of the use case? (If yes, show AI as a first-class component, not a bolt-on)
- Does the customer value testability? (If yes, emphasize the test kit — no external infra needed)

### OpsEx Questions
- Is auditability important? (regulatory, compliance, PCI, GDPR) → event sourcing + full audit trail
- Does the customer need human-in-the-loop? → workflow pause/resume + review UI
- Is observability a pain point today? → built-in tracing, metrics, logging
- Does the customer have durability concerns? (lost messages, incomplete processes) → durable execution

### Scalability Questions
- What is the expected throughput? (TPS, messages/day, concurrent users)
- Is latency a key concern? (If yes, include a benchmark with specific targets)
- Is the customer replacing a system that doesn't scale? → include throughput benchmark + legacy comparison
- Does the customer need multi-region? → include HA/multi-region strategy
- If AI/Agents are used, is throughput under realistic LLM latency a concern? → include mocked-LLM benchmark showing how Akka's concurrency compensates for model latency

### Scope Sizing Questions
- Is this a demo (show capability) or a pilot (prove on real data)?
- How many external systems need to be mocked?
- Does the customer want a UI? (adds ~1-2 days but greatly improves demo impact)
- Is there a specific business process to model, or is the use case abstract?

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

What the POC proves. Number each goal and explain why it matters to this customer specifically. Typically 2-4 goals. Use the **Goal Discovery** questions above to determine which goals matter most.

Good goals are:
- Tied to a customer pain point from the Background section
- Demonstrable in a live walkthrough
- Measurable (even if qualitatively)

Every POC should cover all three pillars (DevEx, OpsEx, Scalability), but the emphasis varies. Use the discovery questions to decide weighting:

#### DevEx goal (always include)
Show how quickly a production-grade solution can be built using the Akka SDK. Highlight:
- Opinionated component model — entities, workflows, agents compose with minimal boilerplate
- Built-in test kit — unit and integration tests run locally, no external infrastructure
- Local development — full service runs on a developer laptop with one command
- AI-native SDK — agents with tools and session memory are first-class components (if applicable)

#### OpsEx goal (always include)
Show what you get out of the box when deploying to the Akka platform. Highlight whichever matter most to this customer:
- Durable execution — workflow state survives restarts, no work is ever lost
- Observability — built-in tracing, metrics, and logging for every interaction
- Auditability — full event trail of every state transition (critical for compliance)
- Human-in-the-loop — workflow pauses for review before proceeding

#### Scalability goal (always include)
Show Akka's architecture handles load without redesign. Options:
- **Throughput benchmark** — with mocked dependencies (including mocked LLMs at realistic latency), demonstrate concurrent processing at scale
- **Latency proof** — show per-step latency breakdown and end-to-end targets
- **Architecture story** — the same components that power the POC can handle production-grade workloads

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

Table mapping real systems to their mock implementations. Every external dependency must appear here — the POC must be self-contained.

| Real System | Mock Implementation | Configurable |
|-------------|---------------------|--------------|
| Risk Engine | In-memory dataset of sample rules | - |
| Salesforce | Sample customer records | - |
| LLM / Model Provider | Fixed responses with realistic latency (~200-500ms) | Response latency, response content |
| External API | HTTP stub returning mock data | Response latency, failure rate |
| ... | ... | ... |

**Mocking rules:**
- Every mock must have **configurable latency** so the POC can demonstrate both fast-path and degraded-path behavior
- Every mock should support a **configurable failure rate** for resilience demos
- **LLM/Agent mocks are mandatory** when performance testing is a goal — you cannot benchmark throughput against a real LLM with rate limits and variable latency. Use `TestModelProvider` or a fixed-response stub with realistic latency (~200-500ms per inference) to show how Akka's concurrency model processes requests in parallel despite model latency
- Mocks should return **realistic data shapes** — not empty responses or "test" strings. The demo is more convincing when the data looks real.

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
| 2 | Stub services | Deployable mock dependencies with configurable latency and failure rates |
| 3 | Unit tests | Entity and workflow unit tests |
| 4 | Integration tests | End-to-end lifecycle tests |
| 5 | README with curl examples | Step-by-step guide to run locally and interact with the API |

If performance testing is a goal, also include:

| # | Deliverable | Description |
|---|-------------|-------------|
| 6 | Gatling smoke test | Simulation verifying deployed service works end-to-end |
| 7 | Gatling load test | Simulation at target TPS with latency and error rate reporting |
| 8 | Performance results | Gatling Enterprise report at target throughput |

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
| 2 | Stub services | Deployable mock dependencies with configurable latency and failure rates |
| 3 | Unit tests | Entity and workflow unit tests |
| 4 | Integration tests | End-to-end lifecycle tests |
| 5 | README with curl examples | Step-by-step guide to run locally and interact with the API |

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
