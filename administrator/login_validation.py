
# # login_validation.py - Enhanced validation with visual feedback
# from PyQt5 import QtWidgets, QtCore, QtGui
# from PyQt5.QtCore import QTimer, QPropertyAnimation
# from PyQt5.QtWidgets import QGraphicsOpacityEffect
# import re


# class ValidationHelper:
#     @staticmethod
#     def validate_username(username):
#         """Validate username with specific rules"""
#         if len(username) < 3:
#             return False, "Username must be at least 3 characters"
#         if not re.match("^[a-zA-Z0-9_]+$", username):
#             return False, "Username can only contain letters, numbers, and underscores"
#         return True, "Valid username"

#     @staticmethod
#     def validate_password(password):
#         """Validate password with security rules"""
#         if len(password) < 6:
#             return False, "Password must be at least 6 characters"
#         if not re.search(r"[A-Za-z]", password):
#             return False, "Password must contain at least one letter"
#         if not re.search(r"[0-9]", password):
#             return False, "Password must contain at least one number"
#         return True, "Strong password"


# class EnhancedInputField(QtWidgets.QLineEdit):
#     """Input field with real-time validation"""

#     def __init__(self, validator_func=None, parent=None):
#         super().__init__(parent)
#         self.validator_func = validator_func
#         self.is_valid = False
#         self.validation_label = QtWidgets.QLabel()
#         self.validation_label.setStyleSheet("font-size: 12px; padding: 5px;")
#         self.validation_label.hide()

#         # Connect text change to validation
#         self.textChanged.connect(self.validate_input)

#     def validate_input(self):
#         if not self.validator_func:
#             return

#         text = self.text().strip()
#         if not text:
#             self.validation_label.hide()
#             self.setStyleSheet("")
#             self.is_valid = False
#             return

#         is_valid, message = self.validator_func(text)
#         self.is_valid = is_valid

#         if is_valid:
#             self.setStyleSheet("border: 2px solid #10b981; background-color: #f0fdf4;")
#             self.validation_label.setText("✓ " + message)
#             self.validation_label.setStyleSheet("color: #10b981; font-size: 12px; padding: 5px;")
#         else:
#             self.setStyleSheet("border: 2px solid #ef4444; background-color: #fef2f2;")
#             self.validation_label.setText("⚠ " + message)
#             self.validation_label.setStyleSheet("color: #ef4444; font-size: 12px; padding: 5px;")

#         self.validation_label.show()

#         # Animate validation message
#         effect = QGraphicsOpacityEffect()
#         self.validation_label.setGraphicsEffect(effect)

#         animation = QPropertyAnimation(effect, b"opacity")
#         animation.setDuration(200)
#         animation.setStartValue(0.0)
#         animation.setEndValue(1.0)
#         animation.start()

#     def get_validation_label(self):
#         return self.validation_label


# class PasswordStrengthIndicator(QtWidgets.QWidget):
#     """Visual password strength indicator"""

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setup_ui()

#     def setup_ui(self):
#         layout = QtWidgets.QHBoxLayout(self)
#         layout.setContentsMargins(0, 5, 0, 5)

#         self.strength_bars = []
#         for i in range(4):
#             bar = QtWidgets.QFrame()
#             bar.setFixedSize(60, 4)
#             bar.setStyleSheet("background-color: #e5e7eb; border-radius: 2px;")
#             self.strength_bars.append(bar)
#             layout.addWidget(bar)

#         self.strength_label = QtWidgets.QLabel("Password strength")
#         self.strength_label.setStyleSheet("font-size: 12px; color: #6b7280; margin-left: 10px;")
#         layout.addWidget(self.strength_label)

#     def update_strength(self, password):
#         strength = self.calculate_strength(password)
#         colors = ["#ef4444", "#f59e0b", "#10b981", "#059669"]
#         labels = ["Weak", "Fair", "Good", "Strong"]

#         for i, bar in enumerate(self.strength_bars):
#             if i < strength:
#                 bar.setStyleSheet(f"background-color: {colors[min(strength-1, 3)]}; border-radius: 2px;")
#             else:
#                 bar.setStyleSheet("background-color: #e5e7eb; border-radius: 2px;")

#         if password:
#             self.strength_label.setText(f"Password strength: {labels[min(strength-1, 3)]}")
#             self.strength_label.setStyleSheet(f"font-size: 12px; color: {colors[min(strength-1, 3)]}; margin-left: 10px;")
#         else:
#             self.strength_label.setText("Password strength")
#             self.strength_label.setStyleSheet("font-size: 12px; color: #6b7280; margin-left: 10px;")

#     def calculate_strength(self, password):
#         if not password:
#             return 0

#         strength = 0
#         if len(password) >= 6:
#             strength += 1
#         if re.search(r"[a-z]", password):
#             strength += 1
#         if re.search(r"[A-Z]", password):
#             strength += 1
#         if re.search(r"[0-9]", password):
#             strength += 1
#         if re.search(r"[!@#$%^&*(),.?":{}|<>]", password):
#             strength += 1

#         return min(strength, 4)


# # Example usage in a login form with enhanced validation
# class ValidatedLoginForm(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setup_ui()

#     def setup_ui(self):
#         layout = QtWidgets.QVBoxLayout(self)
#         layout.setSpacing(15)

#         # Title
#         title = QtWidgets.QLabel("Secure Login")
#         title.setAlignment(QtCore.Qt.AlignCenter)
#         title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
#         layout.addWidget(title)

#         # Username field with validation
#         username_label = QtWidgets.QLabel("Username:")
#         layout.addWidget(username_label)

#         self.username_input = EnhancedInputField(ValidationHelper.validate_username)
#         self.username_input.setPlaceholderText("Enter your username")
#         layout.addWidget(self.username_input)
#         layout.addWidget(self.username_input.get_validation_label())

#         # Password field with validation
#         password_label = QtWidgets.QLabel("Password:")
#         layout.addWidget(password_label)

#         self.password_input = EnhancedInputField(ValidationHelper.validate_password)
#         self.password_input.setPlaceholderText("Enter your password")
#         self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
#         layout.addWidget(self.password_input)
#         layout.addWidget(self.password_input.get_validation_label())

#         # Password strength indicator
#         self.strength_indicator = PasswordStrengthIndicator()
#         layout.addWidget(self.strength_indicator)

#         # Connect password change to strength indicator
#         self.password_input.textChanged.connect(self.strength_indicator.update_strength)

#         # Login button
#         self.login_btn = QtWidgets.QPushButton("Login")
#         self.login_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #3b82f6;
#                 color: white;
#                 border: none;
#                 border-radius: 6px;
#                 padding: 12px;
#                 font-size: 16px;
#                 font-weight: bold;
#             }
#             QPushButton:hover {
#                 background-color: #2563eb;
#             }
#             QPushButton:disabled {
#                 background-color: #9ca3af;
#             }
#         """)
#         self.login_btn.clicked.connect(self.attempt_login)
#         layout.addWidget(self.login_btn)

#         # Status message
#         self.status_label = QtWidgets.QLabel("")
#         self.status_label.setAlignment(QtCore.Qt.AlignCenter)
#         layout.addWidget(self.status_label)

#         # Enable login button only when both fields are valid
#         self.username_input.textChanged.connect(self.update_login_button)
#         self.password_input.textChanged.connect(self.update_login_button)

#     def update_login_button(self):
#         both_valid = self.username_input.is_valid and self.password_input.is_valid
#         self.login_btn.setEnabled(both_valid)

#     def attempt_login(self):
#         username = self.username_input.text().strip()
#         password = self.password_input.text().strip()

#         # Here you would validate against your authentication system
#         if username == "admin" and password == "admin123":
#             self.status_label.setText("✓ Login successful!")
#             self.status_label.setStyleSheet("color: #10b981; font-weight: bold;")
#         else:
#             self.status_label.setText("⚠ Invalid credentials")
#             self.status_label.setStyleSheet("color: #ef4444; font-weight: bold;")


# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])
#     form = ValidatedLoginForm()
#     form.show()
#     app.exec_()
