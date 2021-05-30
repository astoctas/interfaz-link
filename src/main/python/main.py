from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QSystemTrayIcon, QPlainTextEdit, QLabel, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (QTimer, pyqtSignal)
from serial.tools import list_ports
from PyQt5 import uic
import os
import sys
import threading
from pyInterfaz.pyInterfaz import interfaz
from socketmessages import SocketMessages
from flask import Flask
from flask_socketio import SocketIO

# create a Socket.IO server
sioapp = Flask(__name__)
sioapp.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(sioapp, async_mode='threading', cors_allowed_origins='*')
socket_port = 4268;

def start_server():
    sio.run(sioapp, port=socket_port)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class UI(QMainWindow):
    consoleTrigger = pyqtSignal([str])
    connected_port = False

    def __init__(self):
        super(UI, self).__init__()
        self.consoleTrigger.connect(self.log)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(resource_path("mainwindow.ui"), self)
        self.icon = QIcon(resource_path(os.path.join("icons","base","64.png")))
        self.setWindowIcon(self.icon)
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.show()
        self.tray.setVisible(True);
        #self.tray.showMessage("title", "msg");
        # Creating the options
        menu = QMenu()
        _option1 = QAction("Abrir", self)
        _option1.triggered.connect(self.show)
        menu.addAction(_option1)
        _option2 = QAction("Ocultar", self)
        _option2.triggered.connect(self.hide)
        menu.addAction(_option2)
        # To quit the app
        _quit = QAction("Salir", self)
        _quit.triggered.connect(app.quit)
        menu.addAction(_quit)

        # Adding options to the System Tray
        self.tray.activated.connect(self.trigger_window)
        self.tray.setContextMenu(menu)
        # GET COMPONENTS
        self.console = self.findChild(QPlainTextEdit, "console");
        self.combo = self.findChild(QComboBox, "comboBox");
        self.conectar_button = self.findChild(QPushButton, "conectarButton");
        self.conectar_button.clicked.connect(self.conectar_button_click)
        self.connected_label = self.findChild(QLabel, "connected_label")
        # Start socket server
        ss = SocketMessages(sio, self)
        x = threading.Thread(target=start_server, args=(), daemon=True)
        x.start()
        self.log("Servidor socket corriendo en: http://127.0.0.1:"+str(socket_port))

        #start serial timer
        self.update_serial_ports()
        self.disconnectTimer = QTimer(self)
        self.disconnectTimer.timeout.connect(self.is_connected)
        self.disconnectTimer.start(1000)
        self.connectTimer = QTimer(self)
        self.connectTimer.timeout.connect(self.auto_connect)
        self.connectTimer.start(2000)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_serial_ports)
        self.timer.start(5000)

        if sys.platform.startswith('win'):
            self.showMinimized()
        else:
            self.show()
        self.hide()

    def trigger_window(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()

    def update_serial_ports(self):
        serial_ports = self.list_serialports()
        if self.combo.count() == len(serial_ports):
            return
        self.combo.clear()
        #self.combo.addItem('Automático', None)
        for s in serial_ports:
            self.combo.addItem(s.device + ' ' + s.description, s)
        if self.connected_port:
            for s in serial_ports:
                index = self.combo.findData(s);
                self.combo.setCurrentIndex(index);

    def auto_connect(self):
        if self.connected_port:
            return
        serial_ports = self.list_serialports()
        for s in serial_ports:
                try:
                    if self.conectar_interfaz(s):
                        break
                except:
                    continue

    def is_connected(self):
        if not self.connected_port:
            return False
        serial_ports = self.list_serialports()
        if not (self.connected_port in serial_ports):
            # SE DESCONECTÓ
            self.connected_port = False;
            self.update_serial_ports()
            self.update_connect_label(0)
            return False
        return True

    def list_serialports(self):
        serial_ports = []
        #print('Opening all potential serial ports...')
        the_ports_list = list_ports.comports()
        for port in the_ports_list:
            #print(port)
            if port.pid != None:
                serial_ports.append(port)
        return serial_ports

    def conectar_interfaz(self, port):
        self.log("Intefaz conectando en " + port.device)
        self.update_connect_label(3)
        app.processEvents()
        try:
            self.i = interfaz(port.device)
        except Exception as inst:
            self.update_connect_label(0)
            self.log("No se ha podido acceder al puerto")
            print(inst)
        else:
            self.connected_port = port
            self.log("Intefaz conectada en " + port.device)
            self.update_connect_label(1)
            return True

    def conectar_button_click(self):
        port = self.combo.currentData()
        self.conectar_interfaz(port)

    def update_connect_label(self, value):
        if value == 1:
            self.connected_label.setText("Conectado")
            self.connected_label.setStyleSheet("color: green")
        elif value == 3:
                self.connected_label.setText("Conectando")
                self.connected_label.setStyleSheet("color: orange")
        else:
            self.connected_label.setText("Desconectado")
            self.connected_label.setStyleSheet("color: red")

    def log(self, msg):
        self.console.appendPlainText(msg);
        print(msg)

if __name__ == '__main__':
    app = QApplication([])
    window = UI()
    exit_code = app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)