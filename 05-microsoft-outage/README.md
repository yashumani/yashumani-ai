# Microsoft 365 went down worldwide — and it wasn't a hack

> **The one line:** a network change, not a cyberattack, took Microsoft 365 down for millions of people on Thursday, November 12, 2026.
>
> **The idea in three steps:** an earlier network capacity upgrade introduced a fault; a later network change surfaced it; servers dropped out faster than the rest of the fleet could absorb the load.
>
> This is the full wiki behind the @yashumani.ai Microsoft 365 outage carousel (a bonus news post). The carousel shows the story in 7 slides. This file is the complete version: what happened, the timeline, what caused it, what it was not, and what we still don't know.

---

## 1. What happened

On Thursday, November 12, 2026, Microsoft 365 went down worldwide. Outlook and Exchange Online stopped working for many users, along with Teams, SharePoint, OneDrive, Copilot, Intune, Defender for Office 365, Power BI, and Microsoft Graph. Microsoft 365 serves 430M+ users.

At the peak, around 1:15pm ET on Thursday, Downdetector recorded about 130,000 Outlook reports and about 50,000 Microsoft 365 reports. Problems were reported from 74 countries.

Who felt it: staff of the U.S. House of Representatives, government departments worldwide, and schools. In Colorado, state agencies reported payment processing problems and delays in jail inmate releases.

Microsoft opened two main incidents: EX1550543 (Exchange Online, opened 16:20 UTC / 11:20am ET) and MO1550821 (Microsoft 365, began 18:26 UTC / 1:26pm ET). An earlier Teams incident, TM1550488, hit North America the same morning. Microsoft first announced issues around 10:40am ET.

## 2. The timeline

| When | What |
|---|---|
| Thu Nov 12, ~10:40am ET | Microsoft first reports issues with Microsoft 365. |
| Thu Nov 12, ~1:15pm ET | Peak: ~130,000 Outlook reports on Downdetector; ~50,000 for Microsoft 365. |
| Thu Nov 12, evening | Microsoft exec Charles Lamanna says on X there is no sign of malicious activity. |
| Fri Nov 13, 10:39am ET | Microsoft confirms: "no indication this is the result of malicious or cyber activity." |
| Fri Nov 13, 1:05pm ET | Microsoft's cause statement on X: a technical issue from a network capacity upgrade, surfaced by a recent network change. |
| Fri Nov 13, ~3pm ET | Mostly recovered. Underlying issue fixed; remaining customers and regions still being restored; mail flow still normalizing. No ETA for full recovery. |
| Fri Nov 13, ~2:50pm ET | Downdetector Outlook reports down to ~1,600, from 130,000 at the peak. |

## 3. What caused it

Microsoft's statement on Friday, November 13 at 1:05pm ET (via @MSFT365Status on X):

> "This was a technical issue not related to cyber or AI/agents. The incident was introduced by an issue during an earlier network capacity upgrade that surfaced following a recent network change."

The mechanism, per Microsoft's incident updates:

1. **A capacity upgrade introduced a fault** — an issue during an earlier network capacity upgrade.
2. **A later change surfaced it** — a recent network change brought the fault out.
3. **Servers failed health checks and dropped out** — servers unexpectedly became unavailable after failing automated health checks.
4. **The rest overloaded** — a process for establishing secure connections became overwhelmed, and the remaining servers were strained until they stopped processing requests.

It was not a traffic surge. Microsoft's updates describe the fleet shrinking and the survivors choking, not a flood of requests from outside.

## 4. What it was not

- **Not a hack.** Microsoft confirmed Friday 10:39am ET there is "no indication this is the result of malicious or cyber activity." Charles Lamanna, a Microsoft executive, said the same on X on Thursday night.
- **Not AI or agents.** Microsoft's own words: the incident was "not related to cyber or AI/agents."
- **Not Azure.** Azure was not confirmed affected — the Azure status page showed no active events.

Unconfirmed reporting, not presented as fact: The Verge's Tom Warren reported sources linking the outage to Azure Virtual Network configuration changes. Microsoft has not confirmed this.

## 5. What we don't know yet

- **The definitive root cause.** Microsoft has promised a full post-incident report. It has not been published yet. The network capacity upgrade and the later change are what Microsoft has said so far — the detailed "why" is still coming.
- **The exact global user count.** Microsoft has not said how many users were affected in total.
- **Full recovery timing.** As of Friday afternoon, incidents MO1550821 and EX1550543 were still open. The underlying issue was fixed, but Microsoft gave no ETA for every customer and region to be fully restored.

## 6. The lesson — one change, no safe blast radius

Health checks caught the failure — servers that failed them were pulled out. But the fleet had no fallback: each server that dropped out pushed more load onto the ones left, until they stopped too. The check worked; the blast radius didn't.

That is the same discipline as Post 3's Rule 3: a control that can't stop the run is not a control. Changes need a canary and a rollback — a small, reversible rollout with a way back — the same way evals need to be able to fail a release. A change that goes out everywhere at once, with no measured gate, is a single point of failure wearing a deployment's clothes.

This is what the evidence shows so far. If the postmortem changes the story, this wiki changes with it.

## 7. Sources

- USA Today, November 13, 2026 — outage coverage (peak reports, 74 countries, who was affected).
- People / BBC, November 13, 2026 — outage coverage and Microsoft's statements.
- Microsoft @MSFT365Status on X — incident updates; cause statement Fri Nov 13, 1:05pm ET; "no indication of malicious or cyber activity" Fri 10:39am ET.
- Microsoft 365 admin center incidents: MO1550821, EX1550543, TM1550488.
- Downdetector — report counts (peak ~130,000 Outlook / ~50,000 Microsoft 365; ~1,600 by Fri 2:50pm ET).
- The Verge (Tom Warren) — unconfirmed reporting on Azure Virtual Network config changes; Microsoft has not confirmed this.

---

*Source: @yashumani.ai Post 5 — "Microsoft 365 outage, Nov 12–13, 2026." Comment DECODED on the carousel to get this file. Governed AI, decoded — with evidence.*
