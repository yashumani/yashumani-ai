# Gemini Decisions API — the checker, as a product

> **The one line:** instead of asking a big generative model to judge in free text, Google split judgment into many small, structured, scored questions — and shipped that as a dedicated API.
>
> **The model is Gemini Decision 1** (`gemini-decision-1`), announced by Google DeepMind on Nov 11, 2026 in "Gemini Decisions API: Fast multimodal decisions" (Min Choi, Felix Yu, blog.google). It does not generate text. It scores bounded choices in a single forward pass and returns probabilities and confidence.
>
> This is the full wiki behind the @yashumani.ai Decoded Reel on the Gemini Decisions API. The Reel teaches the shape; this file is the complete version: the call, the three jobs, the worked gate, and the limits.

---

## 1. What a "decision" call looks like

One request carries one shared input plus up to 1,000 independent questions.

- **The input:** one multimodal `Content` block — text, images, audio, video, PDFs — up to 256K tokens (per Google's announcement). The shared input is billed once per request, however many questions you attach; each question adds only its own instruction and criteria tokens.
- **The questions:** three types, mixable in one request (names are Google's):
  - **`noul` (yes/no):** the probability that a condition holds, with optional true/false description criteria.
  - **`choice` (multiple choice):** 2 to 255 options; returns the winner plus normalized probabilities for every candidate.
  - **`score` (ordered rubric):** grades against an ordered rubric starting at 0; returns a continuous weighted score plus per-level probabilities.
- **The answers:** every answer carries a confidence score from 0 to 1, so your code can route ambiguous cases to a fallback or a human reviewer — that routing pattern is Google's own stated design.

Google's published figures (their claims, from the launch post — verify on your own workload before relying on them):

- Latency 150–250 ms end-to-end (50–100 ms of model compute), measured on inputs up to 16K tokens, "nearly flat from 1 to 100 questions per request"
- Price $0.10 per 1M input tokens, **$0 for output tokens**; a no-cost tier in Google AI Studio for prototyping
- "Nearly 5x cheaper across the shared benchmark suite than Gemini 3.5 Flash-Lite with the Interactions API"
- On benchmarks spanning agent routing, reasoning, ranking and multimodal understanding, Google says Decision 1 "leads across the suite, with the lowest calibration error"

The shape, in Google's own example form (a photo of a breakroom counter plus a text note, checked three ways in one request):

```python
from google import genai

client = genai.Client(http_options={"api_version": "v1beta"})

result = client.decisions.create(
    model="gemini-decision-1",
    input=[
        {"type": "image", "uri": ".../spill.jpg", "mime_type": "image/jpeg"},
        {"type": "text", "text": "Breakroom counter check before the 9 AM client meeting."},
    ],
    questions={
        "has_spill": {
            "type": "noul",
            "instructions": "Is there an uncleaned liquid spill on the counter?",
        },
        "next_action": {
            "type": "choice",
            "instructions": "Which cleanup action fits the scene?",
            "criteria": {
                "wipe_with_cloth": "Small counter spill with a cloth or towel already nearby.",
                "dispatch_janitorial": "Large floor hazard, broken glass, or active leak.",
                "ready_for_meeting": "Counter is clean and ready.",
            },
        },
        "severity": {
            "type": "score",
            "instructions": "Rate the severity of the counter mess.",
            "criteria": ["Clean and ready.", "Minor localized spill.", "Major spill or safety hazard."],
        },
    },
)
```

## 2. Why structured beats free-text judging

The Decoded Series has taught this twice already: the worker never grades its own work (Post 3), and the eval loop only works when failures become scores you can re-run (Posts 8/9). A free-text judge breaks both lessons:

| | Free-text judge | Decision call |
|---|---|---|
| **Output** | A paragraph, worded differently every run | The same fields every time: answer, probability, confidence |
| **Your code** | Parses prose and hopes | Reads numbers and branches |
| **Audit** | Re-read essays | Compare scores across runs |
| **Cost shape** | Output tokens, generated token by token | No output tokens billed (Google's pricing) |
| **Failure mode** | Confident, fluent, unmeasurable | A number that can be low — and routed |

Splitting one big judgment into many small questions is the point. Each question is cheap, independent, and checkable on its own. That is what makes the result auditable: when a gate misfires, you can point at the one question that scored wrong instead of re-reading an essay.

## 3. Where it sits in an agent pipeline — three jobs

Google's announcement names the primitives: "tool selection, policy checks, model routing, and context grading." In pipeline terms, that is three jobs:

### Job 1 — Gate (before an action)

The check runs *before* anything irreversible, and it can stop the run. Worked example — an agent drafts a customer reply and wants to send it:

> Draft: "Sorry for the delay — we'll refund you $620 right away."

Three questions run first (illustrative scores, in the API's shape):

1. `noul` — "Does the draft promise a refund over the $500 policy limit?" → **YES, p = 0.87**
2. `choice` — "Which action fits policy?" → send 0.22 · hold 0.17 · **escalate 0.61**
3. `score` — "Tone against the support rubric (0–3)" → **2.4 / 3**

The tone was fine. The promise was not. The gate blocks the send and routes the draft to a human. That is Post 3's rule with a product behind it: *a check that cannot stop the run is not a check — it is a comment.*

### Job 2 — Router (between models and tools)

A `choice` question picks which model tier or which tool should take a task, in milliseconds, before the expensive call happens. Google's own example: Gemini Notebook uses the Decisions API as a real-time router, classifying intent and directing queries to the optimal model tier and thinking level — Google reports up to 40% lower latency on everyday queries while reserving deep-reasoning models for complex tasks (their figure).

### Job 3 — Grader (of context, before the agent sees it)

A `score` question grades the material an agent is about to work from — is this document relevant, is this retrieved chunk on-topic, is this context good enough to act on? Grading context upstream keeps bad inputs from becoming confident outputs downstream. Google also reports internal uses as a safety layer for MCP tools in Search and emoji selection (200+ options) in CC from Google Labs.

## 4. The honest limits

- **A calibrated score is not correctness.** Calibration means the confidence tracks the model's actual accuracy *on the benchmark it was measured on*. Google's "lowest calibration error" is a claim about their suite. Your distribution is different — measure calibration on your own data before you trust any threshold.
- **Whoever writes the rubric decides the outcome.** The model scores the questions you wrote, against the levels you defined. A vague question gets a precise-looking number anyway. The rubric *is* the policy — review it like policy.
- **Bounded means bounded.** The API answers only the options you give it. If the right answer is not in the choice set, it will still pick one of yours — give it an escape option ("none of these / needs a human") where the real world has one.
- **Confidence is the routing signal, not a verdict.** Low confidence should mean "send to a human or a bigger model," not "round it to the nearest answer." The API hands you the number; the threshold is your engineering decision.
- **Launch-stage caveats.** At launch, Google listed support in Google Cloud as "coming soon," and launch coverage noted no Context Caching or Batch API support. Check the current docs before designing around either.

## 5. Before you trust a score — the checklist

- [ ] Every question is one question. If it contains "and," split it.
- [ ] Every choice set includes the real-world escape: none / other / needs a human.
- [ ] Rubric levels are written as observable criteria, not adjectives.
- [ ] You measured calibration on *your* data, not just Google's suite.
- [ ] A confidence threshold exists, and below it a human (or a bigger model) decides.
- [ ] The gate can actually stop the action it guards.
- [ ] Question wording and rubric changes are versioned like code — because they are the policy.

## 6. Sources

- Google (Min Choi, Felix Yu, Google DeepMind), "Gemini Decisions API: Fast multimodal decisions," blog.google, Nov 11, 2026 — the primary source for every capability, price and latency figure above. https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/
- Decisions API documentation, Google AI Studio: https://aistudio.google.com/docs/decisions-api
- Launch coverage: SiliconANGLE, "Google enters decision model market with Gemini Decisions API," Nov 11, 2026.
- Clip used in the Reel: Prompt Engineering, "Gemini Decision 1: You Don't Need an LLM to Make a Decision," YouTube. https://www.youtube.com/watch?v=-On9ZKGiMfA

*Capability, price, latency and benchmark claims are Google's, attributed as such. The worked gate example is illustrative, built in the API's documented shape.*

---

*Source: @yashumani.ai Decoded Series — "Your agent grades itself in paragraphs." Comment DECODED on the Reel to get this file. Governed AI, decoded — with evidence.*
