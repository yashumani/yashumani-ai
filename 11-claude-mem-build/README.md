# Agent memory — the fix: build the 7-file version, locally

> **The one line:** memory without the bill — build the 7-file version, and keep it local.
>
> **The fix:** the last post showed the problem (your agent forgets everything) and the catches (the hosted default, the silent upload, the unauthenticated worker). This one is the fix in two parts: rebuild the mechanism in 7 Python files so you own it, and install the real plugin the safe way — local provider, keep-everything-local, no hosted default.
>
> This is the full wiki behind the @yashumani.ai Post 11 motion Reel

> *Clip source: Alex Newman, "AI Agents Finally Share One Memory (Claude Mem Explained)" — https://www.youtube.com/watch?v=oGSShssjn9c — clip used 02:23–02:45 (web client, 1920×1080 source).*

---

## 1. The 7-file build — the mechanism, owned

The source carousel rebuilds the claude-mem idea from scratch in 7 Python files. The point is not to replace the plugin — it is to own the mechanism, so you can see every step and no installer decides anything for you.

The four moves, each with its one-line meaning:

**1. Lifecycle hooks — memory that wraps any agent loop.** A hook is a function that runs at a fixed point in the agent's life: session start, prompt submitted, tool used, session end. The build wraps the loop so every step is recorded as it happens, without the agent having to remember to remember. *(Config: `src/config.py` — paths, models, token limits; Groq API key, `MAX_AGENT_STEPS`.)*

**2. Compression — 1,187 tokens of tool output into an 83-token note.** A second, cheaper model reads each tool call and writes one short observation: what happened, in one line. The session's transcript is thousands of tokens; the observation is the part worth keeping. *(Deepak's demo numbers — his, not a benchmark. The mechanism is what matters: compress at write time, not at read time.)*

**3. Hybrid search — exact words plus meaning, merged.** Two indexes over the same notes: **SQLite FTS5** for exact words (BM25 ranking — the classic keyword score) and **Chroma** for meaning (vector similarity). Results merge with **RRF** (reciprocal rank fusion — a standard way to combine two ranked lists without tuning weights). Keyword search finds the exact function name; vector search finds the idea you described differently.

**4. Layered retrieval — ~231 tokens to start, full detail only on request.** A new session gets a short index first — the list of what exists, not the content. The agent reads the full observation only when it needs it. That is the whole token trick: you pay for the index on every session and for the detail only when it matters.

The store is two tables in SQLite with FTS5 (`sessions` and `observations`, triggers, stopwords), plus the Chroma vector index. No vector DB server. Free Groq key. Local embeddings.

The demo below (`memory_demo.py`, standard library only) runs the core of it: store three observations, search by keyword with BM25, and show the layered retrieval — index first, detail on request.

## 2. The safe install — local provider, keep-everything-local

If you install the real plugin instead of the rebuild, the install is a decision, not a default. The checklist, in order:

1. **Update first.** Version 15.8.3 (Nov 2, 2026) or later — earlier versions uploaded prompts without asking, and updating does not remove what was already uploaded.
2. **Pick the local provider.** The installer pre-selects CMEM Pro (hosted on cmem.ai, 30-day trial, then $30/month). Choose instead: your own Anthropic plan (`--provider claude`), your own OpenRouter or Gemini key, or the already-logged-in agent over local loopback (`--provider host`). The summarising then runs on your provider, not theirs.
3. **Take the keep-everything-local option.** v15.8.3 asks first and offers it. Say yes.
4. **Know what the worker is.** It runs a background service on port 37777 with no authentication — by the maintainer's explicit choice. That is the audit finding from the last post. Keep it on localhost, don't expose it, and know that anything on your machine can read the store.
5. **Check the built-in first.** Claude Code ships auto memory since v2.1.59+ (MEMORY.md files per project). For light use, that may already be enough — no worker, no second model.

## 3. What it costs

The honest bill, in three lines:

- **Tokens:** the observer model costs model tokens on whichever provider you pick — every tool call gets summarised. That is the real running cost, and it is why the observer is the cheapest fast model, not the best one.
- **Disk and RAM:** light personal use, roughly 100–200 MB total; heavy use, 500+ MB RAM and a store that grows a few hundred MB a month.
- **Complexity:** hooks on every project, a background worker, a second model to configure. The built-in auto memory costs none of that.

Memory is not free. The question is who you pay — your own provider, or a hosted service that reads your prompts.

## 4. Verified vs creator claims

**Verified:**
- The mechanism is as described: lifecycle hooks, observer compression, SQLite + Chroma, hybrid search with RRF, layered retrieval. The build's four moves match the plugin's architecture (hooks → observations → dual store → progressive disclosure).
- The safe-install checklist is the plugin's own documented paths: `--provider claude`, OpenRouter/Gemini keys, `--provider host` loopback, and the v15.8.3 keep-everything-local option.
- The demo (`memory_demo.py`) was run: store → keyword search (BM25) → layered retrieval works on standard-library SQLite alone. The Chroma vector half is the plugin's, not the demo's — the demo shows the keyword half and the layering.
- Claude Code's built-in auto memory (v2.1.59+, MEMORY.md files) is real and is the light-use alternative.

**Creator's claims, as relayed — not independently verified:**
- The 1,187 → 83 token compression and the ~231-token starting index are Deepak's demo numbers. They show the mechanism working once; they are not a benchmark and not a guarantee for your sessions.
- "Free Groq key. Local embeddings. No vector DB server." — true of the DIY rebuild. The plugin itself needs Node.js 20+, auto-installs Bun and uv, and runs a background worker.
- The clip's cross-agent demo (one memory shared across agents) is the maintainer showing his own tool — it demonstrates the feature; it is not an independent test.

**What the source post adds:** Deepak's carousel is the build tutorial this post is built on. Its last slide pushes a paid subscription (Rs.45/month) for the full PDF — a standard funnel, not part of the technical claim.

Memory, owned and local. That is the fix.

---

*Source: Deepak Jose (@datasciencebrain), "Build Claude-Mem From Scratch: Persistent Memory for Any Agent" (Nov 17, 2026) — Instagram post: https://www.instagram.com/p/Df3ikZPE7_H/ — claude-mem: https://github.com/thedotmack/claude-mem — clip: Alex Newman, "AI Agents Finally Share One Memory (Claude Mem Explained)" — https://www.youtube.com/watch?v=oGSShssjn9c. Comment DECODED on the post to get this file. Governed AI, decoded — with evidence.*
