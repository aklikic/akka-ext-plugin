# Akka Demo Showcase — Specification

## Purpose

The Demo Showcase is a self-contained, full-screen storytelling view designed to communicate the depth and production-readiness of systems built with Akka Specify. It answers the question every prospect asks after seeing a demo: *"But can it actually run in production?"*

The showcase transforms a working demo from a "cool prototype" into proof of engineering superiority by revealing the architecture, resilience, and platform capabilities that are invisible at the surface level. It is designed to be dropped into the Akka sales presentation as a single view, or used standalone for customer-specific demo walkthroughs.

## Problem Statement

Competitors like Lovable, Replit, and Bolt can generate working web applications from natural language prompts. Their output looks visually similar to what Akka Specify produces. However, these tools generate:

- Single-process, stateless applications
- Monolithic codebases backed by a single database
- Systems with no resilience, no clustering, no sharding
- Applications that cannot scale beyond a single machine
- Code with no governance, compliance, or operational tooling

Akka Specify produces distributed, event-driven systems with Event Sourced Entities, Key-Value Entities, Workflows, Views, Consumers, service-to-service eventing, and full HA/DR — all automatically. But this sophistication is invisible to the user. The Demo Showcase makes the invisible visible.

## Target Audience

1. **Technical evaluators** (architects, senior engineers) — want proof of architectural depth
2. **Engineering leaders** (VP Eng, CTO) — want proof of team velocity and platform value
3. **Business stakeholders** (VP Product, CEO) — want proof of speed-to-market and cost reduction

## Narrative Structure

The showcase follows a six-tab progressive reveal. Each tab peels back a layer, building conviction:

| Tab | Label | Message | Audience Reaction |
|-----|-------|---------|-------------------|
| 1 | The Brief | Here's the problem we solved | "That's my problem too" |
| 2 | The App | Built in under an hour | "Ok, impressive speed" |
| 3 | The Architecture | Here's what's really inside | "Wait — THAT's what it generated?" |
| 4 | The Proof | It survives anything | "Lovable can't do that" |
| 5 | The Platform | Now multiply by your whole team | "This changes how we work" |
| 6 | Ship It | Deploy today with full HA/DR | "Let's go" |

The pivot between Tab 4 (Proof) and Tab 5 (Platform) is the key narrative turn — shifting from selling a technology to selling an organizational transformation.

---

## Tab Specifications

### Tab 1: The Brief

**Purpose:** Set the stakes. Make the audience recognize their own problem.

**Content:**
- Use case title (e.g., "Intelligent Order Orchestration")
- Customer context in 2-3 sentences — who asked, what they needed, why it's hard
- A "time to build" metric prominently displayed (e.g., "Spec to running system: 47 minutes")
- 3-4 requirement bullets showing the scope of what was asked for
- A subtle comparison: "Traditional estimate: 6-8 weeks with a team of 5"

**Visual design:**
- Left-aligned content on dark background
- Large headline with yellow accent on the use case name
- Time metric in large green text (matching the value prop number style)
- Requirements as a minimal bullet list with yellow left border
- Subtle background dot pattern (matching presentation style)

---

### Tab 2: The App

**Purpose:** Show the working result. Establish credibility. Don't linger — this is table stakes.

**Content:**
- Screenshot or embedded iframe of the running application
- 3-4 callout annotations pointing to key features
- A small stats bar: endpoints created, entity types, event types, lines of code generated

**Visual design:**
- Centered application screenshot/iframe with subtle border and shadow
- Callout annotations as small floating cards with connecting lines
- Stats bar at the bottom as horizontal pill badges
- The screenshot should have a browser chrome frame (dark theme) for realism

---

### Tab 3: The Architecture (Hero Tab)

**Purpose:** The WOW moment. Reveal what Specify actually built — the distributed machinery that competitors cannot generate.

**Content:**

**Left panel — Component inventory:**
- List of all generated components by type:
  - Event Sourced Entities (with entity names, event counts)
  - Key-Value Entities
  - Workflows (with step counts)
  - Views / Projections
  - Consumers
  - Endpoints (HTTP/gRPC)
  - Timed Actions
- Total generated artifacts count

**Center panel — Architecture diagram (animated SVG):**
- Layered architecture visualization:
  - **Top row:** API endpoints (HTTP/gRPC boxes)
  - **Middle rows:** Entities, Workflows, Views — connected by animated event flow arrows
  - **Bottom row:** Event journal, sharding visualization, multi-region indicators
- Components color-coded by type:
  - Event Sourced Entities: Yellow (#F5C518)
  - Key-Value Entities: Green (#28C840)
  - Workflows: Blue (#1E90FF)
  - Views: Purple (#A855F7)
  - Consumers: Orange (#F97316)
  - Endpoints: White (#fff)
- Animated dashed lines showing event flow between components
- Sharding indicator showing entity distribution across nodes

**Right panel — "Surface vs X-Ray" toggle:**
- **Surface view:** Simple API diagram (what the user sees) — a few boxes and arrows
- **X-Ray view:** Full distributed architecture (what's actually running)
- Toggle between views with a smooth morphing animation

**Visual design:**
- Three-column layout (inventory | diagram | comparison)
- SVG diagram uses draw-line animations (stroke-dashoffset) matching the presentation's existing style
- Components animate in with staggered boxIn animations
- Event flow arrows pulse with the `pulse` keyframe
- Dark card backgrounds (#0A0A0A) with thin borders (#1C1C1C)

---

### Tab 4: The Proof

**Purpose:** Show that the generated system is production-grade, not a prototype. This is where competitors fall apart.

**Content:**

**Performance metrics (top row):**
- Concurrent users handled: "10,000+"
- p99 latency: "<5ms"  
- Events processed per second: "50,000+"
- Zero data loss guarantee

**Resilience demonstration (center):**
- Animated failover visualization:
  1. Show 3 nodes in a cluster with entities distributed
  2. One node turns red (failure)
  3. Entities automatically rebalance to surviving nodes
  4. "0 requests dropped" counter stays at zero
  5. Failed node recovers, entities rebalance back
- Timeline showing: failure → detection → recovery → rebalance (with millisecond timestamps)

**Comparison table (bottom):**
| Capability | Lovable / Replit | Akka Specify |
|-----------|-----------------|--------------|
| Architecture | Single process, stateless | Distributed, event-driven |
| State management | PostgreSQL, single DB | Event sourcing + sharding |
| Concurrent users | ~100 (single thread) | 10,000+ (actor-based) |
| Failover | Full restart, data loss risk | Zero-downtime, auto-rebalance |
| Multi-region | Not supported | Active-active HA/DR |
| Consistency | Best effort | Exactly-once event processing |

**Visual design:**
- Metrics as large number cards (green text, dark background)
- Cluster visualization as animated SVG circles with entity dots
- Comparison table with red/green visual indicators
- Yellow accent borders on the Akka column

---

### Tab 5: The Platform

**Purpose:** Shift from "one demo" to "your team's new velocity." This is where engineering leaders decide to buy.

**Content:**

**Panel A — Multi-Tenant by Default:**
- Visual: Multiple service cards on shared compute, with isolation boundaries drawn
- Message: "Ship service #2, #3, #4 onto the same platform. No noisy neighbor. No new infrastructure. Marginal cost of each new service approaches zero."
- Stat: "1 platform, N services, shared compute"

**Panel B — API-First Control Plane:**
- Visual: Terminal mock showing `akka service list`, `akka service deploy`, `akka metrics get`
- Message: "Every operation is an API call. Wire into your internal developer portal — Backstage, Cortex, whatever you run."
- Stat: "100% of operations available via API"

**Panel C — Extensible SDLC Integration:**
- Visual: Flow diagram — Specify commands → CI/CD → code review → compliance gates → deploy
- Message: "Specify doesn't replace your process — it plugs into it. Custom templates, custom checks, your team's conventions baked in."
- Stat: "Integrates with any GitOps workflow"

**Panel D — Living Best Practices:**
- Visual: Changelog feed with weekly updates
- Message: "Every app gets smarter over time. Akka's engineering team ships best practices weekly — they flow into your existing services, not just new ones."
- Stat: "Weekly platform updates, zero migration effort"

**Visual design:**
- 2x2 grid of cards
- Each card: icon (top-left), bold one-liner, visual element, supporting text
- Cards have thin yellow top border (3px, animated scaleX on reveal)
- Subtle hover effect (border-color lighten)
- Staggered reveal animation (0.1s delay between cards)

---

### Tab 6: Ship It

**Purpose:** Close the deal. Remove the last objection: "but how hard is it to deploy?"

**Content:**

**Deployment options (top):**
- One-click deploy to Akka Cloud
- Container export for any Kubernetes environment  
- GitOps integration (generated CI/CD pipeline)

**HA/DR topology (center):**
- Multi-region architecture diagram showing:
  - 2-3 regions with active-active replication
  - Automatic failover arrows between regions
  - Data replication indicators

**Compliance & certifications (bottom-left):**
- Grid of certification badges (SOC2, ISO 27001, GDPR, etc.)
- "19 certifications out of the box"

**Cost comparison (bottom-right):**
- Side-by-side: "Build it yourself" vs "Akka Specify"
- Team size, timeline, infrastructure cost, maintenance burden

**Visual design:**
- Deployment options as horizontal cards with icons
- HA/DR diagram as animated SVG (matching presentation style)
- Certifications as a compact logo grid
- Cost comparison as a two-column card with green highlights on savings

---

## Visual Design System

All styling inherits from the Akka sales presentation:

### Colors
```css
--yellow: #F5C518       /* Primary accent */
--black: #000           /* Primary background */
--dark: #07070C         /* Secondary background */
--white: #fff           /* Primary text */
--gray: #555            /* Tertiary text */

/* Extended palette */
Dark surfaces: #0A0A0A, #0D0D0D, #141414
Borders: #1A1A1A, #1C1C1C, #222, #333
Text grays: #666, #888, #999, #B8B8B8
Green (metrics): #28C840
Red (failures): #E74C3C
Blue (workflows): #1E90FF
```

### Typography
```css
font-family: 'Instrument Sans', -apple-system, BlinkMacSystemFont, sans-serif;

/* Scale */
Tab headline:    clamp(28px, 3vw, 44px), weight 700
Section label:   11px uppercase, letter-spacing 3px, weight 600
Card title:      clamp(15px, 1.4vw, 20px), weight 700
Body text:       13-14px, color #999 or #B8B8B8
Metric numbers:  clamp(24px, 2.2vw, 34px), weight 700, color #28C840
Code/terminal:   'SF Mono', 'Cascadia Code', 'Consolas', monospace
```

### Animation patterns
```css
/* Element reveal */
initial:  opacity: 0; transform: translateY(16px);
visible:  opacity: 1; transform: none;
timing:   opacity .5s ease, transform .5s cubic-bezier(0.16,1,0.3,1);

/* Staggered delays */
Children stagger by 0.1s increments

/* SVG line draw */
stroke-dasharray: 1000; stroke-dashoffset: 1000;
animation: drawLine 0.75s ease forwards;

/* Pulse (event flow) */
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.3; } }
```

### Component patterns
```css
/* Cards */
background: #0A0A0A;
border: 1px solid #1C1C1C;
border-radius: 10px;
padding: 20px;

/* Yellow top accent bar */
::before { height: 3px; background: var(--yellow); transform: scaleX(0); }
.visible::before { transform: scaleX(1); }

/* Eyebrow labels */
::before { width: 28px; height: 2px; background: var(--yellow); margin-right: 10px; }

/* Background dot pattern */
background-image: radial-gradient(circle, rgba(245,197,24,0.04) 1px, transparent 1px);
background-size: 48px 48px;
```

---

## Layout & Navigation

### Overall structure
```
+--------------------------------------------------+
|  [Full-screen view, 100vh]                       |
|                                                   |
|  +--------+-------------------------------------+ |
|  |        |                                     | |
|  | LEFT   |         CONTENT AREA                | |
|  | NAV    |                                     | |
|  |        |         (tab content fills           | |
|  | Tab 1  |          this entire area)           | |
|  | Tab 2  |                                     | |
|  | Tab 3  |                                     | |
|  | Tab 4  |                                     | |
|  | Tab 5  |                                     | |
|  | Tab 6  |                                     | |
|  |        |                                     | |
|  +--------+-------------------------------------+ |
+--------------------------------------------------+
```

### Left navigation
- Fixed width: 220px
- Dark background: #0A0A0A
- Right border: 1px solid #1C1C1C
- Each tab: icon + label, padding 16px 20px
- Active tab: yellow left border (3px), slightly lighter background (#141414)
- Hover: background #0D0D0D
- Tabs are navigable via click or keyboard (1-6 number keys)

### Content transitions
- Tab content slides horizontally (translateX) with 0.4s ease transition
- Outgoing tab slides left and fades; incoming tab slides in from right
- Elements within each tab use staggered reveal animations on tab activation

### Keyboard navigation
- Number keys 1-6: jump to tab
- ArrowRight/ArrowLeft: next/previous tab (when this view is active in the presentation)
- Escape: return to presentation flow

---

## Data Model (for extensibility)

Each demo showcase is driven by a configuration object:

```javascript
const demoConfig = {
  // Tab 1: The Brief
  brief: {
    title: "Intelligent Order Orchestration",
    context: "A Fortune 500 retailer needed real-time order orchestration across 2,000 stores...",
    buildTime: "47 minutes",
    traditionalEstimate: "6-8 weeks, team of 5",
    requirements: [
      "Real-time inventory reservation across 2,000 locations",
      "Multi-step order workflows with compensation logic",
      "Event-driven notifications to customers and fulfillment",
      "Sub-10ms response times at 10,000 concurrent orders"
    ]
  },

  // Tab 2: The App
  app: {
    screenshot: "demo-screenshots/order-app.png",  // or iframe URL
    callouts: [
      { x: "20%", y: "30%", label: "Real-time inventory", desc: "Live stock levels across all locations" },
      { x: "60%", y: "50%", label: "Order workflow", desc: "Multi-step orchestration with rollback" }
    ],
    stats: {
      endpoints: 12,
      entityTypes: 4,
      eventTypes: 18,
      linesOfCode: 3200
    }
  },

  // Tab 3: The Architecture
  architecture: {
    components: [
      { type: "event-sourced-entity", name: "Order", events: 6 },
      { type: "event-sourced-entity", name: "Payment", events: 4 },
      { type: "key-value-entity", name: "InventoryItem", events: 0 },
      { type: "workflow", name: "OrderFulfillment", steps: 5 },
      { type: "view", name: "OrdersByCustomer" },
      { type: "view", name: "InventoryDashboard" },
      { type: "consumer", name: "NotificationConsumer" },
      { type: "consumer", name: "AnalyticsConsumer" },
      { type: "endpoint", name: "OrderAPI" },
      { type: "endpoint", name: "InventoryAPI" },
      { type: "timed-action", name: "OrderTimeout" }
    ],
    connections: [
      { from: "OrderAPI", to: "Order" },
      { from: "Order", to: "OrderFulfillment", type: "event" },
      { from: "OrderFulfillment", to: "Payment", type: "command" },
      { from: "OrderFulfillment", to: "InventoryItem", type: "command" },
      { from: "Order", to: "OrdersByCustomer", type: "event-stream" },
      { from: "Order", to: "NotificationConsumer", type: "event-stream" },
      { from: "InventoryItem", to: "InventoryDashboard", type: "state-change" },
      { from: "OrderTimeout", to: "OrderFulfillment", type: "timer" }
    ]
  },

  // Tab 4: The Proof
  proof: {
    metrics: {
      concurrentUsers: "10,000+",
      p99Latency: "<5ms",
      eventsPerSecond: "50,000+",
      dataLoss: "Zero"
    },
    clusterNodes: 3
  },

  // Tab 5: The Platform
  platform: {
    services: ["Order Service", "Payment Service", "Notification Service"],
    apiExamples: [
      "$ akka service list",
      "$ akka service deploy order-service --region us-east-1",
      "$ akka metrics get order-service --window 1h"
    ],
    sdlcSteps: ["Specify", "Generate", "Review", "Test", "Gate", "Deploy"],
    recentUpdates: [
      { week: "Week 16", update: "Optimized sharding for high-cardinality entities" },
      { week: "Week 15", update: "New workflow compensation patterns" },
      { week: "Week 14", update: "EU AI Act governance templates" }
    ]
  },

  // Tab 6: Ship It
  ship: {
    regions: ["us-east-1", "eu-west-1", "ap-southeast-1"],
    certifications: ["SOC2", "ISO 27001", "GDPR", "HIPAA", "FedRAMP"],
    costComparison: {
      traditional: { team: 5, weeks: 8, infraMonthly: "$12,000", maintenance: "2 FTEs" },
      akka: { team: 1, weeks: 0.1, infraMonthly: "$800", maintenance: "Platform-managed" }
    }
  }
};
```

This configuration allows each demo/POC to be showcased by swapping the config object. Future integration with Akka Specify can auto-generate this config from the project's component registry.

---

## Integration with Sales Presentation

When integrated into the main `akka-sales-presentation.html`:

1. The showcase becomes a new section between the dev-zero demo (s5) and resilience (s6)
2. It receives its own wrapper (`#demo-wrapper`) with sticky positioning
3. The wrapper height should be large enough to allow the presenter to navigate all 6 tabs while anchored
4. Left/right arrow key navigation within the showcase overrides the presentation's view-jump behavior while the showcase is active
5. Scrolling past the wrapper exits the showcase and continues the presentation flow

## Future: Akka Specify Skill Integration

This showcase format can become a `specify:demo-showcase` skill that:

1. Introspects the generated project's component registry
2. Auto-populates the architecture tab from actual entity/workflow/view definitions
3. Runs a load test and populates the proof tab with real metrics
4. Generates the SVG architecture diagram from the component graph
5. Packages the showcase as a deployable HTML artifact alongside the application
