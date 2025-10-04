import sys
import sqlite3
import hashlib
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from gui import DashboardWindow
from PyQt5.QtGui import QFont


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parking System - Login")
        self.setFixedSize(400, 300)
        self.init_ui()
        self.init_db()

    def init_ui(self):
        self.setStyleSheet('''
            QWidget {
                background-color: #2C3E50;
                color: white;
                font-family: Arial;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #34495E;
                border-radius: 5px;
                background-color: #34495E;
                font-size: 14px;
                color: white;
            }
            QPushButton {
                padding: 10px;
                background-color: #3498DB;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QLabel {
                font-size:14px;
            }
        ''')

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel('🚗 Smart Parking System')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #3498DB; margin-bottom: 20px;')

        form_layout = QVBoxLayout()

        lbl_user = QLabel('Username:')
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText('Enter username')

        lbl_pass = QLabel('Password:')
        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText('Enter password')
        self.input_pass.setEchoMode(QLineEdit.Password)

        btn_login = QPushButton('LOGIN')
        btn_login.clicked.connect(self.authenticate)

        form_layout.addWidget(lbl_user)
        form_layout.addWidget(self.input_user)
        form_layout.addWidget(lbl_pass)
        form_layout.addWidget(self.input_pass)
        form_layout.addWidget(btn_login)

        layout.addWidget(title)
        layout.addLayout(form_layout)
        self.setLayout(layout)

        # Connect enter key
        self.input_pass.returnPressed.connect(self.authenticate)

    def init_db(self):
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
        # Insert default admin if not exists
        default_password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password_hash, role)
            VALUES (?, ?, ?)''', ('admin', default_password_hash, 'admin'))
        conn.commit()
        conn.close()

    def authenticate(self):
        username = self.input_user.text().strip()
        password = self.input_pass.text().strip()
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')
            return
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect('parking_system.db')
        cursor = conn.cursor()
        cursor.execute('SELECT role FROM users WHERE username=? AND password_hash=?', (username, password_hash))
        result = cursor.fetchone()
        conn.close()
        if result:
            self.hide()
            self.dashboard = DashboardWindow(username, result[0])
            self.dashboard.show()
        else:
            QMessageBox.critical(self, 'Login Failed', 'Invalid username or password')
            self.input_pass.clear()