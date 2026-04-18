# Enterprise QA & Release Strategy
## Version 1.0 — April 2026
**Living document** — update this file whenever we change testing policy or add new use cases.

## 1. Core Philosophy (Nexla LLM Evaluation Best Practices)

We follow the key principles from Nexla’s “LLM Evaluation: Key Concepts & Best Practices”:

> “LLM evaluation is a structured process that assesses an LLM’s performance across various tasks and capabilities… The goal is to validate whether it meets the requirements of a **specific use case**.”

**Key Nexla principles we enforce:**
- Evaluation must be **use-case focused** (not generic benchmarks).
- We use **multiple metrics** together (never rely on one metric alone).
- Every metric has a **minimum threshold** required for release.
- Human review is still required for high-risk changes (we are not 100% automated yet).

## 2. Our Specific Use Cases (This is what makes our evaluation unique)

All LLM tests in `tests/llm/` **must** map to one of these use cases:

### Use Case 1: Revenue Analysis & Executive Summarization
- **Description**: User asks questions about revenue data. LLM must analyze, summarize, and recommend actions.
- **Success criteria**:
  - Numbers must be 100% faithful to source data (no hallucination).
  - Output must be concise, actionable, and include clear recommendations.
- **Metrics we will enforce**: Hallucination, Answer Relevancy, G-Eval (custom business criteria), Faithfulness.

### Use Case 2: Agent Tool Orchestration / Autonomous Execution
- **Description**: User gives a business goal. Agent must choose correct tools, call them in the right order, and complete the task.
- **Success criteria**:
  - Correct tool selection.
  - Successful end-to-end task completion.
  - Structured output (JSON) when required.
- **Metrics we will enforce**: Tool Correctness, Task Completion, JSON Correctness.

### Use Case 3: Structured Data Output (JSON mode)
- **Description**: Any request that must return machine-readable data for downstream systems.
- **Success criteria**: Output must be valid JSON matching our exact schema.
- **Metrics we will enforce**: JSON Correctness + Faithfulness.

### Use Case 4: Consistency & Reliability
- **Description**: Same input must produce statistically similar outputs across multiple runs.
- **Metrics we will enforce**: Consistency score (custom).

## 3. Testing Pyramid & CI/CD Quality Gates

| Stage                  | What runs                          | When it runs          | Must pass for next stage? | Thresholds defined in |
|------------------------|------------------------------------|-----------------------|---------------------------|-----------------------|
| Code Quality           | Unit tests, lint, type check       | Every PR              | Yes                       | tests/unit/           |
| Feature + LLM Evals    | All LLM metrics + feature tests    | PR + main branch      | Yes                       | tests/llm/            |
| UI/UX                  | Playwright visual + accessibility  | main branch only      | Yes                       | tests/ui_ux/          |
| Release                | Canary / blue-green deployment     | Manual approval       | —                         | scripts/release/      |

**LLM Evaluation Rule**:  
A release is blocked if **any** use-case metric falls below its threshold.

## 4. Current LLM Metrics & Thresholds (we will implement one by one)

We will add these metrics step-by-step (following Nexla recommendation to use multiple metrics).

| Metric                  | Use Case                  | Threshold | Why it matters (Nexla)                  | Test file (future)                  |
|-------------------------|---------------------------|-----------|-----------------------------------------|-------------------------------------|
| Answer Relevancy        | All                       | ≥ 0.90    | Prevents off-topic or rambling answers  | tests/llm/relevancy/                |
| Hallucination           | Revenue Analysis          | ≤ 0.05    | No invented numbers                     | tests/llm/hallucination/            |
| Faithfulness            | All                       | ≥ 0.95    | Answer must be grounded in context      | tests/llm/faithfulness/             |
| Tool Correctness        | Agent Orchestration       | 1.0       | Agent must pick right tool              | tests/llm/agent/                    |
| G-Eval (Custom)         | Revenue Analysis          | ≥ 0.85    | Business-specific quality (actionable?) | tests/llm/geval/                    |
| JSON Correctness        | Structured Output         | 1.0       | Downstream systems must consume output  | tests/llm/json/                     |

## 5. Release Process (High-Level Flow)

1. Developer opens PR → Code quality gates run.
2. PR merged to `main` → Full LLM evaluation runs automatically.
3. All LLM metrics pass → UI/UX tests run.
4. All tests pass → Manual approval (GitHub Environment) → Canary release to staging.
5. Monitoring in staging (24h) → Production rollout (feature flags enabled).

**Rollback policy**: Any production incident triggers immediate rollback + post-mortem that updates this strategy document.

## 6. How to Update This Document
- When we add a new use case → update Section 2.
- When we change a threshold → update Section 4 and the test code.
- After every major release → review this file.

**Last updated**: [Insert date when you commit]
**Owner**: QA Engineer (you)
