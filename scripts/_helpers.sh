#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PATH="$ROOT_DIR/.venv"
PYTHON_BIN="$VENV_PATH/bin/python"
PIP_BIN="$VENV_PATH/bin/pip"

export ROOT_DIR VENV_PATH PYTHON_BIN PIP_BIN

function ensure_venv() {
  if [[ ! -d "$VENV_PATH" ]]; then
    python3 -m venv "$VENV_PATH"
  fi
}

function in_venv() {
  local cmd="$1"
  shift || true
  if [[ -x "$VENV_PATH/bin/$cmd" ]]; then
    "$VENV_PATH/bin/$cmd" "$@"
  else
    "$cmd" "$@"
  fi
}

function run_python() {
  if [[ -x "$PYTHON_BIN" ]]; then
    "$PYTHON_BIN" "$@"
  else
    python3 "$@"
  fi
}

function run_pip() {
  if [[ -x "$PIP_BIN" ]]; then
    "$PIP_BIN" "$@"
  else
    pip "$@"
  fi
}

function with_env() {
  if [[ -f "$ROOT_DIR/.env" ]]; then
    # shellcheck disable=SC1090
    set -a
    source "$ROOT_DIR/.env"
    set +a
  fi
  "$@"
}
