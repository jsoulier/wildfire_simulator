from PyQt5.QtWidgets import QFileDialog
from qgis.core import QgsProcessingFeedback
import json
import processing
import rasterio

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

def to_list(path, start, end, resolution):
    with rasterio.open(path) as src:
        if src.crs.to_string() != "EPSG:2959":
            raise ValueError("Raster CRS does not match EPSG:2959")
        data = src.read(1)
        transform = src.transform
        x1, y1 = start
        x2, y2 = end
        points = []
        width = 0
        for y in range(y1, y2, resolution):
            points.append([])
            for x in range(x1, x2, resolution):
                row, col = rasterio.transform.rowcol(transform, x, y)
                try:
                    value = data[row, col]
                    points[-1].append(Point(x, y, value.item()))
                except:
                    pass
            width = max(width, len(points[-1]))
        return points, width, len(points)

start = (480000, 5090000)
end = (490000, 5100000)
resolution = 100
slopes, slopes_width, slopes_height = to_list(slope_path, start, end, resolution)
aspects, aspects_width, aspects_height = to_list(aspect_path, start, end, resolution)

with open(json_path, 'w') as f:
    data = {}
    data["cells"] = {}
    data["cells"]["default"] = {}
    data["cells"]["default"]["delay"] = "inertial"
    data["cells"]["default"]["config"] = {}
    data["cells"]["default"]["config"]["slope"] = 20
    data["cells"]["default"]["config"]["aspect"] = 90.0
    data["cells"]["default"]["config"]["fuelModelNumber"] = 1
    data["cells"]["default"]["config"]["windDirection"] = 90.0
    data["cells"]["default"]["config"]["windSpeed"] = 10
    for row in range(slopes_height):
        for col in range(slopes_width):
            try:
                slope = slopes[row][col]
                aspect = aspects[row][col]
            except:
                continue
            if slope.value <= -9999.0:
                continue
            name = "{}_{}".format(int(slope.x), int(slope.y))
            data["cells"][name] = {}
            data["cells"][name]["neighborhood"] = {}
            for neighbor in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                c = col + neighbor[0]
                r = row + neighbor[1]
                if not (
                    r >= 0 and
                    c >= 0 and
                    r < slopes_height and
                    c < slopes_width and
                    slopes[r][c].value > -9999.0):
                    continue
                s = slopes[r][c]
                data["cells"][name]["neighborhood"]["{}_{}".format(s.x, s.y)] = resolution
            data["cells"][name]["config"] = {}
            data["cells"][name]["config"]["slope"] = slope.value
            data["cells"][name]["config"]["aspect"] = aspect.value
            data["cells"][name]["config"]["fuelModelNumber"] = 1
            data["cells"][name]["config"]["windDirection"] = 90.0
            data["cells"][name]["config"]["windSpeed"] = 10
            data["cells"][name]["state"] = {}
            data["cells"][name]["state"]["x"] = int(slope.x)
            data["cells"][name]["state"]["y"] = int(slope.y)
            data["cells"][name]["state"]["ignited"] = False

    # TODO:
    data["cells"]['480400_5091100']["state"]["ignited"] = True

    json.dump(data, f, indent=4)