# Wildfire Simulator

Table of Contents
1. [Installation Intructions](#1-installation-instructions)
    1. [Windows](#11-windows)
        1. [Git](#111-git)
        2. [Visual Studio](#visual_studio_-visual-studio)
        3. [QGIS (Advanced)](#qgis_-qgis-advanced)
    2. [Linux](#12-linux)
        1. [Debian-based](#121-debian-based)
        2. [Other](#122-other)
2. [Building the Wildfire Simulator](#2-building-the-wildfire-simulator)
    1. [Basic Model](#21-basic-model)
    2. [Advanced Model](#22-advanced-model)
        1. [CMake Options](#221-cmake-options)
    3. [VSCode](#23-vscode)
3. [Using the Wildfire Simulator](#3-using-the-wildfire-simulator)
    1. [Basic Model](#31-basic-model)
    2. [Advanced Model](#32-advanced-model)
        1. [Using the CLI](#321-using-the-cli)
            1. [Viewing the Results](#3211-viewing-the-results)
        2. [Preparing Maps](#322-preparing-maps)
        3. [Installing the Plugin](#323-installing-the-plugin)
        4. [Simulating](#324-simulating)
4. [Other](#4-other)
    1. [Enabling Hidden Folders on Windows](#41-enabling-hidden-folders-on-windows)

## 1. Installation Instructions

The wildfire simulator requires several dependencies:
- Git
- C++ compiler
- CMake
- QGIS (advanced model)

For detailed instructions on installing these dependencies, please navigate to the platform-specific installation section.

### 1.1 Windows

#### 1.1.1 Git

1. In your browser of choice, enter and navigate to the following link: https://git-scm.com/downloads

2. Click on the Windows download button

![Git for Windows](doc/git_2.png)

3. Click on the 64-bit Git for Windows setup button

![Git for Windows](doc/git_3.png)

4. Run the Git installer located in your Downloads folder (double-click on the file)

![Git for Windows](doc/git_4.png)

5. Click Next in the installer window

![Git for Windows](doc/git_5.png)

6. Click Next in the installer window (optionally change the installation path)

![Git for Windows](doc/git_6.png)

7. Click Next in the installer window (optionally check additional options)

![Git for Windows](doc/git_7.png)

8. Click Next in the installer window

![Git for Windows](doc/git_8.png)

9. Click Next in the installer window (optionally change your editor preference)

![Git for Windows](doc/git_9.png)

10. Click Next in the installer window (optionally change your default branch name)

![Git for Windows](doc/git_10.png)

11. Click Next in the installer window

![Git for Windows](doc/git_11.png)

12. Click Next in the installer window

![Git for Windows](doc/git_12.png)

13. Click Next in the installer window

![Git for Windows](doc/git_13.png)

14. Click Next in the installer window

![Git for Windows](doc/git_14.png)

15. Click Next in the installer window

![Git for Windows](doc/git_15.png)

16. Click Next in the installer window

![Git for Windows](doc/git_16.png)

17. Click Next in the installer window

![Git for Windows](doc/git_17.png)

18. Click Install in the installer window

![Git for Windows](doc/git_18.png)

19. Click Finish in the installer window

![Git for Windows](doc/git_19.png)

#### 1.1.2 Visual Studio

1. Navigate to the following link and download the Community edition of Visual Studio: https://visualstudio.microsoft.com/downloads/

![](doc/visual_studio_1.png)

2. When the download finishes, run the installer and press "Continue"

![](doc/visual_studio_2.png)

3. Once the next download finishes, press "Modify"

![](doc/visual_studio_3.png)

4. Ensure "Desktop development with C++" is selected, then press "Install while downloading"

![](doc/visual_studio_4.png)

5. In the Windows search, type in "Environment Variables" and press "Edit the system environment variables"

![](doc/visual_studio_5.png)

6. Press "Environment Variables"

![](doc/visual_studio_6.png)

7. Under "System variables", press "Path" followed by "Edit"

![](doc/visual_studio_7.png)

8. Press "New" and enter the following path. Afterwards, press "Ok"
```
C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin
```

![](doc/visual_studio_8.png)

9. Press "Ok"

![](doc/visual_studio_9.png)

10. Press "Ok"

![](doc/visual_studio_10.png)

11. To verify your installation, open a new shell and type "cmake". You should see something like the following

![](doc/visual_studio_11.png)

#### 1.1.3 QGIS (Advanced)

1. Navigate to the following link and click "Skip it and go to download": https://qgis.org/download/

![](doc/qgis_1.png)

2. Press "Long Term Version for Windows (3.40 LTR)"

![](doc/qgis_2.png)

3. When the download finishes, run the installer and press "Next"

![](doc/qgis_3.png)

4. Check "I accept the terms in the License Agreement" and press "Next"

![](doc/qgis_4.png)

5. Press "Next"

![](doc/qgis_5.png)

6. Press "Install"

![](doc/qgis_6.png)

7. Press on the administrative access icon and press "Yes"

![](doc/qgis_7.png)

7. Press "Finish"

![](doc/qgis_8.png)

9. To verify your installation, type in "QGIS" the Windows search. You should see something like the following

![](doc/qgis_9.png)

### 1.2 Linux

### 1.2.1 Debian-based

For Debian-based systems (Debian, Ubuntu, Linux-mint, etc), run the following command:

> NOTE: You must have sudo. If you do not, ask your Linux adminstrator for permissions or to install the packages

```bash
sudo apt-get install git cmake g++
```

### 1.2.2 Other

For other Linux distributions, refer to the package manager of your platform

> TODO: QGIS

## 2. Building the Wildfire Simulator

Open a Powershell or Bash instance.
Download the simulator to the directory of your choosing:

```
git clone https://github.com/jsoulier/wildfire_simulator --recurse-submodules
```

Navigate to the newly cloned directory

```
cd wildfire_simulator
```

You should see the following files:

```pwsh
$ ls -l
total 6008
drwxr-xr-x 1 jaans 197610       0 Mar  8 14:24 advanced/
drwxr-xr-x 1 jaans 197610       0 Mar  8 14:24 basic/
-rw-r--r-- 1 jaans 197610 5006260 Mar  8 14:24 cadmium_installation_manual.pdf
drwxr-xr-x 1 jaans 197610       0 Mar  8 14:24 doc/
-rw-r--r-- 1 jaans 197610 1045733 Mar  8 14:24 elevation_specification.pdf
-rw-r--r-- 1 jaans 197610   85387 Mar  8 14:24 land_specification.pdf
-rw-r--r-- 1 jaans 197610    3776 Mar  8 14:28 README.md
```

Proceed with the [basic](#21-basic-model) and/or [advanced](#22-advanced-model) model.

### 2.1 Basic Model

> TODO:

### 2.2 Advanced Model

### 2.2.3 Building

Navigate to the advanced directory

```pwsh
cd advanced
```

Create to folder to build from and enter that folder

```pwsh
mkdir build
cd build
```

Run the CMake generator. You should see output similar to the following (may vary based on platform)

```pwsh
cmake ..
```

![](doc/advanced_building_1.png)

Run the CMake build command. You should see output similar to the following (may vary based on platform).
You can safely ignore any warnings.

```pwsh
cmake --build .
```

![](doc/advanced_building_2.png)

You should now see the following files under `bin/`. (pdb is Windows debug builds only)

```pwsh
$ ls -l bin
total 12116
-rwxr-xr-x 1 jaans 197610  1455616 Mar  8 14:36 wildfire_simulator.exe*
-rw-r--r-- 1 jaans 197610 10948608 Mar  8 14:36 wildfire_simulator.pdb
```

#### 2.2.1 CMake Options

For better performance, you may want to produce a release mode build (with `-O3`).
With single-config generators (Makefiles, Ninja), use the following commands instead.

```pwsh
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

With multi-config generators (Visual Studio, XCode), use the following commands instead.

```pwsh
cmake ..
cmake --build . --config Release
```

For faster build times, you can run a CMake build across multiple threads.
You can do this with the following option (and replace 8 with your desired number of threads).

```pwsh
cmake --build . --parallel 8
```

### 2.3 VSCode

For instructions on installing VSCode, see the [Cadmium Installation Manual](cadmium_installation_manual.pdf)

> TODO: Show how it can be easier to build through VSCode and CMake Tools

## 3. Using the Wildfire Simulator

### 3.1 Basic Model

### 3.2 Advanced Model

#### 3.2.1 Using the CLI

> TODO: Revisit when we add the slider for moisture parameters

The advanced model takes in JSON in the following schema:

```json
{
    "cells": {
        "default": {
            "delay": "inertial"
        },
        // coordinates
        "480478_5091045": {
            // coordinates of neighbouring cells
            "neighborhood": {
                "480428_5091073": 50,
                "480478_5091101": 50,
                "480528_5091073": 50
            },
            "state": {
                // slope of the cell (degrees)
                "slope": 26.935840606689453,
                // direction of slope (degrees)
                "aspect": 255.75865173339844,
                // fuel model numbers (internal to behave)
                "fuelModelNumber": 9,
                // direction of wind (degrees)
                "windDirection": 90,
                // speed of wind (meters per minute)
                "windSpeed": 30,
                // if the cell is initially ignited
                "ignited": false
            }
        },
        // ...
    }
}
```

After providing the model with the JSON data, it will output results as CSV.
The CSV contains the location and time of ignited cells.

```csv
time,x,y,ignited
1969-12-31 19:00:00,481978,5094013,1
1969-12-31 19:00:00,481978,5094013,1
1969-12-31 21:48:22,482028,5094041,1
1969-12-31 21:48:23,482078,5094013,1
// ...
```

You can invoke the advanced model with the following:

```
./<path>/wildfire_plugin.exe <in JSON path> <out CSV path>
```

From the advanced/ directory, run the following:

```bash
./build/bin/wildfire_simulator.exe samples/map.json results.csv
```

The simulation will now run for a while.
You should see a file called results.csv in your current directory.
You can view the current results at any time by opening it.
You can cancel the simulation at any time by pressing Left Control and C at the same time.

#### 3.2.1.1 Viewing the Results

> NOTE: The following steps are automated using the plugin. Skip to 3.2.2 to continue with plugin steps

1. It is difficult to analyze the results by reading the CSV. Instead, open QGIS.

![](doc/viewing_1.png)

2. Press "Layer", "Add Layer", "Add Raster Layer" to open the Data Source Manager

![](doc/viewing_2.png)

3. Press "File" and the triple dots

![](doc/viewing_3.png)

4. Navigate to advanced/samples and select the file with the .tif extension.
Afterwards, press "Open"

![](doc/viewing_4.png)

5. Press "Add"

![](doc/viewing_5.png)

6. You should now see a rectangular map on screen

![](doc/viewing_6.png)

7. Press "Layer", "Add Layer", "Add Delimited Text Layer"

![](doc/viewing_7.png)

8. Select the triple dots

![](doc/viewing_8.png)

9. Select results.csv and press "Open"

![](doc/viewing_9.png)

10. Select the "Geometry Definition" pulldown and the "Geometry CRS" selector to open the Coordinate Reference System Selector
> NOTE: These are steps you may only have to do once.
If the Add button is not grayed-out, you can proceed with 12.

![](doc/viewing_10.png)

11. In the Filter, type "2959" and select it under the Predefined Coordinate Reference Systems panel.
Afterwards, press "Ok"

![](doc/viewing_11.png)

12. Press "Add"

![](doc/viewing_12.png)

13. You should now see an overlay of dots on the map (it may be a different colour for you).

![](doc/viewing_13.png)

14. Right click on results under the Layers panel and select "Properties"

![](doc/viewing_14.png)

15. Press on "Temporal" and use the following settings:
- Enabled "Dynamic Temporal Control"
- Set configuration to "Single Field with Date/Time"
- Set Field to "time"
- Enabled "Accumulate features over time"
Afterwards, press "Ok"
> NOTE: The points will disappear from the map

![](doc/viewing_15.png)

16. Press on the "Temporal Controller Panel"

![](doc/viewing_16.png)

17. In the Temporal Controller panel, use the following settings:
- Use "Animated temporal navigation"
- Press "Set to Full Range"
- Use "seconds"

![](doc/viewing_17.png)

18. Use the slider to change the current time in the simulation.
You should see when the slider is zero, there are very few points.
The points should spread outwards as you increase the slider.

![](doc/viewing_18.png)

#### 3.2.2 Preparing Maps

> NOTE: The government servers can be __very__ slow at times.
You can grab some sample maps from here: https://github.com/jsoulier/wildfire_simulator/releases/tag/v0.1.
Download the files with the .tif extension (landcover and dtm). Afterwards, proceed from step 7.

1. To install a land cover map of Canada, navigate to the following link and press "Explore" followed by "Go to resource":
https://open.canada.ca/data/en/dataset/ee1580ab-a23d-4f86-a09b-79763677eb47. The downloaded map will contain the entirety of Canada

![](doc/maps_1.png)

2. To install an elevation map of Canada, navigate to the following link and press "Explore" followed by "Go to resource":
https://open.canada.ca/data/en/dataset/957782bf-847c-4644-a757-e383c0057995

![](doc/maps_2.png)

3. Press on "1m" for 1 meter resolution maps

![](doc/maps_3.png)

4. Press on the region of your choosing. In the following image, we choose Quebec (QC)

![](doc/maps_4.png)

5. Press on the region of your choosing. In the following image, we choose Riviere Gatineau (#1)

![](doc/maps_5.png)

6. Press on any dtm (digital terrain elevation) maps to download them. We chose the first one

![](doc/maps_6.png)

7. After everything has finished download, launch QGIS

![](doc/maps_7.png)

8. Press "Layer", "Add Layer", "Add Raster Layer" to open the Data Source Manager

![](doc/maps_8.png)

9. Press "File" and the triple dots

![](doc/maps_9.png)

10. Press the downloaded files (land cover, dtm) in your file explorer and press "Open"

> NOTE: These instructions are specific to the Windows 11 file explorer. It will look slightly different other platforms

> NOTE: You can select multiple files by holding down Left Control and left clicking on the files

![](doc/maps_10.png)

11. Press "Add"

![](doc/maps_11.png)

12. You may see the following window. If you do, press "Ok"

![](doc/maps_12.png)

13. Close the Data Source Manager

![](doc/maps_13.png)

14. You should see 2 maps under the Layers panel on the left and a coloured map of Canada

![](doc/maps_14.png)

15. Right click on the dtm map in the Layers panel and press "Zoom to Layer(s)".
You should see something similar to the following

> NOTE: You may also need to press "Move to Top". If the option is not visible, ignore

![](doc/maps_15.png)

16. The land cover map is approximately 2 gigabytes.
You'll need to crop the map to use it for simulation to avoid running out of memory.
Press "Raster", "Extraction", "Clip Raster by Extent"

![](doc/maps_16.png)

17. For the Input layer, press the pulldown and the land cover map

![](doc/maps_17.png)

18. For the Clipping extent, press the pulldown followed by "Calculate from layer" and the dtm map

![](doc/maps_18.png)

19. Optionally save the clipped map to a file

![](doc/maps_19.png)

20. Press "Run"

![](doc/maps_20.png)

21. You should now see a new map in the Layers panel

> NOTE: If you saved to a file, you may to refer to step 8 to load it

![](doc/maps_21.png)

22. Hide the old land cover map by toggling its visibility.
If you zoom out, you should now see a similar land cover map but constrained to the size of the dtm map.

> NOTE: You can zoom by holding Left Control and scrolling with your mouse wheel

> NOTE: You may need to bring the dtm map to the front by right clicking in the Layers panel and pressing "Move to Top"

![](doc/maps_22.png)

#### 3.2.3 Installing the Plugin

> TODO: Linux instructions will be different

1. In the Windows search, type in "OSGeo Shell" and press "OSGeo4W Shell"

![](doc/installing_plugin_1.png)

2. In the shell, type "python -m pip install rasterio".
You can close the shell afterwards

![](doc/installing_plugin_2.png)

3. Open your file explorer and navigate to the advanced directory.
You should see a folder called "wildfire_simulator_plugin".
Click on the folder and press Left Control and C and the same time to copy to your clipboard.

![](doc/installing_plugin_3.png)

4. Navigate to the following directory:
```bash
C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python
```
> NOTE: You will need to modify the path according to your username

> NOTE: You may want to enable hidden folders.
See [Enabling Hidden Folders on Windows](#41-enabling-hidden-folders-on-windows) for details

![](doc/installing_plugin_4.png)

5. Right click in the folder view and select "New" and "Folder".
Name the folder "plugins"

> NOTE: If you already see a directory called "plugins", you can skip and continue with step 6.

> TODO: Windows won't let me take a screen shot of the "New" and "Folder" steps

![](doc/installing_plugin_5.png)

6. Navigate to the plugins folder and press Left Control and V at the same time to copy the plugin

![](doc/installing_plugin_6.png)

7. Start QGIS. If you are already running it, restart it.

8. To verify the rasterio installation, press "Plugins" and "Python Console".
In the Python Console, type "import rasterio".
You should see no errors

![](doc/installing_plugin_7.png)
![](doc/installing_plugin_8.png)

9. Press "Plugins", "Manage and Install Plugins"

![](doc/installing_plugin_9.png)

10. In the Plugins window, type "wildfire" and check the Wildfire Simulator plugin

![](doc/installing_plugin_10.png)

#### 3.2.4 Simulating

> Todo

## 4. Other

### 4.1 Enabling Hidden Folders on Windows

1. Open your File Explorer and click on "See More" (triple dots) and "Options"

![](doc/hidden_folders_1.png)

2. In the Folder Options window, press "View", "Show hidden files, folders, and drives", and "Ok"

![](doc/hidden_folders_2.png)

3. If you navigate to your home directory (C:\Users\<username>), you should now see an AppData directory

![](doc/hidden_folders_3.png)