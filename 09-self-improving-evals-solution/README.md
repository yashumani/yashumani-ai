# Self-improving evals — the loop (the solution)

> **The one line:** a dashboard that only says pass is not an eval. The loop is: real prompts, transcripts, answer *and* path, the same eval on every swap, gated in CI.
>
> **The loop in five steps:** 100 real prompts, tuned so the agent passes about half. Every failure becomes a transcript, and every transcript becomes a new test. Score the answer *and* the path. Re-run the same eval on every model swap. Gate deploys on green evals.
>
> This is the full wiki behind the @yashumani.ai Post 9 motion Reel
(Decoded Series #9 — the solution post; Post 8 is the problem). The Reel opens with a clip from the talk, then walks the loop in five steps. This file is the complete version: the two kinds of evals, the five steps, what the demo proves, and the checklist.

> *Clip source: "Why Most AI Agents Fail—and How Anthropic Builds Reliable Ones", Marius Buleandra (Anthropic), Arize Observe 2026 — https://www.youtube.com/watch?v=ijlrwKiYYM4. The Reel uses 6:16–6:52 (375.4–412.6s): "How should you do it? There are two categories of evals… regression evals… capability evals… the best startups put a lot of effort into capability evals just to know what's possible." The clip opens on the question the post answers. The slide behind him names both kinds: capability evals — "What can this agent do?" (start low, hill-climb); regression evals — "Does it still do what it used to do?" (near 100%, a drop means breakage). Downloaded from the already-on-disk talk file, web client, 1920×1080 H.264, no bot check.*

---

## 1. Two kinds of evals — and why you need both

Buleandra's answer to "how should you do it?" starts with a split:

- **Regression evals** — the ones the talk covered earlier. They sit near 100%, saturated; you refresh them now and then. Their job is to give you the signal that something is wrong: the fixed set tells you if the new model broke what used to work.
- **Capability evals** — the more important half, in his words. They ask what the agent *can* do: start low, hill-climb, and find out what is possible. The best startups he works with put a lot of effort into capability evals "just to know what's possible" — and with that information they change the product, the features, even the market they sell into.

Capability evals that saturate graduate into the regression suite — that is the slide's own footer. One set finds the ceiling; the other guards the floor.

## 2. Step 1 — 100 real prompts, and the 50% rule

Take 100 real user prompts and run your agent over them.

- If it passes **80% or more, your eval is too easy.** A test everything passes carries no information — it cannot tell a better agent from a worse one, or a regression from an improvement.
- The sweet spot is **50%**. Half the cases pass, half fail, and every change you make moves the number in a way you can read. His words, later in the talk: the ideal is "starting from that ideal sweet spot… like 50% and… trying to get to… 80%".

The 50% figure is the speaker's rule of thumb, not a universal constant — but the principle behind it is standard eval practice: an eval near 100% pass usually means the criteria are too easy (or the cases are), and an eval near 0% means the criteria are misfiring. What matters is not the exact number but that the eval *discriminates*: a better agent scores higher, a broken one scores lower. The demo in this folder sits at exactly 50% for its good agent, on purpose.

## 3. Step 2 — every failed run is a transcript

Every failed run leaves a transcript: everything the agent did, step by step. Feed that transcript to a strong model and ask "what went wrong?"

That is the self-improving part. Each failure becomes a new test case, added to the eval set — so the set grows from real failures, not from cases someone invented in advance. This is standard error-analysis practice: Hamel Husain has argued for years that error analysis on real outputs comes before any tooling, and the practical guides agree — start your eval set with real failures from logs and support tickets, not with cases an LLM invents. Fifty cases chosen to cover distinct failure types tell you more than 500 polite, well-formed ones.

The talk's framing adds the scale: "Scaling Transcript Review with AI" — a human reads the transcripts that matter most, and a model does the first pass over the rest.

## 4. Step 3 — score two things: the answer AND the path

Score the right answer **and** the right path. A right answer reached by the wrong path is a failure waiting for next week.

This is the process-supervision vs outcome-supervision distinction, and it is well established: OpenAI's "Let's Verify Step by Step" (2023) showed process supervision beats outcome supervision on hard math, because outcome-only grading rewards any route to the answer — including guessing, memorised answers, and shortcuts that happen to land right. The same failure shows up in agent evals: in one study of coding agents, a quarter of failed runs ended with the agent *reporting success*. Agent evals therefore grade what the agent leaves behind, not what it says.

The talk says it directly (10:23–10:34, transcript-verified): "there's like two things you need to eval on — the outcome of the agent and then the transcript of the agent." And the hard part he names right after (10:41–10:59): evaluating an outcome *and* a transcript usually means an LLM judge or an LLM agent — "and that's pretty hard because that agent also has its own problems, so you need to find a way to calibrate that agent" against human-labelled data.

The demo makes the point in miniature:

```python
# eval_demo.py — 6 word problems. Scores answer AND path.
# Run: python3 eval_demo.py        -> SCOREBOARD: answer 3/6, path 3/6, full 3/6
# Run: python3 eval_demo.py --bad  -> SCOREBOARD: answer 6/6, path 0/6, full 0/6
```

The `--bad` agent peeks at the answer key: 6/6 on answers, 0/6 on paths. An answer-only dashboard would call it a 50-point improvement. The path check calls it what it is — worthless. That is the talk's story, reproduced in six lines of output.

## 5. Step 4 — the same eval, every model swap

A new model drops. Run the same eval before you switch.

Buleandra's story, as relayed in the source post and told in Post 8: a new model showed a **+9% gain** on the dashboard. Re-running the same eval set showed the gain was fake — **6% of it was the model dodging a bug** rather than fixing it. The transcript caught what the dashboard missed. The three lucky breaks the transcript found — world knowledge filling in missing data, SQL LIMIT dodging a bug in the SQL execution tool, a date format revealing inconsistencies — are in the Post 8 wiki; this post is the loop that would have caught them before shipping.

Two flags on this one, stated plainly:

- **The numbers are the speaker's anecdote, not independently verified.** No second source carries the +9% / 6% figures. Treat them as his story, not as data.
- **The principle is verified and load-bearing.** Regression evals exist precisely for this: the same fixed set, re-run on every change, so a model swap cannot silently trade one failure for another. Aggregate scores hide per-case changes — that is why the eval set is fixed and the transcripts are read, not just the headline number. The talk's own chapters name it: "Regression vs Capability Evals".

A capability eval asks "can the new model do harder things?" A regression eval asks "did it break anything that used to work?" You need both, and the regression set is the one that stops a fake +9% from shipping.

## 6. Step 5 — plug evals into CI

No green evals, no deploy. Every prompt edit, tool change, or model swap triggers a run.

This is eval-driven development: the eval set is a test suite for the agent, and it runs in CI like any other test suite. The practical guides say the same thing — wire the set into CI so every change triggers a run, and turn each new production failure into a new test case. That closes the loop: failures → transcripts → new tests → better agent → new failures, each one caught earlier than the last.

That is what "self-improving" means here. The eval does not improve itself by magic. It improves because every failure is harvested into the set, and the set is the thing that decides what ships.

## 7. Before you ship it — the checklist

- [ ] The eval set is built from real user prompts and real failures, not invented cases.
- [ ] The pass rate sits near the middle — high enough to mean something, low enough to discriminate.
- [ ] Every case scores the path, not just the answer — a right answer by the wrong route fails.
- [ ] The same fixed set re-runs on every model swap, prompt edit, and tool change.
- [ ] Failures are harvested: each one becomes a new test case.
- [ ] Deploys are gated on green evals — no green, no ship.
- [ ] Someone reads the transcripts, not just the dashboard number.

If any box is unchecked, you don't have an eval system. You have a dashboard.

## 8. Verified vs creator claims

**Verified:**
- The talk is real — "Why Most AI Agents Fail—and How Anthropic Builds Reliable Ones | Arize Observe 2026", speaker Marius Buleandra of Anthropic, on the Arize AI YouTube channel. Its chapters cover evals, regression vs capability evals, mining production transcripts, and reading transcripts.
- The clip's words are verified directly against the talk transcript (6:16–6:52): two categories of evals, regression evals near 100% and saturated, capability evals as the more important half, "the best startups… put a lot of effort into… capability evals just to know what's possible". The slide in the clip frames names both kinds and their questions.
- The "two things to eval" passage is verified against the transcript (10:23–10:59): outcome *and* transcript, judged by an LLM judge or LLM agent that itself needs calibrating against human-labelled data.
- The 50% principle — evals near 100% pass carry no signal; evals must discriminate. Standard eval practice, multiple sources.
- Score the path, not just the answer — process vs outcome supervision is established (OpenAI, 2023); agent evals grade what the agent leaves behind.
- Failures → transcripts → new test cases — standard error-analysis-first practice (Hamel Husain; eval-set guides).
- Evals in CI — standard eval-driven development practice.
- The demo — verified by running `eval_demo.py` in this folder (2026-11-15): good agent answer 3/6, path 3/6, full 3/6, GATE PASS; `--bad` peeking agent answer 6/6, path 0/6, full 0/6, GATE FAIL.

**Speaker's claims, as relayed — not independently verified:**
- The +9% fake gain and the 6% bug-dodge. Buleandra's own anecdote from the talk — the words are verified directly against the talk transcript (13:10–14:50) and the three mechanisms against the slide in the Post 8 clip frames. Still his story, no second source: the figures are what he said happened, not independently measured facts.
- The exact "100 prompts" and "50% sweet spot" numbers are the speaker's working rules, not measured constants.
- His title: the source post calls him an "Anthropic Senior Engineer". The talk confirms he is at Anthropic; the exact title is not independently confirmed.

**What the source post adds:** @0xsojalsec's caption is a faithful summary of the talk's eval chapters — the five steps map onto the talk's own structure (evals essential → regression vs capability → mining transcripts → reading transcripts → scaling review). The post itself is a screenshot of the talk thumbnail, not a separate claim.

## 9. Where this comes from

From the AI Brain's evals pages, built from the research library: Post 3's Rule 3 (evals that can fail a release), the RAG scoreboard discipline (fixed questions, re-run after every change), and the guardrails-evals concept page. The regression-eval idea is Post 3's rule applied to model swaps: the same test, every time, no exceptions.

Related work by the same author: [HarnessLab](https://github.com/yashumani/HarnessLab) (agents are disposable, harnesses are durable), [Prefrontal](https://github.com/yashumani/Prefrontal) (a context compiler for agents), and [Talk2Data](https://github.com/yashumani/Talk2Data) (governed execution — the LLM interprets wording only; deterministic services do the work).

---

*Source: @0xsojalsec (Nov 14, 2026) on Marius Buleandra (Anthropic), Arize Observe 2026 — Instagram post: https://www.instagram.com/p/Dfv4DUVjFoq/ — talk: https://www.youtube.com/watch?v=ijlrwKiYYM4. Comment DECODED on the post to get this file. Governed AI, decoded — with evidence.*
