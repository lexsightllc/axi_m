# ADR 0001: Standardised Repository Structure

- Status: Accepted
- Deciders: Structure Steward Team
- Date: 2024-10-27

## Context

The repository previously contained multiple divergent project roots with
inconsistent tooling, duplicated documentation, and no unified automation
surface. Contributors had to memorise bespoke commands, which made quality gates
fragile.

## Decision

Adopt a canonical repository layout with:

- `src/` based Python packaging and mirrored `tests/` hierarchy.
- Centralised `scripts/` toolbelt (with PowerShell mirrors) mapping to `make`
targets.
- Pre-commit enforcement for linting, formatting, typing, tests, and commit
lint.
- CI orchestrating `make check`, caching dependencies, publishing SBOMs, and
signing releases.

## Consequences

- Onboarding becomes deterministic: `make bootstrap` + `make check` reproduces
  CI locally.
- Legacy material is archived under `docs/legacy/` but remains discoverable.
- The repository is now ready for Renovate/Dependabot automation because
  dependency manifests are consolidated.
