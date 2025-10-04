
import sqlite3
from utils import setup_logging
import logging

def initialize_database():
    """
    Initialize database with all required tables
    """
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'staff'
            )
        ''')

        # Create vehicles_master table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles_master (
                vehicle_number TEXT PRIMARY KEY,
                vehicle_type TEXT NOT NULL,
                category TEXT NOT NULL,
                first_entry DATETIME NOT NULL,
                last_slot TEXT,
                avg_duration INTEGER
            )
        ''')

        # Create slots table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS slots (
                slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                zone TEXT NOT NULL,
                is_occupied BOOLEAN NOT NULL DEFAULT 0,
                vehicle_num TEXT,
                entry_time DATETIME
            )
        ''')

        # Create parking_history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parking_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_num TEXT NOT NULL,
                slot_id INTEGER NOT NULL,
                zone TEXT NOT NULL,
                entry_time DATETIME NOT NULL,
                exit_time DATETIME,
                duration_min INTEGER
            )
        ''')

        # Create active_vehicles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_vehicles (
                vehicle_number TEXT PRIMARY KEY,
                slot_id INTEGER NOT NULL,
                zone TEXT NOT NULL,
                entry_time DATETIME NOT NULL
            )
        ''')

        # Create vehicle_preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicle_preferences (
                vehicle_number TEXT PRIMARY KEY,
                preferred_zone TEXT,
                long_duration BOOLEAN DEFAULT 0
            )
        ''')

        # Create daily_summary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_summary (
                date DATE NOT NULL,
                zone TEXT NOT NULL,
                total_slots INTEGER NOT NULL,
                occupied INTEGER NOT NULL,
                available INTEGER NOT NULL,
                PRIMARY KEY (date, zone)
            )
        ''')

        conn.commit()
        conn.close()

        # Initialize slots if empty
        initialize_slots()

        logger.info("Database initialized successfully")

    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def initialize_slots():
    """
    Initialize parking slots if they don't exist
    """
    conn = sqlite3.connect('parking_system.db')
    cursor = conn.cursor()

    # Check if slots already exist
    cursor.execute('SELECT COUNT(*) FROM slots')
    slot_count = cursor.fetchone()[0]

    if slot_count == 0:
        # Zone A (Student) - 50 slots
        for i in range(1, 51):
            cursor.execute('INSERT INTO slots (zone, is_occupied) VALUES (?, ?)', ('A', 0))

        # Zone B (Faculty) - 30 slots  
        for i in range(1, 31):
            cursor.execute('INSERT INTO slots (zone, is_occupied) VALUES (?, ?)', ('B', 0))

        # Zone C (VIP) - 20 slots
        for i in range(1, 21):
            cursor.execute('INSERT INTO slots (zone, is_occupied) VALUES (?, ?)', ('C', 0))

        conn.commit()
        print("Parking slots initialized successfully")

    conn.close()
