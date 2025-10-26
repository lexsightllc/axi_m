SHELL := /bin/bash

.PHONY: bootstrap dev lint fmt typecheck test e2e coverage build package release update-deps security-scan sbom gen-docs migrate clean check

bootstrap:
./scripts/bootstrap "$(ARGS)"

dev:
./scripts/dev "$(ARGS)"

lint:
./scripts/lint "$(ARGS)"

fmt:
./scripts/fmt "$(ARGS)"

typecheck:
./scripts/typecheck "$(ARGS)"

test:
./scripts/test "$(ARGS)"

e2e:
./scripts/e2e "$(ARGS)"

coverage:
./scripts/coverage "$(ARGS)"

build:
./scripts/build "$(ARGS)"

package:
./scripts/package "$(ARGS)"

release:
./scripts/release "$(ARGS)"

update-deps:
./scripts/update-deps "$(ARGS)"

security-scan:
./scripts/security-scan "$(ARGS)"

sbom:
./scripts/sbom "$(ARGS)"

gen-docs:
./scripts/gen-docs "$(ARGS)"

migrate:
./scripts/migrate "$(ARGS)"

clean:
./scripts/clean "$(ARGS)"

check:
./scripts/check "$(ARGS)"
