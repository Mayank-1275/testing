# database_manager.py
import sqlite3
import system_config as cfg

class DatabaseManager:
    def __init__(self, db_path=cfg.DB_PATH):
        self.db_path = db_path
        # ensure file exists
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.close()

    def execute(self, sql, params=(), commit=False):
        """
        Run an INSERT/UPDATE/DELETE or any SQL where caller doesn't need fetched rows.
        Returns lastrowid for inserts or number of affected rows for others.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(sql, params)
            if commit:
                conn.commit()
            # return lastrowid for inserts, else rowcount
            return cur.lastrowid if cur.lastrowid else cur.rowcount

    def fetchone(self, sql, params=()):
        """Execute a SELECT and return a single row (sqlite3.Row) or None."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchone()

    def fetchall(self, sql, params=()):
        """Execute a SELECT and return list of sqlite3.Row."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchall()

    def executescript(self, script):
        """Execute a full SQL script (multiple statements)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(script)
            conn.commit()

# single global instance for convenience
db = DatabaseManager()
