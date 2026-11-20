# Claude Code: 20 commands in 60 seconds (Quick-fire Ep. 1)

> **The one line:** twenty Claude Code commands, in four beats — start and steer, review and verify, control context, branch and manage. Every one is from Claude Code's own docs.
>
> **The list:** /init, /plan, /model, /effort, /diff, /code-review, /security-review, /run, /verify, /insights, /clear, /compact, /context, /resume, /rewind, /branch, /fork, /tasks, /permissions, /doctor.
>
> This is the full wiki behind the @yashumani.ai Quick-fire Ep. 1 motion Reel. The Reel runs the 20 in four beats of five, with the one-line use for each on screen. This file is the complete version: the full table in the docs' own words, the two that are skills rather than built-in commands, and the commands that were removed and must not appear.

> *Source: Claude Code official commands reference — https://code.claude.com/docs/en/commands. All 20 commands below were re-verified against the live page on 2026-11-20 (page updated 2026-11-19T23:01:23Z). Format inspired by @chase.h.ai — his 20-in-64s reel (https://www.instagram.com/reel/DfqvfB9IPA5/) is the template; all five commands he names in the first 15 seconds (/insights, /run, /security-review, /init, /diff) were verified real.*

---

## 1. Beat 1 — Start & steer

| Command | What it does (docs wording) |
|---|---|
| `/init` | Initialize project with a `CLAUDE.md` guide. |
| `/plan` | Enter plan mode directly from the prompt. |
| `/model` | Switch the AI model and save it as your default for new sessions. |
| `/effort` | Set the effort level: `low` to `xhigh`, `max`, or `auto`. |
| `/diff` | Review the changes in your working tree, including the edits Claude has made so far. |

## 2. Beat 2 — Review & verify

| Command | What it does (docs wording) |
|---|---|
| `/code-review` | Review the current diff, or a PR number, branch, or path you pass, for correctness bugs. Alias: `/review`. |
| `/security-review` | Analyze the changes on your current branch for security vulnerabilities. |
| `/run` | Launch and drive your project's app to see a change working, not only passing tests. **Bundled skill, not a built-in command** — still slash-invokable. |
| `/verify` | Confirm a code change does what it should by building your project's app, running it, and observing the result, rather than relying on tests or type checks. **Bundled skill, not a built-in command** — still slash-invokable. |
| `/insights` | Generate an HTML report analyzing your recent sessions on this machine: which projects you work in, how you use Claude Code, where things go wrong, and features to try. |

## 3. Beat 3 — Context control

| Command | What it does (docs wording) |
|---|---|
| `/clear` | Start a new conversation with empty context. Aliases: `/reset`, `/new`. |
| `/compact` | Free up context by summarizing the conversation so far. |
| `/context` | Visualize current context usage as a colored grid. |
| `/resume` | Resume a conversation by ID or name, or open the session picker. Alias: `/continue`. |
| `/rewind` | Rewind the conversation and/or code to a previous point, or summarize from a selected message. Aliases: `/checkpoint`, `/undo`. |

## 4. Beat 4 — Branch & manage

| Command | What it does (docs wording) |
|---|---|
| `/branch` | Create a branch of the current conversation at this point, so you can try a different direction without losing the conversation as it stands. |
| `/fork` | Copy the current conversation into a new background session and keep working here. |
| `/tasks` | View and manage background work in the current session, including subagents that have finished. Also available as `/bashes`. |
| `/permissions` | Manage allow, ask, and deny rules for tool permissions. Alias: `/allowed-tools`. |
| `/doctor` | Run a setup checkup that diagnoses installation, settings, extension, and `CLAUDE.md` problems and proposes fixes that Claude applies after you confirm. Alias: `/checkup`. |

---

## 5. The honest flags

- **`/run` and `/verify` are bundled skills, not built-in commands.** The docs mark both as **Skill**. They work exactly like slash commands — type `/run`, it runs — but they are prompts handed to Claude, not behavior coded into the CLI. The Reel tags both `SKILL` on screen; the caption calls all twenty "commands" because that is the format's name and every one is slash-invokable.
- **Do not list `/vim`, `/pr-comments`, or `/ultraplan`.** All three are removed: `/vim` in v2.1.92, `/pr-comments` in v2.1.91, `/ultraplan` removed with no version note — use plan mode instead. Any reel listing them is stale.
- **Availability varies.** The docs note that not every command appears for every user — availability depends on platform, plan, and environment. `/desktop`, for example, only shows on macOS and x64 Windows when signed in with a Claude subscription.
- **These CLIs ship weekly.** This list was verified against the live docs on 2026-11-20. Re-check before any repost or reuse — commands get removed without warning.

## 6. Swaps if a command drops

Verified present on the same docs page, in case a re-check removes one of the twenty: `/usage` (session cost and plan usage limits), `/memory` (edit `CLAUDE.md` files, auto memory), `/mcp` (manage MCP server connections), `/background` (detach the session to run as a background agent), `/batch` (orchestrate large-scale changes in parallel), `/loop` (run a prompt repeatedly), `/schedule` (cloud scheduled tasks), `/export` (export the conversation as plain text).

---

## Next episode

**Quick-fire Ep. 2 — OpenAI Codex CLI.** The direct rival, same shape: 20 commands, four beats. One caveat to carry: the official Codex slash-commands page now redirects to the ChatGPT desktop app commands page, so the episode's wiki links the verbatim mirror and notes the move. After that: Grok Build (the surprise — `/imagine` and `/imagine-video` inside a terminal), Gemini CLI, Cursor CLI, and the Grok chatbot features list as the non-coding closer.
