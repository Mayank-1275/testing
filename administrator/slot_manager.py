# slot_manager.py
from PyQt5 import QtWidgets, QtCore
from admin_gui import make_card, make_section_label, make_primary_button, make_ghost_button, make_combo, maximize_window
from database_manager import db
import initialize_slots, system_config as cfg

# Separate Add Slot Window (has Back button)
class AddSlotWindow(QtWidgets.QWidget):
    def __init__(self, parent_refresh_fn=None):
        super().__init__()
        self.setWindowTitle("Add Slot")
        self.parent_refresh_fn = parent_refresh_fn
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        main_layout.addWidget(make_section_label("Add Slot"))

        card = make_card()
        grid = QtWidgets.QGridLayout()
        grid.setColumnStretch(1, 1)

        self.zone_cb = make_combo(cfg.DEFAULT_ZONE_LIST)
        self.type_cb = make_combo(cfg.DEFAULT_TYPE_LIST)
        self.location_cb = make_combo(cfg.DEFAULT_LOCATION_LIST)

        grid.addWidget(QtWidgets.QLabel("Zone:"), 0, 0)
        grid.addWidget(self.zone_cb, 0, 1)
        grid.addWidget(QtWidgets.QLabel("Type:"), 1, 0)
        grid.addWidget(self.type_cb, 1, 1)
        grid.addWidget(QtWidgets.QLabel("Location:"), 2, 0)
        grid.addWidget(self.location_cb, 2, 1)

        card.layout().addLayout(grid)

        btn_row = QtWidgets.QHBoxLayout()
        self.add_btn = make_primary_button("Add Slot")
        self.add_btn.clicked.connect(self.add_slot)
        btn_row.addWidget(self.add_btn)

        self.back_btn = make_ghost_button("Back")
        self.back_btn.clicked.connect(self.close)
        btn_row.addWidget(self.back_btn)

        card.layout().addLayout(btn_row)
        main_layout.addWidget(card)
        self.status = QtWidgets.QLabel("")
        main_layout.addWidget(self.status)
        self.setLayout(main_layout)

    def add_slot(self):
        seq = db.fetchone("SELECT seq FROM sqlite_sequence WHERE name='slots'")
        next_id = (seq["seq"] + 1) if seq else 1
        slot_code = f"SLOT-{next_id:03d}"
        zone = self.zone_cb.currentText()
        type_ = self.type_cb.currentText()
        location = self.location_cb.currentText()
        db.execute("INSERT INTO slots (slot_code, zone, type, location, occupied) VALUES (?, ?, ?, ?, ?)",
                   (slot_code, zone, type_, location, 0), commit=True)
        self.status.setText(f"Added {slot_code}")
        if callable(self.parent_refresh_fn):
            self.parent_refresh_fn()

class SlotManagerWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GuideLo — Slot Manager")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)
        main_layout.addWidget(make_section_label("Slot Manager"))

        top_card = make_card()
        top_card.layout().addWidget(make_section_label("Import or Add Slots"))

        # CSV import button (opens dialog immediately, but window stays separate)
        self.csv_btn = make_primary_button("Import Slots from CSV")
        self.csv_btn.clicked.connect(self.import_csv)
        top_card.layout().addWidget(self.csv_btn)

        # Open Add Slot page button (opens new window)
        self.open_add_btn = make_primary_button("Open Add Slot Page")
        self.open_add_btn.clicked.connect(self.open_add_slot_window)
        top_card.layout().addWidget(self.open_add_btn)

        main_layout.addWidget(top_card)

        # Existing slots card
        list_card = make_card()
        list_card.layout().addWidget(make_section_label("Existing Slots"))
        self.slot_list = QtWidgets.QListWidget()
        list_card.layout().addWidget(self.slot_list)
        main_layout.addWidget(list_card)

        # Back / Close button for Slot Manager - closes this window
        bottom_row = QtWidgets.QHBoxLayout()
        self.close_btn = make_ghost_button("Back / Close")
        self.close_btn.clicked.connect(self.close)
        bottom_row.addStretch()
        bottom_row.addWidget(self.close_btn)
        main_layout.addLayout(bottom_row)

        self.setLayout(main_layout)
        self.refresh_slot_list()

    def refresh_slot_list(self):
        rows = db.fetchall("SELECT id, slot_code, zone, type, location, occupied FROM slots ORDER BY id DESC")
        self.slot_list.clear()
        for r in rows:
            self.slot_list.addItem(f"ID:{r['id']} Code:{r['slot_code']} Zone:{r['zone']} Type:{r['type']} Loc:{r['location']} Occ:{r['occupied']}")

    def import_csv(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if fname:
            initialize_slots.import_from_csv(fname)
            self.refresh_slot_list()

    def open_add_slot_window(self):
        # open separate add slot window and pass refresh function
        self.add_win = AddSlotWindow(parent_refresh_fn=self.refresh_slot_list)
        maximize_window(self.add_win)
        self.add_win.show()
