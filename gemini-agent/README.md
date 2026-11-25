# The Gemini agent — an agent with an identity, a budget, and a boss's inbox

>
> **The one line:** at Gemini at Work (Oct 8, 2026), Google announced a single agent for all of work — one you give objectives, not instructions — and, unusually, published the governance to go with it: its own identity, per-project spending caps that pause it, and four security questions.
>
> **The honesty line:** everything in this wiki is what Google *announced*. The agent was described in contemporaneous reporting as a private preview with wider availability to come; Google's own keynote post gives no general-availability date and no agent-specific price. Announced is not the same as proven. This wiki separates the two throughout.
>
> This is the full wiki behind the @yashumani.ai Decoded Reel on the Gemini agent. The Reel shows the idea in about 105 seconds. This file is the complete version: what was announced, how Google says it is governed, what Google did not say, and the four questions as a checklist you can run on any agent — including your own.

> *Clip source: Google Cloud, "Gemini at Work 2026 in 2 Minutes" — https://www.youtube.com/watch?v=ODQtU9TNlKA — clip used 01:33–02:03 (30.3s), the governance segment, downloaded via web client, 1920×1080 source. Primary written source: Thomas Kurian, "Gemini at Work 2026: Introducing Gemini agent," Google Cloud Blog, Oct 8, 2026 — https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026*

---

## 1. What Google announced

Google Cloud CEO Thomas Kurian's keynote post opens with the definition:

> "Gemini answers your questions, handles your knowledge work, creates your images and media, and writes and runs code — all in a single agent and a single API. **You give it objectives, not instructions.** You delegate an outcome and come back to finished work."

That sentence is the whole product. Earlier assistants took a prompt and returned text. This one is pitched as taking an *outcome* — it "plans the work, uses skills and tools, connects to your systems, and brings back something finished — inside the documents, the inbox, and the developer environments you already work in."

Google lists six architectural principles. In plain terms:

- **Unified agent.** Chat, autonomous work on assigned objectives, and code generation in one interface and one API. You can assign work, schedule tasks, or have it respond to events.
- **Omnipresent access.** Web, iOS and Android, Windows and Mac desktops, the command line, Google Workspace, Microsoft 365, and Slack — plus third-party apps, and a headless mode with no interface at all.
- **Persistent execution.** It runs in the cloud. Work that takes hours or days keeps running after you close your laptop, with "a single set of memories, context, and one personalization graph" on every device.
- **Multi-agent orchestration.** It can spin up temporary sub-agents — "each with their own identity" — and coordinate parallel and sequential steps over hours or days. It can also *be* a coworker agent (section 3).
- **Deeply contextual.** It arrives knowing your tools, data, and work history, and learns from each interaction. Teams can scope dedicated projects with their own context, skills, and tools.
- **Model choice flexibility.** "Gemini is the agent, and the model underneath it is a separate choice." It routes each job across Google's Gemini family **and Anthropic's Claude models** today, with other private and open models promised later.

Three things power it, per Google:

- **Tools.** Connectors to Confluence, Microsoft Office, Teams, Slack, Workspace, Git, Jira, Salesforce, ServiceNow, BigQuery, Databricks, Postgres, Snowflake, desktop files — "and any Model Context Protocol (MCP) server inside or outside your company network." Plus an enterprise tools registry where teams publish tools for the rest of the company.
- **Skills.** Reusable instruction sets for multi-step tasks. Google ships a global library; teams can publish to a shared company registry; individuals can build personal skills. Google says the agent "continuously learns from each execution."
- **Context and memory — four kinds.** *Session* memory (the task in front of it, even over days), *semantic* memory (a structured knowledge base built as it reads and works), *procedural* memory (how a job gets done, including skills it writes for itself), and *episodic* memory (everything it has done before). Google's own framing: "Gemini onboards itself the way a new hire would."

Inside Workspace, it works three ways: **personal assistance** (it is briefed on your calendar, team, and projects before you ask), **proactive delegation** (Workspace spots a delegatable task — say, your manager asking for a deck — and offers a one-click handoff), and **as a member of your team** (the coworker agent, next section).

## 2. The coworker agent — the part that changes the org chart

Describe a role — events coordinator, finance analyst — and Gemini creates a persistent agent for it. Per Google's post, that agent receives **its own Workspace account, including an email address, calendar, Drive, and presence in your company directory**. Colleagues add it to a Chat space or @mention it like anyone else. It can be tagged in a document comment, suggest an edit, and reply in the thread — "appearing under its own name in version history."

Two design choices matter more than the novelty:

1. **It acts under its own identity, not yours.** When it sends, edits, or books, the record says the agent did it. That is what makes an audit trail meaningful (section 4).
2. **It sees only what is shared with it.** "A coworker agent acts under its own identity rather than yours, and it sees only what you share with it. Access follows the sharing and membership your team already uses." It does not inherit your access — it accumulates its own, by being invited.

This is the shift the Reel is built on: an agent stops being a feature inside your account and becomes a *principal* in the system — with an inbox, a calendar, and a name in the directory. Everything in the governance section follows from that.

## 3. The money control — spending caps that pause the agent

Google is unusually blunt about cost: "While per-token prices have dropped 98% since 2024, enterprise AI volume has exploded. Running every simple loop through a premium model quickly breaks corporate budgets."

Three controls:

- **Multi-model orchestration** — pick (or combine) models per task.
- **Smart Routing** — automatic triage so each workload runs on the model with "maximum performance at the lowest possible cost."
- **Real-time spend caps** — the concrete one. "You can set a hard limit on a project's AI spend in the Cloud Billing Console, and Gemini enforces it. Gemini monitors token usage and sandbox costs, and **if a spend cap is triggered, that project's agent pauses**, and you can choose to resume work with a single click in the console. Because the tracking is per project, companies can charge AI costs back to specific departments."

A cap that *pauses* the agent is a different thing from a budget alert. An alert tells a human the money is gone; a cap stops the loop that is spending it. If you run agents today, this is the pattern to copy first: a hard, per-project ceiling with a defined paused state and a human-only resume.

What Google does **not** specify in the post: the cap's time period, alert thresholds, or how quickly enforcement bites after the limit is crossed. Do not assume details from other Google billing products carry over — the post doesn't say they do.

## 4. The governance — four questions

Google's post reduces agent governance to four questions. Quoted verbatim:

> - Who is the agent, and what identity does it have?
> - What is it allowed to do or what permissions is it granted?
> - What did it do and where can I see what it did?
> - What should it never touch?

And Google's answers, as announced:

- **Identity.** "Every agent gets its own identity, cryptographically attested and governed like an employee, with least-privilege permissions. That identity is stamped into the logs that capture its work, and into any virtual machine spun up to run code on its behalf."
- **Authorization.** Fine-grained, role-based permissions "approved by your organization's security administrators." When the agent connects to an external system, "its identity is mapped and propagated through industry standards such as OAuth."
- **Auditing.** "Every action Gemini takes is written to an audit trail and attributed to the agent rather than to a person," monitorable in real time.
- **Policy and the never-touch list.** All agents run inside an **Agent Sandbox** with its own network boundary; all traffic passes through **Agent Gateway**, "an AI network firewall enforcing your organization's policies in real time. You write the policy once, such as: 'agents may not open documents classified Need to Know.' Gemini applies it to every agent in your company instead of checking one agent at a time."

Identity, policy, and observability answer the first three questions; Agent Gateway answers the fourth.

## 5. The four questions as a checklist — for any agent, not just Google's

This is the transferable part. Before any agent goes live in your team — Google's, another vendor's, or one you built — you should be able to answer all four, in writing:

- [ ] **Who is the agent?** It has its own identity and credentials — not a shared API key, not your personal token. It has a named human owner. You can revoke the agent without revoking a person.
- [ ] **What may it do?** Its permissions are an explicit, role-scoped list, approved by someone other than the person who built it. Read and write are granted separately. Anything not on the list is denied.
- [ ] **What did it do?** Every action is logged under the agent's own identity — tool calls, files touched, messages sent, money spent — in a trail a human actually reviews, with alerts on the unusual.
- [ ] **What must it never touch?** A written never-list exists (data classes, systems, actions) and is enforced by the platform — a gateway, a sandbox, a policy check — not by a line in the prompt the agent can talk its way around.
- [ ] **What does it cost, and what stops it?** A hard spend cap per project, a defined paused state when the cap trips, and a human-only resume. (Google's fifth, implicit question — worth adding to the four.)
- [ ] **What is its status, honestly?** Preview, beta, or GA — and what has actually been tested in production, by whom. An announcement is a claim, not a result.

If you cannot tick a box, you do not have a governed agent. You have a demo with credentials.

## 6. What Google did not say

Stated plainly, from the keynote post itself:

- **No general-availability date** for the Gemini agent. Contemporaneous reporting (9to5Google, VentureBeat via reporters' briefings) described a private preview with wide availability "coming soon" for Workspace customers on select Business and Enterprise plans — that wording is reporters relaying Google, not a date in the post.
- **No agent-specific price.** Reporting said the agent would be included where Gemini Enterprise is available, at no additional charge; the post itself does not state pricing.
- **No independent verification.** The customer results in the post are Google's and its customers' claims, with no methodology given. Nothing in the post is a third-party test.
- **Preview scope elsewhere, too.** The industry specializations (Financial Services, Legal) are "in preview," with Government, Healthcare, and Retail "coming soon."

None of that makes the announcement unimportant. The architecture — identity, caps, gateway, the four questions — is a governance template worth copying now, on whatever stack you run. It makes the *availability* a thing to verify later, not a thing to assume today.

## 7. Sources

- Thomas Kurian, "Gemini at Work 2026: Introducing Gemini agent," Google Cloud Blog, Oct 8, 2026. https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026
- Google, "Google Cloud launches Gemini agent," The Keyword, Oct 8, 2026. https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/gemini-at-work/
- Google Cloud, "Gemini at Work 2026 in 2 Minutes" (video, 2,788,799 views when clipped, Nov 24, 2026). https://www.youtube.com/watch?v=ODQtU9TNlKA
- 9to5Google, "Google Cloud announces 'Gemini agent' as 'universal agent for work'," Oct 8, 2026 — private-preview status. https://9to5google.com/2026/10/08/gemini-agent-google-cloud/

---

*Source: @yashumani.ai — "Google just gave an AI agent its own email address." Comment DECODED on the Reel to get this file. Governed AI, decoded — with evidence.*

