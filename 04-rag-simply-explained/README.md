# RAG, simply explained

> **The one line:** a model can't know your docs — so give it the right page before it answers.
>
> **The idea in three steps:** Retrieve the relevant pages. Read them into context. Answer from them — and say which page the answer came from.
>
> This is the full wiki behind the @yashumani.ai Post 4 carousel (Decoded Series #4). The carousel shows the idea in 7 slides. This file is the complete version: the problem, the three steps, how to retrieve well, what RAG is not, and the scoreboard.

---

## 1. The problem — the model answers from memory

A language model answers from what it learned in training: its weights. That works for general knowledge. It fails for *your* stuff — your docs, your prices, your policies, your code — because none of that is in the weights, and what is in them is frozen in time.

So when you ask it about your own material, it does the only thing it can: it guesses, fluently. That guess is what people call a hallucination. Most of the time, the model isn't broken. It was just never given the facts.

## 2. The three steps — retrieve, read, answer

```
Question
  → RETRIEVE: find the pages that might answer it
  → READ: put those pages into the model's context
  → ANSWER: answer from the pages, citing which one
```

That is all RAG is: Retrieval-Augmented Generation. Nothing in the model changes. No retraining. The knowledge stays outside the weights, in your documents — so when a document changes, the answer changes, with no training run.

- **Retrieve** — search your docs for the question. Keywords, vectors, or both (section 3).
- **Read** — the retrieved chunks become part of the prompt. This is the context the model actually reasons over.
- **Answer** — the model answers from those pages. If the pages don't contain the answer, the honest answer is "I can't find that in your docs" — not a confident guess.

The demo in this folder, `rag_demo.py`, is the smallest version of this: three tiny policy docs, keyword retrieval, answers that cite the doc they came from. Run it with `--bad` and watch the same questions fail — the only thing that changed is which page got retrieved.

## 3. Retrieve well — keywords, vectors, and a reranker

Retrieval is where RAG is won or lost. The library's measured pipeline, in order:

1. **Filter first** — metadata (title, date, source type) shrinks the search space before retrieval starts.
2. **Hybrid search** — BM25 keywords *plus* vector embeddings. Keywords catch exact tokens embeddings blur together (error codes, names, versions). Vectors catch paraphrases keywords miss.
3. **Rerank narrowly** — retrieve generously (top 10–20), then a cross-encoder reranker reads the query against each candidate together and picks the winner (top 3–5 into context).

Why the reranker earns its place: in Deepak Jose's experiment on 55 near-duplicate help-centre articles, hybrid search alone barely moved top-1 accuracy — but adding the reranker was the biggest single jump. One honest caveat from the same experiment: the reranker also *hurt* one query, dropping it from #1 to #10. Rerankers are net-positive, not magic — which is why section 5 exists.

The numbers behind that experiment come from one 20-question synthetic corpus, so treat the ordering as the lesson, not the exact scores. The pipeline — filter, hybrid search, rerank — is the transferable part.

## 4. What RAG is not — retrieve vs train

The most common beginner error: fine-tuning a model to teach it facts.

| The model needs to… | Do this |
|---|---|
| Answer from your docs, catalog, or history — facts that change | **RAG** — retrieve it |
| Output a consistent format, style, or classification — behave a certain way | **Fine-tune** — train it |
| Do both | RAG for the facts + a fine-tuned small model for the rendering |

Fine-tuning bakes behaviour into the weights; it memorizes facts poorly and can degrade general ability. RAG keeps knowledge outside the weights, updateable and reversible. Start with RAG. Add fine-tuning only when you can name a behaviour retrieval alone cannot enforce — and evaluate the adapter before and after on a held-out set.

## 5. The scoreboard — measure retrieval before blaming the model

A fixed test set of questions, re-run after every retrieval change, is how you stop guessing about RAG quality. The demo's scoreboard is the smallest version: 3 questions, 3/3 with good retrieval, 0/3 when retrieval picks the wrong page.

```python
# rag_demo.py — three fixed questions. Retrieval decides the score.
# Run: python3 rag_demo.py        -> SCOREBOARD: 3/3 correct
# Run: python3 rag_demo.py --bad  -> SCOREBOARD: 0/3 correct (exit 1)
```

Then break it on purpose: add a near-duplicate doc to the corpus — two policies that say almost the same thing — and watch retrieval pick the wrong one. That failure is the lesson: wrong chunk in, wrong answer out. Fix the retrieval (better chunking, a filter, a reranker), not the model.

## 6. Before you ship it — the checklist

- [ ] The answer cites the page it came from — no citation, no trust.
- [ ] When the docs don't contain the answer, the system says so instead of guessing.
- [ ] Retrieval is measured on a fixed question set, re-run after every change.
- [ ] Knowledge lives in documents, not in a training run — change a doc, the answer changes.
- [ ] You have run it on a case where retrieval *should* fail, and watched it fail.
- [ ] Nothing irreversible happens on a retrieved answer without human approval.

If any box is unchecked, you don't have a RAG system. You have a chatbot with a search box.

## 7. Where this comes from

From the AI Brain's RAG pages, built from the research library: the hybrid + reranker pipeline and its measured experiment (Deepak Jose, via `datasciencebrain-hybrid-search-reranker`), the three foundational techniques — hybrid search, MMR diversity, metadata filtering (WDF AI, `wdf-ai-rag-pipeline-hybrid-mmr`), the RAG module inside a real agent (Aman Views' minimal agent), and the retrieve-vs-train decision (`rag-vs-fine-tuning`). The scoreboard discipline is Post 3's Rule 3 applied to retrieval: evals that can fail a release.

Related work by the same author: [HarnessLab](https://github.com/yashumani/HarnessLab) (agents are disposable, harnesses are durable), [Prefrontal](https://github.com/yashumani/Prefrontal) (a context compiler for agents), and [Talk2Data](https://github.com/yashumani/Talk2Data) (governed execution — the LLM interprets wording only; deterministic services do the work).

---

*Source: @yashumani.ai Post 4 — "RAG, simply explained." Comment DECODED on the carousel to get this file. Governed AI, decoded — with evidence.*
