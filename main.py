<<<<<<< HEAD
from gui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
=======
from gui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
>>>>>>> 3508a699cb3b3084ed8ee2b733643c54a21b8047
    sys.exit(app.exec())