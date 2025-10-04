# initialize_slots.py
# Functions to create initial slots: default and CSV import.
import csv
from database_manager import db
import system_config as cfg

def initialize_default_slots(n=10):
    for i in range(1, n+1):
        code = f"SLOT-{i:03d}"
        db.execute("INSERT OR IGNORE INTO slots (slot_code, zone, type, location, occupied) VALUES (?, ?, ?, ?, ?)",
                   (code, cfg.DEFAULT_ZONE_LIST[i % len(cfg.DEFAULT_ZONE_LIST)],
                    cfg.DEFAULT_TYPE_LIST[i % len(cfg.DEFAULT_TYPE_LIST)],
                    cfg.DEFAULT_LOCATION_LIST[i % len(cfg.DEFAULT_LOCATION_LIST)], 0), commit=True)

def import_from_csv(path):
    # CSV expected columns: slot_code,zone,type,location
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            slot_code = r.get("slot_code") or None
            zone = r.get("zone") or None
            type_ = r.get("type") or None
            location = r.get("location") or None
            db.execute("INSERT OR IGNORE INTO slots (slot_code, zone, type, location, occupied) VALUES (?, ?, ?, ?, ?)",
                       (slot_code, zone, type_, location, 0), commit=True)

if __name__ == "__main__":
    initialize_default_slots(30)
    print("Default slots added.")
