"""eval_demo.py — the smallest self-improving eval.

A toy agent answers 6 word problems and returns (answer, path).
The eval scores TWO things per case: the right answer AND the right path.
Run: python3 eval_demo.py        -> good agent: 3/6 answer, 3/6 path
Run: python3 eval_demo.py --bad  -> peeking agent: 6/6 answer, 0/6 path

The peeking agent is the talk's story in miniature: the answer-only
dashboard says it is +50 points better. The path check says it is worthless.
Stdlib only. No model calls. Exit 0 when the full-pass rate is >= 50%.
"""
import sys

# question, expected answer, required ops (with repeats), what the naive
# single-step agent produces (it only ever does the FIRST operation).
CASES = [
    ("A shop sells 4 pens for $12. How much is one pen?",
     3, ["divide"], 3),
    ("Sara reads 20 pages a day for 7 days. How many pages?",
     140, ["multiply"], 140),
    ("A tank holds 100 litres. 35 used. How much is left?",
     65, ["subtract"], 65),
    ("A car uses 8 litres per 100 km. How much for 250 km?",
     20, ["divide", "multiply"], 2.5),
    ("A 10 m rope is cut in 2, then each piece is cut in half again. "
     "How long is one piece?",
     2.5, ["divide", "divide"], 5),
    ("Tom has 3 boxes with 12 apples each and gives away 10. "
     "How many are left?",
     26, ["multiply", "subtract"], 36),
]

FIRST_OP = {"divide": "divide", "multiply": "multiply", "subtract": "subtract"}


def good_agent(case):
    """Does the first operation only. Fails every multi-step problem."""
    _, _, ops, first_result = case
    return first_result, [FIRST_OP[ops[0]]]


def bad_agent(case):
    """Peeks at the answer key. Right answer, no path at all."""
    _, expected, _, _ = case
    return expected, ["recall"]


def path_ok(steps, required):
    """Every required op must appear in the path, as many times as required."""
    for op in set(required):
        if steps.count(op) < required.count(op):
            return False
    return True


def main():
    bad = "--bad" in sys.argv
    agent = bad_agent if bad else good_agent
    print(f"agent: {'peeking (--bad)' if bad else 'single-step (good)'}")
    print(f"{'case':<6}{'answer':<10}{'path':<8}verdict")
    n_ans = n_path = n_full = 0
    for i, case in enumerate(CASES, 1):
        q, expected, ops, _ = case
        answer, steps = agent(case)
        ans_ok = (answer == expected)
        pth_ok = path_ok(steps, ops)
        n_ans += ans_ok
        n_path += pth_ok
        n_full += (ans_ok and pth_ok)
        if ans_ok and pth_ok:
            verdict = "PASS"
        elif ans_ok:
            verdict = "RIGHT ANSWER, WRONG PATH"
        else:
            verdict = "FAIL"
        print(f"{i:<6}{str(answer):<10}{'ok' if pth_ok else 'no':<8}{verdict}")
    n = len(CASES)
    print(f"\nSCOREBOARD: answer {n_ans}/{n}  path {n_path}/{n}  "
          f"full pass {n_full}/{n}")
    if bad:
        print("The answer-only dashboard said 100%. The path check caught it.")
    else:
        print("50% pass — right at the sweet spot. This eval can still tell "
              "a better agent from a worse one.")
    ok = (n_full / n) >= 0.5
    print("GATE:", "PASS — ship it." if ok else "FAIL — no deploy.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
