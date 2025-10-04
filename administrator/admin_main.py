
# admin_main_enhanced.py
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QFrame, QGraphicsDropShadowEffect
from auth import is_first_time, set_first_time_flag
import create_tables, initialize_slots, reset_database, slot_manager, user_manager


class ModernCard(QtWidgets.QFrame):
    """Professional card widget with shadow and hover effects"""

    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("modernCard")
        self.setup_ui(title)
        self.setup_shadow_effect()
        self.setup_hover_animation()

    def setup_ui(self, title):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 25, 30, 25)
        self.main_layout.setSpacing(20)

        if title:
            title_label = QtWidgets.QLabel(title)
            title_label.setObjectName("cardTitle")
            self.main_layout.addWidget(title_label)

    def setup_shadow_effect(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)

    def setup_hover_animation(self):
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(1.0)

        self.hover_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.hover_animation.setDuration(200)

    def enterEvent(self, event):
        self.hover_animation.setStartValue(1.0)
        self.hover_animation.setEndValue(0.95)
        self.hover_animation.start()

    def leaveEvent(self, event):
        self.hover_animation.setStartValue(0.95)
        self.hover_animation.setEndValue(1.0)
        self.hover_animation.start()

    def addWidget(self, widget):
        self.main_layout.addWidget(widget)

    def addLayout(self, layout):
        self.main_layout.addLayout(layout)


class ModernButton(QtWidgets.QPushButton):
    """Enhanced button with animations and modern styling"""

    def __init__(self, text, button_type="primary", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.setObjectName(f"{button_type}Button")
        self.setup_animations()

    def setup_animations(self):
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(200)
        self.scale_animation.setEasingCurve(QEasingCurve.OutCubic)

    def enterEvent(self, event):
        if self.isEnabled():
            current_rect = self.geometry()
            hover_rect = QtCore.QRect(
                current_rect.x() - 2, current_rect.y() - 1,
                current_rect.width() + 4, current_rect.height() + 2
            )
            self.scale_animation.setStartValue(current_rect)
            self.scale_animation.setEndValue(hover_rect)
            self.scale_animation.start()

    def leaveEvent(self, event):
        current_rect = self.geometry()
        normal_rect = QtCore.QRect(
            current_rect.x() + 2, current_rect.y() + 1,
            current_rect.width() - 4, current_rect.height() - 2
        )
        self.scale_animation.setStartValue(current_rect)
        self.scale_animation.setEndValue(normal_rect)
        self.scale_animation.start()


class StatusIndicator(QtWidgets.QFrame):
    """Professional status indicator with icon and text"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statusIndicator")
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setObjectName("statusIcon")
        layout.addWidget(self.icon_label)

        self.text_label = QtWidgets.QLabel()
        self.text_label.setObjectName("statusText")
        layout.addWidget(self.text_label)

        layout.addStretch()

    def set_status(self, status_type, text, icon=""):
        self.setObjectName(f"status{status_type.title()}")
        self.icon_label.setText(icon)
        self.text_label.setText(text)
        self.style().unpolish(self)
        self.style().polish(self)


class FirstTimeActionWindow(QtWidgets.QWidget):
    """Enhanced first-time action window with professional styling"""

    def __init__(self, title, action_fn, success_text):
        super().__init__()
        self.setWindowTitle(f"GuideLo — {title}")
        self.action_fn = action_fn
        self.success_text = success_text
        self.setup_ui()
        self.apply_professional_style()

    def setup_ui(self):
        # Main layout with proper spacing
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # Header
        header_layout = QtWidgets.QVBoxLayout()
        header_layout.setAlignment(QtCore.Qt.AlignCenter)

        # Icon
        icon_label = QtWidgets.QLabel("⚙️")
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        icon_label.setObjectName("actionIcon")
        header_layout.addWidget(icon_label)

        # Title
        title_label = QtWidgets.QLabel(self.windowTitle().replace("GuideLo — ", ""))
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setObjectName("actionTitle")
        header_layout.addWidget(title_label)

        main_layout.addLayout(header_layout)

        # Content card
        content_card = ModernCard()

        # Description
        desc_label = QtWidgets.QLabel("This action is intended to run only during first-time setup.")
        desc_label.setObjectName("actionDescription")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(QtCore.Qt.AlignCenter)
        content_card.addWidget(desc_label)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(15)

        self.run_btn = ModernButton("Run Action", "primary")
        self.run_btn.clicked.connect(self.run_action)
        button_layout.addWidget(self.run_btn)

        self.close_btn = ModernButton("Cancel", "secondary")
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)

        content_card.addLayout(button_layout)
        main_layout.addWidget(content_card)

        # Status indicator
        self.status_indicator = StatusIndicator()
        self.status_indicator.hide()
        main_layout.addWidget(self.status_indicator)

    def run_action(self):
        try:
            self.run_btn.setText("Running...")
            self.run_btn.setEnabled(False)

            # Show processing status
            self.status_indicator.set_status("info", "Processing...", "⏳")
            self.status_indicator.show()

            # Use timer to allow UI update
            QTimer.singleShot(100, self.execute_action)

        except Exception as e:
            self.show_error(f"Error: {e}")

    def execute_action(self):
        try:
            self.action_fn()
            self.status_indicator.set_status("success", self.success_text, "✅")
            self.run_btn.setText("Completed")

        except Exception as e:
            self.status_indicator.set_status("error", f"Error: {e}", "❌")
            self.run_btn.setText("Run Action")
            self.run_btn.setEnabled(True)

    def apply_professional_style(self):
        style = """
        QWidget {
            font-family: 'Segoe UI', 'SF Pro Display', sans-serif;
            background-color: #f8fafc;
        }

        #actionIcon {
            font-size: 64px;
            margin-bottom: 20px;
        }

        #actionTitle {
            font-size: 28px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 10px;
        }

        #actionDescription {
            font-size: 16px;
            color: #64748b;
            margin-bottom: 30px;
            line-height: 1.6;
        }

        #modernCard {
            background: white;
            border-radius: 16px;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }

        #primaryButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #4f46e5, stop:1 #7c3aed);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: 600;
            min-height: 45px;
        }

        #primaryButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #4338ca, stop:1 #6d28d9);
        }

        #primaryButton:disabled {
            background: #9ca3af;
        }

        #secondaryButton {
            background: #f1f5f9;
            color: #64748b;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: 600;
            min-height: 45px;
        }

        #secondaryButton:hover {
            background: #e2e8f0;
            color: #475569;
        }

        #statusIndicator {
            border-radius: 12px;
            border: 2px solid transparent;
        }

        #statusSuccess {
            background-color: #ecfdf5;
            border-color: #10b981;
        }

        #statusError {
            background-color: #fef2f2;
            border-color: #ef4444;
        }

        #statusInfo {
            background-color: #eff6ff;
            border-color: #3b82f6;
        }

        #statusIcon {
            font-size: 20px;
            font-weight: bold;
        }

        #statusText {
            font-size: 16px;
            font-weight: 600;
        }
        """
        self.setStyleSheet(style)


class AdminMainWindow(QtWidgets.QWidget):
    """Enhanced admin main window with professional styling and animations"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GuideLo — Admin Dashboard")
        self.setup_ui()
        self.apply_professional_style()

    def setup_ui(self):
        # Main scroll area for large content
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("mainScroll")

        # Main content widget
        content_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(content_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(35)

        # Header section
        self.setup_header(main_layout)

        # Status indicator
        self.status_indicator = StatusIndicator()
        main_layout.addWidget(self.status_indicator)

        # First-time setup section
        self.setup_first_time_section(main_layout)

        # Management section
        self.setup_management_section(main_layout)

        # System section
        self.setup_system_section(main_layout)

        scroll.setWidget(content_widget)

        # Main window layout
        window_layout = QtWidgets.QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(scroll)

        self.update_first_time_ui()

    def setup_header(self, layout):
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setSpacing(20)

        # Logo and title
        logo_title_layout = QtWidgets.QHBoxLayout()

        logo_label = QtWidgets.QLabel("🏢")
        logo_label.setObjectName("mainLogo")
        logo_title_layout.addWidget(logo_label)

        title_container = QtWidgets.QVBoxLayout()
        title_container.setSpacing(5)

        title_label = QtWidgets.QLabel("Admin Dashboard")
        title_label.setObjectName("mainTitle")
        title_container.addWidget(title_label)

        subtitle_label = QtWidgets.QLabel("System Management & Configuration")
        subtitle_label.setObjectName("mainSubtitle")
        title_container.addWidget(subtitle_label)

        logo_title_layout.addLayout(title_container)
        logo_title_layout.addStretch()

        header_layout.addLayout(logo_title_layout)
        layout.addLayout(header_layout)

    def setup_first_time_section(self, layout):
        self.ft_card = ModernCard("🚀 Initial Setup")

        desc_label = QtWidgets.QLabel("Complete these steps to set up your system for first use:")
        desc_label.setObjectName("sectionDescription")
        self.ft_card.addWidget(desc_label)

        # Setup buttons in a grid
        buttons_grid = QtWidgets.QGridLayout()
        buttons_grid.setSpacing(15)

        # Create Tables button
        self.create_tables_btn = ModernButton("🗄️ Create Database Tables", "primary")
        self.create_tables_btn.clicked.connect(self.open_create_tables_window)
        buttons_grid.addWidget(self.create_tables_btn, 0, 0)

        # Initialize Slots button
        self.initialize_slots_btn = ModernButton("🎯 Initialize Default Slots", "primary")
        self.initialize_slots_btn.clicked.connect(self.open_initialize_slots_window)
        buttons_grid.addWidget(self.initialize_slots_btn, 0, 1)

        # Import CSV button
        self.import_csv_btn = ModernButton("📊 Import Master CSV", "primary")
        self.import_csv_btn.clicked.connect(self.open_import_csv_window)
        buttons_grid.addWidget(self.import_csv_btn, 1, 0, 1, 2)

        self.ft_card.addLayout(buttons_grid)
        layout.addWidget(self.ft_card)

    def setup_management_section(self, layout):
        mgmt_card = ModernCard("⚙️ Management Tools")

        desc_label = QtWidgets.QLabel("Access system management tools:")
        desc_label.setObjectName("sectionDescription")
        mgmt_card.addWidget(desc_label)

        buttons_row = QtWidgets.QHBoxLayout()
        buttons_row.setSpacing(20)

        self.slot_manager_btn = ModernButton("🎰 Slot Manager", "secondary")
        self.slot_manager_btn.clicked.connect(self.open_slot_manager)
        buttons_row.addWidget(self.slot_manager_btn)

        self.user_manager_btn = ModernButton("👥 User Manager", "secondary")
        self.user_manager_btn.clicked.connect(self.open_user_manager)
        buttons_row.addWidget(self.user_manager_btn)

        mgmt_card.addLayout(buttons_row)
        layout.addWidget(mgmt_card)

    def setup_system_section(self, layout):
        system_card = ModernCard("🔧 System Administration")

        desc_label = QtWidgets.QLabel("System-level operations (use with caution):")
        desc_label.setObjectName("sectionDescription")
        system_card.addWidget(desc_label)

        self.reset_btn = ModernButton("🔄 Reset System", "danger")
        self.reset_btn.clicked.connect(self.reset_system)
        system_card.addWidget(self.reset_btn)

        layout.addWidget(system_card)

    def update_first_time_ui(self):
        ft = is_first_time()
        self.ft_card.setVisible(ft)

        if ft:
            self.status_indicator.set_status("warning", 
                "First-time setup is active. Complete the initial setup steps below.", "⚠️")
        else:
            self.status_indicator.set_status("success", 
                "System is ready. All initial setup steps have been completed.", "✅")

    # First-time action windows
    def open_create_tables_window(self):
        def job():
            create_tables.run_first_time_setup()
            set_first_time_flag(False)
            self.update_first_time_ui()
        w = FirstTimeActionWindow("Create Database Tables", job, "Database tables created successfully!")
        w.showMaximized()

    def open_initialize_slots_window(self):
        def job():
            initialize_slots.initialize_default_slots(30)
            set_first_time_flag(False)
            self.update_first_time_ui()
        w = FirstTimeActionWindow("Initialize Default Slots", job, "Default slots initialized successfully!")
        w.showMaximized()

    def open_import_csv_window(self):
        def job():
            from PyQt5 import QtWidgets
            fname, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select CSV File", "", "CSV Files (*.csv)")
            if fname:
                initialize_slots.import_from_csv(fname)
                set_first_time_flag(False)
                self.update_first_time_ui()
            else:
                raise Exception("No file selected")
        w = FirstTimeActionWindow("Import Master CSV", job, "CSV file imported successfully!")
        w.showMaximized()

    def open_slot_manager(self):
        self.sm = slot_manager.SlotManagerWindow()
        self.sm.showMaximized()

    def open_user_manager(self):
        self.um = user_manager.UserManagerWindow()
        self.um.showMaximized()

    def reset_system(self):
        reply = QtWidgets.QMessageBox()
        reply.setWindowTitle("Reset System")
        reply.setIcon(QtWidgets.QMessageBox.Warning)
        reply.setText("⚠️ System Reset Confirmation")
        reply.setInformativeText("This will permanently delete all slots and users data and re-enable first-time setup.\n\nThis action cannot be undone. Are you sure you want to continue?")
        reply.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        reply.setDefaultButton(QtWidgets.QMessageBox.No)

        if reply.exec_() == QtWidgets.QMessageBox.Yes:
            try:
                reset_database.reset_all()
                set_first_time_flag(True)
                self.update_first_time_ui()
                self.status_indicator.set_status("success", "System has been reset successfully!", "✅")
            except Exception as e:
                self.status_indicator.set_status("error", f"Reset failed: {e}", "❌")

    def apply_professional_style(self):
        style = """
        QWidget {
            font-family: 'Segoe UI', 'SF Pro Display', 'Arial', sans-serif;
            font-size: 16px;
        }

        QScrollArea {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #f8fafc, stop:1 #e2e8f0);
            border: none;
        }

        #mainScroll {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #f8fafc, stop:1 #e2e8f0);
        }

        #mainLogo {
            font-size: 48px;
            margin-right: 20px;
        }

        #mainTitle {
            font-size: 36px;
            font-weight: 800;
            color: #1e293b;
            letter-spacing: -1px;
        }

        #mainSubtitle {
            font-size: 18px;
            color: #64748b;
            font-weight: 400;
        }

        #modernCard {
            background: white;
            border-radius: 20px;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }

        #cardTitle {
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 10px;
        }

        #sectionDescription {
            font-size: 16px;
            color: #64748b;
            margin-bottom: 25px;
            line-height: 1.5;
        }

        #primaryButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #4f46e5, stop:1 #7c3aed);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 18px 25px;
            font-size: 16px;
            font-weight: 600;
            min-height: 55px;
            text-align: left;
        }

        #primaryButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #4338ca, stop:1 #6d28d9);
        }

        #primaryButton:disabled {
            background: #9ca3af;
        }

        #secondaryButton {
            background: white;
            color: #475569;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 18px 25px;
            font-size: 16px;
            font-weight: 600;
            min-height: 55px;
        }

        #secondaryButton:hover {
            background: #f8fafc;
            border-color: #cbd5e1;
            color: #334155;
        }

        #dangerButton {
            background: #fef2f2;
            color: #dc2626;
            border: 2px solid #fecaca;
            border-radius: 12px;
            padding: 18px 25px;
            font-size: 16px;
            font-weight: 600;
            min-height: 55px;
        }

        #dangerButton:hover {
            background: #fee2e2;
            border-color: #fca5a5;
            color: #b91c1c;
        }

        #statusIndicator {
            border-radius: 16px;
            border: 2px solid transparent;
        }

        #statusSuccess {
            background-color: #ecfdf5;
            border-color: #10b981;
        }

        #statusError {
            background-color: #fef2f2;
            border-color: #ef4444;
        }

        #statusWarning {
            background-color: #fffbeb;
            border-color: #f59e0b;
        }

        #statusInfo {
            background-color: #eff6ff;
            border-color: #3b82f6;
        }

        #statusIcon {
            font-size: 24px;
        }

        #statusText {
            font-size: 18px;
            font-weight: 600;
        }
        """
        self.setStyleSheet(style)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    window = AdminMainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
