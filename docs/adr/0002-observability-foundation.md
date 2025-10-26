# ADR 0002: Observability Foundation

- Status: Accepted
- Deciders: Structure Steward Team
- Date: 2024-10-27

## Context

The prior implementation configured logging via `logging.basicConfig` directly
inside modules, producing plain-text logs without event identifiers or
consistent schema. This impeded ingestion by log aggregation systems and made it
impossible to correlate telemetry across services.

## Decision

- Adopt structured logging via module-level loggers with explicit event keys
  (e.g., `axiom_system.perform_inference`).
- Reserve JSON formatting and exporter integration for future phases, but ensure
  all logs include stable fields via the `extra` argument so they can be parsed.
- Require instrumentation of critical flows (policy updates, high-entropy
  inferences, reflection trail generation) using the structured logger.

## Consequences

- Log consumers can filter by `event` or `system` fields without string parsing.
- Adding OpenTelemetry exporters will not require code changes beyond handler
  configuration.
- Tests confirm timestamps are timezone-aware, preventing ambiguous auditing.
