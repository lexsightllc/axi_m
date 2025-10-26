# AXIΩM Ontological Framework

The AXIΩM Ontological Framework is a Python-first research codebase that models
constraint-governed artificial intelligence governance. The repository now uses a
standardized, automation-friendly layout so that contributors can bootstrap a
development workstation, run a comprehensive quality gate locally, and produce
reproducible artifacts without bespoke knowledge.

## Repository Topology

```
.
├── assets/                     # Design assets, diagrams, exported imagery
├── ci/                         # Local CI harnesses and shared workflow snippets
├── configs/                    # Static configuration files consumed by tooling
├── data/                       # Version-controlled datasets and domain samples
├── docs/                       # Living documentation, ADRs, and reference guides
├── infra/                      # Infrastructure-as-code manifests and IaC scripts
├── sbom/                       # Generated Software Bills of Materials
├── scripts/                    # Cross-platform developer task shims
├── src/                        # First-party Python packages (src layout)
├── tests/                      # Unit, integration, and end-to-end suites
└── .github/workflows/          # CI/CD pipelines
```

Legacy artifacts that predate this consolidation live under `docs/legacy/` for
historical reference. They are not executed as part of the modern toolchain but
their concepts inform the documented architecture decisions.

## Developer Tasks

All repeatable tasks are exposed through the `scripts/` toolbelt and mirrored as
`make` targets. Each script is non-interactive, honours environment variables,
and exits with a non-zero code on failure. Use them directly or through `make`:

| Command | Description |
| --- | --- |
| `./scripts/bootstrap` | Provision `.venv`, install Python & Node tooling, set git hooks, and prime caches. |
| `./scripts/dev` | Launch a watch-mode feedback loop (`ptw` when available, otherwise `pytest`). |
| `./scripts/lint` | Run Ruff checks (with `--fix` optionally enabling autofix) across `src/` and `tests/`. |
| `./scripts/fmt` | Apply `ruff format`, `black`, and `isort` to the Python tree. |
| `./scripts/typecheck` | Execute `mypy` in strict mode against `src/` and tests. |
| `./scripts/test` | Run unit and integration suites with coverage reporting. |
| `./scripts/e2e` | Execute end-to-end scenarios under `tests/e2e/` when present. |
| `./scripts/coverage` | Produce coverage reports and enforce threshold gates. |
| `./scripts/build` | Produce source and wheel distributions via `python -m build`. |
| `./scripts/package` | Alias for `build`, reserved for packaging workflows. |
| `./scripts/release` | Drive semantic version bumping, changelog updates, and tag creation. |
| `./scripts/update-deps` | Regenerate dependency locks using pip-tools. |
| `./scripts/security-scan` | Run Bandit and pip-audit; integrates additional scanners when available. |
| `./scripts/sbom` | Emit a CycloneDX SBOM into `sbom/`. |
| `./scripts/gen-docs` | Build the MkDocs documentation site into `site/`. |
| `./scripts/migrate` | Run schema migrations (no-ops until migration tooling is introduced). |
| `./scripts/clean` | Remove caches, build artefacts, and temporary files. |
| `./scripts/check` | Orchestrate lint, typecheck, tests, coverage, and security gates locally. |

Example usage:

```bash
make bootstrap
make check
```

### Environment Variables

Create a local `.env` from `.env.example` and export variables before invoking
scripts. `PYTHONPATH` is set to `src/` by default so tooling resolves the
package layout without manual configuration.

## Observability and Telemetry

The Python package now emits structured logging through the standard library’s
logging API. All log statements include machine-parseable event identifiers so
metrics pipelines (e.g., OpenTelemetry processors) can attach metrics or traces.
Future instrumentation work will surface application metrics via Prometheus
exporters and propagate trace context in API boundaries as services emerge.

## Documentation

MkDocs powers the documentation site. Architecture Decision Records (ADRs) live
under `docs/adr/` and are versioned alongside code. Run `./scripts/gen-docs` to
rebuild documentation locally.

## Contribution Expectations

See [CONTRIBUTING.md](CONTRIBUTING.md) for the review workflow, coding
standards, commit conventions, and branch policies. All contributions must pass
`make check` before submission and follow Conventional Commit messages, which
are enforced by the commit template and commitlint hook installed by
`scripts/bootstrap`.

## Licensing

This project is licensed under the Apache License, Version 2.0. Historical
artifacts in `docs/legacy/` retain their original licensing and should be
consulted before reuse.
