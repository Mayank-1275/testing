import sys
from PyQt5.QtWidgets import QApplication
from login import LoginWindow

def main():
    app = QApplication(sys.argv)
    login_win = LoginWindow()
    login_win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
