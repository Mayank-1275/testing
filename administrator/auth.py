# auth.py
# Authentication helpers. (Note: password stored plaintext for simplicity.)
from database_manager import db

def is_first_time():
    row = db.fetchone("SELECT value FROM config WHERE key = ?", ("first_time_setup",))
    return row and row["value"] == "true"

def set_first_time_flag(value: bool):
    val = "true" if value else "false"
    # upsert
    if db.fetchone("SELECT 1 FROM config WHERE key = ?", ("first_time_setup",)):
        db.execute("UPDATE config SET value = ? WHERE key = ?", (val, "first_time_setup"), commit=True)
    else:
        db.execute("INSERT INTO config (key, value) VALUES (?, ?)", ("first_time_setup", val), commit=True)

def validate_user(username, password):
    row = db.fetchone("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return row is not None
