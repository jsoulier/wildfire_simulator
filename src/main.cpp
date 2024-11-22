#include <QApplication>
#include <QMainWindow>
#include <qgis_gui.h>
#include <qgis_core.h>
#include <qgsapplication.h>

int main(int argc, char** argv)
{
    // Initialize the Qt application
    QApplication app(argc, argv);

    // Initialize QGIS resources
    QgsApplication qgisApp(argc, argv, true);

    // Set the QGIS prefix path (adjust this to your installation path)
    QgsApplication::setPrefixPath("C:/OSGeo4W/apps/qgis-dev", true);

    // Initialize QGIS
    QgsApplication::init();

    // Create a main window for the GUI
    QMainWindow mainWindow;
    mainWindow.setWindowTitle("Minimal QGIS GUI Example");
    mainWindow.resize(800, 600);
    mainWindow.show();

    // Run the application
    int result = app.exec();

    // Cleanup QGIS resources
    QgsApplication::exitQgis();

    return result;
}