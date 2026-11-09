# Chatbot vs Agent — Turn ChatGPT into an agent in 3 moves

> **The one line:** a chatbot answers and stops. An agent plans, uses tools, checks its own work — and finishes.
>
> **Agent = Model + Harness.** The model is the brain. The harness is everything around it: the context it gets, the tools it may call, the budget it must stay inside, the check that can stop it, and the human approval before anything irreversible happens.
>
> This is the full wiki behind the @yashumani.ai Post 1 Reel. The Reel shows the idea in 20 seconds. This file is the complete version: the example, the loop, the code, and the checklist.

---

## 1. Chatbot vs agent

| | Chatbot | Agent |
|---|---|---|
| **You give it** | One message | A task + context + tools + a check |
| **It does** | Writes one reply | Plans, acts, observes, checks, repeats |
| **It stops when** | The reply is written | The task is done — or the check fails |
| **It can** | Only write text | Read files, query data, call APIs, draft work |
| **It must never** | — | Send, delete, buy, or publish without approval |

A chatbot is a single turn. An agent is a loop with a finish line.

## 2. The 3 moves

### Move 1 — Context: give it what it needs, nothing it doesn't

The model can only work with what is in its context. "Summarise churn risk" with no data is guessing.

**The example task:** every Friday, find which customers are at risk of churning and draft a follow-up email for each one.

Context for that task, written down before the model runs:

- The customer list, with plan, last login, and support tickets (from the CRM export)
- What "at risk" means here: no login in 30 days **and** an open support ticket
- What to draft: a short follow-up email, one per customer, in the company's tone
- What **not** to include: payment details, internal notes, other customers' data

Rule: if the context does not contain the fact, the model must say "not in the context" — not invent it. That rule is part of the harness, not a hope.

### Move 2 — Tools: let it act, inside a fence

A model that can only write cannot finish this task. It needs tools — and a fence around them.

Allowed tools for this task:

- `read_customers()` — read the CRM export (read-only)
- `draft_email(customer, reason)` — draft, never send
- `lookup_ticket(customer)` — read one support ticket

Denied, always:

- Sending email, deleting records, changing a plan, spending money

Every tool call is logged: what was called, with what input, what came back. If a tool fails, the loop sees the failure — it does not pretend the step worked.

### Move 3 — Check: the step most people skip

The check is what turns a chatbot into an agent you can trust. It runs **before** anything is finished, and it can stop the run.

The check for this task, written as rules, not vibes:

1. Every drafted email must name a customer who is actually in the at-risk list.
2. Every reason in the email must match a real ticket or a real last-login date.
3. No email may contain another customer's data.
4. Nothing is sent. Drafts wait for a human to approve.

**The moment the check earns its keep:** the agent drafts a follow-up for a customer who cancelled last month. The customer's last login is old, so they look at-risk — but the CRM status is `cancelled`. The check catches it, rejects that draft, and the loop retries without that customer. A chatbot would have sent the email. The agent does not.

> **A check that cannot stop the run is not a check. It is a comment.**

## 3. The loop

```
Task + Context
  → Plan (what steps, in what order)
  → Act (call one tool)
  → Observe (read the tool's result)
  → Check (does this hold up? is it in bounds?)
  → if check fails: fix and retry, or stop and ask a human
  → if check passes: next step, until the task is done
  → Human approval before anything irreversible
```

Not a straight line. A loop. The dot in the Reel travels Context → Agent → Checked and back for a reason: the check feeds back into the work.

**Limits that keep the loop safe:**

- Max 5 steps. If it is not done in 5, stop and ask a human.
- One tool per step. No chains the human cannot follow.
- Budget: a maximum number of model calls per run.
- Approval: drafts are drafts. Sending is a human decision.

## 4. The minimal harness (copy, run, break it)

This is a teaching harness, not production code. Standard library only, and it runs as-is: the model is a scripted demo that drafts to the cancelled customer first, so you can watch the check catch it. Swap `call_model` for your model call when you are ready.

```python
# minimal_harness.py — a chatbot is a call; an agent is a loop with a check.
# Standard library only. It runs as-is with a scripted demo model, so you can
# see the loop (including the check catching the cancelled customer) before
# you wire in a real model: replace call_model() with yours when ready.

MAX_STEPS = 5

# --- Demo model: a fixed script of decisions, so this file runs out of the box.
# Step 1 reads the customers, step 2 drafts to Beta (cancelled — the check
# must catch it), step 3 drafts to Acme (genuinely at risk), then it finishes.
_DEMO_STEPS = [
    {"tool": "read_customers", "args": {}},
    {"tool": "draft_email", "args": {"customer": "Beta", "reason": "no login in 60 days and an open ticket"}},
    {"tool": "draft_email", "args": {"customer": "Acme", "reason": "no login in 42 days and an open ticket"}},
    {"done": True, "result": "done"},
]
_step = {"i": 0}

def call_model(context, history):
    """Demo model. Return {'tool': name, 'args': {...}} or {'done': True, ...}."""
    i = _step["i"]
    _step["i"] += 1
    return _DEMO_STEPS[i] if i < len(_DEMO_STEPS) else {"done": True, "result": "done"}

# --- Tools: the only actions the agent may take. Drafts, never sends. ---
def read_customers():
    return [
        {"name": "Acme", "last_login_days": 42, "open_ticket": True, "status": "active"},
        {"name": "Beta", "last_login_days": 60, "open_ticket": True, "status": "cancelled"},
    ]

def draft_email(customer, reason):
    return f"Subject: Checking in\n\nHi {customer}, we noticed {reason} — can we help?"

TOOLS = {"read_customers": read_customers, "draft_email": draft_email}

# --- Check: can stop the run. A check that cannot stop is not a check. ---
def check(draft, at_risk_names):
    if draft["customer"] not in at_risk_names:
        return False, "customer is not in the at-risk list"
    if "cancelled" in draft["customer_status"]:
        return False, "customer already cancelled — do not contact"
    return True, "ok"

def run(task_context):
    _step["i"] = 0  # restart the demo script on each run
    customers = read_customers()
    status_by_name = {c["name"]: c["status"] for c in customers}
    history, drafts = [], []
    # At risk = no login in 30 days AND an open ticket (status is NOT part of
    # this definition — that is exactly what the check has to catch for Beta).
    at_risk = [c["name"] for c in customers
               if c["last_login_days"] > 30 and c["open_ticket"]]
    for step in range(MAX_STEPS):
        decision = call_model(task_context, history)
        if decision.get("done"):
            return {"status": "finished", "drafts": drafts, "history": history}
        tool = TOOLS[decision["tool"]]
        result = tool(**decision["args"])
        history.append({"step": step, "tool": decision["tool"], "result": result})
        if decision["tool"] == "draft_email":
            draft = {**decision["args"], "customer_status": status_by_name[decision["args"]["customer"]]}
            ok, why = check(draft, at_risk)
            if not ok:
                history.append({"step": step, "check": "FAILED", "reason": why})
                continue  # retry without the bad draft; do not finish with it
            drafts.append(result)
    return {"status": "stopped — max steps, needs a human", "drafts": drafts, "history": history}

if __name__ == "__main__":
    print(run("Every Friday, find at-risk customers and draft a follow-up for each."))
```

Run it: `python minimal_harness.py` — the output shows Beta's draft rejected ("customer already cancelled — do not contact") and only Acme's draft kept. Then break it on purpose: remove the check, and watch the cancelled customer get an email. Put the check back, and watch it get caught. That is the whole lesson.

## 5. Before you trust it — the checklist

- [ ] The context is written down. Nothing is assumed.
- [ ] The tool list is an allowlist. Everything else is denied.
- [ ] The check is written as rules, and it can stop the run.
- [ ] The loop has a max step count and a budget.
- [ ] Every tool call and every check result is logged (a trace).
- [ ] Nothing irreversible happens without human approval.
- [ ] You have run it on a case where the check *should* fail, and watched it fail.

If you cannot tick the check box, you have a chatbot with extra steps — not an agent.

## 6. Where this comes from

This wiki follows the same principles as [HarnessLab](https://github.com/yashumani/HarnessLab) — *"Agents are disposable. Harnesses are durable."* — start deterministic, add agency only where uncertainty requires it, give every agent minimum necessary context, tools, permissions, time, and budget, and require human approval for anything irreversible.

Related work by the same author: [Prefrontal](https://github.com/yashumani/Prefrontal) (a context compiler for agents) and [Talk2Data](https://github.com/yashumani/Talk2Data) (governed execution — the LLM interprets wording only; deterministic services do the work).

---

*Source: @yashumani.ai Post 1 — "ChatGPT can do more than chat." Comment DECODED on the Reel to get this file. Governed AI, decoded — with evidence.*
