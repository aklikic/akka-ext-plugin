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

Every POC should run standalone on a developer laptop with zero external dependencies. This ensures the demo works reliably in any environment, removes setup friction, and lets the customer focus on what Akka does rather than debugging connectivity.

What this means in practice:
- **All external systems are mocked** — databases, APIs, message brokers, third-party services. Mocks return realistic data with configurable latency and failure rates.
- **All AI/LLM dependencies are mockable** — if the POC uses Agents, provide a mock model mode that returns fixed responses with realistic latency (~200-500ms). This is critical for performance testing — you cannot benchmark throughput against a real LLM with rate limits and variable latency.
- **Single command to run** — one command starts everything. No Docker compose, no external databases, no API keys required for the basic demo flow.
- **Mocks are replaceable by configuration** — swapping a mock for a real service is a URL change in config, not a code change. This makes the Phase 2 path credible.

### Performance Testing with Gatling Enterprise

When scalability/throughput is a goal, the POC includes performance testing using **Gatling Enterprise**:

- **Gatling simulations** are a separate module (e.g., `performance-tests/`) — not part of the Akka service itself
- **Two simulation types**:
  - **Smoke test** — small number of requests to verify the deployed service works end-to-end
  - **Load test** — sustained TPS at target throughput, measuring latency percentiles and error rates
- **Test against deployed service** — the Akka service and its stub dependencies are deployed to **Akka Serverless**. Gatling runs against the deployed service URL, not localhost. This proves real infrastructure behavior, not just local performance.
- **Stub services deploy alongside** — mock/stub external dependencies are packaged as a separate Akka service and deployed to the platform. This gives realistic network latency between the main service and its dependencies.
- **Configurable parameters** — simulations accept system properties for `BASE_URL`, `RATE_PER_SEC`, `DURATION`, `RAMP_UP`, and any domain-specific parameters (e.g., `ACCOUNT_POOL_SIZE` for cache hit ratio tuning)
- **Gatling Enterprise packaging** — simulations are packaged as a fat JAR for upload to Gatling Enterprise, enabling distributed load generation and rich reporting

When performance testing is in scope, the **Deliverables** table should include:
- Gatling smoke test simulation
- Gatling load test simulation
- Stub services deployable to Akka Serverless
- Performance test results at target TPS

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
- Does the customer want a UI / dashboard? The UI should be minimalistic and map directly to the service's HTTP endpoints — it is a thin functional layer over the API, not a separate design exercise. Every UI action corresponds to an endpoint the service already exposes. Do not invent UI features that don't have a backing endpoint.
- Is there a specific business process to model, or is the use case abstract?

### Deployment & Phasing Questions
- **Does the customer need a phased approach?** The default POC model is two phases:
  - **Phase 1** — runs locally on the developer's laptop and deploys to Akka's Serverless environment. Self-contained with synthetic data, no infosec review needed, fast turnaround. Proves all goals.
  - **Phase 2** (if needed) — deploys to the customer's own environment via Akka's BYOC (Bring Your Own Cloud). Can be self-contained (same synthetic data in customer infra) and/or integrated with customer's application landscape.
- Not every engagement needs Phase 2. Ask: does the customer need to run in their own environment for this evaluation, or is Akka's Serverless environment sufficient?
- Does the customer have infosec or compliance requirements that affect where the POC runs? (HIPAA, SOC 2, HITRUST, data residency)
- Is there a preference for cloud provider? (AWS, Azure, GCP, on-prem)

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

### 2. Table of Contents

Auto-generated list of all sections. Place after the header, before the Executive Summary.

### 3. Executive Summary

3-5 sentences. What we're building, why it matters to this customer, and what the expected outcome is. A busy executive should be able to read only this and understand the proposal.

Do NOT list Akka features here. Focus on the customer's problem and the outcome.

### 4. Background

Set the context: what the customer does, what system or process this targets, and why now. Include:

- **Current state** — what exists today (technology, process, pain points)
- **Pain points** — specific problems this POC addresses

Use a Mermaid diagram if the current state or pain points benefit from visualization (e.g., a flow showing where latency comes from, or a diagram of a monolithic architecture's bottlenecks).

If the current state is assumed (pre-sales, no deep discovery yet), say so explicitly: *"Assumed based on initial conversations — to be validated."*

### 5. Proposed Solution

Bridge between the problem (Background) and the proof points (Goals). This section answers "what are we actually building?" before diving into goals and scope details. Include:

#### What We're Building

One paragraph. Plain language summary of the solution — what it does, not how it's built. A non-technical stakeholder should understand the value.

#### Solution Overview

A Mermaid diagram showing the end-to-end flow from input to output, including human actors. This is a business-level flow, not an Akka component diagram (that goes in Architecture). Use the same color conventions as architecture diagrams.

#### How It Works

Table with columns: **Step**, **What happens**, **Rules or AI?** (or similar discriminator relevant to the use case). Walk through the process step by step. This makes the solution concrete and reviewable.

#### Design Decisions

Table with columns: **Decision**, **Rationale**. Document the key choices made in the solution design and why. Examples: "Rules for matching, AI for exceptions", "Synthetic data, self-contained", "Human-in-the-loop for exceptions". This builds confidence that decisions are deliberate, not arbitrary.

### 6. Goals

What the POC proves. Number each goal and explain why it matters to this customer specifically. Typically 2-4 goals. Use the **Goal Discovery** questions above to determine which goals matter most.

Goals should emerge from the Goal Discovery conversation and the customer's specific pain points. Name goals using the customer's language and priorities, not generic Akka categories.

Each goal should include:

- **Title** — descriptive name tied to customer objectives (e.g., "Platform Performance — Complete the Daily Batch Reliably and Fast")
- **Why it matters** — paragraph connecting to customer pain point or stated objective
- **What we demonstrate** — bullet list of specific capabilities shown
- **How we demonstrate it** — numbered steps for the live demo or walkthrough
- **Platform comparison notes** (optional) — if the customer is evaluating alternatives, note what the comparison will cover

Good goals are:
- Tied to a customer pain point from the Background section
- Demonstrable in a live walkthrough
- Measurable (even if qualitatively)

The following are **common themes** that Akka POCs often demonstrate — use them as inspiration, not as mandatory categories:

- **Developer Experience** — how fast and pleasant it is to build with Akka
- **Operational Experience** — what you get out of the box on the Akka platform
- **Scalability** — how the architecture handles growing load
- **Quality of Output** — built-in evaluation and regression testing for AI outputs
- **AI Governance** — runtime-enforced guardrails, audit trail, human-in-the-loop

### 7. Scope

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

See Core Principles above for mocking guidelines (configurable latency/failure, realistic data, LLM mocks for performance testing).

State clearly: *"The POC runs standalone with no external dependencies. All mocks are replaced by configuration change, not code change, when connecting to real systems."*

### 8. Architecture

At minimum, include the **Akka Implementation Diagram** — shows how the Proposed Solution maps to Akka components (entities, workflows, agents, views, endpoints, etc.), with external systems and human actors. The business-level flow is already in the Proposed Solution section; this diagram shows the technical implementation.

Optional (include when they add value):
- Data flow / event sourcing diagram
- Benchmark architecture diagram

#### Diagram conventions

- Use Mermaid for all diagrams
- Color Akka components distinctly from external systems:
  - **Blue** (`#1a73e8`) — Akka transactional components (Entity, Workflow, View, Endpoint, Consumer, Timed Action)
  - **Purple** (`#7c4dff`) — Akka AI components (Agent, Evaluator, Guardrail)
  - **Orange** (`#ff8f00`) — External systems (mocked or real)
  - **Green** (`#2e7d32`) — Human actors
  - **Teal** (`#00897b`) — Web UI
- Number flow lines to show sequence
- Include a legend below each diagram

### 9. Deliverables

Numbered table of what ships:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | Working Akka service | Complete implementation with all components and mocked data |
| 2 | Stub services | Deployable mock dependencies with configurable latency and failure rates |
| 3 | Unit tests | Entity and workflow unit tests |
| 4 | Integration tests | End-to-end lifecycle tests |
| 5 | README with examples | Step-by-step guide to run locally and interact with the API |

If performance testing is a goal, also include:

| # | Deliverable | Description |
|---|-------------|-------------|
| 6 | Gatling smoke test | Simulation verifying deployed service works end-to-end |
| 7 | Gatling load test | Simulation at target TPS with latency and error rate reporting |
| 8 | Performance results | Gatling Enterprise report at target throughput |

### 10. Success Criteria

Table with three columns — tie each criterion back to a goal:

| Goal | Success Criterion | How Measured |
|------|-------------------|--------------|
| Prove workflow resilience | Workflow survives simulated crash mid-process | Kill and restart during workflow |
| Prove latency target | VALIDATION + ENGINE < 250ms p95 | Per-step metrics via OpenTelemetry |
| ... | ... | ... |

Criteria must be **observable** — something you can demonstrate in a live session or measure in a test run. Avoid vague criteria like "system performs well."

### 11. Phased Approach

Use the **Deployment & Phasing Questions** from Goal Discovery to determine whether a phased approach is needed. The default model:

#### Phase 1: Self-Contained POC on Akka Serverless (this scope)

The POC runs locally on the developer's laptop and deploys to **Akka's Serverless environment**. No infrastructure provisioning, no VPC setup, no infosec review required. Uses synthetic data and mocked external dependencies.

State clearly what Phase 1 proves (map to goals) and what the outcome is.

**Outcome:** One sentence — e.g., "A working system that proves the architecture, demonstrates all goals, and provides the evaluation data needed for the customer's decision."

#### Phase 2: BYOC Deployment (if needed)

Include Phase 2 only if the customer needs to run in their own environment. Not every engagement requires this — if Akka Serverless is sufficient for the evaluation, say so and omit Phase 2.

Phase 2 deploys the service to the customer's environment via Akka's BYOC (Bring Your Own Cloud). It can be **self-contained** (same synthetic data, just running in customer infrastructure) and/or **integrated** with the customer's application landscape. The scope depends on what the customer needs to validate:

- **Self-contained in BYOC** — proves the platform runs in their environment, satisfies infosec, no integration dependencies
- **Integrated in BYOC** — connects to real data sources, real systems, real compliance frameworks

When Phase 2 is included, it typically covers:

1. **Provision Akka BYOC** — VPC installation in the customer's environment per infosec requirements
2. **Connect to real data and systems** (if integrating) — replace mocks with actual integrations
3. **Implement full governance/compliance requirements** — map customer's compliance framework onto platform capabilities
4. **Production performance validation** — load testing with real volumes
5. **Expand to additional use cases** — same architecture, new domains
6. **Certification path** — SOC 2, HITRUST, etc. as applicable

This section is strategic — it shows the customer that the POC is a starting point with a clear path to production.

### 12. Assumptions & Open Questions

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
| **Internal Milestones** | POC has distinct internal build phases (e.g., milestone 1: core workflow, milestone 2: AI agent, milestone 3: dashboard) |

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

## Table of Contents

1. Executive Summary
2. Background
3. Proposed Solution
4. Goals
5. Scope
6. Architecture
7. Deliverables
8. Success Criteria
9. Phased Approach
10. Assumptions & Open Questions

## 1. Executive Summary

{3-5 sentences: what we're building, why it matters, expected outcome}

## 2. Background

### Current State

{What exists today — technology, process, scale}

### Pain Points

{Specific problems this POC addresses}

## 3. Proposed Solution

### What We're Building

{One paragraph: plain language summary of the solution}

### Solution Overview

{Mermaid diagram showing end-to-end business flow with legend}

### How It Works

| Step | What happens | Rules or AI? |
|------|-------------|--------------|
| | | |

### Design Decisions

| Decision | Rationale |
|----------|-----------|
| | |

## 4. Goals

### Goal 1: {Name — tied to customer objective}

**Why it matters:** {Connect to customer pain point}

**What we demonstrate:**
- {Capability 1}
- {Capability 2}

**How we demonstrate it:** {Numbered demo steps}

**Platform comparison notes:** {If evaluating alternatives}

### Goal 2: {Name}

{Same structure as Goal 1}

## 5. Scope

### What's Included

| Component | Type | Purpose |
|-----------|------|---------|
| | | |

### What's NOT in Scope

- {Item}

### What's Mocked / Stubbed

| Real System | Mock Implementation | Configurable |
|-------------|---------------------|--------------|
| | | |

The POC runs standalone with no external dependencies. All mocks are replaced by configuration change, not code change, when connecting to real systems.

## 6. Architecture

### Akka Implementation Diagram

{Mermaid diagram showing how the solution maps to Akka components, with numbered flow lines}

**Legend:**
- **Blue** — Akka transactional components (Entity, Workflow, View, Endpoint, Consumer, Timed Action)
- **Purple** — Akka AI components (Agent, Evaluator, Guardrail)
- **Orange** — External systems (mocked)
- **Green** — Human actors
- **Teal** — Web UI

## 7. Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | Working Akka service | Complete implementation with all components and mocked data |
| 2 | Stub services | Deployable mock dependencies with configurable latency and failure rates |
| 3 | Unit tests | Entity and workflow unit tests |
| 4 | Integration tests | End-to-end lifecycle tests |
| 5 | README with examples | Step-by-step guide to run locally and interact with the API |

## 8. Success Criteria

| Goal | Success Criterion | How Measured |
|------|-------------------|--------------|
| | | |

## 9. Phased Approach

### Phase 1: Self-Contained POC on Akka Serverless (this scope)

{What it proves, deployed to Akka Serverless, no infra investment needed}

**Outcome:** {One sentence}

### Phase 2: BYOC Deployment (if needed)

1. **Provision Akka BYOC** — {VPC in customer's environment}
2. **Connect real systems** (if integrating) — replace mocks with actual service APIs
3. **Implement full governance** — {customer-specific compliance}
4. **Production validation** — load testing with real volumes
5. **Expand use cases** — {customer-specific expansion path}

## 10. Assumptions & Open Questions

### Assumptions

1. {Assumption}

### Open Questions

1. {Question}

Please validate the assumptions above or suggest changes.
```
