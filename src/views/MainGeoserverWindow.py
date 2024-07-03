from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QProgressDialog, QMessageBox, \
    QMainWindow
from PyQt5.QtCore import Qt

from src.utils.Utils import is_valid_url, validate_bbox, valid_int
from src.views.MainEsriWindow import QueryLayerThread


class MainGeoserverWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.layer_url_label = QLabel("Layer URL:")
        self.layer_url_input = QLineEdit("https://wmts.mapama.gob.es/sig/cambioclimatico/mc_inst_com_der_emision/ows")

        self.type_name_label = QLabel("Type name")
        self.type_name_input = QLineEdit("mc_inst_com_der_emision")

        self.attr_id_label = QLabel("Atrribute ID")
        self.attr_id_input = QLineEdit("id")

        self.xmin_label = QLabel("XMin:")
        self.xmin_input = QLineEdit("-20.654297")

        self.ymin_label = QLabel("YMin:")
        self.ymin_input = QLineEdit("33.868169")

        self.xmax_label = QLabel("XMax:")
        self.xmax_input = QLineEdit("12.722168")

        self.ymax_label = QLabel("YMax:")
        self.ymax_input = QLineEdit("45.566015")

        self.src_label = QLabel("SRC name:")
        self.src_input = QLineEdit("urn:ogc:def:crs:EPSG::4326")

        self.name_file_label = QLabel("SRC name:")
        self.name_file_input = QLineEdit("wfs_emision")

        self.max_record_label = QLabel("Max Record")
        self.max_record_input = QLineEdit("1000")

        self.query_button = QPushButton("Query Layer")
        self.query_button.clicked.connect(self.query_layer)

        layout = QVBoxLayout()
        layout.addWidget(self.layer_url_label)
        layout.addWidget(self.layer_url_input)
        layout.addWidget(self.type_name_label)
        layout.addWidget(self.type_name_input)
        layout.addWidget(self.attr_id_label)
        layout.addWidget(self.attr_id_input)
        layout.addWidget(self.xmin_label)
        layout.addWidget(self.xmin_input)
        layout.addWidget(self.ymin_label)
        layout.addWidget(self.ymin_input)
        layout.addWidget(self.xmax_label)
        layout.addWidget(self.xmax_input)
        layout.addWidget(self.ymax_label)
        layout.addWidget(self.ymax_input)
        layout.addWidget(self.src_label)
        layout.addWidget(self.src_input)
        layout.addWidget(self.max_record_label)
        layout.addWidget(self.max_record_input)
        layout.addWidget(self.name_file_label)
        layout.addWidget(self.name_file_input)
        layout.addWidget(self.query_button)

        container = QWidget()
        container.setLayout(layout)
        self.setFixedWidth(600)
        self.setCentralWidget(container)

    def query_layer(self):

        if not self.layer_url_input.text() or not self.name_file_input.text() or not self.src_input.text() \
                or not self.attr_id_input.text() or not self.type_name_input.text():
            QMessageBox.warning(self, "Input Error", "Layer URL, Type Name, Attribute ID, Name File Input "
                                                     "and SRC are required")
            return

        if not is_valid_url(self.layer_url_input.text()):
            QMessageBox.warning(self, "Input Error", "Layer URL is not valid")
            return

        isInt, value_int, messageInt = valid_int(self.max_record_input.text())

        if not isInt:
            QMessageBox.warning(self, "Input Error", messageInt)
            return

        isBBOX, bbox, messageBbox = validate_bbox(self.xmin_input.text(), self.ymin_input.text(),
                                              self.xmax_input.text(), self.ymax_input.text())
        if not isBBOX:
            QMessageBox.warning(self, messageBbox)

        layer_url = self.layer_url_input.text()
        bbox = (bbox[0], bbox[1], bbox[2], bbox[3], self.src_input.text())
        name_file = self.name_file_input.text()
        type_name = self.type_name_input.text()
        attr_id = self.attr_id_input.text()
        max_record = value_int

        self.progress_dialog = QProgressDialog("Querying layer...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.show()

        self.thread = QueryLayerThread(self.controller, type_name=type_name, layer_url=layer_url, bbox=bbox,
                                       name_file=name_file, attr_id=attr_id, max_record=max_record)
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.result_signal.connect(self.query_layer_finished)
        self.thread.start()

    def update_progress(self, value):
        self.progress_dialog.setValue(value)

    def query_layer_finished(self, json_path, excel_path, message=None):
        self.progress_dialog.close()
        if json_path and excel_path:
            QMessageBox.information(self, "Query Completed", f"JSON saved at: {json_path}\n, Exist changes, "
                                                             f"reporting saved at: {excel_path}")
        elif json_path:
            QMessageBox.information(self, "Query Completed", f"JSON saved at: {json_path}")
        elif message:
            QMessageBox.information(self, "Query Failed", f"{message}")
        else:
            QMessageBox.information(self, "Query Failed", "No files were saved.")
