# Context engineering, simply explained

**The Decoded Series #5** — the full write-up for the Wed Nov 18 post.

**Source:** IBM Technology, "Context Engineering for AI Agents: 4 Failure Modes
to Avoid", presented by Martin Keen —
https://www.youtube.com/watch?v=BwXremQ-i6I
(~348K views — the most-viewed context engineering video on YouTube).
The post uses an 18.5-second clip from the video (64.0–82.5s in the original):
Keen's definition of context engineering and his setup of the four failure
modes. The rest of this wiki is the full picture from the video.

## The definition

> Context engineering is deciding what actually goes into the context window
> at each step of an agent's run.

The context window is everything the model can see while it works: the task,
the conversation history, tool definitions, retrieved documents, and the
agent's own notes to itself. Context engineering is the job of choosing what
goes in there — and what stays out.

The term was popularized by Dex Horthy in 2025.

## The four failure modes

Keen's example through the video is a migration agent: an AI agent given the
job of migrating an aging codebase to a new database driver. Four things go
wrong with its context window.

### 1. Context Poisoning — bad information becomes "truth"

A mistake gets into the context window somewhere, and then gets treated as
fact — because to the model, its own notes look like ground truth.

In the example, the agent skims the new driver's documentation, misreads it,
and writes itself a note: the new driver retries failed connections
automatically. The note is completely wrong. But once it is in the window, the
agent treats it as a fact and plans around it.

### 2. Context Distraction — long histories derail the agent

The sheer size of the history starts steering the agent. A language model is
a pattern-continuation machine, and when the context holds an hour of the
agent's own past actions, that history becomes the strongest pattern around —
stronger than the reasoning it picked up in training.

So instead of asking what the job needs next, the model drifts into doing
more of what it has already done. Agents in this state get stuck going over
old ground.

### 3. Context Confusion — too many tools hurt accuracy

This one comes from the tools. Every tool definition sits in the window
whether it actually gets used or not, and having more of them makes choosing
the right tool harder.

Keen cites a benchmark: a model failed a task when it was offered 46 tools,
then passed the very same task when it was only offered 19. That is tool
sprawl at work.

### 4. Context Clash — conflicting information breaks reasoning

The window contains information that disagrees with itself. The agent
eventually notices that no retries are happening, figures out the bad note was
wrong — and writes a correction into its history. Now both versions sit in the
window, presenting conflicting information, and the agent has to reason
through the contradiction.

## The four fixes

Keen's own summary: all four fixes work by throwing something away.

| Failure mode | Fix | What it means |
|---|---|---|
| Poisoning | **Validate** | Before a conclusion gets written down into the context window, check it against something. A false note that never gets written down cannot poison anything. |
| Distraction | **Compact** | When the history gets really long, the agent summarizes it. Compaction is lossy — a summary can drift — but a short summary steers less than an hour of raw history. |
| Confusion | **Curate** | The agent doesn't need 46 tools for the task. Keep only the tools the task actually needs in the window. |
| Clash | **Prune** | When information gets superseded, cut the old version out. If the context disagrees with itself, the fix is to remove the part that is wrong. |

## The lesson

Keen's question, answered by the whole video: how does an agent get better at
long tasks by holding less context? By throwing things away. Every fix above
removes something from the window — a false note, a long history, unused
tools, a superseded version — and the agent gets better because the window
holds less, and what it holds is more trustworthy.

**Better by holding less.**

## The governed-AI lens

This is the core idea of this page, which is why the video is Decoded #5.
Everything the page has covered so far is a way of governing what goes into
context:

- **The checker (Post 3, Rule 1)** is validation: the worker never grades its
  own work, and a conclusion never becomes "truth" without a separate check.
  That is the fix for poisoning, built into the harness.
- **The allowlist (Post 3, Rule 2)** is curation: only the tools the job is
  allowed to use are ever in the window. That is the fix for confusion,
  enforced before the agent runs.
- **Evals that can fail a release (Post 3, Rule 3)** are the guardrail that
  catches a poisoned or distracted run before it ships — the check that the
  window held the right thing.
- **RAG (Post 4)** is curation of knowledge: retrieve the right page before
  the agent answers, instead of letting the whole document store into the
  window.

Context engineering is not a separate topic from governed AI. It is the same
job, stated from the model's side: decide what goes into the window, and the
harness, the checker, and the evals are how you enforce that decision.

## Credit

- Video: IBM Technology, "Context Engineering for AI Agents: 4 Failure Modes
  to Avoid", Martin Keen — https://www.youtube.com/watch?v=BwXremQ-i6I
- The 18.5s clip in the post is used for commentary, with credit on screen,
  in the caption, and here. Watch the full video for the migration-agent
  example in full — the failure modes and the fixes are all Keen's.
- The term "context engineering" was popularized by Dex Horthy (2025).
