
import sqlite3
from datetime import datetime, timedelta
from utils import setup_logging
import logging

def delete_old_history(days=90):
    """
    Delete parking history older than specified days
    """
    try:
        cutoff_date = datetime.now() - timedelta(days=days)

        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM parking_history 
            WHERE exit_time IS NOT NULL AND datetime(exit_time) < ?
        ''', (cutoff_date.isoformat(),))

        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()

        logging.info(f"Deleted {deleted_count} old history records")
        return deleted_count

    except Exception as e:
        logging.error(f"Error deleting old history: {e}")
        return 0

def delete_user(username):
    """
    Delete a user account
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        # Don't delete the admin user
        if username.lower() == 'admin':
            return False

        cursor.execute('DELETE FROM users WHERE username = ?', (username,))

        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()

        return deleted

    except Exception as e:
        logging.error(f"Error deleting user: {e}")
        return False

def delete_vehicle_data(vehicle_number):
    """
    Delete all data for a specific vehicle (use with caution)
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        # Remove from active vehicles if present
        cursor.execute('DELETE FROM active_vehicles WHERE vehicle_number = ?', 
                      (vehicle_number,))

        # Remove from vehicle preferences
        cursor.execute('DELETE FROM vehicle_preferences WHERE vehicle_number = ?', 
                      (vehicle_number,))

        # Remove from parking history
        cursor.execute('DELETE FROM parking_history WHERE vehicle_num = ?', 
                      (vehicle_number,))

        # Remove from vehicles master
        cursor.execute('DELETE FROM vehicles_master WHERE vehicle_number = ?', 
                      (vehicle_number,))

        # Free any slots occupied by this vehicle
        cursor.execute('''
            UPDATE slots 
            SET is_occupied = 0, vehicle_num = NULL, entry_time = NULL 
            WHERE vehicle_num = ?
        ''', (vehicle_number,))

        conn.commit()
        conn.close()

        logging.info(f"Deleted all data for vehicle {vehicle_number}")
        return True

    except Exception as e:
        logging.error(f"Error deleting vehicle data: {e}")
        return False

def cleanup_orphaned_records():
    """
    Clean up orphaned records in database
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        # Remove active vehicles that don't have slots
        cursor.execute('''
            DELETE FROM active_vehicles 
            WHERE slot_id NOT IN (SELECT slot_id FROM slots)
        ''')

        # Remove parking history for non-existent vehicles
        cursor.execute('''
            DELETE FROM parking_history 
            WHERE vehicle_num NOT IN (SELECT vehicle_number FROM vehicles_master)
        ''')

        conn.commit()
        conn.close()

        logging.info("Orphaned records cleaned up")
        return True

    except Exception as e:
        logging.error(f"Error cleaning up orphaned records: {e}")
        return False

def clear_daily_summaries(older_than_days=30):
    """
    Clear old daily summaries
    """
    try:
        cutoff_date = datetime.now().date() - timedelta(days=older_than_days)

        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM daily_summary WHERE date < ?', (cutoff_date,))

        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()

        logging.info(f"Deleted {deleted_count} old daily summary records")
        return deleted_count

    except Exception as e:
        logging.error(f"Error clearing daily summaries: {e}")
        return 0
