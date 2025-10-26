# Developer Guide

This guide summarises daily operations for engineers working on the AXIΩM
Ontological Framework.

## Toolchain

- Python 3.11 (managed via `.tool-versions` or your preferred environment
  manager)
- Node.js 20 for commitlint and Commitizen automation
- mkdocs-material for documentation generation

## Bootstrap

```bash
make bootstrap
```

This command creates `.venv`, installs Python optional dependencies (`.[dev]`),
installs Node development tooling via `npm install`, configures the commit
message template, and installs pre-commit hooks (`pre-commit` and commitlint).

## Local Quality Gate

```bash
make check
```

`make check` delegates to `./scripts/check` which executes linting, formatting
validation, mypy, pytest (with coverage), and the security scan. Failures block
merge and must be addressed before PR submission.

## Documentation

Documentation lives in `docs/`. MkDocs builds the static site:

```bash
./scripts/gen-docs
```

## Dependency Management

- `requirements.lock` provides an initial offline snapshot of development
  tooling. Regenerate it with `./scripts/update-deps` when you have network
  access so pip-tools can resolve updated versions deterministically.
- Commit the refreshed lockfile alongside dependency bumps and note the
  coverage/security impact in the changelog.

## Release Flow

1. Ensure `main` is green and up to date.
2. Run `./scripts/release --dry-run` to preview the next semantic version bump.
3. Remove `--dry-run` to cut the release (`cz bump`).
4. Push the commit and annotated tag, then open a release PR summarising the
   changes.

## Observability

Structured logging is emitted through the standard library logging API using
machine-parseable event identifiers. Emit logs via the module-level `logger` and
include contextual extras so log aggregators can index the payload.

## Data Governance

- Persist test fixtures under `tests/fixtures/` as plain text or JSON.
- Large artefacts belong in `assets/` and should use Git LFS when exceeding
  repository size guidance.

## Security

- Run `./scripts/security-scan` before merging. The script orchestrates Bandit
  and pip-audit.
- Secrets must never land in `.env` or committed configuration. Use Vault or
  Doppler where applicable; environment variables are validated during bootstrap
  and runtime.
