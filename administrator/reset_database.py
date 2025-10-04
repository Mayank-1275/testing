# reset_database.py
# Clears application data and restores admin user
from database_manager import db
import create_tables

def reset_all():
    # delete data from tables but keep structures
    db.execute("DELETE FROM slots", commit=True)
    db.execute("DELETE FROM history", commit=True)
    # Optionally keep users but recreate default admin:
    db.execute("DELETE FROM users", commit=True)
    db.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
               ("mayank", "mayank1234", "admin"), commit=True)
    # set first_time_setup to true
    if db.fetchone("SELECT 1 FROM config WHERE key = ?", ("first_time_setup",)):
        db.execute("UPDATE config SET value = ? WHERE key = ?", ("true", "first_time_setup"), commit=True)
    else:
        db.execute("INSERT INTO config (key, value) VALUES (?, ?)", ("first_time_setup", "true"), commit=True)

if __name__ == "__main__":
    reset_all()
    print("System reset complete.")
