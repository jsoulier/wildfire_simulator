# Wildfire Simulator

## Instructions

### **Building the Project**
Before proceeding, ensure that you have read the primary [README file](../README.md) in the project directory to install all required dependencies.

1. Create a build directory:
   ```sh
   mkdir build
   ```
2. Navigate into the build directory:
   ```sh
   cd build
   ```
3. Run CMake to configure the project:
   ```sh
   cmake ..
   ```
4. Build the project:
   ```sh
   cmake --build . --config Release
   ```

### **Running the Simulation**
Once the executable is built, navigate to the `bin` directory:
   ```sh
   cd bin
   ```
Run the wildfire simulation using the sample configuration file:
   ```sh
   ./wildfire_simulator.exe ../../samples/grid_config.json
   ```

### **Output and Visualization**
- The output CSV file will be saved in the `bin` folder, alongside the `.exe` file.
- To visualize the results, visit:
  [Cell-DEVS Viewer](https://devssim.carleton.ca/cell-devs-viewer/)
- Upload both the **output CSV file** and the **input JSON configuration file** to visualize the simulation on a grid.

---
