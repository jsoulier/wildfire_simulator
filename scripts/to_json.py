from PyQt5.QtWidgets import QFileDialog
from qgis.core import QgsProcessingFeedback
import json
import processing
import rasterio
import numpy

FUEL_MODELS = {
    1: 10,   # temperate or sub-polar needleleaf forest -> FM10
    2: 13,   # sub-polar taiga -> FM13
    5: 9,    # temperate or sub-polar broadleaf deciduous forest -> FM9
    6: 8,    # forest foliage temperate or sub-polar -> FM8
    8: 141,  # temperate or sub-polar shrubland -> SH1
    10: 101, # temperate or sub-polar grassland -> GR1
    11: 93,  # sub-polar or polar shrubland-lichen-moss -> NB3
    12: 103, # sub-polar or polar grassland-lichen-moss -> GR3
    13: 99,  # sub-polar or polar barren-lichen-moss -> NB9
    14: 94,  # wetland -> NB4
    15: 93,  # cropland -> NB3
    16: 99,  # barren lands -> NB9
    17: 91,  # urban -> NB1
    18: 98,  # water -> NB8
    19: 92,  # snow and ice -> NB2
}

elevation_path, _ = QFileDialog.getOpenFileName(
    None,
    "Select Elevation File",
    "",
    "GeoTIFF Files (*.tif);;All Files (*)")
if not elevation_path:
    exit()
land_path, _ = QFileDialog.getOpenFileName(
    None,
    "Select Land File",
    "",
    "GeoTIFF Files (*.tif);;All Files (*)")
if not land_path:
    exit()
feedback = QgsProcessingFeedback()
slope_path = elevation_path.replace('.tif', '_slope.tif')
aspect_path = elevation_path.replace('.tif', '_aspect.tif')
processing.run("qgis:slope", {
    "INPUT": elevation_path,
    "Z_FACTOR": 1.0,
    "OUTPUT": slope_path
}, feedback=feedback)
processing.run("qgis:aspect", {
    "INPUT": elevation_path,
    "Z_FACTOR": 1.0,
    "OUTPUT": aspect_path
}, feedback=feedback)

class Point:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

def to_list(path, start, end, resolution):
    with rasterio.open(path) as src:
        crs = src.crs.to_string()
        if crs != "EPSG:2959":
            transform, width, height = rasterio._warp._calculate_default_transform(
                src.crs, "EPSG:2959", src.width, src.height, *src.bounds)
            reprojected_data = numpy.empty((height, width), dtype=numpy.float32)
            rasterio._warp._reproject(
                source=src.read(1),
                destination=reprojected_data,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs="EPSG:2959",
                resampling=rasterio._warp.Resampling.nearest)
            transform = transform
            data = reprojected_data
        else:
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

start = (420000, 5109980)
end = (422552, 5119989)
resolution = 100
slopes, slopes_width, slopes_height = to_list(slope_path, start, end, resolution)
aspects, aspects_width, aspects_height = to_list(aspect_path, start, end, resolution)
land, land_width, land_height = to_list(land_path, start, end, resolution)
width = min(min(slopes_width, aspects_width), land_width)
height = min(min(slopes_height, aspects_height), land_height)

json_path, _ = QFileDialog.getSaveFileName(
    None,
    "Save JSON File",
    "",
    "JSON Files (*.json);;All Files (*)")
if not json_path:
    exit()
with open(json_path, "w") as f:
    data = {}
    data["cells"] = {}
    data["cells"]["default"] = {}
    data["cells"]["default"]["delay"] = "inertial"
    for row in range(height):
        for col in range(width):
            try:
                slope = slopes[row][col]
                aspect = aspects[row][col]
                fuel = land[row][col]
            except:
                continue
            if slope.value <= -9999.0:
                continue
            fuel = FUEL_MODELS[int(fuel.value)]
            name = "{}_{}".format(int(slope.x), int(slope.y))
            data["cells"][name] = {}
            data["cells"][name]["neighborhood"] = {}
            for neighbor in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                c = col + neighbor[0]
                r = row + neighbor[1]
                if c < 0 or r < 0 or c >= width or r >= height:
                    continue
                try:
                    if slopes[r][c].value <= -9999.0:
                        continue
                    aspects[r][c]
                    land[r][c]
                except:
                    continue
                s = slopes[r][c]
                data["cells"][name]["neighborhood"]["{}_{}".format(s.x, s.y)] = resolution
            data["cells"][name]["state"] = {}
            data["cells"][name]["state"]["slope"] = slope.value
            data["cells"][name]["state"]["aspect"] = aspect.value
            data["cells"][name]["state"]["fuelModelNumber"] = fuel
            data["cells"][name]["state"]["windDirection"] = 90.0
            data["cells"][name]["state"]["windSpeed"] = 10
            data["cells"][name]["state"]["x"] = int(slope.x)
            data["cells"][name]["state"]["y"] = int(slope.y)
            data["cells"][name]["state"]["ignited"] = False

    # TODO:
    data["cells"]["420100_5110080"]["state"]["ignited"] = True

    json.dump(data, f, indent=4)