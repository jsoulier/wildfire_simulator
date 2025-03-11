from qgis.core import QgsProcessingFeedback
from PyQt5.QtWidgets import QFileDialog
import json
import processing
import rasterio
import numpy

START = (824399, 5237360)
END = (831982, 5248133)
SPARK = (825149, 5243548)
RESOLUTION = 50
WIND_SPEED = 30
WIND_DIRECTION = 90
FUELS = {
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

class Point:
    def __init__(self, x, y, value, shifted):
        self.x = x
        self.y = y
        self.value = value
        self.shifted = shifted

class Map:
    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height

def get_paths():
    paths = {}
    paths["elevation"], _ = QFileDialog.getOpenFileName(
        None,
        "Select Elevation File",
        "",
        "GeoTIFF Files (*.tif);;All Files (*)")
    if not paths["elevation"]:
        return False
    paths["land"], _ = QFileDialog.getOpenFileName(
        None,
        "Select Land File",
        "",
        "GeoTIFF Files (*.tif);;All Files (*)")
    if not paths["land"]:
        return False
    paths["json"], _ = QFileDialog.getSaveFileName(
        None,
        "Save JSON File",
        "",
        "JSON Files (*.json);;All Files (*)")
    if not paths["json"]:
        return False
    paths["slope"] = paths["elevation"].replace(".tif", ".slope.tif")
    paths["aspect"] = paths["elevation"].replace(".tif", ".aspect.tif")
    return paths

def convert_maps(paths):
    feedback = QgsProcessingFeedback()
    processing.run("qgis:slope", {
        "INPUT": paths["elevation"],
        "Z_FACTOR": 1.0,
        "OUTPUT": paths["slope"]
    }, feedback=feedback)
    processing.run("qgis:aspect", {
        "INPUT": paths["elevation"],
        "Z_FACTOR": 1.0,
        "OUTPUT": paths["aspect"]
    }, feedback=feedback)

def get_raw_maps(path):
    with rasterio.open(path) as src:
        crs = src.crs.to_string()
        if crs != "EPSG:2959":
            transform, width, height = rasterio._warp._calculate_default_transform(
                src.crs, "EPSG:2959", src.width, src.height, *src.bounds)
            data = numpy.empty((height, width), dtype=numpy.float32)
            rasterio._warp._reproject(
                source=src.read(1),
                destination=data,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs="EPSG:2959",
                resampling=rasterio._warp.Resampling.nearest)
        else:
            data = src.read(1)
            transform = src.transform
        x1, y1 = START
        x2, y2 = END
        points = []
        width = 0
        shift = 0
        y_resolution = int(RESOLUTION / 2 * 1.1547)
        x_resolution = int(RESOLUTION * 2)
        for y in range(y1, y2, y_resolution):
            points.append([])
            for x in range(x1, x2, x_resolution):
                shifted = False
                if shift % 2:
                    x += int(x_resolution / 2)
                    shifted = True
                row, col = rasterio.transform.rowcol(transform, x, y)
                try:
                    value = data[row, col]
                    points[-1].append(Point(x, y, value.item(), shifted))
                except:
                    pass
            width = max(width, len(points[-1]))
            shift += 1
        return Map(points, width, len(points))

def dump_json(maps, paths, width, height):
    def get_name(point):
        return "{}_{}".format(point.x, point.y)
    with open(paths["json"], "w") as f:
        data = {}
        data["cells"] = {}
        data["cells"]["default"] = {}
        data["cells"]["default"]["delay"] = "inertial"
        for row in range(height):
            for col in range(width):
                try:
                    slope = maps["slope"].data[row][col]
                    aspect = maps["aspect"].data[row][col]
                    land = maps["land"].data[row][col]
                except Exception as e:
                    continue
                if slope.value <= -9999.0:
                    continue
                if aspect.value <= -9999.0:
                    continue
                try:
                    fuel = FUELS[int(land.value)]
                except:
                    continue
                name = get_name(slope)
                data["cells"][name] = {}
                data["cells"][name]["neighborhood"] = {}
                neighborhood = []
                if not slope.shifted:
                    neighborhood = [(0, -2), (0, -1), (0, 1), (0, 2), (-1, -1), (-1, 1)]
                else:
                    neighborhood = [(0, -2), (0, -1), (0, 1), (0, 2), (1, -1), (1, 1)]
                for neighbor in neighborhood:
                    c = col + neighbor[0]
                    r = row + neighbor[1]
                    if c < 0 or r < 0 or c >= width or r >= height:
                        continue
                    try:
                        s = maps["slope"].data[r][c]
                        if s.value <= -9999.0:
                            continue
                        a = maps["aspect"].data[r][c]
                        if a.value <= -9999.0:
                            continue
                        FUELS[int(maps["land"].data[r][c].value)]
                    except:
                        continue
                    data["cells"][name]["neighborhood"][get_name(s)] = RESOLUTION
                data["cells"][name]["state"] = {}
                data["cells"][name]["state"]["slope"] = slope.value
                data["cells"][name]["state"]["aspect"] = aspect.value
                data["cells"][name]["state"]["fuelModelNumber"] = fuel
                data["cells"][name]["state"]["windDirection"] = WIND_DIRECTION
                data["cells"][name]["state"]["windSpeed"] = WIND_SPEED
                data["cells"][name]["state"]["x"] = int(slope.x)
                data["cells"][name]["state"]["y"] = int(slope.y)
                data["cells"][name]["state"]["ignited"] = False
        try:
            data["cells"][get_name(Point(SPARK[0], SPARK[1], 0, False))]["state"]["ignited"] = True
        except:
            print("Invalid spark location: {}".format(SPARK))
        json.dump(data, f, indent=4)

def main():
    paths = get_paths()
    if not paths:
        return
    convert_maps(paths)
    maps = {}
    maps["slope"] = get_raw_maps(paths["slope"])
    maps["aspect"] = get_raw_maps(paths["aspect"])
    maps["land"] = get_raw_maps(paths["land"])
    width = min(min(maps["slope"].width, maps["aspect"].width), maps["land"].width)
    height = min(min(maps["slope"].height, maps["aspect"].height), maps["land"].height)
    dump_json(maps, paths, width, height)

main()