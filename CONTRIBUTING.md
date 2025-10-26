# Contributing

Thank you for investing time in the AXIΩM Ontological Framework. This document
captures the expectations that keep the repository deterministic, observable,
and safe to modify.

## Code of Conduct

Participation in this project is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

## Workflow

1. Fork or branch from `main`. Feature work should target short-lived branches
   named using kebab-case (`feature/new-telemetry-channel`).
2. Run `make bootstrap` to provision toolchains, pre-commit hooks, and commit
   templates.
3. Develop in small, reviewable increments. Keep commits atomic and use
   Conventional Commit messages (e.g. `feat(core): add epistemic checksum`).
4. Ensure `make check` passes locally. The command orchestrates linting,
   formatting, type checking, unit tests, coverage enforcement, and security
   scans.
5. Update documentation and ADRs alongside functional changes.
6. Open a pull request with:
   - A summary referencing the affected domain areas.
   - Evidence of successful checks.
   - Notes on observability, migrations, or follow-up actions where relevant.

## Licensing and Contributor Terms

- All inbound contributions are accepted under the Mozilla Public License 2.0
  (MPL-2.0). By submitting a contribution you affirm that you have the right to
  do so under inbound=outbound terms and that the project may redistribute your
  contribution under MPL-2.0.
- Modifications to MPL-covered files must remain under MPL-2.0. Larger works
  that merely depend upon or interface with these files may remain under their
  own licenses, provided the MPL obligations for the covered files are met.

## Testing Standards

- Unit tests mirror the package hierarchy under `tests/unit/` and follow the
  naming pattern `test_*.py`.
- Integration tests belong in `tests/integration/` and end-to-end flows in
  `tests/e2e/`. Tag E2E scenarios with Given/When/Then comments for readability.
- Determinism matters: seed random number generators, isolate filesystem and
  network IO unless explicitly under `tests/e2e/`, and prefer textual fixtures
  stored beneath `tests/fixtures/`.

## Code Style

- Python formatting is enforced with `ruff format` and `black`; imports are
  normalised via `isort`.
- Static analysis uses Ruff (lint rules) and mypy in strict mode. Lint
  exemptions require inline justification.
- Logging must use structured event identifiers (see `axiom_core.axiom_system`).
- Prefer type annotations for all public APIs. Avoid implicit `Any`.

## Commit Conventions

- Use Conventional Commits. Example prefixes: `feat`, `fix`, `chore`, `docs`,
  `refactor`, `test`.
- The commit template `.gitmessage` is installed by `scripts/bootstrap` and
  ensures the required structure.
- Commit messages are validated by commitlint via a commit-msg hook.

## Dependency Management

- Application dependencies are declared in `pyproject.toml`.
- Run `./scripts/update-deps` to regenerate `requirements.lock`.
- Security scans (`./scripts/security-scan`) must pass before merging.

## Releasing

1. Run `./scripts/release` to bump the version via Commitizen, update the
   changelog, build artefacts, and create a signed tag.
2. Push the tag and open a release PR summarising changes and verifying
   compatibility.

## Support

Questions can be raised via GitHub issues using the “Structure” template or in
synchronous design reviews captured as ADRs.
