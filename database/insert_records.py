
import sqlite3
from datetime import datetime
from utils import setup_logging
import logging

def add_vehicle(vehicle_number, vehicle_type, category, entry_time, slot_id):
    """
    Add or update vehicle in vehicles_master table
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        # Check if vehicle already exists
        cursor.execute('SELECT first_entry FROM vehicles_master WHERE vehicle_number = ?', 
                      (vehicle_number,))
        existing = cursor.fetchone()

        if existing:
            # Update existing vehicle
            cursor.execute('''
                UPDATE vehicles_master 
                SET vehicle_type = ?, category = ?, last_slot = ?
                WHERE vehicle_number = ?
            ''', (vehicle_type, category, f'Slot {slot_id}', vehicle_number))
        else:
            # Insert new vehicle
            cursor.execute('''
                INSERT INTO vehicles_master 
                (vehicle_number, vehicle_type, category, first_entry, last_slot)
                VALUES (?, ?, ?, ?, ?)
            ''', (vehicle_number, vehicle_type, category, entry_time, f'Slot {slot_id}'))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        logging.error(f"Error adding vehicle: {e}")
        return False

def add_parking_session(vehicle_number, slot_id, zone, entry_time):
    """
    Add parking session to history and active_vehicles tables
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        # Add to parking history
        cursor.execute('''
            INSERT INTO parking_history (vehicle_num, slot_id, zone, entry_time)
            VALUES (?, ?, ?, ?)
        ''', (vehicle_number, slot_id, zone, entry_time))

        # Add to active vehicles
        cursor.execute('''
            INSERT OR REPLACE INTO active_vehicles (vehicle_number, slot_id, zone, entry_time)
            VALUES (?, ?, ?, ?)
        ''', (vehicle_number, slot_id, zone, entry_time))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        logging.error(f"Error adding parking session: {e}")
        return False

def add_user_log(username, action, timestamp=None):
    """
    Add user activity log (optional feature)
    """
    if not timestamp:
        timestamp = datetime.now().isoformat()

    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        # Create user_logs table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp DATETIME NOT NULL
            )
        ''')

        cursor.execute('''
            INSERT INTO user_logs (username, action, timestamp)
            VALUES (?, ?, ?)
        ''', (username, action, timestamp))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        logging.error(f"Error adding user log: {e}")
        return False

def add_daily_summary(date, zone, total_slots, occupied, available):
    """
    Add daily summary record
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO daily_summary 
            (date, zone, total_slots, occupied, available)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, zone, total_slots, occupied, available))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        logging.error(f"Error adding daily summary: {e}")
        return False
