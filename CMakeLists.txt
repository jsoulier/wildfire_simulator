cmake_minimum_required(VERSION 3.22)
project(capstone)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(BINARY_DIR ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${BINARY_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${BINARY_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${BINARY_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG ${BINARY_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${BINARY_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${BINARY_DIR})
make_directory(${BINARY_DIR})

set(OSGEO_DIR "C:/OSGeo4W")

file(GLOB SRC ${CMAKE_SOURCE_DIR}/src/*)
file(GLOB RES ${CMAKE_SOURCE_DIR}/res/*)
file(GLOB QGIS_DLLS ${OSGEO_DIR}/apps/qgis/bin/*)
file(GLOB QT_DLLS ${OSGEO_DIR}/apps/Qt5/bin/*)
file(GLOB QT_PLUGINS ${OSGEO_DIR}/apps/Qt5/plugins/*)

list(APPEND CMAKE_MODULE_PATH ${OSGEO_DIR}/apps/Qt5/lib/cmake/Qt5)
find_package(Qt5 COMPONENTS Core Gui Widgets Xml REQUIRED)
add_subdirectory(${CMAKE_SOURCE_DIR}/lib/behave)
add_subdirectory(${CMAKE_SOURCE_DIR}/lib/cadmium)

add_executable(${PROJECT_NAME} ${SRC})

# QGIS provides their own json_fwd.hpp
target_include_directories(${PROJECT_NAME} BEFORE PUBLIC
    ${CMAKE_SOURCE_DIR}/lib/cadmium/json/include)

target_link_libraries(${PROJECT_NAME}
    cadmium
    behave_lib
    Qt5::Core
    Qt5::Gui
    Qt5::Widgets
    Qt5::Xml
    ${OSGEO_DIR}/apps/qgis/lib/qgis_core.lib
    ${OSGEO_DIR}/apps/qgis/lib/qgis_gui.lib
    ${OSGEO_DIR}/apps/qgis/lib/qgis_3d.lib)
target_include_directories(${PROJECT_NAME} PRIVATE
    ${Qt5Core_INCLUDE_DIRS}
    ${Qt5Gui_INCLUDE_DIRS}
    ${Qt5Widgets_INCLUDE_DIRS}
    ${Qt5Xml_INCLUDE_DIRS}
    ${CMAKE_SOURCE_DIR}/lib/behave/src)

target_compile_definitions(${PROJECT_NAME} PRIVATE
    _USE_MATH_DEFINES)
target_compile_definitions(${PROJECT_NAME} PRIVATE
    _SILENCE_ALL_MS_EXT_DEPRECATION_WARNINGS)

foreach(PATH ${RES})
    get_filename_component(NAME ${PATH} NAME)
    configure_file(${PATH} ${BINARY_DIR}/${NAME} COPYONLY)
endforeach()
foreach(PATH ${QGIS_DLLS})
    get_filename_component(NAME ${PATH} NAME)
    configure_file(${PATH} ${BINARY_DIR}/${NAME} COPYONLY)
endforeach()
foreach(PATH ${QT_DLLS})
    get_filename_component(NAME ${PATH} NAME)
    configure_file(${PATH} ${BINARY_DIR}/${NAME} COPYONLY)
endforeach()
foreach(PATH ${QT_PLUGINS})
    file(COPY ${PATH} DESTINATION ${BINARY_DIR})
endforeach()