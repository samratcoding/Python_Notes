# pip install pyqt6
# pip install pyqt6-tools

# Qt Designer Path
# env\Lib\site-packages\qt6_applications\Qt\bin

# UI to Py
# Activate virtual Environment, if project in local environment: source env/scripts/activate
# pyuic6 -x gui_path.ui -o py_path.py

# Load UI file
from PyQt6 import uic
uic.loadUi('hello.ui', window) # Functional
uic.loadUi('hello.ui',self) # Class base


# Functional Way
from PyQt6.QtWidgets import *
import sys

app = QApplication(sys.argv)
window = QMainWindow()
window.statusBar().showMessage("Welcome to here")
window.menuBar().addMenu("Open File")

window.setGeometry(0, 0, 700, 300)
window.show()
sys.exit(app.exec())


# Class Base
from PyQt6.QtWidgets import *
import sys
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 700, 400)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
