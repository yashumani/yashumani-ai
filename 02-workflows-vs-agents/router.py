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
