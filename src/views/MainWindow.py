import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QWidget, QComboBox, QStackedWidget, QMainWindow)
from src.views.MainEsriWindow import MainEsriWindow
from src.views.MainGeoserverWindow import MainGeoserverWindow
from src.controllers.EsriController import EsriController
from src.controllers.GeoserverController import GeoserverController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__controller = None
        self.setWindowTitle("PyExtractGeoServices")

        # Verifica si el icono existe
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, 'py_extract_geo.ico')
        else:
            icon_path = os.path.abspath('icon/py_extract_geo.ico')

        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Icon not found: {icon_path}")

        self.service_type_label = QLabel("Service Type:")
        self.service_type_input = QComboBox()
        self.service_type_input.addItems(["Esri Service", "Geoserver Service"])
        self.service_type_input.currentIndexChanged.connect(self.switch_layout)

        self.stack = QStackedWidget(self)

        self.esri_view = MainEsriWindow(EsriController())
        self.geoserver_view = MainGeoserverWindow(GeoserverController())

        self.stack.addWidget(self.esri_view)
        self.stack.addWidget(self.geoserver_view)

        layout = QVBoxLayout()
        layout.addWidget(self.service_type_label)
        layout.addWidget(self.service_type_input)
        layout.addWidget(self.stack)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.switch_layout(0)

    def switch_layout(self, index):
        if index == 0:
            self.controller = EsriController()
            self.esri_view.controller = self.__controller
        else:
            self.controller = GeoserverController()
            self.geoserver_view.controller = self.__controller
        self.stack.setCurrentIndex(index)

    @property
    def controller(self):
        return self.__controller

    @controller.setter
    def controller(self, controller):
        self.__controller = controller
