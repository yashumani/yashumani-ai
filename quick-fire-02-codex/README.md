# Codex: 20 commands in 60 seconds (Quick-fire Ep. 2)

> **The one line:** twenty Codex CLI commands, in four beats — start and steer, review the work, control context, tools and threads. Every one verified against the shipped CLI itself.
>
> **The list:** /init, /model, /permissions, /plan, /status, /review, /diff, /mention, /ps, /feedback, /compact, /new, /clear, /resume, /fork, /mcp, /apps, /subagents, /experimental, /statusline.
>
> This is the full wiki behind the @yashumani.ai Quick-fire Ep. 2 motion Reel. The Reel runs the 20 in four beats of five, with the one-line use for each on screen. This file is the complete version: the same twenty with the same one-line uses, how each was verified, the two November-list commands that did not survive re-verification, and the swaps.

> *Source note: the official slash-commands page — https://developers.openai.com/codex/cli/slash-commands — now redirects to a ChatGPT desktop app commands page (checked 2026-11-22), so it no longer serves the CLI list. This list was verified instead against the shipped CLI's own source: `codex-rs/tui/src/slash_command.rs` in OpenAI's openai/codex repo at release tag `rust-v0.171.0` (Codex CLI 0.171.0, released 2026-11-20), cross-checked at tags 0.165.0 and 0.169.0 and against a verbatim mirror of the official page. Format inspired by @chase.h.ai — his 20-in-64s reel (https://www.instagram.com/reel/DfqvfB9IPA5/) is the series template.*

---

## 1. Beat 1 — Start & steer

| Command | What it does |
|---|---|
| `/init` | Generate an AGENTS.md scaffold in the current directory. |
| `/model` | Choose the active model and reasoning effort. |
| `/permissions` | Set what Codex can do without asking first. |
| `/plan` | Switch to plan mode before implementing. |
| `/status` | Show session config and token usage. |

## 2. Beat 2 — Review the work

| Command | What it does |
|---|---|
| `/review` | Ask Codex to review your working tree. |
| `/diff` | Show the Git diff, including untracked files. |
| `/mention` | Attach a file to the conversation. |
| `/ps` | Show background terminals and their recent output. |
| `/feedback` | Send logs to the Codex maintainers. |

## 3. Beat 3 — Context control

| Command | What it does |
|---|---|
| `/compact` | Summarize the conversation to free tokens. |
| `/new` | Start a new conversation in the same CLI session. |
| `/clear` | Clear the terminal and start a new chat. |
| `/resume` | Resume a saved conversation. |
| `/fork` | Fork the conversation into a new thread. |

## 4. Beat 4 — Tools & threads

| Command | What it does |
|---|---|
| `/mcp` | List configured MCP tools. |
| `/apps` | Browse apps and insert one into your prompt. |
| `/subagents` | Switch between this session's subagents. |
| `/experimental` | Toggle experimental features. |
| `/statusline` | Configure the TUI status-line fields. |

Notes on individual commands: `/apps` inserts the app into your prompt as `$app-slug`. `/permissions` is the current name for the older `/approvals`, which the docs say still works as an alias but no longer appears in the slash popup.

---

## 5. The honest flags

- **`/personality` was dropped.** It is in the official-page copy (friendly / pragmatic / none) and was on this episode's November draft list, but it is **not in the shipped CLI**: the slash-command source at tags 0.165.0, 0.169.0, and 0.171.0 has no such command. What survives is a `personality` key in config.toml — a setting, not a slash command. Any reel listing `/personality` today is working from the stale page copy.
- **`/agent` was replaced by `/subagents`.** The singular `/agent` ("switch the active agent thread") is also absent from the shipped source. The shipped commands are `/subagents` — "switch between this session's subagents," the same job — and `/agents`, which opens the Agent Command Center added in 0.167.0. This episode uses `/subagents`.
- **`/clear` is in — and this time it's verified.** In November it appeared in third-party guides but not in the official-page copy, so it was excluded. It is present in the shipped 0.171.0 source ("clear the terminal and start a new chat"), so it takes the twentieth slot.
- **The official docs URL moved.** https://developers.openai.com/codex/cli/slash-commands redirects to a ChatGPT desktop app commands page whose short list (`/feedback`, `/goal`, `/init`, `/mcp`, `/plan`, `/review`, `/status`) is the desktop app's composer set, not the CLI's. The CLI list above comes from the CLI's own source; the mirror of the old official page (dev-docs.moodybeard.com) agrees with the source on 18 of the 20 and is stale exactly on `/personality` and `/agent`.
- **Availability varies.** A few shipped commands are platform- or build-gated (for example `/app` is macOS/Windows only). None of the twenty above is gated that way in the source, but experimental-adjacent behaviour can still vary by version and account.
- **These CLIs ship weekly.** 0.171.0 landed 2026-11-20, two days before this check. This list was verified against the shipped source on 2026-11-22. Re-check before any repost or reuse — as `/personality` shows, commands disappear without the docs page changing.

## 6. Swaps if a command drops

Verified present in the same 0.171.0 source, in case a re-check removes one of the twenty: `/goal` (set or view the goal for a long-running task), `/skills` (use skills to improve how Codex performs specific tasks), `/agents` (open the agent command center), `/copy` (copy the last response), `/export` (export the conversation as markdown), `/rename` (rename the current thread), `/usage` (view account usage), `/logout` (log out of Codex), `/quit` and `/exit` (exit the CLI).

---

## Next episode

**Quick-fire Ep. 3 — Grok Build.** The surprise pick: xAI's terminal coding agent, with two commands no other CLI in this series has — `/imagine` and `/imagine-video`, image and video generation inside the terminal. After that: Gemini CLI (with the honest catch — no longer free for personal Google sign-in since June 2026), Cursor CLI, and the Grok chatbot features list as the non-coding closer.
