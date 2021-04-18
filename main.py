import sys
from PyQt5 import QtWidgets

from windows.mainwindow import Ui_MainWindow
import config.config


# open a new window
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    # window.slider_productivity.
    window.show()
    app.exec()
