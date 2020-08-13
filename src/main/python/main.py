from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QSystemTrayIcon
from PyQt5.QtGui import QIcon
import serial
from serial.tools import list_ports
from PyQt5 import uic
import os
import sys


def list_serialports():
    serial_ports = []
    print('Opening all potential serial ports...')
    the_ports_list = list_ports.comports()
    for port in the_ports_list:
        print(port)
        if port.pid != None:
            serial_ports.append(port)
    return serial_ports


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(resource_path("mainwindow.ui"), self)
        serial_ports = list_serialports()
        self.icon = QIcon(resource_path(os.path.join("icons","base","64.png")))
        self.setWindowIcon(self.icon)
        self.tray = QSystemTrayIcon(self.icon)
        self.tray.show()
        self.tray.showMessage("title", "msg");
        # GET COMPONENTS
        self.combo = self.findChild(QComboBox, "comboBox");
        self.combo.addItem('Automático', None)
        for s in serial_ports:
            self.combo.addItem(s.device + ' ' + s.description, s)
        self.conectarBtn = self.findChild(QPushButton, "conectarButton");
        self.conectarBtn.clicked.connect(self.clickedConectarBtn)
        self.show()
        #self.showMinimized()
        ### TODO: SYSTEM TRAY ###


    def clickedConectarBtn(self):
        port = self.combo.currentData()


if __name__ == '__main__':
    app = QApplication([])
    window = UI()
    exit_code = app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)