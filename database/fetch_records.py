
import sqlite3
from datetime import datetime, date
from utils import setup_logging
import logging

def get_dashboard_stats():
    """
    Get dashboard statistics
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        # Get total slots
        cursor.execute('SELECT COUNT(*) FROM slots')
        total_slots = cursor.fetchone()[0]

        # Get occupied slots
        cursor.execute('SELECT COUNT(*) FROM slots WHERE is_occupied = 1')
        occupied_slots = cursor.fetchone()[0]

        # Calculate available slots
        available_slots = total_slots - occupied_slots

        # Get total unique vehicles
        cursor.execute('SELECT COUNT(DISTINCT vehicle_number) FROM vehicles_master')
        total_vehicles = cursor.fetchone()[0]

        conn.close()

        return {
            'total_slots': total_slots,
            'occupied_slots': occupied_slots,
            'available_slots': available_slots,
            'total_vehicles': total_vehicles
        }

    except Exception as e:
        logging.error(f"Error getting dashboard stats: {e}")
        return {
            'total_slots': 0,
            'occupied_slots': 0,
            'available_slots': 0,
            'total_vehicles': 0
        }

def get_zone_stats():
    """
    Get zone-wise statistics
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT zone, 
                   COUNT(*) as total,
                   SUM(CASE WHEN is_occupied = 1 THEN 1 ELSE 0 END) as occupied,
                   SUM(CASE WHEN is_occupied = 0 THEN 1 ELSE 0 END) as available
            FROM slots 
            GROUP BY zone
            ORDER BY zone
        ''')

        result = cursor.fetchall()
        conn.close()
        return result

    except Exception as e:
        logging.error(f"Error getting zone stats: {e}")
        return []

def get_active_vehicles():
    """
    Get currently parked vehicles
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT av.vehicle_number, vm.vehicle_type, vm.category, 
                   'Slot ' || av.slot_id || ' (Zone ' || av.zone || ')',
                   datetime(av.entry_time, 'localtime')
            FROM active_vehicles av
            JOIN vehicles_master vm ON av.vehicle_number = vm.vehicle_number
            ORDER BY av.entry_time DESC
        ''')

        result = cursor.fetchall()
        conn.close()
        return result

    except Exception as e:
        logging.error(f"Error getting active vehicles: {e}")
        return []

def find_available_slot(zone, prefer_corner=False, prefer_front=False):
    """
    Find available slot in specified zone
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        if prefer_corner:
            # Prefer higher slot numbers (corner slots)
            cursor.execute('''
                SELECT slot_id FROM slots 
                WHERE zone = ? AND is_occupied = 0 
                ORDER BY slot_id DESC LIMIT 1
            ''', (zone,))
        elif prefer_front:
            # Prefer lower slot numbers (front slots)
            cursor.execute('''
                SELECT slot_id FROM slots 
                WHERE zone = ? AND is_occupied = 0 
                ORDER BY slot_id ASC LIMIT 1
            ''', (zone,))
        else:
            # Default: first available slot
            cursor.execute('''
                SELECT slot_id FROM slots 
                WHERE zone = ? AND is_occupied = 0 
                LIMIT 1
            ''', (zone,))

        result = cursor.fetchone()
        conn.close()

        if result:
            return {'slot_id': result[0]}
        return None

    except Exception as e:
        logging.error(f"Error finding available slot: {e}")
        return None

def is_vehicle_parked(vehicle_number):
    """
    Check if vehicle is currently parked
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        cursor.execute('SELECT 1 FROM active_vehicles WHERE vehicle_number = ?', 
                      (vehicle_number,))
        result = cursor.fetchone()
        conn.close()

        return result is not None

    except Exception as e:
        logging.error(f"Error checking if vehicle is parked: {e}")
        return False

def get_vehicle_history(vehicle_number):
    """
    Get parking history for a specific vehicle
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT vehicle_num, slot_id, zone, entry_time, exit_time, duration_min
            FROM parking_history 
            WHERE vehicle_num = ? AND exit_time IS NOT NULL
            ORDER BY entry_time DESC
        ''', (vehicle_number,))

        columns = ['vehicle_num', 'slot_id', 'zone', 'entry_time', 'exit_time', 'duration_min']
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()

        return result

    except Exception as e:
        logging.error(f"Error getting vehicle history: {e}")
        return []

def get_parked_vehicle_info(vehicle_number):
    """
    Get current parking information for a vehicle
    """
    try:
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT slot_id, zone, entry_time
            FROM active_vehicles 
            WHERE vehicle_number = ?
        ''', (vehicle_number,))

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                'slot_id': result[0],
                'zone': result[1],
                'entry_time': result[2]
            }
        return None

    except Exception as e:
        logging.error(f"Error getting parked vehicle info: {e}")
        return None

def get_parking_history_data(target_date=None):
    """
    Get parking history data for reports
    """
    try:
        if not target_date:
            target_date = date.today()

        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT ph.vehicle_num, vm.vehicle_type, vm.category, ph.slot_id, 
                   ph.zone, ph.entry_time, ph.exit_time, ph.duration_min
            FROM parking_history ph
            JOIN vehicles_master vm ON ph.vehicle_num = vm.vehicle_number
            WHERE DATE(ph.entry_time) = ?
            ORDER BY ph.entry_time
        ''', (target_date,))

        columns = ['vehicle_num', 'vehicle_type', 'category', 'slot_id', 
                  'zone', 'entry_time', 'exit_time', 'duration_min']
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()

        return result

    except Exception as e:
        logging.error(f"Error getting parking history data: {e}")
        return []
