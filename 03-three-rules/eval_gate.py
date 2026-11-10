# eval_gate.py — the smallest eval gate that can fail a release.
# Standard library only. Runs as-is. Companion to Post 3 wiki (03-three-rules).
#
#   python eval_gate.py        -> RELEASE: SHIP   (exit 0)
#   python eval_gate.py --bad  -> RELEASE: BLOCKED (exit 1)
#
# --bad simulates a release where evals were demoted to advisory:
# the work is the same, the evals are the same, only the gate is off —
# and the gate still blocks it, because a gate that can't fail a release
# is itself a failing eval.

import sys

ALLOWED_TOOLS = {"read", "draft"}  # Rule 2: the allowlist. Never send/delete/buy/publish.


def check_separate_checker(release):
    """Rule 1: worker is not its own checker."""
    return release["checker"] != release["worker"]


def check_guardrail_blocks(release):
    """Rule 2: every tool the release uses must be on the allowlist."""
    return all(tool in ALLOWED_TOOLS for tool in release["tools"])


def check_evals_can_fail(release):
    """Rule 3: evals must be able to block a merge."""
    return release["evals_block_merge"] is True


EVALS = [
    ("worker is not its own checker", check_separate_checker),
    ("guardrail blocks disallowed tools", check_guardrail_blocks),
    ("evals can block a merge", check_evals_can_fail),
]

GOOD_RELEASE = {
    "worker": "draft_agent",
    "checker": "rules_checker",
    "tools": ["read", "draft"],
    "evals_block_merge": True,
}


def run(release):
    failures = [name for name, fn in EVALS if not fn(release)]
    for name, fn in EVALS:
        print(("PASS " if fn(release) else "FAIL ") + name)
    if failures:
        print("RELEASE: BLOCKED — %d of %d evals failed" % (len(failures), len(EVALS)))
        return 1
    print("RELEASE: SHIP — %d of %d evals passed" % (len(EVALS), len(EVALS)))
    return 0


if __name__ == "__main__":
    release = dict(GOOD_RELEASE)
    if "--bad" in sys.argv:
        release["evals_block_merge"] = False
    sys.exit(run(release))
