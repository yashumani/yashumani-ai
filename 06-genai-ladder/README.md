# Gen AI in 10 steps — the ladder

> **The one line:** using AI and building with it are 10 ideas apart.
> Climb in order — each rung uses the one below it.
>
> This is the full wiki behind the @yashumani.ai Post 6 motion Reel
> (Decoded Series #6). The Reel opens with a clip from KodeKloud, then
> climbs the ladder in three bands.
> This file is the complete version: all 10 rungs, the rule that matters
> for each, and the check that keeps it honest.
>
> *Source notes: the ladder shape is prompted by Deepak Jose's 10-step
> ladder (@datasciencebrain); the take here is our own. The clip is
> KodeKloud's "Don't learn AI Agents without Learning these Fundamentals"
> (https://www.youtube.com/watch?v=ZaPbP9DwBOE) — the 40-second opening
> (0–40.3s): prompt engineering, context windows, tokens, embeddings,
> RAG, vector DB, MCPs, agents, LangChain, LangGraph — six of the
> ladder's ten rungs named in one breath (tokens, embeddings, context
> window, RAG, MCP, agents), then "we'll start with AI fundamentals,
> then move on to RAG, vector DB, LangChain, LangGraph, MCP, prompt
> engineering, and finally put it all together with a complete system"
> — and "Let's start with the basics."*

---

## The shape: three bands

- **READ (1–4)** — how a model takes text in.
- **CONNECT (5–7)** — how it reaches beyond its own weights.
- **RUN (8–10)** — how you run it without it running you.

Skip a band and the next one has nothing to stand on. An agent with no
context discipline burns its budget; RAG with no embeddings retrieves
noise; evals with no known answers measure nothing.

---

## READ

### 1. Tokens — the model reads numbered pieces, not words

Text is cut into tokens before the model ever sees it. A word can be one
token or several, and the count changes with the language — the same
sentence costs more tokens in some languages than in others.

**The rule:** count tokens, not words, when you budget a prompt.
**The check:** if a prompt behaves differently across languages, look at
the token counts first.

### 2. Embeddings — text becomes a vector; similar meanings sit close

An embedding turns a chunk of text into a list of numbers — a point in a
high-dimensional space. Chunks with similar meanings end up near each
other, so distance becomes a stand-in for relevance.

**The rule:** similarity is a distance, not a judgement. Close means
"about the same topic", not "true".
**The check:** retrieve a chunk, read it, and ask whether it actually
answers the question — never trust the score alone.

### 3. Next-token prediction — the model scores options

A language model does one thing: given the text so far, it scores every
possible next token and picks one. Everything else — answers, code, plans
— is that loop repeated.

**The rule:** low temperature for decisions, higher temperature only for
drafts. Temperature is not creativity; it is randomness.
**The check:** if an answer must be the same every time, run it twice at
temperature 0. Different answers mean the prompt, not the model, is
undecided.

### 4. Context window — one fixed budget, shared by everything

The window is a fixed number of tokens, and everything shares it: the
system prompt, the conversation history, the retrieved documents, and the
answer being written. Every token you add to one side is a token taken
from another.

**The rule:** write down what lives in the window before you add to it.
**The check:** if the model starts forgetting the instructions, the
window is full — trim the history or the retrieved docs, not the rules.

---

## CONNECT

### 5. Tool calling — the model writes the request; your code runs it

The model never touches your systems. It writes a structured request —
"look up this customer", "draft this email" — and your code decides
whether to run it. The model proposes; the executor disposes.

**The rule:** the allowlist lives in your code, not in the prompt. If the
action isn't on the list, it never runs.
**The check:** log every tool call and who approved it. A call with no
log entry is a call that never happened — treat it as a bug.

### 6. MCP — one standard plug, not a custom integration each time

Without a standard, every tool needs its own custom wiring: its own
auth, its own schema, its own error handling. MCP (Model Context
Protocol) is one plug shape: a server exposes tools, resources, and
prompts, and any client that speaks MCP can use them.

**The rule:** standardise the plug, not the tool. The tool stays yours;
the way it connects becomes boring.
**The check:** a new tool should take configuration, not code. If adding
a tool means writing a new integration, the plug isn't standard yet.

### 7. RAG — retrieve the closest chunks, paste them into the prompt

RAG is three steps: embed your documents, retrieve the chunks closest to
the question, paste them into the prompt so the model answers from your
text instead of its memory.

**The rule:** grounding beats a bigger model. A small model with the right
chunk outperforms a large model guessing.
**The check:** the answer must cite the chunk it came from. No citation,
no trust — the model may be answering from memory.

---

## RUN

### 8. Agents — decide, act, observe; fewer steps beat better steps

An agent is a loop: decide what to do, act, observe the result, repeat.
The loop is the whole idea — and its weakness is arithmetic. Reliability
compounds against you: every step is a chance to fail.

```python
# how often a 20-step agent finishes if each step is 95% reliable
print(f"{0.95 ** 20:.1%}")  # 35.8%
```

At 95% per step, a 20-step task finishes only about 36% of the time.
At 99% per step it finishes about 82% of the time. The fix is rarely a
smarter model — it is fewer steps, a check after each one, and a hard
stop when the check fails.

**The rule:** fewer steps beat better steps. Cut the loop before you
upgrade the model.
**The check:** count the steps, multiply the reliabilities, and say the
number out loud. If the number is embarrassing, the design is wrong.

### 9. Evals — test with known answers; report kappa, not raw agreement

An eval is a fixed test set with known answers. Run the system, compare,
and the score means something — but only if the score measures what you
think it measures. Raw agreement between a judge and a human is the
classic trap: most cases are easy and passing, so two raters can agree
most of the time while the judge catches nothing on the hard cases.

Cohen's kappa corrects for that. It asks: how much do the raters agree
*beyond what chance would give*? A high raw agreement with a low kappa
means the agreement is mostly the easy cases. Report kappa alongside raw
agreement — never raw agreement alone.

**The rule:** the test set decides, not the demo. If the evals can't fail
a release, they are a dashboard, not quality control.
**The check:** every eval run ends in one of two states — ship, or
blocked. If "blocked" has never happened, the evals have never been
tested either.

### 10. Security — private data + untrusted input + a way out = a leak

Three ingredients make a leak: private data in the system, untrusted
input reaching it, and a way for the result to leave. Remove any one and
the leak closes. Leave all three and the model will eventually combine
them — a prompt in a document, a tool with broad permissions, an output
channel nobody watches.

**The rule:** nothing irreversible without human approval. The approval
gate is not a feature; it is the wall.
**The check:** for every tool and every output channel, name the human
who approves it. A channel with no approver is an open door.

---

## The checklist — the ladder on one sheet

1. Tokens — count tokens, not words.
2. Embeddings — similarity is distance, not judgement.
3. Next-token — low temperature for decisions.
4. Context — one budget, shared by everything.
5. Tool calling — the allowlist lives in your code.
6. MCP — standardise the plug, not the tool.
7. RAG — the answer cites its chunk, or it doesn't ship.
8. Agents — fewer steps beat better steps.
9. Evals — report kappa, not raw agreement.
10. Security — nothing irreversible without human approval.

---

## Principles

- Governed AI, decoded — with evidence.
- A check that cannot stop the run is not a check.
- Agents are disposable. Harnesses are durable.
