import os
import sys

from PyQt5.QtWidgets import QApplication
from ui.Index import UIIndexWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = UIIndexWindow()
    myWindow.show()
    sys.exit(app.exec_())