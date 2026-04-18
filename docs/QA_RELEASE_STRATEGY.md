# QA & Release Strategy for Enterprise AI Platform
## Core Principle #1: Use-Case-Focused LLM Evaluation (Nexla Best Practice)

**Directly from Nexla LLM Evaluation Guide:**
> "LLM evaluation must be done for a specific use case."

### Why This Principle Exists
- Generic benchmarks (MMLU, GLUE, HELM) only tell you the model is "smart".
- Our platform requires the LLM to perform **autonomous execution** on revenue intelligence, data orchestration, and agent workflows.
- A model that excels at creative writing can still hallucinate numbers or pick wrong tools — which would be catastrophic in enterprise software.

### How We Apply This in Our QA Framework
Every LLM test in `tests/llm/` **must** be tied to one of our defined use cases below.

### Our Specific Use Cases (Define Yours Here)
1. **Revenue Analysis & Executive Summarization**  
   - Input: Raw revenue data + user question  
   - Expected: Accurate numbers, clear insights, actionable recommendations  
   - Metrics we will enforce: Faithfulness (no hallucination), Answer Relevancy, Task Completion

2. **Agent Tool Orchestration / Autonomous Execution**  
   - Input: Business request  
   - Expected: Correct tool selection + successful task completion  
   - Metrics: Tool Correctness, Task Completion, JSON correctness (for tool outputs)

3. **Structured Data Output (JSON mode)**  
   - Input: Any request that needs machine-readable output  
   - Expected: Valid JSON matching our schema  
   - Metric: JSON Correctness

4. **Consistency in High-Stakes Queries**  
   - Same input must produce statistically identical outputs across runs.

### Release Gates
- PR → Only unit tests
- Main branch → Full LLM evaluation using the metrics above
- Release to production only if **all use-case metrics pass their thresholds**

We will implement one metric per learning step (starting with Answer Relevancy in Step 4.2).

This document is the single source of truth for every release decision.
