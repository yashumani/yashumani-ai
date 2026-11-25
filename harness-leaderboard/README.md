# The Harness Leaderboard — Same model, different harness, measured

> **The one line:** hold the model fixed, swap only the harness, and the same open model solves up to ~10 points more (or fewer) tasks. The harness is not packaging. It is part of the result.
>
> **Agent = Model + Harness.** Post 1 of this series argued it from design. This is the same claim with a leaderboard behind it: the Harness Leaderboard, a public Hugging Face Space by Joël Niklaus, runs coding-agent harnesses against identical models and publishes every trajectory.
>
> This is the full wiki behind the @yashumani.ai Harness Leaderboard Reel. All numbers below are from **v0.1.9** of the board, as read on 20 November 2026. The board is versioned and changes often — check the live Space before quoting a number.

---

## 1. The experiment

Most leaderboards rank a model, or a model inside one fixed agent. In practice you choose both: a model, and the harness that drives it — the system prompt, tool schemas, edit format, history compaction, retries and subagents. This board isolates the second choice.

**Held fixed for every harness:**

- Model weights, provider and reasoning effort (a metering proxy inside each sandbox enforces the effort on every call and counts tokens, so cost and time are measured outside the harness)
- Task text, time limit, internet access and scoring
- The model's context window, longest reply and image support, passed to every harness through its own settings

**Left to the harness:** prompts, tools, compaction, retries and subagents — as shipped.

**The field (v0.1.9):**

- **11 harnesses, versions pinned:** Claude Code 2.1.300, Codex 0.162.1, Pi 1.2.0, OpenCode 2.2.6, Hermes Agent v0.22.1, mini-swe-agent 2.4.6, Kimi Code 2.2.0, Qwen Code 0.25.2, OpenClaw 2026.11.1, DeepSeek Harness 0.2.2-rc.1, Grok Build 1.0.77
- **4 open models:** GLM-5.3-Flash and DeepSeek-V4.1-Flash (1,048,576-token context); Flint and Ripple-65B-Preview (262,144-token context — the smaller window is deliberate: it forces harnesses to compact history, so the board tests compaction too)
- **2 benchmarks:** Terminal-Bench 2.1 (87 of 89 tasks — build, debug, configure in a terminal) and DeepSWE v1.1 (111 of 113 tasks — long-horizon features and fixes in real Go, Python, TS/JS and Rust repos)
- **3 attempts per task** per model and effort — 39,204 attempts on the board. Task score = share of attempts that pass; headline = mean of the two benchmarks, with a 95% confidence interval. A paired bootstrap decides which harnesses are statistically tied with the leader. Infrastructure failures are re-run and excluded; agent errors and timeouts count as fails; reading the hidden tests or the reference solution counts as a fail even if the grader passed it.

## 2. The results (v0.1.9, all models, all efforts)

| Harness | Macro (95% CI) | Terminal-Bench 2.1 | DeepSWE | $/trial | $/solve |
|---|---|---|---|---|---|
| OpenCode | 52.5% (49.8–55.3) | 60.9% | 44.1% | $0.52 | $1.11 |
| Kimi Code | 51.7% (49.0–54.4) | 59.8% | 43.6% | $0.63 | $1.37 |
| Grok Build | 50.3% (47.7–53.0) | 57.1% | 43.5% | $0.66 | $1.57 |
| DeepSeek Harness | 49.9% (47.2–52.7) | 56.9% | 43.0% | $0.57 | $1.31 |
| mini-swe-agent | 49.9% (47.2–52.6) | 58.8% | 41.0% | $0.59 | $1.41 |
| Pi | 49.4% (46.7–52.1) | 57.4% | 41.4% | $0.48 | $1.02 |
| Hermes Agent | 49.3% (46.5–52.1) | 56.2% | 42.4% | $0.61 | $1.35 |
| Claude Code | 48.8% (46.2–51.5) | 55.2% | 42.4% | $0.63 | $1.51 |
| Codex | 47.5% (44.8–50.2) | 58.4% | 36.6% | $0.52 | $1.23 |
| Qwen Code | 43.9% (41.3–46.5) | 52.7% | 35.1% | $0.52 | $1.33 |
| OpenClaw | 42.7% (40.0–45.4) | 49.4% | 36.0% | $0.36 | $1.13 |

Cost is priced at the cheapest checked provider's list price, whichever provider served the trial.

## 3. Four findings

### 1. The spread is real — about 10 points

Top to bottom of the board is 52.5% → 42.7% on identical models and tasks: **9.8 points that belong to the harness alone.** On a single model the spread is wider — on Ripple-65B-Preview, Kimi Code solves 56.4% against OpenClaw's 34.4%, a 22-point gap. Same weights. Different setup around them.

### 2. The top is a crowd — and the winner flips with the model

By the board's paired bootstrap, only Kimi Code is statistically tied with the leader OpenCode (−0.9 points); the rest trail by −2.2 to −9.8. But the all-models average hides the real story: **only OpenCode and Kimi Code are tied for first on all four models.** Hermes Agent is tied for first on GLM-5.3-Flash and Flint, and 11th on DeepSeek-V4.1-Flash. Codex is tied for first on DeepSeek-V4.1-Flash and Ripple-65B-Preview, and 11th on GLM-5.3-Flash. There is no "best harness." There is a best pairing of harness and model — read your model's column, not the average.

### 3. The noise is almost as big as the effect

Three attempts per task give the board its own noise instrument. A task "flips" when one attempt passes and another fails:

| Comparison | Flip rate |
|---|---|
| Same harness, re-run | 24.1% |
| Swap the harness | 27.1% |
| Swap the effort (same harness) | 27.1% |
| Swap the model (same harness) | 33.8% |

Swapping the harness adds only **+3.0 points** of flips beyond plain re-run noise (+4.0 on Terminal-Bench 2.1, +2.0 on DeepSWE). Two lessons: the model still matters more than the harness — and a single run tells you very little. If one attempt flips a quarter of tasks by itself, a one-off "agent A beat agent B" demo is mostly dice.

### 4. Cost per solved task separates the pack

On accuracy vs cost per trial, three harnesses sit on the Pareto frontier — none is beaten on both axes:

- **OpenClaw** — $0.36 per trial, 42.7%. Cheapest, least accurate.
- **Pi** — $0.48 per trial, 49.4%, and the lowest cost per solved task at **$1.02**.
- **OpenCode** — $0.52 per trial, 52.5%. Most accurate.

The other eight are dominated on these numbers: OpenCode is both cheaper and more accurate than Kimi Code, Grok Build, Claude Code and Hermes Agent. More expensive did not mean more solved — Grok Build and Claude Code carry the highest cost per trial and neither is on the frontier. Inside a statistical tie, let the invoice decide — and compare cost **per solve**, never per call.

## 4. The bugs are a lesson on their own

Running harnesses against models that are not their vendor's own exposed defaults that silently change behaviour:

- **OpenClaw** asks for at most 8,192 tokens per reply when it is not told the model's longest reply — although its documentation says it then sends no limit.
- **Codex** assumes a 272,000-token window for unknown models; its window setting cannot raise that — only a model catalog file can. It also cuts command output at 10,000 bytes.
- **Claude Code** lowers its reply limit to the room left in the context only on Anthropic's servers.
- **DeepSeek Harness** sets its compaction point from the model's longest reply, so when the longest reply equals the context window (Flint), automatic compaction never fires.
- **Grok Build** sends images it opens to the model, even when the model is set up as text-only.

Rule: when you run a harness against a model it does not know, set the context window and max output tokens **explicitly**. Do not trust the defaults.

## 5. Choosing a harness — the checklist

- [ ] Start from the board's column for **your model**, not the all-models average.
- [ ] Compare **cost per solved task**, not cost per call or per token.
- [ ] Run candidate harnesses on **your own tasks, at least 3 attempts each** — one run is mostly noise.
- [ ] Track the share of tasks solved on **all** attempts, not just at least once — unattended work needs consistency.
- [ ] Set the context window and max reply **explicitly**; audit the harness's defaults for your model.
- [ ] Read a few full trajectories before you trust a score — the board publishes them for a reason.

## 6. Caveats — read before quoting

- **Open models only.** Claude Code and Codex scores here show how they drive GLM, DeepSeek, Flint and Ripple — not how they drive Claude or GPT.
- **Two benchmarks only.** Nothing here covers network automation, infra ops, or your codebase.
- **Harnesses ran on different days.** Provider speed varies day to day while the per-task time limit stays fixed, so a harness that ran on a fast day fits more calls into the limit.
- **List prices.** Vendor cache discounts and subscriptions are not modelled.
- **Versioned and changing.** These are v0.1.9 numbers. An earlier version (v0.1.1, nine harnesses, three models) told the same story with different names on top — which is itself the point: rankings move, the harness effect does not disappear.

## 7. Sources

- Harness Leaderboard (v0.1.9), a Hugging Face Space by Joël Niklaus — https://huggingface.co/spaces/joelniklaus/harness-leaderboard (public since early November 2026; flagged in the Open Source Trends tracker briefings of Nov 15 and Nov 22, 2026)
- Numbers as tabulated from the Space's public data in "Same Model, 11 Harnesses: What the Harness Leaderboard v0.1.9 Tells Engineers" (read 2026-11-20) — https://mlh.forem.wtf/supachai/same-model-11-harnesses-what-the-harness-leaderboard-v019-tells-engineers-3lpb
- Launch coverage of v0.1.1 (nine harnesses): New Runtime, 2026-11-07 — https://newruntime.com/posts/joel-niklaus-releases-harness-leaderboard-comparing-nine-coding-f0efa5/
- Independent recomputation of v0.1.1 from the board's own records: bokonon.ai note, 2026-11-06 — https://bokonon.ai/notes/2026-11-06-a-tie-a-tail-and-a-cap/
- Clip in the Reel: Raja Jamwal, "Same AI Model, Broken Game vs Working Game: What an Agent Harness Does" — https://www.youtube.com/watch?v=dzEBiSKLww8 (LangChain's harness-only Terminal-Bench result: ~53% → 66.5% with the model held fixed)

---

*Source: @yashumani.ai — "Same model. Different harness. Different score." Comment DECODED on the Reel to get this file. Governed AI, decoded — with evidence.*
