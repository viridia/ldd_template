#!/usr/bin/env bash
# Runs the verification recipe (CLAUDE.md's "Verification" section) as one command, filtering
# routine output and only widening it for a step that actually failed.
#
# A warning counts as a failure here even though a compiler's own exit code ignores it, because
# CLAUDE.md's convention is that this tree is warning-free.
#
# Usage: scripts/verify.sh
#
# The recipe grows with the project: a build, its tests, a linter, and a flag for any slow step
# that only some changes need, kept out of the default run.

set -uo pipefail
cd "$(dirname "$0")/.."

if [[ $# -gt 0 ]]; then
    echo "usage: $0" >&2
    exit 2
fi

failed=0
declare -a fail_names=()

# Runs one step, capturing combined output. Passes if the command exits 0 *and* prints no
# "warning:" line; on failure, prints the full output rather than staying filtered, since a
# filtered failure is useless for debugging. On success it prints only the lines matching
# SUMMARY, so a passing test run costs a line rather than one per test.
SUMMARY='test result|tests passed|FAILED'
run_step() {
    local name="$1"
    shift
    echo "== ${name} =="
    local output status warnings
    output=$("$@" 2>&1)
    status=$?
    warnings=$(printf '%s\n' "${output}" | grep -ci 'warning:' || true)

    if [[ ${status} -ne 0 ]]; then
        printf '%s\n' "${output}"
        echo "FAILED (exit ${status}): ${name}"
        failed=1
        fail_names+=("${name}")
    elif [[ ${warnings} -gt 0 ]]; then
        printf '%s\n' "${output}" | grep -i 'warning:'
        echo "FAILED (warnings): ${name}"
        failed=1
        fail_names+=("${name} (warnings)")
    else
        printf '%s\n' "${output}" | grep -E "${SUMMARY}" || echo "ok"
        echo "pass: ${name}"
    fi
    echo
}

summarize() {
    echo "=================================="
    if [[ ${failed} -eq 0 ]]; then
        echo "All checks passed."
    else
        echo "FAILED:"
        printf '  - %s\n' "${fail_names[@]}"
    fi
    exit ${failed}
}

# First because it costs milliseconds, and because a reference that stopped resolving is the one
# kind of breakage nothing else here would ever notice.
run_step "scripts/xref.py" python3 scripts/xref.py --quiet
run_step "scripts/test_devfmt.py" python3 scripts/test_devfmt.py

# The project's own steps go here, for example:
# run_step "cmake --build build" cmake --build build
# run_step "ctest" ctest --test-dir build --output-on-failure

summarize
