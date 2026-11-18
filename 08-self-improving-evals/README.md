# Self-improving evals — the problem: a fake +9%

> **The one line:** a dashboard can say your agent got 9% better while the model didn't improve at all.
>
> **The problem:** an agent without an eval that catches its own luck is a demo, not a system. A new model scored +9% on the dashboard — and the transcript showed the gain was fake.
>
> This is the full wiki behind the @yashumani.ai Post 8 motion Reel
(Decoded Series #8). The Reel tells the problem: the mistake, the
+9% story, and what the transcript found. The fix — the 5-step loop that
turns failures into better evals — is the next post (Decoded #9).

> *Clip source: "Why Most AI Agents Fail—and How Anthropic Builds Reliable Ones", Marius Buleandra (Anthropic), Arize Observe 2026 — https://www.youtube.com/watch?v=ijlrwKiYYM4. The Reel uses 12:48–13:10 (766.6–790.4s): the +9% story — he ran the evals on a new model, got a +9% score, and thought it was a breakthrough. The clip ends on that line; the Reel's slides deliver the twist (the gain was fake — the transcript caught what the dashboard missed). Downloaded via the web client, 1920×1080 H.264, no bot check.*

---

## 1. The mistake — graphs and loops, no eval that learns

Marius Buleandra of Anthropic, speaking at Arize Observe 2026 ("Why Most AI Agents Fail—and How Anthropic Builds Reliable Ones"), put it plainly: the biggest mistake in AI right now is building graphs and loops without a self-improving eval agent.

The failure mode is simple. A team builds an agent, watches it work on a few examples, ships it — and has no instrument that tells them when it starts failing. Agent errors compound across long-running workflows: one wrong step early becomes a wrong outcome late, and without evals there is nothing that catches the drift. The talk's own chapter list says it: "Why Evals Are Essential", "Regression vs Capability Evals", "Mining Production Transcripts for Evals", "Why You Must Read the Transcripts".

The eval is not a report card you check after shipping. It is the loop that fixes the agent — and this post is about what happens when that loop is missing.

## 2. The +9% story — a breakthrough that wasn't

Buleandra's story, as relayed in the source post: a new model showed a **+9% gain** on the dashboard. Re-running the same eval set showed the gain was fake — **6% of it was the model dodging a bug** rather than fixing it. The transcript caught what the dashboard missed.

What the transcript actually found — three lucky breaks, from his slide (visible in the clip frames) and his own words right after the clip (13:10–14:50, transcript-verified):

1. **World knowledge** — the agent used world knowledge to fill in an obvious category for missing data.
2. **SQL LIMIT** — it always added LIMIT to its SQL queries, which happened to circumvent a bug in the SQL execution tool. His words: "because it was using a limit, it was circumventing an issue with the harness."
3. **Date format** — a particular date format happened to reveal inconsistencies.

His slide's footer, in his own words on the slide: "None of it attributable to model capability."

Two flags on this one, stated plainly:

- **The numbers are the speaker's anecdote, not independently verified.** I did not watch the full talk, and no second source carries the +9% / 6% figures. Treat them as his story, not as data.
- **The principle is verified and load-bearing.** Regression evals exist precisely for this: the same fixed set, re-run on every change, so a model swap cannot silently trade one failure for another. Aggregate scores hide per-case changes — that is why the eval set is fixed and the transcripts are read, not just the headline number. The talk's own chapters name it: "Regression vs Capability Evals".

A capability eval asks "can the new model do harder things?" A regression eval asks "did it break anything that used to work?" You need both, and the regression set is the one that stops a fake +9% from shipping.

That is the problem. The fix — the 5-step loop — is the next post.

## 3. Verified vs creator claims

**Verified:**
- The talk is real — "Why Most AI Agents Fail—and How Anthropic Builds Reliable Ones | Arize Observe 2026", speaker Marius Buleandra of Anthropic, on the Arize AI YouTube channel. Its chapters cover evals, regression vs capability evals, mining production transcripts, and reading transcripts.
- The +9%/6% words were verified directly against the talk transcript (13:10–14:50) and the three mechanisms against the slide in the clip frames. Still his story, no second source: the figures are what he said happened, not independently measured facts.

**Speaker's claims, as relayed — not independently verified:**
- The +9% fake gain and the 6% bug-dodge. Buleandra's own anecdote from the talk.
- His title: the source post calls him an "Anthropic Senior Engineer". The talk confirms he is at Anthropic; the exact title is not independently confirmed.

**What the source post adds:** @0xsojalsec's caption is a faithful summary of the talk's eval chapters. The post itself is a screenshot of the talk thumbnail, not a separate claim.

---

*Source: @0xsojalsec (Nov 14, 2026) on Marius Buleandra (Anthropic), Arize Observe 2026 — Instagram post: https://www.instagram.com/p/Dfv4DUVjFoq/ — talk: https://www.youtube.com/watch?v=ijlrwKiYYM4. Comment DECODED on the post to get this file. Governed AI, decoded — with evidence.*
