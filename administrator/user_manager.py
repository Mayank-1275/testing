# user_manager.py
from PyQt5 import QtWidgets, QtCore
from admin_gui import make_card, make_section_label, make_primary_button, make_ghost_button, make_input
from database_manager import db

class UserManagerWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GuideLo — User Manager")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)
        main_layout.addWidget(make_section_label("User Management"))

        form_card = make_card()
        form_card.layout().addWidget(make_section_label("Add New User"))

        form_layout = QtWidgets.QFormLayout()
        self.username_input = make_input("username")
        self.password_input = make_input("password")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)

        form_card.layout().addLayout(form_layout)
        self.add_btn = make_primary_button("Add User")
        self.add_btn.clicked.connect(self.add_user)
        form_card.layout().addWidget(self.add_btn, alignment=QtCore.Qt.AlignLeft)

        main_layout.addWidget(form_card)

        list_card = make_card()
        list_card.layout().addWidget(make_section_label("Existing Users"))
        self.user_list = QtWidgets.QListWidget()
        list_card.layout().addWidget(self.user_list)

        # Back button closes window
        bottom = QtWidgets.QHBoxLayout()
        bottom.addStretch()
        self.back_btn = make_ghost_button("Back / Close")
        self.back_btn.clicked.connect(self.close)
        bottom.addWidget(self.back_btn)

        main_layout.addWidget(list_card)
        main_layout.addLayout(bottom)
        self.setLayout(main_layout)
        self.refresh_users()

    def refresh_users(self):
        self.user_list.clear()
        rows = db.fetchall("SELECT id, username, role FROM users ORDER BY id")
        for r in rows:
            self.user_list.addItem(f"ID:{r['id']} {r['username']} ({r['role']})")

    def add_user(self):
        u = self.username_input.text().strip()
        p = self.password_input.text().strip()
        if not u or not p:
            QtWidgets.QMessageBox.warning(self, "Invalid", "Provide username and password")
            return
        db.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", (u, p, "staff"), commit=True)
        self.username_input.clear()
        self.password_input.clear()
        self.refresh_users()
