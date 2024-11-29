// #include <QApplication>
// #include <QMainWindow>

// #include <qgsapplication.h>
// #include <qgsmapcanvas.h>
// #include <qgsvectorlayer.h>
// #include <qgsproject.h>

// #include "state.hpp"
// #include "cell.hpp"

// int main(int argc, char *argv[])
// {
    // Initialize the Qt application
    // QApplication app(argc, argv);

    // // Initialize QGIS application
    // QgsApplication qgisApp(argc, argv, true);

    // // Set QGIS application path
    // QgsApplication::setPrefixPath("/path/to/qgis", true);
    // QgsApplication::initQgis();

    // // Create a main window to hold the map canvas
    // QMainWindow mainWindow;

    // // Create a map canvas
    // QgsMapCanvas *mapCanvas = new QgsMapCanvas(&mainWindow);
    // mapCanvas->setCanvasColor(Qt::white);

    // // Create a vector layer (e.g., shapefile)
    // QString layerPath = "lpr_000b21a_e.shp";
    // QString layerName = "Sample Layer";
    // QString providerName = "ogr";

    // QgsVectorLayer *vectorLayer = new QgsVectorLayer(layerPath, layerName, providerName);

    // if (!vectorLayer->isValid()) {
    //     qDebug() << "Failed to load the layer!";
    //     return -1;
    // }

    // // Add the layer to the project
    // QgsProject::instance()->addMapLayer(vectorLayer);

    // // Set the layer to the map canvas
    // mapCanvas->setLayers({ vectorLayer });
    // mapCanvas->setExtent(vectorLayer->extent());
    // mapCanvas->refresh();

    // // Show the main window
    // mainWindow.setCentralWidget(mapCanvas);
    // mainWindow.resize(800, 600);
    // mainWindow.show();

    // // Execute the application
    // int result = app.exec();

    // // Cleanup QGIS resources
    // QgsApplication::exitQgis();

    // return 0;
// }


#include <cadmium/celldevs/grid/coupled.hpp>
#include <cadmium/core/logger/csv.hpp>
#include <cadmium/core/simulation/root_coordinator.hpp>
#include <chrono>
#include <fstream>
#include <string>
#include "cell.hpp"
#include "state.hpp"

std::shared_ptr<cadmium::celldevs::GridCell<State, double>> addGridCell(const cadmium::celldevs::coordinates & cellId, const std::shared_ptr<const cadmium::celldevs::GridCellConfig<State, double>>& cellConfig) {
	auto cellModel = cellConfig->cellModel;
	if (cellModel == "default" || cellModel == "") {
		return std::make_shared<GridCell>(cellId, cellConfig);
	} else {
		throw std::bad_typeid();
	}
}

int main(int argc, char ** argv) {
	if (argc < 2) {
		std::cout << "Program used with wrong parameters. The program must be invoked as follows:";
		std::cout << argv[0] << " SCENARIO_CONFIG.json [MAX_SIMULATION_TIME (default: 500)]" << std::endl;
		return -1;
	}
	std::string configFilePath = argv[1];
	double simTime = (argc > 2)? std::stod(argv[2]) : 500;
	auto paramsProcessed = std::chrono::high_resolution_clock::now();

	auto model = std::make_shared<cadmium::celldevs::GridCellDEVSCoupled<State, double>>("sir", addGridCell, configFilePath);
	model->buildModel();
	auto modelGenerated = std::chrono::high_resolution_clock::now();
	std::cout << "Model creation time: " << std::chrono::duration_cast<std::chrono::duration<double, std::ratio<1>>>( modelGenerated - paramsProcessed).count() << " seconds" << std::endl;

	modelGenerated = std::chrono::high_resolution_clock::now();
	auto rootCoordinator = cadmium::RootCoordinator(model);
	auto logger = std::make_shared<cadmium::CSVLogger>("grid_log.csv", ";");
	rootCoordinator.setLogger(logger);
	rootCoordinator.start();
	auto engineStarted = std::chrono::high_resolution_clock::now();
	std::cout << "Engine creation time: " << std::chrono::duration_cast<std::chrono::duration<double, std::ratio<1>>>(engineStarted - modelGenerated).count() << " seconds" << std::endl;

	engineStarted = std::chrono::high_resolution_clock::now();
	rootCoordinator.simulate(simTime);
	auto simulationDone =  std::chrono::high_resolution_clock::now();
	std::cout << "Simulation time: " << std::chrono::duration_cast<std::chrono::duration<double, std::ratio<1>>>(simulationDone - engineStarted).count() << " seconds" << std::endl;
	rootCoordinator.stop();
}