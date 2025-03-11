from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QComboBox, QPushButton, QWidget, QDockWidget,
    QFileDialog, QAction
)
from PyQt5.QtCore import Qt
from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsGeometry,
    QgsWkbTypes,
    QgsFeature,
    QgsProcessingFeedback,
    QgsVectorLayerTemporalProperties,
    QgsDataSourceUri,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsMessageLog,
    Qgis,
    QgsTemporalNavigationObject,
)
from qgis.gui import QgsMapToolIdentifyFeature
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand
from qgis.PyQt.QtGui import QColor
import json
import os
import processing
import rasterio
import numpy
import math
import subprocess
import threading
import csv

#########################
# CONSTANTS
#########################

START = (824399, 5237360)
END = (831982, 5248133)
SPARK = (825149, 5243548)
RESOLUTION = 5
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

#########################
# PLUGIN CLASSES
#########################

class WFSPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.dock_widget = None
        self.map_tool = None
        self.rubber_band = None
        self.selected_region = None

    def initGui(self):
        self.action = QAction('Wildfire Simulator', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        if not self.dock_widget:
            self.dock_widget = WFSDockWidget(self)
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dock_widget)
        self.dock_widget.show()

class WFSDockWidget(QDockWidget):
    def __init__(self, plugin):
        super(WFSDockWidget, self).__init__(plugin.iface.mainWindow())
        self.plugin = plugin
        self.setWindowTitle("Wildfire Simulator")
        self.iface = plugin.iface

        self.plugin.rubber_band = QgsRubberBand(self.plugin.iface.mapCanvas(), QgsWkbTypes.PolygonGeometry)
        self.plugin.rubber_band.setColor(QColor(Qt.green))
        self.plugin.rubber_band.setWidth(2)

        self.plugin.fire_origin_rubber_band = QgsRubberBand(self.plugin.iface.mapCanvas(), QgsWkbTypes.PolygonGeometry)
        self.plugin.fire_origin_rubber_band.setColor(QColor(Qt.red))
        self.plugin.fire_origin_rubber_band.setWidth(2)

        # Set up map selection tool and pass the plugin to it.
        self.map_tool = RegionSelectionTool(self.iface, self, self.plugin.rubber_band)
        self.fire_origin_map_tool = RegionSelectionTool(self.iface, self, self.plugin.fire_origin_rubber_band)
        # self.iface.mapCanvas().setMapTool(self.map_tool)

        self.layout = QVBoxLayout()

        # --- Slope layer dropdown ---
        self.slope_label = QLabel("Select Slope Layer:")
        self.layout.addWidget(self.slope_label)
        self.slope_selector = QComboBox()
        self.populate_raster_layers(self.slope_selector)
        self.layout.addWidget(self.slope_selector)

        # --- Aspect layer dropdown ---
        self.aspect_label = QLabel("Select Aspect Layer:")
        self.layout.addWidget(self.aspect_label)
        self.aspect_selector = QComboBox()
        self.populate_raster_layers(self.aspect_selector)
        self.layout.addWidget(self.aspect_selector)

        # --- Landcover layer dropdown ---
        self.landcover_label = QLabel("Select Landcover Layer:")
        self.layout.addWidget(self.landcover_label)
        self.landcover_selector = QComboBox()
        self.populate_raster_layers(self.landcover_selector)
        self.layout.addWidget(self.landcover_selector)

        # --- Buttons ---
        self.select_button = QPushButton("Select Simulation Area")
        self.select_button.clicked.connect(self.activate_selection)
        self.layout.addWidget(self.select_button)

        self.fire_origin_button = QPushButton("Select Fire Origin Area")
        self.fire_origin_button.clicked.connect(self.activate_fire_origin_selection)
        self.layout.addWidget(self.fire_origin_button)

        self.clear_button = QPushButton("Clear Selected Area")
        self.clear_button.clicked.connect(self.clear_selection)
        self.layout.addWidget(self.clear_button)

        self.convert_button = QPushButton("Convert to JSON")
        self.convert_button.clicked.connect(self.convert_to_json)
        self.layout.addWidget(self.convert_button)

        self.cadmium_button = QPushButton("Run cadmium")
        self.cadmium_button.clicked.connect(self.run_cadmium)
        self.layout.addWidget(self.cadmium_button)

        self.cancel_cadmium_button = QPushButton("Cancel cadmium")
        self.cancel_cadmium_button.clicked.connect(self.end_cadmium_run)
        self.layout.addWidget(self.cancel_cadmium_button)
        self.cancel_cadmium_button.hide()

        self.cadmium_proc = None

        container = QWidget()
        container.setLayout(self.layout)
        self.setWidget(container)

    def populate_raster_layers(self, selector):
        """Populate the dropdown with GeoTIFF (raster) layers."""
        selector.clear()
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            if isinstance(layer, QgsRasterLayer):
                ds = layer.dataProvider().dataSourceUri().lower()
                if ds.endswith('.tif') or ds.endswith('.tiff'):
                    selector.addItem(layer.name(), layer)

    def activate_selection(self):
        """Activate the polygon selection tool."""
        self.plugin.iface.mapCanvas().setMapTool(self.map_tool)

    def activate_fire_origin_selection(self):
        self.plugin.iface.mapCanvas().setMapTool(self.fire_origin_map_tool)

    def clear_selection(self):
        """Clear the current selection and rubber band."""
        if self.plugin.rubber_band:
            self.plugin.selected_region = None
            self.plugin.rubber_band.reset()
            self.plugin.rubber_band = None
            self.plugin.iface.mapCanvas().refresh()
        if self.plugin.fire_origin_rubber_band:
            self.plugin.selected_region = None
            self.plugin.fire_origin_rubber_band.reset()
            self.plugin.fire_origin_rubber_band = None
            self.plugin.iface.mapCanvas().refresh()
        self.map_tool.points = []
        self.fire_origin_map_tool.points = []
        self.plugin.iface.mapCanvas().setMapTool(None)
        print("Selection cleared!")

    def convert_to_json(self):
        """Clip the selected GeoTIFFs to the drawn area, process them, and output JSON."""

        slope_layer = self.slope_selector.currentData()
        aspect_layer = self.aspect_selector.currentData()
        landcover_layer = self.landcover_selector.currentData()

<<<<<<< HEAD:scripts/MapLoader/MapLoader.py
        if slope_layer and aspect_layer and landcover_layer and self.plugin.selected_region and self.plugin.selected_region.isGeosValid():
            json_file_path, _ = QFileDialog.getSaveFileName(self, "Save JSON File", "", "JSON Files (*.json);;All Files (*)")
            if not json_file_path:
                print("No JSON file path provided.")
                return
            
            # Create an in-memory mask layer from the drawn polygon
            mask_layer = createTemporaryPolygonLayer(self.plugin.selected_region)
            
            # Determine output file paths for the clipped rasters
            clipped_aspect_path = os.path.splitext(json_file_path)[0] + "_aspect.tif"
            clipped_slope_path = os.path.splitext(json_file_path)[0] + "_slope.tif"
            clipped_land_path = os.path.splitext(json_file_path)[0] + "_landcover.tif"
=======
        if not slope_layer or not aspect_layer or not landcover_layer or not self.plugin.selected_region or not self.plugin.selected_region.isGeosValid():
            raise Exception("No valid layers or selected region. Cannot convert to JSON.")
        
        # Create an in-memory mask layer from the drawn polygon
        mask_layer = createTemporaryPolygonLayer(self.plugin.selected_region)
        # Determine output file paths for the clipped rasters
        json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "map.json")
        clipped_aspect_path = os.path.splitext(json_file_path)[0] + "_aspect.tif"
        clipped_slope_path = os.path.splitext(json_file_path)[0] + "_slope.tif"
        clipped_land_path = os.path.splitext(json_file_path)[0] + "_landcover.tif"
>>>>>>> 7d2eee017fc5091fd2ce4debed4a91e79d399fd6:advanced/plugin/plugin.py

        # Use the GDAL Clip algorithm to clip the rasters using the mask
        params_aspect = {
            "INPUT": aspect_layer.source(),
            "MASK": mask_layer,
            "CROP_TO_CUTLINE": True,
            "OUTPUT": clipped_aspect_path
        }
        params_slope = {
            "INPUT": slope_layer.source(),
            "MASK": mask_layer,
            "CROP_TO_CUTLINE": True,
            "OUTPUT": clipped_slope_path
        }
        params_land = {
            "INPUT": landcover_layer.source(),
            "MASK": mask_layer,
            "CROP_TO_CUTLINE": True,
            "OUTPUT": clipped_land_path
        }

        processing.run("gdal:cliprasterbymasklayer", params_aspect)
        processing.run("gdal:cliprasterbymasklayer", params_slope)
        processing.run("gdal:cliprasterbymasklayer", params_land)

        # Prepare paths for further processing:
        paths = {
            "aspect": clipped_aspect_path,
            "slope": clipped_slope_path,
            "land": clipped_land_path,
            "json": json_file_path,
        }

<<<<<<< HEAD:scripts/MapLoader/MapLoader.py
            # Resample and align the landcover raster to match the slope and aspect rasters
            with rasterio.open(paths["slope"]) as slope_src:
                slope_transform = slope_src.transform
                slope_crs = slope_src.crs
                slope_width = slope_src.width
                slope_height = slope_src.height

            with rasterio.open(paths["land"]) as land_src:
                land_data = land_src.read(1)
                land_transform = land_src.transform
                land_crs = land_src.crs

                # Resample landcover to match slope raster
                resampled_land_data = numpy.empty((slope_height, slope_width), dtype=numpy.float32)
                rasterio._warp._reproject(
                    source=land_data,
                    destination=resampled_land_data,
                    src_transform=land_transform,
                    src_crs=land_crs,
                    dst_transform=slope_transform,
                    dst_crs=slope_crs,
                    resampling=rasterio._warp.Resampling.nearest
                )

                # Save the resampled landcover raster
                resampled_land_path = os.path.splitext(json_file_path)[0] + "_landcover_resampled.tif"
                with rasterio.open(resampled_land_path, 'w', driver='GTiff', height=slope_height, width=slope_width,
                                count=1, dtype=resampled_land_data.dtype, crs=slope_crs, transform=slope_transform) as dst:
                    dst.write(resampled_land_data, 1)

                paths["land"] = resampled_land_path

            # # Process the clipped and resampled rasters and generate JSON
            # maps = {
            #     "slope": get_raw_maps(paths["slope"]),
            #     "aspect": get_raw_maps(paths["aspect"]),
            #     "land": get_raw_maps(paths["land"])
            # }
            # width = min(maps["slope"].width, maps["aspect"].width, maps["land"].width)
            # height = min(maps["slope"].height, maps["aspect"].height, maps["land"].height)

            dump_json(paths)
            print("JSON conversion completed.")
        else:
            print("No valid layers or selected region. Cannot convert to JSON.")
=======
        # # Run processing to generate slope and aspect rasters from the clipped elevation
        # feedback = QgsProcessingFeedback()
        # try:
        #     processing.run("qgis:slope", {
        #         "INPUT": paths["elevation"],
        #         "Z_FACTOR": 1.0,
        #         "OUTPUT": paths["slope"]
        #     }, feedback=feedback)
        #     processing.run("qgis:aspect", {
        #         "INPUT": paths["elevation"],
        #         "Z_FACTOR": 1.0,
        #         "OUTPUT": paths["aspect"]
        #     }, feedback=feedback)
        # except Exception as e:
        #     print(f"Error generating slope or aspect: {e}")
        #     return

        maps = {
            "slope": get_raw_maps(paths["slope"]),
            "aspect": get_raw_maps(paths["aspect"]),
            "land": get_raw_maps(paths["land"])
        }

        width = min(maps["slope"].width, maps["aspect"].width, maps["land"].width)
        height = min(maps["slope"].height, maps["aspect"].height, maps["land"].height)
        dump_json(maps, paths, width, height)
        print("JSON conversion completed.")

    def on_cadmium_finish_running(self, csv_path):
        uri = f"file:///{csv_path}?delimiter=,&xField=x&yField=y&crs=EPSG:2959"
        layer = QgsVectorLayer(uri, "ignition", "delimitedtext")
        if not layer.isValid():
            print("Failed to load layer!")
            return
        QgsProject.instance().addMapLayer(layer)
        props = layer.temporalProperties()
        props.setIsActive(True)
        props.setAccumulateFeatures(True)
        props.setMode(QgsVectorLayerTemporalProperties.TemporalMode.ModeFeatureDateTimeInstantFromField)
        props.setStartField("time")

    def run_cadmium(self):
        if self.cadmium_proc:
            return
        root = os.path.dirname(os.path.abspath(__file__))
        capstone = os.path.join(root, "capstone.exe")
        map_json = os.path.join(root, "map.json")
        map_csv = os.path.join(root, "ignition.csv")
        def callback():
            self.cadmium_proc = subprocess.Popen([capstone, map_json, map_csv])
            self.cancel_cadmium_button.show()
            self.cadmium_proc.wait()
            self.end_cadmium_run()
            self.on_cadmium_finish_running(map_csv)
            return
        self.cadmium_button.hide()
        thread = threading.Thread(target=callback)
        thread.start()
    
    def end_cadmium_run(self):
        if not self.cadmium_proc:
            return
        self.cancel_cadmium_button.hide()
        self.cadmium_proc.kill()
        self.cadmium_button.show()
        self.cadmium_proc = None
>>>>>>> 7d2eee017fc5091fd2ce4debed4a91e79d399fd6:advanced/plugin/plugin.py

class RegionSelectionTool(QgsMapToolEmitPoint):
    def __init__(self, iface, plugin, rubber_band):
        super(RegionSelectionTool, self).__init__(iface.mapCanvas())
        self.points = []  # List to store clicked QgsPointXY objects
        self.plugin = plugin
        self.rubber_band = rubber_band

    def canvasPressEvent(self, event):
        point = self.toMapCoordinates(event.pos())
        
        if len(self.points) > 2 and self.is_near_first_point(point):
            self.points.append(self.points[0])  # Automatically close the polygon
            self.plugin.selected_region = QgsGeometry.fromPolygonXY([self.points])
            self.highlight_region()
            return

        # Add the new point to the list
        self.points.append(point)
        self.plugin.selected_region = QgsGeometry.fromPolygonXY([self.points])
        self.highlight_region()

    def is_near_first_point(self, point, tolerance=50):
        """Check if the current point is near the first point (within a certain tolerance)."""
        first_point = self.points[0]
        dist = math.sqrt((first_point.x() - point.x())**2 + (first_point.y() - point.y())**2)
        return dist <= tolerance

    def highlight_region(self):
        if self.plugin.selected_region:
            self.rubber_band.reset()
            for p in self.points:
                self.rubber_band.addPoint(p)

    def clear_highlight(self):
        self.plugin.reset()
        self.plugin.iface.mapCanvas().refresh()

#########################
# HELPER FUNCTIONS
#########################

def createTemporaryPolygonLayer(geometry):
    """
    Creates an in-memory vector layer (Polygon) with the given geometry.
    This layer will be used as a mask for clipping.
    """
    crs = QgsProject.instance().crs().authid()
    mem_layer = QgsVectorLayer(f"Polygon?crs={crs}", "mask", "memory")
    prov = mem_layer.dataProvider()
    feat = QgsFeature()
    feat.setGeometry(geometry)
    prov.addFeatures([feat])
    mem_layer.updateExtents()
    return mem_layer

def read_raster(path):
    """Read a raster file and return its data and metadata."""
    with rasterio.open(path) as src:
        data = src.read(1)  # Read the first band
        transform = src.transform
        crs = src.crs
        return data, transform, crs

def dump_json(paths):
    """Read raster data and populate the JSON file."""
    # Read raster data
    slope_data, slope_transform, _ = read_raster(paths['slope'])
    aspect_data, _, _ = read_raster(paths['aspect'])
    landcover_data, _, _ = read_raster(paths['land'])

    # Get dimensions
    height, width = slope_data.shape

    # Initialize JSON structure
    data = {
        "cells": {
            "default": {
                "delay": "inertial"
            }
        }
    }

    # Iterate over each cell
    for row in range(height):
        for col in range(width):
            # Get values from rasters
            slope_value = slope_data[row][col]
            aspect_value = aspect_data[row][col]
            landcover_value = landcover_data[row][col]

            # Skip invalid values
            if slope_value <= -9999.0 or aspect_value <= -9999.0:
                continue

            # Map landcover value to fuel model
            try:
                fuel = FUELS[int(landcover_value)]
            except KeyError:
                continue

            # Get cell coordinates
            x, y = slope_transform * (col, row)
            cell_name = f"{int(x)}_{int(y)}"

            # Add cell to JSON
            data["cells"][cell_name] = {
                "neighborhood": {},
                "state": {
                    "slope": float(slope_value),
                    "aspect": float(aspect_value),
                    "fuelModelNumber": fuel,
                    "windDirection": WIND_DIRECTION,
                    "windSpeed": WIND_SPEED,
                    "x": float(x),
                    "y": float(y),
                    "ignited": False
                }
            }

            # Define neighborhood (simple example: 4-connected neighbors)
            neighborhood = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for neighbor in neighborhood:
                c = col + neighbor[0]
                r = row + neighbor[1]

                # Skip out-of-bounds neighbors
                if c < 0 or r < 0 or c >= width or r >= height:
                    continue

                # Get neighbor coordinates
                neighbor_x, neighbor_y = slope_transform * (c, r)
                neighbor_name = f"{int(neighbor_x)}_{int(neighbor_y)}"

                # Add neighbor to neighborhood
                data["cells"][cell_name]["neighborhood"][neighbor_name] = RESOLUTION

    # Write JSON to file
    with open(paths['json'], "w") as f:
        json.dump(data, f, indent=4)
    print(f"JSON file saved to: {paths['json']}")
