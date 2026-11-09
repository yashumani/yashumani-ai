# Workflows vs Agents — Not everything needs an agent

> **The one line:** a workflow runs the same steps every time. An agent decides its steps as it goes.
>
> **The test:** can you draw the flowchart before it runs? Yes → workflow. No → agent — with a harness.
>
> This is the full wiki behind the @yashumani.ai Post 2 carousel. The carousel shows the idea in 7 slides. This file is the complete version: the test, both examples, the router code, and the checklist.

---

## 1. Workflow vs agent

| | Workflow | Agent |
|---|---|---|
| **Steps** | Fixed, written down in advance | Decided as it goes |
| **Same input gives** | The same path, every time | A path that can differ each run |
| **Good for** | Jobs you already understand | Jobs with surprises in them |
| **Costs** | Almost nothing to run | A model call per decision |
| **Testing** | Test each step, one by one | Test on cases — including cases where it should fail |
| **It must never** | — | Send, delete, buy, or publish without approval |

A workflow is a recipe. An agent is a cook who can improvise — and who needs a kitchen with rules.

## 2. The test: draw the flowchart first

Before you reach for an agent, try to draw the flowchart.

- **"Every Friday, find at-risk customers and draft a follow-up for each one."** You can draw that flowchart: read the CRM export → find no-login-in-30-days + open ticket → draft one email per customer → human approves. That is a workflow. It costs zero model calls. An agent doing the same job would burn up to 5 model calls re-deciding steps you already knew.
- **"A customer writes in with a complaint nobody scripted."** You cannot draw that flowchart. The input is unpredictable: it might be a refund, a bug, a cancellation, or something you have never seen. That is where an agent earns its keep — it plans, acts, observes, and checks, inside a harness.

> **Start deterministic. Add agency only where uncertainty requires it.** That is the first principle of HarnessLab, and it is the whole rule: if you can write the steps down, write them down. Don't pay a model to re-decide them every run.

## 3. Example A — the workflow: Friday churn report

Fixed steps, same every Friday:

```
1. read_customers()      — read the CRM export (read-only)
2. find_at_risk()        — no login in 30 days AND an open ticket
3. draft_followups()     — one short email per customer
4. human approves        — nothing sends itself
```

No model decides anything. No loop, no retries, no surprises. If a step fails, the run stops and a human looks at it. You can test step 2 on last week's data and know exactly what it will do next week.

## 4. Example B — the agent: the weird complaint

A customer writes in. Nobody wrote a script for this one. The agent runs the loop from Post 1:

```
Task + Context
  → Plan (what is this about — refund, bug, cancellation?)
  → Act (call one tool: read the ticket, check the account)
  → Observe (read the result)
  → Check (does the draft match a real fact? is this customer real?)
  → if check fails: fix and retry, or stop and ask a human
  → Human approval before anything irreversible
```

The harness is what makes this safe instead of scary: max 5 steps, an allowlist of tools (read, draft — never send), a check that can stop the run, and a human before anything goes out. Same harness as Post 1. The agent is the same machine; the job is just one you couldn't flowchart.

## 5. Agent-washing: the mistake to avoid

**Agent-washing** is calling a fixed pipeline an "agent" — or using an agent for a fixed job.

It costs you three things:

1. **Money and time.** A model call per decision, for decisions you already made.
2. **Reliability.** The same input can take a different path each run, for no reason.
3. **Testability.** You can't test a step-by-step path when there is no fixed path.

If the flowchart exists, ship the flowchart. The agent is not the upgrade; the agent is the tool for the jobs the flowchart can't cover.

## 6. The minimal router (copy, run, break it)

This is a teaching router, not production code. Standard library only, and it runs as-is. It asks the one question — is this a known task? — and sends it down the right path.

```python
# router.py — workflow or agent? Ask one question: can you draw the flowchart first?
# Standard library only. Runs as-is.

KNOWN = {
    "friday_churn_report": ["read_customers", "find_at_risk", "draft_followups"],
    "weekly_invoice_summary": ["read_invoices", "sum_by_customer", "send_summary"],
}

MAX_AGENT_STEPS = 5

def route(task):
    """Known task -> workflow (fixed steps, 0 model calls).
    Unknown task -> agent (harness: budget, tools, check, approval)."""
    if task in KNOWN:
        return {"mode": "workflow", "steps": KNOWN[task], "model_calls": 0}
    return {"mode": "agent",
            "harness": {"max_steps": MAX_AGENT_STEPS,
                        "tools": ["read", "draft"],
                        "check": "must_pass",
                        "approval": "human_before_send"},
            "model_calls": MAX_AGENT_STEPS}

if __name__ == "__main__":
    for task in ["friday_churn_report", "weird_customer_complaint"]:
        print(task, "->", route(task))
```

Run it: `python router.py`. The churn report routes to the workflow — 0 model calls. The weird complaint routes to the agent — up to 5 calls, inside the harness. Then break it on purpose: route the churn report as an agent and watch it spend 5 model calls doing a job the flowchart already solved. Put the routing back, and the cost disappears. That is the whole lesson.

## 7. Before you build it — the checklist

- [ ] You tried to draw the flowchart first.
- [ ] If the flowchart exists, you shipped the workflow, not an agent.
- [ ] If it doesn't exist, the agent has a harness: max steps, a budget, a tool allowlist.
- [ ] The check is written as rules, and it can stop the run.
- [ ] Every step and every check result is logged (a trace).
- [ ] Nothing irreversible happens without human approval.
- [ ] You have run the agent on a case where the check *should* fail, and watched it fail.

If you can't draw the flowchart *and* you have no harness, you don't have an agent. You have a chatbot with a credit card.

## 8. Where this comes from

This wiki follows the first principle of [HarnessLab](https://github.com/yashumani/HarnessLab) — *"Agents are disposable. Harnesses are durable."* — start deterministic, add agency only where uncertainty requires it. The loop and the check come from Post 1's wiki ([01 — Chatbot vs Agent](../01-chatbot-vs-agent/README.md)).

Related work by the same author: [Prefrontal](https://github.com/yashumani/Prefrontal) (a context compiler for agents) and [Talk2Data](https://github.com/yashumani/Talk2Data) (governed execution — the LLM interprets wording only; deterministic services do the work).

---

*Source: @yashumani.ai Post 2 — "Not everything needs an agent." Prompted by Deepak Jose's 50-concepts list (@datasciencebrain); the take here is our own. Comment DECODED on the carousel to get this file. Governed AI, decoded — with evidence.*
