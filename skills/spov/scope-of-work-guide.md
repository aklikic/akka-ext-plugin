# POC / SPOV Scope of Work — Guide & Template

This guide defines the standard structure for Akka POC and SPOV (Scope of Proof of Value) documents.

## Purpose

A scope of work document aligns the Akka team and the customer on what will be built, what it proves, and what comes next. It is the single artifact that the customer reviews before we start building.

## Audience

- **Primary**: Customer stakeholders (technical leads, architects, decision-makers)
- **Secondary**: Akka team members building the POC

## Tone

Professional but direct. Lead with value, not technology. Use tables over prose for structured information. Every section should earn its place — if it doesn't help the customer decide or the team build, cut it.

Never name specific competitors in the document. Use "alternative frameworks" or "alternative approaches." The doc may circulate internally at the customer — don't give competitors free visibility. The customer already knows who they're evaluating.

No CLI commands in customer-facing text. Use outcome-oriented language: "start the service with a single command", "run the test suite", "all tests pass with no external setup." The audience is stakeholders, not developers.

## Document Stages

Every scope doc progresses through three stages. The header includes the current stage.

| Stage | Purpose | Distribution | Timeline | Open Questions |
|-------|---------|-------------|----------|----------------|
| **DRAFT** | Internal working document | Not for distribution | TBD | Populated |
| **PROPOSAL** | Shared with customer for discussion | Customer stakeholders | TBD or tentative | Drive engagement |
| **AGREED** | Scope confirmed, ready to execute | All parties | Confirmed with dates | Resolved and removed |

Sections that change between stages are annotated with:
*This section is confirmed at AGREED stage.*

---

## Core Principles

### Self-Contained POC

Every POC should run standalone on a developer laptop with zero external dependencies. This ensures the demo works reliably in any environment, removes setup friction, and lets the customer focus on what Akka does rather than debugging connectivity.

What this means in practice:
- **All external systems are mocked** — databases, APIs, message brokers, third-party services. Mocks return realistic data with configurable latency and failure rates.
- **All AI/LLM dependencies are mockable** — if the POC uses Agents, provide a mock model mode that returns fixed responses with realistic latency (~200-500ms). This is critical for performance testing — you cannot benchmark throughput against a real LLM with rate limits and variable latency.
- **Single command to run** — one command starts everything. No Docker compose, no external databases, no API keys required for the basic demo flow.
- **Mocks are replaceable by configuration** — swapping a mock for a real service is a URL change in config, not a code change. This makes the next steps path credible.

### The Use Case is a Vehicle

The use case is the vehicle to POC Akka. Expected Benefits must reflect what the **platform** brings, not what the use case solves. The customer already knows the value of their use case — what they need to see is what Akka delivers as a platform.

### Performance Testing with Gatling Enterprise

When scalability/throughput is a goal, the POC includes performance testing using **Gatling Enterprise**:

- **Gatling simulations** are a separate module (e.g., `performance-tests/`) — not part of the Akka service itself
- **Two simulation types**:
  - **Smoke test** — small number of requests to verify the deployed service works end-to-end
  - **Load test** — sustained TPS at target throughput, measuring latency percentiles and error rates
- **Test against deployed service** — the Akka service and its stub dependencies are deployed to **Akka Serverless**. Gatling runs against the deployed service URL, not localhost. This proves real infrastructure behavior, not just local performance.
- **Stub services deploy alongside** — mock/stub external dependencies are packaged as a separate Akka service and deployed to the platform. This gives realistic network latency between the main service and its dependencies.
- **Configurable parameters** — simulations accept system properties for `BASE_URL`, `RATE_PER_SEC`, `DURATION`, `RAMP_UP`, and any domain-specific parameters
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
- Is the customer evaluating Akka against alternative frameworks?
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

### Deployment Questions
- Does the customer have infosec or compliance requirements that affect where the POC runs? (HIPAA, SOC 2, HITRUST, data residency)
- Is there a preference for cloud provider? (AWS, Azure, GCP, on-prem)

---

## Required Sections

### 1. Header

| Field | Description |
|-------|-------------|
| **Title** | `{Customer} x Akka — {One-line description}` |
| **Status** | `DRAFT`, `PROPOSAL`, or `AGREED` (see Document Stages) |
| **Date** | Month Year |
| **Version** | `1.0 — Draft for Discussion` (update as it evolves) |
| **Prepared for** | Customer name, key contacts |
| **Prepared by** | Akka / Lightbend |

Include the document stages table after the header fields (see Document Stages above).

### 2. Executive Summary

3-5 sentences. What we're building, why it matters to this customer, and what the expected outcome is. A busy executive should be able to read only this and understand the proposal.

Do NOT list Akka features here. Focus on the customer's problem and the outcome.

### 3. Background

Set the context: what the customer does, what system or process this targets, and why now. This section covers **Current State only** — what exists today (technology landscape, process, scale).

Do NOT include a Pain Points subsection here. Pain points are obvious to the customer and repeating them in Background is redundant — they appear in Expected Benefits (Section 6) where they are mapped to what Akka delivers.

Use a Mermaid diagram if the current state benefits from visualization (e.g., a flow showing the existing architecture or process).

If the current state is assumed (pre-sales, no deep discovery yet), say so explicitly: *"Assumed based on initial conversations — to be validated."*

### 4. Proposed Solution

Bridge between the problem (Background) and the proof points (Goals). This section answers "what are we actually building?" before diving into goals and scope details. Include:

#### What We're Building

One paragraph. Plain language summary of the solution — what it does, not how it's built. A non-technical stakeholder should understand the value.

#### Solution Overview

A Mermaid diagram showing the end-to-end flow from input to output, including human actors. This is a business-level flow, not an Akka component diagram (that goes in Architecture). Use the same color conventions as architecture diagrams.

#### How It Works

Table with columns: **Step**, **What happens**, **Rules or AI?** (or similar discriminator relevant to the use case). Walk through the process step by step. This makes the solution concrete and reviewable.

#### Design Decisions

Table with columns: **Decision**, **Rationale**. Document the key choices made in the solution design and why. Examples: "Rules for matching, AI for exceptions", "Synthetic data, self-contained", "Human-in-the-loop for exceptions". This builds confidence that decisions are deliberate, not arbitrary.

### 5. Goals

What the POC proves. Number each goal and explain why it matters to this customer specifically. Typically 2-4 goals. Use the **Goal Discovery** questions above to determine which goals matter most.

Goals should emerge from the Goal Discovery conversation and the customer's specific pain points. Name goals using the customer's language and priorities, not generic Akka categories.

Each goal should include:

- **Title** — descriptive name tied to customer objectives (e.g., "Platform Performance — Complete the Daily Batch Reliably and Fast")
- **Why it matters** — paragraph connecting to customer pain point or stated objective
- **What we demonstrate** — bullet list of specific capabilities shown
- **How we demonstrate it** — numbered steps for the live demo or walkthrough
- **Platform comparison notes** (optional) — if the customer is evaluating alternatives, note what the comparison will cover. Never name specific competitors.

Good goals are:
- Tied to a customer pain point
- Demonstrable in a live walkthrough
- Measurable (even if qualitatively)

The following are **common themes** that Akka POCs often demonstrate — use them as inspiration, not as mandatory categories:

- **Developer Experience** — how fast and pleasant it is to build with Akka
- **Operational Experience** — what you get out of the box on the Akka platform
- **Scalability** — how the architecture handles growing load
- **Quality of Output** — built-in evaluation and regression testing for AI outputs
- **AI Governance** — runtime-enforced guardrails, audit trail, human-in-the-loop

### 6. Expected Benefits

Maps customer pain points to what **Akka as a platform** delivers. This is NOT about what the use case solves — the customer already knows that. This is about what the platform brings.

Table with columns: **Pain Point**, **What Akka delivers**.

Example rows (adapt to customer):

| Pain Point | What Akka delivers |
|------------|---------------------|
| Cross-cloud complexity | Single platform — agent, orchestration, state, and API in one service |
| Volume overwhelm | Concurrent processing — actor model scales horizontally, same architecture for this use case and core workloads |
| Consistency risk | Deterministic orchestration — Workflows enforce same steps every time |
| Compliance exposure | Built-in audit trail & AI governance — logged out of the box, no custom logging to build |
| Operational blind spots | Observability out of the box — Akka Console and Grafana, zero config |
| Slow time-to-production | Rapid development — production-grade service in days, one codebase |

Key principle: the use case is a vehicle to POC Akka. Benefits must reflect what Akka brings, not what the use case solves.

### 7. Scope

Three subsections:

#### What's Included

List the Akka components that will be built, in a table:

| Component | Type | Purpose |
|-----------|------|---------|
| ... | ... | ... |

#### What's NOT in Scope

Bullet list of things the customer might expect but that are explicitly excluded. Be specific — "production deployment" is better than "out of scope items".

#### What's Mocked / Stubbed

Table mapping real systems to their mock implementations. Every external dependency must appear here — the POC must be self-contained.

| Real System | Mock Implementation | Configurable |
|-------------|---------------------|--------------|
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
| ... | ... | ... |

Criteria must be **observable** — something you can demonstrate in a live session or measure in a test run. Avoid vague criteria like "system performs well."

### 11. Timeline

*This section is confirmed at AGREED stage.*

In DRAFT and PROPOSAL stages, include only a milestones table with TBD dates:

| Milestone | Target |
|-----------|--------|
| Scope agreed | TBD |
| POC delivered | TBD |
| Live demo walkthrough | TBD |

Do NOT include duration estimates (e.g., "2 weeks") until scope is agreed. Add:

*"Timeline will be confirmed once scope is agreed. Key dependency: customer availability for the live demo walkthrough."*

At AGREED stage, replace TBD with confirmed dates.

### 12. Next Steps

*This section is confirmed at AGREED stage.*

What happens after the POC. Keep it simple — two items:

1. **Deploy Akka in customer's environment** — BYOC/BYOK8s into their VPC
2. **Connect real systems** — replace mocks with actual APIs via configuration change

Do not add items like PII/PCI sanitization, production performance validation, or "expand to other use cases" — those are sales conversations, not scope doc content. Don't plant the idea of running outside Akka Serverless unless the customer explicitly asks.

### 13. Assumptions & Open Questions

*This section is confirmed at AGREED stage.*

Two parts:

**Assumptions** — what we assumed to be true while writing this scope. Numbered list. The customer should validate or correct these.

**Open Questions** — specific questions for the customer that would affect scope or design. Numbered list.

At AGREED stage, assumptions are validated and open questions are resolved and removed.

End this section with: *"Please validate the assumptions above or suggest changes."*

---

## Optional Sections

Include these when they add value for the specific engagement:

| Section | When to Include |
|---------|-----------------|
| **Non-Functional Requirements** | Performance/scale/availability are key selling points (latency targets, TPS, availability SLAs) |
| **Multi-Region / HA Strategy** | Enterprise modernization where HA is a requirement |
| **Platform Comparison** | Customer is evaluating alternatives — show side-by-side without naming competitors |
| **Throughput Benchmark** | Performance is a primary proof point |
| **Internal Milestones** | POC has distinct internal build phases (e.g., milestone 1: core workflow, milestone 2: AI agent, milestone 3: dashboard) |

---

## Scaffold

```markdown
# {Customer} x Akka — {One-line description}

## Scope of Work

**Status:** DRAFT
**Date:** {Month Year}
**Version:** 1.0 — Draft for Discussion
**Prepared for:** {Customer} — {Contact names}
**Prepared by:** Akka / Lightbend

| Stage | Purpose | Distribution |
|-------|---------|-------------|
| **DRAFT** | Internal working document | Not for distribution |
| **PROPOSAL** | Shared with customer for discussion | Customer stakeholders |
| **AGREED** | Scope confirmed, ready to execute | All parties |

---

## Table of Contents

1. Executive Summary
2. Background
3. Proposed Solution
4. Goals
5. Expected Benefits
6. Scope
7. Architecture
8. Deliverables
9. Success Criteria
10. Timeline
11. Next Steps
12. Assumptions & Open Questions

## 1. Executive Summary

{3-5 sentences: what we're building, why it matters, expected outcome}

## 2. Background

### Current State

{What exists today — technology, process, scale}

*Assumed based on initial conversations — to be validated.*

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

### Goal 2: {Name}

{Same structure as Goal 1}

## 5. Expected Benefits

| Pain Point | What Akka delivers |
|------------|---------------------|
| | |

## 6. Scope

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

## 7. Architecture

### Akka Implementation Diagram

{Mermaid diagram showing how the solution maps to Akka components, with numbered flow lines}

**Legend:**
- **Blue** — Akka transactional components (Entity, Workflow, View, Endpoint, Consumer, Timed Action)
- **Purple** — Akka AI components (Agent, Evaluator, Guardrail)
- **Orange** — External systems (mocked)
- **Green** — Human actors
- **Teal** — Web UI

## 8. Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | Working Akka service | Complete implementation with all components and mocked data |
| 2 | Stub services | Deployable mock dependencies with configurable latency and failure rates |
| 3 | Unit tests | Entity and workflow unit tests |
| 4 | Integration tests | End-to-end lifecycle tests |
| 5 | README with examples | Step-by-step guide to run locally and interact with the API |

## 9. Success Criteria

| Goal | Success Criterion | How Measured |
|------|-------------------|--------------|
| | | |

## 10. Timeline

| Milestone | Target |
|-----------|--------|
| Scope agreed | TBD |
| POC delivered | TBD |
| Live demo walkthrough | TBD |

*Timeline will be confirmed once scope is agreed. Key dependency: customer availability for the live demo walkthrough.*

## 11. Next Steps

1. **Deploy Akka in customer's environment** — BYOC/BYOK8s into their VPC
2. **Connect real systems** — replace mocks with actual APIs via configuration change

## 12. Assumptions & Open Questions

### Assumptions

1. {Assumption}

### Open Questions

1. {Question}

Please validate the assumptions above or suggest changes.
```
