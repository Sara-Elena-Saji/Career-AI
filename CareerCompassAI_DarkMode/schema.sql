-- CareerCompassAI V2 Schema
-- Stores user submissions and career recommendation results

CREATE TABLE IF NOT EXISTS submissions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    skills      TEXT    NOT NULL,
    interests   TEXT    NOT NULL,
    top_career  TEXT    NOT NULL,
    top_score   INTEGER NOT NULL,
    all_results TEXT    NOT NULL,          -- pipe-separated top career names
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
