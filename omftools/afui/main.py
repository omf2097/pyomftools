import sys
from PyQt5.QtWidgets import QApplication
from .editor import AFUiApp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AFUiApp()
    window.show()
    sys.exit(app.exec_())
