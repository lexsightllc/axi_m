# Changelog

All notable changes to this project will be documented in this file. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-10-27
### Added
- Repository-wide standardization with canonical tooling, automation hooks, and
  developer scripts.
- Structured logging, deterministic entropy handling, and pytest-based unit
  tests for the ontological core.
- Continuous integration workflow running `make check` with dependency caching
  and SBOM publication.

### Changed
- Migrated Python sources into `src/` with aligned test layout under
  `tests/unit/`.
- Replaced legacy logging configuration with structured event identifiers.

### Removed
- Redundant legacy project roots moved under `docs/legacy/`.
