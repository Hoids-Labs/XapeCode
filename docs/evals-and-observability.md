# Evaluations & Observability

`xape` includes native instrumentation for distributed tracing, cost monitoring, and benchmark evaluations via [Langfuse](https://langfuse.com).

---

## 1. Live Session Tracing with Langfuse

Every prompt leg, tool call, subagent fan-out, and context compaction can be traced directly into Langfuse Cloud or a self-hosted instance.

### Configuration
Set your project credentials in `.env`:
```ini
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

### Trace Contents
* **Root Spans:** Grouped by session ID (`xape/<session-id>`).
* **Tool Call Spans:** Detailed input arguments, outputs, execution latencies, and exit codes.
* **Token Usage & Costs:** Exact input, output, and cache read tokens recorded per leg.

---

## 2. Benchmark Suite (Terminal-Bench Layout)

The evaluation suite runs realistic developer tasks against pristine checkouts to score agent problem-solving capabilities without human supervision.

### Run Benchmark Tasks
```bash
# Run all benchmark tasks
make eval-benchmark

# Run a specific difficulty tier
uv run python -m evals benchmark --difficulty easy

# Limit trials and concurrency
uv run python -m evals benchmark --trials 3 --threads 4
```

### Task Structure
Each benchmark task under `evals/benchmark/tasks/` contains:
* `instruction.md`: The developer prompt fed to the agent.
* `environment/`: Seed codebase.
* `tests/test.sh`: Automated verifier script that evaluates the outcome and outputs `reward.txt` (`1` for pass, `0` for fail).
* `solution/solve.sh`: Canonical reference implementation.

---

## 3. Regression Datasets

To prevent regressions in agent behaviors (e.g., tool-calling discipline, context compaction preservation):

```bash
# Run deterministic regression cases
make eval-regression-dataset

# Run natural-language judged regression suite
make eval-regression-suite
```

