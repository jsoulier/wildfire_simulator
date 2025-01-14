from PyQt5.QtWidgets import QFileDialog
from qgis.core import (
    QgsProcessingFeedback,
    QgsRasterLayer,
    QgsRasterDataProvider
)
import processing
import numpy as np
import rasterio
import json

RESOLUTION = 1000

path, _ = QFileDialog.getOpenFileName(
    None,
    "Select GeoTIFF File",
    "",
    "GeoTIFF Files (*.tif);;All Files (*)")
if not path:
    exit()
feedback = QgsProcessingFeedback()
slope_path = path.replace('.tif', '_slope.tif')
aspect_path = path.replace('.tif', '_aspect.tif')
json_path = path.replace('.tif', '.json')
processing.run("qgis:slope", {
    'INPUT': path,
    'Z_FACTOR': 1.0,
    'OUTPUT': slope_path
}, feedback=feedback)
processing.run("qgis:aspect", {
    'INPUT': path,
    'Z_FACTOR': 1.0,
    'OUTPUT': aspect_path
}, feedback=feedback)

class Point:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

def to_list(path):
    with rasterio.open(path) as src:
        width = src.width
        height = src.height
        transform = src.transform
        data = src.read(1)
        points = []
        i = 0
        for row in range(0, height, RESOLUTION):
            points.append([])
            for col in range(0, width, RESOLUTION):
                x, y = transform * (col, row)
                value = data[row, col]
                points[i].append(Point(x, y, value.item()))
            i += 1
        return points

slopes = to_list(slope_path)
aspects = to_list(aspect_path)

with open(json_path, 'w') as f:
    width = len(slopes[0])
    height = len(slopes)
    data = {}
    data['scenario'] = {}
    data['scenario']['shape'] = [width, height]
    data['scenario']['origin'] = [0, 0]
    data["cells"] = {}
    data["cells"]["default"] = {}
    data["cells"]["default"]["delay"] = "inertial"
    data["cells"]["default"]["state"] = {}
    data["cells"]["default"]["state"]["ignited"] = False
    data["cells"]["default"]["config"] = {}
    data["cells"]["default"]["config"]["slope"] = 20
    data["cells"]["default"]["config"]["aspect"] = 90.0
    data["cells"]["default"]["config"]["fuelModelNumber"] = 1
    data["cells"]["default"]["config"]["windDirection"] = 90.0
    data["cells"]["default"]["config"]["windSpeed"] = 10
    for row in range(height):
        for col in range(width):
            slope = slopes[row][col]
            aspect = aspects[row][col]
            name = "c{}_{}".format(int(slope.x), int(slope.y))
            data["cells"][name] = {}
            data["cells"][name]["config"] = {}
            data["cells"][name]["config"]["slope"] = slope.value
            data["cells"][name]["config"]["aspect"] = aspect.value
            data["cells"][name]["config"]["fuelModelNumber"] = 1
            data["cells"][name]["config"]["windDirection"] = 90.0
            data["cells"][name]["config"]["windSpeed"] = 10
    json.dump(data, f, indent=4)