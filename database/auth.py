
import sqlite3
import hashlib
from utils import setup_logging
import logging

def create_default_admin():
    """
    Create default admin user if it doesn't exist
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        # Create users table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'staff'
            )
        ''')

        # Create default admin user (username: admin, password: admin123)
        admin_password = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        ''', ('admin', admin_password, 'admin'))

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error creating default admin: {e}")

def authenticate_user(username, password):
    """
    Authenticate user credentials
    """
    try:
        # Hash the password
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Check credentials
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        cursor.execute('SELECT role FROM users WHERE username = ? AND password_hash = ?',
                      (username, password_hash))
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

    except Exception as e:
        print(f"Authentication error: {e}")
        return None

def create_user(username, password, role='staff'):
    """
    Create a new user
    """
    try:
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        ''', (username, password_hash, role))

        conn.commit()
        conn.close()
        return True

    except sqlite3.IntegrityError:
        return False  # Username already exists
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def change_password(username, old_password, new_password):
    """
    Change user password
    """
    try:
        # First authenticate with old password
        if not authenticate_user(username, old_password):
            return False

        # Hash new password
        new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()

        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        cursor.execute('UPDATE users SET password_hash = ? WHERE username = ?',
                      (new_password_hash, username))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"Error changing password: {e}")
        return False
