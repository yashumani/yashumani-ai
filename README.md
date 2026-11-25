# The Decoded Series — wiki hub

The full write-ups behind the **Decoded Series** on
[@yashumani.ai](https://www.instagram.com/yashumani.ai).
Each post shares some of the idea; the wiki shares the rest.

**How it works:** comment **DECODED** on a post and the link to its wiki arrives by DM.

## Wikis

- [01 — Chatbot vs Agent: turn ChatGPT into an agent in 3 moves](01-chatbot-vs-agent/README.md) — context, tools, and the check, plus a minimal harness you can run.
- [02 — Workflows vs Agents: not everything needs an agent](02-workflows-vs-agents/README.md) — the flowchart test, both examples, and a minimal router you can run.
- [03 — The 3 rules that make AI reliable](03-three-rules/README.md) — a separate checker, a guardrail that blocks, and evals that can fail a release, plus a runnable eval gate.
- [04 — RAG, simply explained](04-rag-simply-explained/README.md) — retrieve, read, answer; how to retrieve well, RAG vs fine-tuning, and the scoreboard, plus a tiny runnable demo.
- [05 — Context engineering, simply explained](05-context-engineering/README.md) — deciding what goes into the context window; the 4 failure modes, the 4 fixes, and why less context works better.
- [06 — Gen AI in 10 steps: the ladder](06-genai-ladder/README.md) — using AI and building with it are 10 ideas apart; all 10 rungs, with the rule and the check for each.
- [08 — Self-improving evals, the problem: a +9% gain that was luck, not a better model](08-self-improving-evals/README.md) — what the transcript found.
- [09 — Self-improving evals, the fix: the 5-step loop](09-self-improving-evals-solution/README.md) — two eval types, five steps, and the runnable demo.
- [10 — Agent memory, the problem: your agent forgets everything (and the fix has an install screen)](10-claude-mem-problem/README.md) — hooks, compression, layered retrieval, and the three catches.
- [11 — Agent memory, the fix: build the 7-file version, locally](11-claude-mem-build/README.md) — the 7-file rebuild, the safe local-only install, and a runnable demo.
- [Microsoft 365 outage (bonus news post)](05-microsoft-outage/README.md) — a network change, not a hack, took Microsoft 365 down worldwide; the full timeline + sources.
- [The Harness Leaderboard: same model, different harness, measured](harness-leaderboard/README.md) — hold the model fixed and swap only the harness: the full v0.1.9 table, how the board keeps the comparison fair, the noise numbers, and the checklist for choosing a harness.
- [Gemini Decisions API: the checker, as a product](gemini-decisions-api/README.md) — Gemini Decision 1 scores up to 1,000 bounded questions in one pass instead of judging in paragraphs; the decision call in code, the gate / router / grader jobs, and the checklist for trusting a score.
- [OpenClaw: the agent runtime that lives in your chat apps](openclaw-agent/README.md) — a persistent runtime on your own machine, talked to through WhatsApp, Telegram, Slack or Discord: the 4-layer Gateway architecture, the agent loop, and the safety checklist for skills and ClawHub.
- [The Gemini agent: an agent with an identity, a budget, and a boss's inbox](gemini-agent/README.md) — what Google announced at Gemini at Work: coworker agents with their own Workspace accounts, per-project spending caps that pause them, and the four security questions as a deploy checklist.

## Quick-fire series

- [Ep. 1 — Claude Code: 20 commands in 60 seconds](quick-fire-01-claude-code/README.md) — twenty commands in four beats, every one from Claude Code's own docs.
- [Ep. 2 — Codex: 20 commands in 60 seconds](quick-fire-02-codex/README.md) — twenty commands in four beats, every one verified against the shipped CLI itself.

## Principles

- Governed AI, decoded — with evidence.
- A check that cannot stop the run is not a check.
- Agents are disposable. Harnesses are durable.
