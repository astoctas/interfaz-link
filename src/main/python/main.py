# import threading
from flask import Flask, render_template
from flask_socketio import SocketIO
import pyfirmata
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QSystemTrayIcon, QPlainTextEdit, QLabel, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (QTimer, pyqtSignal)
from serial.tools import list_ports
from PyQt5 import uic
import os
import sys
from subprocess import run
import importlib

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def update_interfaz():
    try:
        res = run(['pip', 'install', '--upgrade', '--no-deps', '--target='+resource_path(os.path.join('modules','pyInterfaz')), '--ignore-installed', 'pyinterfaz'])
        print(res)
    except:
        print("Falló actualización de librería o Pip no instalado")

#importar pyInterfaz dinamicamente para updates
try:
    sys._MEIPASS
    update_interfaz()
except:
    print("Desarrollo - No se actualiza pyInterfaz")

pyInterfaz = importlib.import_module("modules.pyInterfaz.pyInterfaz.pyInterfaz", package="pyInterfaz")
sioserver = importlib.import_module("modules.pyInterfaz.pyInterfaz.socketioserver", package="socketioserver")

interfaz = pyInterfaz.interfaz
SocketIOServer = sioserver.SocketIOServer

class UI(QMainWindow):
    consoleTrigger = pyqtSignal([str])
    connected_port = False

    def __init__(self):
        super(UI, self).__init__()
        self.connect_status = 0;
        self.consoleTrigger.connect(self.log)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(resource_path("mainwindow.ui"), self)
        self.icon = QIcon(resource_path(os.path.join("icons","base","64.png")))
        self.setWindowIcon(self.icon)
        # Menu
        self.salir_menu = self.findChild(QAction, "actionSalir")
        self.salir_menu.triggered.connect(app.quit)
        self.crear_acceso_directo_menu = self.findChild(QAction, "actionCrear_acceso_directo")
        self.crear_acceso_directo_menu.setVisible(sys.platform.startswith("win"))
        # TrayICON
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
        ss = SocketIOServer(self)

        #start serial timer
        self.devices = []
        self.update_serial_ports()
        self.disconnectTimer = QTimer(self)
        self.disconnectTimer.timeout.connect(self.is_connected)
        self.disconnectTimer.start(1000)
        self.connectTimer = QTimer(self)
        self.connectTimer.timeout.connect(self.auto_connect)
        self.connectTimer.start(2000)

        #if sys.platform.startswith('win'):
        #    self.showMinimized()
        #else:
        #    self.show()
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
        serial_ports = self.list_serialports()
        _devices = list(map(lambda x: x.device, serial_ports))
        if _devices != self.devices:
            self.devices = _devices
            self.update_serial_ports()
            if self.connected_port:
                return
            if len(_devices):
                print("Reconectando...")
                for s in serial_ports:
                    self.update_connect_label(4)
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
            self.i.sp.close()
            self.tray.showMessage("Interfaz robótica","Interfaz desconectada");
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
            if port.device != None:
                serial_ports.append(port)
        return serial_ports

    def conectar_interfaz(self, port):
        self.log("Intefaz conectando en " + port.device)
        self.update_connect_label(3, port.device)
        if self.connected_port:
            self.i.sp.close()
            self.connected_port = False
        try:
            self.i = interfaz(port.device)
        except Exception as inst:
            self.update_connect_label(0)
            self.log("No se ha podido acceder al puerto")
            print(inst)
        else:
            self.connected_port = port
            str1 = "Intefaz "+self.i.modelo+ " conectada en " + port.device
            self.tray.showMessage("Interfaz robótica", str1);
            self.log(str1)
            self.i.lcd().print(0, "Conectado en")
            self.i.lcd().print(1, port.device)
            self.update_connect_label(1, port.device)
            return True

    def conectar_button_click(self):
        port = self.combo.currentData()
        self.conectar_interfaz(port)

    def update_connect_label(self, value, port = ""):
        if value == 1:
            self.connected_label.setText("Conectado en "+port)
            self.connected_label.setStyleSheet("color: green")
        elif value == 3:
                self.connected_label.setText("Conectando en "+port)
                self.connected_label.setStyleSheet("color: orange")
        elif value == 4:
                self.connected_label.setText("Buscando...")
                self.connected_label.setStyleSheet("color: orange")
        else:
            if self.connect_status != 4 :
                self.connected_label.setText("Desconectado")
                self.connected_label.setStyleSheet("color: red")
        self.connect_status = value;
        app.processEvents()

    def log(self, msg):
        self.console.appendPlainText(msg);
        print(msg)

if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    window = UI()
    exit_code = app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)