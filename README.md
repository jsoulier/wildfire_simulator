# Wildfire Simulator

Table of Contents
1. [Installation Intructions](#1-installation-instructions)
    1. [Windows](#11-windows)
        1. [Git](#111-git)
        2. [Visual Studio](#112-visual-studio)
        3. [QGIS (Advanced Setup)](#113-qgis-advanced-setup)
    2. [Linux](#12-linux)
        1. [Debian-based](#121-debian-based)
        2. [Other](#122-other)
2. [Building the Wildfire Simulator](#2-building-the-wildfire-simulator)
    1. [Basic Setup](#21-basic-setup)
    2. [Advanced Setup](#22-advanced-setup)
        1. [CMake Options](#221-cmake-options)
    3. [VSCode](#23-vscode)
3. [Using the Wildfire Simulator](#3-using-the-wildfire-simulator)
    1. [Basic Model](#31-basic-model)
    2. [Advanced Model](#32-advanced-model)
        1. [Preparing Maps](#321-preparing-maps)
        2. [Simulating](#322-simulating)

## 1. Installation Instructions

The widlfire simulator requires several dependencies:
- Git
- C++ compiler
- CMake
- QGIS (advanced setup)

For detailed instructions on installing these dependencies, please navigate to the platform-specific installation section.

### 1.1 Windows

#### 1.1.1 Git

1. In your browser of choice, enter and navigate to the following link: https://git-scm.com/downloads

2. Click on the Windows download button

![Git for Windows](doc/111_git_2.png)

3. Click on the 64-bit Git for Windows setup button

![Git for Windows](doc/111_git_3.png)

4. Run the Git installer located in your Downloads folder (double-click on the file)

![Git for Windows](doc/111_git_4.png)

5. Click Next in the installer window

![Git for Windows](doc/111_git_5.png)

6. Click Next in the installer window (optionally change the installation path)

![Git for Windows](doc/111_git_6.png)

7. Click Next in the installer window (optionally check additional options)

![Git for Windows](doc/111_git_7.png)

8. Click Next in the installer window

![Git for Windows](doc/111_git_8.png)

9. Click Next in the installer window (optionally change your editor preference)

![Git for Windows](doc/111_git_9.png)

10. Click Next in the installer window (optionally change your default branch name)

![Git for Windows](doc/111_git_10.png)

11. Click Next in the installer window

![Git for Windows](doc/111_git_11.png)

12. Click Next in the installer window

![Git for Windows](doc/111_git_12.png)

13. Click Next in the installer window

![Git for Windows](doc/111_git_13.png)

14. Click Next in the installer window

![Git for Windows](doc/111_git_14.png)

15. Click Next in the installer window

![Git for Windows](doc/111_git_15.png)

16. Click Next in the installer window

![Git for Windows](doc/111_git_16.png)

17. Click Next in the installer window

![Git for Windows](doc/111_git_17.png)

18. Click Install in the installer window

![Git for Windows](doc/111_git_18.png)

19. Click Finish in the installer window

![Git for Windows](doc/111_git_19.png)

#### 1.1.2 Visual Studio

1. Navigate to the following link and download the Community edition of Visual Studio: https://visualstudio.microsoft.com/downloads/

![](doc/1121.png)

2. When the download finishes, run the installer and press "Continue"

![](doc/1122.png)

3. Once the next download finishes, press "Modify"

![](doc/1123.png)

4. Ensure "Desktop development with C++" is selected, then press "Install while downloading"

![](doc/1124.png)

5. In the Windows search, type in "Environment Variables" and press "Edit the system environment variables"

![](doc/1125.png)

6. Press "Environment Variables"

![](doc/1126.png)

7. Under "System variables", press "Path" followed by "Edit"

![](doc/1127.png)

8. Press "New" and enter the following path. Afterwards, press "Ok"
```
C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin
```

![](doc/1128.png)

9. Press "Ok"

![](doc/1129.png)

10. Press "Ok"

![](doc/11210.png)

11. To verify your installation, open a new shell and type "cmake". You should see something like the following

![](doc/11211.png)

#### 1.1.3 QGIS (Advanced Setup)

1. Navigate to the following link and click "Skip it and go to download": https://qgis.org/download/

![](doc/1131.png)

2. Press "Long Term Version for Windows (3.40 LTR)"

![](doc/1132.png)

3. When the download finishes, run the installer and press "Next"

![](doc/1133.png)

4. Check "I accept the terms in the License Agreement" and press "Next"

![](doc/1134.png)

5. Press "Next"

![](doc/1135.png)

6. Press "Install"

![](doc/1136.png)

7. Press on the administrative access icon and press "Yes"

![](doc/1137.png)

7. Press "Finish"

![](doc/1138.png)

9. To verify your installation, type in "QGIS" the Windows search. You should see something like the following

![](doc/1139.png)

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

Proceed with the [basic](#21-basic-setup) and/or [advanced](#22-advanced-setup) setup.

### 2.1 Basic Setup

> TODO:

### 2.2 Advanced Setup

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

![](doc/221.png)

Run the CMake build command. You should see output similar to the following (may vary based on platform).
You can safely ignore any warnings.

```pwsh
cmake --build .
```

![](doc/222.png)

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

#### 3.2.1 Preparing Maps

> The government servers can be __very__ slow at times. You can grab some sample maps from here and continue from step 7: https://github.com/jsoulier/wildfire_simulator/releases/tag/v0.1

1. To install a land cover map of Canada, navigate to the following link and press "Explore" followed by "Go to resource":
https://open.canada.ca/data/en/dataset/ee1580ab-a23d-4f86-a09b-79763677eb47. The downloaded map will contain the entirety of Canada

![](doc/3211.png)

2. To install an elevation map of Canada, navigate to the following link and press "Explore" followed by "Go to resource":
https://open.canada.ca/data/en/dataset/957782bf-847c-4644-a757-e383c0057995

![](doc/3212.png)

3. Press on "1m" for 1 meter resolution maps

![](doc/3213.png)

4. Press on the region of your choosing. In the following image, we choose Quebec (QC)

![](doc/3214.png)

5. Press on the region of your choosing. In the following image, we choose Riviere Gatineau (#1)

![](doc/3215.png)

6. Press on any dtm (digital terrain elevation) maps to download them. We chose the first one

![](doc/3216.png)

7. After everything has finished download, launch QGIS

![](doc/3217.png)

8. Press "Layer", "Add Layer", "Add Raster Layer" to open the Data Source Manager

![](doc/3218.png)

9. Press "File" and the triple dots

![](doc/3219.png)

10. Press the downloaded files (land cover, dtm) in your file explorer and press "Open"

> These instructions are specific to the Windows 11 file explorer. It will look slightly different other platforms

> You can select multiple files by holding down Left Control and left clicking on the files

![](doc/32110.png)

11. Press "Add"

![](doc/32111.png)

12. You may see the following window. If you do, press "Ok"

![](doc/32112.png)

13. Close the Data Source Manager

![](doc/32113.png)

14. You should see 2 maps under the Layers panel on the left and a coloured map of Canada

![](doc/32114.png)

15. Right click on the dtm map in the Layers panel and press "Zoom to Layer(s)".
You should see something similar to the following

> You may also need to press "Move to Top". If the option is not visible, ignore

![](doc/32115.png)

16. The land cover map is approximately 2 gigabytes.
You'll need to crop the map to use it for simulation to avoid running out of memory.
Press "Raster", "Extraction", "Clip Raster by Extent"

![](doc/32116.png)

17. For the Input layer, press the pulldown and the land cover map

![](doc/32117.png)

18. For the Clipping extent, press the pulldown followed by "Calculate from layer" and the dtm map

![](doc/32118.png)

19. Optionally save the clipped map to a file

![](doc/32119.png)

20. Press "Run"

![](doc/32120.png)

21. You should now see a new map in the Layers panel

> If you saved to a file, you may to refer to step 8 to load it

![](doc/32121.png)

22. Hide the old land cover map by toggling its visibility.
If you zoom out, you should now see a similar land cover map but constrained to the size of the dtm map.

> You can zoom by holding Left Control and scrolling with your mouse wheel

![](doc/32122.png)

#### 3.2.2 Simulating

> Todo