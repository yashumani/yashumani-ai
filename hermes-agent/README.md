# Hermes Agent — The agent that rewrites its own skills

> **The one line:** Hermes Agent is a free, open-source agent that lives on your own machine, remembers across sessions, and — its headline idea — turns experience into reusable skills it improves over time.
>
> **The checker's question:** if the agent writes its own skills, who verifies them? A learning loop without a check is just a faster way to repeat a mistake.
>
> This is the full wiki behind the @yashumani.ai Hermes Agent Reel. The Reel shows the loop live in under two minutes. This file is the complete version: what Hermes is, how the loop actually works, what runs unattended, what an independent audit found, and the checklist for using it safely.

---

## 1. What Hermes Agent is

Hermes Agent is an autonomous AI agent built by **Nous Research**, first released on **February 25, 2026** (v0.1.0) under the **MIT License** — free and open source. Source: the project's own repository and site.

- **Repository:** https://github.com/NousResearch/hermes-agent
- **Site:** https://hermes-agent.nousresearch.com

Verified from the project's README and documentation:

| Fact | What the sources say |
|---|---|
| **Where it runs** | On your own computer or server, as a long-lived process — "a $5 VPS, a GPU cluster, or serverless infrastructure"; six terminal backends (local, Docker, SSH, and others) |
| **Which model** | Model-agnostic: Nous Portal, OpenRouter, OpenAI, "your own endpoint, and many others" — switch with `hermes model`, no code changes |
| **Where you talk to it** | A terminal UI, plus a single gateway process serving Telegram, Discord, Slack, WhatsApp, Signal and CLI, with cross-platform conversation continuity |
| **Memory** | Persistent across sessions: agent-curated memory, FTS5 session search with LLM summarisation for cross-session recall, and Honcho-based dialectic user modelling — it builds a model of who you are |
| **Schedules** | A built-in cron scheduler, jobs described in natural language, delivered to any platform — daily reports, nightly backups, weekly audits, running unattended |
| **Delegation** | It can spawn isolated subagents for parallel workstreams |

One caution on popularity: Hermes became one of the most-starred agent repositories on GitHub in 2026, but star counts in secondary coverage vary wildly, and some coverage questions how organic that growth was. Popularity is not evidence either way — judge the mechanism and the record, which is what the rest of this file does.

## 2. The headline idea: the learning loop

The README's own words: *"It's the only agent with a built-in learning loop — it creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions."*

Unpacked, the loop is four steps:

```
Experience  →  Skill  →  Memory  →  Better next run
   ↑                                        │
   └────────── skill refined in use ────────┘
```

1. **Experience.** The agent does a hard task — not a demo task, a real one, with real friction.
2. **Skill creation.** After a complex task, it writes down *how it solved it* as a reusable skill (compatible with the agentskills.io open standard). This is autonomous: nobody has to tell it to save the method.
3. **Memory.** The skill is stored alongside curated memory and the user model, and past conversations are searchable, so the next session starts from everything the previous ones learned.
4. **Reuse and refinement.** Next time a similar task appears, the agent loads the skill instead of starting over — and, per the project, improves the skill during use. A background "curator" process periodically reviews the skill library, moving skills between active, stale and archived states so they don't pile up forever.

**You can watch step 2 happen.** In NetworkChuck's demo video (the clip in the Reel), his Hermes agent finishes setting up a network tool, gets a new instruction — "Search the network, see what you can find" — and, unprompted, first saves the setup method: the terminal shows `Self-improvement review: skill "twingate-client-operations" created`. Nobody asked it to do that. That is the loop, caught live.

### Claim vs evidence — keep them separate

| Statement | Status |
|---|---|
| Hermes creates reusable skills from experience, autonomously | **Verified mechanism** — documented in the README and shown live in independent demos |
| Hermes keeps persistent memory and a user model across sessions | **Verified mechanism** — documented; memory files and session search are inspectable |
| Hermes runs scheduled jobs and works via messaging platforms | **Verified mechanism** — documented gateway + cron scheduler |
| "It gets better the longer it runs" / skills measurably improve with use | **Project claim** — no independent benchmark verification was found. The loop exists; whether its output *improves* outcomes is unproven in public |
| "The only agent with a built-in learning loop" | **Project marketing claim** — the README's wording, not an independently established fact |

That last distinction is the whole lesson of this post: a mechanism you can watch is a fact; an improvement you cannot measure is a claim.

## 3. What runs unattended

Because Hermes is a long-lived process with a scheduler and a messaging gateway, a lot happens while you are not watching:

- Scheduled jobs fire on their own — reports, backups, audits — and deliver results to Telegram, Slack, Discord and the rest.
- Anyone who can message the gateway can give it work (subject to its access controls).
- Subagents run in parallel on delegated tasks.
- The learning loop itself runs in the background: memory nudges, skill creation after complex tasks, and the curator's periodic skill review.

None of that is a flaw by itself — it is the product. But it changes the trust question from "is this one answer right?" to "what can this process do, write, and keep, while nobody is looking?" That is a governance question, and it has a concrete record to check.

## 4. The governance record: the v0.8.0 audit

On **April 11, 2026**, an independent security researcher (@Anic888) published an audit of **Hermes Agent v0.8.0** on the project's own issue tracker (issue #7826), later summarised in a Cloud Security Alliance research note (May 2026). It reported **four critical and nine high-severity findings in the default configuration**, including:

- **Shell-command screening by pattern matching.** The terminal tool passed commands to a shell, guarded by regex-based detection the audit found bypassable — so in the default setup, the model's judgement was effectively the last line of defence for arbitrary command execution.
- **File reading with no deny list.** The file tool could read anything the process could read — including, for example, SSH keys.
- **Approvals skipped in containers.** The approval logic was unconditionally bypassed in containerised environments — the deployment many people would assume is the *safer* one had the "are you sure?" step switched off.
- **Persistent skill injection.** Because the agent can write skills that persist across sessions, a malicious or manipulated skill, once planted, survives — the learning loop's memory becomes the persistence mechanism.

The audit findings carry no CVE identifiers, and the CSA note records no patch status for them and no response from Nous Research at the time of writing; the project has shipped many releases since v0.8.0. Separately, several CVEs in Hermes components were disclosed in 2026 (for example a symlink flaw in the file tools, fixed in v0.9.0). Read the audit as what it is: a dated, version-specific record about the *default configuration* — and a permanent lesson about what to check in *any* self-modifying agent, Hermes included, at whatever version you run.

Notice the shape of the problem. It is not "the model made a mistake." It is:

> The system that writes the skills is the same system that decides the skills are good. There is no second pair of eyes inside the loop.

That is exactly the failure the Decoded Series keeps coming back to: **a check that cannot stop the run is not a check — and a learner that grades its own homework has no check at all.**

## 5. Before you trust it — the checklist

For Hermes, or any agent that creates and reuses its own skills:

- [ ] **Read every skill the agent creates** before its second run uses it. Treat agent-written skills like code from a stranger: useful, unreviewed.
- [ ] **Keep approval prompts on** — and verify they actually fire in your deployment, especially in containers.
- [ ] **Run it sandboxed first** (Docker or an equivalent fence), with the smallest toolset the job needs. Freedom is earned, not default.
- [ ] **Fence the files.** Know what the process can read — credentials and keys should be outside its reach unless the job truly needs them.
- [ ] **Pin and review updates.** A fast-moving project changes its defaults; re-check the security-relevant settings after upgrades, and know which version you are running relative to published audits and fixes.
- [ ] **Audit the memory.** Periodically read what it has stored about you and what skills exist. Delete what should not persist.
- [ ] **Measure the claim yourself.** If "self-improving" matters to you, keep a few repeat tasks and compare results over time. Your benchmark beats their tagline.

If you cannot tick the first two boxes, you do not have a self-improving agent. You have an unsupervised one.

## 6. Where this comes from

Primary sources, checked 2026-11-24:

- Nous Research, *Hermes Agent* repository and README — https://github.com/NousResearch/hermes-agent (MIT License; learning loop, memory, gateway, scheduler, backends as quoted above)
- Hermes Agent official site — https://hermes-agent.nousresearch.com
- Anic888, "Security Audit: 4 Critical, 9 High severity findings in default configuration" — NousResearch/hermes-agent issue #7826, April 11, 2026 (via the project's issue tracker)
- Cloud Security Alliance, research note on Hermes Agent CVEs, May 4, 2026 — summarises the audit and lists CVE-2026-7396, CVE-2026-7397, CVE-2026-6829
- Clip source: NetworkChuck, "you need to use Hermes RIGHT NOW!! (goodbye OpenClaw!!)" — https://www.youtube.com/watch?v=QQEgIo4Juxg (skill-creation moment at ~20:15–20:32; short clip used for commentary and teaching, with credit)

---

*Source: @yashumani.ai — "This agent rewrites its own skills." Comment DECODED on the Reel to get this file. Governed AI, decoded — with evidence.*
