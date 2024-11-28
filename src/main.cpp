#include <QApplication>
#include <QMainWindow>

#include <qgsapplication.h>
#include <qgsmapcanvas.h>
#include <qgsvectorlayer.h>
#include <qgsproject.h>

int main(int argc, char *argv[])
{
    // Initialize the Qt application
    QApplication app(argc, argv);

    // Initialize QGIS application
    QgsApplication qgisApp(argc, argv, true);

    // Set QGIS application path
    QgsApplication::setPrefixPath("/path/to/qgis", true);
    QgsApplication::initQgis();

    // Create a main window to hold the map canvas
    QMainWindow mainWindow;

    // Create a map canvas
    QgsMapCanvas *mapCanvas = new QgsMapCanvas(&mainWindow);
    mapCanvas->setCanvasColor(Qt::white);

    // Create a vector layer (e.g., shapefile)
    QString layerPath = "lpr_000b21a_e.shp";
    QString layerName = "Sample Layer";
    QString providerName = "ogr";

    QgsVectorLayer *vectorLayer = new QgsVectorLayer(layerPath, layerName, providerName);

    if (!vectorLayer->isValid()) {
        qDebug() << "Failed to load the layer!";
        return -1;
    }

    // Add the layer to the project
    QgsProject::instance()->addMapLayer(vectorLayer);

    // Set the layer to the map canvas
    mapCanvas->setLayers({ vectorLayer });
    mapCanvas->setExtent(vectorLayer->extent());
    mapCanvas->refresh();

    // Show the main window
    mainWindow.setCentralWidget(mapCanvas);
    mainWindow.resize(800, 600);
    mainWindow.show();

    // Execute the application
    int result = app.exec();

    // Cleanup QGIS resources
    QgsApplication::exitQgis();

    return result;
}