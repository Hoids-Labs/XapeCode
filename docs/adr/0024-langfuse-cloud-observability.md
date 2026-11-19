# 0024. Langfuse Cloud tracing and evaluation scores

**Status:** Accepted
**Date:** 2026-11-12

## Context

Runtime traces, evaluation datasets, experiments, regression suites, and trace mining need one
observability platform. Langfuse provides tracing, evaluation orchestration, and score reporting.
Tracing must remain optional, preserve the current agent behavior when disabled, and avoid changing
the process-global OpenTelemetry environment used by other integrations.

## Decision

1. **Langfuse Cloud owns runtime traces.** When both `LANGFUSE_PUBLIC_KEY` and
   `LANGFUSE_SECRET_KEY` are configured, `init_tracing()` instruments pydantic-ai through logfire
   and exports OTLP spans to the configured `LANGFUSE_BASE_URL` (`LANGFUSE_HOST` remains a
   compatibility alias). The exporter uses Langfuse's Basic
   authentication and real-time ingestion header.
2. **Trace grouping follows xape sessions.** REPL turns and headless runs propagate the xape
   session id, trace metadata, input, and output using Langfuse's supported OTEL attributes.
3. **Langfuse owns evaluation orchestration.** Datasets, experiments, regression workflows, and
   trace mining use Langfuse. After evaluation, numeric scores are attached to the corresponding
   Langfuse sessions when Langfuse credentials are configured.
4. **No credentials means no reporting.** With neither Langfuse key set, tracing remains a no-op
   and evaluation commands report that Langfuse score reporting was skipped. Supplying only one key
   is an explicit configuration error.
5. **Credentials remain in Settings.** The OTLP exporter and score client are configured directly
   from `Settings`; global `OTEL_*` variables are not modified. Logfire's default scrubbing remains
   enabled; only the opaque `session.id` attribute is exempted so Langfuse can group xape sessions.

## Consequences

- Runtime traces, datasets, experiments, and numeric evaluation scores share Langfuse.
- Langfuse tracing is activated by both API keys. Commands that require Langfuse explicitly report
  missing credentials rather than pretending to publish results.
- Trace metadata uses Langfuse's trace metadata convention, including the shared xape session id
  used to join evaluation runs and Kitaru recordings.
- Langfuse is a runtime dependency shared by the top-level evals package.
