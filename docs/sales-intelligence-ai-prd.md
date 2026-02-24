# Sales Intelligence AI — Product Requirements Document (Working Draft)

## 1. Product Vision
Build an **AI-native business intelligence platform** that replaces traditional static dashboards with a conversational interface that can:

- Translate natural language into safe data queries.
- Compute sales KPIs deterministically (no model-side math).
- Explain trends, anomalies, and performance shifts.
- Provide decision-ready recommendations.
- Scale as a secure multi-tenant SaaS platform.

**North Star Experience:** users should feel like they are talking to a revenue analyst, not configuring dashboards.

---

## 2. Positioning

### Category
AI-Native Business Intelligence Platform

### Competitive Alternatives
- Tableau
- Power BI
- Looker

### Differentiators
- Conversation-first UX
- Deterministic KPI computation layer
- Built-in decision support
- SaaS-native multi-tenant architecture

---

## 3. Target Users

### Primary Users
- Sales Managers
- Revenue Operations teams
- Founders / Executives
- Growth teams

### Secondary Users
- Sales Representatives
- Finance Analysts
- Marketing Analysts

---

## 4. Problem Statement
Traditional BI tools are hard to adopt in revenue teams because they are often:
- Dashboard-first and setup-heavy
- SQL-dependent
- Static/reactive instead of contextual
- Training-intensive

Sales-focused teams need:
- Instant answers
- Explainable context
- Comparisons and trends
- Actionable recommendations

**Opportunity:** deliver an AI-native BI experience built specifically for revenue workflows.

---

## 5. Core Product Objectives
- Eliminate SQL dependency for business users.
- Provide accurate, data-backed answers only.
- Prevent hallucinated analytics through deterministic logic.
- Deliver executive-ready, concise insights.
- Support secure internal deployment and enterprise controls.
- Scale to multi-tenant SaaS workloads.

---

## 6. Functional Requirements

### 6.1 Conversational Interface
Users must be able to:
- Ask free-form questions
- Ask follow-up questions
- Compare segments
- Request trends
- Ask “why” questions

System must:
- Maintain session context
- Handle ambiguity
- Ask clarifying questions when required

### 6.2 NL → Query Engine
System must:
- Convert user input into **safe `SELECT` queries only**
- Restrict query generation to an allow-listed schema
- Reject destructive queries
- Validate query before execution
- Return structured output only

Required output format:

```json
{
  "intent": "",
  "query": ""
}
```

No reasoning text is allowed in this stage.

### 6.3 Deterministic KPI Engine
All KPIs must be computed in backend logic from executed query results (never model-side arithmetic).

Required KPIs:
- Total revenue
- Revenue by product
- Revenue by country
- Revenue by city
- Average deal size
- Monthly revenue trend
- Daily revenue
- Month-over-month growth
- Top customers by revenue
- Revenue concentration
- Product performance comparison

### 6.4 Insight Layer
After query execution, system must:
- Explain trends
- Highlight top performers
- Highlight underperformers
- Compute percentage changes
- Detect anomalies
- Produce executive-ready summaries

If data is insufficient, return exactly:

`Insufficient data.`

### 6.5 Visualization Recommendation
Auto-suggest visualization based on intent/result shape:
- Line chart for time trends
- Bar chart for comparisons
- Pie chart for distribution
- Table for granular breakdown

### 6.6 Mock Data Requirement (Development)
Generate a synthetic **1000-row** dataset with:
- `id`
- `name`
- `phone_number`
- `city`
- `country`
- `amount`
- `product`
- `per_price`
- `price` (`amount × per_price`)
- `date`

Dataset constraints:
- Multiple countries/cities/products
- Multi-month date range
- Realistic value distributions
- Consistent pricing logic

---

## 7. Non-Functional Requirements

### Accuracy
- Zero fabricated numbers
- All numeric outputs must originate from executed queries
- No simulated KPI outputs

### Security
- Read-only query enforcement
- Injection prevention
- Strict schema validation

### Performance
- Query response target: < 2 seconds
- Support concurrent users

### Scalability
- Multi-tenant SaaS architecture
- Tenant-level data isolation
- Role-based access controls

### Transparency
- Ability to display generated query to users/admins
- Clear indication of data source and period

---

## 8. System Architecture Overview

### Core Modules
1. Conversation Layer
2. Intent Detection
3. NL → Query Generator
4. Query Validator
5. Query Executor
6. Deterministic KPI Engine
7. Insight Generator
8. Visualization Recommender
9. Tenant & Access Manager

**Architecture principle:** strict separation of concerns across modules.

---

## 9. User Flows

### Flow 1 — Simple KPI
User: “What is total revenue?”
1. Generate query
2. Execute query
3. Compute KPI deterministically
4. Return insight
5. Recommend visualization

### Flow 2 — Comparison
User: “Compare revenue between Germany and France.”
1. Generate grouped query
2. Compute comparison
3. Calculate percentage difference
4. Return concise insight

### Flow 3 — Trend Analysis
User: “Show monthly revenue trend.”
1. Group by month
2. Compute trend
3. Calculate growth rates
4. Recommend line chart

### Flow 4 — Diagnostic
User: “Why did revenue drop?”
1. Compare current vs previous period
2. Identify contributing drivers
3. Explain likely factors from data

---

## 10. SaaS-Specific Requirements
- Tenant-level database separation
- Usage tracking
- Query logging
- Role-based permissions
- Subscription tiers
- Admin dashboard
- Data source connectors (future phase)

---

## 11. Risks and Mitigations
| Risk | Mitigation |
|---|---|
| Hallucinated analytics | Deterministic KPI engine |
| SQL injection | Strict query validation + read-only enforcement |
| Schema drift | Dynamic schema registry |
| Ambiguous prompts | Clarification workflow |
| Model inconsistency | Structured output contracts |

---

## 12. Success Metrics
- Query accuracy rate
- Insight usefulness score
- Average response time
- User retention
- Daily active users
- Reduction in manual dashboard usage

---

## 13. Roadmap

### Phase 1 — MVP
- Mock dataset
- Core KPIs
- NL → Query
- Insight explanation
- Basic visualization recommendations

### Phase 2 — Intelligence
- Anomaly detection
- Comparison engine
- What-if simulations

### Phase 3 — SaaS
- Multi-tenant architecture
- Role management
- Usage tracking
- Billing integration

### Phase 4 — Advanced
- Forecasting
- CRM integrations
- Real-time data
- Alerts & notifications

---

## Strategic Positioning
This product should become:

**Conversational BI + Sales Intelligence + AI Analyst**

Not just dashboards, but a reasoning and decision-support layer over business data.
