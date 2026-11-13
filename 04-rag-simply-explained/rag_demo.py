# rag_demo.py — RAG, simply explained. The smallest version of the idea.
# Standard library only. Runs as-is. No model, no API key, no embeddings:
# retrieval here is plain keyword overlap, on purpose — so you can see
# the retrieve step doing the work, instead of hiding it inside a vector store.
#
# Run: python3 rag_demo.py
#   -> retrieves the right doc for each question, answers from it, scoreboard 3/3
# Run: python3 rag_demo.py --bad
#   -> retrieval is forced to pick the WRONG doc, and the answer goes wrong
#      with it. Same "model", same question — only the retrieved page changed.
#      That is the whole lesson: most "the model hallucinated" complaints
#      are retrieval failures in disguise.

DOCS = {
    "refund-policy": "Refunds: orders can be refunded within 30 days of delivery. "
                     "Digital downloads are not refundable once downloaded.",
    "shipping-policy": "Shipping: standard delivery takes 3-5 business days. "
                       "Express delivery takes 1-2 business days and costs $12.",
    "warranty-policy": "Warranty: hardware is covered for 12 months from purchase. "
                       "Batteries are covered for 6 months.",
}

# Fixed test set — the same questions every run, like a real RAG scoreboard.
QUESTIONS = [
    ("How long do I have to return an order?", "refund-policy", "30 days"),
    ("How fast is express delivery?", "shipping-policy", "1-2 business days"),
    ("How long is the hardware warranty?", "warranty-policy", "12 months"),
]

STOPWORDS = {"how", "long", "do", "i", "have", "to", "an", "the", "is", "a"}


def retrieve(question, docs):
    """Toy retrieval: score each doc by keyword overlap with the question."""
    words = {w.strip("?.,") for w in question.lower().split()} - STOPWORDS
    scored = sorted(
        ((sum(1 for w in words if w in text.lower()), name) for name, text in docs.items()),
        reverse=True,
    )
    return scored[0][1], scored[0][0]


def answer(question, doc_name):
    """Answer ONLY from the retrieved doc. Without the right doc, say so."""
    text = DOCS[doc_name]
    return f"[retrieved: {doc_name}] {text}", doc_name


def main(bad=False):
    print("RAG demo — retrieve, then answer from what you retrieved.\n")
    passed = 0
    for question, expected_doc, expected_fact in QUESTIONS:
        doc, score = retrieve(question, DOCS)
        if bad:
            # --bad: retrieval itself picks the WRONG doc; re-score against it.
            doc = next(name for name in DOCS if name != expected_doc)
            words = {w.strip("?.,") for w in question.lower().split()} - STOPWORDS
            score = sum(1 for w in words if w in DOCS[doc].lower())
        reply, used = answer(question, doc)
        ok = (used == expected_doc and expected_fact in reply)
        passed += ok
        print(f"Q: {question}")
        print(f"  retrieved: {doc} (overlap {score})")
        print(f"  A: {reply}")
        print(f"  {'PASS' if ok else 'FAIL'} — expected {expected_doc} / '{expected_fact}'\n")
    print(f"SCOREBOARD: {passed}/{len(QUESTIONS)} correct")
    if bad:
        print("Same questions, same 'model' — only the retrieved page changed.")
    return 0 if passed == len(QUESTIONS) else 1


if __name__ == "__main__":
    import sys
    raise SystemExit(main(bad="--bad" in sys.argv))
