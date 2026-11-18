# Agent memory — the problem: your agent forgets everything (and the fix has an install screen)

> **The one line:** your agent forgets everything when the session ends — and the tool that remembers it has an install screen worth reading first.
>
> **The problem:** a coding agent starts every session cold. It keeps a transcript of the last session on disk, but the next session doesn't read it. So you re-explain the project, the decisions, and the bugs — every time.
>
> This is the full wiki behind the @yashumani.ai Post 10 motion Reel

> *Clip source: AICodeKing, "I Tried this Trending Opensource Claude Code Plugin & IT'S ACTUALLY CRAZY!" — https://www.youtube.com/watch?v=3Zq4cceOTa4 — clip used 00:49–01:13 (24.5s), downloaded via web client, 1920×1080 source.*

---

## 1. The amnesia problem — every session starts cold

Claude Code keeps a transcript of the session on disk. A new session does not read it.

That is the whole problem. The model did the work, learned the project, made the decisions — and the next morning none of it is in context. You re-explain the architecture, re-state the constraints, re-discover the bug you already fixed. The agent is not forgetful by design; it is forgetful because nothing carries the context across the session boundary.

This is not a model problem. It is a memory problem. The fix is a layer that watches what the agent does, writes down what matters, and puts the relevant slice back into the next session before it starts.

That layer is what claude-mem is.

## 2. What claude-mem does — capture, compress, inject

claude-mem (thedotmack/claude-mem, Apache-2.0, by Alex Newman) is the most-starred answer to the amnesia problem: **~115,631 stars and 10,039 forks on Nov 10, 2026**, version 15.15.1, 4,216 commits, changelog shipping most days. It installs for Claude Code, Codex, Cursor, OpenCode, Gemini, Copilot, and more.

It works in three moves:

1. **Capture.** It registers lifecycle hooks into the agent — SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop, SessionEnd. Every step the agent takes is recorded as it happens.
2. **Compress.** A second, cheaper model (the "observer") reads each step and writes it down as a short observation — a note, not a transcript. Observations, sessions, and summaries go into a local store.
3. **Inject.** When a new session starts, the SessionStart hook injects a short context index from the last sessions — a three-layer progressive disclosure: a short index first, full detail only on request.

The store is local and dual: **SQLite** (`~/.claude-mem/claude-mem.db`) for the observations, with **Chroma** on top for vector search and SQLite's own full-text search (FTS5) for keywords. Hybrid search merges the two.

The idea is sound. A second agent takes notes so the first one doesn't have to start cold. The mechanism is the reason for the star count.

## 3. The catches — read the install screen first

Here is where the governed part matters. Three catches, all verified against the project's own docs and independent write-ups:

**Catch 1 — the installer pre-selects the hosted plan.** The install steers you toward CMEM Pro, a hosted service on cmem.ai that runs the summarising for you: 30-day free trial, then **$30 a month** (Heavy $70, Max $100 tiers), card required. The core plugin is free and Apache-2.0 — but the default path is the paid hosted one, and the summarising then happens on someone else's server.

**Catch 2 — it uploaded your prompts without asking.** Browser setup in versions **15.2.0 to 15.8.2 uploaded the last 30 days of prompts to cmem.ai without asking**. Version 15.8.3 (Nov 2, 2026) asks first and offers a keep-everything-local option — but it does **not** remove prompts that were already uploaded. Update before running setup, and pick the local option deliberately.

**Catch 3 — the local worker has no authentication.** The background worker runs a local HTTP service (port 37777) that exposes 30+ endpoints with no authentication at all. Two independent security audits, in February and March 2026 — one automated, one a manual community review — rated it HIGH risk: one endpoint returned Anthropic, Gemini, and OpenRouter API keys in cleartext, plus a path-traversal flaw in the search tools that could read arbitrary files such as SSH keys. The maintainer closed the audit issue in April 2026. The hooks that make capture effortless also write API keys, credentials, and proprietary source straight into a local store whose read and write API ships, by the maintainer's explicit choice, with no authentication.

And one more, quieter catch: **Claude Code now ships built-in auto memory** (since v2.1.59+), writing MEMORY.md files per project. For light use, the plugin is partly redundant — check what the built-in already does before adding a background worker and a second model to your setup.

None of this makes the tool unusable. It makes the install a decision, not a default. That is the whole point of this post.

## 4. The conflation flag — 118K stars is not 7 files

The source carousel for this post says two things: "claude-mem has ~118K GitHub stars" and "the idea behind it fits in 7 Python files." Both are true — about **different things**.

The ~118K stars belong to the **plugin** — a large project (4,216 commits, version 15.15.1, a background worker, an MCP server, installers for a dozen agents). The "7 Python files" is **Deepak Jose's from-scratch rebuild of the idea** — a tutorial that re-implements the mechanism (hooks, compression, hybrid search, layered retrieval) in miniature. The rebuild is a good way to learn the mechanism. It is not the plugin, and the plugin's star count is not evidence for the rebuild.

## 5. Verified vs creator claims

**Verified:**
- claude-mem is real — thedotmack/claude-mem, Apache-2.0, by Alex Newman; 115,631 stars / 10,039 forks as of Nov 10, 2026 (README, version 15.15.1); 4,216 commits; supports Claude Code, Codex, Cursor, OpenCode, Gemini, Copilot, and more.
- The mechanism is as described: lifecycle hooks (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop, SessionEnd), an observer model compressing steps into observations, SQLite + Chroma storage under `~/.claude-mem/`, progressive disclosure at session start.
- The CMEM Pro default: the installer pre-selects the hosted service (30-day free trial, then $30/month, card required). The core stays free and Apache-2.0.
- The silent prompt upload: browser setup in v15.2.0–v15.8.2 uploaded the last 30 days of prompts without asking; v15.8.3 (Nov 2, 2026) asks first and offers keep-everything-local, but does not remove earlier uploads.
- The security audits: February and March 2026, rated the worker API HIGH risk — 30+ unauthenticated endpoints, one returning API keys in cleartext, path-traversal flaw. The maintainer closed the audit issue in April 2026.
- Claude Code ships built-in auto memory since v2.1.59+ (MEMORY.md files per project).

**Creator's claims, as relayed — not independently verified:**
- The caption's "~118K stars" — plausible (115,631 on Nov 10, gaining roughly a thousand stars a day), but the exact figure was not re-checked against the GitHub API at filing time.
- Deepak's compression figure — 1,187 tokens of tool output → an 83-token note — is his demo's numbers, not a benchmark. It shows the mechanism; it does not measure it.
- "Free Groq key. Local embeddings. No vector DB server." — true of the DIY rebuild; the plugin itself needs Node.js 20+, auto-installs Bun and uv, and runs a background worker.

**What the source post adds:** Deepak's carousel is a build-it-yourself tutorial, not a review of the plugin. Its last slide pushes a paid subscription (Rs.45/month) for the full PDF — a standard funnel, not part of the technical claim.

That is the problem. The fix — the 7-file build and the safe local-only install — is the next post.

---

*Source: Deepak Jose (@datasciencebrain), "Build Claude-Mem From Scratch: Persistent Memory for Any Agent" (Nov 17, 2026) — Instagram post: https://www.instagram.com/p/Df3ikZPE7_H/ — claude-mem: https://github.com/thedotmack/claude-mem. Comment DECODED on the post to get this file. Governed AI, decoded — with evidence.*
