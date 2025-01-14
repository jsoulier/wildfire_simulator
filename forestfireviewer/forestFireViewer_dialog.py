import csv
from qgis.PyQt import uic, QtWidgets
from qgis.PyQt.QtWidgets import QFileDialog, QSlider, QLabel
from PyQt5.QtCore import Qt
from qgis.core import QgsMessageLog
import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'forestFireViewer_dialog_base.ui'))

class forestFireViewerDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(forestFireViewerDialog, self).__init__(parent)
        self.setupUi(self)
        self.data = []
        self.file_button.clicked.connect(self.open_file_dialog)
        self.slider.valueChanged.connect(self.update_ignitions)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if file_path:
            try:
                self.load_csv(file_path)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load CSV file: {str(e)}")

    def load_csv(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            self.data = []
            for row in reader:
                self.data.append(row)
        time_points = [int(float(row['time'])) for row in self.data]
        self.slider.setMinimum(min(time_points))
        self.slider.setMaximum(max(time_points))
        QgsMessageLog.logMessage('Min: {}'.format(min(time_points)))
        QgsMessageLog.logMessage('Max: {}'.format(max(time_points)))
        self.slider.setTickInterval(1)
        self.update_ignitions()

    def update_ignitions(self):
        if not self.data:
            return
        selected_time = self.slider.value()
        grid_size = (15, 15)
        grid = [[None for _ in range(grid_size[1])] for _ in range(grid_size[0])]
        for row in self.data:
            time = int(float(row['time']))
            if time > selected_time:
                break
            model_name = row['model_name']
            model_name = model_name.strip('()').split(',') 
            x, y = int(model_name[0]), int(model_name[1])
            ignited = row['data']
            if ignited == 1:
                cell = QLabel("🔥")
                cell.setStyleSheet("font-size: 20px; color: red;")
                QgsMessageLog.logMessage('This is an error message')
            else:
                cell = QLabel("⚪")
                cell.setStyleSheet("font-size: 20px; color: gray;")
                QgsMessageLog.logMessage('This is also an error message')
            grid[x][y] = cell
        self.update_grid_layout(grid)

    def update_grid_layout(self, grid):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                cell = grid[row][col]
                if cell:
                    self.grid_layout.addWidget(cell, row, col)