import csv
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsFields,
    QgsField,
    QgsSymbol,
    QgsRendererCategory,
    QgsCategorizedSymbolRenderer
)
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog

path, _ = QFileDialog.getOpenFileName(
    None,
    "Select CSV File",
    "",
    "CSV Files (*.csv);;All Files (*)")
if not path:
    exit()

fields = QgsFields()
fields.append(QgsField("ignited", QVariant.Int))
layer = QgsVectorLayer("Point?crs=EPSG:2959", "Ignited", "memory")
provider = layer.dataProvider()
provider.addAttributes(fields)
layer.updateFields()

with open(path, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    features = []
    for row in reader:
        data = row['data'].split(":")
        if len(data) == 3:
            x = float(data[0])
            y = float(data[1])
            ignited = int(data[2])
            point = QgsPointXY(x, y)
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPointXY(point))
            feature.setAttributes([ignited])
            features.append(feature)
    provider.addFeatures(features)
    layer.updateExtents()

if layer.isValid():
    QgsProject.instance().addMapLayer(layer)
    categories = []
    values = [(1, "red"), (0, "blue")]
    for value, color in values:
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        symbol.setColor(QColor(color))
        category = QgsRendererCategory(value, symbol, str(value))
        categories.append(category)
    renderer = QgsCategorizedSymbolRenderer("ignited", categories)
    layer.setRenderer(renderer)
    layer.triggerRepaint()