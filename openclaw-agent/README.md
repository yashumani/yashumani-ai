# OpenClaw — the agent runtime that lives in your chat apps

> **The one line:** OpenClaw is not a chatbot and not a library. It is a free, open-source (MIT) agent *runtime* — a persistent background process on your own machine that you talk to through the chat apps you already use.
>
> **Runtime = Gateway + loop + memory + skills.** The Gateway is the control plane. The loop is how work gets done. Memory is what makes run two smarter than run one. Skills are how it gains new capabilities — and where the risk lives.
>
> This is the full wiki behind the @yashumani.ai OpenClaw Reel. The Reel teaches the shape in about two minutes. This file is the complete version: the architecture, the loop, the skill system, and the safety checklist.

---

## 1. What OpenClaw is — and is not

| | Chatbot app | Agent framework / library | **OpenClaw** |
|---|---|---|---|
| **What you get** | A chat window | Code you build an agent with | A running agent |
| **Where it lives** | A vendor's cloud tab | Inside your app | A background process on your hardware |
| **You reach it via** | Its website | Your own UI | WhatsApp, Telegram, Slack, Discord, … |
| **Model** | The vendor's | Your choice, wired by you | Your choice — Claude, GPT, Gemini, or local via Ollama |
| **When it works** | When you prompt it | When your code calls it | On your prompt — and on a heartbeat schedule |
| **Memory** | Session, maybe | You build it | Layered, persistent, stored on your disk |

OpenClaw was created by Peter Steinberger and first released in November 2025 (as Clawdbot, then briefly Moltbot, before settling on OpenClaw in January 2026). It is MIT-licensed, self-hosted, and model-agnostic. In early 2026 it became the most-starred agent repository on GitHub and the main open-source counterpart to hosted agent products and to Nous Research's Hermes Agent. (Star counts are deliberately not quoted here — check the repo for the current number.)

The mental model that matters: **an agent OS, not an app.** You don't open OpenClaw. It runs, the way a mail server runs — and your chat apps are its front door.

## 2. The architecture — four layers

```
WhatsApp ─┐
Telegram ─┤
Slack ────┤   Channels        one adapter per platform,
Discord ──┤   (Layer 1)       one normalised message format
…dozens ──┘        │
                   ▼
            ┌─────────────┐
            │   GATEWAY   │   a single long-lived process:
            │  (Layer 2)  │   WebSocket control plane —
            └─────────────┘   routing · sessions · lanes · policy
                   │
                   ▼
            Agent Runtime     receive → assemble → call model
            (Layer 3)         → run tools → respond → remember
                   │
                   ▼
            Model providers   Claude · GPT · Gemini ·
            (Layer 4)         local models via Ollama
```

### Layer 1 — Channels

A channel is an adapter for one messaging platform (the official docs list WhatsApp via Baileys, Telegram via grammY, Slack, Discord, Signal, iMessage, WebChat, and more; third-party channels extend the list to dozens). Each adapter does two jobs: normalise whatever that platform sends into one common message format, and serialise the agent's reply back out. The agent never speaks "WhatsApp" or "Telegram" — it speaks the common format, and the adapters translate.

Why this matters: the interface is the chat app already on your phone. There is no new app to install, no dashboard you must keep open.

### Layer 2 — The Gateway

The Gateway is the heart of the system: **one long-lived background process** on your machine (a daemon — `systemd` on Linux, `LaunchAgent` on macOS). Per the official architecture docs:

- It owns all messaging surfaces — it is the only process that holds a WhatsApp session, for example.
- Control clients (CLI, web UI, macOS app, automations) and paired devices ("nodes") connect to it over **WebSocket** (default bind `127.0.0.1:18789`).
- It routes every message to the right session, enforces policy and pairing/auth, and emits system events (`agent`, `chat`, `presence`, `health`, `heartbeat`, `cron`).
- **Per-session lanes:** runs are serialised per session — one session's tasks execute one at a time, in order, so two tasks in the same conversation can never race or interleave tool calls. (The official agent-loop doc: "a loop is a single, serialized run per session.")

This is the design decision worth stealing: a single control plane that every surface and every run passes through is what makes policy, logging, and approvals enforceable at all. If the agent could be reached around the Gateway, the Gateway's rules would be decoration.

### Layer 3 — The Agent Runtime

The runtime executes the loop (section 3). It assembles the context for each run — the conversation, the relevant memory, the skills snapshot — calls the model, executes the tool calls the model asks for, streams the reply back through the Gateway, and persists what happened.

### Layer 4 — Model providers

OpenClaw is model-agnostic. Cloud providers (Anthropic's Claude, OpenAI's GPT family, Google's Gemini) and local models (via Ollama) plug in behind the same interface. Swap the model and nothing else changes: same channels, same memory, same skills. The model is a component; the runtime is the product.

## 3. The loop

Per the official agent-loop documentation, a run is:

```
intake → context assembly → model inference → tool execution
       → streaming replies → persistence
```

In plain words, for every run:

1. **Receive** — a message arrives from any channel (or the heartbeat/cron fires).
2. **Assemble** — context is built: recent conversation + layered memory + the active skills.
3. **Call the model** — the model decides the next step.
4. **Run tools** — shell commands, file operations, browser control, API calls — executed by the runtime, not the model.
5. **Respond** — the reply streams back through the same chat app the message came from.
6. **Remember** — the run is persisted; memory is layered (working context, daily notes, long-term memory files on your disk, in Markdown), so the next run starts from what this one learned.

Two properties do the safety work:

- **Serialised per session.** No parallel tool chaos inside one conversation.
- **The heartbeat.** A scheduler wakes the agent at a configurable interval (every 30 minutes by default, per the community guide) so it can check in, follow up, and run standing tasks *without being prompted*. This is the feature that makes it feel alive — and the feature that makes its permissions matter even when you're not watching.

## 4. Skills and ClawHub

A **skill** is a small package that teaches the agent a new capability: a `SKILL.md` of instructions the agent follows, plus the tools and know-how for one job — browsing and summarising, triaging email, running a script, controlling a device.

Skills are published to **ClawHub**, OpenClaw's community registry. Thousands of skills are available, installable in one step. That openness is the ecosystem's engine: anyone can publish, and the agent can gain a capability its authors never built.

It is also, structurally, the ecosystem's weak point — see the next section.

## 5. The governance catch

Three facts, multiplied:

1. **The agent has real authority.** It can run shell commands, read and write files, browse, and act in your connected accounts.
2. **It lives where you chat.** The front door is WhatsApp/Telegram — apps designed for casual, fast messages, not for careful permission review.
3. **A skill inherits the agent's authority.** A skill is instructions + code that the agent follows with its own reach. There is no meaningful sandbox between "the skill's instructions" and "the agent's permissions."

And this is not hypothetical. Published security research in 2026 found the supply-chain risk already realised:

- **Unit 42 (Palo Alto Networks), 2026** — an analysis of ClawHub as "an emerging AI supply chain threat": skills are markdown-driven packages with broad local system access; researchers identified malicious skills that survived screening, in three categories — infostealers connecting to command-and-control infrastructure, a scanner-evasion skill (inflated file size to exceed scan thresholds), and "agentic" threats that manipulate the agent's own behaviour for financial gain. ClawHub responded to earlier campaigns by adding VirusTotal integration and ClawScan screening — and evasive skills were still found afterwards.
- **ICLR 2026 Workshop audit ("ClawdPwned")** — a large-scale audit of 2,556 public skills against the OWASP LLM Top 10 identified 49 likely-malicious skills, including credential harvesting and wallet-key theft; the most common mechanisms were sensitive-information disclosure and excessive agency.
- **Koi Security's "ClawHavoc" disclosure (Feb 2026)** — documented hundreds of malicious skills using fake prerequisite instructions to deliver the AMOS infostealer; Bitdefender Labs reported roughly 17% of the skills it analysed in the platform's first weeks carried malicious payloads.

The pattern to learn: **the registry is not the review.** Scanners help; they are not a guarantee. In this architecture, *installing a skill is granting a permission* — treat it with the same care as running an installer from a stranger, because that is what it is.

### Before you trust it — the checklist

- [ ] The Gateway binds to loopback (or a private tailnet/VPN) — never exposed raw to the internet.
- [ ] Pairing/approvals are on: new devices and senders must be approved before the agent obeys them.
- [ ] Exec approvals are on for shell commands — the agent asks before anything irreversible.
- [ ] Every skill is read before it is installed — the `SKILL.md` *is* the code; read it like code.
- [ ] Skills come from authors you can identify; a fresh account with a too-good skill is a red flag.
- [ ] The agent's accounts are scoped: a dedicated email/calendar beats your primary identity.
- [ ] Memory files are reviewed — memory poisoning is an attack; know what the agent "believes."
- [ ] You can answer, for last week: what did it do, with which tools, on whose instruction? If you can't, turn the heartbeat off until you can.

> **The rule that generalises:** an agent's safety is not a property of its model. It is a property of its gateway, its permissions, and what you install into it.

## 6. Where this comes from

- Official OpenClaw documentation — Gateway architecture (`docs.openclaw.ai/concepts/architecture`): single long-lived Gateway, WebSocket control plane on `127.0.0.1:18789`, channel adapters (Baileys/grammY/…), pairing and auth.
- Official OpenClaw documentation — Agent loop (`docs.openclaw.ai/concepts/agent-loop`): intake → context assembly → model inference → tool execution → streaming replies → persistence; runs serialised per session.
- Milvus community guide (2026-02-10) — history (Clawdbot → Moltbot → OpenClaw), MIT licence, local Markdown memory, heartbeat defaults.
- Unit 42, Palo Alto Networks (2026) — "OpenClaw's Skill Marketplace and the Emerging AI Supply Chain Threat."
- Krishna et al., ICLR 2026 Workshop on Agents in the Wild — "ClawdPwned: Malicious Instructions in the OpenClaw AI Agent Skills Repository" (audit of 2,556 skills; 49 likely malicious).
- Fireship — "The wild rise of OpenClaw..." (YouTube) — the clip used in the Reel, with credit; short clip for commentary/teaching only.

---

*Source: @yashumani.ai — "OpenClaw: the agent that lives in your chat apps." Comment DECODED on the Reel to get this file. Governed AI, decoded — with evidence.*

