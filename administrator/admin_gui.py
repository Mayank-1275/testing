# admin_gui.py
from PyQt5 import QtWidgets, QtCore, QtGui

APP_STYLE = """
QWidget {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
        stop:0 #e6f0ff, stop:1 #f8fafc);
    font-family: "Segoe UI", Roboto, Arial;
    font-size: 13px;
    color: #0f172a;
}
QLabel#title {
    font-size: 26px;
    font-weight: 800;
    color: #0b1726;
}
QLabel.section {
    font-size: 15px;
    font-weight: 700;
    color: #0f172a;
}
QPushButton.primary {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
      stop:0 #06b6d4, stop:1 #2563eb);
    color: white;
    padding: 10px 18px;
    border-radius: 10px;
    font-weight: 700;
    min-height: 38px;
}
QPushButton.ghost {
    background: transparent;
    border: 1px solid rgba(15,23,42,0.08);
    padding: 8px 14px;
    border-radius: 8px;
}
QLineEdit, QComboBox {
    background: white;
    border: 1px solid #e6eef9;
    border-radius: 8px;
    padding: 8px;
    min-height: 30px;
}
QListWidget {
    background: white;
    border: 1px solid #e6eef9;
    border-radius: 8px;
    min-height: 120px;
}
QFrame#card {
    background: rgba(255,255,255,0.95);
    border-radius: 12px;
    border: 1px solid rgba(15,23,42,0.05);
    padding: 14px;
}
"""

def apply_app_style(app: QtWidgets.QApplication):
    app.setStyleSheet(APP_STYLE)

def make_title(text):
    lbl = QtWidgets.QLabel(text)
    lbl.setObjectName("title")
    lbl.setAlignment(QtCore.Qt.AlignCenter)
    return lbl

def make_section_label(text):
    lbl = QtWidgets.QLabel(text)
    lbl.setProperty("class", "section")
    lbl.setStyleSheet("")  # uses stylesheet
    return lbl

def make_primary_button(text):
    btn = QtWidgets.QPushButton(text)
    btn.setProperty("class", "primary")
    return btn

def make_ghost_button(text):
    btn = QtWidgets.QPushButton(text)
    btn.setProperty("class", "ghost")
    return btn

def make_input(placeholder=""):
    le = QtWidgets.QLineEdit()
    le.setPlaceholderText(placeholder)
    return le

def make_combo(items):
    cb = QtWidgets.QComboBox()
    cb.addItems(items)
    return cb

def make_card():
    frame = QtWidgets.QFrame()
    frame.setObjectName("card")
    frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
    layout = QtWidgets.QVBoxLayout(frame)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(8)
    return frame

def maximize_window(window):
    # Show window maximized (full screen-like)
    window.showMaximized()
