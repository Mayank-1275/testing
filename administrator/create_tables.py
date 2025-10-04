# create_tables.py
# Run once on first-time setup (or call from GUI).
from database_manager import db

CREATE_SCRIPT = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'admin'
);

CREATE TABLE IF NOT EXISTS slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot_code TEXT UNIQUE,
    zone TEXT,
    type TEXT,
    location TEXT,
    occupied INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot_id INTEGER,
    action TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(slot_id) REFERENCES slots(id)
);
"""

def run_first_time_setup():
    db.executescript(CREATE_SCRIPT)
    # set default config flag first_time_setup = true (if not present)
    existing = db.fetchone("SELECT value FROM config WHERE key = ?", ("first_time_setup",))
    if not existing:
        db.execute("INSERT INTO config (key, value) VALUES (?, ?)", ("first_time_setup", "true"), commit=True)
    # create default admin user if not exists
    admin = db.fetchone("SELECT id FROM users WHERE username = ?", ("mayank",))
    if not admin:
        db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                   ("mayank", "mayank1234", "admin"), commit=True)

if __name__ == "__main__":
    run_first_time_setup()
    print("Tables created and default admin ensured.")
