cmake_minimum_required(VERSION 3.22)
project(project)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/bin)

# For behave includes
# add_compile_options(-Wno-write-strings)

add_subdirectory(${CMAKE_SOURCE_DIR}/lib/behave)
add_subdirectory(${CMAKE_SOURCE_DIR}/lib/cadmium)

file(GLOB SRC ${CMAKE_SOURCE_DIR}/src/*)
add_executable(${PROJECT_NAME} ${SRC})
target_link_libraries(${PROJECT_NAME} PUBLIC cadmium behave_lib)

include_directories(C:/OSGeo4W/apps/qgis/include)
include_directories(C:/OSGeo4W/apps/Qt5/include/QtCore)
include_directories(C:/OSGeo4W/apps/Qt5/include/QtGui)
include_directories(C:/OSGeo4W/apps/Qt5/include/QtWidgets)
include_directories(C:/OSGeo4W/apps/Qt5/include)
target_link_libraries(${PROJECT_NAME} PUBLIC C:/OSGeo4W/apps/qgis/lib/qgis_3d.lib)
target_link_libraries(${PROJECT_NAME} PUBLIC C:/OSGeo4W/apps/qgis/lib/qgis_gui.lib)
target_link_libraries(${PROJECT_NAME} PUBLIC C:/OSGeo4W/apps/qgis/lib/qgis_core.lib)
target_link_libraries(${PROJECT_NAME} PUBLIC C:/OSGeo4W/apps/Qt5/lib/Qt5Core.lib)
target_link_libraries(${PROJECT_NAME} PUBLIC C:/OSGeo4W/apps/Qt5/lib/Qt5Gui.lib)
target_link_libraries(${PROJECT_NAME} PUBLIC C:/OSGeo4W/apps/Qt5/lib/Qt5Widgets.lib)

configure_file(C:/OSGeo4W/apps/qgis/bin/qgis_3d.dll ${CMAKE_BINARY_DIR}/bin COPYONLY)
configure_file(C:/OSGeo4W/apps/qgis/bin/qgis_gui.dll ${CMAKE_BINARY_DIR}/bin COPYONLY)
configure_file(C:/OSGeo4W/apps/qgis/bin/qgis_core.dll ${CMAKE_BINARY_DIR}/bin COPYONLY)
configure_file(C:/OSGeo4W/apps/Qt5/bin/Qt5Core.dll ${CMAKE_BINARY_DIR}/bin COPYONLY)
configure_file(C:/OSGeo4W/apps/Qt5/bin/Qt5Gui.dll ${CMAKE_BINARY_DIR}/bin COPYONLY)
configure_file(C:/OSGeo4W/apps/Qt5/bin/Qt5Widgets.dll ${CMAKE_BINARY_DIR}/bin COPYONLY)

# Ensure the "platforms" directory exists inside the binary output
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/bin/platforms)

# Copy the platform plugin(s)
configure_file(C:/OSGeo4W/apps/Qt5/plugins/platforms/qwindows.dll ${CMAKE_BINARY_DIR}/bin/platforms/qwindows.dll COPYONLY)


target_compile_options(${PROJECT_NAME} PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/Za>)
