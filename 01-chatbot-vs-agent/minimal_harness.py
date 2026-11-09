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
