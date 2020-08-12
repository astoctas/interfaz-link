from PyQt5.QtWidgets import QMainWindow, QComboBox, QPushButton, QSystemTrayIcon
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QTimer
from fbs_runtime.application_context.PyQt5 import ApplicationContext
# noinspection PyPackageRequirements
from serial.tools import list_ports
from PyQt5 import uic
import os


def list_serialports():
    serial_ports = []
    print('Opening all potential serial ports...')
    the_ports_list = list_ports.comports()
    for port in the_ports_list:
        print(port)
        if port.pid != None:
            serial_ports.append(port)
    return serial_ports


import sys


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(scriptDir, "mainwindow.ui"), self)
        serial_ports = list_serialports()
        self.icon = QIcon(os.path.join(scriptDir,"..","icons","base","64.png"))
        self.setWindowIcon(self.icon)
        self.tray = QSystemTrayIcon(self.icon)
        self.tray.show()
        #self.tray.showMessage("title", "msg");
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
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = UI()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)