from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem,
                             QLineEdit, QComboBox, QMessageBox, QGridLayout)
from PyQt5.QtCore import Qt, QTimer
import sqlite3
from datetime import datetime
from PyQt5.QtGui import QFont


class DashboardWindow(QMainWindow):
    def __init__(self, username, role):
        super().__init__()
        self.username = username
        self.role = role
        self.setWindowTitle(f'Parking Dashboard - {self.username}')
        self.setGeometry(100, 100, 1200, 800)
        self.init_ui()
        self.setup_timer()
        self.load_dashboard_data()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        v_layout = QVBoxLayout()

        # Header
        header = self.create_header()
        v_layout.addWidget(header)

        # Tabs
        self.tabs = QTabWidget()

        self.tab_dashboard = QWidget()
        self.tab_vehicle_entry = QWidget()
        self.tab_vehicle_exit = QWidget()
        self.tab_history = QWidget()

        self.tabs.addTab(self.tab_dashboard, "📊 Dashboard")
        self.tabs.addTab(self.tab_vehicle_entry, "🚗 Vehicle Entry")
        self.tabs.addTab(self.tab_vehicle_exit, "🚪 Vehicle Exit")
        self.tabs.addTab(self.tab_history, "📋 History")

        self.init_dashboard_tab()
        self.init_vehicle_entry_tab()
        self.init_vehicle_exit_tab()
        self.init_history_tab()

        v_layout.addWidget(self.tabs)
        main_widget.setLayout(v_layout)

    def create_header(self):
        header = QWidget()
        layout = QHBoxLayout()
        title = QLabel('🚗 Smart Parking System')
        title.setFont(QFont('Arial', 16, QFont.Bold))
        user_lbl = QLabel(f'Logged in as: {self.username} ({self.role})')
        logout_btn = QPushButton('Logout')
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(user_lbl)
        layout.addWidget(logout_btn)
        header.setLayout(layout)
        return header

    def init_dashboard_tab(self):
        layout = QVBoxLayout()
        # Stats Cards
        stats_layout = QHBoxLayout()
        self.total_slots_label = QLabel('Total Slots: 0')
        self.occupied_slots_label = QLabel('Occupied: 0')
        self.available_slots_label = QLabel('Available: 0')
        self.total_vehicles_label = QLabel('Vehicles: 0')
        for lbl in [self.total_slots_label, self.occupied_slots_label,
                    self.available_slots_label, self.total_vehicles_label]:
            lbl.setStyleSheet('font-size: 16px; padding: 10px; border: 1px solid #ccc; border-radius: 5px;')
            stats_layout.addWidget(lbl)
        layout.addLayout(stats_layout)

        # Zone info table
        self.zone_table = QTableWidget()
        self.zone_table.setColumnCount(4)
        self.zone_table.setHorizontalHeaderLabels(['Zone', 'Total Slots', 'Occupied', 'Available'])
        layout.addWidget(self.zone_table)

        self.tab_dashboard.setLayout(layout)

    def init_vehicle_entry_tab(self):
        layout = QVBoxLayout()
        form = QWidget()
        grid = QGridLayout()

        # Vehicle Number
        grid.addWidget(QLabel('Vehicle Number:'), 0, 0)
        self.entry_vehicle_num = QLineEdit()
        self.entry_vehicle_num.setPlaceholderText('e.g., MH01AB1234')
        grid.addWidget(self.entry_vehicle_num, 0, 1)

        # Vehicle Type
        grid.addWidget(QLabel('Vehicle Type:'), 1, 0)
        self.entry_vehicle_type = QComboBox()
        self.entry_vehicle_type.addItems(['Car', 'Bike'])
        grid.addWidget(self.entry_vehicle_type, 1, 1)

        # Category
        grid.addWidget(QLabel('Category:'), 2, 0)
        self.entry_category = QComboBox()
        self.entry_category.addItems(['Student', 'Faculty', 'VIP'])
        grid.addWidget(self.entry_category, 2, 1)

        # Park button
        park_btn = QPushButton('Park Vehicle')
        park_btn.clicked.connect(self.park_vehicle)
        grid.addWidget(park_btn, 3, 0, 1, 2)

        form.setLayout(grid)
        layout.addWidget(form)
        self.tab_vehicle_entry.setLayout(layout)

    def init_vehicle_exit_tab(self):
        layout = QVBoxLayout()

        # Vehicle exit form
        form = QWidget()
        grid = QGridLayout()
        self.exit_vehicle_num_input = QLineEdit()
        self.exit_vehicle_num_input.setPlaceholderText('Enter vehicle number')
        grid.addWidget(QLabel('Vehicle Number:'), 0, 0)
        grid.addWidget(self.exit_vehicle_num_input, 0, 1)

        exit_btn = QPushButton('Exit Vehicle')
        exit_btn.clicked.connect(self.exit_vehicle)
        grid.addWidget(exit_btn, 1, 0, 1, 2)

        form.setLayout(grid)
        layout.addWidget(form)

        # Current parking
        lbl_current = QLabel('Currently Parked Vehicles:')
        self.table_current = QTableWidget()
        self.table_current.setColumnCount(5)
        self.table_current.setHorizontalHeaderLabels(['Vehicle', 'Type', 'Category', 'Slot', 'Entry'])
        layout.addWidget(lbl_current)
        layout.addWidget(self.table_current)

        self.tab_vehicle_exit.setLayout(layout)

    def init_history_tab(self):
        layout = QVBoxLayout()
        self.table_history = QTableWidget()
        self.table_history.setColumnCount(7)
        self.table_history.setHorizontalHeaderLabels(['Vehicle', 'Type', 'Category', 'Slot', 'Entry', 'Exit', 'Duration'])
        layout.addWidget(QLabel('Parking History'))
        layout.addWidget(self.table_history)
        self.tab_history.setLayout(layout)

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_dashboard_data)
        self.timer.start(30000)  # refresh every 30 sec

    def load_dashboard_data(self):
        conn = sqlite3.connect('parking_system.db')
        c = conn.cursor()
        # Get total slots info
        c.execute('SELECT COUNT(*) FROM slots')
        total_slots = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM slots WHERE is_occupied=1')
        occupied = c.fetchone()[0]
        available = total_slots - occupied
        c.execute('SELECT COUNT(DISTINCT vehicle_number) FROM vehicles_master')
        total_vehicles = c.fetchone()[0]
        self.total_slots_label.setText(f'Total Slots: {total_slots}')
        self.occupied_slots_label.setText(f'Occupied: {occupied}')
        self.available_slots_label.setText(f'Available: {available}')
        self.total_vehicles_label.setText(f'Vehicles: {total_vehicles}')
        # Zone summary
        c.execute('''SELECT zone, COUNT(*) as total_slots, SUM(is_occupied) as occupied
                     FROM slots GROUP BY zone''')
        self.zone_table.setRowCount(0)
        for row_idx, row in enumerate(c.fetchall()):
            zone, total, occupied_in_zone = row
            available_zone = total - occupied_in_zone
            self.zone_table.insertRow(row_idx)
            self.zone_table.setItem(row_idx, 0, QTableWidgetItem(f"Zone {zone}"))
            self.zone_table.setItem(row_idx, 1, QTableWidgetItem(str(total)))
            self.zone_table.setItem(row_idx, 2, QTableWidgetItem(str(occupied_in_zone)))
            self.zone_table.setItem(row_idx, 3, QTableWidgetItem(str(available_zone)))
        # Current vehicles
        c.execute('''SELECT av.vehicle_number, vm.vehicle_type, vm.category, 
                     'Slot ' || av.slot_id || ' (' || av.zone || ')', 
                     datetime(av.entry_time) FROM active_vehicles av 
                     JOIN vehicles_master vm ON av.vehicle_number = vm.vehicle_number''')
        self.table_current.setRowCount(0)
        for row_idx, row in enumerate(c.fetchall()):
            for col_idx, val in enumerate(row):
                self.table_current.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))
        # refresh history table
        self.load_history()
        conn.close()

    def load_history(self):
        conn = sqlite3.connect('parking_system.db')
        c = conn.cursor()
        c.execute('''SELECT vehicle_num, vehicle_type, category, slot_id, entry_time, exit_time, duration_min 
                     FROM parking_history''')
        self.table_history.setRowCount(0)
        for row_idx, row in enumerate(c.fetchall()):
            for col_idx, val in enumerate(row):
                self.table_history.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))
        conn.close()

    def park_vehicle(self):
        vehicle_number = self.entry_vehicle_num.text().upper().strip()
        v_type = self.entry_vehicle_type.currentText()
        category = self.entry_category.currentText()
        if not vehicle_number:
            QMessageBox.warning(self, 'Error', 'Enter vehicle number')
            return
        conn = sqlite3.connect('parking_system.db')
        c = conn.cursor()
        # Check duplicate
        c.execute('SELECT * FROM active_vehicles WHERE vehicle_number=?', (vehicle_number,))
        if c.fetchone():
            QMessageBox.warning(self, 'Error', 'Vehicle already parked')
            conn.close()
            return
        # Find slot based on category/zone
        zone_map = {'Student':'A','Faculty':'B','VIP':'C'}
        zone = zone_map.get(category,'A')
        c.execute('SELECT slot_id FROM slots WHERE zone=? AND is_occupied=0 LIMIT 1', (zone,))
        slot = c.fetchone()
        if not slot:
            QMessageBox.warning(self, 'No Slot', f'No slots available in Zone {zone}')
            conn.close()
            return
        slot_id = slot[0]
        now = datetime.now().isoformat()
        # Insert into master
        c.execute('''INSERT OR REPLACE INTO vehicles_master (vehicle_number, vehicle_type, category, first_entry, last_slot)
                     VALUES (?, ?, ?, COALESCE((SELECT first_entry FROM vehicles_master WHERE vehicle_number=?), ?), ?)''',
                   (vehicle_number, v_type, category, vehicle_number, now, now))
        # Update slot
        c.execute('UPDATE slots SET is_occupied=1, vehicle_num=?, entry_time=? WHERE slot_id=?',
                  (vehicle_number, now, slot_id))
        # Add to active
        c.execute('INSERT INTO active_vehicles VALUES (?, ?, ?, ?)',
                  (vehicle_number, slot_id, zone, now))
        # Add to history
        c.execute('''INSERT INTO parking_history (vehicle_num, slot_id, zone, entry_time)
                     VALUES (?, ?, ?, ?)''', (vehicle_number, slot_id, zone, now))
        conn.commit()
        conn.close()
        QMessageBox.information(self, 'Success', f'Vehicle {vehicle_number} parked in Slot {slot_id} (Zone {zone})')
        self.entry_vehicle_num.clear()
        self.load_dashboard_data()

    def exit_vehicle(self):
        vehicle_number = self.exit_vehicle_num_input.text().upper().strip()
        if not vehicle_number:
            QMessageBox.warning(self, 'Error', 'Enter vehicle number')
            return
        conn = sqlite3.connect('parking_system.db')
        c = conn.cursor()
        c.execute('SELECT slot_id, entry_time FROM active_vehicles WHERE vehicle_number=?', (vehicle_number,))
        result = c.fetchone()
        if not result:
            QMessageBox.warning(self, 'Error', 'Vehicle not found')
            conn.close()
            return
        slot_id, entry_time = result
        now = datetime.now().isoformat()
        # Calculate duration
        e_time = datetime.fromisoformat(entry_time)
        exit_time = datetime.fromisoformat(now)
        duration = int((exit_time - e_time).total_seconds() / 60)
        # Free slot
        c.execute('UPDATE slots SET is_occupied=0, vehicle_num=NULL, entry_time=NULL WHERE slot_id=?', (slot_id,))
        c.execute('DELETE FROM active_vehicles WHERE vehicle_number=?', (vehicle_number,))
        # Update history
        c.execute('''UPDATE parking_history 
                     SET exit_time=?, duration_min=? WHERE vehicle_num=? AND exit_time IS NULL''',
                  (now, duration, vehicle_number))
        conn.commit()
        conn.close()
        QMessageBox.information(self, 'Exited', f'{vehicle_number} exited. Duration: {duration} mins')
        self.load_dashboard_data()
        self.exit_vehicle_num_input.clear()

    def logout(self):
        from PyQt5.QtWidgets import QMessageBox
        reply = QMessageBox.question(self, 'Logout', 'Are you sure?',
                                     QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()