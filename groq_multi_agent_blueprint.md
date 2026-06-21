# ClaimPilot AI — Multi-Agent Revenue Cycle Intelligence Platform

**Professional GenAI Engineer Portfolio Blueprint**  
**Target:** GenAI Engineer / AI Engineer / Applied AI Engineer roles  
**Primary LLM Provider:** Groq API  
**Implementation Style:** Phase-wise, test-first, deployment-ready

---

## 1. Project Summary

**ClaimPilot AI** is a production-style **multi-agent AI platform** for a real business problem: reducing revenue leakage and manual review time in healthcare-style claims / invoice exception workflows.

The system ingests claim-like records, policy/rule documents, denial reasons, historical resolution notes, and transaction metadata. A **supervisor agent** routes work to specialized agents that:

- classify claim issues,
- retrieve relevant policy/rule context,
- detect missing data,
- propose correction actions,
- estimate financial risk,
- generate a human-review summary, and
- produce an auditable resolution package.

This project is intentionally designed to look like a **serious AI engineering system**, not a toy chatbot. It demonstrates:

- multi-agent architecture,
- agent orchestration,
- tool use,
- retrieval and memory,
- structured outputs,
- asynchronous workflows,
- evaluation and observability,
- CI/CD and deployment discipline.

---

## 2. Why This Project Is Strong

Groq supports tool use and structured JSON outputs through its API, which makes it suitable for fast agentic workflows that need external functions and auditable outputs.[web:36] Groq also offers server-side agentic tool systems and very low-latency model execution, which makes it useful for production-style interactive agents.[web:36][web:42] Production multi-agent systems typically work best when specialized agents are coordinated by a centralized orchestrator with shared memory and auditable communication, especially in enterprise environments.[web:35][web:41] LangGraph is well-suited to stateful multi-agent workflows and commonly uses supervisor and subgraph patterns to orchestrate specialized agents in a controllable way.[web:34][web:40][web:46]

---

## 3. Real Business Problem

### Problem Statement

In revenue-cycle, claims-processing, and invoice-exception operations, organizations lose money because records are rejected, underpaid, or delayed due to missing documentation, coding inconsistencies, policy mismatches, duplicate submissions, and manual review bottlenecks.

These workflows are ideal for a multi-agent system because they require:

- document understanding,
- rule interpretation,
- retrieval from past cases,
- financial reasoning,
- recommendation generation,
- and a final auditable human-readable decision package.

### Why It Feels Real

This is not just “AI answers questions.” It is closer to a **workflow copilot for operations teams**:

- intake data comes from multiple systems,
- different specialists reason over different aspects,
- the orchestration layer combines outputs,
- and a final reviewer still approves the recommendation.

That is exactly the kind of engineered project that signals GenAI depth.

---

## 4. Product Concept

### Product Name

**ClaimPilot AI**

### One-Line Pitch

A multi-agent AI platform that triages claims/invoice exceptions, retrieves policy evidence, estimates denial risk, and drafts resolution recommendations with full auditability.

### Core User Personas

- **Operations Analyst** — needs fast triage and clear next actions
- **Revenue Cycle Specialist** — validates claim/payment issues and supporting evidence
- **Manager** — wants exception trends, financial risk, and team productivity insights
- **Compliance Reviewer** — needs traceable evidence and controllable outputs

### Business Outcome

- reduce manual review time,
- reduce leakage from unresolved claims,
- standardize recommendation quality,
- and create explainable decision support.

---

## 5. Multi-Agent Architecture

A supervisor model is a common production pattern in enterprise multi-agent systems because one orchestrating agent can route work to narrower specialists and maintain a clearer audit trail.[web:44][web:35] Specialized agents typically perform better when each is scoped to a narrow task and orchestrated as modular subgraphs rather than one monolithic agent trying to do everything.[web:40][web:46]

### High-Level Pattern

Use a **central supervisor + specialist subagents + critic/reviewer** architecture.

### Agent Roles

#### 1. Supervisor Agent
Responsible for:
- receiving the case,
- deciding which agents must run,
- maintaining workflow state,
- merging outputs,
- and escalating to human review when confidence is low.

#### 2. Intake Agent
Responsible for:
- normalizing incoming structured claim/invoice data,
- identifying missing fields,
- validating record shape,
- extracting case metadata.

#### 3. Policy Retrieval Agent
Responsible for:
- retrieving relevant policy, payer rule, SOP, and exception-handling guidance,
- ranking evidence chunks,
- attaching citations.

#### 4. Classification Agent
Responsible for:
- identifying issue category,
- mapping denial or exception reason,
- classifying the likely root cause.

#### 5. Financial Risk Agent
Responsible for:
- estimating lost revenue risk,
- prioritizing high-value cases,
- scoring urgency.

#### 6. Resolution Agent
Responsible for:
- generating recommended next actions,
- producing supporting rationale,
- proposing documentation or correction steps.

#### 7. Critic / QA Agent
Responsible for:
- verifying evidence alignment,
- checking JSON schema compliance,
- flagging hallucination risk,
- requiring re-run if outputs are weak.

#### 8. Reporting Agent
Responsible for:
- building the final human-readable summary,
- generating a case note,
- optionally producing email / Slack / PDF-friendly outputs.

---

## 6. Architecture Diagram

```text
┌────────────────────────────────────────────────────────────────────┐
│                        ClaimPilot AI                               │
├────────────────────────────────────────────────────────────────────┤
│ Frontend (Next.js)                                                 │
│  ├── Analyst Workbench                                             │
│  ├── Case Review Dashboard                                         │
│  ├── Trend & KPI Views                                             │
│  └── Evaluation Admin                                              │
│                 │                                                   │
│                 ▼                                                   │
│ Backend API (FastAPI)                                              │
│  ├── Auth / Sessions                                               │
│  ├── Case APIs                                                     │
│  ├── Agent Workflow APIs                                           │
│  ├── Eval APIs                                                     │
│  └── Observability APIs                                            │
│                 │                                                   │
│                 ▼                                                   │
│ LangGraph Orchestrator                                             │
│  ├── Supervisor Agent                                              │
│  ├── Intake Agent Subgraph                                         │
│  ├── Retrieval Agent Subgraph                                      │
│  ├── Classification Agent Subgraph                                 │
│  ├── Financial Risk Agent Subgraph                                 │
│  ├── Resolution Agent Subgraph                                     │
│  ├── Critic Agent Subgraph                                         │
│  └── Reporting Agent Subgraph                                      │
│                 │                                                   │
│                 ▼                                                   │
│ Shared Services                                                    │
│  ├── Groq LLM Service                                              │
│  ├── Retrieval Service                                             │
│  ├── Rules Engine                                                  │
│  ├── Case Memory Store                                             │
│  ├── Audit/Event Logger                                            │
│  └── Evaluation Engine                                             │
│                 │                                                   │
│                 ▼                                                   │
│ Data Layer                                                         │
│  ├── PostgreSQL                                                    │
│  ├── Redis                                                         │
│  ├── Qdrant                                                        │
│  ├── Object Storage (MinIO/S3)                                     │
│  └── Seeded Business Datasets                                      │
└────────────────────────────────────────────────────────────────────┘
```

---

## 7. Recommended Stack

| Layer | Technology | Why |
|---|---|---|
| LLM Inference | **Groq API** | Fast low-latency tool-friendly inference [web:36][web:42] |
| Agent Orchestration | **LangGraph** | Stateful supervisor + subgraph orchestration [web:34][web:46] |
| Agent Toolkit | LangChain + Pydantic | Tool definitions and structured schemas |
| Backend | FastAPI | Async APIs and workflow endpoints |
| Frontend | Next.js 14 + TypeScript + Tailwind | Professional analyst UI |
| Vector Store | Qdrant | Retrieval for policy docs and prior resolutions |
| Database | PostgreSQL | Cases, workflows, audits, evaluations |
| Cache/Queue | Redis | State cache, rate limiting, async coordination |
| Blob Store | MinIO or S3 | Uploaded files and report artifacts |
| Background Jobs | Celery or Arq | Long-running case processing |
| Observability | Langfuse / OpenTelemetry / Phoenix | Traces, prompts, latency, evals |
| Testing | pytest, pytest-asyncio, Playwright | Backend + workflow + E2E validation |
| CI/CD | GitHub Actions | Build, lint, test, deploy |
| Deployment | Railway/Render + Vercel | Fast portfolio deployment |

---

## 8. Core Features

### Case Triage
- Upload or create a claim/invoice exception case
- Parse structured fields and supporting docs
- Identify missing fields and inconsistencies

### Policy-Aware Retrieval
- Retrieve payer policy / business rules / SOPs
- Return evidence chunks with similarity scores
- Link evidence to every recommendation

### Multi-Agent Resolution Flow
- Supervisor routes work across agents
- Each agent returns structured outputs
- Critic agent validates before final result

### Financial Prioritization
- Estimate risk amount or expected leakage
- Prioritize queue by urgency and value

### Human Review Package
- Final recommendation summary
- Root cause category
- Confidence score
- Required next actions
- Evidence references

### Analytics
- Top denial/exception categories
- Revenue at risk by queue
- Agent confidence distribution
- Reviewer override patterns

---

## 9. Data Model

### PostgreSQL Tables

- `users`
- `cases`
- `case_documents`
- `case_events`
- `workflow_runs`
- `agent_runs`
- `agent_messages`
- `policy_chunks`
- `resolution_suggestions`
- `review_outcomes`
- `audit_logs`
- `eval_cases`
- `eval_results`

### Why This Matters

A strong GenAI engineering project should show not just prompting, but **state, workflow traceability, reproducibility, and evaluation**.

---

## 10. Project Structure

```text
claimpilot-ai/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── backend-deploy.yml
│       └── frontend-deploy.yml
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── cases.py
│   │   │   ├── workflows.py
│   │   │   ├── analytics.py
│   │   │   ├── evaluations.py
│   │   │   └── health.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   └── telemetry.py
│   │   ├── services/
│   │   │   ├── groq_service.py
│   │   │   ├── retrieval_service.py
│   │   │   ├── rules_service.py
│   │   │   ├── case_service.py
│   │   │   ├── evaluation_service.py
│   │   │   └── artifact_service.py
│   │   ├── models/
│   │   ├── schemas/
│   │   └── repositories/
│   ├── tests/
│   │   ├── test_cases_api.py
│   │   ├── test_retrieval_service.py
│   │   ├── test_workflow_graph.py
│   │   └── test_eval_pipeline.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── agents/
│   ├── supervisor/
│   │   └── graph.py
│   ├── intake/
│   │   ├── agent.py
│   │   └── prompts.py
│   ├── retrieval/
│   │   ├── agent.py
│   │   └── prompts.py
│   ├── classification/
│   │   ├── agent.py
│   │   └── prompts.py
│   ├── financial_risk/
│   │   ├── agent.py
│   │   └── prompts.py
│   ├── resolution/
│   │   ├── agent.py
│   │   └── prompts.py
│   ├── critic/
│   │   ├── agent.py
│   │   └── prompts.py
│   └── reporting/
│       ├── agent.py
│       └── prompts.py
│
├── graph/
│   ├── state.py
│   ├── router.py
│   ├── edges.py
│   └── schemas.py
│
├── tools/
│   ├── fetch_case_history.py
│   ├── retrieve_policy_evidence.py
│   ├── estimate_financial_risk.py
│   ├── validate_required_fields.py
│   ├── save_resolution_note.py
│   └── compute_case_priority.py
│
├── ingestion/
│   ├── load_policies.py
│   ├── load_case_history.py
│   └── chunk_and_embed.py
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── lib/
│   ├── package.json
│   └── Dockerfile
│
├── infra/
│   ├── docker-compose.yml
│   ├── seed/
│   │   ├── sample_cases.csv
│   │   ├── policies/
│   │   └── historical_notes/
│   └── scripts/
│
├── docs/
│   ├── architecture.md
│   ├── evaluation-plan.md
│   ├── loom-demo-script.md
│   └── phase-commit-plan.md
│
├── .env.example
└── README.md
```

---

## 11. Multi-Agent Workflow Design

### Orchestration Pattern

Use a **supervisor pattern** with subgraphs for each agent role. LangGraph’s supervisor and subgraph patterns are commonly used for stateful multi-agent orchestration because they keep each specialist module isolated while the parent graph controls routing and state transitions.[web:34][web:46]

### Workflow State Example

```python
from typing import TypedDict, List, Dict, Optional

class CaseState(TypedDict):
    case_id: str
    user_id: str
    raw_case: Dict
    normalized_case: Dict
    missing_fields: List[str]
    issue_category: Optional[str]
    retrieved_evidence: List[Dict]
    financial_risk_score: Optional[float]
    recommended_actions: List[str]
    critic_flags: List[str]
    final_summary: Optional[str]
    status: str
    trace_id: str
```

### Workflow Steps

1. Intake validation
2. Entity normalization
3. Policy retrieval
4. Case classification
5. Financial prioritization
6. Resolution proposal
7. Critic review
8. Report generation
9. Human approval or escalation

### Escalation Logic

Escalate to human review when:
- confidence falls below threshold,
- critic flags evidence mismatch,
- required fields remain unresolved,
- financial risk exceeds threshold,
- or policy retrieval is weak.

---

## 12. Groq Integration Strategy

Groq supports tool use and structured outputs, which makes it well-suited for typed agent responses and function-like workflows.[web:36] Groq also offers built-in server-side tools and agentic systems, but for this project you should implement your own application-level orchestration so the architecture is visible in code and easier to explain in interviews.[web:42][web:39]

### Recommended Usage

- Use **Groq** for all agent reasoning layers
- Use **structured JSON outputs** with Pydantic validation
- Use **tool calls** for retrieval, validation, and calculations
- Keep orchestration in **LangGraph**, not hidden in a managed black box

### Suggested Models

- Primary fast reasoning model for agents: use a Groq-hosted strong instruct model available in your account
- Optional alternate model for critic or summarization phases
- Keep model names configurable via env vars

### `groq_service.py` Responsibilities

- centralize API client setup
- handle retries and timeouts
- enforce response schemas
- log token usage and latency
- expose `invoke_structured()` and `invoke_text()` helpers

---

## 13. Retrieval Architecture

### What to Retrieve

- policy documents
- payer/client business rules
- historical resolved cases
- denial reason mappings
- SOP/runbook content

### Retrieval Design

- chunk docs into 400–800 token segments
- store embeddings in Qdrant
- add metadata: payer, plan, rule type, issue category, date
- retrieve top-k evidence with metadata filters
- rerank before passing to downstream agents

### Retrieval Output Shape

```json
[
  {
    "chunk_id": "policy_102_4",
    "source": "policy_manual_2026_q1.pdf",
    "score": 0.89,
    "category": "authorization_rule",
    "text": "Claims over $5,000 require prior authorization..."
  }
]
```

---

## 14. Tools Design

Structured messages and tool-enabled workflows are critical in production multi-agent systems because every handoff and action needs to be inspectable and auditable.[web:35][web:37]

### Tool List

| Tool | Purpose | Input | Output |
|---|---|---|---|
| `validate_required_fields` | Detect missing mandatory case fields | case JSON | missing fields list |
| `retrieve_policy_evidence` | Fetch policy/rule chunks | case context | ranked evidence |
| `fetch_case_history` | Find similar historical cases | case metadata | prior case list |
| `estimate_financial_risk` | Calculate revenue impact | case values | risk score |
| `compute_case_priority` | Assign queue priority | risk + SLA + denial type | priority band |
| `save_resolution_note` | Persist final recommendation | summary + refs | DB confirmation |

### Tool Rules

- tools must return typed JSON
- each tool call must be logged
- failed tools must produce recoverable error objects
- agents should not perform hidden calculations outside tools when deterministic logic is available

---

## 15. API Design

### Core Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | health check |
| `/cases` | POST | create a new case |
| `/cases/{id}` | GET | fetch case details |
| `/cases/{id}/run` | POST | run multi-agent workflow |
| `/cases/{id}/summary` | GET | final recommendation package |
| `/analytics/overview` | GET | KPI dashboard data |
| `/eval/run` | POST | run evaluation suite |
| `/workflow-runs/{id}` | GET | workflow trace |

### Example Case Input

```json
{
  "claim_id": "CLM-100245",
  "payer": "Aetna",
  "amount": 8200.45,
  "denial_reason": "Missing authorization",
  "procedure_code": "99285",
  "diagnosis_code": "J18.9",
  "member_plan": "PPO Gold",
  "notes": "Resubmission requested after denial.",
  "attachments": ["auth_letter.pdf", "visit_summary.pdf"]
}
```

### Example Final Output

```json
{
  "case_id": "case_1024",
  "issue_category": "authorization_gap",
  "financial_risk_score": 0.87,
  "priority": "high",
  "recommended_actions": [
    "Attach prior authorization letter",
    "Resubmit corrected claim within payer SLA",
    "Review coding/document linkage before submission"
  ],
  "evidence_refs": [
    "policy_102_4",
    "history_88",
    "rule_14"
  ],
  "critic_status": "pass",
  "summary": "This claim was likely denied due to a missing prior authorization artifact despite supporting encounter documentation."
}
```

---

## 16. Phase-Wise Implementation Plan

## Phase 1 — Foundation Setup
**Goal:** Create the repo, local infra, and backend skeleton.

### Tasks
- create GitHub repo manually
- scaffold backend, frontend, agents, graph, tools, infra, docs
- create Docker Compose for PostgreSQL, Redis, Qdrant, MinIO
- add FastAPI app with `/health`
- create `.env.example`
- commit clean base structure

### Tests Before Commit
- `pytest` minimal app test passes
- Docker services start cleanly
- `/health` returns success

### Commit Suggestion
`chore: scaffold project structure and local infrastructure`

---

## Phase 2 — Data Ingestion + Retrieval Base
**Goal:** Load policy docs and historical cases into retrieval storage.

### Tasks
- build ingestion scripts
- chunk and embed documents
- load into Qdrant
- add retrieval service with metadata filters
- seed sample business data

### Tests Before Commit
- retrieval returns top-k relevant chunks
- metadata filtering works
- ingestion script is idempotent

### Commit Suggestion
`feat: implement policy and case-history ingestion with vector retrieval`

---

## Phase 3 — Groq Client + Structured Output Layer
**Goal:** Add professional LLM abstraction.

### Tasks
- build `groq_service.py`
- add structured response schemas with Pydantic
- add retries, timeouts, token/latency logging
- implement `invoke_structured()` helper
- add unit tests with mocked Groq responses

### Tests Before Commit
- valid JSON maps to schema
- invalid JSON fails gracefully
- timeout/retry behavior works

### Commit Suggestion
`feat: add Groq client abstraction with schema-validated outputs`

---

## Phase 4 — Single-Agent Baseline
**Goal:** Build one end-to-end baseline before going multi-agent.

### Tasks
- create single workflow for case triage
- combine retrieval + reasoning + recommendation
- return structured final output
- store workflow run and audit logs

### Why This Phase Matters
You should prove the business workflow works in a simpler form before adding orchestration complexity.

### Tests Before Commit
- one sample case resolves end-to-end
- outputs contain evidence refs
- audit logs are written

### Commit Suggestion
`feat: build baseline single-agent claim triage workflow`

---

## Phase 5 — Multi-Agent Supervisor Graph
**Goal:** Replace baseline with supervisor + specialist agents.

### Tasks
- build supervisor graph
- implement Intake, Retrieval, Classification, Risk, Resolution agents
- define graph state and transitions
- add critic agent for validation
- persist per-agent traces

### Tests Before Commit
- graph completes for known happy path
- route selection is deterministic for test fixtures
- critic blocks bad outputs
- failure recovery path works

### Commit Suggestion
`feat: implement LangGraph supervisor workflow with specialist agents`

---

## Phase 6 — Backend APIs + Review Workflow
**Goal:** Expose the system through clean APIs.

### Tasks
- build cases API
- build workflow run API
- add final summary endpoint
- add human-review status update endpoint
- add pagination and filtering

### Tests Before Commit
- API contract tests pass
- invalid case payloads are rejected
- completed runs return full structured output

### Commit Suggestion
`feat: expose multi-agent workflow through review-ready backend APIs`

---

## Phase 7 — Frontend Analyst Workbench
**Goal:** Build a serious product interface.

### Tasks
- create dashboard
- create case detail screen
- create workflow trace viewer
- show evidence drawer and agent steps
- show confidence and critic status
- add analytics overview

### Tests Before Commit
- Playwright smoke tests pass
- major screens render on desktop/mobile
- evidence viewer loads correctly

### Commit Suggestion
`feat: build analyst workbench with workflow trace and evidence views`

---

## Phase 8 — Evaluation and Guardrails
**Goal:** Make the system trustworthy and measurable.

### Tasks
- create evaluation dataset with expected outputs
- add grounding checks
- add tool usage checks
- measure route accuracy, resolution quality, latency
- add prompt/agent regression tests

### Evaluation Metrics
- grounding score
- issue classification accuracy
- critic rejection rate
- financial prioritization agreement
- end-to-end latency

### Tests Before Commit
- evaluation suite runs locally
- outputs are versioned
- regression cases fail when quality drops

### Commit Suggestion
`feat: add evaluation harness and guardrail checks for agent workflows`

---

## Phase 9 — Observability + Deployment
**Goal:** Ship the app like a professional engineer.

### Tasks
- integrate tracing (Langfuse/OpenTelemetry/Phoenix)
- add workflow dashboards
- containerize services
- deploy backend and frontend
- add production env config
- record Loom demo

### Tests Before Commit
- deployment build passes
- environment variables validated on startup
- production health checks pass

### Commit Suggestion
`chore: add observability, deployment configuration, and release readiness`

---

## 17. Testing Strategy

### Unit Tests
- tool functions
- Groq client parsing
- schema validation
- priority calculation
- risk scoring logic

### Integration Tests
- retrieval service + Qdrant
- workflow graph happy path
- workflow graph failure path
- DB persistence of workflow runs

### Contract Tests
- API request/response schema checks
- frontend/backend integration assumptions

### Evaluation Tests
- known labeled cases
- grounding requirements
- evidence citation presence

### E2E Tests
- create case → run workflow → review result
- open evidence drawer → inspect trace → approve/reject recommendation

---

## 18. GitHub Actions

### `ci.yml`

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  backend-test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: claimpilot_test
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports: ["6379:6379"]

      qdrant:
        image: qdrant/qdrant:latest
        ports: ["6333:6333"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip

      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install pytest pytest-asyncio ruff mypy httpx

      - name: Ruff
        run: ruff check backend agents graph tools ingestion

      - name: Mypy
        run: mypy backend/app agents graph tools --ignore-missing-imports

      - name: Run backend tests
        env:
          DATABASE_URL: postgresql+psycopg://test:test@localhost:5432/claimpilot_test
          REDIS_URL: redis://localhost:6379
          QDRANT_URL: http://localhost:6333
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          APP_ENV: test
          JWT_SECRET: test-secret
        run: pytest -q

  frontend-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
          cache-dependency-path: frontend/package-lock.json

      - name: Install deps
        run: cd frontend && npm ci

      - name: Lint
        run: cd frontend && npm run lint

      - name: Build
        run: cd frontend && npm run build
        env:
          NEXT_PUBLIC_API_URL: http://localhost:8000
```

### Optional `backend-deploy.yml`

```yaml
name: Deploy Backend

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'
      - 'agents/**'
      - 'graph/**'
      - 'tools/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Railway
        run: echo "Deploy command here"
```

---

## 19. Required Environment Variables

```bash
APP_ENV=development
DATABASE_URL=postgresql+psycopg://claimpilot:secret@localhost:5432/claimpilot_db
REDIS_URL=redis://localhost:6379
QDRANT_URL=http://localhost:6333
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL_PRIMARY=your_primary_model_name
GROQ_MODEL_CRITIC=your_critic_model_name
JWT_SECRET=change-this
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 20. Suggested Backend Dependencies

```txt
fastapi
uvicorn[standard]
sqlalchemy
psycopg[binary]
alembic
pydantic
pydantic-settings
redis
qdrant-client
langchain
langgraph
groq
python-multipart
minio
httpx
orjson
pytest
pytest-asyncio
mypy
ruff
```

### Suggested Frontend Dependencies

```json
{
  "dependencies": {
    "next": "14.x",
    "react": "18.x",
    "react-dom": "18.x",
    "typescript": "5.x",
    "tailwindcss": "3.x",
    "axios": "latest",
    "@tanstack/react-query": "latest",
    "zustand": "latest",
    "recharts": "latest",
    "lucide-react": "latest"
  }
}
```

---

## 21. README Sections You Should Include

- project overview
- business problem
- multi-agent architecture diagram
- stack overview
- local setup
- seeded demo dataset
- evaluation approach
- screenshots
- Loom video
- future improvements

---

## 22. Loom Demo Script

### 5–7 Minute Flow

1. Introduce the business problem
2. Upload or open a seeded high-value denied claim
3. Run the workflow
4. Show supervisor and specialist agent steps
5. Open evidence drawer and policy matches
6. Show critic validation and confidence
7. Show final recommendation package
8. Show analytics dashboard
9. Show GitHub Actions and test suite

### What Reviewers Will Notice

- modular multi-agent design
- business relevance
- evidence-backed outputs
- professional workflow traces
- deployment and testing maturity

---

## 23. ATS-Optimized Resume Bullets

- Engineered a **multi-agent AI workflow platform** using Groq, LangGraph, FastAPI, and Qdrant to automate policy-aware claims exception triage and recommendation generation
- Designed a **supervisor-based agent architecture** with specialized Intake, Retrieval, Classification, Risk, Resolution, and Critic agents to produce auditable, structured outputs
- Built a **retrieval-grounded decision support system** with vector search, policy evidence linking, workflow tracing, evaluation harnesses, and CI/CD for production-style AI engineering
- Delivered a **full-stack GenAI application** with analyst dashboards, workflow inspection, human-review APIs, Dockerized infrastructure, and GitHub Actions-based quality gates

---

## 24. Recommended Build Order

1. Foundation
2. Retrieval
3. Groq service
4. Single-agent baseline
5. Multi-agent graph
6. APIs
7. Frontend
8. Evaluation
9. Deployment

This order keeps the project understandable, testable, and always demoable.

---

## 25. Gemini CLI Prompting Plan

Use this blueprint phase by phase with Gemini CLI.

```bash
gemini "Implement Phase 1 of ClaimPilot AI. Create the repo structure, docker-compose, FastAPI health endpoint, and environment config."

gemini "Implement Phase 2 of ClaimPilot AI. Build ingestion scripts, chunk policy docs, and load retrieval data into Qdrant."

gemini "Implement Phase 3 of ClaimPilot AI. Build groq_service.py with structured schema outputs, retry handling, and tests."

gemini "Implement Phase 4 of ClaimPilot AI. Build the baseline single-agent triage workflow using Groq and retrieval."

gemini "Implement Phase 5 of ClaimPilot AI using LangGraph. Add a supervisor graph and specialist agents for intake, retrieval, classification, risk, resolution, and critic validation."

gemini "Implement Phase 7 frontend for ClaimPilot AI. Build the analyst dashboard, case detail screen, workflow trace viewer, and evidence drawer."
```

---

## 26. Final Recommendation

If your goal is to stand out for a **GenAI Engineer** role, this is a strong flagship project because it demonstrates specialized agents, orchestration, retrieval, structured tool use, business relevance, testing discipline, and production-minded implementation. Multi-agent systems in production tend to work best when specialists are tightly scoped, orchestration is centralized, and every handoff is observable and auditable, which is exactly the pattern this blueprint follows.[web:35][web:41][web:46]
