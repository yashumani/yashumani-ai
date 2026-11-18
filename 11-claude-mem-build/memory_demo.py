"""memory_demo.py — the claude-mem mechanism in miniature (Decoded #11).

Standard library only. Demonstrates the core of the 7-file build:
  1. store observations in SQLite with FTS5 (sessions + observations),
  2. keyword search with BM25 ranking,
  3. layered retrieval — a short index first, full detail only on request.

The Chroma vector half of hybrid search is the plugin's, not this demo's:
this file shows the keyword half and the layering. No network, no API key.

Run: python3 memory_demo.py
Expected: 3 observations stored, BM25 search finds the right one,
layered retrieval shows the index (~30 tokens of text) then the detail.
"""

import sqlite3

SCHEMA = """
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);
CREATE TABLE observations (
    id INTEGER PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES sessions(id),
    note TEXT NOT NULL
);
CREATE VIRTUAL TABLE obs_fts USING fts5(
    note, content='observations', content_rowid='id'
);
CREATE TRIGGER obs_ai AFTER INSERT ON observations BEGIN
    INSERT INTO obs_fts(rowid, note) VALUES (new.id, new.note);
END;
"""

# Three observations, as the observer model would write them:
# one line each, what happened — not the transcript.
SEED = [
    (1, "Fixed the login bug: the session cookie expired after 15 minutes, not 24 hours."),
    (1, "Chose SQLite FTS5 for keyword search and Chroma for vector search, merged with RRF."),
    (2, "The deploy failed because the worker port 37777 was already in use by an old process."),
]


def build(conn):
    conn.executescript(SCHEMA)
    conn.execute("INSERT INTO sessions (id, title) VALUES (1, 'memory build'), (2, 'deploy debug')")
    conn.executemany("INSERT INTO observations (session_id, note) VALUES (?, ?)", SEED)
    conn.commit()


def keyword_search(conn, query, limit=3):
    """BM25-ranked keyword search over the FTS5 index."""
    rows = conn.execute(
        "SELECT o.id, o.note, rank FROM obs_fts JOIN observations o ON o.id = obs_fts.rowid "
        "WHERE obs_fts MATCH ? ORDER BY rank LIMIT ?",
        (query, limit),
    ).fetchall()
    return rows


def layered_retrieval(conn, query):
    """Layer 1: a short index (ids + first words). Layer 2: full detail on request."""
    hits = keyword_search(conn, query)
    index = [(row[0], row[1][:40] + "...") for row in hits]
    detail = {row[0]: row[1] for row in hits}
    return index, detail


def main():
    conn = sqlite3.connect(":memory:")
    build(conn)
    stored = conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
    assert stored == 3, f"expected 3 observations, got {stored}"
    print(f"stored: {stored} observations")

    hits = keyword_search(conn, "FTS5 Chroma")
    assert len(hits) == 1 and hits[0][0] == 2, f"expected observation 2, got {hits}"
    print(f"BM25 search 'FTS5 Chroma' -> observation {hits[0][0]}: {hits[0][1]}")

    index, detail = layered_retrieval(conn, "login bug")
    assert len(index) == 1 and index[0][0] == 1
    index_text = " | ".join(f"#{i}: {t}" for i, t in index)
    print(f"layer 1 (index, ~30 tokens of text): {index_text}")
    print(f"layer 2 (detail on request): {detail[1]}")

    print("DEMO PASS: store -> BM25 search -> layered retrieval")


if __name__ == "__main__":
    main()
