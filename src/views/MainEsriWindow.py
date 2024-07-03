from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QProgressDialog, \
    QMessageBox
from arcgis.geometry import Envelope
from PyQt5.QtCore import Qt

from src.utils.Utils import is_valid_url, validate_bbox
from src.views.QueryThreadLayer import QueryLayerThread


class MainEsriWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.setWindowTitle("ExtractPyGeoServices")

        self.layer_url_label = QLabel("Layer URL:")
        self.layer_url_input = QLineEdit("https://serviciosgis.ign.es/servicios/rest/services/Signa/Servicios_Industria/MapServer/23")

        self.where_label = QLabel("Where Clause:")
        self.where_input = QLineEdit("1=1")

        self.out_fields_label = QLabel("Out Fields:")
        self.out_fields_input = QLineEdit("*")

        self.return_geometry_label = QLabel("Return Geometry:")
        self.return_geometry_input = QLineEdit("True")

        self.attr_id_label = QLabel("Atrribute ID")
        self.attr_id_input = QLineEdit("objectid")

        self.xmin_label = QLabel("XMin:")
        self.xmin_input = QLineEdit("-20.654297")

        self.ymin_label = QLabel("YMin:")
        self.ymin_input = QLineEdit("33.868169")

        self.xmax_label = QLabel("XMax:")
        self.xmax_input = QLineEdit("12.722168")

        self.ymax_label = QLabel("YMax:")
        self.ymax_input = QLineEdit("45.566015")

        self.name_file_label = QLabel("File output name")
        self.name_file_input = QLineEdit("esri_layer_query")

        self.query_button = QPushButton("Query Layer")
        self.query_button.clicked.connect(self.query_layer)

        layout = QVBoxLayout()
        layout.addWidget(self.layer_url_label)
        layout.addWidget(self.layer_url_input)
        layout.addWidget(self.attr_id_label)
        layout.addWidget(self.attr_id_input)
        layout.addWidget(self.where_label)
        layout.addWidget(self.where_input)
        layout.addWidget(self.out_fields_label)
        layout.addWidget(self.out_fields_input)
        layout.addWidget(self.return_geometry_label)
        layout.addWidget(self.return_geometry_input)
        layout.addWidget(self.xmin_label)
        layout.addWidget(self.xmin_input)
        layout.addWidget(self.ymin_label)
        layout.addWidget(self.ymin_input)
        layout.addWidget(self.xmax_label)
        layout.addWidget(self.xmax_input)
        layout.addWidget(self.ymax_label)
        layout.addWidget(self.ymax_input)
        layout.addWidget(self.name_file_label)
        layout.addWidget(self.name_file_input)
        layout.addWidget(self.query_button)

        container = QWidget()
        container.setLayout(layout)
        self.setFixedWidth(600)
        self.setCentralWidget(container)

    def query_layer(self):

        if not self.layer_url_input.text() or not self.name_file_input.text() or not self.attr_id_input.text():
            QMessageBox.warning(self, "Input Error", "Layer URL, Name File Input and Attribute ID are required")
            return

        if not is_valid_url(self.layer_url_input.text()):
            QMessageBox.warning(self, "Input Error", "Layer URL is not valid")
            return

        isBBOX, bbox, message = validate_bbox(self.xmin_input.text(), self.ymin_input.text(),
                                              self.xmax_input.text(), self.ymax_input.text())
        if not isBBOX:
            QMessageBox.warning(self, message)

        layer_url = self.layer_url_input.text()
        where_clause = self.where_input.text()
        attr_id = self.attr_id_input.text()
        out_fields = self.out_fields_input.text()
        return_geometry = self.return_geometry_input.text().lower() == 'true'
        name_file_out = self.name_file_input.text()
        geometry = None
        if bbox:
            geometry = Envelope({
                "xmin": bbox[0],
                "ymin": bbox[1],
                "xmax": bbox[2],
                "ymax": bbox[3],
                "spatialReference": {"wkid": 4326}
            })

        self.progress_dialog = QProgressDialog("Querying layer...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.show()

        self.thread = QueryLayerThread(self.controller, layer_url=layer_url, attr_id=attr_id,
                                       where_clause=where_clause, out_fields=out_fields,
                                       return_geometry=return_geometry, geometry=geometry,
                                       name_file_out=name_file_out)
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
