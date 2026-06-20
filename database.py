import sqlite3
import os

# Use /tmp for writable storage on serverless platforms (e.g. Vercel).
# Vercel sets the VERCEL env var automatically; locally (Windows/Mac/Linux)
# this falls back to a local file in the project directory.
if os.environ.get("DB_PATH"):
    DB_PATH = os.environ["DB_PATH"]
elif os.environ.get("VERCEL"):
    DB_PATH = "/tmp/careers.db"
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "careers_local.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    skills TEXT NOT NULL,
    interests TEXT NOT NULL,
    top_career TEXT NOT NULL,
    top_score INTEGER NOT NULL,
    all_results TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()

def save_submission(name, skills, interests, results):
    """
    results: list of dicts with keys: title, score, reason, roadmap
    """
    init_db()  # Ensure table exists (safe to call multiple times)
    top = results[0]
    all_str = "|".join([r["title"] for r in results])
    conn = get_connection()
    conn.execute(
        "INSERT INTO submissions (name, skills, interests, top_career, top_score, all_results) VALUES (?, ?, ?, ?, ?, ?)",
        (name, skills, interests, top["title"], top["score"], all_str)
    )
    conn.commit()
    conn.close()
