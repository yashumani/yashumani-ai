# The 3 rules that make AI reliable

> **The one line:** reliable AI isn't luck. It's three checks around the same model.
>
> **The rules:** 1. The worker never grades its own work. 2. A guardrail that can't block is decoration. 3. Evals that can fail a release.
>
> This is the full wiki behind the @yashumani.ai Post 3 carousel (Decoded Series #3). The carousel shows the idea in 7 slides. This file is the complete version: each rule, why it exists, the guardrail and eval code, and the checklist.

---

## 1. Rule 1 — the worker never grades its own work

An agent that grades its own output will pass itself. That is not a check; it is a mirror.

Split the jobs:

- **Worker** — does the task: drafts the email, writes the code, summarises the ticket.
- **Checker** — a separate step with the pass/fail criteria written as rules, not vibes. It reads the worker's output and the original facts, and says pass or fail.

Put the criteria in the same skill file as the task, so the worker iterates until the checker passes — and the checker is never the worker. Post 1's harness already works this way: the check runs after the act, and a failed check retries or stops the run.

The test for this rule: delete the checker and watch the worker ship its first draft. If nothing changes, you never had a checker.

## 2. Rule 2 — a guardrail that can't block is decoration

A prompt that says "be careful" is not a guardrail. A guardrail is a deterministic hook that always fires and can stop the action before it runs.

The shape, from Post 1:

1. The model **picks** from an allowlist of tools — read, draft. Never send, delete, buy, or publish.
2. An **executor validates the arguments** before anything runs: is this customer real? Is this customer cancelled? Is the amount inside the limit?
3. If validation fails, the action **never runs**. No appeal to the model, no second opinion.

A guardrail you can talk your way past is a suggestion. Test yours the way you test a lock: try a bad action on purpose and watch it get blocked. If it runs, the guardrail is decoration.

## 3. Rule 3 — evals that can fail a release

Evals are a fixed test set, run on every change, with a judge that is calibrated — and a result that can block the merge.

The pipeline: PR → pytest → agent run → code checks + LLM judge → merge or fail. Every run traced, so a failure points at the exact case that broke.

Two things make evals real:

- **Fixed set.** The same cases every run. A demo that passes once is not an eval.
- **A blocking gate.** If evals can't fail a release, you don't have quality control — you have a dashboard. The fixed set decides, not the demo.

The demo in this folder, `eval_gate.py`, is the smallest version of this: three fixed cases, one of which is a release that must fail. Run it with `--bad` and watch the gate stop the release.

## 4. The minimal eval gate (copy, run, break it)

Standard library only, runs as-is. See `eval_gate.py` in this folder.

```python
# eval_gate.py — three fixed evals. A release ships only if all three pass.
# Run: python eval_gate.py        -> RELEASE: SHIP
# Run: python eval_gate.py --bad  -> RELEASE: BLOCKED (exit 1)

ALLOWED_TOOLS = {"read", "draft"}          # Rule 2: the allowlist

def check_separate_checker(release):
    return release["checker"] != release["worker"]

def check_guardrail_blocks(release):
    return all(tool in ALLOWED_TOOLS for tool in release["tools"])

def check_evals_can_fail(release):
    return release["evals_block_merge"] is True

EVALS = [
    ("worker is not its own checker", check_separate_checker),
    ("guardrail blocks disallowed tools", check_guardrail_blocks),
    ("evals can block a merge", check_evals_can_fail),
]
```

Then break it on purpose: flip `evals_block_merge` to `False` in a release and watch the gate block it — the release is unchanged, the evals are unchanged, and the only thing that moved is the gate doing its job. That is the whole lesson: the gate, not the demo, decides.

## 5. Before you ship it — the checklist

- [ ] A separate checker grades the work — the worker never grades itself.
- [ ] The guardrail can block: you tried a bad action and watched it stop.
- [ ] Evals ran on the fixed set, and they can fail this release.
- [ ] Every run is traced: steps, tool calls, and check results.
- [ ] Nothing irreversible happens without human approval.
- [ ] You have run the agent on a case where the check *should* fail, and watched it fail.

If any box is unchecked, you don't have a reliable system. You have a demo with good intentions.

## 6. Where this comes from

These are the top three items of the ranked AI best-practices list (2026-11-04 refresh, still current after the November currency audit): the separate checker, the blocking guardrail, and the release-blocking eval. The harness and the check come from Post 1's wiki ([01 — Chatbot vs Agent](../01-chatbot-vs-agent/README.md)); the flowchart test and the router come from Post 2 ([02 — Workflows vs Agents](../02-workflows-vs-agents/README.md)).

Related work by the same author: [HarnessLab](https://github.com/yashumani/HarnessLab) (agents are disposable, harnesses are durable), [Prefrontal](https://github.com/yashumani/Prefrontal) (a context compiler for agents), and [Talk2Data](https://github.com/yashumani/Talk2Data) (governed execution — the LLM interprets wording only; deterministic services do the work).

---

*Source: @yashumani.ai Post 3 — "Reliable AI isn't luck. It's 3 rules." Comment DECODED on the carousel to get this file. Governed AI, decoded — with evidence.*
