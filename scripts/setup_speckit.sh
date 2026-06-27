#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INTEGRATION="${SPECKIT_INTEGRATION:-claude}"
OK=true

log()  { echo "[setup-speckit] $*"; }
warn() { echo "[setup-speckit] WARN: $*" >&2; }
err()  { echo "[setup-speckit] ERROR: $*" >&2; OK=false; }

# ── 1. Locate specify CLI ─────────────────────────────────────────────────────
SPECIFY_CMD=""

if command -v specify &>/dev/null; then
    SPECIFY_CMD="specify"
elif command -v uvx &>/dev/null; then
    SPECIFY_CMD="uvx --from git+https://github.com/github/spec-kit.git specify"
elif command -v pipx &>/dev/null; then
    log "specify not found — installing via pipx..."
    pipx install git+https://github.com/github/spec-kit.git
    SPECIFY_CMD="specify"
else
    err "Neither 'specify', 'uvx', nor 'pipx' found."
    err "Install one of: pipx (https://pipx.pypa.io) or uv (https://docs.astral.sh/uv)"
    exit 1
fi

log "Using: $SPECIFY_CMD"

# ── 2. Check .specify/ directory ─────────────────────────────────────────────
if [[ ! -d "$REPO_ROOT/.specify" ]]; then
    log ".specify/ not found — running init..."
    (cd "$REPO_ROOT" && $SPECIFY_CMD init --here --force --integration "$INTEGRATION")
else
    log ".specify/ found"
fi

# ── 3. Check integration skills ───────────────────────────────────────────────
SKILLS_DIR="$REPO_ROOT/.claude/skills"
EXPECTED_SKILL="$SKILLS_DIR/speckit-specify.md"

if [[ ! -f "$EXPECTED_SKILL" ]]; then
    log "spec-kit skills missing from .claude/skills/ — re-running init..."
    (cd "$REPO_ROOT" && $SPECIFY_CMD init --here --force --integration "$INTEGRATION")
else
    log "skills found in .claude/skills/"
fi

# ── 4. Check constitution exists ──────────────────────────────────────────────
CONSTITUTION="$REPO_ROOT/.specify/memory/constitution.md"
if [[ ! -f "$CONSTITUTION" ]]; then
    warn "constitution.md missing — copy from template"
    cp "$REPO_ROOT/.specify/templates/constitution-template.md" "$CONSTITUTION"
    warn "Created $CONSTITUTION from template — fill it in with /speckit-constitution"
else
    log "constitution.md found"
fi

# ── 5. Summary ────────────────────────────────────────────────────────────────
if $OK; then
    log "All good. Next step: open Claude Code in $REPO_ROOT and run /speckit-constitution"
else
    exit 1
fi
